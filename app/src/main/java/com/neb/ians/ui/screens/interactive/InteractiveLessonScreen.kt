package com.neb.ians.ui.screens.interactive

import android.annotation.SuppressLint
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
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
    val lessonUrl = "$BASE_URL/interactive/$courseSlug/$lessonSlug/"

    Column(modifier = Modifier.fillMaxSize()) {
        NebTopBar(
            showBrand = false,
            title = "Lesson",
            onBack = onNavigateBack
        )

        if (pageProgress < 100) {
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
                    }
                    loadUrl(lessonUrl)
                }
            },
            update = { webView ->
                if (pageProgress == 100) {
                    webView.evaluateJavascript(ANDROID_INJECT_JS, null)
                }
            }
        )
    }
}

private const val ANDROID_INJECT_JS = """
(function() {
    if (document.documentElement.dataset.androidInjected) return;
    document.documentElement.dataset.androidInjected = '1';

    var style = document.createElement('style');
    style.textContent = `
        .md-topbar, .md-bottom-nav, .md-drawer-overlay, .md-side-drawer,
        .ix-breadcrumb, .md-footer, .site-footer, .site-main > .md-container > :not(.ix-lesson-page) {
            display: none !important;
        }
        .site-main {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        .ix-lesson-page {
            padding-top: 8px !important;
            padding-bottom: 0 !important;
        }
        .ix-lesson-layout {
            display: flex !important;
            flex-direction: column !important;
            grid-template-columns: none !important;
        }
        .ix-sim-column {
            width: 100% !important;
            max-width: 100% !important;
            order: 1 !important;
        }
        .ix-learn-column {
            width: 100% !important;
            max-width: 100% !important;
            order: 2 !important;
        }
        .ix-sim-shell {
            position: relative !important;
            top: auto !important;
            border-radius: 12px !important;
        }
        .ix-sim-stage {
            aspect-ratio: 4 / 3 !important;
            max-height: 60vh !important;
            min-height: 200px !important;
        }
        .ix-lesson-header {
            display: none !important;
        }
        body {
            overflow-x: hidden !important;
        }
    `;
    document.head.appendChild(style);

    var topbar = document.querySelector('.md-topbar');
    if (topbar) topbar.remove();
    var footer = document.querySelector('.md-footer') || document.querySelector('.site-footer');
    if (footer) footer.remove();
    var nav = document.querySelector('.md-bottom-nav');
    if (nav) nav.remove();
    var bc = document.querySelector('.ix-breadcrumb');
    if (bc) bc.remove();
    var header = document.querySelector('.ix-lesson-header');
    if (header) header.remove();

    var main = document.querySelector('.site-main');
    if (main) {
        main.style.paddingTop = '0';
        main.style.paddingBottom = '0';
    }
})();
"""