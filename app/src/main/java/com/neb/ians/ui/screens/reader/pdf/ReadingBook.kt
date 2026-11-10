package com.neb.ians.ui.screens.reader.pdf

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Color as AColor
import android.os.Handler
import android.os.Looper
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsIgnoringVisibility
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsIgnoringVisibility
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.FormatSize
import androidx.compose.material.icons.outlined.Fullscreen
import androidx.compose.material.icons.outlined.FullscreenExit
import androidx.compose.material.icons.outlined.KeyboardArrowDown
import androidx.compose.material.icons.outlined.KeyboardArrowUp
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.Pause
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.TextDecrease
import androidx.compose.material.icons.outlined.TextIncrease
import androidx.compose.material.icons.outlined.Toc
import androidx.compose.material.icons.outlined.VolumeUp
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.neb.ians.R
import com.neb.ians.ui.components.NebDropdownMenu
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import org.json.JSONObject
import org.json.JSONTokener
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.util.zip.GZIPInputStream
import kotlin.math.roundToInt

/** The payload the print pipeline attaches to a book, and how it is unpacked. */
internal object ReadingBookFiles {
    const val ATTACHMENT = "neb-reading.tgz"

    /** Unpack the solid tar.gz into [dest] (written beside it and renamed, so a half unpacked book is never used). */
    fun unpack(bytes: ByteArray, dest: File): File {
        val tmp = File(dest.parentFile, dest.name + ".part")
        tmp.deleteRecursively(); tmp.mkdirs()
        val root = tmp.canonicalPath + File.separator
        GZIPInputStream(bytes.inputStream().buffered(1 shl 16)).use { gz ->
            val h = ByteArray(512)
            while (readFully(gz, h)) {
                if (h.all { it == 0.toByte() }) break
                val name = cstr(h, 0, 100)
                val prefix = cstr(h, 345, 155)
                val size = cstr(h, 124, 12).trim().ifEmpty { "0" }.toLong(8)
                val type = h[156].toInt().toChar()
                val out = File(tmp, if (prefix.isNotEmpty()) "$prefix/$name" else name)
                if ((type == '0' || type == '\u0000') && out.canonicalPath.startsWith(root)) {
                    out.parentFile?.mkdirs()
                    FileOutputStream(out).use { o ->
                        var left = size
                        val buf = ByteArray(64 * 1024)
                        while (left > 0) {
                            val n = gz.read(buf, 0, minOf(buf.size.toLong(), left).toInt())
                            if (n < 0) break
                            o.write(buf, 0, n); left -= n
                        }
                    }
                } else skip(gz, size)
                val pad = (512 - size % 512) % 512
                skip(gz, pad)
            }
        }
        dest.deleteRecursively()
        check(tmp.renameTo(dest)) { "reading book: rename failed" }
        return dest
    }

    private fun cstr(b: ByteArray, off: Int, len: Int): String {
        var e = off
        while (e < off + len && b[e] != 0.toByte()) e++
        return String(b, off, e - off, Charsets.UTF_8)
    }

    private fun readFully(i: InputStream, b: ByteArray): Boolean {
        var n = 0
        while (n < b.size) { val r = i.read(b, n, b.size - n); if (r < 0) return false; n += r }
        return true
    }

    private fun skip(i: InputStream, count: Long) {
        var left = count
        val buf = ByteArray(8192)
        while (left > 0) { val r = i.read(buf, 0, minOf(buf.size.toLong(), left).toInt()); if (r < 0) return; left -= r }
    }
}

/** Where a book's own structure stands: not looked for yet, absent (reflow the page instead) or unpacked. */
sealed interface BookState {
    data object Loading : BookState
    data object None : BookState
    data class Ready(val dir: File) : BookState
}

/** Talks to the reader page. Calls made before the page has loaded wait for it. */
internal class RdBookController {
    var web: WebView? = null
    private val pending = ArrayList<String>()
    var ready = false
    var speakText: ((String) -> Unit)? = null

    fun run(js: String) {
        val w = web
        if (w == null || !ready) { pending.add(js); return }
        w.evaluateJavascript(js, null)
    }

    fun eval(js: String, done: (String?) -> Unit) {
        val w = web ?: return done(null)
        w.evaluateJavascript(js) { raw -> done(raw?.let { runCatching { JSONTokener(it).nextValue() as? String }.getOrNull() }) }
    }

