package com.neb.ians.data.api

import retrofit2.HttpException
import java.io.IOException
import java.net.ConnectException
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
            is OfflineException -> "You're offline. Saved content will stay available when it has been loaded before."
            is ApiClientException -> e.friendlyMessage
            is HttpException -> mapHttpException(e)
            is UnknownHostException -> "You're offline. Please check your internet connection."
            is ConnectException -> "Couldn't connect to NEBians. Please check your internet connection."
            is SocketTimeoutException -> "The connection took too long. Please try again."
            is SerializationException -> "Something changed on the server. Please update the app or try again."
            is IOException -> mapNetworkMessage(e.message)
            else -> mapUnexpectedMessage(e.message)
        }
    }

    private fun mapHttpException(e: HttpException): String {
        val code = e.code()
        val errorBodyStr = try {
            e.response()?.errorBody()?.string()
        } catch (_: Exception) {
            null
        }
        val isHtml = e.response()?.errorBody()?.contentType()?.toString()?.contains("text/html", ignoreCase = true) == true
        if (code in listOf(403, 429, 503, 520, 522, 524) && isHtml) return WAF_ERROR_MESSAGE
        if (!errorBodyStr.isNullOrEmpty()) {
            if (errorBodyStr.contains("imunify360", ignoreCase = true) || errorBodyStr.contains("Web Shield", ignoreCase = true)) return WAF_ERROR_MESSAGE
            val parsed = parseServerMessage(errorBodyStr)
            if (!parsed.isNullOrBlank()) return parsed
        }
        return when (code) {
            400 -> "Please check the information and try again."
            401 -> "Please sign in again to continue."
            403 -> "You don't have permission to do that."
            404 -> "This content is no longer available."
            408 -> "The request took too long. Please try again."
            409 -> "This change conflicts with newer content. Please refresh and try again."
            413 -> "That file is too large. Please choose a smaller file."
            429 -> "Too many requests. Please wait a moment and try again."
            in 500..599 -> "NEBians is having trouble right now. Please try again shortly."
            else -> "Something went wrong. Please try again."
        }
    }

    private fun parseServerMessage(body: String): String? {
        return try {
            val jsonElement = Json.parseToJsonElement(body)
            val errorObject = jsonElement.jsonObject
            
            // 1. Try standard keys
            val raw = try {
                errorObject["error"]?.jsonPrimitive?.content
                    ?: errorObject["message"]?.jsonPrimitive?.content
                    ?: errorObject["detail"]?.jsonPrimitive?.content
            } catch (_: Exception) { null }
            
            if (raw != null) {
                return sanitize(raw)
            }
            
            // 2. Try parsing field errors dictionary
            val fieldErrors = mutableListOf<String>()
            for ((key, value) in errorObject) {
                val errors = when (value) {
                    is kotlinx.serialization.json.JsonArray -> {
                        value.mapNotNull { 
                            try { it.jsonPrimitive.content } catch (_: Exception) { null }
                        }.filter { it.isNotBlank() }
                    }
                    is kotlinx.serialization.json.JsonPrimitive -> {
                        try {
                            val content = value.content
                            if (content.isNotBlank()) listOf(content) else emptyList()
                        } catch (_: Exception) { emptyList() }
                    }
                    else -> emptyList()
                }
                if (errors.isNotEmpty()) {
                    fieldErrors.add("$key: ${errors.joinToString(", ")}")
                }
            }
            
            if (fieldErrors.isNotEmpty()) {
                return sanitize(fieldErrors.joinToString("; "))
            }
            null
        } catch (_: Exception) {
            null
        }
    }

    private fun mapNetworkMessage(message: String?): String {
        val msg = message.orEmpty()
        return when {
            msg.isBlank() -> "Network error. Please try again."
            isDeveloperMessage(msg) -> "Something went wrong. Please try again."
            msg.contains("timeout", ignoreCase = true) -> "The connection took too long. Please try again."
            msg.contains("failed to connect", ignoreCase = true) -> "Couldn't connect to NEBians. Please check your internet connection."
            else -> "Network error. Please try again."
        }
    }

    private fun mapUnexpectedMessage(message: String?): String {
        val msg = message.orEmpty()
        return when {
            msg.isBlank() || isDeveloperMessage(msg) -> "Something went wrong. Please try again."
            msg == "Not authenticated" -> "Please sign in to continue."
            else -> sanitize(msg) ?: "Something went wrong. Please try again."
        }
    }

    private fun sanitize(message: String?): String? {
        val msg = message?.trim().orEmpty()
        if (msg.isBlank() || isDeveloperMessage(msg)) return null
        return msg.take(180)
    }

    private fun isDeveloperMessage(message: String): Boolean {
        val msg = message.lowercase()
        return listOf(
            "serial name",
            "required for type",
            "missing at path",
            "jsonencodingexception",
            "jsondecodingexception",
            "jsonsyntaxexception",
            "stacktrace",
            "traceback",
            "nullpointer",
            "sqlite",
            "room",
            "retrofit",
            "okhttp",
            "java.",
            "kotlin."
        ).any { it in msg }
    }

    /**
     * Contributor-facing diagnostic mapping for upload / edit failures. Unlike
     * [mapException] (which hides server internals behind friendly strings so
     * students aren't shown tracebacks), this surfaces the *real* cause — HTTP
     * status, the server's error body, and the exception class — and logs the
     * full throwable to logcat (tag "NebUpload"). Upload/edit screens are
     * owner/contributor only, so a technical message here is both safe and
     * exactly what's needed to answer "why did my upload fail?".
     */
    fun mapExceptionVerbose(e: Throwable, op: String): String {
        val httpBody = if (e is HttpException) safeErrorBody(e) else null
        logRawWithBody(e, op, httpBody)
        return when (e) {
            is HttpException -> {
                val code = e.code()
                val serverMsg = httpBody?.let { parseServerMessage(it) }
                val snippet = httpBody?.replace(Regex("\\s+"), " ")?.trim()?.take(180).orEmpty()
                val detail = serverMsg ?: snippet.ifBlank { "(empty response body)" }
                "$op failed (HTTP $code): $detail"
            }
            is SerializationException ->
                "$op failed: the server's reply didn't match this app version - please update the app. (${e.message?.take(80).orEmpty()})"
            else -> {
                val friendly = mapException(e)
                val raw = e.message?.replace(Regex("\\s+"), " ")?.trim()?.take(140).orEmpty()
                val cls = e::class.simpleName ?: "Error"
                if (friendly.contains("Something went wrong") || friendly.contains("Network error")) {
                    "$op failed ($cls): ${raw.ifBlank { friendly }}"
                } else {
                    friendly
                }
            }
        }
    }

    private fun safeErrorBody(e: HttpException): String? =
        try { e.response()?.errorBody()?.string() } catch (_: Exception) { null }

    private fun logRaw(e: Throwable, op: String) {
        val body = if (e is HttpException) safeErrorBody(e) else null
        logRawWithBody(e, op, body)
    }

    private fun logRawWithBody(e: Throwable, op: String, errorBody: String?) {
        try {
            val body = if (e is HttpException && !errorBody.isNullOrBlank()) " HTTP ${e.code()} body=${errorBody.take(600)}" else ""
            android.util.Log.e("NebUpload", "$op failed: ${e::class.qualifiedName}: ${e.message}$body", e)
        } catch (_: Throwable) {
            // The unit-test JVM has no android.util.Log; never let logging break a flow.
        }
    }

    fun isHostSecurityError(e: Throwable): Boolean {
        return when (e) {
            is ApiClientException -> e.isWafBlock
            is HttpException -> {
                val code = e.code()
                val errorBodyStr = try {
                    e.response()?.errorBody()?.string()
                } catch (_: Exception) {
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

class OfflineException : IOException("No internet connection")

class ApiClientException(
    val statusCode: Int,
    val isWafBlock: Boolean,
    val friendlyMessage: String,
    cause: Throwable? = null
) : IOException(friendlyMessage, cause)
