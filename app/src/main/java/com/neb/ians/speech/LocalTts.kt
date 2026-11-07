package com.neb.ians.speech

import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.nio.FloatBuffer
import java.nio.LongBuffer
import java.text.Normalizer
import java.util.Random
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.ln
import kotlin.math.max
import kotlin.math.sin
import kotlin.math.sqrt

/** On-device ONNX voices the user can download and remove. Nothing here is bundled. */
enum class LocalTtsId(val key: String, val dir: String) {
    Paradee("paradee", "paradee-8m"),
    LeokaniDala("leokani_dala", "leokani-dala"),
    LeokaniPono("leokani_pono", "leokani-pono"),
    Supertonic("supertonic", "supertonic-3");

    companion object {
        fun fromKey(key: String?): LocalTtsId? = values().firstOrNull { it.key == key }
    }
}

data class LocalVoice(val key: String, val label: String)

data class LocalTtsInfo(
    val id: LocalTtsId,
    val title: String,
    val meta: String,
    val files: List<ModelFile>,
    val voices: List<LocalVoice>,
    val sampleRate: Int,
) {
    val bytes: Long get() = files.sumOf { it.bytes }
    val defaultVoice: String get() = voices.first().key
}

object LocalTtsCatalog {
    private const val PARADEE = "https://huggingface.co/sahilmahendrakar/Paradee-8M-v1.2/resolve/main/"
    private const val LEOKANI = "https://huggingface.co/milliwattlabs/leokani-tts-7M/resolve/main/"
    private const val SUPERTONIC = "https://huggingface.co/Supertone/supertonic-3/resolve/main/"

    // English pronunciation dictionary shared by the two Kokoro-style models.
    private val cmuDict = ModelFile(
        "cmudict.dict", "https://huggingface.co/empero-ai/PiVo-1.4M/resolve/main/pivo/resources/cmudict.dict", 3_618_488L, shared = true,
    )

    private val supertonicVoices = listOf("M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5")

    val all: List<LocalTtsInfo> = listOf(
        LocalTtsInfo(
            id = LocalTtsId.Paradee,
            title = "Paradee 8M",
            meta = "English, 4 voices",
            files = listOf(
                ModelFile("config.json", PARADEE + "config.json", 1_827L),
                ModelFile("paradee_int8.onnx", PARADEE + "onnx/paradee_int8.onnx", 8_462_119L),
                cmuDict,
            ),
            voices = listOf(
                LocalVoice("af_heart", "Heart, American female"),
                LocalVoice("am_puck", "Puck, American male"),
                LocalVoice("bf_isabella", "Isabella, British female"),
                LocalVoice("bm_fable", "Fable, British male"),
            ),
            sampleRate = 24_000,
        ),
        LocalTtsInfo(
            id = LocalTtsId.LeokaniDala,
            title = "Leokani 7M, Dala",
            meta = "English, American female",
            files = listOf(
                ModelFile("config.json", LEOKANI + "config.json", 2_343L),
                ModelFile("model.onnx", LEOKANI + "leokani-tts-int8.onnx", 7_838_742L),
                cmuDict,
            ),
            voices = listOf(LocalVoice("dala", "Dala")),
            sampleRate = 24_000,
        ),
        LocalTtsInfo(
            id = LocalTtsId.LeokaniPono,
            title = "Leokani 7M, Pono",
            meta = "English, American male",
            files = listOf(
                ModelFile("config.json", LEOKANI + "pono/config.json", 2_361L),
                ModelFile("model.onnx", LEOKANI + "pono/leokani-tts.onnx", 28_418_086L),
                cmuDict,
            ),
            voices = listOf(LocalVoice("pono", "Pono")),
            sampleRate = 24_000,
        ),
        LocalTtsInfo(
            id = LocalTtsId.Supertonic,
            title = "Supertonic 3",
            meta = "31 languages, 10 voices",
            files = buildList {
                add(ModelFile("onnx/tts.json", SUPERTONIC + "onnx/tts.json", 8_253L))
                add(ModelFile("onnx/unicode_indexer.json", SUPERTONIC + "onnx/unicode_indexer.json", 277_676L))
                add(ModelFile("onnx/duration_predictor.onnx", SUPERTONIC + "onnx/duration_predictor.onnx", 3_700_147L))
                add(ModelFile("onnx/text_encoder.onnx", SUPERTONIC + "onnx/text_encoder.onnx", 36_416_150L))
                add(ModelFile("onnx/vector_estimator.onnx", SUPERTONIC + "onnx/vector_estimator.onnx", 256_534_781L))
                add(ModelFile("onnx/vocoder.onnx", SUPERTONIC + "onnx/vocoder.onnx", 101_424_195L))
                supertonicVoices.forEach { add(ModelFile("voice_styles/$it.json", SUPERTONIC + "voice_styles/$it.json", 292_000L)) }
            },
            voices = supertonicVoices.map { LocalVoice(it, if (it.startsWith("M")) "Male ${it.drop(1)}" else "Female ${it.drop(1)}") },
            sampleRate = 44_100,
        ),
    )

