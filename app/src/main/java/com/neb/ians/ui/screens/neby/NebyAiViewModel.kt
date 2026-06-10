package com.neb.ians.ui.screens.neby

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ArenaModel
import com.neb.ians.data.api.ArenaSession
import com.neb.ians.data.api.NebyStreamEvent
import com.neb.ians.data.repository.NebyRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class NebyChatMessage(
    val id: String,
    val role: String,
    val content: String,
    val isStreaming: Boolean = false,
    val isError: Boolean = false
)

data class NebyAiUiState(
    val models: List<ArenaModel> = emptyList(),
    val selectedModel: ArenaModel? = null,
    val sessions: List<ArenaSession> = emptyList(),
    val currentSessionId: String? = null,
    val messages: List<NebyChatMessage> = emptyList(),
    val input: String = "",
    val isLoading: Boolean = true,
    val isStreaming: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class NebyAiViewModel @Inject constructor(
    private val repository: NebyRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(NebyAiUiState())
    val uiState: StateFlow<NebyAiUiState> = _uiState.asStateFlow()

    init {
        bootstrap()
    }

    private fun bootstrap() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val models = repository.getModels().getOrElse { emptyList() }
            val sessions = repository.getSessions().getOrElse { emptyList() }
            _uiState.update {
                it.copy(
                    models = models,
                    selectedModel = it.selectedModel ?: models.firstOrNull(),
                    sessions = sessions,
                    isLoading = false,
                    error = if (models.isEmpty()) "Neby AI is unavailable right now." else null
                )
            }
        }
    }

    fun onInputChange(value: String) {
        _uiState.update { it.copy(input = value) }
    }

    fun selectModel(model: ArenaModel) {
        _uiState.update { it.copy(selectedModel = model) }
    }

    fun newChat() {
        _uiState.update { it.copy(currentSessionId = null, messages = emptyList(), input = "") }
    }

    fun openSession(sessionId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, currentSessionId = sessionId) }
            repository.getSession(sessionId)
                .onSuccess { detail ->
                    val msgs = detail.messages.map {
                        NebyChatMessage(
                            id = it.id,
                            role = it.role,
                            content = it.content,
                            isError = it.error != null
                        )
                    }
                    _uiState.update { it.copy(messages = msgs, isLoading = false) }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
        }
    }

    fun deleteSession(sessionId: String) {
        viewModelScope.launch {
            repository.deleteSession(sessionId).onSuccess {
                _uiState.update { state ->
                    val cleared = state.currentSessionId == sessionId
                    state.copy(
                        sessions = state.sessions.filterNot { it.id == sessionId },
                        currentSessionId = if (cleared) null else state.currentSessionId,
                        messages = if (cleared) emptyList() else state.messages
                    )
                }
            }
        }
    }

    fun send() {
        val state = _uiState.value
        val text = state.input.trim()
        if (text.isEmpty() || state.isStreaming) return
        val model = state.selectedModel ?: return

        viewModelScope.launch {
            // Resolve (or create) the session first.
            var sessionId = state.currentSessionId
            if (sessionId == null) {
                val created = repository.createSession(model.id, text.take(60)).getOrElse {
                    _uiState.update { s -> s.copy(error = "Couldn't start a chat. Try again.") }
                    return@launch
                }
                sessionId = created.id
                _uiState.update { s ->
                    s.copy(
                        currentSessionId = created.id,
                        sessions = listOf(created) + s.sessions
                    )
                }
            }

            val userMsg = NebyChatMessage(id = "u-${System.currentTimeMillis()}", role = "user", content = text)
            val assistantId = "a-${System.currentTimeMillis()}"
            _uiState.update { s ->
                s.copy(
                    input = "",
                    isStreaming = true,
                    error = null,
                    messages = s.messages + userMsg + NebyChatMessage(
                        id = assistantId,
                        role = "assistant",
                        content = "",
                        isStreaming = true
                    )
                )
            }

            repository.sendMessage(sessionId, text).collect { event ->
                when (event) {
                    is NebyStreamEvent.Delta -> updateAssistant(assistantId) { it + event.content }
                    is NebyStreamEvent.Failed -> {
                        _uiState.update { s ->
                            s.copy(
                                isStreaming = false,
                                messages = s.messages.map { m ->
                                    if (m.id == assistantId) m.copy(
                                        content = if (m.content.isBlank()) event.message else m.content,
                                        isStreaming = false,
                                        isError = true
                                    ) else m
                                }
                            )
                        }
                    }
                    is NebyStreamEvent.Meta -> Unit
                    NebyStreamEvent.Done -> {
                        _uiState.update { s ->
                            s.copy(
                                isStreaming = false,
                                messages = s.messages.map { m ->
                                    if (m.id == assistantId) m.copy(isStreaming = false) else m
                                }
                            )
                        }
                    }
                }
            }
            // Safety: ensure streaming flag clears even if stream ends without [DONE].
            _uiState.update { s ->
                if (s.isStreaming) s.copy(
                    isStreaming = false,
                    messages = s.messages.map { if (it.id == assistantId) it.copy(isStreaming = false) else it }
                ) else s
            }
        }
    }

    private fun updateAssistant(id: String, transform: (String) -> String) {
        _uiState.update { s ->
            s.copy(messages = s.messages.map { if (it.id == id) it.copy(content = transform(it.content)) else it })
        }
    }
}
