package com.neb.ians.ui.screens.reader

import android.app.Application
import android.content.Context
import android.media.AudioManager
import android.net.Uri
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import javax.inject.Inject

data class MediaPlayerUiState(
    val resource: ApiResource? = null,
    val title: String = "",
    val isVideo: Boolean = true,
    val isLoading: Boolean = true,
    val isPlaying: Boolean = false,
    val isBuffering: Boolean = false,
    val hasError: Boolean = false,
    val errorMessage: String? = null,
    val currentTimeMs: Long = 0,
    val durationMs: Long = 0,
    val bufferedPercent: Int = 0,
    val volume: Float = 1f,
    val isMuted: Boolean = false,
    val speed: Float = 1f,
    val speedMenuOpen: Boolean = false,
    val resumePositionMs: Long = 0,
    val subjectColorArgb: Int = 0,
    val videoWidth: Int = 0,
    val videoHeight: Int = 0
)

@HiltViewModel
class MediaPlayerViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val application: Application,
    private val resourceRepository: ResourceRepository,
    private val downloadManager: ResourceDownloadManager
) : ViewModel() {

    private val initialResourceId: String = savedStateHandle.get<String>("resourceId") ?: ""
    private var activeResourceId: String = ""

    private val _uiState = MutableStateFlow(MediaPlayerUiState())
    val uiState: StateFlow<MediaPlayerUiState> = _uiState.asStateFlow()

    private var player: ExoPlayer? = null
    private var tickJob: Job? = null
    private var loadJob: Job? = null
    private var playWhenReady: Boolean = false
    private val audioManager: AudioManager =
        application.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    private val maxVolume: Int = audioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)

    companion object {
        private const val SAVE_INTERVAL_MS = 2500L
        private const val RESUME_MIN_MS = 8000L
        private const val RESUME_END_PAD_MS = 12000L
        private const val PREFS_NAME = "nmp_positions"
    }

    init {
        ensurePlayer()
        if (initialResourceId.isNotBlank()) setResource(initialResourceId)
    }

    fun setResource(resourceId: String) {
        if (resourceId.isBlank()) return
        if (activeResourceId == resourceId && _uiState.value.resource != null) return
        savePosition()
        ensurePlayer()
        stopPlayerForLoad()
        loadJob?.cancel()
        activeResourceId = resourceId
        _uiState.value = MediaPlayerUiState(isLoading = true)
        loadJob = viewModelScope.launch {
            val downloaded = downloadManager.findDownloaded(resourceId)
            val localFile = downloaded?.localPath?.let { java.io.File(it) }?.takeIf { it.exists() }
            if (downloaded != null && localFile != null) {
                if (activeResourceId != resourceId) return@launch
                val offlineResource = ApiResource(
                    id = downloaded.resourceId,
                    title = downloaded.title,
                    subject = "Downloaded",
                    gradeLevel = "",
                    type = downloaded.type,
                    fileUrl = downloaded.fileUrl,
                    thumbnailUrl = downloaded.thumbnailUrl,
                    fileSize = downloaded.sizeBytes
                )
                configureResource(
                    resource = offlineResource,
                    playableUri = Uri.fromFile(localFile).toString(),
                    mimeHint = downloaded.mimeType
                )
                return@launch
            }

            resourceRepository.getResource(resourceId)
                .onSuccess { resource ->
                    if (activeResourceId != resourceId) return@onSuccess
                    // Paid resources are gated server-side: the API returns an empty
                    // file URL for any viewer who hasn't unlocked them. Never hand
                    // ExoPlayer a blank/gated URL — surface a clear message instead
                    // of the raw "source error". (A blank URL on a paid resource is
                    // treated as locked even if a stale payload omits hasAccess.)
                    if (resource.isPaid && (resource.fileUrl.isBlank() || !resource.hasAccess)) {
                        _uiState.update {
                            it.copy(
                                isLoading = false,
                                hasError = true,
                                errorMessage = "This is paid content — purchase to unlock"
                            )
                        }
                        return@onSuccess
                    }
                    val cachedFile = downloadManager.getLocalFile(resource.id, resource.fileUrl)?.takeIf { it.exists() }
                    val playableUri = cachedFile?.let { Uri.fromFile(it).toString() } ?: resource.fileUrl
                    if (playableUri.isBlank()) {
                        _uiState.update { it.copy(isLoading = false, hasError = true, errorMessage = "No file available") }
                    } else {
                        configureResource(resource, playableUri)
                    }
                }
                .onFailure { e ->
                    if (activeResourceId != resourceId) return@onFailure
                    _uiState.update {
                        it.copy(isLoading = false, hasError = true, errorMessage = ApiErrorMapper.mapException(e))
                    }
                }
        }
    }

    private fun configureResource(resource: ApiResource, playableUri: String, mimeHint: String = "") {
        val mediaHint = "$mimeHint ${resource.type} ${resource.fileUrl} $playableUri".lowercase()
        val isVideo = mediaHint.contains("video/") || listOf(".mp4", ".webm", ".mkv", ".mov", ".m4v", ".avi", ".ogv")
            .any(mediaHint::contains)
        val subjectColor = com.neb.ians.util.getSubjectColor(
            resource.subject.split(",").firstOrNull()?.trim().orEmpty()
        )
        val prefs = application.getSharedPreferences(PREFS_NAME, 0)
        val resumeMs = prefs.getLong("pos_$activeResourceId", 0L)
        val savedSpeed = prefs.getFloat("speed_$activeResourceId", 1f)
        _uiState.update {
            it.copy(
                resource = resource,
                title = resource.title,
                isVideo = isVideo,
                isLoading = false,
                hasError = false,
                errorMessage = null,
                resumePositionMs = resumeMs,
                speed = savedSpeed,
                subjectColorArgb = subjectColor.hashCode()
            )
        }
        initPlayer(playableUri)
    }

    /**
     * The player instance must be STABLE for the lifetime of this VM: the
     * Compose stage captures `getPlayer()` in a binding that only rebinding
     * can refresh — and rebinding loses races against state-flow updates. The
     * old code released and recreated the ExoPlayer on every setResource, so
     * the stage could be left bound to a released instance: audio ticks from
     * the fresh player while the dead player's surface stays black until a
     * fullscreen round-trip rebinds. One instance, swapped media items only.
     */
    private fun ensurePlayer(): ExoPlayer {
        player?.let { return it }
        val exoPlayer = ExoPlayer.Builder(application).build()
        player = exoPlayer
        exoPlayer.addListener(object : Player.Listener {
            override fun onPlaybackStateChanged(state: Int) {
                _uiState.update {
                    it.copy(
                        isBuffering = state == Player.STATE_BUFFERING,
                        hasError = state == Player.STATE_IDLE && exoPlayer.playerError != null
                    )
                }
            }

            override fun onPlayerError(error: PlaybackException) {
                _uiState.update { it.copy(hasError = true, errorMessage = error.localizedMessage) }
            }

            override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                _uiState.update {
                    it.copy(
                        videoWidth = videoSize.width,
                        videoHeight = videoSize.height
                    )
                }
            }

            override fun onIsPlayingChanged(isPlaying: Boolean) {
                playWhenReady = isPlaying
                _uiState.update { it.copy(isPlaying = isPlaying) }
                if (isPlaying) startTick() else stopTick()
            }
        })
        return exoPlayer
    }

    private fun initPlayer(fileUrl: String) {
        val exoPlayer = ensurePlayer()
        exoPlayer.stop()
        exoPlayer.clearMediaItems()
        exoPlayer.setMediaItem(MediaItem.fromUri(fileUrl))
        exoPlayer.setPlaybackSpeed(_uiState.value.speed)
        exoPlayer.prepare()

        val resume = _uiState.value.resumePositionMs
        if (resume > RESUME_MIN_MS) {
            exoPlayer.seekTo(resume)
        }

        exoPlayer.playWhenReady = false
    }

    fun play() {
        player?.let { p ->
            if (p.playbackState == Player.STATE_ENDED) {
                p.seekTo(0)
            }
            p.playWhenReady = true
            _uiState.update { it.copy(isPlaying = true) }
        }
    }

    fun pause() {
        player?.let { p ->
            p.playWhenReady = false
            _uiState.update { it.copy(isPlaying = false) }
            savePosition()
        }
    }

    fun togglePlay() {
        val p = player ?: return
        if (p.playbackState == Player.STATE_ENDED) {
            p.seekTo(0)
            p.playWhenReady = true
            _uiState.update { it.copy(isPlaying = true) }
        } else if (p.playWhenReady) {
            pause()
        } else {
            play()
        }
    }

    fun seekBy(deltaMs: Long) {
        player?.let { p ->
            val newPos = (p.currentPosition.coerceAtMost(p.duration.coerceAtLeast(0)) + deltaMs)
                .coerceIn(0, p.duration.coerceAtLeast(0))
            p.seekTo(newPos)
            updateProgress()
        }
    }

    fun seekToRatio(ratio: Float) {
        player?.let { p ->
            val d = p.duration.coerceAtLeast(0)
            if (d > 0) {
                p.seekTo((ratio * d).toLong())
                updateProgress()
            }
        }
    }

    fun setVolume(v: Float) {
        player?.volume = v.coerceIn(0f, 1f)
        _uiState.update { it.copy(volume = v, isMuted = v == 0f) }
    }

    fun toggleMute() {
        val st = _uiState.value
        if (st.isMuted) {
            setVolume(st.volume.coerceAtLeast(0.1f))
        } else {
            player?.volume = 0f
            _uiState.update { it.copy(isMuted = true) }
        }
    }

    fun setSpeed(speed: Float) {
        player?.setPlaybackSpeed(speed)
        _uiState.update { it.copy(speed = speed, speedMenuOpen = false) }
        if (activeResourceId.isNotBlank()) {
            application.getSharedPreferences(PREFS_NAME, 0).edit().putFloat("speed_$activeResourceId", speed).apply()
        }
    }

    fun toggleSpeedMenu() {
        _uiState.update { it.copy(speedMenuOpen = !it.speedMenuOpen) }
    }

    fun dismissSpeedMenu() {
        _uiState.update { it.copy(speedMenuOpen = false) }
    }

    fun resumeFromSaved() {
        val resume = _uiState.value.resumePositionMs
        if (resume > RESUME_MIN_MS) {
            player?.seekTo(resume)
            _uiState.update { it.copy(resumePositionMs = 0) }
        }
        play()
    }

    fun skipResume() {
        _uiState.update { it.copy(resumePositionMs = 0) }
        clearSavedPosition()
    }

    private fun startTick() {
        tickJob?.cancel()
        tickJob = viewModelScope.launch {
            while (isActive) {
                updateProgress()
                delay(250)
            }
        }
    }

    private fun stopTick() {
        tickJob?.cancel()
        tickJob = null
        updateProgress()
    }

    private fun updateProgress() {
        val p = player ?: return
        if (p.playbackState == Player.STATE_IDLE) return
        val d = p.duration.coerceAtLeast(0)
        val t = p.currentPosition.coerceAtLeast(0)
        val buf = if (d > 0 && p.bufferedPosition > 0) ((p.bufferedPosition.toFloat() / d) * 100).toInt().coerceIn(0, 100) else 0
        _uiState.update {
            it.copy(
                currentTimeMs = t,
                durationMs = d,
                bufferedPercent = buf
            )
        }
        savePositionDebounced()
    }

    private var lastSaveMs = 0L

    private fun savePositionDebounced() {
        val p = player ?: return
        if (!p.playWhenReady) return
        val now = System.currentTimeMillis()
        if (now - lastSaveMs < SAVE_INTERVAL_MS) return
        lastSaveMs = now
        savePosition()
    }

    private fun savePosition() {
        val p = player ?: return
        val d = p.duration.coerceAtLeast(0)
        val t = p.currentPosition.coerceAtLeast(0)
        if (d <= 0) return
        val prefs = application.getSharedPreferences(PREFS_NAME, 0)
        if (t > RESUME_MIN_MS && t < d - RESUME_END_PAD_MS) {
            prefs.edit().putLong("pos_$activeResourceId", t).apply()
        } else if (t >= d - RESUME_END_PAD_MS) {
            prefs.edit().remove("pos_$activeResourceId").apply()
        }
    }

    private fun clearSavedPosition() {
        if (activeResourceId.isNotBlank()) {
            application.getSharedPreferences(PREFS_NAME, 0).edit().remove("pos_$activeResourceId").apply()
        }
    }

    fun setVolumeFraction(fraction: Float) {
        val vol = (fraction.coerceIn(0f, 1f) * maxVolume).toInt()
        audioManager.setStreamVolume(AudioManager.STREAM_MUSIC, vol, 0)
    }

    fun getVolumeFraction(): Float {
        val cur = audioManager.getStreamVolume(AudioManager.STREAM_MUSIC)
        return if (maxVolume > 0) cur.toFloat() / maxVolume else 0.5f
    }

    fun getPlayer(): ExoPlayer? = player

    fun stopPlayback() {
        savePosition()
        loadJob?.cancel()
        loadJob = null
        activeResourceId = ""
        releasePlayer()
        _uiState.value = MediaPlayerUiState(isLoading = false)
    }

    /** Halt playback for a resource swap while keeping the instance alive. */
    private fun stopPlayerForLoad() {
        stopTick()
        player?.let {
            it.playWhenReady = false
            it.stop()
            it.clearMediaItems()
        }
    }

    private fun releasePlayer() {
        stopTick()
        player?.clearVideoSurface()
        player?.stop()
        player?.release()
        player = null
    }

    override fun onCleared() {
        savePosition()
        releasePlayer()
        super.onCleared()
    }
}
