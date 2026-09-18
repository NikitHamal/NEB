package com.agentx.app.ui.screens.assistant

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.ChatBubbleOutline
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.agentx.app.data.local.entity.ConversationEntity
import com.agentx.app.ui.components.AxCard
import com.agentx.app.ui.components.AxEmptyState
import com.agentx.app.ui.components.AxFilledButton
import com.agentx.app.ui.components.AxTextButton
import com.agentx.app.util.FormatUtils
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AssistantScreen(
    onOpenChat: (String) -> Unit,
    onOpenSettings: () -> Unit,
    viewModel: ConversationsViewModel = hiltViewModel()
) {
    val conversations by viewModel.conversations.collectAsStateWithLifecycle()
    val scope = rememberCoroutineScope()
    var menuFor by remember { mutableStateOf<String?>(null) }
    var renameFor by remember { mutableStateOf<ConversationEntity?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Filled.Bolt, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(8.dp))
                        Text("AgentX", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                    }
                },
                actions = {
                    IconButton(onClick = onOpenSettings) {
                        Icon(Icons.Filled.Settings, contentDescription = "Settings")
                    }
                },
                modifier = Modifier.statusBarsPadding()
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = {
                scope.launch { onOpenChat(viewModel.createNew()) }
            }) {
                Icon(Icons.Filled.Add, contentDescription = "New chat")
            }
        }
    ) { padding ->
        if (conversations.isEmpty()) {
            AxEmptyState(
                icon = Icons.Filled.SmartToy,
                title = "No conversations yet",
                subtitle = "Start a new chat and tell AgentX what to do on this phone. All offline.",
                modifier = Modifier.padding(padding).fillMaxSize(),
                action = {
                    AxFilledButton(text = "New chat", onClick = {
                        scope.launch { onOpenChat(viewModel.createNew()) }
                    })
                }
            )
        } else {
            LazyColumn(
                modifier = Modifier.padding(padding).fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(conversations, key = { it.id }) { conversation ->
                    ConversationRow(
                        conversation = conversation,
                        menuOpen = menuFor == conversation.id,
                        onOpen = { onOpenChat(conversation.id) },
                        onMenu = { menuFor = conversation.id },
                        onDismissMenu = { menuFor = null },
                        onRename = { renameFor = conversation; menuFor = null },
                        onClear = { viewModel.clear(conversation.id); menuFor = null },
                        onDelete = { viewModel.delete(conversation.id); menuFor = null }
                    )
                }
            }
        }
    }

    renameFor?.let { conversation ->
        var title by remember(conversation.id) { mutableStateOf(conversation.title) }
        AlertDialog(
            onDismissRequest = { renameFor = null },
            title = { Text("Rename conversation") },
            text = {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it.take(80) },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                AxFilledButton(text = "Save", onClick = {
                    if (title.isNotBlank()) viewModel.rename(conversation.id, title.trim())
                    renameFor = null
                })
            },
            dismissButton = { AxTextButton(text = "Cancel", onClick = { renameFor = null }) }
        )
    }
}

@Composable
private fun ConversationRow(
    conversation: ConversationEntity,
    menuOpen: Boolean,
    onOpen: () -> Unit,
    onMenu: () -> Unit,
    onDismissMenu: () -> Unit,
    onRename: () -> Unit,
    onClear: () -> Unit,
    onDelete: () -> Unit
) {
    AxCard(modifier = Modifier.fillMaxWidth().clickable(onClick = onOpen)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                Icons.Filled.ChatBubbleOutline,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(22.dp)
            )
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    conversation.title.ifBlank { "New chat" },
                    style = MaterialTheme.typography.titleSmall,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(Modifier.height(2.dp))
                Text(
                    conversation.lastPreview.ifBlank { "No messages yet" },
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(Modifier.height(2.dp))
                Text(
                    FormatUtils.formatTimeAgo(conversation.updatedAt) + " · " + conversation.messageCount + " messages",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            IconButton(onClick = onMenu) {
                Icon(Icons.Filled.MoreVert, contentDescription = "Conversation options")
                DropdownMenu(expanded = menuOpen, onDismissRequest = onDismissMenu) {
                    DropdownMenuItem(
                        text = { Text("Rename") },
                        leadingIcon = { Icon(Icons.Filled.Edit, contentDescription = null) },
                        onClick = onRename
                    )
                    DropdownMenuItem(
                        text = { Text("Clear messages") },
                        onClick = onClear
                    )
                    DropdownMenuItem(
                        text = { Text("Delete", color = MaterialTheme.colorScheme.error) },
                        leadingIcon = { Icon(Icons.Filled.Delete, contentDescription = null, tint = MaterialTheme.colorScheme.error) },
                        onClick = onDelete
                    )
                }
            }
        }
    }
}
