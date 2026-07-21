package com.neb.ians.ui.components

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
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
        try {
            val rec = if (Build.VERSION.SDK_INT >= 31) MediaRecorder(context) else @Suppress("DEPRECATION") MediaRecorder()
            rec.setAudioSource(MediaRecorder.AudioSource.MIC)
            rec.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            rec.setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            rec.setAudioChannels(1)
            rec.setAudioSamplingRate(44100)
            rec.setAudioEncodingBitRate(96000)
            rec.setOutputFile(file.absolutePath)
            rec.prepare()
            rec.start()
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

/** Live recording strip rendered inside the comment bar while recording. */
@Composable
fun VoiceRecordingStrip(
    recorder: VoiceNoteRecorder,
    modifier: Modifier = Modifier
) {
    val pulse by rememberInfiniteTransition(label = "rec-pulse").animateFloat(
        initialValue = 0.45f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(700), RepeatMode.Reverse),
        label = "rec-pulse-alpha"
    )
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        // Pulsing record dot
        Box(
            modifier = Modifier
                .width(10.dp)
                .height(10.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.error.copy(alpha = if (recorder.isPaused) 0.4f else pulse))
        )
        Text(
            text = formatVoiceTime(recorder.elapsedMs),
            style = MaterialTheme.typography.bodyMedium,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.error,
            fontSize = 13.sp
        )
        // Live waveform bars driven by microphone amplitude
        Row(
            modifier = Modifier.weight(1f),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            recorder.amplitudes.forEach { amp ->
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height((4 + amp * 22).dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(
                            if (amp > 0.12f) MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.35f)
                        )
                )
            }
        }
        // Pause / resume
        IconButton(onClick = recorder::togglePause, modifier = Modifier.width(34.dp).height(34.dp)) {
            Icon(
                imageVector = if (recorder.isPaused) Icons.Filled.PlayArrow else Icons.Filled.Pause,
                contentDescription = if (recorder.isPaused) "Resume recording" else "Pause recording",
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.width(18.dp).height(18.dp)
            )
        }
        // Discard
        IconButton(onClick = recorder::cancel, modifier = Modifier.width(34.dp).height(34.dp)) {
            Icon(
                imageVector = Icons.Filled.Close,
                contentDescription = "Delete recording",
                tint = MaterialTheme.colorScheme.error,
                modifier = Modifier.width(18.dp).height(18.dp)
            )
        }
        // Finish + stage
        IconButton(onClick = recorder::stop, modifier = Modifier.width(34.dp).height(34.dp)) {
            Icon(
                imageVector = Icons.Filled.Check,
                contentDescription = "Finish recording",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.width(18.dp).height(18.dp)
            )
        }
    }
}

fun formatVoiceTime(ms: Long): String {
    val totalSec = (ms / 1000).coerceAtLeast(0)
    val m = totalSec / 60
    val s = totalSec % 60
    return "%d:%02d".format(m, s)
}
