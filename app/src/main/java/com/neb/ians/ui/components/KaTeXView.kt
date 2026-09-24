package com.neb.ians.ui.components

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Color as AndroidColor
import android.os.Handler
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalInspectionMode
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import org.json.JSONObject

private val LatexCommandRegex = Regex(
    """\\(frac|dfrac|tfrac|sqrt|int|iint|oint|sum|prod|lim|infty|partial|nabla|vec|hat|bar|dot|ddot|overline|underline|binom|begin|end|left|right|cdot|times|div|pm|mp|leq|geq|neq|approx|equiv|propto|alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|rho|sigma|tau|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Sigma|Phi|Psi|Omega|ce|text|mathrm|mathbf|mathbb)\b"""
)

private val InlineDollarRegex = Regex("""(?<!\\)\$([^$\n]{1,200})\$""")

private fun looksLikeMath(candidate: String): Boolean {
    val s = candidate.trim()
    if (s.isEmpty() || s.length > 80) return false
    if (s.contains('\\')) return true
    val hasOperator = s.any { it in "=+*/^_<>" } || Regex("""\d\s*-\s*\d""").containsMatchIn(s)
    if (!hasOperator) return false
    return s.any { it.isDigit() || it.isLetter() }
}

/**
 * Checks if [text] contains mathematical / scientific LaTeX syntax that requires KaTeX rendering.
 *
 * Deliberately conservative: prose that merely mentions prices ("$5 a month and $10 a year")
 * must never reach the WebView renderer, because that path cannot lay out ordinary
 * paragraphs the way Compose text does.
 */
fun hasLatexMath(text: String?): Boolean {
    if (text.isNullOrBlank()) return false
    if (text.contains("$$") || text.contains("\\[") || text.contains("\\(")) return true
    if (text.contains("\\begin{") || text.contains("\\end{")) return true
    if (LatexCommandRegex.containsMatchIn(text)) return true
    val inline = InlineDollarRegex.find(text) ?: return false
    return looksLikeMath(inline.groupValues[1])
}

private class KaTeXBridge(private val onHeight: (Int) -> Unit) {
    private val mainHandler = Handler(Looper.getMainLooper())

    @JavascriptInterface
    fun onHeightChanged(heightPx: Int) {
        mainHandler.post {
            onHeight(heightPx)
        }
    }
}

/**
 * High-performance, offline-ready KaTeX mathematical formula renderer for Jetpack Compose.
 * Uses local bundled KaTeX 0.16.11 assets from `file:///android_asset/katex/`.
 */
@SuppressLint("SetJavaScriptEnabled")
@Composable
fun KaTeXMathView(
    content: String,
    modifier: Modifier = Modifier,
    displayMode: Boolean = true,
    center: Boolean = true,
    fontSizeSp: Float = 15f,
    textColor: Color = MaterialTheme.colorScheme.onSurface,
    primaryColor: Color = MaterialTheme.colorScheme.primary,
    minHeight: Dp = if (displayMode) 44.dp else 24.dp,
    onLinkClick: ((String) -> Unit)? = null
) {
    if (LocalInspectionMode.current) {
        Box(modifier = modifier.height(minHeight)) {
            Text(content, fontSize = fontSizeSp.sp, color = textColor)
        }
        return
    }

    val context = LocalContext.current
    val density = LocalDensity.current
    var contentHeightPx by remember(content, fontSizeSp) { mutableStateOf<Int?>(null) }

    val textColorHex = remember(textColor) {
        String.format("#%06X", 0xFFFFFF and textColor.toArgb())
    }
    val primaryColorHex = remember(primaryColor) {
        String.format("#%06X", 0xFFFFFF and primaryColor.toArgb())
    }

    val htmlData = remember(content, displayMode, center, fontSizeSp, textColorHex, primaryColorHex) {
        buildKaTeXHtml(
            content = content,
            displayMode = displayMode,
            center = center,
            fontSizeSp = fontSizeSp,
            textColorHex = textColorHex,
            primaryColorHex = primaryColorHex
        )
    }

    val heightModifier = if (contentHeightPx != null && contentHeightPx!! > 0) {
        val calculatedDp = with(density) { contentHeightPx!!.toDp() }
        Modifier.height(calculatedDp)
    } else {
        Modifier.heightIn(min = minHeight)
    }

    AndroidView(
        factory = { ctx ->
            WebView(ctx).apply {
                layoutParams = ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
                )
                setBackgroundColor(AndroidColor.TRANSPARENT)
                isVerticalScrollBarEnabled = false
                isHorizontalScrollBarEnabled = false
                isNestedScrollingEnabled = false
                overScrollMode = View.OVER_SCROLL_NEVER

                settings.apply {
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    allowFileAccess = true
                    loadWithOverviewMode = true
                    useWideViewPort = false
                    cacheMode = WebSettings.LOAD_CACHE_ELSE_NETWORK
                    defaultTextEncodingName = "UTF-8"
                }

                addJavascriptInterface(
                    KaTeXBridge { px ->
                        val current = contentHeightPx
                        if (px > 0 && (current == null || kotlin.math.abs(px - current) > 2)) {
                            contentHeightPx = px
                        }
                    },
                    "KaTeXBridge"
                )

                webViewClient = object : WebViewClient() {
                    override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                        val url = request?.url?.toString()
                        if (url != null && onLinkClick != null) {
                            onLinkClick(url)
                            return true
                        }
                        return false
                    }
                }

                loadDataWithBaseURL(
                    "file:///android_asset/katex/",
                    htmlData,
                    "text/html",
                    "UTF-8",
                    null
                )
            }
        },
        update = { webView ->
            if (webView.tag != htmlData) {
                webView.tag = htmlData
                webView.loadDataWithBaseURL(
                    "file:///android_asset/katex/",
                    htmlData,
                    "text/html",
                    "UTF-8",
                    null
                )
            }
        },
        modifier = modifier
            .fillMaxWidth()
            .then(heightModifier)
    )
}

