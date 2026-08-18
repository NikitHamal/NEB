package com.neb.ians.data.needle

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import android.webkit.JavascriptInterface
import android.webkit.RenderProcessGoneDetail
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.webkit.WebViewAssetLoader
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.ByteArrayInputStream
import java.io.FileInputStream
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.doubleOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import org.json.JSONObject

sealed interface NeedleRuntimeState {
    data object Idle : NeedleRuntimeState
    data class Loading(val label: String, val progress: Float? = null) : NeedleRuntimeState
    data class Ready(val source: String, val loadSeconds: Double, val heapBytes: Long) : NeedleRuntimeState
    data class Error(val message: String) : NeedleRuntimeState
}

data class NeedleRuntimeResult(
    val requestId: String,
    val resultJson: String,
    val durationMs: Double
)

@Singleton
class NeedleWebRuntime @Inject constructor(
    @ApplicationContext private val context: Context,
    private val modelManager: NeedleModelManager
) {
    private val mainHandler = Handler(Looper.getMainLooper())
    private val json = Json { ignoreUnknownKeys = true }
    private val _state = MutableStateFlow<NeedleRuntimeState>(NeedleRuntimeState.Idle)
    val state: StateFlow<NeedleRuntimeState> = _state.asStateFlow()
    private val _results = MutableSharedFlow<NeedleRuntimeResult>(extraBufferCapacity = 8)
    val results: SharedFlow<NeedleRuntimeResult> = _results.asSharedFlow()
    private val _errors = MutableSharedFlow<Pair<String?, String>>(extraBufferCapacity = 8)
    val errors: SharedFlow<Pair<String?, String>> = _errors.asSharedFlow()
    private var webView: WebView? = null

    fun prepare() {
        if (!modelManager.modelFile.exists()) {
            _state.value = NeedleRuntimeState.Error("The model is not installed")
            return
        }
        if (webView != null || _state.value is NeedleRuntimeState.Ready) return
        mainHandler.post { createRuntime() }
    }

    fun run(requestId: String, query: String): Boolean {
        if (_state.value !is NeedleRuntimeState.Ready || query.isBlank()) return false
        mainHandler.post {
            webView?.evaluateJavascript(
                "window.NebyRuntime.run(${JSONObject.quote(requestId)}, ${JSONObject.quote(query)});",
                null
            )
        }
        return true
    }

    fun release(clearSavedRuntime: Boolean = false) {
        mainHandler.post { releaseNow(clearSavedRuntime) }
    }

    fun restart() {
        mainHandler.post {
            releaseNow(false)
            if (modelManager.modelFile.exists()) createRuntime()
        }
    }

    private fun releaseNow(clearSavedRuntime: Boolean) {
        val current = webView
        if (clearSavedRuntime) {
            current?.evaluateJavascript("window.NebyRuntime.clearCache();", null)
            android.webkit.WebStorage.getInstance()
                .deleteOrigin("https://appassets.androidplatform.net")
        }
        current?.removeJavascriptInterface("NeedleAndroid")
        current?.stopLoading()
        current?.destroy()
        webView = null
        _state.value = NeedleRuntimeState.Idle
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun createRuntime() {
        if (webView != null) return
        _state.value = NeedleRuntimeState.Loading("Starting private AI")
        val assetLoader = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context))
            .addPathHandler("/model/") { path -> modelResponse(path) }
            .build()
        val runtime = WebView(context)
        runtime.settings.javaScriptEnabled = true
        runtime.settings.domStorageEnabled = true
        runtime.settings.allowFileAccess = false
        runtime.settings.allowContentAccess = false
        runtime.settings.databaseEnabled = true
        runtime.addJavascriptInterface(Bridge(), "NeedleAndroid")
        runtime.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                _state.value = NeedleRuntimeState.Loading("Loading local engine")
            }

            override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest): WebResourceResponse? {
                val handled = assetLoader.shouldInterceptRequest(request.url)
                if (handled != null) return handled
                return blockedResponse()
            }

            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                return request?.url?.host != "appassets.androidplatform.net"
            }

            override fun onRenderProcessGone(view: WebView?, detail: RenderProcessGoneDetail?): Boolean {
                webView = null
                        _state.value = NeedleRuntimeState.Error("The local AI process stopped. Tap retry to reload it.")
                view?.destroy()
                return true
            }
        }
        webView = runtime
        runtime.loadUrl("https://appassets.androidplatform.net/assets/needle2/bootstrap.html?v=3")
    }

    private fun modelResponse(path: String): WebResourceResponse {
        val file = modelManager.modelFile
        if (path != "needle2.cact" || !file.exists()) return blockedResponse(404, "Not Found")
        return WebResourceResponse(
            "application/octet-stream",
            null,
            200,
            "OK",
            mapOf(
                "Content-Length" to file.length().toString(),
                "Cache-Control" to "no-store"
            ),
            FileInputStream(file)
        )
    }

    private fun blockedResponse(code: Int = 403, reason: String = "Blocked"): WebResourceResponse {
        return WebResourceResponse(
            "text/plain",
            "UTF-8",
            code,
            reason,
            emptyMap(),
            ByteArrayInputStream(ByteArray(0))
        )
    }

    private fun handleMessage(raw: String) {
        val envelope = runCatching { json.parseToJsonElement(raw).jsonObject }.getOrNull() ?: return
        when (envelope["type"]?.jsonPrimitive?.contentOrNull) {
            "bridge-ready" -> {
                webView?.evaluateJavascript("window.NebyRuntime.initialize();", null)
            }
            "status" -> {
                val status = envelope["status"]?.jsonPrimitive?.contentOrNull.orEmpty()
                val progress = envelope["progress"]?.jsonPrimitive?.doubleOrNull?.toFloat()
                _state.value = NeedleRuntimeState.Loading(statusLabel(status), progress)
            }
            "ready" -> {
                _state.value = NeedleRuntimeState.Ready(
                    source = envelope["source"]?.jsonPrimitive?.contentOrNull ?: "cold",
                    loadSeconds = envelope["loadSeconds"]?.jsonPrimitive?.doubleOrNull ?: 0.0,
                    heapBytes = envelope["heapBytes"]?.jsonPrimitive?.contentOrNull?.toLongOrNull() ?: 0L
                )
            }
            "result" -> {
                val id = envelope["id"]?.jsonPrimitive?.contentOrNull ?: return
                val result = envelope["result"]?.toString() ?: return
                _results.tryEmit(
                    NeedleRuntimeResult(
                        requestId = id,
                        resultJson = result,
                        durationMs = envelope["durationMs"]?.jsonPrimitive?.doubleOrNull ?: 0.0
                    )
                )
            }
            "error" -> {
                val id = envelope["id"]?.jsonPrimitive?.contentOrNull
                val message = envelope["message"]?.jsonPrimitive?.contentOrNull ?: "Local inference failed"
                if (id == null) _state.value = NeedleRuntimeState.Error(message)
                _errors.tryEmit(id to message)
            }
        }
    }

    private fun statusLabel(status: String): String = when (status) {
        "loading-engine" -> "Loading AI engine"
        "restoring" -> "Restoring saved runtime"
        "cache-hit" -> "Using saved engine"
        "downloading" -> "Reading on-device model"
        "loading-model" -> "Loading model into memory"
        "preparing-tools" -> "Preparing NEBians tools"
        "saving" -> "Optimizing future launches"
        else -> "Preparing private AI"
    }

    private inner class Bridge {
        @JavascriptInterface
        fun onMessage(message: String) {
            mainHandler.post { handleMessage(message) }
        }
    }
}
