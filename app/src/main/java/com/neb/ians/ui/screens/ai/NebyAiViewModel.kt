package com.neb.ians.ui.screens.ai

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import android.util.Base64
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiArenaCreateSessionRequest
import com.neb.ians.data.api.ApiArenaMessage
import com.neb.ians.data.api.ApiArenaModel
import com.neb.ians.data.api.ApiArenaSendMessageRequest
import com.neb.ians.data.api.ApiArenaSession
import com.neb.ians.data.api.ApiArenaUpdateSessionRequest
import com.neb.ians.data.api.ApiQwenFile
import com.neb.ians.data.api.ApiQwenSendMessageRequest
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import okhttp3.ResponseBody
import retrofit2.HttpException
import javax.inject.Inject

/** Which model catalogue is being browsed in the model picker. */
enum class ModelSource { ARENA, QWEN }

/** A file the user has attached but not yet sent. */
data class PendingFile(
    val uri: Uri,
    val name: String,
    val sizeBytes: Long
)

data class NebyAiUiState(
    val arenaModels: List<ApiArenaModel> = emptyList(),
    val qwenModels: List<ApiArenaModel> = emptyList(),
    val sessions: List<ApiArenaSession> = emptyList(),
    val selectedSession: ApiArenaSession? = null,
    val messages: List<ApiArenaMessage> = emptyList(),
    val selectedSource: ModelSource = ModelSource.ARENA,
    val selectedModelId: String? = null,
    val pendingFiles: List<PendingFile> = emptyList(),
    val isLoading: Boolean = true,
    val isStreaming: Boolean = false,
    val isCreatingSession: Boolean = false,
    /** Fatal error shown as an empty state when nothing else can render. */
    val error: String? = null,
    /** Transient message surfaced through a snackbar. */
    val snackbar: String? = null
) {
    val visibleModels: List<ApiArenaModel>
        get() = if (selectedSource == ModelSource.QWEN) qwenModels else arenaModels
}

