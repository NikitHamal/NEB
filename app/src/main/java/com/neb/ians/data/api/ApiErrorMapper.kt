package com.neb.ians.data.api

import retrofit2.HttpException
import java.io.IOException
import java.net.SocketTimeoutException
import java.net.UnknownHostException

object ApiErrorMapper {
    fun mapException(e: Throwable): String {
        return when (e) {
            is ApiClientException -> e.friendlyMessage
            is HttpException -> {
                val code = e.code()
                val isHtml = e.response()?.errorBody()?.contentType()?.toString()?.contains("text/html", ignoreCase = true) == true
                if (code in listOf(403, 429, 503, 520, 522, 524) && isHtml) {
                    "NEBians server is temporarily protected by the hosting security filter. Please wait a few minutes and try again. If it keeps happening, switch networks or contact support."
                } else {
                    e.message ?: "An unexpected server error occurred ($code)"
                }
            }
            is UnknownHostException -> "No internet connection. Please check your network."
            is SocketTimeoutException -> "Connection timed out. Please try again."
            is IOException -> e.message ?: "Network error. Please try again."
            else -> e.message ?: "An unexpected error occurred."
        }
    }

    fun isHostSecurityError(e: Throwable): Boolean {
        return when (e) {
            is ApiClientException -> e.isWafBlock
            is HttpException -> {
                val code = e.code()
                val isHtml = e.response()?.errorBody()?.contentType()?.toString()?.contains("text/html", ignoreCase = true) == true
                code in listOf(403, 429, 503, 520, 522, 524) && isHtml
            }
            else -> false
        }
    }
}

class ApiClientException(
    val statusCode: Int,
    val isWafBlock: Boolean,
    val friendlyMessage: String,
    cause: Throwable? = null
) : IOException(friendlyMessage, cause)