    fun flush() { ready = true; val w = web ?: return; pending.forEach { w.evaluateJavascript(it, null) }; pending.clear() }
}

private const val HOST = "reader.nebians.local"

private fun mime(path: String) = when (path.substringAfterLast('.', "").lowercase()) {
    "html" -> "text/html"; "css" -> "text/css"; "js" -> "application/javascript"; "json" -> "application/json"
    "svg" -> "image/svg+xml"; "jpg", "jpeg" -> "image/jpeg"; "png" -> "image/png"; "ttf" -> "font/ttf"; else -> "application/octet-stream"
}

private val FONTS = mapOf(
    "poppins_regular.ttf" to R.font.poppins_regular, "poppins_medium.ttf" to R.font.poppins_medium,
    "poppins_semibold.ttf" to R.font.poppins_semibold, "poppins_bold.ttf" to R.font.poppins_bold
)

private fun serve(context: Context, dir: File, path: String): WebResourceResponse? {
    val p = path.trimStart('/').ifEmpty { "index.html" }
    val stream: InputStream? = runCatching {
        when {
            p.startsWith("f/") -> FONTS[p.removePrefix("f/")]?.let { context.resources.openRawResource(it) }
            p == "index.html" || p == "reader.css" || p == "reader.js" || p == "book.css" -> context.assets.open("reader/$p")
            p == "meta.json" || p.startsWith("c/") || p.startsWith("r/") -> {
                val f = File(dir, p)
                if (f.canonicalPath.startsWith(dir.canonicalPath + File.separator) && f.isFile) f.inputStream() else null
            }
            else -> null
        }
    }.getOrNull()
    if (stream == null) return WebResourceResponse("text/plain", "utf-8", 404, "Not found", emptyMap(), "".byteInputStream())
    val enc = if (mime(p).startsWith("text") || p.endsWith(".json") || p.endsWith(".js") || p.endsWith(".svg")) "utf-8" else null
    return WebResourceResponse(mime(p), enc, 200, "OK", mapOf("Cache-Control" to "max-age=3600"), stream)
}

private fun settingsJs(s: ReadingSettings, theme: ReadingTheme, top: Int, bottom: Int): String {
    val o = JSONObject()
    o.put("theme", theme.name.lowercase()); o.put("scale", s.fontScale.toDouble()); o.put("line", s.lineSpacing.toDouble())
    o.put("margin", s.margin); o.put("font", if (s.font == ReadingFont.Serif) "serif" else "sans"); o.put("justify", s.justify)
    o.put("hide", s.hideAnswers); o.put("top", top); o.put("bottom", bottom); o.put("accent", "#0058DF")
    return o.toString()
}

/**
 * Reading mode for a book that carries its own structure: the book's HTML in a WebView (real tables,
 * choices, formulas as typeset vectors, folded solutions), with the same bars, sheet and controls as the
 * reflowed view. Page numbers are the PDF's, so the slider, bookmarks and "original page" agree.
 */
