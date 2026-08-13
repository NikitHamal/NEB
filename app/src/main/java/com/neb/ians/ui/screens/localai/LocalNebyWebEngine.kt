package com.neb.ians.ui.screens.localai

import android.annotation.SuppressLint
import android.content.Context
import android.os.Handler
import android.os.Looper
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.webkit.WebViewAssetLoader
import org.json.JSONObject
import java.io.File

/**
 * Runs the Needle 2 on-device engine inside a hidden WebView.
 *
 * The model assets live in app-private storage (`filesDir/needle/`) and are
 * served to the page through a [WebViewAssetLoader] under the synthetic
 * `https://appassets.androidplatform.net/needle/` origin. The page
 * (`bridge.html`) imports the same `needle.js` the website ships, loads
 * `needle.wasm` + `needle2.cact` from storage, and exposes a `__run(query)`
 * entry point. Results are pushed back to Kotlin through a `NebyBridge`
 * JavaScript interface.
 *
 * Because everything is read from local storage and the engine does no
 * networking, inference is fully offline after the model is downloaded.
 *
 * NOTE: A WebView must be created on the main thread — call [createView] from a
 * Compose `AndroidView` factory (which runs on the main thread). Keep one
 * instance for the lifetime of the screen so the ~14 MB model isn't reloaded on
 * every recomposition.
 */
class LocalNebyWebEngine(private val context: Context, private val assetDir: File) {

    private val mainHandler = Handler(Looper.getMainLooper())

    private var webView: WebView? = null
    private var ready = false
    private var pendingReadySeconds: String? = null

    private var onReadyCb: ((seconds: String) -> Unit)? = null
    private var onResultCb: ((json: String) -> Unit)? = null
    private var onErrorCb: ((message: String) -> Unit)? = null

    val isReady: Boolean get() = ready

    fun setCallbacks(
        onReady: (String) -> Unit,
        onResult: (String) -> Unit,
        onError: (String) -> Unit,
    ) {
        onReadyCb = onReady
        onResultCb = onResult
        onErrorCb = onError
        // The bridge may have already reported ready before callbacks were set
        // (defensive — the screen now attaches before loading, but guard anyway).
        pendingReadySeconds?.let {
            pendingReadySeconds = null
            ready = true
            onReady(it)
        }
    }

    @SuppressLint("SetJavaScriptEnabled", "AddJavascriptInterface")
    fun createView(): WebView {
        // Serve every file under filesDir/needle/ at the synthetic
        // https://appassets.androidplatform.net/needle/ origin. The built-in
        // InternalStoragePathHandler streams files from app internal storage and
        // guards against path traversal.
        val assetLoader = WebViewAssetLoader.Builder()
            .addPathHandler("/needle/", WebViewAssetLoader.InternalStoragePathHandler(context, assetDir))
            .build()

        val view = WebView(context)
        view.settings.javaScriptEnabled = true
        view.settings.domStorageEnabled = true
        view.settings.allowFileAccess = false
        view.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?,
            ): WebResourceResponse? {
                val url = request?.url ?: return null
                val response = assetLoader.shouldInterceptRequest(url) ?: return null
                // The built-in handler guesses MIME from the extension, which can
                // yield text/plain for .js/.wasm. The WebView refuses to run a
                // <script> served as text/plain, so pin the correct types.
                return when (url.path?.substringAfterLast('.')) {
                    "js" -> response.also { it.mimeType = "text/javascript" }
                    "wasm" -> response.also { it.mimeType = "application/wasm" }
                    else -> response
                }
            }
        }
        view.addJavascriptInterface(Bridge(), "NebyBridge")
        webView = view
        view.loadUrl("https://appassets.androidplatform.net/needle/bridge.html")
        return view
    }

    /** Runs a query against the loaded model. Result is delivered via the onResult callback. */
    fun runQuery(query: String) {
        if (!ready) return
        val arg = JSONObject().put("q", query).toString() // {"q":"..."}
        mainHandler.post {
            webView?.evaluateJavascript("__run($arg.q);") { }
        }
    }

    fun destroy() {
        mainHandler.post {
            webView?.destroy()
            webView = null
        }
    }

    /** JS bridge object — called from `bridge.html` on a background thread. */
    private inner class Bridge {
        @JavascriptInterface
        fun onReady(seconds: String) {
            mainHandler.post {
                if (onReadyCb != null) {
                    ready = true
                    onReadyCb?.invoke(seconds)
                } else {
                    pendingReadySeconds = seconds
                }
            }
        }

        @JavascriptInterface
        fun onResult(json: String) {
            mainHandler.post { onResultCb?.invoke(json) }
        }

        @JavascriptInterface
        fun onError(message: String) {
            mainHandler.post { onErrorCb?.invoke(message) }
        }
    }
}