    fun info(id: LocalTtsId): LocalTtsInfo = all.first { it.id == id }
}

/**
 * Runs one local voice at a time. Every call happens on the read-aloud engine thread; the
 * model is opened on first use and closed when the engine releases it.
 */
class LocalTtsRunner {
    private val env: OrtEnvironment get() = OrtEnvironment.getEnvironment()
    private var openId: LocalTtsId? = null
    private var kokoro: KokoroModel? = null
    private var supertonic: SupertonicModel? = null

    var sampleRate: Int = 24_000
        private set

    fun open(id: LocalTtsId, dir: File, sharedDir: File) {
        if (openId == id) return
        close()
        val threads = (Runtime.getRuntime().availableProcessors() / 2).coerceIn(2, 4)
        val info = LocalTtsCatalog.info(id)
        when (id) {
            LocalTtsId.Paradee -> kokoro = KokoroModel(env, dir, File(sharedDir, "cmudict.dict"), "paradee_int8.onnx", threads, paradee = true, voices = info.voices.map { it.key })
            LocalTtsId.LeokaniDala, LocalTtsId.LeokaniPono ->
                kokoro = KokoroModel(env, dir, File(sharedDir, "cmudict.dict"), "model.onnx", threads, paradee = false, voices = emptyList())
            LocalTtsId.Supertonic -> supertonic = SupertonicModel(env, File(dir, "onnx"), File(dir, "voice_styles"), threads)
        }
        sampleRate = info.sampleRate.let { rate -> supertonic?.sampleRate ?: rate }
        openId = id
    }

    fun speak(text: String, voice: String, speed: Float, sink: PcmSink): Boolean {
        kokoro?.let { return it.speak(text, voice, speed, sink) }
        supertonic?.let { return it.speak(text, voice, speed, sink) }
        return false
    }

    fun close() {
        runCatching { kokoro?.close() }
        runCatching { supertonic?.close() }
        kokoro = null
        supertonic = null
        openId = null
    }
}

private fun OnnxTensor.floats(): FloatArray {
    val buf = floatBuffer
    val out = FloatArray(buf.remaining())
    buf.get(out)
    return out
}

private fun options(threads: Int) = OrtSession.SessionOptions().apply {
    setIntraOpNumThreads(threads)
    setInterOpNumThreads(1)
}

// ---------------------------------------------------------------------------------------------
// Paradee and Leokani: phonemes in, audio out. Both use Kokoro's phoneme set.
// ---------------------------------------------------------------------------------------------

