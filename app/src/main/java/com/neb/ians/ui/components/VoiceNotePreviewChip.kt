package com.neb.ians.ui.components

import android.content.Context
import android.media.MediaPlayer
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.screens.forum.PendingForumAttachment
import kotlinx.coroutines.delay
import kotlin.random.Random

/**
 * One-at-a-time playback holder for staged (not-yet-posted) voice notes in
 * comment composers. android.media.MediaPlayer is enough here — takes are
 * small local files, and the shared ExoPlayers stay untouched.
 */
object VoiceNotePreviewPool {
    private var player: MediaPlayer? = null

    var activeId by mutableStateOf<String?>(null)
        private set
    var isPlaying by mutableStateOf(false)
        private set
    var positionMs by mutableLongStateOf(0L)
        private set
    var durationMs by mutableLongStateOf(0L)
        private set
    var error by mutableStateOf<String?>(null)
        private set

    fun toggle(id: String, uri: Uri, context: Context) {
        if (activeId == id && player != null) {
            val p = player ?: return
            if (isPlaying) {
                runCatching { p.pause() }
                isPlaying = false
            } else {
                runCatching { p.start() }
                isPlaying = true
            }
            return
        }
        releaseInternal()
        error = null
        activeId = id
        positionMs = 0L
        durationMs = 0L
        val mp = MediaPlayer()
        try {
            mp.setDataSource(context, uri)
            mp.setOnPreparedListener { prepared ->
                durationMs = prepared.duration.toLong().coerceAtLeast(0L)
                runCatching { prepared.start() }
                isPlaying = true
            }
            mp.setOnCompletionListener {
                isPlaying = false
                positionMs = 0L
                runCatching { player?.seekTo(0) }
            }
            mp.setOnErrorListener { _, _, _ ->
                error = "Couldn't play this voice note"
                releaseInternal()
                true
            }
            player = mp
            mp.prepareAsync()
        } catch (_: Exception) {
            error = "Couldn't play this voice note"
            releaseInternal()
        }
    }

    fun seekTo(ms: Long) {
        val p = player ?: return
        runCatching { p.seekTo(ms.toInt().coerceAtLeast(0)) }
        positionMs = ms.coerceAtLeast(0L)
    }

    /** Called periodically by the owning chip while it is active. */
    fun syncProgress() {
        val p = player ?: return
        positionMs = runCatching { p.currentPosition.toLong() }.getOrDefault(positionMs).coerceAtLeast(0L)
        if (durationMs <= 0L) {
            durationMs = runCatching { p.duration.toLong() }.getOrDefault(durationMs).coerceAtLeast(0L)
        }
    }

    fun stop() {
        releaseInternal()
    }

    private fun releaseInternal() {
        runCatching { player?.stop() }
        runCatching { player?.release() }
        player = null
        activeId = null
        isPlaying = false
        positionMs = 0L
        durationMs = 0L
    }
}

/**
 * Composer chip for a staged voice note: tap-to-play preview with a
 * deterministic waveform (seeded per chip so it doesn't reshuffle on
 * recomposition), played-portion tinting, mono timestamps, upload progress
 * and a remove button. Posted comments use ForumAudioPlayer instead.
 */
