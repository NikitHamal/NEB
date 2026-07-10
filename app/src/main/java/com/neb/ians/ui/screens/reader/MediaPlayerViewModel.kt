package com.neb.ians.ui.screens.reader

import android.app.Application
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
    val subjectColorArgb: Int = 0
)

@HiltViewModel
class MediaPlayerViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val application: Application,
    private val resourceRepository: ResourceRepository,
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""

    private val _uiState = MutableStateFlow(MediaPlayerUiState())
    val uiState: StateFlow<MediaPlayerUiState> = _uiState.asStateFlow()

    private var player: ExoPlayer? = null
    private var tickJob: Job? = null
    private var playWhenReady: Boolean = false

    companion object {
        private const val SAVE_INTERVAL_MS = 2500L
        private const val RESUME_MIN_MS = 8000L
        private const val RESUME_END_PAD_MS = 12000L
        private const val PREFS_NAME = "nmp_positions"
    }

    init {
        loadResource()
    }

    private fun loadResource() {
        viewModelScope.launch {
            resourceRepository.getResource(resourceId)
                .onSuccess { resource ->
                    val isVideo = when {
                        resource.type.contains("video", ignoreCase = true) -> true
                        resource.fileUrl.contains(".mp4", ignoreCase = true) ||
                            resource.fileUrl.contains(".webm", ignoreCase = true) ||
                            resource.fileUrl.contains(".mkv", ignoreCase = true) -> true
                        else -> false
                    }
                    val subjectColor = com.neb.ians.util.getSubjectColor(
                        resource.subject.split(",").firstOrNull()?.trim().orEmpty()
                    )
                    val prefs = application.getSharedPreferences(PREFS_NAME, 0)
                    val resumeMs = prefs.getLong("pos_$resourceId", 0L)
                    val savedSpeed = prefs.getFloat("speed_$resourceId", 1f)
                    _uiState.update {
                        it.copy(
                            resource = resource,
                            title = resource.title,
                            isVideo = isVideo,
                            isLoading = false,
                            resumePositionMs = resumeMs,
                            speed = savedSpeed,
                            subjectColorArgb = subjectColor.hashCode()
                        )
                    }
                    if (resource.fileUrl.isNotBlank()) {
                        initPlayer(resource.fileUrl)
                    } else {
                        _uiState.update { it.copy(hasError = true, errorMessage = "No file available") }
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(isLoading = false, hasError = true, errorMessage = ApiErrorMapper.mapException(e))
                    }
                }
        }
    }

    private fun initPlayer(fileUrl: String) {
        val exoPlayer = ExoPlayer.Builder(application).build()
        player = exoPlayer

        exoPlayer.setMediaItem(MediaItem.fromUri(fileUrl))
        exoPlayer.prepare()

        val resume = _uiState.value.resumePositionMs
        if (resume > RESUME_MIN_MS) {
            exoPlayer.seekTo(resume)
        }

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

            override fun onIsPlayingChanged(isPlaying: Boolean) {
                playWhenReady = isPlaying
                _uiState.update { it.copy(isPlaying = isPlaying) }
                if (isPlaying) startTick() else stopTick()
            }
        })

        exoPlayer.playWhenReady = false
    }

    fun play() {
        player?.let { p ->
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
        if (p.playWhenReady) pause() else play()
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
        application.getSharedPreferences(PREFS_NAME, 0).edit().putFloat("speed_$resourceId", speed).apply()
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
        val st = _uiState.value
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
            prefs.edit().putLong("pos_$resourceId", t).apply()
        } else if (t >= d - RESUME_END_PAD_MS) {
            prefs.edit().remove("pos_$resourceId").apply()
        }
    }

    private fun clearSavedPosition() {
        application.getSharedPreferences(PREFS_NAME, 0).edit().remove("pos_$resourceId").apply()
    }

    fun getPlayer(): ExoPlayer? = player

    override fun onCleared() {
        super.onCleared()
        savePosition()
        player?.stop()
        player?.release()
        player = null
    }
}