/**
 * Universal text component with automatic KaTeX math formula rendering.
 *
 * If [text] contains mathematical LaTeX syntax (`$$`, `$`, `\frac`, `\sqrt`, etc.),
 * it seamlessly renders formulas via KaTeX. Otherwise, it uses native Compose [Text]
 * for maximum performance with zero overhead.
 */
@Composable
fun KaTeXText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurface,
    fontWeight: FontWeight? = null,
    textAlign: TextAlign? = null,
    maxLines: Int = Int.MAX_VALUE,
    overflow: TextOverflow = TextOverflow.Clip,
    fontSize: TextUnit = TextUnit.Unspecified,
    displayMode: Boolean = false,
    onClick: (() -> Unit)? = null,
    onLinkClick: ((String) -> Unit)? = null
) {
    if (text.isBlank()) return

    val containsMath = remember(text) { hasLatexMath(text) }
    val effectiveFontWeight = fontWeight ?: style.fontWeight
    val effectiveStyle = style.copy(
        fontWeight = effectiveFontWeight,
        fontSize = if (fontSize != TextUnit.Unspecified) fontSize else style.fontSize
    )

    if (containsMath) {
        val fontSizeSp = if (fontSize != TextUnit.Unspecified && fontSize.isSp) {
            fontSize.value
        } else if (effectiveStyle.fontSize.isSp) {
            effectiveStyle.fontSize.value
        } else {
            15f
        }

        KaTeXMathView(
            content = text,
            modifier = if (onClick != null) modifier.clickable(onClick = onClick) else modifier,
            displayMode = displayMode,
            center = displayMode,
            fontSizeSp = fontSizeSp,
            textColor = color,
            minHeight = if (displayMode) 40.dp else 22.dp,
            onLinkClick = onLinkClick
        )
    } else {
        Text(
            text = text,
            modifier = if (onClick != null) modifier.clickable(onClick = onClick) else modifier,
            style = effectiveStyle,
            color = color,
            textAlign = textAlign,
            maxLines = maxLines,
            overflow = overflow
        )
    }
}

private fun buildKaTeXHtml(
    content: String,
    displayMode: Boolean,
    center: Boolean,
    fontSizeSp: Float,
    textColorHex: String,
    primaryColorHex: String
): String {
    val escapedContent = JSONObject.quote(content)
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="stylesheet" href="katex.min.css">
    <script src="katex.min.js"></script>
    <script src="contrib/mhchem.min.js"></script>
    <script src="contrib/auto-render.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        html, body {
            background-color: transparent !important;
            color: $textColorHex;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: ${fontSizeSp}px;
            line-height: 1.55;
            word-break: break-word;
            overflow: hidden;
            user-select: text;
            -webkit-user-select: text;
        }
        #math-container {
            display: inline-block;
            width: 100%;
            white-space: pre-wrap;
            padding: ${if (displayMode) "4px 2px" else "1px 0"};
        }
        .katex-display {
            margin: 4px 0 !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            padding: 4px 0 !important;
            text-align: ${if (center) "center" else "left"} !important;
            -webkit-overflow-scrolling: touch;
        }
        .katex {
            font-size: 1.06em;
            color: inherit;
        }
        .katex-error {
            color: #ef4444 !important;
            font-family: monospace;
            font-size: 0.9em;
        }
        a {
            color: $primaryColorHex;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div id="math-container">
        <div id="math-target"></div>
    </div>
    <script>
        var rawContent = $escapedContent;
        var isDisplay = $displayMode;
        var el = document.getElementById('math-target');

        function doRender() {
            var raw = (rawContent || '').trim();
            var hasDelims = raw.indexOf('$$') !== -1 || raw.indexOf('\\[') !== -1 ||
                            raw.indexOf('\\(') !== -1 || (raw.indexOf('$') !== -1 && raw.lastIndexOf('$') > raw.indexOf('$'));

            if (isDisplay && !hasDelims) {
                try {
                    katex.render(raw, el, {
                        displayMode: true,
                        throwOnError: false,
                        output: 'htmlAndMathml'
                    });
                } catch (e) {
                    el.innerText = raw;
                }
            } else {
                el.textContent = raw;
                if (window.renderMathInElement) {
                    renderMathInElement(el, {
                        delimiters: [
                            {left: "$$", right: "$$", display: true},
                            {left: "\\[", right: "\\]", display: true},
                            {left: "\\(", right: "\\)", display: false},
                            {left: "$", right: "$", display: false}
                        ],
                        throwOnError: false
                    });
                }
            }
            reportHeight();
        }

        var lastReportedHeight = 0;
        var reportScheduled = false;

        function reportHeight() {
            var c = document.getElementById('math-container');
            if (!c || !window.KaTeXBridge || !window.KaTeXBridge.onHeightChanged) return;
            var h = Math.ceil(Math.max(c.offsetHeight, c.scrollHeight));
            if (h <= 0 || Math.abs(h - lastReportedHeight) <= 2) return;
            lastReportedHeight = h;
            window.KaTeXBridge.onHeightChanged(h);
        }

        function scheduleReport() {
            if (reportScheduled) return;
            reportScheduled = true;
            (window.requestAnimationFrame || window.setTimeout)(function () {
                reportScheduled = false;
                reportHeight();
            }, 0);
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', doRender);
        } else {
            doRender();
        }
        window.addEventListener('load', scheduleReport);
        if (window.ResizeObserver) {
            new ResizeObserver(scheduleReport).observe(document.getElementById('math-container'));
        }
    </script>
</body>
</html>
    """.trimIndent()
}