@Composable
fun PendingVoiceNoteChip(
    attachment: PendingForumAttachment,
    onRemove: (String) -> Unit
) {
    val context = LocalContext.current
    val isActive = VoiceNotePreviewPool.activeId == attachment.localId
    val playing = isActive && VoiceNotePreviewPool.isPlaying
    val totalMs = when {
        VoiceNotePreviewPool.durationMs > 0L && isActive -> VoiceNotePreviewPool.durationMs
        attachment.durationMs > 0L -> attachment.durationMs
        else -> 0L
    }
    val currentMs = if (isActive) VoiceNotePreviewPool.positionMs else 0L
    val progress = if (totalMs > 0L) (currentMs.toFloat() / totalMs.toFloat()).coerceIn(0f, 1f) else 0f

    // Keep pool progress flowing while this chip owns playback.
    LaunchedEffect(playing) {
        while (playing) {
            VoiceNotePreviewPool.syncProgress()
            delay(150L)
        }
    }
    // Removing / navigating away must not leak playback.
    DisposableEffect(attachment.localId) {
        onDispose {
            if (VoiceNotePreviewPool.activeId == attachment.localId) {
                VoiceNotePreviewPool.stop()
            }
        }
    }

    // Deterministic fake-waveform amplitudes per chip.
    val bars = 26
    val seed = attachment.localId.hashCode()
    val primary = MaterialTheme.colorScheme.primary

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 6.dp),
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = androidx.compose.foundation.BorderStroke(
            1.dp,
            if (attachment.error != null) MaterialTheme.colorScheme.error.copy(alpha = 0.5f)
            else MaterialTheme.colorScheme.outlineVariant
        )
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(9.dp)
        ) {
            // Play/pause disc (spinner while the upload is in flight)
            Surface(
                onClick = {
                    if (!attachment.uploading && attachment.error == null) {
                        VoiceNotePreviewPool.toggle(attachment.localId, attachment.uri, context)
                    }
                },
                shape = CircleShape,
                color = if (attachment.error != null) MaterialTheme.colorScheme.errorContainer else primary,
                modifier = Modifier.width(34.dp).height(34.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    if (attachment.uploading) {
                        CircularProgressIndicator(
                            color = MaterialTheme.colorScheme.onPrimary,
                            strokeWidth = 2.dp,
                            modifier = Modifier.width(18.dp).height(18.dp)
                        )
                    } else {
                        Icon(
                            imageVector = if (playing) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                            contentDescription = if (playing) "Pause voice note" else "Play voice note",
                            tint = if (attachment.error != null) MaterialTheme.colorScheme.onErrorContainer
                            else MaterialTheme.colorScheme.onPrimary,
                            modifier = Modifier.width(19.dp).height(19.dp)
                        )
                    }
                }
            }

            // Waveform with played-portion tint
            Row(
                modifier = Modifier.weight(1f),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(2.dp)
            ) {
                repeat(bars) { index ->
                    val amp = 0.30f + Random(seed + index).nextFloat() * 0.70f
                    val played = progress > 0f && (index + 0.5f) / bars <= progress
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .height((5 + amp * 19).dp)
                            .clip(RoundedCornerShape(3.dp))
                            .background(
                                when {
                                    attachment.error != null -> MaterialTheme.colorScheme.error.copy(alpha = 0.35f)
                                    played -> primary
                                    else -> MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.32f)
                                }
                            )
                    )
                }
            }

            // Timestamps / state label
            Text(
                text = when {
                    attachment.error != null -> attachment.error
                    attachment.uploading -> "Uploading…"
                    totalMs > 0L -> "${formatVoiceTime(currentMs)} / ${formatVoiceTime(totalMs)}"
                    else -> formatVoiceTime(currentMs)
                },
                style = MaterialTheme.typography.labelSmall,
                fontFamily = if (attachment.error != null) FontFamily.Default else FontFamily.Monospace,
                fontWeight = FontWeight.SemiBold,
                color = if (attachment.error != null) MaterialTheme.colorScheme.error
                else MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 11.sp,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )

            // Remove
            Surface(
                onClick = {
                    if (VoiceNotePreviewPool.activeId == attachment.localId) VoiceNotePreviewPool.stop()
                    onRemove(attachment.localId)
                },
                shape = CircleShape,
                color = Color.Transparent,
                modifier = Modifier.width(28.dp).height(28.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Filled.Close,
                        contentDescription = "Remove voice note",
                        tint = MaterialTheme.colorScheme.error,
                        modifier = Modifier.width(16.dp).height(16.dp)
                    )
                }
            }
        }
    }
}
