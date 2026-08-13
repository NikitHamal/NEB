package com.neb.ians.data.repository

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

/**
 * Downloads the Needle 2 on-device model assets from the NEBians cloud and
 * stores them in app-private storage so the APK stays small (the ~14 MB model
 * is NOT bundled). Everything needed for offline inference lives in
 * `filesDir/needle/`: the engine glue (`needle.js`), the engine (`needle.wasm`)
 * and the weights (`needle2.cact`), plus the tiny `bridge.html` that drives them.
 *
 * The three binary assets are the exact files the website ships under
 * `/static/web/js/needle2/`, so the Android app runs the same engine + model as
 * the browser (just inside a WebView instead of a Web Worker).
 *
 * A `complete.v<N>` marker + byte-size checks make the download idempotent:
 * re-opening the screen after it's downloaded loads straight from storage and
 * works fully offline.
 */
class LocalNebyModelManager(private val context: Context) {

    companion object {
        const val CLOUD_BASE = "https://nebians.consica.com.np/static/web/js/needle2/"
        /** Bump when the model/engine changes so users re-download once. */
        const val ASSET_VERSION = 3

        /** Filename -> expected byte size (integrity check). */
        val FILES: List<Pair<String, Long>> = listOf(
            "needle.js" to 62433L,
            "needle.wasm" to 314737L,
            "needle2.cact" to 13737679L,
        )

        const val BRIDGE_HTML = "bridge.html"
        private const val MARKER = "complete.v$ASSET_VERSION"
    }

    val assetDir: File
        get() = File(context.filesDir, "needle")

    /** True when all assets are present, match expected sizes, and the version marker exists. */
    fun isReady(): Boolean {
        val dir = assetDir
        if (!dir.isDirectory) return false
        if (!File(dir, MARKER).exists()) return false
        return FILES.all { (name, size) ->
            val f = File(dir, name)
            f.isFile && f.length() == size
        }
    }

    /** Total byte size of the downloadable assets (for the setup UI). */
    fun totalBytes(): Long = FILES.sumOf { it.second }

    /**
     * Downloads (or verifies) every asset. `onProgress` receives 0..100.
     * Idempotent: files that already match the expected size are skipped.
     * Writes [BRIDGE_HTML] and the completion marker on success.
     */
    suspend fun download(onProgress: (Int) -> Unit): Result<Unit> = withContext(Dispatchers.IO) {
        runCatching {
            val dir = assetDir
            dir.mkdirs()

            FILES.forEachIndexed { i, (name, size) ->
                val target = File(dir, name)
                if (target.isFile && target.length() == size) {
                    onProgress(((i + 1) * 100) / FILES.size)
                    return@forEachIndexed
                }
                downloadOne(name, size, target, i, onProgress)
            }

            File(dir, BRIDGE_HTML).writeText(BRIDGE_HTML_SOURCE)
            File(dir, MARKER).writeText("ok")
        }
    }

    private fun downloadOne(name: String, size: Long, target: File, index: Int, onProgress: (Int) -> Unit) {
        val part = File(target.parentFile, "$name.part")
        val base = index * 100 / FILES.size
        val span = 100 / FILES.size
        val connection = URL(CLOUD_BASE + name).openConnection() as HttpURLConnection
        try {
            connection.connectTimeout = 20_000
            connection.readTimeout = 40_000
            connection.instanceFollowRedirects = true
            connection.connect()
            if (connection.responseCode !in 200..299) {
                throw IOException("HTTP ${connection.responseCode} while downloading $name")
            }
            val total = connection.contentLengthLong.let { if (it > 0) it else size }
            val input = connection.inputStream
            val output = part.outputStream()
            val buffer = ByteArray(64 * 1024)
            var read = 0L
            try {
                while (true) {
                    val n = input.read(buffer)
                    if (n < 0) break
                    output.write(buffer, 0, n)
                    read += n
                    val pct = (base + (read.toDouble() / total * span)).toInt().coerceIn(base, base + span)
                    onProgress(pct.coerceIn(0, 100))
                }
            } finally {
                input.close()
                output.close()
            }
            if (part.length() != size) {
                throw IOException("Size mismatch for $name: expected $size bytes, got ${part.length()}")
            }
            if (target.exists()) target.delete()
            if (!part.renameTo(target)) {
                throw IOException("Could not finalize $name")
            }
            onProgress(((index + 1) * 100) / FILES.size)
        } finally {
            connection.disconnect()
        }
    }

