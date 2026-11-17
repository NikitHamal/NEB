package com.neb.ians.ui.screens.interactive

import android.annotation.SuppressLint
import android.webkit.JsResult
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.activity.compose.BackHandler
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.neb.ians.ui.components.NebTopBar

private const val BASE_URL = "https://nebians.consica.com.np"

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun InteractiveLessonScreen(
    courseSlug: String,
    lessonSlug: String,
    onNavigateBack: () -> Unit
) {
    val nativeSim = remember(courseSlug, lessonSlug) { com.neb.ians.ui.sim.NativeSims.simFor(courseSlug, lessonSlug) }
    if (nativeSim != null) {
        com.neb.ians.ui.sim.NativeLessonScreen(sim = nativeSim, onNavigateBack = onNavigateBack)
        return
    }
    var pageProgress by remember { mutableStateOf(0) }
    var isFullscreen by remember { mutableStateOf(false) }
    val lessonUrl = "$BASE_URL/interactive/$courseSlug/$lessonSlug/"
    var webView: WebView? by remember { mutableStateOf(null) }
    var loadFailed by remember { mutableStateOf(false) }
    val view = androidx.compose.ui.platform.LocalView.current
    val lifecycleOwner = androidx.lifecycle.compose.LocalLifecycleOwner.current

    // The lab is a page of its own: while it is fullscreen the system bars step aside.
    androidx.compose.runtime.DisposableEffect(isFullscreen) {
        val window = (view.context as? android.app.Activity)?.window
        val controller = window?.let { androidx.core.view.WindowCompat.getInsetsController(it, view) }
        if (isFullscreen) {
            controller?.systemBarsBehavior = androidx.core.view.WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            controller?.hide(androidx.core.view.WindowInsetsCompat.Type.systemBars())
        }
        onDispose { controller?.show(androidx.core.view.WindowInsetsCompat.Type.systemBars()) }
    }

    // WebGL lives in the WebView's GPU process: pause it with the screen, free it with the page.
    androidx.compose.runtime.DisposableEffect(lifecycleOwner) {
        val observer = androidx.lifecycle.LifecycleEventObserver { _, event ->
            when (event) {
                androidx.lifecycle.Lifecycle.Event.ON_PAUSE -> webView?.onPause()
                androidx.lifecycle.Lifecycle.Event.ON_RESUME -> webView?.onResume()
                else -> Unit
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
            webView?.let { w ->
                (w.parent as? android.view.ViewGroup)?.removeView(w)
                w.stopLoading()
                w.destroy()
            }
            webView = null
        }
    }

    fun leaveFullscreen() {
        isFullscreen = false
        webView?.evaluateJavascript("window.dispatchEvent(new Event('nebfullscreenexit'))", null)
    }

    BackHandler(enabled = true) {
        if (isFullscreen) {
            leaveFullscreen()
        } else if (webView?.canGoBack() == true) {
            webView?.goBack()
        } else {
            onNavigateBack()
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.fillMaxSize()) {
            if (!isFullscreen) {
                NebTopBar(
                    showBrand = false,
                    title = "Lesson",
                    onBack = {
                        if (webView?.canGoBack() == true) {
                            webView?.goBack()
                        } else {
                            onNavigateBack()
                        }
                    }
                )
            }

            if (pageProgress in 1..99) {
                LinearProgressIndicator(
                    progress = { pageProgress / 100f },
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.primary,
                )
            }

            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { ctx ->
                    WebView(ctx).apply {
                        webView = this
                        settings.apply {
                            javaScriptEnabled = true
                            domStorageEnabled = true
                            allowFileAccess = false
                            allowContentAccess = false
                            cacheMode = WebSettings.LOAD_DEFAULT
                            mixedContentMode = 0
                            userAgentString = userAgentString + " NEBiansAndroid"
                            mediaPlaybackRequiresUserGesture = false
                            useWideViewPort = true
                            loadWithOverviewMode = true
                        }
                        setLayerType(android.view.View.LAYER_TYPE_HARDWARE, null)
                        webViewClient = object : WebViewClient() {
                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                super.onPageStarted(view, url, favicon)
                                loadFailed = false
                            }

                            override fun onPageFinished(view: WebView?, url: String?) {
                                super.onPageFinished(view, url)
                                view?.evaluateJavascript(ANDROID_INJECT_JS, null)
                            }

                            override fun onReceivedError(
                                view: WebView?,
                                request: android.webkit.WebResourceRequest?,
                                error: android.webkit.WebResourceError?
                            ) {
                                super.onReceivedError(view, request, error)
                                if (request?.isForMainFrame == true) loadFailed = true
                            }

                            override fun onRenderProcessGone(
                                view: WebView?,
                                detail: android.webkit.RenderProcessGoneDetail?
                            ): Boolean {
                                // The GPU/render process was killed (memory pressure): offer a clean retry.
                                loadFailed = true
                                return true
                            }
                        }
                        webChromeClient = object : WebChromeClient() {
                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                pageProgress = newProgress
                            }

                            override fun onJsAlert(view: WebView?, url: String?, message: String?, result: JsResult?): Boolean {
                                if (message == "NEBY_FULLSCREEN_ENTER") {
                                    isFullscreen = true
                                    result?.confirm()
                                    return true
                                }
                                if (message == "NEBY_FULLSCREEN_EXIT") {
                                    isFullscreen = false
                                    result?.confirm()
                                    return true
                                }
                                return false
                            }
                        }
                        loadUrl(lessonUrl)
                    }
                }
            )
        }

        if (loadFailed) {
            Column(
                modifier = Modifier
                    .align(Alignment.Center)
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                androidx.compose.material3.Text(
                    text = "This lesson could not load",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
                androidx.compose.foundation.layout.Spacer(Modifier.padding(top = 12.dp))
                androidx.compose.material3.FilledTonalButton(onClick = {
                    loadFailed = false
                    webView?.reload() ?: Unit
                }) { androidx.compose.material3.Text("Try again") }
            }
        }

        AnimatedVisibility(
            visible = isFullscreen,
            enter = fadeIn(),
            exit = fadeOut(),
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(start = 4.dp, top = 8.dp)
        ) {
            IconButton(
                onClick = { leaveFullscreen() },
                modifier = Modifier
                    .background(
                        MaterialTheme.colorScheme.surface.copy(alpha = 0.85f),
                        MaterialTheme.shapes.small
                    )
            ) {
                androidx.compose.material3.Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Exit fullscreen",
                    tint = MaterialTheme.colorScheme.onSurface
                )
            }
        }
    }
}

