package com.neb.ians.ui.screens.canvas

import com.neb.ians.data.api.ApiArenaCreateSessionRequest
import com.neb.ians.data.api.ApiArenaModel
import com.neb.ians.data.api.ApiArenaSendMessageRequest
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import okhttp3.ResponseBody
import org.json.JSONObject
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

class CanvasAiException(message: String) : Exception(message)

@Singleton
class CanvasAiGenerator @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {

    private val sessionMutex = Mutex()
    private val sessionByBoard = mutableMapOf<String, String>()
    private var cachedModels: List<ApiArenaModel> = emptyList()

    suspend fun generate(
        prompt: String,
        boardId: String,
        parentId: String?,
        baseX: Float,
        baseY: Float,
        webSearch: Boolean,
        speedMode: String,
        context: String?
    ): CanvasNode = withContext(Dispatchers.IO) {
        val token = authRepository.getBearerToken()
            ?: throw CanvasAiException("Sign in to generate with Neby")

        val instruction = buildInstruction(prompt, context, webSearch, speedMode)

        val raw = try {
            exchange(token, boardId, instruction, speedMode)
        } catch (e: CanvasAiException) {
            throw e
        } catch (e: Exception) {
            sessionMutex.withLock { sessionByBoard.remove(boardId) }
            exchange(token, boardId, instruction, speedMode)
        }

        val obj = extractJsonObject(raw)
            ?: throw CanvasAiException("Neby returned an unreadable answer")

        toNode(obj, prompt, boardId, parentId, baseX, baseY, webSearch, speedMode)
    }

    private suspend fun exchange(
        token: String,
        boardId: String,
        instruction: String,
        speedMode: String
    ): String {
        val sessionId = ensureSession(token, boardId, speedMode)
        val body = apiService.sendArenaMessage(token, sessionId, ApiArenaSendMessageRequest(instruction))
        val streamed = consumeSse(body)
        if (streamed.isNotBlank()) return streamed
        val detail = apiService.getArenaSessionDetail(token, sessionId)
        return detail.messages.lastOrNull { it.role == "assistant" }?.content.orEmpty()
    }

    private suspend fun ensureSession(token: String, boardId: String, speedMode: String): String =
        sessionMutex.withLock {
            sessionByBoard[boardId]?.let { return@withLock it }

            if (cachedModels.isEmpty()) {
                cachedModels = runCatching {
                    apiService.getArenaModels(token).models.filter { it.active && it.id.isNotBlank() }
                }.getOrDefault(emptyList())
            }
            if (cachedModels.isEmpty()) {
                throw CanvasAiException("No Neby models are available right now")
            }
            val model = if (speedMode == "deep") {
                cachedModels.firstOrNull { it.thinking && !it.randomOnly } ?: cachedModels.first()
            } else {
                cachedModels.firstOrNull { !it.thinking && !it.randomOnly } ?: cachedModels.first()
            }
            val response = apiService.createArenaSession(
                token,
                ApiArenaCreateSessionRequest(modelId = model.id, title = "Canvas board")
            )
            sessionByBoard[boardId] = response.session.id
            response.session.id
        }

    private fun consumeSse(body: ResponseBody): String {
        val builder = StringBuilder()
        var failure: String? = null
        body.byteStream().bufferedReader().useLines { lines ->
            for (line in lines) {
                if (!line.startsWith("data:")) continue
                val payload = line.removePrefix("data:").trim()
                if (payload.isEmpty()) continue
                if (payload == "[DONE]") break
                val root = runCatching { JSONObject(payload) }.getOrNull() ?: continue
                val error = root.optJSONObject("error")
                if (error != null) {
                    failure = error.optString("message").ifBlank { "Neby hit an error" }
                    break
                }
                root.optJSONArray("choices")
                    ?.optJSONObject(0)
                    ?.optJSONObject("delta")
                    ?.optString("content")
                    ?.takeIf { it.isNotEmpty() }
                    ?.let { builder.append(it) }
            }
        }
        failure?.let { throw CanvasAiException(it) }
        return builder.toString()
    }

