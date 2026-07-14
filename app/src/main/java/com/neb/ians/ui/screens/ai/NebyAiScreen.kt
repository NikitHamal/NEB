package com.neb.ians.ui.screens.ai

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.History
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import android.content.Intent
import android.net.Uri
import coil.compose.AsyncImage
import androidx.compose.material.icons.outlined.PlayCircle
import androidx.compose.material.icons.outlined.Headphones
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiArenaMessage
import com.neb.ians.data.api.ApiArenaModel
import com.neb.ians.data.api.ApiArenaSession
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebIconButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebPrimaryButton
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.util.formatTimeAgo
import kotlinx.coroutines.launch

private val ArenaTint = Color(0xFF2563EB)
private val QwenTint = Color(0xFF7C3AED)

private fun providerLabel(provider: String): String =
    if (provider == "qwen") "Qwen" else "Arena"

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NebyAiScreen(
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: NebyAiViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var input by remember { mutableStateOf("") }
    var showSessions by remember { mutableStateOf(false) }
    var renameTarget by remember { mutableStateOf<ApiArenaSession?>(null) }
    var deleteTarget by remember { mutableStateOf<ApiArenaSession?>(null) }

    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    val listState = rememberLazyListState()
    val clipboard = LocalClipboardManager.current
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    val filePicker = rememberLauncherForActivityResult(
        ActivityResultContracts.GetMultipleContents()
    ) { uris ->
        if (uris.isNotEmpty()) viewModel.addFiles(uris)
    }

    LaunchedEffect(uiState.snackbar) {
        uiState.snackbar?.let {
            snackbarHostState.showSnackbar(it)
            viewModel.clearSnackbar()
        }
    }

    // Scroll to bottom when new messages arrive or streamed content grows.
    val messageCount = uiState.messages.size
    val lastContentLength = uiState.messages.lastOrNull()?.content?.length ?: 0
    LaunchedEffect(messageCount, lastContentLength) {
        val total = listState.layoutInfo.totalItemsCount
        if (total > 0) {
            runCatching { listState.animateScrollToItem(total - 1) }
        }
    }

    val activeSession = uiState.selectedSession

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Neby AI",
                subtitle = activeSession?.let {
                    val model = it.modelName.ifBlank { it.modelCode.ifBlank { "AI model" } }
                    "$model · ${providerLabel(it.provider)}"
                } ?: "AI study chat",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick,
                actions = {
                    WebIconButton(
                        imageVector = Icons.Outlined.History,
                        contentDescription = "Chat history",
                        onClick = { showSessions = true }
                    )
                }
            )
        },
        containerColor = MaterialTheme.colorScheme.surface,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        bottomBar = {
            if (uiState.error == null) {
                ChatInput(
                    value = input,
                    pendingFiles = uiState.pendingFiles,
                    sending = uiState.isStreaming,
                    showAttach = true,
                    onValueChange = { input = it },
                    onAttach = { filePicker.launch("*/*") },
                    onRemoveFile = viewModel::removeFile,
                    onClearFiles = viewModel::clearPendingFiles,
                    onSend = {
                        val message = input
                        input = ""
                        viewModel.send(message)
                    }
                )
            }
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
                uiState.error != null -> {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        WebEmptyState(
                            title = "Neby AI unavailable",
                            message = uiState.error ?: "Try again later.",
                            icon = painterResource(id = R.drawable.ic_science),
                            modifier = Modifier.padding(16.dp)
                        )
                        WebPrimaryButton(text = "Retry", onClick = viewModel::load)
                    }
                }
                activeSession == null -> {
                    ModelPickerPanel(
                        source = uiState.selectedSource,
                        models = uiState.visibleModels,
                        selectedModelId = uiState.selectedModelId,
                        isCreating = uiState.isCreatingSession,
                        onSourceChange = viewModel::selectSource,
                        onModelSelect = viewModel::selectModel,
                        onStartChat = viewModel::startChat
                    )
                }
                else -> {
                    LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        if (uiState.messages.isEmpty() && !uiState.isStreaming) {
                            item(key = "empty-hint") {
                                Text(
                                    text = "Ask Neby anything about your studies. " +
                                        if (activeSession.provider == "qwen")
                                            "You can also attach files with the paperclip."
                                        else "",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(6.dp)
                                )
                            }
                        }
                        items(uiState.messages, key = { it.id }) { message ->
                            ChatBubble(
                                message = message,
                                onCopy = { text ->
                                    clipboard.setText(AnnotatedString(text))
                                    scope.launch { snackbarHostState.showSnackbar("Copied to clipboard") }
                                }
                            )
                        }
                        if (uiState.isStreaming) {
                            item(key = "typing-indicator") {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    modifier = Modifier.padding(horizontal = 6.dp)
                                ) {
                                    CircularProgressIndicator(
                                        modifier = Modifier.size(14.dp),
                                        strokeWidth = 2.dp
                                    )
                                    Text(
                                        text = "Neby is responding…",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        } else {
                            val lastMessage = uiState.messages.lastOrNull()
                            if (lastMessage != null && lastMessage.role == "assistant" && lastMessage.content.isNotBlank()) {
                                item(key = "regenerate-pill") {
                                    RegeneratePill(onClick = viewModel::regenerate)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (showSessions) {
        ModalBottomSheet(
            onDismissRequest = { showSessions = false },
            sheetState = sheetState
        ) {
            SessionsSheetContent(
                sessions = uiState.sessions,
                activeSessionId = activeSession?.id,
                onNewChat = {
                    viewModel.startNewChat()
                    showSessions = false
                },
                onOpen = {
                    viewModel.openSession(it.id)
                    showSessions = false
                },
                onRename = { renameTarget = it },
                onDelete = { deleteTarget = it }
            )
        }
    }

    renameTarget?.let { target ->
        var titleText by remember(target.id) { mutableStateOf(target.title) }
        AlertDialog(
            onDismissRequest = { renameTarget = null },
            title = { Text("Rename chat") },
            text = {
                OutlinedTextField(
                    value = titleText,
                    onValueChange = { titleText = it },
                    singleLine = true,
                    label = { Text("Title") }
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.renameSession(target.id, titleText)
                        renameTarget = null
                    }
                ) { Text("Save") }
            },
            dismissButton = {
                TextButton(onClick = { renameTarget = null }) { Text("Cancel") }
            }
        )
    }

    deleteTarget?.let { target ->
        AlertDialog(
            onDismissRequest = { deleteTarget = null },
            title = { Text("Delete chat?") },
            text = { Text("\"${target.title}\" and all its messages will be permanently deleted.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.deleteSession(target.id)
                        deleteTarget = null
                    }
                ) { Text("Delete", color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = {
                TextButton(onClick = { deleteTarget = null }) { Text("Cancel") }
            }
        )
    }
}

// ----------------------------------------------------------------------
// Sessions sheet
// ----------------------------------------------------------------------

@Composable
private fun SessionsSheetContent(
    sessions: List<ApiArenaSession>,
    activeSessionId: String?,
    onNewChat: () -> Unit,
    onOpen: (ApiArenaSession) -> Unit,
    onRename: (ApiArenaSession) -> Unit,
    onDelete: (ApiArenaSession) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .padding(bottom = 24.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Chats",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.weight(1f)
            )
            WebPrimaryButton(text = "New chat", onClick = onNewChat)
        }
        Spacer(modifier = Modifier.heightIn(min = 12.dp))
        if (sessions.isEmpty()) {
            Text(
                text = "No chats yet. Start one to talk to Neby.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(vertical = 18.dp)
            )
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(max = 480.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(top = 12.dp)
            ) {
                items(sessions, key = { it.id }) { session ->
                    SessionRow(
                        session = session,
                        isActive = session.id == activeSessionId,
                        onOpen = { onOpen(session) },
                        onRename = { onRename(session) },
                        onDelete = { onDelete(session) }
                    )
                }
            }
        }
    }
}

@Composable
private fun SessionRow(
    session: ApiArenaSession,
    isActive: Boolean,
    onOpen: () -> Unit,
    onRename: () -> Unit,
    onDelete: () -> Unit
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebPanelShape)
            .clickable(onClick = onOpen),
        shape = WebPanelShape,
        color = if (isActive) MaterialTheme.colorScheme.secondaryContainer
        else MaterialTheme.colorScheme.surfaceContainerLowest,
        border = if (isActive) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(start = 14.dp, end = 4.dp, top = 10.dp, bottom = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = session.title.ifBlank { "New chat" },
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.heightIn(min = 4.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    ProviderChip(provider = session.provider)
                    Text(
                        text = session.modelName.ifBlank { session.modelCode.ifBlank { "Model" } },
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false)
                    )
                    if (session.lastMessageAt > 0) {
                        Text(
                            text = formatTimeAgo(session.lastMessageAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                }
            }
            IconButton(onClick = onRename) {
                Icon(
                    imageVector = Icons.Outlined.Edit,
                    contentDescription = "Rename chat",
                    modifier = Modifier.size(18.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            IconButton(onClick = onDelete) {
                Icon(
                    imageVector = Icons.Outlined.Delete,
                    contentDescription = "Delete chat",
                    modifier = Modifier.size(18.dp),
                    tint = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

@Composable
private fun ProviderChip(provider: String) {
    val isQwen = provider == "qwen"
    val tint = if (isQwen) QwenTint else ArenaTint
    Box(
        modifier = Modifier
            .clip(WebPillShape)
            .background(tint.copy(alpha = 0.12f))
            .padding(horizontal = 8.dp, vertical = 2.dp)
    ) {
        Text(
            text = providerLabel(provider),
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.SemiBold,
            color = tint
        )
    }
}

// ----------------------------------------------------------------------
// Model picker
// ----------------------------------------------------------------------

@Composable
private fun ModelPickerPanel(
    source: ModelSource,
    models: List<ApiArenaModel>,
    selectedModelId: String?,
    isCreating: Boolean,
    onSourceChange: (ModelSource) -> Unit,
    onModelSelect: (String) -> Unit,
    onStartChat: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Start a new chat",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "Pick a model. Qwen models can read files you attach.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(top = 2.dp, bottom = 12.dp)
        )
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            SourceTab(
                text = "Arena models",
                selected = source == ModelSource.ARENA,
                tint = ArenaTint,
                onClick = { onSourceChange(ModelSource.ARENA) }
            )
            SourceTab(
                text = "Qwen models",
                selected = source == ModelSource.QWEN,
                tint = QwenTint,
                onClick = { onSourceChange(ModelSource.QWEN) }
            )
        }
        Spacer(modifier = Modifier.heightIn(min = 12.dp))
        if (models.isEmpty()) {
            Text(
                text = "No models available in this catalogue right now.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(vertical = 20.dp)
            )
        } else {
            LazyColumn(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(vertical = 4.dp)
            ) {
                items(models, key = { it.id }) { model ->
                    ModelRow(
                        model = model,
                        selected = model.id == selectedModelId,
                        onClick = { onModelSelect(model.id) }
                    )
                }
            }
        }
        Spacer(modifier = Modifier.heightIn(min = 12.dp))
        if (isCreating) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                Text(
                    text = "Starting chat…",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            WebPrimaryButton(
                text = "Start chat",
                onClick = onStartChat,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
private fun SourceTab(
    text: String,
    selected: Boolean,
    tint: Color,
    onClick: () -> Unit
) {
    val background = if (selected) tint.copy(alpha = 0.14f) else Color.Transparent
    val borderColor = if (selected) tint else MaterialTheme.colorScheme.outline
    val contentColor = if (selected) tint else MaterialTheme.colorScheme.onSurfaceVariant
    Box(
        modifier = Modifier
            .clip(WebPillShape)
            .background(background)
            .border(1.dp, borderColor, WebPillShape)
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
            color = contentColor
        )
    }
}

@Composable
private fun ModelRow(
    model: ApiArenaModel,
    selected: Boolean,
    onClick: () -> Unit
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebPanelShape)
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        color = if (selected) MaterialTheme.colorScheme.secondaryContainer
        else MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(
            1.dp,
            if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant
        )
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            RadioButton(selected = selected, onClick = onClick)
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = model.name.ifBlank { model.code.ifBlank { "Model" } },
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                if (model.provider.isNotBlank()) {
                    Text(
                        text = model.provider,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
            if (model.thinking) {
                Row(
                    modifier = Modifier
                        .clip(WebPillShape)
                        .background(MaterialTheme.colorScheme.tertiaryContainer)
                        .padding(horizontal = 8.dp, vertical = 3.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(3.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Psychology,
                        contentDescription = null,
                        modifier = Modifier.size(13.dp),
                        tint = MaterialTheme.colorScheme.onTertiaryContainer
                    )
                    Text(
                        text = "Thinking",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onTertiaryContainer
                    )
                }
            }
        }
    }
}

// ----------------------------------------------------------------------
// Chat bubbles
// ----------------------------------------------------------------------

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun ChatBubble(
    message: ApiArenaMessage,
    onCopy: (String) -> Unit
) {
    val isUser = message.role == "user"
    val shape = RoundedCornerShape(
        topStart = 18.dp,
        topEnd = 18.dp,
        bottomStart = if (isUser) 18.dp else 6.dp,
        bottomEnd = if (isUser) 6.dp else 18.dp
    )
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            modifier = Modifier
                .fillMaxWidth(if (isUser) 0.84f else 0.92f)
                .clip(shape)
                .then(
                    if (!isUser && message.content.isNotBlank()) {
                        Modifier.combinedClickable(
                            onClick = {},
                            onLongClick = { onCopy(message.content) }
                        )
                    } else Modifier
                ),
            shape = shape,
            color = if (isUser) MaterialTheme.colorScheme.primaryContainer
            else MaterialTheme.colorScheme.surfaceContainerLowest,
            border = if (isUser) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
        ) {
            Column(modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp)) {
                if (message.attachments.isNotEmpty()) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                            .padding(bottom = 6.dp),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        message.attachments.forEach { attachment ->
                            AttachmentChip(fileName = attachment.fileName.ifBlank { "Attachment" })
                        }
                    }
                }
                if (isUser) {
                    Text(
                        text = message.content.ifBlank { "…" },
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                } else if (message.content.isBlank()) {
                    Text(
                        text = "…",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    MarkdownText(
                        markdown = message.content,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                }
            }
        }
    }
}

@Composable
private fun AttachmentChip(fileName: String) {
    Row(
        modifier = Modifier
            .clip(WebPillShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(horizontal = 10.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = Icons.Outlined.Description,
            contentDescription = null,
            modifier = Modifier.size(14.dp),
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = fileName,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
private fun RegeneratePill(onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .clip(WebPillShape)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, WebPillShape)
            .clickable(onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(
            imageVector = Icons.Filled.Refresh,
            contentDescription = null,
            modifier = Modifier.size(15.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Text(
            text = "Regenerate",
            style = MaterialTheme.typography.labelMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.primary
        )
    }
}

// ----------------------------------------------------------------------
// Input bar
// ----------------------------------------------------------------------

@Composable
private fun ChatInput(
    value: String,
    pendingFiles: List<PendingFile>,
    sending: Boolean,
    showAttach: Boolean,
    onValueChange: (String) -> Unit,
    onAttach: () -> Unit,
    onRemoveFile: (PendingFile) -> Unit,
    onClearFiles: () -> Unit,
    onSend: () -> Unit
) {
    Surface(
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 0.dp,
        modifier = Modifier.navigationBarsPadding()
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            if (pendingFiles.isNotEmpty()) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .weight(1f)
                            .horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        pendingFiles.forEach { file ->
                            PendingFileChip(file = file, onRemove = { onRemoveFile(file) })
                        }
                    }
                    TextButton(
                        onClick = onClearFiles,
                        contentPadding = PaddingValues(horizontal = 8.dp, vertical = 2.dp),
                        modifier = Modifier.align(Alignment.CenterVertically)
                    ) {
                        Text("Clear", style = MaterialTheme.typography.labelMedium)
                    }
                }
            }
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 10.dp),
                verticalAlignment = Alignment.Bottom,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                if (showAttach) {
                    IconButton(onClick = onAttach, enabled = !sending) {
                        Icon(
                            imageVector = Icons.Outlined.AttachFile,
                            contentDescription = "Attach files",
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                OutlinedTextField(
                    value = value,
                    onValueChange = onValueChange,
                    modifier = Modifier
                        .weight(1f)
                        .heightIn(min = 54.dp, max = 140.dp),
                    placeholder = { Text("Ask Neby…") },
                    enabled = !sending,
                    minLines = 1,
                    maxLines = 5
                )
                IconButton(
                    enabled = (value.isNotBlank() || pendingFiles.isNotEmpty()) && !sending,
                    onClick = onSend
                ) {
                    Icon(
                        imageVector = Icons.Filled.Send,
                        contentDescription = "Send",
                        tint = if ((value.isNotBlank() || pendingFiles.isNotEmpty()) && !sending)
                            MaterialTheme.colorScheme.primary
                        else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun PendingFileChip(
    file: PendingFile,
    onRemove: () -> Unit
) {
    val context = LocalContext.current
    val ext = file.name.substringAfterLast('.', "").lowercase()
    val isImage = ext in listOf("png", "jpg", "jpeg", "webp", "gif", "bmp")

    Row(
        modifier = Modifier
            .clip(WebPillShape)
            .background(MaterialTheme.colorScheme.secondaryContainer)
            .clickable {
                runCatching {
                    val intent = Intent(Intent.ACTION_VIEW).apply {
                        setDataAndType(file.uri, context.contentResolver.getType(file.uri) ?: "*/*")
                        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                    context.startActivity(Intent.createChooser(intent, "Open file"))
                }
            }
            .padding(start = 8.dp, end = 4.dp, top = 3.dp, bottom = 3.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        if (isImage) {
            Box(
                modifier = Modifier
                    .size(16.dp)
                    .clip(RoundedCornerShape(4.dp))
                    .background(Color.LightGray)
            ) {
                AsyncImage(
                    model = file.uri,
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            }
        } else {
            val icon = when {
                ext == "pdf" -> Icons.Outlined.Description
                ext in listOf("mp4", "mkv", "avi", "mov", "webm", "3gp", "wmv", "flv") -> Icons.Outlined.PlayCircle
                ext in listOf("mp3", "wav", "ogg", "flac", "aac", "m4a", "wma") -> Icons.Outlined.Headphones
                else -> Icons.Outlined.Description
            }
            Icon(
                imageVector = icon,
                contentDescription = null,
                modifier = Modifier.size(14.dp),
                tint = MaterialTheme.colorScheme.onSecondaryContainer
            )
        }
        Text(
            text = file.name,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSecondaryContainer,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.width(120.dp)
        )
        IconButton(onClick = onRemove, modifier = Modifier.size(20.dp)) {
            Icon(
                imageVector = Icons.Filled.Close,
                contentDescription = "Remove file",
                modifier = Modifier.size(13.dp),
                tint = MaterialTheme.colorScheme.onSecondaryContainer
            )
        }
    }
}