private class KokoroModel(
    private val env: OrtEnvironment,
    dir: File,
    dictFile: File,
    modelName: String,
    threads: Int,
    private val paradee: Boolean,
    private val voices: List<String>,
) {
    private val session: OrtSession = env.createSession(File(dir, modelName).path, options(threads))
    private val vocab = HashMap<Int, Long>()
    private val phonemizer = EnglishPhonemizer(dictFile)
    private val maxIds = if (paradee) 500 else 400
    private val window = FloatArray(WIN) { i -> (0.5 - 0.5 * cos(2.0 * PI * i / WIN)).toFloat() }

    init {
        val vocabJson = JSONObject(File(dir, "config.json").readText()).getJSONObject("vocab")
        for (k in vocabJson.keys()) {
            if (k.isEmpty()) continue
            vocab[k.codePointAt(0)] = vocabJson.getLong(k)
        }
    }

    fun speak(text: String, voice: String, speed: Float, sink: PcmSink): Boolean {
        val voiceIndex = voices.indexOf(voice).coerceAtLeast(0).toLong()
        for (sentence in phonemizer.sentences(text)) {
            val phonemes = phonemizer.phonemes(sentence)
            val ids = ArrayList<Long>()
            phonemes.codePoints().forEach { cp -> vocab[cp]?.let { ids.add(it) } }
            for (chunk in split(ids)) {
                val audio = if (paradee) runParadee(chunk, voiceIndex, speed) else runLeokani(chunk, speed)
                if (audio.isNotEmpty() && !sink.onPcm(audio)) return true
            }
        }
        return true
    }

    private fun split(ids: List<Long>): List<List<Long>> {
        if (ids.isEmpty()) return emptyList()
        if (ids.size <= maxIds) return listOf(ids)
        val mid = ids.size / 2
        val comma = vocab[','.code]
        val space = vocab[' '.code]
        for (mark in listOf(comma, space)) {
            if (mark == null) continue
            var best = -1
            for (i in ids.indices) if (ids[i] == mark && (best < 0 || kotlin.math.abs(i - mid) < kotlin.math.abs(best - mid))) best = i
            if (best >= 0 && best + 1 < ids.size) return split(ids.subList(0, best + 1)) + split(ids.subList(best + 1, ids.size))
        }
        return split(ids.subList(0, mid)) + split(ids.subList(mid, ids.size))
    }

    private fun padded(chunk: List<Long>): LongArray {
        val arr = LongArray(chunk.size + 2)
        for (i in chunk.indices) arr[i + 1] = chunk[i]
        return arr
    }

    private fun runParadee(chunk: List<Long>, voice: Long, speed: Float): FloatArray {
        val ids = padded(chunk)
        val tIds = OnnxTensor.createTensor(env, LongBuffer.wrap(ids), longArrayOf(1, ids.size.toLong()))
        val tSpeed = OnnxTensor.createTensor(env, FloatBuffer.wrap(floatArrayOf(speed)), longArrayOf(1))
        val tVoice = OnnxTensor.createTensor(env, LongBuffer.wrap(longArrayOf(voice)), longArrayOf(1))
        try {
            val result = session.run(mapOf("input_ids" to tIds, "speed" to tSpeed, "voice" to tVoice))
            val audio = (result.get(0) as OnnxTensor).floats()
            result.close()
            return audio
        } finally {
            tIds.close(); tSpeed.close(); tVoice.close()
        }
    }

    private fun runLeokani(chunk: List<Long>, speed: Float): FloatArray {
        val ids = padded(chunk)
        val tIds = OnnxTensor.createTensor(env, LongBuffer.wrap(ids), longArrayOf(1, ids.size.toLong()))
        val tSpeed = OnnxTensor.createTensor(env, FloatBuffer.wrap(floatArrayOf(speed)), longArrayOf(1))
        try {
            val result = session.run(mapOf("ids" to tIds, "speed" to tSpeed))
            val mag = (result.get(0) as OnnxTensor).floats()
            val phase = (result.get(1) as OnnxTensor).floats()
            result.close()
            return istft(mag, phase, mag.size / BINS)
        } finally {
            tIds.close(); tSpeed.close()
        }
    }

    /** Magnitude and phase laid out [bin][frame] to audio, inverse of 'same'-padded frames. */
    private fun istft(mag: FloatArray, phase: FloatArray, frames: Int): FloatArray {
        if (frames <= 0) return FloatArray(0)
        val size = (frames - 1) * HOP + WIN
        val y = FloatArray(size)
        val norm = FloatArray(size)
        val re = DoubleArray(WIN)
        val im = DoubleArray(WIN)
        for (f in 0 until frames) {
            for (k in 0 until BINS) {
                val m = mag[k * frames + f].toDouble()
                val p = phase[k * frames + f].toDouble()
                re[k] = m * cos(p)
                im[k] = if (k == 0 || k == BINS - 1) 0.0 else m * sin(p)
            }
            for (k in 1 until BINS - 1) {
                re[WIN - k] = re[k]
                im[WIN - k] = -im[k]
            }
            // inverse FFT through the forward one: ifft(x) = conj(fft(conj(x))) / n, the output is real
            for (k in 0 until WIN) im[k] = -im[k]
            Fft.transform(re, im)
            val start = f * HOP
            for (n in 0 until WIN) {
                val w = window[n]
                y[start + n] += (re[n] / WIN).toFloat() * w
                norm[start + n] += w * w
            }
        }
        val out = FloatArray(frames * HOP)
        for (i in out.indices) out[i] = y[PAD + i] / max(norm[PAD + i], 1e-11f)
        return out
    }

    fun close() {
        session.close()
    }

    private companion object {
        const val WIN = 1024
        const val HOP = 300
        const val BINS = WIN / 2 + 1
        const val PAD = (WIN - HOP) / 2
    }
}