private const val ANDROID_INJECT_JS = """
(function() {
    if (document.documentElement.dataset.androidInjected) return;
    document.documentElement.dataset.androidInjected = '1';

    var style = document.createElement('style');
    style.textContent = `
        .md-topbar { display: none !important; }
        .md-bottom-nav { display: none !important; }
        .md-drawer-overlay, .md-side-drawer { display: none !important; }
        .ix-breadcrumb { display: none !important; }
        .md-footer, .site-footer { display: none !important; }
        .ix-lesson-header { display: none !important; }
        .site-main { padding: 0 !important; margin: 0 !important; }
        .ix-lesson-page { padding: 8px 8px 0 8px !important; }
        .ix-lesson-layout {
            display: flex !important;
            flex-direction: column !important;
            grid-template-columns: 1fr !important;
            gap: 16px !important;
        }
        .ix-sim-column { width: 100% !important; max-width: 100% !important; }
        .ix-learn-column { width: 100% !important; max-width: 100% !important; }
        .ix-sim-shell:not(.ix-fake-fullscreen) { position: relative !important; top: auto !important; }
        .ix-sim-shell:not(.ix-fake-fullscreen) .ix-sim-stage {
            aspect-ratio: 4 / 3 !important;
            max-height: 55vh !important;
            min-height: 200px !important;
        }
        body { overflow-x: hidden !important; }

        body.ix-no-scroll .site-main,
        body.ix-no-scroll .ix-lesson-page { padding: 0 !important; margin: 0 !important; }
        body.ix-no-scroll .ix-lesson-layout { gap: 0 !important; }
        .ix-sim-shell.ix-fake-fullscreen {
            position: fixed !important;
            inset: 0 !important;
            z-index: 9999 !important;
            border-radius: 0 !important;
            border: none !important;
        }
        .ix-sim-shell.ix-fake-fullscreen .ix-sim-stage {
            aspect-ratio: auto !important;
            max-height: none !important;
            min-height: 0 !important;
            height: 100% !important;
        }
        body.ix-no-scroll .ix-learn-column,
        body.ix-no-scroll .ix-lesson-nav { display: none !important; }
    `;
    document.head.appendChild(style);

    window.scrollTo(0, 0);
})();
"""