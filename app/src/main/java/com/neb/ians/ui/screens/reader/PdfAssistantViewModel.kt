package com.neb.ians.ui.screens.reader

import android.app.Application
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.PdfAssistantHistoryItem
import com.neb.ians.data.api.PdfAssistantRequest
import com.neb.ians.data.repository.SecurePrefs
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.util.UUID
import javax.inject.Inject

@Serializable
data class PdfAiMessage(
    val id: String,
    val role: String,
    val content: String,
    val createdAt: Long
)

@Serializable
data class PdfAiSession(
    val id: String,
    val title: String,
    val messages: List<PdfAiMessage>,
    val updatedAt: Long
)

data class PdfAssistantUiState(
    val prompt: String = "",
    val sessions: List<PdfAiSession> = emptyList(),
    val currentSessionId: String = "",
    val messages: List<PdfAiMessage> = emptyList(),
    val isPromptOpen: Boolean = false,
    val isPanelOpen: Boolean = false,
    val isMinimized: Boolean = false,
    val isFullscreen: Boolean = false,
    val showHistory: Boolean = false,
    val isThinking: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class PdfAssistantViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val application: Application,
    private val apiService: ApiService
) : ViewModel() {
    private val resourceId: String = savedStateHandle.get<String>("resourceId").orEmpty()
    private val json = Json { ignoreUnknownKeys = true }
    private val prefs = application.getSharedPreferences("pdf_ai_history", 0)
    private val storageKey = "sessions_$resourceId"
    private val _uiState = MutableStateFlow(initialState())
    val uiState: StateFlow<PdfAssistantUiState> = _uiState.asStateFlow()

    fun openPrompt() {
        _uiState.update { it.copy(isPromptOpen = true, isPanelOpen = true, isMinimized = false) }
    }

    fun togglePanel() {
        _uiState.update { it.copy(isPanelOpen = !it.isPanelOpen, isMinimized = false) }
    }

    fun collapseToFab() {
        _uiState.update {
            it.copy(
                isPromptOpen = false,
                isPanelOpen = false,
                isMinimized = false,
                isFullscreen = false,
                showHistory = false
            )
        }
    }

    fun onPromptChange(value: String) {
        _uiState.update { it.copy(prompt = value.take(4000)) }
    }

    fun toggleHistory() {
        _uiState.update { it.copy(showHistory = !it.showHistory) }
    }

    fun toggleFullscreen() {
        _uiState.update { it.copy(isFullscreen = !it.isFullscreen, isMinimized = false) }
    }

    fun minimize() {
        _uiState.update { it.copy(isMinimized = true, isFullscreen = false, showHistory = false) }
    }

    fun expandPanel() {
        _uiState.update { it.copy(isPanelOpen = true, isMinimized = false) }
    }

    fun newChat() {
        val session = emptySession()
        val sessions = listOf(session) + _uiState.value.sessions
        _uiState.update {
            it.copy(
                sessions = sessions,
                currentSessionId = session.id,
                messages = emptyList(),
                isPanelOpen = true,
                isMinimized = false,
                showHistory = false,
                error = null
            )
        }
        persist(sessions)
    }

    fun selectSession(sessionId: String) {
        val session = _uiState.value.sessions.firstOrNull { it.id == sessionId } ?: return
        _uiState.update {
            it.copy(
                currentSessionId = session.id,
                messages = session.messages,
                isPanelOpen = true,
                isMinimized = false,
                showHistory = false,
                error = null
            )
        }
    }

    fun send() {
        val prompt = _uiState.value.prompt.trim()
        if (prompt.isBlank() || _uiState.value.isThinking) return
        val priorMessages = _uiState.value.messages
        val userMessage = PdfAiMessage(
            id = UUID.randomUUID().toString(),
            role = "user",
            content = prompt,
            createdAt = System.currentTimeMillis()
        )
        val pendingMessages = priorMessages + userMessage
        updateCurrentSession(pendingMessages)
        _uiState.update {
            it.copy(
                prompt = "",
                messages = pendingMessages,
                isPromptOpen = true,
                isPanelOpen = true,
                isMinimized = false,
                isThinking = true,
                error = null
            )
        }

        viewModelScope.launch {
            val token = SecurePrefs.getAuthToken(application)?.takeIf { it.isNotBlank() }
            if (token == null) {
                _uiState.update { it.copy(isThinking = false, error = "Please sign in to use PDF AI") }
                return@launch
            }
            runCatching {
                apiService.askPdfAssistant(
                    bearerToken = "Bearer $token",
                    resourceId = resourceId,
                    request = PdfAssistantRequest(
                        prompt = prompt,
                        history = priorMessages.takeLast(8).map {
                            PdfAssistantHistoryItem(role = it.role, content = it.content)
                        }
                    )
                )
            }.onSuccess { response ->
                val answer = response.answer.ifBlank { response.error.orEmpty() }
                if (answer.isBlank()) {
                    _uiState.update { it.copy(isThinking = false, error = "AI returned an empty answer") }
                } else {
                    val assistantMessage = PdfAiMessage(
                        id = UUID.randomUUID().toString(),
                        role = "assistant",
                        content = answer,
                        createdAt = System.currentTimeMillis()
                    )
                    val completed = pendingMessages + assistantMessage
                    updateCurrentSession(completed)
                    _uiState.update { it.copy(messages = completed, isThinking = false, error = null) }
                }
            }.onFailure { error ->
                val errorMsg = if (error is retrofit2.HttpException && error.code() == 402) {
                    "Neby Credits exhausted. You get 10 free credits every month, or convert 2 NEBians points to 1 credit or contact developer on WhatsApp (+977 9765324034)."
                } else {
                    error.message ?: "PDF AI is unavailable"
                }
                _uiState.update {
                    it.copy(isThinking = false, error = errorMsg)
                }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }

    private fun initialState(): PdfAssistantUiState {
        val sessions = runCatching {
            val raw = prefs.getString(storageKey, null).orEmpty()
            if (raw.isBlank()) emptyList() else json.decodeFromString<List<PdfAiSession>>(raw)
        }.getOrDefault(emptyList()).sortedByDescending { it.updatedAt }
        val current = sessions.firstOrNull() ?: emptySession()
        val all = if (sessions.isEmpty()) listOf(current) else sessions
        return PdfAssistantUiState(
            sessions = all,
            currentSessionId = current.id,
            messages = current.messages
        )
    }

    private fun emptySession(): PdfAiSession = PdfAiSession(
        id = UUID.randomUUID().toString(),
        title = "PDF chat",
        messages = emptyList(),
        updatedAt = System.currentTimeMillis()
    )

    private fun updateCurrentSession(messages: List<PdfAiMessage>) {
        val state = _uiState.value
        val current = state.sessions.firstOrNull { it.id == state.currentSessionId } ?: emptySession()
        val title = messages.firstOrNull { it.role == "user" }?.content?.trim()?.take(42)?.ifBlank { "PDF chat" } ?: current.title
        val updated = current.copy(title = title, messages = messages, updatedAt = System.currentTimeMillis())
        val sessions = (state.sessions.filterNot { it.id == current.id } + updated).sortedByDescending { it.updatedAt }
        _uiState.update { it.copy(sessions = sessions, currentSessionId = updated.id, messages = messages) }
        persist(sessions)
    }

    private fun persist(sessions: List<PdfAiSession>) {
        prefs.edit().putString(storageKey, json.encodeToString(sessions.take(20))).apply()
    }
}
