package com.neb.ians.ui.components

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import java.io.File

/**
 * Live voice-note recorder for comment composers. Owns MediaRecorder, the
 * RECORD_AUDIO runtime permission handshake, a 100 ms amplitude ticker and
 * pause/stop/delete semantics. [onVoiceNote] receives (file, durationMs) once
 * a recording is finished via stop; [onError] surfaces user-facing failures.
 */
class VoiceNoteRecorder internal constructor(
    private val context: Context,
    private val scope: kotlinx.coroutines.CoroutineScope,
    private val onVoiceNote: (File, Long) -> Unit,
    private val onError: (String) -> Unit
) {
    var isRecording by mutableStateOf(false)
        private set
    var isPaused by mutableStateOf(false)
        private set
    var elapsedMs by mutableLongStateOf(0L)
        private set
    val amplitudes = mutableStateListOf<Float>()

    /** Assigned by the composable holder — mic tap entry point that performs
     * the runtime permission handshake before calling [start]. */
    var micClick: () -> Unit = {}
        internal set

    private var recorder: MediaRecorder? = null
    private var outputFile: File? = null

    fun start() {
        if (isRecording) return
        val file = File(context.cacheDir, "voice_${System.currentTimeMillis()}.m4a")
        val rec = try {
            val r = if (Build.VERSION.SDK_INT >= 31) MediaRecorder(context) else @Suppress("DEPRECATION") MediaRecorder()
            r.setAudioSource(MediaRecorder.AudioSource.MIC)
            r.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            r.setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            r.setAudioChannels(1)
            r.setAudioSamplingRate(44100)
            r.setAudioEncodingBitRate(96000)
            r.setOutputFile(file.absolutePath)
            r.prepare()
            r.start()
            r
        } catch (e: Exception) {
            file.delete()
            onError("Couldn't start recording")
            return
        }
        recorder = rec
        outputFile = file
        elapsedMs = 0L
        amplitudes.clear()
        repeat(20) { amplitudes.add(0.08f) }
        isPaused = false
        isRecording = true
        scope.launch {
            val started = System.currentTimeMillis()
            var pausedAccum = 0L
            var pauseStart = 0L
            while (isActive && recorder != null) {
                val active = isRecording && !isPaused
                if (active) {
                    elapsedMs = System.currentTimeMillis() - started - pausedAccum
                    val amp = runCatching { recorder?.maxAmplitude ?: 0 }.getOrDefault(0)
                    val norm = (amp / 32767f).coerceIn(0f, 1f)
                    amplitudes.removeAt(0)
                    amplitudes.add(0.06f + norm * 0.94f)
                }
                if (isPaused && pauseStart == 0L) pauseStart = System.currentTimeMillis()
                if (!isPaused && pauseStart != 0L) {
                    pausedAccum += System.currentTimeMillis() - pauseStart
                    pauseStart = 0L
                }
                delay(100)
            }
        }
        scope.launch {
            // Hard cap at 5 minutes — auto-stop rather than balloon the file.
            delay(5 * 60_000L)
            if (isRecording) stop()
        }
    }

    fun togglePause() {
        val rec = recorder ?: return
        if (!isRecording) return
        try {
            if (isPaused) rec.resume() else rec.pause()
            isPaused = !isPaused
        } catch (_: Exception) { /* pause unsupported — keep recording */ }
    }

    /** Finish and hand the voice note to the caller. */
    fun stop() {
        val rec = recorder ?: return
        val file = outputFile
        val duration = elapsedMs
        isRecording = false
        isPaused = false
        recorder = null
        outputFile = null
        runCatching { rec.stop() }
        runCatching { rec.release() }
        if (file == null || !file.exists() || file.length() == 0L || duration < 300L) {
            file?.delete()
            onError("Recording too short")
            return
        }
        onVoiceNote(file, duration)
    }

    /** Discard the in-flight recording without emitting anything. */
    fun cancel() {
        val rec = recorder ?: return
        val file = outputFile
        isRecording = false
        isPaused = false
        recorder = null
        outputFile = null
        runCatching { rec.stop() }
        runCatching { rec.release() }
        file?.delete()
        elapsedMs = 0L
    }
}

@Composable
fun rememberVoiceNoteRecorder(
    onVoiceNote: (File, Long) -> Unit,
    onError: (String) -> Unit = {}
): VoiceNoteRecorder {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val recorder = remember(context) { VoiceNoteRecorder(context, scope, onVoiceNote, onError) }

    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) recorder.start() else onError("Microphone permission is needed to record voice notes")
    }

    // Keep the mic entry point pointed at the current composition's launcher.
    SideEffect {
        recorder.micClick = {
            if (ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) ==
                PackageManager.PERMISSION_GRANTED
            ) {
                recorder.start()
            } else {
                permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
            }
        }
    }

    return recorder
}

/**
 * Live recording strip rendered inside the comment bar while recording.
 * Modern take: glowing pulsing record dot with an expanding halo, a
 * spring-animated gradient waveform that breathes with the mic amplitude,
 * and proper iconography — pause/resume, a STOP square (finish & stage) and
 * a trash DELETE — all on tinted control discs.
 */