    fun delete() {
        val dir = assetDir
        if (dir.exists()) dir.deleteRecursively()
    }

    /** The tiny HTML/JS page that loads the WASM engine + weights and exposes
     *  the inference entry point to the Kotlin bridge. Served from app-private
     *  storage via [androidx.webkit.WebViewAssetLoader]. */
    private val BRIDGE_HTML_SOURCE: String = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body><script src="needle.js"></script>
<script>
var NEBY_TOOLS = [
  {"name":"search_resources","description":"Search for study resources on NEBians - notes, past papers, textbooks, PDFs.","parameters":{"type":"object","properties":{"query":{"type":"string","description":"search keywords"},"subject":{"type":"string","description":"subject name e.g. Mathematics, Physics, English"},"resource_type":{"type":"string","enum":["PDF","Note","Video","Link",""],"description":"optional type filter"}},"required":["query"]}},
  {"name":"find_notes","description":"Find study notes or past exam papers for a specific subject and grade on NEBians.","parameters":{"type":"object","properties":{"subject":{"type":"string","description":"subject name e.g. Mathematics, Physics, Chemistry"},"grade_level":{"type":"string","description":"e.g. Class 11, Class 12, SEE"},"exam_type":{"type":"string","enum":["Notes","Board","Final","SEE","Mock","Reference",""],"description":"type of material"}},"required":[]}},
  {"name":"get_forum_posts","description":"Get forum posts from the NEBians discussion forum.","parameters":{"type":"object","properties":{"category":{"type":"string","description":"category to filter e.g. Science, Math, Help, General"},"sort":{"type":"string","enum":["recent","popular"],"description":"sort order"}},"required":[]}},
  {"name":"navigate_to","description":"Navigate the user to a specific page on NEBians.","parameters":{"type":"object","properties":{"page":{"type":"string","enum":["home","library","forum","search","news","settings","bookmarks","upload","results","leaderboard","tools"],"description":"destination page"}},"required":["page"]}},
  {"name":"get_subjects","description":"List all available subjects on NEBians.","parameters":{"type":"object","properties":{},"required":[]}}
];
var __runtime = null, __outPtr = 0, __max = 128;
function __alloc(s) {
  var b = new TextEncoder().encode(s);
  var p = __runtime._malloc(b.length + 1);
  __runtime.HEAPU8.set(b, p);
  __runtime.HEAPU8[p + b.length] = 0;
  return p;
}
async function __init() {
  var t0 = performance.now();
  var wasm = new Uint8Array(await (await fetch('needle.wasm')).arrayBuffer());
  var model = new Uint8Array(await (await fetch('needle2.cact')).arrayBuffer());
  __runtime = await createNeedle({ wasmBinary: wasm });
  var mp = __runtime._malloc(model.length);
  __runtime.HEAPU8.set(model, mp);
  if (__runtime._needle_load(mp, BigInt(model.length)) !== 0) throw new Error('model load failed');
  var sp = __alloc(''); var tp = __alloc(JSON.stringify(NEBY_TOOLS));
  if (__runtime._needle_init(sp, tp) < 0) throw new Error('tool init failed');
  __outPtr = __runtime._malloc(16384);
  var secs = ((performance.now() - t0) / 1000).toFixed(1);
  NebyBridge.onReady(secs);
}
function __run(query) {
  try {
    __runtime._needle_reset();
    var qp = __alloc(query);
    __runtime._needle_complete(qp, __max, __outPtr, 16384);
    var out = __runtime.UTF8ToString(__outPtr);
    __runtime._free(qp);
    NebyBridge.onResult(out);
  } catch (e) {
    NebyBridge.onError(String(e));
  }
}
__init().catch(function (e) { NebyBridge.onError(String(e)); });
</script></body></html>
    """.trimIndent()
}
