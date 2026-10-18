package com.neb.ians.ui.screens.ai

import androidx.compose.material.icons.outlined.KeyboardArrowDown
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.ui.theme.nebEffectsSpec
import androidx.compose.animation.scaleOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.fadeIn
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.runtime.derivedStateOf
import androidx.compose.foundation.lazy.itemsIndexed
import com.neb.ians.ui.screens.ai.chat.enterOnce
import com.neb.ians.ui.screens.ai.chat.UserMessage
import com.neb.ians.ui.screens.ai.chat.NebyChatWelcome
import com.neb.ians.ui.screens.ai.chat.NebyChatComposer
import com.neb.ians.ui.screens.ai.chat.ChatPhase
import com.neb.ians.ui.screens.ai.chat.ChatActions
import com.neb.ians.ui.screens.ai.chat.AssistantMessage
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
import androidx.compose.foundation.layout.height
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
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.History
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import android.content.Intent
import android.net.Uri
import coil.compose.AsyncImage
import androidx.compose.material.icons.outlined.PlayCircle
import androidx.compose.material.icons.outlined.Headphones
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import com.neb.ians.ui.components.NebConfirmDialog
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebSelectIndicator
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebIconButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebPrimaryButton
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.util.formatTimeAgo
import kotlinx.coroutines.launch
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebLoader

private val ArenaTint = Color(0xFF47474B)
private val QwenTint = Color(0xFF7C7C83)

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

    // Follow the conversation only while the reader is at the bottom; a new message always scrolls.
    val atBottom by remember {
        derivedStateOf {
            val info = listState.layoutInfo
            val last = info.visibleItemsInfo.lastOrNull()
            last == null || (last.index >= info.totalItemsCount - 1 && last.offset + last.size <= info.viewportEndOffset + 120)
        }
    }
    val messageCount = uiState.messages.size
    val lastContentLength = uiState.messages.lastOrNull()?.content?.length ?: 0
    LaunchedEffect(messageCount) {
        val total = listState.layoutInfo.totalItemsCount
        if (total > 0) runCatching { listState.animateScrollToItem(total - 1, Int.MAX_VALUE / 4) }
    }
    LaunchedEffect(lastContentLength) {
        val total = listState.layoutInfo.totalItemsCount
        if (total > 0 && atBottom) runCatching { listState.scrollToItem(total - 1, Int.MAX_VALUE / 4) }
    }
    val context = LocalContext.current
    val copy: (String) -> Unit = { text ->
        clipboard.setText(AnnotatedString(text))
        scope.launch { snackbarHostState.showSnackbar("Copied") }
    }
    val actions = remember(viewModel) {
        ChatActions(
            onCopy = { text -> clipboard.setText(AnnotatedString(text)); scope.launch { snackbarHostState.showSnackbar("Copied") } },
            onShare = { text ->
                runCatching {
                    context.startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply { type = "text/plain"; putExtra(Intent.EXTRA_TEXT, text) }, "Share Neby's answer"))
                }
            },
            onRegenerate = viewModel::regenerate
        )
    }
    val modelLabel = uiState.selectedSession?.let { it.modelName.ifBlank { it.modelCode } }

    val activeSession = uiState.selectedSession

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Neby AI",
                subtitle = activeSession?.let {
                    val model = it.modelName.ifBlank { it.modelCode.ifBlank { "AI model" } }
                    "$model, ${providerLabel(it.provider)}"
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
            if (uiState.error == null && uiState.selectedSession != null) {
                NebyChatComposer(
                    value = input,
                    onValueChange = { input = it },
                    pendingFiles = uiState.pendingFiles,
                    streaming = uiState.isStreaming,
                    canAttach = true,
                    onAttach = { filePicker.launch("*/*") },
                    onRemoveFile = viewModel::removeFile,
                    onSend = {
                        val message = input
                        input = ""
                        viewModel.send(message)
                    },
                    onStop = viewModel::stop
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
                    ) { NebLoader() }
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
                    Box(Modifier.fillMaxSize()) {
                        LazyColumn(
                            state = listState,
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 12.dp, bottom = 20.dp),
                            verticalArrangement = Arrangement.spacedBy(18.dp)
                        ) {
                            if (uiState.messages.isEmpty() && !uiState.isStreaming) {
                                item(key = "welcome") {
                                    NebyChatWelcome(name = null, onStarter = { viewModel.send(it) })
                                }
                            }
                            itemsIndexed(uiState.messages, key = { _, m -> m.id }) { i, message ->
                                val isLast = i == uiState.messages.lastIndex
                                val fresh = message.id.startsWith("local-")
                                if (message.role == "user") {
                                    UserMessage(message, onCopy = copy, modifier = Modifier.enterOnce(message.id, fresh))
                                } else {
                                    val phase = when {
                                        !(isLast && uiState.isStreaming) -> ChatPhase.Idle
                                        message.content.isNotBlank() -> ChatPhase.Writing
                                        uiState.messages.getOrNull(i - 1)?.attachments?.isNotEmpty() == true -> ChatPhase.Reading
                                        else -> ChatPhase.Thinking
                                    }
                                    AssistantMessage(
                                        message = message,
                                        phase = phase,
                                        isLast = isLast,
                                        modelLabel = modelLabel,
                                        actions = actions,
                                        modifier = Modifier.enterOnce(message.id, fresh)
                                    )
                                }
                            }
                        }
                        JumpToLatest(
                            visible = !atBottom && uiState.messages.isNotEmpty(),
                            streaming = uiState.isStreaming,
                            onClick = { scope.launch { val n = listState.layoutInfo.totalItemsCount; if (n > 0) listState.animateScrollToItem(n - 1, Int.MAX_VALUE / 4) } },
                            modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 12.dp)
                        )
                    }
                }
            }
        }
    }

    if (showSessions) {
        NebModalSheet(
            onDismiss = { showSessions = false },
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
        NebDialog(
            onDismissRequest = { renameTarget = null },
            title = "Rename chat",
            icon = Icons.Outlined.Edit,
            confirm = NebDialogAction(
                label = "Save",
                onClick = {
                    viewModel.renameSession(target.id, titleText)
                    renameTarget = null
                }
            ),
            dismiss = NebDialogAction("Cancel", { renameTarget = null })
        ) {
            NebDialogTextField(
                value = titleText,
                onValueChange = { titleText = it },
                label = "Title"
            )
        }
    }

    deleteTarget?.let { target ->
        NebConfirmDialog(
            title = "Delete chat?",
            message = "\"${target.title}\" and all its messages will be permanently deleted.",
            confirmLabel = "Delete",
            onConfirm = {
                viewModel.deleteSession(target.id)
                deleteTarget = null
            },
            onDismiss = { deleteTarget = null },
            icon = Icons.Outlined.DeleteOutline,
            destructive = true
        )
    }
}

@Composable
private fun JumpToLatest(visible: Boolean, streaming: Boolean, onClick: () -> Unit, modifier: Modifier) {
    AnimatedVisibility(
        visible = visible,
        enter = fadeIn(nebEffectsSpec()) + scaleIn(nebSpatialSpec(), initialScale = 0.8f),
        exit = fadeOut(nebEffectsSpec()) + scaleOut(nebSpatialSpec(), targetScale = 0.8f),
        modifier = modifier
    ) {
        Row(
            Modifier
                .clip(RoundedCornerShape(18.dp))
                .background(MaterialTheme.colorScheme.inverseSurface)
                .nebPressable(onClick = onClick)
                .padding(horizontal = 14.dp, vertical = 9.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Icon(Icons.Outlined.KeyboardArrowDown, contentDescription = null, tint = MaterialTheme.colorScheme.inverseOnSurface, modifier = Modifier.size(18.dp))
            Text(if (streaming) "Neby is writing" else "Latest", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.inverseOnSurface)
        }
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
                NebLoader(size = NebLoaderSize.Inline)
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
            NebSelectIndicator(selected = selected)
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