    private fun buildInstruction(
        prompt: String,
        context: String?,
        webSearch: Boolean,
        speedMode: String
    ): String {
        val depth = if (speedMode == "deep") {
            "Go deep: four to six sections, exam-grade rigour."
        } else {
            "Stay tight: two to four sections, no padding."
        }
        val search = if (webSearch) {
            "Prefer current, verifiable facts; name sources inline when a claim is time-sensitive."
        } else {
            ""
        }
        val parent = context?.takeIf { it.isNotBlank() }?.let {
            "This card branches from an existing card titled \"$it\". Build on it, do not repeat it.\n"
        }.orEmpty()

        return buildString {
            appendLine("You are Neby, the study companion inside the NEBians app for Nepali students.")
            appendLine("Turn the request below into ONE visual knowledge card.")
            appendLine("Reply with a single raw JSON object and nothing else. No prose, no markdown fence.")
            appendLine()
            appendLine("Schema:")
            appendLine("{")
            appendLine("  \"title\": string, max 46 chars,")
            appendLine("  \"kind\": one of topic|question|practice|summary|comparison|note|task|goal,")
            appendLine("  \"color\": one of default|blue|green|amber|rose|purple|slate,")
            appendLine("  \"summary\": string, 1-2 sentences, **bold** allowed,")
            appendLine("  \"sections\": [ section, ... ]")
            appendLine("}")
            appendLine()
            appendLine("A section is one of:")
            appendLine("{\"type\":\"text\",\"content\":string}")
            appendLine("{\"type\":\"bullets\",\"title\":string,\"bulletItems\":[string]}")
            appendLine("{\"type\":\"comparison\",\"title\":string,\"headers\":[string],\"rows\":[[string]]}")
            appendLine("{\"type\":\"diagram\",\"title\":string,\"nodes\":[{\"id\":string,\"label\":string,\"desc\":string}]}")
            appendLine("{\"type\":\"cards\",\"title\":string,\"cardItems\":[{\"title\":string,\"subtitle\":string,\"bullets\":[string]}]}")
            appendLine("{\"type\":\"flowchart\",\"title\":string,\"flowSteps\":[{\"title\":string,\"desc\":string}]}")
            appendLine("{\"type\":\"timeline\",\"title\":string,\"timelineItems\":[{\"number\":int,\"title\":string,\"subtitle\":string}]}")
            appendLine()
            appendLine(depth)
            if (search.isNotBlank()) appendLine(search)
            appendLine("Write plain ASCII for formulae (eta = 1 - T_C / T_H). Keep every string under 220 chars.")
            appendLine()
            append(parent)
            append("Request: ")
            append(prompt.trim())
        }
    }

    private fun extractJsonObject(raw: String): JSONObject? {
        if (raw.isBlank()) return null
        val cleaned = raw
            .replace("```json", "")
            .replace("```", "")
            .trim()
        val start = cleaned.indexOf('{')
        val end = cleaned.lastIndexOf('}')
        if (start < 0 || end <= start) return null
        return runCatching { JSONObject(cleaned.substring(start, end + 1)) }.getOrNull()
    }

    private fun toNode(
        obj: JSONObject,
        prompt: String,
        boardId: String,
        parentId: String?,
        baseX: Float,
        baseY: Float,
        webSearch: Boolean,
        speedMode: String
    ): CanvasNode {
        val content = CanvasJsonSerializer.parseContent(obj)
        val title = obj.optString("title").ifBlank { content.title }
            .ifBlank { prompt.trim().take(38) }
        if (content.summary.isBlank() && content.sections.isEmpty()) {
            throw CanvasAiException("Neby returned an empty card")
        }
        val kind = obj.optString("kind", "topic").lowercase().ifBlank { "topic" }
        val color = obj.optString("color", "default").lowercase()
            .takeIf { it in ALLOWED_COLORS } ?: "default"

        return CanvasNode(
            id = "node_${System.currentTimeMillis()}_${UUID.randomUUID().toString().take(5)}",
            boardId = boardId,
            parentId = parentId,
            prompt = prompt.trim(),
            title = title,
            content = content.copy(title = title),
            status = "done",
            x = baseX,
            y = baseY,
            kind = kind,
            color = color,
            webSearchEnabled = webSearch,
            modelUsed = speedMode,
            createdAt = System.currentTimeMillis(),
            updatedAt = System.currentTimeMillis()
        )
    }

    companion object {
        private val ALLOWED_COLORS = setOf("default", "blue", "green", "amber", "rose", "purple", "slate")
    }
}
