package com.neb.ians.ui.screens.localai

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.LocalNebyModelManager
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject
import javax.inject.Inject

enum class LocalNebyStatus { NOT_DOWNLOADED, DOWNLOADING, DOWNLOAD_FAILED, READY }

/** A single chat message. `reasoning` and `navPage` are only set on assistant messages. */
data class LocalNebyMessage(
    val id: Long,
    val role: String,           // "user" | "assistant"
    val text: String,
    val reasoning: String = "",
    val confidence: Double? = null,
    val navPage: String? = null, // for navigate_to tool calls (offline navigation)
    val toolName: String? = null,
)

data class LocalNebyUiState(
    val status: LocalNebyStatus = LocalNebyStatus.NOT_DOWNLOADED,
    val progress: Int = 0,
    val messages: List<LocalNebyMessage> = emptyList(),
    val isThinking: Boolean = false,
    val engineReady: Boolean = false,
    val loadSeconds: String? = null,
    val snackbar: String? = null,
)

@HiltViewModel
class LocalNebyViewModel @Inject constructor(
    @ApplicationContext private val appContext: Context,
) : ViewModel() {

    private val manager = LocalNebyModelManager(appContext)
    private var engine: LocalNebyWebEngine? = null

    private val _uiState = MutableStateFlow(LocalNebyUiState())
    val uiState: StateFlow<LocalNebyUiState> = _uiState.asStateFlow()

    val assetDir = manager.assetDir
    val totalBytes: Long get() = manager.totalBytes()

    init {
        load()
    }

    fun load() {
        _uiState.update {
            it.copy(status = if (manager.isReady()) LocalNebyStatus.READY else LocalNebyStatus.NOT_DOWNLOADED)
        }
    }

    /** Called by the screen once it has created the WebView engine. */
    fun attachEngine(engine: LocalNebyWebEngine) {
        this.engine = engine
        engine.setCallbacks(
            onReady = { seconds -> onEngineReady(seconds) },
            onResult = { json -> onInferenceResult(json) },
            onError = { msg -> onEngineError(msg) },
        )
    }

    fun downloadModel() {
        if (_uiState.value.status == LocalNebyStatus.DOWNLOADING) return
        _uiState.update { it.copy(status = LocalNebyStatus.DOWNLOADING, progress = 0) }
        viewModelScope.launch {
            val result = manager.download { pct ->
                _uiState.update { it.copy(progress = pct) }
            }
            result.fold(
                onSuccess = {
                    _uiState.update {
                        it.copy(status = LocalNebyStatus.READY, progress = 100, snackbar = "Model ready — works offline now")
                    }
                },
                onFailure = { e ->
                    _uiState.update {
                        it.copy(
                            status = LocalNebyStatus.DOWNLOAD_FAILED,
                            snackbar = e.message?.takeIf { it.isNotBlank() } ?: "Download failed",
                        )
                    }
                },
            )
        }
    }

    fun deleteModel() {
        engine?.destroy()
        manager.delete()
        _uiState.update {
            it.copy(status = LocalNebyStatus.NOT_DOWNLOADED, messages = emptyList(), engineReady = false, loadSeconds = null)
        }
    }

    fun send(text: String) {
        val trimmed = text.trim()
        val state = _uiState.value
        if (trimmed.isEmpty() || state.isThinking) return
        if (!state.engineReady) {
            _uiState.update { it.copy(snackbar = "Model is still loading — one second.") }
            return
        }
        val now = System.currentTimeMillis()
        _uiState.update {
            it.copy(
                messages = it.messages + LocalNebyMessage(now, "user", trimmed),
                isThinking = true,
            )
        }
        engine?.runQuery(trimmed)
    }

    private fun onEngineReady(seconds: String) {
        _uiState.update { it.copy(engineReady = true, loadSeconds = seconds) }
    }

    private fun onEngineError(message: String) {
        _uiState.update {
            it.copy(isThinking = false, snackbar = "Model error: ${message.take(120)}")
        }
    }

    /** Parses the model's JSON result (which includes `reasoning`) and renders it. */
    private fun onInferenceResult(json: String) {
        val now = System.currentTimeMillis()
        _uiState.update { state ->
            val (text, reasoning, confidence, navPage, toolName) = parseResult(json)
            val msg = LocalNebyMessage(
                id = now,
                role = "assistant",
                text = text,
                reasoning = reasoning,
                confidence = confidence,
                navPage = navPage,
                toolName = toolName,
            )
            state.copy(messages = state.messages + msg, isThinking = false)
        }
    }

    private fun parseResult(json: String): ResultParts {
        return try {
            val obj = JSONObject(json)
            val calls: JSONArray = obj.optJSONArray("function_calls") ?: JSONArray()
            val reasoning = obj.optString("reasoning", "").trim().takeIf { it.isNotEmpty() }
            val confidence = if (obj.has("confidence") && !obj.isNull("confidence")) {
                obj.optDouble("confidence")
            } else null

            if (calls.length() == 0) {
                ResultParts(
                    text = reasoning ?: "I couldn't map that to anything in my toolkit. Try a study question like \u201Cfind physics notes for class 12\u201D.",
                    reasoning = "",
                    confidence = confidence,
                    navPage = null,
                    toolName = null,
                )
            } else {
                val call = calls.getJSONObject(0)
                val name = call.optString("name")
                val args = call.optJSONObject("arguments") ?: JSONObject()
                val argPairs = args.keys().asSequence().joinToString(", ") { k ->
                    "$k=${args.optString(k)}"
                }
                val navPage = if (name == "navigate_to") args.optString("page").takeIf { it.isNotBlank() } else null
                val text = when (name) {
                    "navigate_to" -> "Opening ${args.optString("page", "that page")} for you."
                    else -> "I'd use $name${if (argPairs.isNotBlank()) " with $argPairs" else ""} for you."
                }
                ResultParts(text, reasoning ?: "", confidence, navPage, name)
            }
        } catch (e: Exception) {
            ResultParts("The on-device model returned something I couldn't read.", "", null, null, null)
        }
    }

    fun clearSnackbar() {
        _uiState.update { it.copy(snackbar = null) }
    }

    private data class ResultParts(
        val text: String,
        val reasoning: String,
        val confidence: Double?,
        val navPage: String?,
        val toolName: String?,
    )
}
