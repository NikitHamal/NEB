package com.neb.ians.speech

import android.content.Context
import android.os.StatFs
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

enum class SpeechModelId { Whistle, Phonon }

sealed interface ModelState {
    data object NotInstalled : ModelState
    data class Downloading(val done: Long, val total: Long) : ModelState {
        val fraction: Float get() = if (total <= 0) 0f else (done.toFloat() / total).coerceIn(0f, 1f)
    }
    data class Installed(val bytes: Long) : ModelState
    data class Failed(val message: String) : ModelState
}

data class ModelFile(val name: String, val url: String, val bytes: Long)

/** A voice from Gradium's public catalog (`gradium/phonon-voices`). */
data class PhononVoice(
    val name: String,
    val remotePath: String,
    val gender: String,
    val age: String,
    val description: String,
)

sealed interface VoiceCatalog {
    data object Loading : VoiceCatalog
    data class Ready(val voices: List<PhononVoice>) : VoiceCatalog
    data object Unavailable : VoiceCatalog
}

object SpeechCatalog {
    const val WHISTLE_LABEL = "Whistle"
    const val PHONON_LABEL = "Phonon"

    private const val WHISTLE_BASE = "https://huggingface.co/Cactus-Compute/whistle/resolve/main/"
    private const val PHONON_BASE = "https://huggingface.co/gradium/phonon-31m-en/resolve/main/"
    const val VOICES_BASE = "https://huggingface.co/gradium/phonon-voices/resolve/main/"

    val whistleFiles = listOf(ModelFile("whistle.cact", WHISTLE_BASE + "whistle.cact", 17_720_000L))

    val phononFiles = listOf(
        ModelFile("config.json", PHONON_BASE + "config.json", 4_634L),
        ModelFile("tokenizer.json", PHONON_BASE + "tokenizer.json", 277_967L),
        ModelFile("default-voice.safetensors", PHONON_BASE + "default-voice.safetensors", 256_136L),
        ModelFile("model.q8.gguf", PHONON_BASE + "model.q8.gguf", 64_512_352L),
    )

    val sttLanguages = listOf(
        "" to "Auto", "en" to "English", "de" to "German", "fr" to "French",
        "es" to "Spanish", "it" to "Italian", "nl" to "Dutch", "pl" to "Polish",
    )

    fun files(id: SpeechModelId) = if (id == SpeechModelId.Whistle) whistleFiles else phononFiles
    fun totalBytes(id: SpeechModelId) = files(id).sumOf { it.bytes }
}

/**
 * Owns the on-device speech models: download with resume, remove, and the voice catalog.
 * Models live in `filesDir/speech`, not in the APK, and are only fetched when the user
 * asks for them. Downloads run in an app-wide scope so they survive leaving the screen.
 */
