package com.neb.ians.speech

import android.util.Log

/** Receives the 24 kHz mono PCM that Phonon produces; return false to stop early. */
interface PcmSink {
    fun onPcm(pcm: FloatArray): Boolean
}

/**
 * JNI surface of `libneb_speech.so` (see `src/main/cpp`). Whistle (speech to text) and
 * Phonon (text to speech) are single-threaded engines: callers serialise every call
 * through one dedicated thread each (see [WhistleEngine] and [PhononEngine]).
 */
internal object NativeSpeech {
    private val loaded: Boolean = try {
        System.loadLibrary("neb_speech")
        true
    } catch (t: Throwable) {
        Log.e("NebSpeech", "libneb_speech failed to load", t)
        false
    }

    val sttSupported: Boolean by lazy { loaded && sttCompiled() }

    /** Phonon's library is shipped for arm64 only and needs ARMv8.2 dotprod + fp16. */
    val ttsSupported: Boolean by lazy { loaded && cpuHasDotprodAndFp16() && ttsAvailable() }

    private fun cpuHasDotprodAndFp16(): Boolean = try {
        val info = java.io.File("/proc/cpuinfo").readText()
        val features = info.lineSequence().firstOrNull { it.startsWith("Features") }.orEmpty()
        features.contains("asimddp") && (features.contains("asimdhp") || features.contains("fphp"))
    } catch (_: Throwable) {
        false
    }

    // Whistle
    external fun sttCompiled(): Boolean
    external fun sttLoad(path: String): Int
    external fun sttError(): String
    external fun sttTranscribe(pcm: FloatArray, samples: Int, lang: String?, keywords: String?): String?
    external fun sttStream(pcm: FloatArray, samples: Int, lang: String?, keywords: String?): String?
    external fun sttStop(): String?

    // Phonon
    external fun ttsAvailable(): Boolean
    external fun ttsLoad(dir: String, lang: String, threads: Int): Long
    external fun ttsError(handle: Long): String
    external fun ttsVoices(handle: Long): Array<String>
    external fun ttsSetVoice(handle: Long, name: String): Boolean
    external fun ttsSetLanguage(handle: Long, lang: String): Boolean
    external fun ttsSpeak(handle: Long, text: String, sink: PcmSink): Boolean
    external fun ttsFree(handle: Long)
}