private object Fft {
    /** In-place radix-2 forward transform; the size must be a power of two. */
    fun transform(re: DoubleArray, im: DoubleArray) {
        val n = re.size
        var j = 0
        for (i in 1 until n) {
            var bit = n shr 1
            while (j and bit != 0) { j = j xor bit; bit = bit shr 1 }
            j = j xor bit
            if (i < j) {
                val tr = re[i]; re[i] = re[j]; re[j] = tr
                val ti = im[i]; im[i] = im[j]; im[j] = ti
            }
        }
        var len = 2
        while (len <= n) {
            val ang = -2.0 * PI / len
            val wr = cos(ang)
            val wi = sin(ang)
            var i = 0
            while (i < n) {
                var cr = 1.0
                var ci = 0.0
                for (k in 0 until len / 2) {
                    val a = i + k
                    val b = a + len / 2
                    val xr = re[b] * cr - im[b] * ci
                    val xi = re[b] * ci + im[b] * cr
                    re[b] = re[a] - xr; im[b] = im[a] - xi
                    re[a] += xr; im[a] += xi
                    val nr = cr * wr - ci * wi
                    ci = cr * wi + ci * wr
                    cr = nr
                }
                i += len
            }
            len = len shl 1
        }
    }
}

// ---------------------------------------------------------------------------------------------
// Supertonic 3: text goes in as characters, four graphs and a flow-matching loop make the audio.
// ---------------------------------------------------------------------------------------------

