package com.neb.ians.ui.screens.reader

import com.neb.ians.ui.components.MarkdownText

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
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.material3.HorizontalDivider
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
import androidx.compose.material.icons.filled.KeyboardArrowDown
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
                            viewModel = viewModel,
                            modifier = if (state.isFullscreen) Modifier.fillMaxSize() else Modifier.height(420.dp)
                        )
                    }
                }
                PdfAiPromptBar(
                    value = state.prompt,
                    onValueChange = viewModel::onPromptChange,
                    onSend = viewModel::send,
                    onCollapse = viewModel::collapseToFab,
                    onTogglePanel = viewModel::togglePanel,
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
    viewModel: PdfAssistantViewModel,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        tonalElevation = 2.dp,
        shadowElevation = 10.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 14.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Filled.AutoAwesome,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(Modifier.width(8.dp))
                Column(Modifier.weight(1f)) {
                    Text(
                        text = currentTitle(state, documentTitle),
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "AI Study Assistant",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                IconButton(onClick = viewModel::newChat, modifier = Modifier.size(34.dp)) {
                    Icon(Icons.Filled.Add, contentDescription = "New chat", modifier = Modifier.size(18.dp))
                }
                IconButton(onClick = viewModel::toggleHistory, modifier = Modifier.size(34.dp)) {
                    Icon(
                        Icons.Filled.History,
                        contentDescription = "History",
                        tint = if (state.showHistory) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(18.dp)
                    )
                }
                IconButton(onClick = viewModel::toggleFullscreen, modifier = Modifier.size(34.dp)) {
                    Icon(
                        imageVector = if (state.isFullscreen) Icons.Filled.FullscreenExit else Icons.Filled.Fullscreen,
                        contentDescription = "Toggle full screen",
                        modifier = Modifier.size(18.dp)
                    )
                }
                IconButton(onClick = viewModel::minimize, modifier = Modifier.size(34.dp)) {
                    Icon(Icons.Filled.Minimize, contentDescription = "Minimize", modifier = Modifier.size(18.dp))
                }
                IconButton(onClick = viewModel::collapseToFab, modifier = Modifier.size(34.dp)) {
                    Icon(Icons.Filled.Close, contentDescription = "Close", modifier = Modifier.size(18.dp))
                }
            }

            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)

            if (state.showHistory) {
                PdfAiHistoryList(
                    sessions = state.sessions,
                    currentSessionId = state.currentSessionId,
                    onSelectSession = viewModel::selectSession,
                    modifier = Modifier.weight(1f)
                )
            } else {
                val listState = rememberLazyListState()
                LaunchedEffect(state.messages.size, state.isThinking) {
                    if (state.messages.isNotEmpty()) {
                        listState.animateScrollToItem(state.messages.size)
                    }
                }
                LazyColumn(
                    state = listState,
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                    contentPadding = PaddingValues(vertical = 12.dp)
                ) {
                    if (state.messages.isEmpty()) {
                        item {
                            Surface(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 16.dp),
                                shape = RoundedCornerShape(16.dp),
                                color = MaterialTheme.colorScheme.surfaceContainerLow
                            ) {
                                Column(
                                    modifier = Modifier.padding(16.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Icon(
                                        Icons.Filled.AutoAwesome,
                                        contentDescription = null,
                                        tint = MaterialTheme.colorScheme.primary,
                                        modifier = Modifier.size(32.dp)
                                    )
                                    Spacer(Modifier.height(8.dp))
                                    Text(
                                        text = "Ask Neby AI about this document",
                                        style = MaterialTheme.typography.titleSmall,
                                        fontWeight = FontWeight.Bold
                                    )
                                    Spacer(Modifier.height(4.dp))
                                    Text(
                                        text = "Get summaries, explanations, formula derivations, or key questions.",
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        textAlign = androidx.compose.ui.text.style.TextAlign.Center
                                    )
                                }
                            }
                        }
                    }
                    items(state.messages, key = { it.id }) { message ->
                        PdfAiMessageBubble(message)
                    }
                    if (state.isThinking) {
                        item {
                            PdfAiThinkingBubble()
                        }
                    }
                    if (!state.error.isNullOrBlank()) {
                        item {
                            Surface(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 6.dp),
                                shape = RoundedCornerShape(12.dp),
                                color = MaterialTheme.colorScheme.errorContainer
                            ) {
                                Text(
                                    text = state.error!!,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onErrorContainer,
                                    modifier = Modifier.padding(12.dp)
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
            Box(modifier = Modifier.padding(horizontal = 13.dp, vertical = 10.dp)) {
                if (isUser) {
                    Text(
                        text = message.content,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
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
private fun PdfAiHistoryList(
    sessions: List<PdfAiSession>,
    currentSessionId: String,
    onSelectSession: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        if (sessions.isEmpty()) {
            item {
                Text("No chat history yet", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(12.dp))
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
    onTogglePanel: () -> Unit,
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
            modifier = Modifier.padding(start = 6.dp, end = 6.dp, top = 7.dp, bottom = 7.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onCollapse, modifier = Modifier.size(36.dp)) {
                Icon(Icons.Filled.Close, contentDescription = "Close PDF AI", modifier = Modifier.size(18.dp))
            }
            IconButton(onClick = onTogglePanel, modifier = Modifier.size(36.dp)) {
                Icon(
                    imageVector = if (attached) Icons.Filled.KeyboardArrowDown else Icons.Filled.KeyboardArrowUp,
                    contentDescription = if (attached) "Collapse chat view" else "Expand chat view",
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
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
