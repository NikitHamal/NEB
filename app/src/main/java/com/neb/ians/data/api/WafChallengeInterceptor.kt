package com.neb.ians.data.api

import android.content.Context
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebView
import android.webkit.WebViewClient
import okhttp3.Interceptor
import okhttp3.Response
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

class WafChallengeInterceptor(private val context: Context) : Interceptor {

    companion object {
        private const val BASE_URL = "https://nebians.consica.com.np/"
        private const val RETRY_HEADER = "X-Waf-Retried"
        private const val CHALLENGE_TIMEOUT_SECONDS = 15L

        @Volatile
        private var cachedCookies: String? = null
    }

    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()

        if (originalRequest.header(RETRY_HEADER) != null) {
            val strippedRequest = originalRequest.newBuilder()
                .removeHeader(RETRY_HEADER)
                .build()
            return chain.proceed(strippedRequest)
        }

        val requestBuilder = originalRequest.newBuilder()
            .header("User-Agent", "Mozilla/5.0 (Linux; Android 11; Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36")
            .header("Accept", "application/json, text/plain, */*")
            .header("Accept-Language", "en-US,en;q=0.9")
            .header("Connection", "keep-alive")
            .header("Sec-Ch-Ua", "\"Chromium\";v=\"125\", \"Android\";v=\"11\"")
            .header("Sec-Ch-Ua-Mobile", "?1")
            .header("Sec-Ch-Ua-Platform", "\"Android\"")

        val currentCookies = cachedCookies ?: CookieManager.getInstance().getCookie(BASE_URL)
        if (!currentCookies.isNullOrEmpty()) {
            requestBuilder.header("Cookie", currentCookies)
        }

        val request = requestBuilder.build()
        val response = chain.proceed(request)

        val contentType = response.body?.contentType()?.toString() ?: ""
        val isHtml = contentType.contains("text/html", ignoreCase = true)
        val isJson = contentType.contains("application/json", ignoreCase = true)
        val isText = contentType.contains("text/plain", ignoreCase = true)

        if (response.code in listOf(200, 403, 503, 429, 520, 522, 524) && (isHtml || isJson || isText)) {
            val bodyString = try {
                response.peekBody(1024 * 50).string()
            } catch (e: Exception) {
                ""
            }

            val isChallenge = bodyString.contains("imunify360", ignoreCase = true) ||
                    bodyString.contains("Web Shield", ignoreCase = true) ||
                    bodyString.contains("wait one moment", ignoreCase = true) ||
                    bodyString.contains("checking your browser", ignoreCase = true) ||
                    bodyString.contains("window.toShowcaptcha", ignoreCase = true)

            if (isChallenge) {
                if (originalRequest.header(RETRY_HEADER) != null) {
                    throw ApiClientException(
                        statusCode = response.code,
                        isWafBlock = true,
                        friendlyMessage = "NEBians server is temporarily protected by the hosting security filter. Please wait a few minutes and try again. If it keeps happening, switch networks or contact support."
                    )
                }

                val solvedCookies = solveChallengeInWebView()
                if (!solvedCookies.isNullOrEmpty()) {
                    cachedCookies = solvedCookies

                    val retriedRequest = originalRequest.newBuilder()
                        .header("User-Agent", "Mozilla/5.0 (Linux; Android 11; Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36")
                        .header("Accept", "application/json, text/plain, */*")
                        .header("Accept-Language", "en-US,en;q=0.9")
                        .header("Connection", "keep-alive")
                        .header("Cookie", solvedCookies)
                        .header(RETRY_HEADER, "true")
                        .build()

                    response.close()
                    return chain.proceed(retriedRequest)
                } else {
                    throw ApiClientException(
                        statusCode = response.code,
                        isWafBlock = true,
                        friendlyMessage = "NEBians server is temporarily protected by the hosting security filter. Please wait a few minutes and try again. If it keeps happening, switch networks or contact support."
                    )
                }
            } else if (isHtml) {
                throw ApiClientException(
                    statusCode = response.code,
                    isWafBlock = false,
                    friendlyMessage = "The server returned an invalid response (HTML). Please check your internet connection or if you need to sign in to your network."
                )
            } else if (response.code in listOf(403, 429, 503, 520, 522, 524)) {
                throw ApiClientException(
                    statusCode = response.code,
                    isWafBlock = true,
                    friendlyMessage = "NEBians server is temporarily protected by the hosting security filter. Please wait a few minutes and try again. If it keeps happening, switch networks or contact support."
                )
            }
        }

        return response
    }

    private fun solveChallengeInWebView(): String? {
        val result = AtomicReference<String?>(null)
        val latch = CountDownLatch(1)
        var webViewRef: WebView? = null

        Handler(Looper.getMainLooper()).post {
            try {
                val webView = WebView(context)
                webViewRef = webView
                val settings = webView.settings
                settings.javaScriptEnabled = true
                settings.domStorageEnabled = true
                settings.databaseEnabled = true
                settings.userAgentString = "Mozilla/5.0 (Linux; Android 11; Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"

                val cookieManager = CookieManager.getInstance()
                cookieManager.setAcceptCookie(true)
                cookieManager.setAcceptThirdPartyCookies(webView, true)

                webView.webViewClient = object : WebViewClient() {
                    private var isFinished = false

                    override fun onPageFinished(view: WebView?, url: String?) {
                        super.onPageFinished(view, url)
                        val cookies = cookieManager.getCookie(BASE_URL)
                        if (!cookies.isNullOrEmpty() && (cookies.contains("revisit") || cookies.contains("shield") || cookies.length > 20)) {
                            if (!isFinished) {
                                isFinished = true
                                result.set(cookies)
                                tryDestroyWebView(webViewRef)
                                latch.countDown()
                            }
                        } else {
                            Handler(Looper.getMainLooper()).postDelayed({
                                if (!isFinished) {
                                    isFinished = true
                                    result.set(cookieManager.getCookie(BASE_URL))
                                    tryDestroyWebView(webViewRef)
                                    latch.countDown()
                                }
                            }, 3000)
                        }
                    }

                    override fun onReceivedError(view: WebView?, errorCode: Int, description: String?, failingUrl: String?) {
                        super.onReceivedError(view, errorCode, description, failingUrl)
                        if (!isFinished) {
                            isFinished = true
                            result.set(null)
                            tryDestroyWebView(webViewRef)
                            latch.countDown()
                        }
                    }
                }

                webView.loadUrl(BASE_URL)
            } catch (e: Exception) {
                result.set(null)
                latch.countDown()
            }
        }

        latch.await(CHALLENGE_TIMEOUT_SECONDS, TimeUnit.SECONDS)
        tryDestroyWebView(webViewRef)
        return result.get()
    }

    private fun tryDestroyWebView(webViewRef: WebView?) {
        try {
            webViewRef?.let {
                Handler(Looper.getMainLooper()).post {
                    try { it.destroy() } catch (_: Exception) {}
                }
            }
        } catch (_: Exception) {}
    }
}