private class SupertonicModel(
    private val env: OrtEnvironment,
    onnxDir: File,
    private val stylesDir: File,
    threads: Int,
) {
    private val dp = env.createSession(File(onnxDir, "duration_predictor.onnx").path, options(threads))
    private val textEnc = env.createSession(File(onnxDir, "text_encoder.onnx").path, options(threads))
    private val estimator = env.createSession(File(onnxDir, "vector_estimator.onnx").path, options(threads))
    private val vocoder = env.createSession(File(onnxDir, "vocoder.onnx").path, options(threads))
    private val indexer: LongArray
    val sampleRate: Int
    private val baseChunk: Int
    private val compress: Int
    private val latentDim: Int
    private val rng = Random()
    private var styleName = ""
    private var styleTtl: OnnxTensor? = null
    private var styleDp: OnnxTensor? = null

    init {
        val cfg = JSONObject(File(onnxDir, "tts.json").readText())
        sampleRate = cfg.getJSONObject("ae").getInt("sample_rate")
        baseChunk = cfg.getJSONObject("ae").getInt("base_chunk_size")
        compress = cfg.getJSONObject("ttl").getInt("chunk_compress_factor")
        latentDim = cfg.getJSONObject("ttl").getInt("latent_dim")
        val arr = JSONArray(File(onnxDir, "unicode_indexer.json").readText())
        indexer = LongArray(arr.length()) { arr.getLong(it) }
    }

    fun speak(text: String, voice: String, speed: Float, sink: PcmSink): Boolean {
        useStyle(voice)
        val lang = if (text.any { it in '\u0900'..'\u097F' }) "hi" else "en"
        val gap = FloatArray((0.25f * sampleRate).toInt())
        var first = true
        for (chunk in chunkText(text, 300)) {
            val audio = infer(chunk, lang, speed * 1.05f)
            if (audio.isEmpty()) continue
            if (!first && !sink.onPcm(gap)) return true
            first = false
            if (!sink.onPcm(audio)) return true
        }
        return true
    }

    private fun useStyle(name: String) {
        val wanted = if (File(stylesDir, "$name.json").exists()) name else "M1"
        if (wanted == styleName && styleTtl != null) return
        styleTtl?.close(); styleDp?.close()
        val root = JSONObject(File(stylesDir, "$wanted.json").readText())
        styleTtl = tensorOf(root.getJSONObject("style_ttl"))
        styleDp = tensorOf(root.getJSONObject("style_dp"))
        styleName = wanted
    }

    private fun tensorOf(node: JSONObject): OnnxTensor {
        val dims = node.getJSONArray("dims")
        val shape = longArrayOf(dims.getLong(0), dims.getLong(1), dims.getLong(2))
        val flat = FloatArray((shape[0] * shape[1] * shape[2]).toInt())
        var idx = 0
        val data = node.getJSONArray("data")
        for (a in 0 until data.length()) {
            val rows = data.getJSONArray(a)
            for (b in 0 until rows.length()) {
                val vals = rows.getJSONArray(b)
                for (c in 0 until vals.length()) flat[idx++] = vals.getDouble(c).toFloat()
            }
        }
        return OnnxTensor.createTensor(env, FloatBuffer.wrap(flat), shape)
    }

    private fun infer(text: String, lang: String, speed: Float): FloatArray {
        val ids = ArrayList<Long>()
        preprocess(text, lang).codePoints().forEach { cp -> if (cp < indexer.size && indexer[cp] >= 0) ids.add(indexer[cp]) }
        if (ids.isEmpty()) return FloatArray(0)
        val n = ids.size
        val tIds = OnnxTensor.createTensor(env, LongBuffer.wrap(ids.toLongArray()), longArrayOf(1, n.toLong()))
        val tMask = OnnxTensor.createTensor(env, FloatBuffer.wrap(FloatArray(n) { 1f }), longArrayOf(1, 1, n.toLong()))
        val ttl = styleTtl!!
        val dpStyle = styleDp!!
        var textEmb: OrtSession.Result? = null
        var tTotal: OnnxTensor? = null
        try {
            val duration = dp.run(mapOf("text_ids" to tIds, "style_dp" to dpStyle, "text_mask" to tMask)).use { r ->
                (r.get(0) as OnnxTensor).floats()[0] / speed
            }
            if (!(duration > 0f)) return FloatArray(0)
            textEmb = textEnc.run(mapOf("text_ids" to tIds, "style_ttl" to ttl, "text_mask" to tMask))
            val emb = textEmb.get(0) as OnnxTensor

            val wavLen = (duration * sampleRate).toLong()
            val chunkSize = (baseChunk * compress).toLong()
            val latentLen = ((wavLen + chunkSize - 1) / chunkSize).toInt().coerceAtLeast(1)
            val dim = latentDim * compress
            var xt = FloatArray(dim * latentLen) { gauss() }
            val latentMask = FloatArray(latentLen) { 1f }
            val steps = TOTAL_STEPS
            val totalT = OnnxTensor.createTensor(env, FloatBuffer.wrap(floatArrayOf(steps.toFloat())), longArrayOf(1))
            tTotal = totalT
            val shape = longArrayOf(1, dim.toLong(), latentLen.toLong())
            for (step in 0 until steps) {
                val tNoisy = OnnxTensor.createTensor(env, FloatBuffer.wrap(xt), shape)
                val tLatentMask = OnnxTensor.createTensor(env, FloatBuffer.wrap(latentMask), longArrayOf(1, 1, latentLen.toLong()))
                val tStep = OnnxTensor.createTensor(env, FloatBuffer.wrap(floatArrayOf(step.toFloat())), longArrayOf(1))
                try {
                    xt = estimator.run(
                        mapOf(
                            "noisy_latent" to tNoisy, "text_emb" to emb, "style_ttl" to ttl,
                            "latent_mask" to tLatentMask, "text_mask" to tMask,
                            "current_step" to tStep, "total_step" to totalT,
                        )
                    ).use { r -> (r.get(0) as OnnxTensor).floats() }
                } finally {
                    tNoisy.close(); tLatentMask.close(); tStep.close()
                }
            }
            val tLatent = OnnxTensor.createTensor(env, FloatBuffer.wrap(xt), shape)
            try {
                val wav = vocoder.run(mapOf("latent" to tLatent)).use { r -> (r.get(0) as OnnxTensor).floats() }
                return if (wav.size > wavLen) wav.copyOf(wavLen.toInt()) else wav
            } finally {
                tLatent.close()
            }
        } finally {
            tIds.close(); tMask.close(); tTotal?.close(); textEmb?.close()
        }
    }

    private fun gauss(): Float {
        val u1 = max(1e-10, rng.nextDouble())
        val u2 = rng.nextDouble()
        return (sqrt(-2.0 * ln(u1)) * cos(2.0 * PI * u2)).toFloat()
    }

    private fun preprocess(raw: String, lang: String): String {
        var t = Normalizer.normalize(raw, Normalizer.Form.NFKD)
        val sb = StringBuilder()
        t.codePoints().forEach { cp ->
            val emoji = cp in 0x1F000..0x1FAFF || cp in 0x2600..0x27BF
            if (!emoji) sb.appendCodePoint(cp)
        }
        t = sb.toString()
        val map = mapOf(
            "\u2013" to "-", "\u2011" to "-", "\u2014" to "-", "_" to " ", "\u201C" to "\"", "\u201D" to "\"",
            "\u2018" to "'", "\u2019" to "'", "\u00B4" to "'", "`" to "'", "[" to " ", "]" to " ", "|" to " ",
            "/" to " ", "#" to " ", "\u2192" to " ", "\u2190" to " ", "@" to " at ",
        )
        for ((a, b) in map) t = t.replace(a, b)
        t = t.replace(Regex("[\u2665\u2606\u2661\u00A9\\\\]"), "")
        t = t.replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?").replace(" ;", ";").replace(" :", ":")
        t = t.replace(Regex("\\s+"), " ").trim()
        if (t.isNotEmpty() && !Regex(".*[.!?;:,'\"\u201C\u201D\u2018\u2019)\\]}\u2026\u3002]$").matches(t)) t += "."
        return "<$lang>$t</$lang>"
    }

    private fun chunkText(text: String, maxLen: Int): List<String> {
        val out = ArrayList<String>()
        for (para in text.trim().split(Regex("\\n\\s*\\n"))) {
            val p = para.trim()
            if (p.isEmpty()) continue
            if (p.length <= maxLen) { out.add(p); continue }
            val cur = StringBuilder()
            for (sentence in p.split(Regex("(?<=[.!?])\\s+"))) {
                var s = sentence.trim()
                if (s.isEmpty()) continue
                while (s.length > maxLen) {
                    var cut = s.lastIndexOf(' ', maxLen)
                    if (cut <= 0) cut = maxLen
                    if (cur.isNotEmpty()) { out.add(cur.toString()); cur.setLength(0) }
                    out.add(s.substring(0, cut).trim())
                    s = s.substring(cut).trim()
                }
                if (cur.isNotEmpty() && cur.length + s.length + 1 > maxLen) { out.add(cur.toString()); cur.setLength(0) }
                if (cur.isNotEmpty()) cur.append(' ')
                cur.append(s)
            }
            if (cur.isNotEmpty()) out.add(cur.toString())
        }
        return out
    }

    fun close() {
        styleTtl?.close(); styleDp?.close()
        dp.close(); textEnc.close(); estimator.close(); vocoder.close()
    }

    private companion object {
        const val TOTAL_STEPS = 8
    }
}

