package com.neb.ians.admin

import android.annotation.SuppressLint
import android.app.DownloadManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.webkit.CookieManager
import android.webkit.DownloadListener
import android.webkit.URLUtil
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebChromeClient.FileChooserParams
import android.graphics.Bitmap
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

private const val ADMIN_URL = "https://nebians.consica.com.np/admin/"
private const val ALLOWED_HOST = "nebians.consica.com.np"

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)
        setContent {
            AdminTheme {
                AdminWebApp()
            }
        }
    }
}

@Composable
private fun AdminTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = androidx.compose.material3.lightColorScheme(
            primary = Color(0xFF004AC6),
            surface = Color(0xFFF5F6F8),
            onSurface = Color(0xFF0B1C30),
            surfaceContainer = Color(0xFFECEEF1)
        ),
        content = content
    )
}

@SuppressLint("SetJavaScriptEnabled")
@Composable
private fun AdminWebApp() {
    val context = androidx.compose.ui.platform.LocalContext.current
    var webView by remember { mutableStateOf<WebView?>(null) }
    var progress by remember { mutableFloatStateOf(0f) }
    var isLoading by remember { mutableStateOf(true) }
    var hasPageError by remember { mutableStateOf(false) }
    var filePathCallback by remember { mutableStateOf<ValueCallback<Array<Uri>>?>(null) }

    val fileLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenMultipleDocuments()) { uris ->
        filePathCallback?.onReceiveValue(uris.toTypedArray())
        filePathCallback = null
    }

    BackHandler(enabled = webView?.canGoBack() == true) {
        webView?.goBack()
    }

    DisposableEffect(Unit) {
        onDispose {
            filePathCallback?.onReceiveValue(null)
            filePathCallback = null
            webView?.apply {
                stopLoading()
                destroy()
            }
        }
    }

    Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.surface) {
        Box(modifier = Modifier.fillMaxSize()) {
            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { ctx ->
                    WebView(ctx).apply {
                        webView = this
                        configureAdminWebView(
                            onProgress = { p ->
                                progress = p / 100f
                                isLoading = p < 100
                            },
                            onError = { hasPageError = true },
                            onFileChooser = { callback, acceptTypes ->
                                filePathCallback?.onReceiveValue(null)
                                filePathCallback = callback
                                fileLauncher.launch(resolveAcceptTypes(acceptTypes))
                            }
                        )
                        loadUrl(ADMIN_URL)
                    }
                },
                update = { webView = it }
            )

            if (isLoading) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .windowInsetsPadding(WindowInsets.statusBars)
                        .align(Alignment.TopCenter)
                ) {
                    LinearProgressIndicator(
                        progress = progress.coerceIn(0f, 1f),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(3.dp)
                    )
                }
            }

            if (hasPageError) {
                Column(
                    modifier = Modifier.align(Alignment.Center),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    CircularProgressIndicator()
                    Text(
                        text = "Trying to reconnect to NEBians Admin...",
                        color = MaterialTheme.colorScheme.onSurface,
                        modifier = Modifier.windowInsetsPadding(WindowInsets.statusBars)
                    )
                }
            }
        }
    }
}

private fun WebView.configureAdminWebView(
    onProgress: (Int) -> Unit,
    onError: () -> Unit,
    onFileChooser: (ValueCallback<Array<Uri>>, Array<String>) -> Unit
) {
    settings.apply {
        javaScriptEnabled = true
        domStorageEnabled = true
        databaseEnabled = true
        loadsImagesAutomatically = true
        mediaPlaybackRequiresUserGesture = false
        cacheMode = WebSettings.LOAD_DEFAULT
        useWideViewPort = true
        loadWithOverviewMode = true
        builtInZoomControls = false
        displayZoomControls = false
        allowFileAccess = true
        allowContentAccess = true
        safeBrowsingEnabled = true
        userAgentString = "$userAgentString NEBiansAdminAndroid/1.0"
    }

    CookieManager.getInstance().apply {
        setAcceptCookie(true)
        setAcceptThirdPartyCookies(this@configureAdminWebView, true)
    }

    webViewClient = object : WebViewClient() {
        override fun onPageStarted(view: WebView, url: String?, favicon: Bitmap?) {
            super.onPageStarted(view, url, favicon)
        }

        override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
            val uri = request.url ?: return false
            return if (uri.host == ALLOWED_HOST || uri.host?.endsWith(".consica.com.np") == true) {
                false
            } else {
                view.context.startActivity(Intent(Intent.ACTION_VIEW, uri))
                true
            }
        }

        override fun onPageFinished(view: WebView, url: String) {
            super.onPageFinished(view, url)
            CookieManager.getInstance().flush()
        }

        override fun onReceivedError(view: WebView, request: WebResourceRequest, error: WebResourceError) {
            if (request.isForMainFrame) onError()
            super.onReceivedError(view, request, error)
        }
    }

    webChromeClient = object : WebChromeClient() {
        override fun onProgressChanged(view: WebView, newProgress: Int) {
            onProgress(newProgress)
            super.onProgressChanged(view, newProgress)
        }

        override fun onShowFileChooser(
            webView: WebView,
            filePathCallback: ValueCallback<Array<Uri>>,
            fileChooserParams: FileChooserParams
        ): Boolean {
            onFileChooser(filePathCallback, fileChooserParams.acceptTypes ?: emptyArray())
            return true
        }
    }

    setDownloadListener(DownloadListener { url, userAgent, contentDisposition, mimeType, _ ->
        runCatching {
            val request = DownloadManager.Request(Uri.parse(url)).apply {
                setMimeType(mimeType)
                addRequestHeader("User-Agent", userAgent)
                CookieManager.getInstance().getCookie(url)?.let { addRequestHeader("Cookie", it) }
                setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                val guessed = URLUtil.guessFileName(url, contentDisposition, mimeType)
                setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, guessed)
            }
            val dm = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
            dm.enqueue(request)
        }
    })
}

private fun resolveAcceptTypes(acceptTypes: Array<String>): Array<String> {
    val clean = acceptTypes.map { it.trim() }.filter { it.isNotBlank() && it != "*/*" }
    return if (clean.isEmpty()) arrayOf("image/*", "application/pdf", "text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") else clean.toTypedArray()
}
