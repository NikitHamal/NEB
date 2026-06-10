package com.neb.ians.ui.screens.neby

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.History
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ArenaModel
import com.neb.ians.ui.components.NebColors
import com.neb.ians.ui.components.NebTopBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NebyAiScreen(
    onNavigateBack: () -> Unit,
    isDark: Boolean = false,
    onToggleTheme: () -> Unit = {},
    viewModel: NebyAiViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var showModelSheet by remember { mutableStateOf(false) }
    var showHistory by remember { mutableStateOf(false) }
    val listState = rememberLazyListState()

    LaunchedEffect(uiState.messages.size, uiState.messages.lastOrNull()?.content) {
        if (uiState.messages.isNotEmpty()) {
            listState.animateScrollToItem(uiState.messages.lastIndex)
        }
    }

    Scaffold(
        topBar = {
            NebTopBar(
                showBrand = false,
                title = "Neby AI",
                onBack = onNavigateBack,
                isDark = isDark,
                onToggleTheme = onToggleTheme
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(top = padding.calculateTopPadding())
        ) {
            HeaderBar(
                modelName = uiState.selectedModel?.name ?: "Select model",
                onModelClick = { showModelSheet = true },
                onHistory = { showHistory = true },
                onNewChat = viewModel::newChat
            )
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)

            Box(modifier = Modifier.weight(1f)) {
                when {
                    uiState.isLoading && uiState.messages.isEmpty() ->
                        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator()
                        }
                    uiState.messages.isEmpty() -> WelcomeState()
                    else -> LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        items(uiState.messages, key = { it.id }) { msg ->
                            MessageBubble(msg)
                        }
                    }
                }
            }

            InputBar(
                value = uiState.input,
                onValueChange = viewModel::onInputChange,
                onSend = viewModel::send,
                enabled = uiState.selectedModel != null && !uiState.isStreaming
            )
        }
    }

    if (showModelSheet) {
        ModelSheet(
            models = uiState.models,
            selectedId = uiState.selectedModel?.id,
            onSelect = {
                viewModel.selectModel(it)
                showModelSheet = false
            },
            onDismiss = { showModelSheet = false }
        )
    }

    if (showHistory) {
        HistorySheet(
            sessions = uiState.sessions,
            currentId = uiState.currentSessionId,
            onOpen = {
                viewModel.openSession(it)
                showHistory = false
            },
            onDelete = viewModel::deleteSession,
            onDismiss = { showHistory = false }
        )
    }
}

@Composable
private fun HeaderBar(
    modelName: String,
    onModelClick: () -> Unit,
    onHistory: () -> Unit,
    onNewChat: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Surface(
            onClick = onModelClick,
            shape = CircleShape,
            color = MaterialTheme.colorScheme.secondaryContainer,
            modifier = Modifier.weight(1f, fill = false)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Icon(
                    Icons.Filled.AutoAwesome,
                    null,
                    tint = MaterialTheme.colorScheme.onSecondaryContainer,
                    modifier = Modifier.size(18.dp)
                )
                Text(
                    modelName,
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSecondaryContainer,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f, fill = false)
                )
                Icon(
                    Icons.Outlined.ExpandMore,
                    null,
                    tint = MaterialTheme.colorScheme.onSecondaryContainer,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
        Spacer(Modifier.weight(1f))
        IconButton(onClick = onHistory) {
            Icon(Icons.Outlined.History, contentDescription = "Chat history")
        }
        IconButton(onClick = onNewChat) {
            Icon(Icons.Outlined.Add, contentDescription = "New chat")
        }
    }
}

@Composable
private fun WelcomeState() {
    Box(Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(64.dp)
                    .clip(CircleShape)
                    .background(NebColors.brandBrush),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Filled.AutoAwesome,
                    null,
                    tint = androidx.compose.ui.graphics.Color.White,
                    modifier = Modifier.size(30.dp)
                )
            }
            Text("Ask Neby AI", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(
                "Your study assistant. Ask about NEB subjects, get summaries, or work through problems step by step.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
        }
    }
}

