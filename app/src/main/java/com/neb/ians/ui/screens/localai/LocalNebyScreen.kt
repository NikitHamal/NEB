package com.neb.ians.ui.screens.localai

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.ClearAll
import androidx.compose.material.icons.outlined.CloudDownload
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.OfflineBolt
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Storage
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.needle.LocalNeedleMessage
import com.neb.ians.data.needle.LocalNeedleToolCall
import com.neb.ians.data.needle.NeedleModelState
import com.neb.ians.data.needle.NeedleRuntimeState
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun LocalNebyScreen(
    onNavigateBack: () -> Unit,
    onToolAction: (LocalNeedleToolCall) -> Unit,
    viewModel: LocalNebyViewModel = hiltViewModel()
) {
    val modelState by viewModel.modelState.collectAsStateWithLifecycle()
    val runtimeState by viewModel.runtimeState.collectAsStateWithLifecycle()
    val messages by viewModel.messages.collectAsStateWithLifecycle()
    val isRunning by viewModel.isRunning.collectAsStateWithLifecycle()
    var input by remember { mutableStateOf("") }
    var showMenu by remember { mutableStateOf(false) }
    var showDelete by remember { mutableStateOf(false) }
    val listState = rememberLazyListState()
    val ready = runtimeState is NeedleRuntimeState.Ready

    LaunchedEffect(messages.size, isRunning) {
        if (messages.isNotEmpty()) listState.animateScrollToItem(messages.size + if (isRunning) 1 else 0)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                title = {
                    Column {
                        Text("Neby Local", fontWeight = FontWeight.SemiBold)
                        Text(
                            text = if (ready) "Private · offline · on-device" else "Needle 2 setup",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                actions = {
                    if (modelState is NeedleModelState.Ready) {
                        Box {
                            IconButton(onClick = { showMenu = true }) {
                                Icon(Icons.Outlined.MoreVert, contentDescription = "More options")
                            }
                            DropdownMenu(expanded = showMenu, onDismissRequest = { showMenu = false }) {
                                DropdownMenuItem(
                                    text = { Text("Clear chat") },
                                    leadingIcon = { Icon(Icons.Outlined.ClearAll, contentDescription = null) },
                                    onClick = {
                                        showMenu = false
                                        viewModel.clearHistory()
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("Remove offline AI", color = MaterialTheme.colorScheme.error) },
                                    leadingIcon = {
                                        Icon(
                                            Icons.Outlined.DeleteOutline,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.error
                                        )
                                    },
                                    onClick = {
                                        showMenu = false
                                        showDelete = true
                                    }
                                )
                            }
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        },
        bottomBar = {
            if (modelState is NeedleModelState.Ready) {
                LocalChatInput(
                    value = input,
                    enabled = ready && !isRunning,
                    onValueChange = { input = it },
                    onSend = {
                        val value = input
                        input = ""
                        viewModel.send(value)
                    }
                )
            }
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
        when (val state = modelState) {
            NeedleModelState.Checking -> LoadingCenter("Checking on-device model", Modifier.padding(padding))
            NeedleModelState.NotInstalled -> ModelSetup(
                error = null,
                resumableBytes = 0L,
                onDownload = viewModel::downloadModel,
                modifier = Modifier.padding(padding)
            )
            is NeedleModelState.Error -> ModelSetup(
                error = state.message,
                resumableBytes = state.resumableBytes,
                onDownload = viewModel::downloadModel,
                modifier = Modifier.padding(padding)
            )
            is NeedleModelState.Downloading -> DownloadProgress(
                state = state,
                onCancel = viewModel::cancelDownload,
                modifier = Modifier.padding(padding)
            )
            is NeedleModelState.Ready -> LazyColumn(
                state = listState,
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                item(key = "runtime-status") {
                    RuntimeStatus(state = runtimeState, onRetry = viewModel::retryRuntime)
                }
                if (messages.isEmpty()) {
                    item(key = "welcome") { WelcomeCard(onSuggestion = viewModel::send) }
                }
                items(messages, key = { it.id }) { message ->
                    LocalMessageBubble(message = message, onToolAction = onToolAction)
                }
                if (isRunning) {
                    item(key = "thinking") {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(9.dp),
                            modifier = Modifier.padding(start = 4.dp)
                        ) {
                            CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                            Text(
                                "Needle is choosing an action…",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }

    if (showDelete) {
        AlertDialog(
            onDismissRequest = { showDelete = false },
            title = { Text("Remove offline AI?") },
            text = { Text("This deletes the downloaded model and saved runtime. Your chat history stays until you clear it.") },
            confirmButton = {
                TextButton(onClick = {
                    showDelete = false
                    viewModel.deleteModel()
                }) { Text("Remove", color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = { TextButton(onClick = { showDelete = false }) { Text("Cancel") } }
        )
    }
}

@Composable
private fun LoadingCenter(label: String, modifier: Modifier = Modifier) {
    Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            CircularProgressIndicator()
            Spacer(Modifier.height(12.dp))
            Text(label, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
private fun ModelSetup(
    error: String?,
    resumableBytes: Long,
    onDownload: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Surface(shape = CircleShape, color = MaterialTheme.colorScheme.primaryContainer) {
            Icon(
                Icons.Outlined.AutoAwesome,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.padding(18.dp).size(38.dp)
            )
        }
        Spacer(Modifier.height(20.dp))
        Text("Set up private on-device AI", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        Text(
            "Download Needle 2 once, then understand NEBians searches and actions without sending your prompt to a server.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(Modifier.height(20.dp))
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            SetupFact(Icons.Outlined.CloudDownload, "13.1 MB model download")
            SetupFact(Icons.Outlined.OfflineBolt, "Works without internet after setup")
            SetupFact(Icons.Outlined.Shield, "Prompts stay on this device")
            SetupFact(Icons.Outlined.Storage, "About 33 MB memory while active")
        }
        if (error != null) {
            Spacer(Modifier.height(16.dp))
            Text(error, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
        }
        Spacer(Modifier.height(22.dp))
        Button(onClick = onDownload, modifier = Modifier.fillMaxWidth()) {
            Icon(Icons.Outlined.CloudDownload, contentDescription = null)
            Spacer(Modifier.width(8.dp))
            Text(if (resumableBytes > 0) "Resume download" else "Download and set up")
        }
        Text(
            "The model is optional and is not included in the app download.",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(top = 10.dp)
        )
    }
}

@Composable
private fun SetupFact(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
        Text(text, style = MaterialTheme.typography.bodySmall)
    }
}

@Composable
private fun DownloadProgress(
    state: NeedleModelState.Downloading,
    onCancel: () -> Unit,
    modifier: Modifier = Modifier
) {
    val fraction = if (state.totalBytes > 0) (state.downloadedBytes.toFloat() / state.totalBytes).coerceIn(0f, 1f) else 0f
    Column(
        modifier = modifier.fillMaxSize().padding(28.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(Icons.Outlined.CloudDownload, contentDescription = null, modifier = Modifier.size(44.dp), tint = MaterialTheme.colorScheme.primary)
        Spacer(Modifier.height(18.dp))
        Text("Downloading Needle 2", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
        Spacer(Modifier.height(6.dp))
        Text(
            "${formatBytes(state.downloadedBytes)} of ${formatBytes(state.totalBytes)}",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.bodySmall
        )
        Spacer(Modifier.height(16.dp))
        LinearProgressIndicator(progress = fraction, modifier = Modifier.fillMaxWidth())
        Spacer(Modifier.height(18.dp))
        OutlinedButton(onClick = onCancel) { Text("Pause") }
    }
}

@Composable
private fun RuntimeStatus(state: NeedleRuntimeState, onRetry: () -> Unit) {
    when (state) {
        NeedleRuntimeState.Idle -> StatusSurface("Starting local runtime…", null)
        is NeedleRuntimeState.Loading -> StatusSurface(state.label, state.progress)
        is NeedleRuntimeState.Ready -> {
            val detail = if (state.source == "snapshot") "Saved runtime restored" else "Runtime prepared"
            Surface(
                color = MaterialTheme.colorScheme.secondaryContainer,
                shape = RoundedCornerShape(14.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Outlined.CheckCircle, contentDescription = null, tint = MaterialTheme.colorScheme.onSecondaryContainer)
                    Spacer(Modifier.width(9.dp))
                    Text(
                        "$detail in ${String.format(Locale.US, "%.1f", state.loadSeconds)}s · offline ready",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSecondaryContainer
                    )
                }
            }
        }
        is NeedleRuntimeState.Error -> Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
            Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(state.message, modifier = Modifier.weight(1f), style = MaterialTheme.typography.bodySmall)
                TextButton(onClick = onRetry) { Text("Retry") }
            }
        }
    }
}

@Composable
private fun StatusSurface(label: String, progress: Float?) {
    Surface(color = MaterialTheme.colorScheme.surfaceContainerHigh, shape = RoundedCornerShape(14.dp), modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                Spacer(Modifier.width(9.dp))
                Text(label, style = MaterialTheme.typography.bodySmall)
            }
            if (progress != null) {
                Spacer(Modifier.height(8.dp))
                LinearProgressIndicator(progress = progress, modifier = Modifier.fillMaxWidth())
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun WelcomeCard(onSuggestion: (String) -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
        shape = RoundedCornerShape(18.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Small model, focused job", fontWeight = FontWeight.SemiBold)
            Text(
                "Neby Local maps your words to NEBians searches and navigation. It is not a general-purpose chatbot.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 5.dp, bottom = 12.dp)
            )
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                listOf(
                    "Find Physics notes for Class 12",
                    "Show popular forum posts",
                    "What subjects are available?"
                ).forEach { suggestion ->
                    OutlinedButton(onClick = { onSuggestion(suggestion) }, contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)) {
                        Text(suggestion, style = MaterialTheme.typography.labelSmall)
                    }
                }
            }
        }
    }
}

@Composable
private fun LocalMessageBubble(message: LocalNeedleMessage, onToolAction: (LocalNeedleToolCall) -> Unit) {
    var reasoningExpanded by remember(message.id) { mutableStateOf(false) }
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (message.isUser) Arrangement.End else Arrangement.Start
    ) {
        Column(modifier = Modifier.fillMaxWidth(if (message.isUser) 0.84f else 0.94f)) {
            Surface(
                shape = RoundedCornerShape(18.dp),
                color = if (message.isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceContainerHigh,
                contentColor = if (message.isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
            ) {
                Text(message.text, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp))
            }
            if (!message.isUser && !message.reasoning.isNullOrBlank()) {
                Surface(
                    modifier = Modifier.padding(top = 6.dp).clickable { reasoningExpanded = !reasoningExpanded },
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.surfaceContainer
                ) {
                    Column(modifier = Modifier.padding(horizontal = 11.dp, vertical = 8.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Outlined.Psychology, contentDescription = null, modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.width(6.dp))
                            Text("How Needle understood this", style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
                        }
                        AnimatedVisibility(visible = reasoningExpanded) {
                            Column {
                                Text(
                                    message.reasoning.orEmpty(),
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(top = 7.dp)
                                )
                                Text(
                                    buildMetrics(message),
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(top = 6.dp)
                                )
                            }
                        }
                    }
                }
            }
            message.toolCalls.forEach { call ->
                ToolActionCard(call = call, onClick = { onToolAction(call) })
            }
        }
    }
}

@Composable
private fun ToolActionCard(call: LocalNeedleToolCall, onClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(top = 7.dp).clickable(onClick = onClick),
        shape = RoundedCornerShape(13.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Row(modifier = Modifier.padding(11.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Outlined.Search, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.width(10.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(toolLabel(call), style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
                Text(
                    call.argumentsJson.removePrefix("{").removeSuffix("}").replace("\"", ""),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Text("Open", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium)
        }
    }
}

@Composable
private fun LocalChatInput(
    value: String,
    enabled: Boolean,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit
) {
    Surface(shadowElevation = 4.dp, color = MaterialTheme.colorScheme.surface) {
        Row(
            modifier = Modifier.fillMaxWidth().imePadding().padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = value,
                onValueChange = onValueChange,
                enabled = enabled,
                placeholder = { Text(if (enabled) "Ask for a NEBians action…" else "Preparing local AI…") },
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(22.dp),
                maxLines = 4,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                keyboardActions = KeyboardActions(onSend = { if (value.isNotBlank() && enabled) onSend() })
            )
            Spacer(Modifier.width(8.dp))
            IconButton(onClick = onSend, enabled = enabled && value.isNotBlank()) {
                Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = MaterialTheme.colorScheme.primary)
            }
        }
    }
}

private fun toolLabel(call: LocalNeedleToolCall): String = when (call.name) {
    "search_resources" -> "Search resources"
    "find_notes" -> "Find notes and papers"
    "get_forum_posts" -> "Open forum discussions"
    "get_subjects" -> "Browse subjects"
    "navigate_to" -> "Open ${call.argument("page") ?: "page"}"
    else -> call.name.replace('_', ' ')
}

private fun buildMetrics(message: LocalNeedleMessage): String {
    val parts = mutableListOf<String>()
    message.confidence?.let { parts += "confidence ${String.format(Locale.US, "%.0f", it * 100)}%" }
    message.durationMs?.let { parts += "${String.format(Locale.US, "%.0f", it)} ms on this device" }
    return parts.joinToString(" · ")
}

private fun formatBytes(bytes: Long): String = String.format(Locale.US, "%.1f MB", bytes / (1024.0 * 1024.0))
