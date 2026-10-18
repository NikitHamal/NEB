package com.neb.ians.data.api

import okhttp3.Interceptor
import okhttp3.Response
import java.io.IOException
import java.net.SocketTimeoutException
import java.net.UnknownHostException

class RetryInterceptor(private val maxRetries: Int = 3, private val initialBackoffMs: Long = 500) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        var lastException: IOException? = null

        for (attempt in 0..maxRetries) {
            try {
                val response = chain.proceed(originalRequest)

                if (response.isSuccessful || attempt == maxRetries) {
                    return response
                }

                val shouldRetry = response.code in RETRYABLE_STATUS_CODES

                if (!shouldRetry) return response

                val waitMs = retryAfterMs(response) ?: (initialBackoffMs * (1L shl attempt))
                response.close()

                if (attempt < maxRetries) {
                    Thread.sleep(waitMs)
                }
            } catch (e: SocketTimeoutException) {
                lastException = e
                if (attempt < maxRetries) {
                    Thread.sleep(initialBackoffMs * (1L shl attempt))
                }
            } catch (e: UnknownHostException) {
                // Transient mobile DNS failures are common when switching
                // networks; retry with a longer backoff instead of failing.
                lastException = IOException("DNS resolution failed", e)
                if (attempt < maxRetries) {
                    Thread.sleep((initialBackoffMs * 2) * (1L shl attempt))
                }
            } catch (e: IOException) {
                lastException = e
                if (attempt < maxRetries) {
                    Thread.sleep(initialBackoffMs * (1L shl attempt))
                }
            }
        }

        throw lastException ?: IOException("Max retries ($maxRetries) exhausted")
    }

    private fun retryAfterMs(response: Response): Long? {
        if (response.code != 429) return null
        val header = response.header("Retry-After")?.trim().orEmpty()
        if (header.isEmpty()) return null
        val seconds = header.toLongOrNull()
        // Bound the wait so a far-future Retry-After never freezes the UI;
        // the repository layer surfaces the 429 and can retry later.
        val bounded = when {
            seconds != null -> seconds.coerceIn(0L, 30L) * 1000L
            else -> null
        }
        return bounded
    }

    companion object {
        private val RETRYABLE_STATUS_CODES = listOf(408, 429, 500, 502, 503, 504, 520, 522, 524)
    }
}