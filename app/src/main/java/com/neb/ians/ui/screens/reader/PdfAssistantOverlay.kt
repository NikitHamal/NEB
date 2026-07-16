package com.neb.ians.ui.screens.reader

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.FullscreenExit
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.Minimize
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun PdfAssistantOverlay(
    documentTitle: String,
    modifier: Modifier = Modifier,
    viewModel: PdfAssistantViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Box(modifier = modifier.fillMaxSize()) {
        if (!state.isPromptOpen) {
            FloatingActionButton(
                onClick = viewModel::openPrompt,
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(18.dp),
                shape = CircleShape,
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(Icons.Filled.AutoAwesome, contentDescription = "Ask AI about this PDF")
            }
        } else {
            val shellModifier = if (state.isFullscreen) {
                Modifier
                    .fillMaxSize()
                    .padding(10.dp)
            } else {
                Modifier
                    .align(Alignment.BottomEnd)
                    .padding(horizontal = 12.dp, vertical = 10.dp)
                    .widthIn(max = 390.dp)
                    .fillMaxWidth()
            }
            Column(
                modifier = shellModifier.imePadding(),
                horizontalAlignment = Alignment.End,
                verticalArrangement = Arrangement.Bottom
            ) {
                AnimatedVisibility(
                    visible = state.isPanelOpen,
                    modifier = if (state.isFullscreen) Modifier.weight(1f) else Modifier,
                    enter = fadeIn() + slideInVertically { it / 4 },
                    exit = fadeOut() + slideOutVertically { it / 4 }
                ) {
                    if (state.isMinimized) {
                        PdfAiMinimizedBar(
                            title = currentTitle(state, documentTitle),
                            onExpand = viewModel::expandPanel
                        )
                    } else {
                        PdfAiPanel(
                            state = state,
                            documentTitle = documentTitle,
                            onToggleHistory = viewModel::toggleHistory,
                            onToggleFullscreen = viewModel::toggleFullscreen,
                            onMinimize = viewModel::minimize,
                            onNewChat = viewModel::newChat,
                            onSelectSession = viewModel::selectSession,
                            modifier = if (state.isFullscreen) Modifier.fillMaxSize() else Modifier.height(420.dp)
                        )
                    }
                }
                PdfAiPromptBar(
                    value = state.prompt,
                    onValueChange = viewModel::onPromptChange,
                    onSend = viewModel::send,
                    onCollapse = viewModel::collapseToFab,
                    isThinking = state.isThinking,
                    attached = state.isPanelOpen
                )
            }
        }
    }
}