// ---------------------------------------------------------------------------------------------
// English front end for the Kokoro-style models: CMU dictionary to Kokoro phonemes.
// ---------------------------------------------------------------------------------------------

internal class EnglishPhonemizer(dictFile: File) {
    private val dict = HashMap<String, String>(140_000)

    init {
        dictFile.bufferedReader().useLines { lines ->
            for (line in lines) {
                if (line.isEmpty() || line[0] == ';') continue
                val sp = line.indexOf(' ')
                if (sp <= 0) continue
                val word = line.substring(0, sp)
                if (word.endsWith(")")) continue
                dict.putIfAbsent(word, line.substring(sp + 1).substringBefore('#').trim())
            }
        }
    }

    fun sentences(text: String): List<String> =
        text.replace('\n', ' ').split(Regex("(?<=[.!?])\\s+")).map { it.trim() }.filter { it.isNotEmpty() }

    fun phonemes(sentence: String): String {
        val out = StringBuilder()
        val token = Regex("[A-Za-z]+(?:'[A-Za-z]+)*|\\d+(?:[.,]\\d+)*(?:st|nd|rd|th)?|[^\\sA-Za-z\\d]")
        var needSpace = false
        for (m in token.findAll(sentence)) {
            val t = m.value
            when {
                t[0].isLetter() -> { if (needSpace) out.append(' '); out.append(word(t.lowercase())); needSpace = true }
                t[0].isDigit() -> {
                    for (w in NumberWords.say(t)) { if (needSpace) out.append(' '); out.append(word(w)); needSpace = true }
                }
                t == "," || t == "." || t == ";" || t == ":" || t == "!" || t == "?" -> { out.append(t); needSpace = true }
                t == "-" || t == "\u2014" || t == "\u2013" -> { out.append(" "); needSpace = false }
                t == "%" -> { if (needSpace) out.append(' '); out.append(word("percent")); needSpace = true }
                t == "&" -> { if (needSpace) out.append(' '); out.append(word("and")); needSpace = true }
                t == "+" -> { if (needSpace) out.append(' '); out.append(word("plus")); needSpace = true }
                t == "=" -> { if (needSpace) out.append(' '); out.append(word("equals")); needSpace = true }
                else -> {}
            }
        }
        return out.toString().trim()
    }