@Composable
private fun MessageBubble(msg: NebyChatMessage) {
    val isUser = msg.role == "user"
    val bg = when {
        msg.isError -> MaterialTheme.colorScheme.errorContainer
        isUser -> MaterialTheme.colorScheme.primary
        else -> MaterialTheme.colorScheme.surfaceContainerHigh
    }
    val fg = when {
        msg.isError -> MaterialTheme.colorScheme.onErrorContainer
        isUser -> MaterialTheme.colorScheme.onPrimary
        else -> MaterialTheme.colorScheme.onSurface
    }
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            color = bg,
            shape = RoundedCornerShape(
                topStart = 16.dp,
                topEnd = 16.dp,
                bottomStart = if (isUser) 16.dp else 4.dp,
                bottomEnd = if (isUser) 4.dp else 16.dp
            ),
            modifier = Modifier.widthIn(max = 320.dp)
        ) {
            val display = if (msg.content.isBlank() && msg.isStreaming) "…" else msg.content
            Text(
                display,
                style = MaterialTheme.typography.bodyMedium,
                color = fg,
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp)
            )
        }
    }
}

@Composable
private fun InputBar(
    value: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    enabled: Boolean
) {
    Surface(
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        tonalElevation = 0.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .imePadding()
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedTextField(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier.weight(1f),
                placeholder = { Text("Message Neby AI") },
                shape = RoundedCornerShape(24.dp),
                maxLines = 4
            )
            val canSend = enabled && value.isNotBlank()
            FilledIconButton(
                onClick = onSend,
                enabled = canSend,
                modifier = Modifier.size(48.dp)
            ) {
                Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send")
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ModelSheet(
    models: List<ArenaModel>,
    selectedId: String?,
    onSelect: (ArenaModel) -> Unit,
    onDismiss: () -> Unit
) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Text(
            "Choose a model",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp)
        )
        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 420.dp)) {
            items(models, key = { it.id }) { model ->
                ListItem(
                    headlineContent = { Text(model.name.ifBlank { model.code }) },
                    supportingContent = {
                        if (model.provider.isNotBlank()) Text(model.provider)
                    },
                    leadingContent = {
                        Icon(Icons.Filled.AutoAwesome, null, tint = MaterialTheme.colorScheme.primary)
                    },
                    trailingContent = {
                        if (model.id == selectedId) {
                            RadioButton(selected = true, onClick = { onSelect(model) })
                        }
                    },
                    modifier = Modifier.clickable { onSelect(model) }
                )
            }
        }
        Spacer(Modifier.height(12.dp))
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun HistorySheet(
    sessions: List<com.neb.ians.data.api.ArenaSession>,
    currentId: String?,
    onOpen: (String) -> Unit,
    onDelete: (String) -> Unit,
    onDismiss: () -> Unit
) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Text(
            "Recent chats",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp)
        )
        if (sessions.isEmpty()) {
            Text(
                "No conversations yet.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 20.dp, vertical = 12.dp)
            )
        } else {
            LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 460.dp)) {
                items(sessions, key = { it.id }) { session ->
                    ListItem(
                        headlineContent = {
                            Text(
                                session.title.ifBlank { "New chat" },
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                fontWeight = if (session.id == currentId) FontWeight.SemiBold else FontWeight.Normal
                            )
                        },
                        supportingContent = {
                            Text(session.modelName.ifBlank { session.modelCode }, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        },
                        trailingContent = {
                            IconButton(onClick = { onDelete(session.id) }) {
                                Icon(
                                    Icons.Outlined.Delete,
                                    contentDescription = "Delete chat",
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        },
                        modifier = Modifier.clickable { onOpen(session.id) }
                    )
                }
            }
        }
        Spacer(Modifier.height(12.dp))
    }
}
