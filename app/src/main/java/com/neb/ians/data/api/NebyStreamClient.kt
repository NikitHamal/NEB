package com.neb.ians.data.api

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.flow.map
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

/** Events emitted while streaming an assistant reply from the Neby AI (AI4Bharat Arena) proxy. */
sealed interface NebyStreamEvent {
    data class Meta(val messageId: String?, val userMessageId: String?) : NebyStreamEvent
    data class Delta(val content: String) : NebyStreamEvent
    data class Failed(val message: String) : NebyStreamEvent
    data object Done : NebyStreamEvent
}

/**
 * Consumes the OpenAI-compatible SSE stream from the Django Neby AI proxy.
 * Retrofit can't model a streaming body cleanly, so this uses OkHttp directly.
 */
@Singleton
class NebyStreamClient @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {
    private val baseUrl = "https://nebians.consica.com.np/"

    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(5, TimeUnit.MINUTES)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val json = Json { ignoreUnknownKeys = true }

    fun sendMessage(sessionId: String, content: String): Flow<NebyStreamEvent> =
        stream("api/neby-arena/sessions/$sessionId/messages/", buildBody("content", content))

    fun regenerate(messageId: String): Flow<NebyStreamEvent> =
        stream("api/neby-arena/messages/$messageId/regenerate/", "{}")

    private fun buildBody(key: String, value: String): String {
        // Encode through kotlinx to escape the value safely.
        return json.encodeToString(
            kotlinx.serialization.json.JsonObject.serializer(),
            kotlinx.serialization.json.buildJsonObject {
                put(key, kotlinx.serialization.json.JsonPrimitive(value))
            }
        )
    }

    private fun stream(path: String, body: String): Flow<NebyStreamEvent> = flow {
        val token = dataStore.data.map { it[stringPreferencesKey("auth_token")] }.first()
        if (token.isNullOrBlank()) {
            emit(NebyStreamEvent.Failed("Not signed in"))
            return@flow
        }
        val request = Request.Builder()
            .url(baseUrl + path)
            .header("Authorization", "Bearer $token")
            .header("Accept", "text/event-stream")
            .post(body.toRequestBody("application/json".toMediaType()))
            .build()

        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                emit(NebyStreamEvent.Failed("Server error (${response.code})"))
                return@flow
            }
            val source = response.body?.source()
            if (source == null) {
                emit(NebyStreamEvent.Failed("Empty response"))
                return@flow
            }
            while (!source.exhausted()) {
                val line = source.readUtf8Line() ?: break
                if (!line.startsWith("data:")) continue
                val payload = line.substring(5).trim()
                if (payload.isEmpty()) continue
                if (payload == "[DONE]") {
                    emit(NebyStreamEvent.Done)
                    break
                }
                val event = parse(payload)
                if (event != null) emit(event)
            }
        }
    }.flowOn(Dispatchers.IO)

    private fun parse(payload: String): NebyStreamEvent? {
        val root = try {
            json.parseToJsonElement(payload).jsonObject
        } catch (_: Exception) {
            return null
        }
        root["error"]?.let { err ->
            val msg = (err as? JsonObject)?.get("message")?.jsonPrimitive?.contentOrNull
            return NebyStreamEvent.Failed(msg ?: "Something went wrong")
        }
        val delta = root["choices"]?.jsonArray?.firstOrNull()
            ?.jsonObject?.get("delta")?.jsonObject ?: return null
        val content = delta["content"]?.jsonPrimitive?.contentOrNull
        if (!content.isNullOrEmpty()) {
            return NebyStreamEvent.Delta(content)
        }
        val messageId = delta["messageId"]?.jsonPrimitive?.contentOrNull
        val userMessageId = delta["userMessageId"]?.jsonPrimitive?.contentOrNull
        if (messageId != null || userMessageId != null) {
            return NebyStreamEvent.Meta(messageId, userMessageId)
        }
        return null
    }
}
