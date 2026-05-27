package com.neb.ians.ui.forum

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.ChatBubbleOutline
import androidx.compose.material.icons.rounded.Forum
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.local.ForumThreadEntity
import com.neb.ians.ui.common.EmptyState
import com.neb.ians.ui.common.NebTag

@Composable
fun ForumScreen(
    onOpenThread: (Long) -> Unit,
    onNewThread: () -> Unit,
    vm: ForumListViewModel = hiltViewModel(),
) {
    val threads by vm.threads.collectAsState()

    Scaffold(
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNewThread,
                text = { Text("New thread") },
                icon = { Icon(Icons.Rounded.Add, contentDescription = null) },
            )
        }
    ) { inner ->
        Column(Modifier.fillMaxSize().padding(inner)) {
            Text(
                "Forum",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.padding(start = 20.dp, end = 20.dp, top = 16.dp),
            )
            Text(
                "Ask. Answer. Share what's working.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 20.dp),
            )
            Spacer(Modifier.height(12.dp))

            if (threads.isEmpty()) {
                EmptyState(
                    title = "No threads yet",
                    body = "Start the first conversation — tap New thread.",
                    icon = Icons.Rounded.Forum,
                )
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 20.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    items(threads, key = { it.id }) { t ->
                        ThreadRow(
                            thread = t,
                            onClick = { onOpenThread(t.id) },
                            onLike = { vm.like(t.id) },
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ThreadRow(
    thread: ForumThreadEntity,
    onClick: () -> Unit,
    @Suppress("UNUSED_PARAMETER") onLike: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = onClick,
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(thread.title, style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(4.dp))
            Text(
                thread.body,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
            if (thread.tags.isNotBlank()) {
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    thread.tags.split(",").take(3).filter { it.isNotBlank() }.forEach { NebTag(it.trim()) }
                }
            }
            Spacer(Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "by ${thread.author}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.weight(1f))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Outlined.ThumbUp,
                        contentDescription = "Thumbs up",
                        modifier = Modifier.padding(end = 4.dp),
                    )
                    Text("${thread.likes}", style = MaterialTheme.typography.labelMedium)
                    Spacer(Modifier.width(16.dp))
                    Icon(
                        Icons.Rounded.ChatBubbleOutline,
                        contentDescription = "Replies",
                        modifier = Modifier.padding(end = 4.dp),
                    )
                    Text("${thread.replyCount}", style = MaterialTheme.typography.labelMedium)
                }
            }
        }
    }
}
