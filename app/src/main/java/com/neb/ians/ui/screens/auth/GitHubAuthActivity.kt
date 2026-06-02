package com.neb.ians.ui.screens.auth

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import com.neb.ians.data.repository.AuthRepository

class GitHubAuthActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val redirectUri = AuthRepository.GITHUB_REDIRECT_URI
        val clientId = AuthRepository.GITHUB_CLIENT_ID
        val authorizeUrl = "https://github.com/login/oauth/authorize?client_id=$clientId&redirect_uri=${Uri.encode(redirectUri)}&scope=read:user,user:email"

        val webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        val layout = FrameLayout(this)
        layout.addView(webView)
        setContentView(layout)

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val url = request?.url?.toString() ?: return false
                if (url.startsWith(redirectUri)) {
                    val uri = Uri.parse(url)
                    val code = uri.getQueryParameter("code")
                    val error = uri.getQueryParameter("error")
                    val errorDescription = uri.getQueryParameter("error_description")

                    val resultIntent = Intent()
                    if (code != null) {
                        resultIntent.putExtra("github_code", code)
                        setResult(RESULT_OK, resultIntent)
                    } else {
                        resultIntent.putExtra("github_error", errorDescription ?: error ?: "GitHub sign-in was cancelled")
                        setResult(RESULT_OK, resultIntent)
                    }
                    finish()
                    return true
                }
                return false
            }
        }

        webView.loadUrl(authorizeUrl)
    }

    override fun onBackPressed() {
        setResult(RESULT_CANCELED)
        super.onBackPressed()
    }
}