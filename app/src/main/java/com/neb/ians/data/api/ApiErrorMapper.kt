package com.neb.ians.data.api

import retrofit2.HttpException
import java.io.IOException
import java.net.SocketTimeoutException
import java.net.UnknownHostException
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.SerializationException

object ApiErrorMapper {
    const val WAF_ERROR_MESSAGE = "NEBians server is temporarily protected by the hosting security filter. Please wait a few minutes and try again. If it keeps happening, switch networks or contact support."

    fun mapException(e: Throwable): String {
        return when (e) {
            is ApiClientException -> e.friendlyMessage
            is HttpException -> {
                val code = e.code()
                val errorBodyStr = try {
                    e.response()?.errorBody()?.string()
                } catch (ex: Exception) {
                    null
                }
                val isHtml = e.response()?.errorBody()?.contentType()?.toString()?.contains("text/html", ignoreCase = true) == true
                
                if (code in listOf(403, 429, 503, 520, 522, 524) && isHtml) {
                    WAF_ERROR_MESSAGE
                } else if (!errorBodyStr.isNullOrEmpty()) {
                    if (errorBodyStr.contains("imunify360", ignoreCase = true) || errorBodyStr.contains("Web Shield", ignoreCase = true)) {
                        WAF_ERROR_MESSAGE
                    } else {
                        try {
                            val jsonElement = Json.parseToJsonElement(errorBodyStr)
                            val errorObject = jsonElement.jsonObject
                            errorObject["error"]?.jsonPrimitive?.content
                                ?: errorObject["message"]?.jsonPrimitive?.content
                                ?: "Server error ($code)"
                        } catch (ex: Exception) {
                            "Server error ($code)"
                        }
                    }
                } else {
                    e.message ?: "An unexpected server error occurred ($code)"
                }
            }
            is UnknownHostException -> "No internet connection. Please check your network."
            is SocketTimeoutException -> "Connection timed out. Please try again."
            is SerializationException -> "The server returned an unexpected response format. Please try again or check your connection."
            is IOException -> {
                val msg = e.message ?: ""
                if (msg.contains("serial name") || msg.contains("required for type") || msg.contains("missing at path")) {
                    "The server returned an unexpected response format. Please try again or check your connection."
                } else {
                    msg.ifEmpty { "Network error. Please try again." }
                }
            }
            else -> {
                val msg = e.message ?: ""
                if (msg.contains("serial name") || msg.contains("required for type") || msg.contains("missing at path")) {
                    "The server returned an unexpected response format. Please try again or check your connection."
                } else {
                    msg.ifEmpty { "An unexpected error occurred." }
                }
            }
        }
    }

    fun isHostSecurityError(e: Throwable): Boolean {
        return when (e) {
            is ApiClientException -> e.isWafBlock
            is HttpException -> {
                val code = e.code()
                val errorBodyStr = try {
                    e.response()?.errorBody()?.string()
                } catch (ex: Exception) {
                    ""
                } ?: ""
                val isHtml = e.response()?.errorBody()?.contentType()?.toString()?.contains("text/html", ignoreCase = true) == true
                (code in listOf(403, 429, 503, 520, 522, 524) && isHtml) ||
                        errorBodyStr.contains("imunify360", ignoreCase = true) ||
                        errorBodyStr.contains("Web Shield", ignoreCase = true)
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