@HiltViewModel
class NebyAiViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    @ApplicationContext private val appContext: Context
) : ViewModel() {

    companion object {
        private const val MAX_FILES = 5
        private const val MAX_FILE_BYTES = 20L * 1024L * 1024L
        private const val DEFAULT_TITLE = "New chat"
        private const val DEFAULT_QWEN_MODEL_ID = "qwen3.7-plus"
        private const val POOL_EXHAUSTED_MESSAGE = "Neby is at capacity, try again in a minute."
        private val ALLOWED_EXTENSIONS = setOf(
            "png", "jpg", "jpeg", "gif", "webp", "bmp", "svg",
            "pdf", "txt", "doc", "docx",
            "mp4", "avi", "mov", "mkv", "webm",
            "mp3", "wav", "ogg", "flac", "aac", "m4a"
        )
    }

    private val json = Json { ignoreUnknownKeys = true }
    private val _uiState = MutableStateFlow(NebyAiUiState())
    val uiState: StateFlow<NebyAiUiState> = _uiState.asStateFlow()

    /** Mutable holder for ids the server reports mid-stream. */
    private class StreamResult {
        var assistantServerId: String? = null
        var userServerId: String? = null
        var errored: Boolean = false
    }

    init {
        load()
    }

    // ------------------------------------------------------------------
    // Loading
    // ------------------------------------------------------------------

    fun load() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to use Neby AI") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val arenaModels = runCatching {
                    apiService.getArenaModels(token).models.filter { it.active && it.id.isNotBlank() }
                }.getOrDefault(emptyList())
                val qwenModels = runCatching {
                    apiService.getQwenModels(token).models.filter { it.active && it.id.isNotBlank() }
                }.getOrDefault(emptyList())
                val sessions = apiService.getArenaSessions(token).sessions
                _uiState.update {
                    it.copy(
                        arenaModels = arenaModels,
                        qwenModels = qwenModels,
                        sessions = sessions,
                        isLoading = false,
                        selectedModelId = it.selectedModelId
                            ?: arenaModels.firstOrNull()?.id
                            ?: qwenModels.firstOrNull()?.id
                    )
                }
                sessions.firstOrNull()?.let { openSession(it.id) }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load Neby AI")
                }
            }
        }
    }

    // ------------------------------------------------------------------
    // Model picker / source switcher
    // ------------------------------------------------------------------

    fun selectSource(source: ModelSource) {
        _uiState.update { state ->
            if (state.selectedSource == source) state
            else {
                val models = if (source == ModelSource.QWEN) state.qwenModels else state.arenaModels
                state.copy(selectedSource = source, selectedModelId = models.firstOrNull()?.id)
            }
        }
    }

    fun selectModel(modelId: String) {
        _uiState.update { it.copy(selectedModelId = modelId) }
    }

    /** Creates a session with the currently selected model and switches to it. */
    fun startChat() {
        val state = _uiState.value
        if (state.isCreatingSession) return
        val modelId = state.selectedModelId ?: state.visibleModels.firstOrNull()?.id
        if (modelId == null) {
            _uiState.update { it.copy(snackbar = "No AI models are currently available") }
            return
        }
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: run {
                _uiState.update { it.copy(snackbar = "Sign in to use Neby AI") }
                return@launch
            }
            _uiState.update { it.copy(isCreatingSession = true) }
            try {
                val request = ApiArenaCreateSessionRequest(modelId = modelId, title = DEFAULT_TITLE)
                val response = if (state.selectedSource == ModelSource.QWEN) {
                    apiService.createQwenArenaSession(token, request)
                } else {
                    apiService.createArenaSession(token, request)
                }
                _uiState.update {
                    it.copy(
                        sessions = listOf(response.session) + it.sessions,
                        selectedSession = response.session,
                        messages = emptyList(),
                        isCreatingSession = false
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isCreatingSession = false, snackbar = friendlyError(e, "Could not create chat"))
                }
            }
        }
    }

    // ------------------------------------------------------------------
    // Sessions
    // ------------------------------------------------------------------

    fun openSession(sessionId: String) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                val detail = apiService.getArenaSessionDetail(token, sessionId)
                _uiState.update {
                    it.copy(
                        selectedSession = detail.session,
                        messages = detail.messages,
                        pendingFiles = emptyList(),
                        error = null
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(snackbar = friendlyError(e, "Could not open chat")) }
            }
        }
    }

    /** Clears the active session so the model picker is shown again. */
    fun startNewChat() {
        _uiState.update {
            it.copy(selectedSession = null, messages = emptyList(), pendingFiles = emptyList())
        }
    }

    fun renameSession(sessionId: String, newTitle: String) {
        val title = newTitle.trim().take(80)
        if (title.isBlank()) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                apiService.updateArenaSession(token, sessionId, ApiArenaUpdateSessionRequest(title = title))
                _uiState.update { state ->
                    state.copy(
                        sessions = state.sessions.map {
                            if (it.id == sessionId) it.copy(title = title) else it
                        },
                        selectedSession = state.selectedSession?.let {
                            if (it.id == sessionId) it.copy(title = title) else it
                        }
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(snackbar = friendlyError(e, "Could not rename chat")) }
            }
        }
    }

    fun deleteSession(sessionId: String) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                apiService.deleteArenaSession(token, sessionId)
                _uiState.update { state ->
                    val wasActive = state.selectedSession?.id == sessionId
                    state.copy(
                        sessions = state.sessions.filterNot { it.id == sessionId },
                        selectedSession = if (wasActive) null else state.selectedSession,
                        messages = if (wasActive) emptyList() else state.messages,
                        pendingFiles = if (wasActive) emptyList() else state.pendingFiles
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(snackbar = friendlyError(e, "Could not delete chat")) }
            }
        }
    }

    // ------------------------------------------------------------------
    // File attachments (Qwen)
    // ------------------------------------------------------------------

    fun addFiles(uris: List<Uri>) {
        if (uris.isEmpty()) return
        viewModelScope.launch(Dispatchers.IO) {
            val current = _uiState.value.pendingFiles.toMutableList()
            var rejection: String? = null
            for (uri in uris) {
                if (current.size >= MAX_FILES) {
                    rejection = "You can attach at most $MAX_FILES files"
                    break
                }
                val (name, size) = queryFileMeta(uri)
                val ext = name.substringAfterLast('.', "").lowercase()
                if (ext.isBlank() || ext !in ALLOWED_EXTENSIONS) {
                    rejection = "File type .$ext is not supported"
                    continue
                }
                if (size > MAX_FILE_BYTES) {
                    rejection = "$name is larger than 20MB"
                    continue
                }
                if (current.none { it.uri == uri }) {
                    current.add(PendingFile(uri = uri, name = name, sizeBytes = size))
                }
            }
            _uiState.update { it.copy(pendingFiles = current.toList(), snackbar = rejection ?: it.snackbar) }
        }
    }

    fun removeFile(file: PendingFile) {
        _uiState.update { state ->
            state.copy(pendingFiles = state.pendingFiles.filterNot { it.uri == file.uri })
        }
    }

    private fun queryFileMeta(uri: Uri): Pair<String, Long> {
        var name = uri.lastPathSegment?.substringAfterLast('/') ?: "file"
        var size = 0L
        try {
            appContext.contentResolver.query(uri, null, null, null, null)?.use { cursor ->
                if (cursor.moveToFirst()) {
                    val nameIdx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                    if (nameIdx >= 0) cursor.getString(nameIdx)?.let { name = it }
                    val sizeIdx = cursor.getColumnIndex(OpenableColumns.SIZE)
                    if (sizeIdx >= 0 && !cursor.isNull(sizeIdx)) size = cursor.getLong(sizeIdx)
                }
            }
        } catch (_: Exception) {
            // best-effort metadata; validation falls back to extension check
        }
        return name to size
    }

    private fun readBase64(uri: Uri): String {
        val bytes = appContext.contentResolver.openInputStream(uri)?.use { it.readBytes() }
            ?: throw IllegalStateException("Could not read file")
        return Base64.encodeToString(bytes, Base64.NO_WRAP)
    }

    // ------------------------------------------------------------------
    // Sending + streaming
    // ------------------------------------------------------------------

    fun send(content: String) {
        val trimmed = content.trim()
        val files = _uiState.value.pendingFiles
        if ((trimmed.isBlank() && files.isEmpty()) || _uiState.value.isStreaming) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(snackbar = "Sign in to use Neby AI") }
                return@launch
            }

            var resolvedSession = _uiState.value.selectedSession
            try {
                val needsQwen = files.isNotEmpty()
                if (resolvedSession == null || (needsQwen && resolvedSession.provider != "qwen")) {
                    resolvedSession = autoCreateSession(token, needsQwen) ?: return@launch
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(snackbar = friendlyError(e, "Could not start chat")) }
                return@launch
            }
            val session = resolvedSession ?: return@launch

            val now = System.currentTimeMillis()
            val userLocalId = "local-user-$now"
            val assistantLocalId = "local-assistant-$now"
            val userMessage = ApiArenaMessage(
                id = userLocalId,
                role = "user",
                content = if (trimmed.isBlank() && files.isNotEmpty()) {
                    files.joinToString(", ") { it.name }
                } else trimmed,
                createdAt = now
            )
            val assistantMessage = ApiArenaMessage(
                id = assistantLocalId,
                role = "assistant",
                content = "",
                createdAt = now
            )
            _uiState.update {
                it.copy(
                    messages = it.messages + userMessage + assistantMessage,
                    pendingFiles = emptyList(),
                    isStreaming = true,
                    snackbar = null
                )
            }

            val result = StreamResult()
            try {
                withContext(Dispatchers.IO) {
                    val body: ResponseBody = if (files.isNotEmpty()) {
                        val apiFiles = files.map { ApiQwenFile(name = it.name, data = readBase64(it.uri)) }
                        apiService.sendQwenMessageWithFiles(
                            token, session.id, ApiQwenSendMessageRequest(content = trimmed, files = apiFiles)
                        )
                    } else if (session.provider == "qwen") {
                        apiService.sendQwenArenaMessage(token, session.id, ApiArenaSendMessageRequest(trimmed))
                    } else {
                        apiService.sendArenaMessage(token, session.id, ApiArenaSendMessageRequest(trimmed))
                    }
                    consumeSse(body, assistantLocalId, result)
                }
                finishStream(token, session, assistantLocalId, userLocalId, trimmed, result)
            } catch (e: Exception) {
                val message = friendlyError(e, "AI response failed")
                setAssistantContentIfBlank(assistantLocalId, message)
                _uiState.update { it.copy(isStreaming = false, snackbar = message) }
            }
        }
    }

    /** Regenerates the last assistant reply, re-streaming into the same bubble. */
    fun regenerate() {
        val state = _uiState.value
        if (state.isStreaming) return
        val session = state.selectedSession ?: return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch

            // If the last assistant message only has a local id, sync with the
            // server first so we have a real message id to regenerate.
            var last = _uiState.value.messages.lastOrNull { it.role == "assistant" } ?: return@launch
            if (last.id.startsWith("local-")) {
                try {
                    val detail = apiService.getArenaSessionDetail(token, session.id)
                    _uiState.update { it.copy(selectedSession = detail.session, messages = detail.messages) }
                    last = detail.messages.lastOrNull { it.role == "assistant" } ?: return@launch
                } catch (e: Exception) {
                    _uiState.update { it.copy(snackbar = friendlyError(e, "Could not regenerate")) }
                    return@launch
                }
            }

            val targetId = last.id
            setAssistantContent(targetId, "")
            _uiState.update { it.copy(isStreaming = true, snackbar = null) }
            val result = StreamResult()
            try {
                withContext(Dispatchers.IO) {
                    consumeSse(apiService.regenerateArenaMessage(token, targetId), targetId, result)
                }
                // Qwen deltas may not stream — recover content from the server.
                if (!result.errored && currentMessageContent(targetId).isBlank()) {
                    recoverFromServer(token, session.id)
                }
                _uiState.update { it.copy(isStreaming = false) }
            } catch (e: Exception) {
                val message = friendlyError(e, "Could not regenerate")
                setAssistantContentIfBlank(targetId, message)
                _uiState.update { it.copy(isStreaming = false, snackbar = message) }
            }
        }
    }

    fun clearSnackbar() {
        _uiState.update { it.copy(snackbar = null) }
    }

    // ------------------------------------------------------------------
    // Internals
    // ------------------------------------------------------------------

    /**
     * Auto-creates a session before sending. When [preferQwen] is true (the
     * user attached files) a Qwen session is created with a file-aware model,
     * mirroring web behavior.
     */
    private suspend fun autoCreateSession(token: String, preferQwen: Boolean): ApiArenaSession? {
        val state = _uiState.value
        val request: ApiArenaCreateSessionRequest
        val useQwen: Boolean
        if (preferQwen) {
            val qwenModel = state.qwenModels.firstOrNull { it.id == DEFAULT_QWEN_MODEL_ID }
                ?: state.qwenModels.firstOrNull()
            if (qwenModel == null) {
                _uiState.update { it.copy(snackbar = "File chat is unavailable right now (no Qwen models)") }
                return null
            }
            request = ApiArenaCreateSessionRequest(modelId = qwenModel.id, title = DEFAULT_TITLE)
            useQwen = true
        } else {
            val source = state.selectedSource
            val models = state.visibleModels.ifEmpty { state.arenaModels.ifEmpty { state.qwenModels } }
            val model = models.firstOrNull { it.id == state.selectedModelId } ?: models.firstOrNull()
            if (model == null) {
                _uiState.update { it.copy(snackbar = "No AI models are currently available") }
                return null
            }
            request = ApiArenaCreateSessionRequest(modelId = model.id, title = DEFAULT_TITLE)
            useQwen = source == ModelSource.QWEN && state.qwenModels.any { it.id == model.id }
        }
        val response = if (useQwen) {
            apiService.createQwenArenaSession(token, request)
        } else {
            apiService.createArenaSession(token, request)
        }
        _uiState.update {
            it.copy(
                sessions = listOf(response.session) + it.sessions,
                selectedSession = response.session,
                messages = emptyList()
            )
        }
        return response.session
    }

    /** Reads the SSE body line by line, appending deltas to [assistantId]. */
    private fun consumeSse(body: ResponseBody, assistantId: String, result: StreamResult) {
        body.byteStream().bufferedReader().useLines { lines ->
            for (line in lines) {
                if (!handleSseLine(line, assistantId, result)) break
            }
        }
    }

    /** Returns false when the stream is done. */
    private fun handleSseLine(line: String, assistantId: String, result: StreamResult): Boolean {
        if (!line.startsWith("data:")) return true
        val payload = line.removePrefix("data:").trim()
        if (payload.isEmpty()) return true
        if (payload == "[DONE]") return false
        try {
            val root = json.parseToJsonElement(payload).jsonObject
            val error = root["error"]
            if (error != null) {
                val message = try {
                    error.jsonObject["message"]?.jsonPrimitive?.contentOrNull
                } catch (_: Exception) {
                    null
                } ?: "Neby hit an error. Please try again."
                result.errored = true
                setAssistantContentIfBlank(assistantId, message)
                _uiState.update { it.copy(snackbar = message) }
                return true
            }
            val delta = root["choices"]?.jsonArray
                ?.firstOrNull()
                ?.jsonObject
                ?.get("delta")
                ?.jsonObject
                ?: return true
            delta["messageId"]?.jsonPrimitive?.contentOrNull?.let { result.assistantServerId = it }
            delta["userMessageId"]?.jsonPrimitive?.contentOrNull?.let { result.userServerId = it }
            delta["content"]?.jsonPrimitive?.contentOrNull?.takeIf { it.isNotEmpty() }?.let {
                appendAssistantChunk(assistantId, it)
            }
        } catch (_: Exception) {
            // ignore malformed lines defensively
        }
        return true
    }

    /** Post-stream bookkeeping: id swap, Qwen content recovery, auto-title. */
    private suspend fun finishStream(
        token: String,
        session: ApiArenaSession,
        assistantLocalId: String,
        userLocalId: String,
        userText: String,
        result: StreamResult
    ) {
        var assistantId = assistantLocalId
        result.assistantServerId?.let { serverId ->
            replaceMessageId(assistantLocalId, serverId)
            assistantId = serverId
        }
        result.userServerId?.let { replaceMessageId(userLocalId, it) }

        // Qwen deltas may not stream — recover content from the session detail.
        if (!result.errored && currentMessageContent(assistantId).isBlank()) {
            recoverFromServer(token, session.id)
        }

        // Bump local session ordering metadata.
        val now = System.currentTimeMillis()
        _uiState.update { state ->
            state.copy(
                isStreaming = false,
                sessions = state.sessions.map {
                    if (it.id == session.id) {
                        it.copy(lastMessageAt = now, messageCount = it.messageCount + 2)
                    } else it
                }
            )
        }

        // Auto-title: after the first user message, name the chat.
        val currentTitle = _uiState.value.sessions.firstOrNull { it.id == session.id }?.title
            ?: session.title
        if ((currentTitle.isBlank() || currentTitle == DEFAULT_TITLE) && userText.isNotBlank()) {
            val newTitle = userText.take(40)
            runCatching {
                apiService.updateArenaSession(token, session.id, ApiArenaUpdateSessionRequest(title = newTitle))
            }.onSuccess {
                _uiState.update { state ->
                    state.copy(
                        sessions = state.sessions.map {
                            if (it.id == session.id) it.copy(title = newTitle) else it
                        },
                        selectedSession = state.selectedSession?.let {
                            if (it.id == session.id) it.copy(title = newTitle) else it
                        }
                    )
                }
            }
        }
    }

    /** Re-fetches the session detail and adopts the server's message list. */
    private suspend fun recoverFromServer(token: String, sessionId: String) {
        runCatching {
            val detail = apiService.getArenaSessionDetail(token, sessionId)
            if (detail.messages.isNotEmpty()) {
                _uiState.update {
                    if (it.selectedSession?.id == sessionId) {
                        it.copy(selectedSession = detail.session, messages = detail.messages)
                    } else it
                }
            }
        }
    }

    private fun currentMessageContent(messageId: String): String =
        _uiState.value.messages.firstOrNull { it.id == messageId }?.content.orEmpty()

    private fun appendAssistantChunk(messageId: String, chunk: String) {
        _uiState.update { state ->
            state.copy(
                messages = state.messages.map {
                    if (it.id == messageId) it.copy(content = it.content + chunk) else it
                }
            )
        }
    }

    private fun setAssistantContent(messageId: String, content: String) {
        _uiState.update { state ->
            state.copy(
                messages = state.messages.map {
                    if (it.id == messageId) it.copy(content = content) else it
                }
            )
        }
    }

    private fun setAssistantContentIfBlank(messageId: String, content: String) {
        _uiState.update { state ->
            state.copy(
                messages = state.messages.map {
                    if (it.id == messageId && it.content.isBlank()) it.copy(content = content) else it
                }
            )
        }
    }

    private fun replaceMessageId(oldId: String, newId: String) {
        if (oldId == newId) return
        _uiState.update { state ->
            state.copy(
                messages = state.messages.map {
                    if (it.id == oldId) it.copy(id = newId) else it
                }
            )
        }
    }

    private fun friendlyError(e: Exception, fallback: String): String = when {
        e is HttpException && e.code() == 503 -> POOL_EXHAUSTED_MESSAGE
        e is HttpException && e.code() == 429 -> "You're sending messages too fast — slow down a little."
        else -> e.localizedMessage?.takeIf { it.isNotBlank() } ?: fallback
    }
}