    private fun word(w: String): String {
        val key = w.replace("'", "").let { if (dict.containsKey(w)) w else it }
        val direct = dict[w] ?: dict[key]
        if (direct != null) return convert(direct)
        // possessives and plurals of known words
        if (w.endsWith("'s") || w.endsWith("s'")) dict[w.dropLast(2).ifEmpty { w }]?.let { return convert(it) + "z" }
        if (w.length > 3 && w.endsWith("s")) dict[w.dropLast(1)]?.let { return convert(it) + sibilantEnding(it) }
        if (w.length > 4 && w.endsWith("ed")) dict[w.dropLast(2)]?.let { return convert(it) + edEnding(it) }
        if (w.length > 4 && w.endsWith("ing")) dict[w.dropLast(3)]?.let { return convert(it) + "ɪŋ" }
        if (w.length > 4 && w.endsWith("ly")) dict[w.dropLast(2)]?.let { return convert(it) + "li" }
        return convert(guess(w))
    }

    private fun sibilantEnding(p: String): String {
        val last = p.trim().split(' ').last()
        return when (last) {
            "S", "Z", "SH", "ZH", "CH", "JH" -> "ᵻz"
            "P", "T", "K", "F", "TH" -> "s"
            else -> "z"
        }
    }

    private fun edEnding(p: String): String {
        val last = p.trim().split(' ').last()
        return when (last) {
            "T", "D" -> "ᵻd"
            "P", "K", "F", "S", "SH", "CH", "TH" -> "t"
            else -> "d"
        }
    }

    /** Last resort for names and new words: spell the sounds out from the letters. */
    private fun guess(w: String): String {
        val out = ArrayList<String>()
        var i = 0
        while (i < w.length) {
            val two = if (i + 1 < w.length) w.substring(i, i + 2) else ""
            val hit = DIGRAPHS[two]
            if (hit != null) { out.addAll(hit); i += 2; continue }
            val c = w[i]
            if (c == 'e' && i == w.lastIndex && w.length > 2) {
                // a final e is silent
            } else if (c == 'y') {
                out.add(if (i == 0) "Y" else "IY0")
            } else if (c == 'c') {
                out.add(if (i + 1 < w.length && w[i + 1] in "eiy") "S" else "K")
            } else if (c == 'x') {
                out.add("K")
                out.add("S")
            } else {
                val sound = LETTERS[c]
                if (sound != null) out.add(sound)
            }
            i++
        }
        return out.joinToString(" ")
    }

    private fun convert(arpa: String): String {
        val sb = StringBuilder()
        for (raw in arpa.trim().split(' ')) {
            if (raw.isEmpty()) continue
            val stress = raw.lastOrNull()?.takeIf { it.isDigit() }
            val ph = if (stress != null) raw.dropLast(1) else raw
            val vowel = VOWELS[ph]
            if (vowel != null) {
                when (stress) { '1' -> sb.append('ˈ'); '2' -> sb.append('ˌ') }
                sb.append(
                    when {
                        ph == "AH" && (stress == '0' || stress == null) -> "ə"
                        ph == "ER" && (stress == '0' || stress == null) -> "ɚ"
                        else -> vowel
                    }
                )
            } else {
                sb.append(CONSONANTS[ph] ?: "")
            }
        }
        return sb.toString()
    }

