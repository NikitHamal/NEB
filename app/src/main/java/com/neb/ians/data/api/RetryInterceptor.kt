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

                val shouldRetry = isRetryableStatus(originalRequest.method, response.code)

                if (!shouldRetry) return response

                // Jitter so many phones refused at once do not come back in the same second.
                val waitMs = (retryAfterMs(response) ?: (initialBackoffMs * (1L shl attempt))) +
                    (0..250).random()
                response.close()

                if (attempt < maxRetries) {
                    Thread.sleep(waitMs)
                }
            } catch (e: SocketTimeoutException) {
                lastException = e
                // A timed-out POST may already have been processed: never send it twice.
                if (!isIdempotent(originalRequest.method)) throw e
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
                if (!isIdempotent(originalRequest.method) && e !is java.net.ConnectException) throw e
                if (attempt < maxRetries) {
                    Thread.sleep(initialBackoffMs * (1L shl attempt))
                }
            }
        }

        throw lastException ?: IOException("Max retries ($maxRetries) exhausted")
    }

    private fun isIdempotent(method: String) = method == "GET" || method == "HEAD" || method == "OPTIONS"

    /**
     * 408, 429 and 503 mean the server did not run the request (queue full, worker
     * limit), so every method may be retried. Gateway errors are retried for reads only.
     * A plain 500 is not retried: it is deterministic and a retry only doubles the load.
     */
    private fun isRetryableStatus(method: String, code: Int): Boolean = when (code) {
        408, 429, 503 -> true
        502, 504, 520, 522, 524 -> isIdempotent(method)
        else -> false
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
}