@Singleton
class SpeechModelManager @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val root = File(context.filesDir, "speech")
    private val prefs = context.getSharedPreferences("neb_speech", Context.MODE_PRIVATE)

    // A separate client: nothing from the app's API client (auth headers) should reach a CDN.
    private val client = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(45, TimeUnit.SECONDS)
        .followRedirects(true)
        .build()

    val whistleFile: File get() = File(root, "whistle/whistle.cact")
    val phononDir: File get() = File(root, "phonon-31m-en")
    private val voicesDir: File get() = File(phononDir, "voices")

    private val _stt = MutableStateFlow(initialState(SpeechModelId.Whistle))
    private val _tts = MutableStateFlow(initialState(SpeechModelId.Phonon))
    val stt: StateFlow<ModelState> = _stt.asStateFlow()
    val tts: StateFlow<ModelState> = _tts.asStateFlow()

    private val _installedVoices = MutableStateFlow(scanVoices())
    val installedVoices: StateFlow<List<String>> = _installedVoices.asStateFlow()

    private val _voiceBusy = MutableStateFlow<Set<String>>(emptySet())
    val voiceBusy: StateFlow<Set<String>> = _voiceBusy.asStateFlow()

    private val _catalog = MutableStateFlow<VoiceCatalog>(VoiceCatalog.Loading)
    val catalog: StateFlow<VoiceCatalog> = _catalog.asStateFlow()

    private val _sttLanguage = MutableStateFlow(prefs.getString("stt_lang", "") ?: "")
    val sttLanguage: StateFlow<String> = _sttLanguage.asStateFlow()

    private val _voice = MutableStateFlow(prefs.getString("voice", "default") ?: "default")
    val voice: StateFlow<String> = _voice.asStateFlow()

    private val _removed = MutableSharedFlow<SpeechModelId>(extraBufferCapacity = 4)
    /** Emitted before files are deleted so engines can drop their handles. */
    val removed: SharedFlow<SpeechModelId> = _removed.asSharedFlow()

    private val jobs = HashMap<SpeechModelId, Job>()

    fun isInstalled(id: SpeechModelId) = (if (id == SpeechModelId.Whistle) stt.value else tts.value) is ModelState.Installed

    fun setSttLanguage(code: String) {
        _sttLanguage.value = code
        prefs.edit().putString("stt_lang", code).apply()
    }

    fun setVoice(name: String) {
        _voice.value = name
        prefs.edit().putString("voice", name).apply()
    }

    private fun stateFlow(id: SpeechModelId) = if (id == SpeechModelId.Whistle) _stt else _tts

    private fun initialState(id: SpeechModelId): ModelState {
        val files = SpeechCatalog.files(id)
        val dir = if (id == SpeechModelId.Whistle) File(root, "whistle") else File(root, "phonon-31m-en")
        val present = files.all { File(dir, it.name).let { f -> f.exists() && f.length() > 0 } }
        return if (present) ModelState.Installed(files.sumOf { File(dir, it.name).length() }) else ModelState.NotInstalled
    }

    private fun scanVoices(): List<String> {
        val names = voicesDir.listFiles { f -> f.extension == "safetensors" }?.map { it.nameWithoutExtension }.orEmpty()
        return names.sorted()
    }

    fun download(id: SpeechModelId) {
        if (jobs[id]?.isActive == true) return
        val total = SpeechCatalog.totalBytes(id)
        val dir = if (id == SpeechModelId.Whistle) whistleFile.parentFile!! else phononDir
        val state = stateFlow(id)
        jobs[id] = scope.launch {
            try {
                dir.mkdirs()
                val free = StatFs(context.filesDir.path).availableBytes
                if (free < total * 12 / 10) throw IOException("Not enough free storage")
                state.value = ModelState.Downloading(0, total)
                var finished = 0L
                for (file in SpeechCatalog.files(id)) {
                    val dest = File(dir, file.name)
                    if (dest.exists() && dest.length() > 0) {
                        finished += dest.length()
                        state.value = ModelState.Downloading(finished, total)
                        continue
                    }
                    val base = finished
                    fetch(file.url, dest) { current -> state.value = ModelState.Downloading(base + current, total) }
                    finished += dest.length()
                }
                state.value = ModelState.Installed(finished)
                if (id == SpeechModelId.Phonon) _installedVoices.value = scanVoices()
            } catch (e: CancellationException) {
                state.value = initialState(id)
                throw e
            } catch (e: Exception) {
                state.value = ModelState.Failed(friendly(e))
            }
        }
    }

    /** Stops a running download; the partial file is kept so the next attempt resumes. */
    fun cancel(id: SpeechModelId) {
        jobs[id]?.cancel()
    }

    fun remove(id: SpeechModelId) {
        jobs[id]?.cancel()
        scope.launch {
            _removed.emit(id)
            // Give an engine a moment to drop its handle before the files go.
            kotlinx.coroutines.delay(150)
            val dir = if (id == SpeechModelId.Whistle) whistleFile.parentFile!! else phononDir
            dir.deleteRecursively()
            stateFlow(id).value = ModelState.NotInstalled
            if (id == SpeechModelId.Phonon) _installedVoices.value = emptyList()
        }
    }

    fun loadCatalog() {
        val cache = File(root, "voices.jsonl")
        if (_catalog.value !is VoiceCatalog.Ready && cache.exists()) {
            parseCatalog(cache.readText())?.let { _catalog.value = VoiceCatalog.Ready(it) }
        }
        scope.launch {
            try {
                val text = withContext(Dispatchers.IO) {
                    client.newCall(Request.Builder().url(SpeechCatalog.VOICES_BASE + "voices.jsonl").build())
                        .execute().use { r ->
                            if (!r.isSuccessful) throw IOException("HTTP ${r.code}")
                            r.body?.string().orEmpty()
                        }
                }
                val voices = parseCatalog(text)
                if (voices != null) {
                    root.mkdirs()
                    cache.writeText(text)
                    _catalog.value = VoiceCatalog.Ready(voices)
                }
            } catch (_: Exception) {
                if (_catalog.value !is VoiceCatalog.Ready) _catalog.value = VoiceCatalog.Unavailable
            }
        }
    }

    private fun parseCatalog(text: String): List<PhononVoice>? {
        val out = ArrayList<PhononVoice>()
        for (line in text.lineSequence()) {
            if (line.isBlank()) continue
            val o = try { JSONObject(line) } catch (_: Exception) { continue }
            // Phonon 31m speaks English only.
            if (o.optString("language") != "en") continue
            val name = o.optString("name").filter { it.isLetterOrDigit() }
            if (name.isEmpty()) continue
            out += PhononVoice(
                name = name,
                remotePath = o.optString("filename"),
                gender = o.optString("gender"),
                age = o.optString("age"),
                description = o.optString("description"),
            )
        }
        return out.takeIf { it.isNotEmpty() }
    }

    fun downloadVoice(voice: PhononVoice) {
        if (voice.name in _voiceBusy.value) return
        _voiceBusy.update { it + voice.name }
        scope.launch {
            try {
                voicesDir.mkdirs()
                fetch(SpeechCatalog.VOICES_BASE + voice.remotePath, File(voicesDir, voice.name + ".safetensors")) {}
                _installedVoices.value = scanVoices()
            } catch (_: Exception) {
                // The row goes back to its download button; the user can retry.
            } finally {
                _voiceBusy.update { it - voice.name }
            }
        }
    }

    fun removeVoice(name: String) {
        scope.launch {
            if (_voice.value == name) setVoice("default")
            File(voicesDir, "$name.safetensors").delete()
            _installedVoices.value = scanVoices()
        }
    }

    private suspend fun fetch(url: String, dest: File, onProgress: (Long) -> Unit) = withContext(Dispatchers.IO) {
        dest.parentFile?.mkdirs()
        val part = File(dest.path + ".part")
        var have = if (part.exists()) part.length() else 0L
        val request = Request.Builder().url(url)
            .header("User-Agent", "NEBians-Android")
            .apply { if (have > 0) header("Range", "bytes=$have-") }
            .build()
        client.newCall(request).execute().use { resp ->
            if (resp.code == 416) {
                // The partial file is already the whole file.
                if (dest.exists()) dest.delete()
                if (!part.renameTo(dest)) throw IOException("Could not save the file")
                return@withContext
            }
            if (!resp.isSuccessful) throw IOException("Server answered ${resp.code}")
            val append = resp.code == 206
            if (!append) have = 0L
            val body = resp.body ?: throw IOException("Empty response")
            val remaining = body.contentLength()
            var written = have
            FileOutputStream(part, append).use { out ->
                val buf = ByteArray(64 * 1024)
                val input = body.byteStream()
                var lastTick = 0L
                while (true) {
                    ensureActive()
                    val n = input.read(buf)
                    if (n < 0) break
                    out.write(buf, 0, n)
                    written += n
                    val now = System.nanoTime()
                    if (now - lastTick > 80_000_000L) {
                        lastTick = now
                        onProgress(written)
                    }
                }
            }
            if (remaining >= 0 && written != have + remaining) throw IOException("The download was cut short")
            onProgress(written)
        }
        if (dest.exists()) dest.delete()
        if (!part.renameTo(dest)) throw IOException("Could not save the file")
    }

    private fun friendly(e: Exception): String = when {
        e is java.net.UnknownHostException || e is java.net.SocketTimeoutException || e is java.net.ConnectException ->
            "No connection. Try again when you are online."
        e is IOException && e.message?.startsWith("Not enough") == true -> "Not enough free storage"
        else -> e.message?.takeIf { it.isNotBlank() } ?: "Download failed"
    }
}