@Composable
private fun PdfAiPanel(
    state: PdfAssistantUiState,
    documentTitle: String,
    onToggleHistory: () -> Unit,
    onToggleFullscreen: () -> Unit,
    onMinimize: () -> Unit,
    onNewChat: () -> Unit,
    onSelectSession: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState()
    LaunchedEffect(state.messages.size, state.isThinking) {
        val count = state.messages.size + if (state.isThinking) 1 else 0
        if (count > 0) listState.animateScrollToItem(count - 1)
    }

    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp, bottomStart = 0.dp, bottomEnd = 0.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        tonalElevation = 4.dp,
        shadowElevation = 8.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(start = 16.dp, end = 6.dp, top = 8.dp, bottom = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Filled.AutoAwesome, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
                Spacer(Modifier.width(8.dp))
                Column(Modifier.weight(1f)) {
                    Text(currentTitle(state, documentTitle), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Grounded in this PDF", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                IconButton(onClick = onToggleHistory, modifier = Modifier.size(38.dp)) {
                    Icon(Icons.Filled.History, contentDescription = "Chat history", modifier = Modifier.size(19.dp))
                }
                IconButton(onClick = onToggleFullscreen, modifier = Modifier.size(38.dp)) {
                    Icon(
                        if (state.isFullscreen) Icons.Filled.FullscreenExit else Icons.Filled.Fullscreen,
                        contentDescription = if (state.isFullscreen) "Exit full screen" else "Full screen",
                        modifier = Modifier.size(19.dp)
                    )
                }
                IconButton(onClick = onMinimize, modifier = Modifier.size(38.dp)) {
                    Icon(Icons.Filled.Minimize, contentDescription = "Minimize", modifier = Modifier.size(19.dp))
                }
            }

            if (state.showHistory) {
                PdfAiHistory(
                    sessions = state.sessions,
                    currentSessionId = state.currentSessionId,
                    onNewChat = onNewChat,
                    onSelectSession = onSelectSession,
                    modifier = Modifier.weight(1f)
                )
            } else {
                LazyColumn(
                    state = listState,
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 14.dp, vertical = 10.dp),
                    verticalArrangement = Arrangement.spacedBy(9.dp)
                ) {
                    if (state.messages.isEmpty() && !state.isThinking) {
                        item {
                            Text(
                                "Ask for an explanation, summary, formula, definition, or answer from this document.",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(12.dp)
                            )
                        }
                    }
                    items(state.messages, key = { it.id }) { message ->
                        PdfAiMessageBubble(message)
                    }
                    if (state.isThinking) {
                        item { PdfAiThinkingBubble() }
                    }
                    state.error?.let { error ->
                        item {
                            Text(
                                error,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.error,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun PdfAiMessageBubble(message: PdfAiMessage) {
    val isUser = message.role == "user"
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            modifier = Modifier.fillMaxWidth(if (isUser) 0.82f else 0.96f),
            shape = RoundedCornerShape(
                topStart = 18.dp,
                topEnd = 18.dp,
                bottomStart = if (isUser) 18.dp else 4.dp,
                bottomEnd = if (isUser) 4.dp else 18.dp
            ),
            color = if (isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceContainerLow
        ) {
            Text(
                message.content,
                style = MaterialTheme.typography.bodyMedium,
                color = if (isUser) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,
                modifier = Modifier.padding(horizontal = 13.dp, vertical = 10.dp)
            )
        }
    }
}

@Composable
private fun PdfAiThinkingBubble() {
    val transition = rememberInfiniteTransition(label = "pdfAiTyping")
    Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp)) {
        repeat(3) { index ->
            val alpha by transition.animateFloat(
                initialValue = 0.25f,
                targetValue = 1f,
                animationSpec = infiniteRepeatable(
                    animation = tween(620, delayMillis = index * 130),
                    repeatMode = RepeatMode.Reverse
                ),
                label = "dot$index"
            )
            Box(
                Modifier
                    .size(7.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = alpha))
            )
        }
    }
}

@Composable
private fun PdfAiHistory(
    sessions: List<PdfAiSession>,
    currentSessionId: String,
    onNewChat: () -> Unit,
    onSelectSession: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxWidth(),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable(onClick = onNewChat),
                shape = RoundedCornerShape(14.dp),
                color = MaterialTheme.colorScheme.primaryContainer
            ) {
                Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Filled.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(8.dp))
                    Text("New PDF chat", fontWeight = FontWeight.SemiBold)
                }
            }
        }
        items(sessions, key = { it.id }) { session ->
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onSelectSession(session.id) },
                shape = RoundedCornerShape(14.dp),
                color = if (session.id == currentSessionId) MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surfaceContainerLow
            ) {
                Column(Modifier.padding(12.dp)) {
                    Text(session.title, style = MaterialTheme.typography.titleSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("${session.messages.size} messages", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

@Composable
private fun PdfAiMinimizedBar(title: String, onExpand: () -> Unit) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(topStart = 18.dp, topEnd = 18.dp, bottomStart = 0.dp, bottomEnd = 0.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(Modifier.padding(start = 14.dp, end = 6.dp, top = 6.dp, bottom = 6.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Filled.AutoAwesome, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
            Spacer(Modifier.width(8.dp))
            Text(title, modifier = Modifier.weight(1f), style = MaterialTheme.typography.titleSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
            IconButton(onClick = onExpand, modifier = Modifier.size(36.dp)) {
                Icon(Icons.Filled.KeyboardArrowUp, contentDescription = "Expand chat")
            }
        }
    }
}

@Composable
private fun PdfAiPromptBar(
    value: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    onCollapse: () -> Unit,
    isThinking: Boolean,
    attached: Boolean
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = if (attached) {
            RoundedCornerShape(topStart = 0.dp, topEnd = 0.dp, bottomStart = 24.dp, bottomEnd = 24.dp)
        } else {
            RoundedCornerShape(24.dp)
        },
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        tonalElevation = 4.dp,
        shadowElevation = 8.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(start = 10.dp, end = 6.dp, top = 7.dp, bottom = 7.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onCollapse, modifier = Modifier.size(36.dp)) {
                Icon(Icons.Filled.Close, contentDescription = "Close PDF AI", modifier = Modifier.size(18.dp))
            }
            OutlinedTextField(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier.weight(1f),
                placeholder = { Text("Ask this PDF", style = MaterialTheme.typography.bodyMedium) },
                maxLines = 3,
                shape = RoundedCornerShape(20.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedBorderColor = Color.Transparent,
                    unfocusedBorderColor = Color.Transparent
                )
            )
            IconButton(
                onClick = onSend,
                enabled = value.isNotBlank() && !isThinking,
                modifier = Modifier
                    .size(42.dp)
                    .background(
                        if (value.isNotBlank() && !isThinking) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceContainerHigh,
                        CircleShape
                    )
            ) {
                if (isThinking) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                } else {
                    Icon(
                        Icons.Filled.ArrowUpward,
                        contentDescription = "Send",
                        tint = if (value.isNotBlank()) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

private fun currentTitle(state: PdfAssistantUiState, documentTitle: String): String {
    return state.sessions.firstOrNull { it.id == state.currentSessionId }?.title
        ?.takeIf { it.isNotBlank() && it != "PDF chat" }
        ?: documentTitle.ifBlank { "PDF chat" }
}