    private companion object {
        val VOWELS = mapOf(
            "AA" to "ɑ", "AE" to "æ", "AH" to "ʌ", "AO" to "ɔ", "AW" to "W", "AY" to "I", "EH" to "ɛ",
            "ER" to "ɜɹ", "EY" to "A", "IH" to "ɪ", "IY" to "i", "OW" to "O", "OY" to "Y", "UH" to "ʊ", "UW" to "u",
        )
        val CONSONANTS = mapOf(
            "B" to "b", "CH" to "ʧ", "D" to "d", "DH" to "ð", "F" to "f", "G" to "ɡ", "HH" to "h", "JH" to "ʤ",
            "K" to "k", "L" to "l", "M" to "m", "N" to "n", "NG" to "ŋ", "P" to "p", "R" to "ɹ", "S" to "s",
            "SH" to "ʃ", "T" to "t", "TH" to "θ", "V" to "v", "W" to "w", "Y" to "j", "Z" to "z", "ZH" to "ʒ",
        )
        val LETTERS = mapOf(
            'a' to "AE1", 'e' to "EH1", 'i' to "IH1", 'o' to "AA1", 'u' to "AH1", 'b' to "B", 'd' to "D", 'f' to "F",
            'g' to "G", 'h' to "HH", 'j' to "JH", 'k' to "K", 'l' to "L", 'm' to "M", 'n' to "N", 'p' to "P",
            'q' to "K", 'r' to "R", 's' to "S", 't' to "T", 'v' to "V", 'w' to "W", 'z' to "Z",
        )
        val DIGRAPHS = mapOf(
            "sh" to listOf("SH"), "ch" to listOf("CH"), "th" to listOf("TH"), "ph" to listOf("F"), "ck" to listOf("K"),
            "ng" to listOf("NG"), "qu" to listOf("K", "W"), "wh" to listOf("W"), "ee" to listOf("IY1"), "ea" to listOf("IY1"),
            "oo" to listOf("UW1"), "ai" to listOf("EY1"), "ay" to listOf("EY1"), "oa" to listOf("OW1"), "ou" to listOf("AW1"),
            "ow" to listOf("OW1"), "oi" to listOf("OY1"), "oy" to listOf("OY1"), "ie" to listOf("IY1"), "au" to listOf("AO1"),
        )
    }
}

internal object NumberWords {
    private val ones = listOf(
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
    )
    private val tens = listOf("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")
    private val scales = listOf("", "thousand", "million", "billion", "trillion")

    /** "42", "3.5", "1,200", "1984", "21st" to spoken words. */
    fun say(token: String): List<String> {
        val ordinal = Regex("(st|nd|rd|th)$").containsMatchIn(token)
        val core = token.replace(Regex("(st|nd|rd|th)$"), "").replace(",", "")
        val parts = core.split('.')
        val whole = parts[0]
        val words = ArrayList<String>()
        if (whole.length == 4 && !ordinal && parts.size == 1 && whole.toInt() in 1100..2099 && whole.toInt() % 1000 >= 10) {
            words.addAll(below100(whole.substring(0, 2).toInt()))
            val tail = whole.substring(2).toInt()
            if (tail == 0) words.add("hundred") else if (tail < 10) { words.add("oh"); words.add(ones[tail]) } else words.addAll(below100(tail))
            return words
        }
        if (whole.length > 15) return whole.map { ones[it - '0'] }
        words.addAll(cardinal(whole.toLong()))
        if (ordinal && words.isNotEmpty()) words[words.lastIndex] = ordinalWord(words.last())
        if (parts.size == 2 && parts[1].isNotEmpty()) {
            words.add("point")
            parts[1].forEach { words.add(ones[it - '0']) }
        }
        return words
    }

    private fun ordinalWord(w: String): String = when (w) {
        "one" -> "first"; "two" -> "second"; "three" -> "third"; "five" -> "fifth"; "eight" -> "eighth"
        "nine" -> "ninth"; "twelve" -> "twelfth"
        else -> if (w.endsWith("y")) w.dropLast(1) + "ieth" else w + "th"
    }

    private fun below100(n: Int): List<String> =
        if (n < 20) listOf(ones[n]) else if (n % 10 == 0) listOf(tens[n / 10]) else listOf(tens[n / 10], ones[n % 10])

    private fun below1000(n: Int): List<String> {
        val out = ArrayList<String>()
        if (n >= 100) { out.add(ones[n / 100]); out.add("hundred") }
        if (n % 100 != 0) out.addAll(below100(n % 100))
        return out
    }

    private fun cardinal(n: Long): List<String> {
        if (n == 0L) return listOf("zero")
        val out = ArrayList<String>()
        var rest = n
        val groups = ArrayList<Int>()
        while (rest > 0) { groups.add((rest % 1000).toInt()); rest /= 1000 }
        for (i in groups.indices.reversed()) {
            if (groups[i] == 0) continue
            out.addAll(below1000(groups[i]))
            if (scales[i].isNotEmpty()) out.add(scales[i])
        }
        return out
    }
}
