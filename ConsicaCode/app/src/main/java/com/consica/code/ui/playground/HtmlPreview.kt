package com.consica.code.ui.playground

import android.webkit.WebView
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView

/**
 * Offline HTML preview. Renders the learner's markup in a sandboxed [WebView] with no network and
 * no JavaScript — everything is local, matching the app's offline-first promise.
 */
@Composable
fun HtmlPreview(html: String, modifier: Modifier = Modifier) {
    AndroidView(
        modifier = modifier,
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = false
                settings.blockNetworkLoads = true
                settings.allowFileAccess = false
                settings.allowContentAccess = false
                isVerticalScrollBarEnabled = true
            }
        },
        update = { web ->
            web.loadDataWithBaseURL(null, wrapHtml(html), "text/html", "UTF-8", null)
        },
    )
}

/** Wrap a fragment in a minimal, mobile-friendly document if it isn't already a full page. */
private fun wrapHtml(html: String): String {
    val lower = html.lowercase()
    if (lower.contains("<html") || lower.contains("<!doctype")) return html
    return """
        <!DOCTYPE html>
        <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: sans-serif; padding: 16px; color: #1A1A1A; line-height: 1.5; }
          </style>
        </head>
        <body>
        $html
        </body>
        </html>
    """.trimIndent()
}
