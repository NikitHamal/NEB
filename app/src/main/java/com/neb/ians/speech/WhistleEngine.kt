package com.neb.ians.speech

import android.annotation.SuppressLint
import android.content.Context
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.asCoroutineDispatcher
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.util.concurrent.Executors
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sqrt

sealed interface DictationState {
    data object Idle : DictationState
    data object Preparing : DictationState
    data object Listening : DictationState
    data object Finishing : DictationState
    data class Error(val message: String) : DictationState
}

/**
 * Live dictation with Whistle. The microphone is read at 16 kHz mono; about one second at a
 * time goes to the engine, which commits the words two consecutive passes agree on. Those
 * arrive on [committed]; the unconfirmed tail is on [pending]. Every engine call runs on one
 * dedicated thread because the engine is process-global and not thread-safe.
 */
@Singleton
class WhistleEngine @Inject constructor(
    @ApplicationContext private val context: Context,
    private val models: SpeechModelManager,
) {
    private val engineThread by lazy {
        Executors.newSingleThreadExecutor { r ->
            Thread(r, "neb-whistle").apply { priority = Thread.NORM_PRIORITY + 1 }
        }.asCoroutineDispatcher()
    }
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

    private val _state = MutableStateFlow<DictationState>(DictationState.Idle)
    val state: StateFlow<DictationState> = _state.asStateFlow()

    private val _level = MutableStateFlow(0f)
    /** 0..1 input loudness for the live meter. */
    val level: StateFlow<Float> = _level.asStateFlow()

    private val _pending = MutableStateFlow("")
    val pending: StateFlow<String> = _pending.asStateFlow()

    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds.asStateFlow()

    private val _committed = MutableSharedFlow<String>(extraBufferCapacity = 64)
    val committed: SharedFlow<String> = _committed.asSharedFlow()

    @Volatile private var loadedPath: String? = null
    @Volatile private var stopRequested = false
    private var session: Job? = null

    val supported: Boolean get() = models.sttSupportedCached
    val isRunning: Boolean get() = session?.isActive == true

    init {
        scope.launch {
            models.removed.collect { id ->
                if (id.isStt) {
                    loadedPath = null
                    cancel()
                }
            }
        }
    }

    fun clearError() {
        if (_state.value is DictationState.Error) _state.value = DictationState.Idle
    }

    /** The caller has already been granted RECORD_AUDIO. */
    fun start() {
        if (isRunning) return
        if (!supported) return fail("Speech to text is not available on this device")
        if (!models.isAnySttInstalled()) return fail("Download the speech to text model first")
        stopRequested = false
        _pending.value = ""
        _seconds.value = 0
        _state.value = DictationState.Preparing
        session = scope.launch {
            try {
                val activeId = models.activeSttModel()
                val rawLang = models.sttLanguage.value
                val effectiveLang = when {
                    activeId == SpeechModelId.ShrutiNepali && rawLang !in listOf("ne", "en", "") -> "ne"
                    else -> rawLang.ifBlank { null }
                }
                withContext(engineThread) {
                    ensureLoaded()
                    NativeSpeech.sttReset()
                }
                record(effectiveLang)
                _state.value = DictationState.Idle
            } catch (e: CancellationException) {
                _state.value = DictationState.Idle
                throw e
            } catch (t: Throwable) {
                fail(t.message ?: "Dictation stopped")
            } finally {
                _level.value = 0f
                _pending.value = ""
            }
        }
    }

    /** Ends the session after the words still in flight are transcribed. */
    fun stop() {
        stopRequested = true
        if (_state.value == DictationState.Listening) {
            _state.value = DictationState.Finishing
        }
    }

    /** Ends the session now. */
    fun cancel() {
        stopRequested = true
        session?.cancel()
    }

    private fun fail(message: String) {
        _state.value = DictationState.Error(message)
    }

    private fun ensureLoaded() {
        val target = models.activeSttFile().path
        if (loadedPath == target) return
        val rc = NativeSpeech.sttLoad(target)
        if (rc < 0 || (rc and 2) == 0) throw IllegalStateException(NativeSpeech.sttError().ifBlank { "The speech model could not be loaded" })
        loadedPath = target
    }

    @SuppressLint("MissingPermission")
    private suspend fun record(lang: String?) = withContext(Dispatchers.IO) {
        val rate = 16_000
        val minBuf = AudioRecord.getMinBufferSize(rate, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT)
        val rec = AudioRecord(
            MediaRecorder.AudioSource.VOICE_RECOGNITION, rate,
            AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT,
            max(minBuf, rate * 2 * 4),
        )
        if (rec.state != AudioRecord.STATE_INITIALIZED) {
            rec.release()
            throw IllegalStateException("The microphone is busy")
        }
        val ns = runCatching {
            if (android.media.audiofx.NoiseSuppressor.isAvailable()) {
                android.media.audiofx.NoiseSuppressor.create(rec.audioSessionId)?.apply { enabled = true }
            } else null
        }.getOrNull()
        val agc = runCatching {
            if (android.media.audiofx.AutomaticGainControl.isAvailable()) {
                android.media.audiofx.AutomaticGainControl.create(rec.audioSessionId)?.apply { enabled = true }
            } else null
        }.getOrNull()
        val keywords = "NEB\nSEE\nIOE\nCEE\nMECEE\nCTEVT\nKathmandu\nPokhara\nLalitpur\nBhaktapur\nTribhuvan\nKathmandu University\nPokhara University\nPurbanchal\nLok Sewa\nNRB\nMBBS\nCSIT\nBCA\nBIM\nBBA"
        val chunks = Channel<FloatArray>(capacity = 10, onBufferOverflow = kotlinx.coroutines.channels.BufferOverflow.DROP_OLDEST)
        val consumer = launch(engineThread) {
            try {
                for (firstChunk in chunks) {
                    var merged = firstChunk
                    while (merged.size < rate * 3) {
                        val next = chunks.tryReceive().getOrNull() ?: break
                        val combined = FloatArray(merged.size + next.size)
                        System.arraycopy(merged, 0, combined, 0, merged.size)
                        System.arraycopy(next, 0, combined, merged.size, next.size)
                        merged = combined
                    }
                    handle(NativeSpeech.sttStream(merged, merged.size, lang, keywords))
                }
            } finally {
                withContext(NonCancellable) { handle(NativeSpeech.sttStop()); _pending.value = "" }
            }
        }
        val frame = ShortArray(rate / 5) // 200ms low-latency read frames
        val acc = FloatArray(rate)
        var filled = 0
        var total = 0L
        var chunkTarget = (rate * 65) / 100 // 0.65s first chunk for 35% faster time-to-first-word
        var silentChunks = 0
        var hadSpeechInChunk = false
        var dcMean = 0f
        try {
            rec.startRecording()
            _state.value = DictationState.Listening
            while (isActive && !stopRequested) {
                val maxRead = min(frame.size, acc.size - filled)
                if (maxRead <= 0) {
                    chunks.send(acc.copyOf(filled))
                    filled = 0
                    hadSpeechInChunk = false
                    continue
                }
                val n = rec.read(frame, 0, maxRead)
                if (n < 0) throw IllegalStateException("The microphone stopped")
                if (n == 0) continue
                var sum = 0.0
                for (i in 0 until n) {
                    val raw = frame[i] * (1f / 32768f)
                    dcMean = dcMean * 0.995f + raw * 0.005f
                    val f = (raw - dcMean).coerceIn(-1f, 1f)
                    sum += f * f
                    acc[filled + i] = f
                }
                filled += n
                total += n
                val rms = sqrt(sum / n).toFloat()
                if (rms >= 0.0032f) hadSpeechInChunk = true
                _level.value = min(1f, rms * 7.5f)
                _seconds.value = (total / rate).toInt()
                val vadEndpointFlush = hadSpeechInChunk && rms < 0.0022f && filled >= (rate * 35) / 100
                if (filled >= chunkTarget || vadEndpointFlush) {
                    var chunkSq = 0.0
                    for (i in 0 until filled) chunkSq += acc[i] * acc[i]
                    val chunkRms = sqrt(chunkSq / filled).toFloat()
                    if (chunkRms < 0.0018f && !hadSpeechInChunk) {
                        silentChunks++
                    } else {
                        silentChunks = 0
                    }
                    if (silentChunks <= 2 || _pending.value.isNotEmpty()) {
                        chunks.send(acc.copyOf(filled))
                        chunkTarget = (rate * 85) / 100 // 0.85s steady-state responsive chunks
                    }
                    filled = 0
                    hadSpeechInChunk = false
                }
            }
        } finally {
            runCatching { rec.stop() }
            runCatching { ns?.release() }
            runCatching { agc?.release() }
            rec.release()
            if (filled > 0 && isActive) chunks.trySend(acc.copyOf(filled))
            _state.value = DictationState.Finishing
            chunks.close()
            withContext(NonCancellable) { consumer.join() }
        }
    }

    private fun handle(json: String?) {
        if (json.isNullOrBlank()) return
        try {
            val o = JSONObject(json)
            val text = o.optString("text").trim()
            if (text.isNotEmpty()) _committed.tryEmit(text)
            _pending.value = o.optString("pending").trim()
        } catch (_: Exception) {
        }
    }
}
