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
    var pageProgress by remember { mutableStateOf(0) }
    var isFullscreen by remember { mutableStateOf(false) }
    val lessonUrl = "$BASE_URL/interactive/$courseSlug/$lessonSlug/"
    var webView: WebView? by remember { mutableStateOf(null) }

    BackHandler(enabled = true) {
        if (webView?.canGoBack() == true) {
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
                        }
                        webViewClient = object : WebViewClient() {
                            override fun onPageFinished(view: WebView?, url: String?) {
                                super.onPageFinished(view, url)
                                view?.evaluateJavascript(ANDROID_INJECT_JS, null)
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

        AnimatedVisibility(
            visible = isFullscreen,
            enter = fadeIn(),
            exit = fadeOut(),
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(start = 4.dp, top = 8.dp)
        ) {
            IconButton(
                onClick = {
                    isFullscreen = false
                },
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
        .ix-sim-shell { position: relative !important; top: auto !important; }
        .ix-sim-stage {
            aspect-ratio: 4 / 3 !important;
            max-height: 55vh !important;
            min-height: 200px !important;
        }
        body { overflow-x: hidden !important; }

        .ix-android-fullscreen .site-main,
        .ix-android-fullscreen .ix-lesson-page { padding: 0 !important; margin: 0 !important; }
        .ix-android-fullscreen .ix-lesson-layout { gap: 0 !important; }
        .ix-android-fullscreen .ix-sim-shell {
            position: fixed !important;
            inset: 0 !important;
            z-index: 9999 !important;
            border-radius: 0 !important;
            border: none !important;
        }
        .ix-android-fullscreen .ix-sim-stage {
            aspect-ratio: auto !important;
            max-height: none !important;
            min-height: 0 !important;
            height: 100% !important;
        }
        .ix-android-fullscreen .ix-learn-column,
        .ix-android-fullscreen .ix-lesson-nav,
        .ix-android-fullscreen .ix-objectives,
        .ix-android-fullscreen .ix-knowledge,
        .ix-android-fullscreen .ix-fun-fact,
        .ix-android-fullscreen .ix-quiz { display: none !important; }
    `;
    document.head.appendChild(style);

    var fsBtn = document.getElementById('ix-fullscreen-btn');
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopImmediatePropagation();
            e.preventDefault();
            var shell = document.getElementById('ix-sim-shell');
            if (shell && shell.classList.contains('ix-android-fullscreen-active')) {
                shell.classList.remove('ix-android-fullscreen-active');
                document.body.classList.remove('ix-android-fullscreen');
                shell.classList.remove('ix-fake-fullscreen');
                document.body.classList.remove('ix-no-scroll');
                alert('NEBY_FULLSCREEN_EXIT');
            } else {
                if (shell) {
                    shell.classList.add('ix-android-fullscreen-active');
                    shell.classList.add('ix-fake-fullscreen');
                }
                document.body.classList.add('ix-android-fullscreen');
                document.body.classList.add('ix-no-scroll');
                alert('NEBY_FULLSCREEN_ENTER');
            }
        }, true);
    }

    window.scrollTo(0, 0);
})();
"""