package com.neb.ians.ui.screens.ai

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.R
import com.neb.ians.data.api.ApiArenaCreateSessionRequest
import com.neb.ians.data.api.ApiArenaMessage
import com.neb.ians.data.api.ApiArenaModel
import com.neb.ians.data.api.ApiArenaSendMessageRequest
import com.neb.ians.data.api.ApiArenaSession
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPrimaryButton
import com.neb.ians.ui.components.WebTopBar
import dagger.hilt.android.lifecycle.HiltViewModel
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
import javax.inject.Inject

data class NebyAiUiState(
    val models: List<ApiArenaModel> = emptyList(),
    val sessions: List<ApiArenaSession> = emptyList(),
    val selectedSession: ApiArenaSession? = null,
    val messages: List<ApiArenaMessage> = emptyList(),
    val isLoading: Boolean = true,
    val isStreaming: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class NebyAiViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val json = Json { ignoreUnknownKeys = true }
    private val _uiState = MutableStateFlow(NebyAiUiState())
    val uiState: StateFlow<NebyAiUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to use Neby AI") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val models = apiService.getArenaModels(token).models.filter { it.active && it.id.isNotBlank() }
                val sessions = apiService.getArenaSessions(token).sessions
                _uiState.update { it.copy(models = models, sessions = sessions, isLoading = false) }
                sessions.firstOrNull()?.let { openSession(it.id) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load Neby AI") }
            }
        }
    }

    fun createSession() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            val model = _uiState.value.models.firstOrNull()
            if (model == null) {
                _uiState.update { it.copy(error = "No AI models are currently available") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val response = apiService.createArenaSession(
                    token,
                    ApiArenaCreateSessionRequest(modelId = model.id, title = "Neby chat")
                )
                val sessions = listOf(response.session) + _uiState.value.sessions
                _uiState.update { it.copy(sessions = sessions, selectedSession = response.session, messages = emptyList(), isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Could not create chat") }
            }
        }
    }

    fun openSession(sessionId: String) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                val detail = apiService.getArenaSessionDetail(token, sessionId)
                _uiState.update { it.copy(selectedSession = detail.session, messages = detail.messages, error = null) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.localizedMessage ?: "Could not open chat") }
            }
        }
    }

    fun send(content: String) {
        val trimmed = content.trim()
        if (trimmed.isBlank() || _uiState.value.isStreaming) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            var session = _uiState.value.selectedSession
            if (session == null) {
                val model = _uiState.value.models.firstOrNull() ?: return@launch
                session = apiService.createArenaSession(
                    token,
                    ApiArenaCreateSessionRequest(modelId = model.id, title = trimmed.take(40))
                ).session
                _uiState.update { it.copy(selectedSession = session, sessions = listOf(session) + it.sessions) }
            }

            val userMessage = ApiArenaMessage(
                id = "local-user-${System.currentTimeMillis()}",
                role = "user",
                content = trimmed,
                createdAt = System.currentTimeMillis()
            )
            val assistantId = "local-assistant-${System.currentTimeMillis()}"
            val assistantMessage = ApiArenaMessage(
                id = assistantId,
                role = "assistant",
                content = "",
                createdAt = System.currentTimeMillis()
            )
            _uiState.update { it.copy(messages = it.messages + userMessage + assistantMessage, isStreaming = true, error = null) }

            try {
                withContext(Dispatchers.IO) {
                    apiService.sendArenaMessage(token, session.id, ApiArenaSendMessageRequest(trimmed))
                        .byteStream()
                        .bufferedReader()
                        .useLines { lines ->
                            lines.forEach { line ->
                                val chunk = extractContent(line)
                                if (chunk.isNotEmpty()) appendAssistantChunk(assistantId, chunk)
                            }
                        }
                }
                _uiState.update { it.copy(isStreaming = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isStreaming = false, error = e.localizedMessage ?: "AI response failed") }
            }
        }
    }

    private fun appendAssistantChunk(messageId: String, chunk: String) {
        _uiState.update { state ->
            state.copy(
                messages = state.messages.map {
                    if (it.id == messageId) it.copy(content = it.content + chunk) else it
                }
            )
        }
    }

    private fun extractContent(line: String): String {
        if (!line.startsWith("data:")) return ""
        val payload = line.removePrefix("data:").trim()
        if (payload == "[DONE]" || payload.isBlank()) return ""
        return try {
            val root = json.parseToJsonElement(payload).jsonObject
            root["choices"]?.jsonArray
                ?.firstOrNull()
                ?.jsonObject
                ?.get("delta")
                ?.jsonObject
                ?.get("content")
                ?.jsonPrimitive
                ?.contentOrNull
                ?: ""
        } catch (_: Exception) {
            ""
        }
    }
}

@Composable
fun NebyAiScreen(
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: NebyAiViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var input by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Neby AI",
                subtitle = uiState.selectedSession?.modelName ?: "AI study chat",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface,
        bottomBar = {
            ChatInput(
                value = input,
                enabled = !uiState.isStreaming,
                onValueChange = { input = it },
                onSend = {
                    val message = input
                    input = ""
                    viewModel.send(message)
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                uiState.isLoading -> {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) { CircularProgressIndicator() }
                }
                uiState.error != null && uiState.messages.isEmpty() -> {
                    WebEmptyState(
                        title = "Neby AI unavailable",
                        message = uiState.error ?: "Try again later.",
                        icon = painterResource(id = R.drawable.ic_science),
                        modifier = Modifier.padding(16.dp)
                    )
                }
                else -> {
                    if (uiState.sessions.isEmpty()) {
                        Surface(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            shape = WebPanelShape,
                            color = MaterialTheme.colorScheme.surfaceContainerLowest,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                        ) {
                            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                Text("Start a Neby chat", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                Text(
                                    text = "Ask questions in a clean native chat powered by the Arena proxy.",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                WebPrimaryButton(text = "New Chat", onClick = viewModel::createSession)
                            }
                        }
                    }
                    if (uiState.models.isNotEmpty()) {
                        Row(
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            uiState.models.take(2).forEach { model ->
                                WebChip(text = model.name.ifBlank { model.code.ifBlank { "Model" } }, selected = false)
                            }
                        }
                    }
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        items(uiState.messages, key = { it.id }) { message ->
                            ChatBubble(message = message)
                        }
                        if (uiState.isStreaming) {
                            item {
                                Text(
                                    text = "Neby is responding...",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(horizontal = 6.dp)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ChatBubble(message: ApiArenaMessage) {
    val isUser = message.role == "user"
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            modifier = Modifier.fillMaxWidth(if (isUser) 0.84f else 0.92f),
            shape = RoundedCornerShape(
                topStart = 18.dp,
                topEnd = 18.dp,
                bottomStart = if (isUser) 18.dp else 6.dp,
                bottomEnd = if (isUser) 6.dp else 18.dp
            ),
            color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceContainerLowest,
            border = if (isUser) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
        ) {
            Text(
                text = message.content.ifBlank { "..." },
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                style = MaterialTheme.typography.bodyMedium,
                color = if (isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
            )
        }
    }
}

@Composable
private fun ChatInput(
    value: String,
    enabled: Boolean,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit
) {
    Surface(
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 0.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.surface)
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.Bottom,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedTextField(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier
                    .weight(1f)
                    .heightIn(min = 54.dp, max = 140.dp),
                placeholder = { Text("Ask Neby...") },
                enabled = enabled,
                minLines = 1,
                maxLines = 5
            )
            IconButton(
                enabled = value.isNotBlank() && enabled,
                onClick = onSend
            ) {
                Icon(Icons.Filled.Send, contentDescription = "Send")
            }
        }
    }
}
