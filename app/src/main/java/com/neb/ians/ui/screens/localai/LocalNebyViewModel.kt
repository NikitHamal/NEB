package com.neb.ians.ui.screens.localai

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.needle.LocalNeedleMessage
import com.neb.ians.data.needle.LocalNeedleToolCall
import com.neb.ians.data.needle.NeedleChatStore
import com.neb.ians.data.needle.NeedleModelManager
import com.neb.ians.data.needle.NeedleModelState
import com.neb.ians.data.needle.NeedleWebRuntime
import dagger.hilt.android.lifecycle.HiltViewModel
import java.util.UUID
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.doubleOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

@HiltViewModel
class LocalNebyViewModel @Inject constructor(
    private val modelManager: NeedleModelManager,
    private val runtime: NeedleWebRuntime,
    private val chatStore: NeedleChatStore
) : ViewModel() {
    val modelState = modelManager.state
    val runtimeState = runtime.state
    val messages = chatStore.messages
    private val json = Json { ignoreUnknownKeys = true }
    private val _isRunning = MutableStateFlow(false)
    val isRunning: StateFlow<Boolean> = _isRunning.asStateFlow()

    init {
        viewModelScope.launch {
            modelState.collect { state ->
                if (state is NeedleModelState.Ready) runtime.prepare()
            }
        }
        viewModelScope.launch {
            runtime.results.collect { response ->
                _isRunning.value = false
                chatStore.add(parseResponse(response.requestId, response.resultJson, response.durationMs))
            }
        }
        viewModelScope.launch {
            runtime.errors.collect { (requestId, message) ->
                _isRunning.value = false
                chatStore.add(
                    LocalNeedleMessage(
                        id = requestId?.let { "error-$it" } ?: UUID.randomUUID().toString(),
                        isUser = false,
                        text = message
                    )
                )
            }
        }
    }

    fun downloadModel() = modelManager.download()

    fun cancelDownload() = modelManager.cancelDownload()

    fun deleteModel() {
        runtime.release(clearSavedRuntime = true)
        modelManager.deleteModel()
    }

    fun retryRuntime() = runtime.restart()

    fun clearHistory() = chatStore.clear()

    fun send(query: String) {
        val clean = query.trim()
        if (clean.isEmpty() || _isRunning.value) return
        val requestId = UUID.randomUUID().toString()
        chatStore.add(
            LocalNeedleMessage(
                id = "user-$requestId",
                isUser = true,
                text = clean
            )
        )
        if (runtime.run(requestId, clean)) {
            _isRunning.value = true
        } else {
            chatStore.add(
                LocalNeedleMessage(
                    id = "error-$requestId",
                    isUser = false,
                    text = "The local model is still preparing. Please try again in a moment."
                )
            )
        }
    }

    private fun parseResponse(requestId: String, raw: String, durationMs: Double): LocalNeedleMessage {
        val root = runCatching { json.parseToJsonElement(raw).jsonObject }.getOrNull()
        if (root == null) {
            return LocalNeedleMessage(
                id = "assistant-$requestId",
                isUser = false,
                text = "Needle returned an unreadable response. Please rephrase your request."
            )
        }
        val calls = root["function_calls"]?.jsonArray.orEmpty().mapNotNull { element ->
            val call = runCatching { element.jsonObject }.getOrNull() ?: return@mapNotNull null
            val name = call["name"]?.jsonPrimitive?.contentOrNull ?: return@mapNotNull null
            LocalNeedleToolCall(name, call["arguments"]?.toString() ?: "{}")
        }
        return LocalNeedleMessage(
            id = "assistant-$requestId",
            isUser = false,
            text = responseText(calls),
            reasoning = root["reasoning"]?.jsonPrimitive?.contentOrNull,
            confidence = root["confidence"]?.jsonPrimitive?.doubleOrNull,
            durationMs = durationMs,
            toolCalls = calls
        )
    }

    private fun responseText(calls: List<LocalNeedleToolCall>): String {
        if (calls.isEmpty()) {
            return "I couldn't map that request to a NEBians action. I work best with resource searches, forum requests, subjects, and app navigation."
        }
        if (calls.size > 1) return "Needle selected ${calls.size} on-device actions."
        return when (calls.first().name) {
            "search_resources" -> "I understood this as a resource search."
            "find_notes" -> "I understood this as a notes or past-paper search."
            "get_forum_posts" -> "I found the matching forum action."
            "get_subjects" -> "I can open the available subjects."
            "navigate_to" -> "I found the destination you asked for."
            else -> "Needle selected an on-device action."
        }
    }
}
