package com.neb.ians.ui.screens.interactive

import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.neb.ians.ui.components.NebTopBar

@Composable
fun InteractiveLessonScreen(
    courseSlug: String,
    lessonSlug: String,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    var isLoading by remember { mutableStateOf(true) }
    var progress by remember { mutableStateOf(0) }
    val baseUrl = "https://nebians.consica.com.np"
    val lessonUrl = "$baseUrl/interactive/$courseSlug/$lessonSlug/"

    Column(modifier = Modifier.fillMaxSize()) {
        NebTopBar(
            showBrand = false,
            title = "Lesson",
            onBack = onNavigateBack
        )

        if (isLoading) {
            LinearProgressIndicator(
                progress = { progress / 100f },
                modifier = Modifier.fillMaxSize().padding(horizontal = 0.dp, vertical = 0.dp),
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
                        mixedContentMode = 0 // MIXED_CONTENT_NEVER
                        userAgentString = userAgentString + " NEBiansAndroid"
                    }
                    webViewClient = object : WebViewClient() {
                        override fun onPageFinished(view: WebView?, url: String?) {
                            super.onPageFinished(view, url)
                            isLoading = false
                            progress = 100
                        }
                    }
                    webChromeClient = object : WebChromeClient() {
                        override fun onProgressChanged(view: WebView?, newProgress: Int) {
                            progress = newProgress
                            isLoading = newProgress < 100
                        }
                    }
                    loadUrl(lessonUrl)
                }
            },
            update = { _ -> }
        )
    }
}