@Composable
fun VoiceRecordingStrip(
    recorder: VoiceNoteRecorder,
    modifier: Modifier = Modifier
) {
    val infinite = rememberInfiniteTransition(label = "rec")
    val haloScale by infinite.animateFloat(
        initialValue = 1f,
        targetValue = 1.9f,
        animationSpec = infiniteRepeatable(tween(950), RepeatMode.Restart),
        label = "rec-halo-scale"
    )
    val haloAlpha by infinite.animateFloat(
        initialValue = 0.45f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(tween(950), RepeatMode.Restart),
        label = "rec-halo-alpha"
    )
    val error = MaterialTheme.colorScheme.error
    val primary = MaterialTheme.colorScheme.primary

    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(7.dp)
    ) {
        // Record dot with an expanding halo (frozen while paused)
        Box(
            modifier = Modifier.width(18.dp),
            contentAlignment = Alignment.Center
        ) {
            if (!recorder.isPaused) {
                Box(
                    modifier = Modifier
                        .width(10.dp)
                        .height(10.dp)
                        .graphicsLayer {
                            scaleX = haloScale
                            scaleY = haloScale
                        }
                        .clip(CircleShape)
                        .background(error.copy(alpha = haloAlpha))
                )
            }
            Box(
                modifier = Modifier
                    .width(9.dp)
                    .height(9.dp)
                    .clip(CircleShape)
                    .background(if (recorder.isPaused) error.copy(alpha = 0.45f) else error)
            )
        }
        Text(
            text = formatVoiceTime(recorder.elapsedMs),
            style = MaterialTheme.typography.bodyMedium,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
            color = error,
            fontSize = 13.sp
        )
        // Live waveform: springy per-bar height animation, error→primary gradient
        Row(
            modifier = Modifier.weight(1f),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            recorder.amplitudes.forEachIndexed { index, amp ->
                val barHeight by animateFloatAsState(
                    targetValue = 3f + amp * 21f,
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioNoBouncy,
                        stiffness = Spring.StiffnessMediumLow
                    ),
                    label = "rec-bar-$index"
                )
                val hot = amp > 0.14f && !recorder.isPaused
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height(barHeight.dp)
                        .clip(RoundedCornerShape(3.dp))
                        .background(
                            Brush.verticalGradient(
                                if (hot) listOf(primary, error)
                                else listOf(
                                    MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.30f),
                                    MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.14f)
                                )
                            )
                        )
                )
            }
        }
        // Pause / resume — neutral disc
        VoiceRecControlButton(
            onClick = recorder::togglePause,
            container = MaterialTheme.colorScheme.surfaceContainerHigh,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            contentDescription = if (recorder.isPaused) "Resume recording" else "Pause recording"
        ) {
            Icon(
                imageVector = if (recorder.isPaused) Icons.Filled.PlayArrow else Icons.Filled.Pause,
                contentDescription = null,
                tint = it,
                modifier = Modifier.width(16.dp).height(16.dp)
            )
        }
        // Stop (finish & stage) — primary disc, square icon
        VoiceRecControlButton(
            onClick = recorder::stop,
            container = primary,
            tint = MaterialTheme.colorScheme.onPrimary,
            contentDescription = "Stop and add voice note"
        ) {
            Icon(
                imageVector = Icons.Filled.Stop,
                contentDescription = null,
                tint = it,
                modifier = Modifier.width(15.dp).height(15.dp)
            )
        }
        // Delete (discard) — errorContainer disc, trash icon
        VoiceRecControlButton(
            onClick = recorder::cancel,
            container = MaterialTheme.colorScheme.errorContainer,
            tint = MaterialTheme.colorScheme.onErrorContainer,
            contentDescription = "Delete recording"
        ) {
            Icon(
                imageVector = Icons.Outlined.Delete,
                contentDescription = null,
                tint = it,
                modifier = Modifier.width(16.dp).height(16.dp)
            )
        }
    }
}

/** Small circular icon button used by the in-bar recording strip. */
@Composable
private fun VoiceRecControlButton(
    onClick: () -> Unit,
    container: Color,
    tint: Color,
    contentDescription: String,
    icon: @Composable (Color) -> Unit
) {
    Surface(
        onClick = onClick,
        shape = CircleShape,
        color = container,
        modifier = Modifier.width(30.dp).height(30.dp)
    ) {
        Box(contentAlignment = Alignment.Center) {
            // Accessible label without duplicating visually
            Box(
                modifier = Modifier
                    .width(1.dp)
                    .height(1.dp)
            ) {
                Text(
                    contentDescription,
                    fontSize = 1.sp,
                    color = Color.Transparent
                )
            }
            icon(tint)
        }
    }
}

fun formatVoiceTime(ms: Long): String {
    val totalSec = (ms / 1000).coerceAtLeast(0)
    val m = totalSec / 60
    val s = totalSec % 60
    return "%d:%02d".format(m, s)
}