@Composable
internal fun ReadingBookMode(
    title: String,
    pageCount: Int,
    startPage: Int,
    jump: ReadJump?,
    settings: ReadingSettings,
    theme: ReadingTheme,
    look: ReaderLook,
    dir: File,
    bookmarked: Boolean,
    chromeVisible: Boolean,
    assistantHidden: Boolean,
    chapterTitle: (Int) -> String?,
    onChromeToggle: () -> Unit,
    onPage: (Int) -> Unit,
    onBack: () -> Unit,
    onToggleBookmark: () -> Unit,
    onContents: () -> Unit,
    onTypography: () -> Unit,
    onOriginal: (Int) -> Unit,
    onZen: () -> Unit,
    onToggleAssistant: () -> Unit,
    onFontScale: (Float) -> Unit,
    onOpenLink: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val palette = remember(theme, look) { readingPalette(theme, look) }
    val ctrl = remember { RdBookController() }
    val main = remember { Handler(Looper.getMainLooper()) }
    val density = LocalDensity.current
    val topInset = WindowInsets.statusBarsIgnoringVisibility.asPaddingValues().calculateTopPadding()
    val bottomInset = WindowInsets.navigationBarsIgnoringVisibility.asPaddingValues().calculateBottomPadding()
    val topPx = (topInset + ReaderBarHeight).value.roundToInt()
    val bottomPx = (bottomInset + 110.dp).value.roundToInt()
    val zen = settings.zen

    var page by remember { mutableIntStateOf(startPage.coerceIn(0, (pageCount - 1).coerceAtLeast(0))) }
    var viewer by remember { mutableStateOf(false) }
    var searching by remember { mutableStateOf(false) }
    var query by remember { mutableStateOf("") }
    var hitCount by remember { mutableIntStateOf(0) }
    var hitIndex by remember { mutableIntStateOf(-1) }
    var listening by remember { mutableStateOf(false) }
    val showBars = (chromeVisible && !zen) || searching

    val cbPage by rememberUpdatedState(onPage)
    val cbTap by rememberUpdatedState(onChromeToggle)
    val cbScale by rememberUpdatedState(onFontScale)
    val cbOrig by rememberUpdatedState(onOriginal)
    val cbLink by rememberUpdatedState(onOpenLink)
    val showBarsNow by rememberUpdatedState(showBars)
    val listeningNow by rememberUpdatedState(listening)
    val startNow by rememberUpdatedState(page)
    val settingsNow by rememberUpdatedState(settingsJs(settings, theme, topPx, bottomPx))

    val speaker = remember(ctrl) { RdSpeaker(context) { if (listeningNow) speakNext(ctrl) { listening = false } } }
    ctrl.speakText = { speaker.speak(it) }
    DisposableEffect(Unit) { onDispose { speaker.shutdown(); ctrl.web?.destroy(); ctrl.web = null } }

    val bridge = remember(ctrl) {
        object {
            @JavascriptInterface fun onPage(p: Int) { main.post { page = (p - 1).coerceAtLeast(0); cbPage(page) } }
            @JavascriptInterface fun onTap(frac: Double) {
                main.post {
                    val w = ctrl.web
                    if (!showBarsNow && frac < 0.18) w?.evaluateJavascript("NebReader.scrollPage(-1)", null)
                    else if (!showBarsNow && frac > 0.82) w?.evaluateJavascript("NebReader.scrollPage(1)", null)
                    else cbTap()
                }
            }
            @JavascriptInterface fun onFontScale(v: Double) { main.post { cbScale(((v * 20).roundToInt() / 20f)) } }
            @JavascriptInterface fun onReady() {}
            @JavascriptInterface fun onMeta(json: String) {}
            @JavascriptInterface fun onSearch(count: Int, index: Int) { main.post { hitCount = count; hitIndex = index } }
            @JavascriptInterface fun onOriginal(p: Int) { main.post { cbOrig((p - 1).coerceAtLeast(0)) } }
            @JavascriptInterface fun onLink(url: String) { main.post { cbLink(url) } }
            @JavascriptInterface fun onViewer(open: Boolean) { main.post { viewer = open } }
        }
    }

    BackHandler(enabled = viewer) { ctrl.run("NebReader.closeViewer()") }
    BackHandler(enabled = searching && !viewer) { searching = false; query = ""; ctrl.run("NebReader.clear()") }

    LaunchedEffect(settings, theme, topPx, bottomPx) { ctrl.run("NebReader.apply($settingsNow)") }
    LaunchedEffect(jump) { jump?.let { ctrl.run("NebReader.goPage(${it.page + 1})") } }
    LaunchedEffect(listening) {
        if (listening) { ctrl.run("NebReader.speechBegin()"); speakNext(ctrl) { listening = false } }
        else { speaker.stop(); ctrl.run("NebReader.speechStop()") }
    }

    Box(modifier.fillMaxSize().background(palette.bg)) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { c ->
                @SuppressLint("SetJavaScriptEnabled")
                val w = WebView(c).apply {
                    setBackgroundColor(palette.bg.toArgb())
                    this.settings.javaScriptEnabled = true
                    this.settings.domStorageEnabled = false
                    this.settings.allowFileAccess = false
                    this.settings.allowContentAccess = false
                    this.settings.cacheMode = WebSettings.LOAD_DEFAULT
                    this.settings.textZoom = 100
                    isVerticalScrollBarEnabled = true
                    overScrollMode = android.view.View.OVER_SCROLL_NEVER
                    addJavascriptInterface(bridge, "NebAndroid")
                    webViewClient = object : WebViewClient() {
                        override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse? =
                            if (request.url.host == HOST) serve(c, dir, request.url.path.orEmpty()) else
                                WebResourceResponse("text/plain", "utf-8", 403, "Blocked", emptyMap(), "".byteInputStream())
                        override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest) = true
                        override fun onPageFinished(view: WebView, url: String?) {
                            view.evaluateJavascript("NebReader.start(${startNow + 1}, $settingsNow)", null)
                            ctrl.flush()
                        }
                    }
                    loadUrl("https://$HOST/index.html")
                }
                ctrl.web = w
                w
            },
            update = { it.setBackgroundColor(palette.bg.toArgb()) }
        )

        // what the system draws over the page sits on the page colour
        Spacer(Modifier.align(Alignment.TopCenter).fillMaxWidth().height(topInset).background(palette.bg))
        Spacer(Modifier.align(Alignment.BottomCenter).fillMaxWidth().height(bottomInset).background(palette.bg))

        if (!showBars && pageCount > 1) {
            Box(Modifier.fillMaxWidth().windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(2.dp)) {
                Box(Modifier.fillMaxWidth((page / (pageCount - 1f)).coerceIn(0f, 1f)).height(2.dp).background(palette.muted.copy(alpha = 0.7f)))
            }
        }

        AnimatedVisibility(
            visible = showBars && !viewer,
            modifier = Modifier.align(Alignment.TopCenter),
            enter = slideInVertically(nebSpatialSpec()) { -it } + fadeIn(nebEffectsSpec()),
            exit = slideOutVertically(nebSpatialSpec()) { -it } + fadeOut(nebEffectsSpec())
        ) {
            Column(Modifier.fillMaxWidth().background(palette.bg)) {
                if (searching) Row(
                    Modifier.windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(ReaderBarHeight).padding(horizontal = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Close search", { searching = false; query = ""; ctrl.run("NebReader.clear()") }, tint = palette.ink)
                    Box(Modifier.weight(1f).padding(horizontal = 6.dp)) {
                        if (query.isEmpty()) Text("Search in the book", style = MaterialTheme.typography.bodyLarge, color = palette.muted)
                        BasicTextField(
                            value = query,
                            onValueChange = { query = it; ctrl.run("NebReader.search(${JSONObject.quote(it)})") },
                            singleLine = true,
                            textStyle = TextStyle(color = palette.ink, fontSize = MaterialTheme.typography.bodyLarge.fontSize),
                            cursorBrush = SolidColor(palette.accent),
                            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                            keyboardActions = KeyboardActions(onSearch = { ctrl.run("NebReader.step(1)") }),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                    if (query.length >= 2) Text(
                        if (hitCount == 0) "None" else "${hitIndex + 1} of $hitCount",
                        style = MaterialTheme.typography.labelMedium, color = palette.muted, modifier = Modifier.padding(end = 2.dp)
                    )
                    NebIconButton(Icons.Outlined.KeyboardArrowUp, "Previous match", { ctrl.run("NebReader.step(-1)") }, tint = palette.ink)
                    NebIconButton(Icons.Outlined.KeyboardArrowDown, "Next match", { ctrl.run("NebReader.step(1)") }, tint = palette.ink)
                } else Row(
                    Modifier.windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(ReaderBarHeight).padding(horizontal = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack, tint = palette.ink)
                    Column(Modifier.weight(1f).padding(horizontal = 6.dp)) {
                        Text(title.ifBlank { "Book" }, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = palette.ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(chapterTitle(page) ?: "Reading mode", style = MaterialTheme.typography.labelMedium, color = palette.muted, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                    NebIconButton(Icons.Outlined.Search, "Search", { searching = true }, tint = palette.ink)
                    NebIconButton(Icons.Outlined.Toc, "Contents", onContents, tint = palette.ink)
                    NebIconButton(Icons.Outlined.FormatSize, "Text and page settings", onTypography, tint = palette.ink)
                    var menu by remember { mutableStateOf(false) }
                    Box {
                        NebIconButton(Icons.Outlined.MoreVert, "More", { menu = true }, tint = palette.ink)
                        NebDropdownMenu(expanded = menu, onDismissRequest = { menu = false }) {
                            DropdownMenuItem(
                                text = { Text(if (bookmarked) "Remove bookmark" else "Bookmark this page") },
                                leadingIcon = { Icon(if (bookmarked) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, null) },
                                onClick = { menu = false; onToggleBookmark() }
                            )
                            DropdownMenuItem(text = { Text("Zen mode") }, leadingIcon = { Icon(Icons.Outlined.Fullscreen, null) }, onClick = { menu = false; onZen() })
                            DropdownMenuItem(
                                text = { Text(if (listening) "Stop reading aloud" else "Read aloud") },
                                leadingIcon = { Icon(Icons.Outlined.VolumeUp, null) },
                                onClick = { menu = false; listening = !listening }
                            )
                            DropdownMenuItem(text = { Text("View original PDF") }, leadingIcon = { Icon(Icons.Outlined.PictureAsPdf, null) }, onClick = { menu = false; onOriginal(page) })
                            DropdownMenuItem(
                                text = { Text(if (assistantHidden) "Show Neby AI button" else "Hide Neby AI button") },
                                leadingIcon = { Icon(Icons.Outlined.AutoAwesome, null) },
                                onClick = { menu = false; onToggleAssistant() }
                            )
                        }
                    }
                }
                HorizontalDivider(color = palette.line)
            }
        }

        AnimatedVisibility(
            visible = showBars && !searching && !viewer,
            modifier = Modifier.align(Alignment.BottomCenter),
            enter = slideInVertically(nebSpatialSpec()) { it } + fadeIn(nebEffectsSpec()),
            exit = slideOutVertically(nebSpatialSpec()) { it } + fadeOut(nebEffectsSpec())
        ) {
            Column(Modifier.fillMaxWidth().background(palette.bg)) {
                HorizontalDivider(color = palette.line)
                Column(Modifier.windowInsetsPadding(WindowInsets.navigationBarsIgnoringVisibility).padding(horizontal = 6.dp, vertical = 4.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        NebIconButton(
                            if (listening) Icons.Outlined.Pause else Icons.Outlined.PlayArrow,
                            if (listening) "Pause reading aloud" else "Read aloud", { listening = !listening }, tint = palette.ink
                        )
                        var dragging by remember { mutableStateOf<Float?>(null) }
                        if (pageCount > 1) Slider(
                            value = dragging ?: page.toFloat(),
                            onValueChange = { dragging = it },
                            onValueChangeFinished = { dragging?.let { v -> ctrl.run("NebReader.goPage(${v.roundToInt() + 1})") }; dragging = null },
                            valueRange = 0f..(pageCount - 1).toFloat(),
                            colors = SliderDefaults.colors(thumbColor = palette.ink, activeTrackColor = palette.ink, inactiveTrackColor = palette.line),
                            modifier = Modifier.weight(1f).semantics { stateDescription = "Page ${(dragging ?: page.toFloat()).roundToInt() + 1} of $pageCount" }
                        ) else Spacer(Modifier.weight(1f))
                        NebIconButton(Icons.Outlined.TextDecrease, "Smaller text", { onFontScale(((settings.fontScale - 0.1f).coerceIn(0.7f, 3f) * 20).roundToInt() / 20f) }, tint = palette.ink)
                        NebIconButton(Icons.Outlined.TextIncrease, "Larger text", { onFontScale(((settings.fontScale + 0.1f).coerceIn(0.7f, 3f) * 20).roundToInt() / 20f) }, tint = palette.ink)
                    }
                    Text(
                        "Page ${page + 1} of $pageCount",
                        style = MaterialTheme.typography.labelMedium, color = palette.muted,
                        modifier = Modifier.padding(start = 16.dp, bottom = 6.dp)
                    )
                }
            }
        }

        AnimatedVisibility(
            visible = chromeVisible && zen && !searching && !viewer,
            modifier = Modifier.align(Alignment.BottomCenter),
            enter = fadeIn(nebEffectsSpec()), exit = fadeOut(nebEffectsSpec())
        ) {
            Row(
                Modifier.windowInsetsPadding(WindowInsets.navigationBarsIgnoringVisibility).padding(bottom = 24.dp)
                    .clip(CircleShape).background(palette.ink).nebPressable(onClick = onZen).padding(horizontal = 16.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Outlined.FullscreenExit, null, tint = palette.bg)
                Spacer(Modifier.width(8.dp))
                Text("Leave zen mode", style = MaterialTheme.typography.labelLarge, color = palette.bg)
            }
        }
    }
}

/** Ask the page for the next block of text and speak it; stop when the book ends. The speaker calls back when it is done. */
private fun speakNext(ctrl: RdBookController, stopped: () -> Unit) {
    ctrl.eval("NebReader.speechNext()") { text ->
        if (text.isNullOrBlank()) stopped() else ctrl.speakText?.invoke(text)
    }
}
