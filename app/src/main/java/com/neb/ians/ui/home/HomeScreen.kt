package com.neb.ians.ui.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoStories
import androidx.compose.material.icons.rounded.Bolt
import androidx.compose.material.icons.rounded.NotificationsActive
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.local.ResourceEntity
import com.neb.ians.ui.common.EmptyState
import com.neb.ians.ui.common.SectionHeader
import com.neb.ians.ui.library.ResourceCard

@Composable
fun HomeScreen(
    onOpenResource: (Long) -> Unit,
    vm: HomeViewModel = hiltViewModel(),
) {
    val recent by vm.recent.collectAsState()
    val favorites by vm.favorites.collectAsState()
    val all by vm.all.collectAsState()

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 24.dp),
    ) {
        item {
            Column(Modifier.padding(start = 20.dp, end = 20.dp, top = 16.dp)) {
                Text("Hello, Student", style = MaterialTheme.typography.headlineMedium)
                Text(
                    "Pick up where you left off.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Spacer(Modifier.height(16.dp))
        }

        item {
            LazyRow(
                contentPadding = PaddingValues(horizontal = 20.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                item {
                    HighlightTile(
                        title = "Announcements",
                        body = "Stay updated with NEB notices.",
                        icon = Icons.Rounded.NotificationsActive,
                    )
                }
                item {
                    HighlightTile(
                        title = "Quick Read",
                        body = "Bite-sized chapter recaps.",
                        icon = Icons.Rounded.Bolt,
                    )
                }
                item {
                    HighlightTile(
                        title = "Daily Practice",
                        body = "A new past-paper every day.",
                        icon = Icons.Rounded.AutoStories,
                    )
                }
            }
        }

        item { SectionHeader("Recent") }
        if (recent.isEmpty()) {
            item { Box(Modifier.fillMaxWidth().height(160.dp)) { EmptyState("Nothing yet", "Open a resource to see it here.", Icons.Rounded.AutoStories) } }
        } else {
            items(recent, key = { "r-${it.id}" }) { r ->
                ResourceCardRow(r, onOpenResource)
            }
        }

        item { SectionHeader("Saved") }
        if (favorites.isEmpty()) {
            item {
                Text(
                    "Tap the bookmark on any resource to save it for offline access.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp),
                )
            }
        } else {
            items(favorites, key = { "f-${it.id}" }) { r ->
                ResourceCardRow(r, onOpenResource)
            }
        }

        item { SectionHeader("All resources") }
        items(all, key = { "a-${it.id}" }) { r -> ResourceCardRow(r, onOpenResource) }
    }
}

@Composable
private fun ResourceCardRow(r: ResourceEntity, onOpen: (Long) -> Unit) {
    ResourceCard(
        resource = r,
        onClick = { onOpen(r.id) },
        onToggleFavorite = {},
        modifier = Modifier.padding(horizontal = 20.dp, vertical = 4.dp),
    )
}

@Composable
private fun HighlightTile(
    title: String,
    body: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
) {
    Card(
        modifier = Modifier.width(220.dp).height(120.dp),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    ) {
        Column(Modifier.padding(14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    color = MaterialTheme.colorScheme.primary.copy(alpha = 0.12f),
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.size(32.dp),
                ) {
                    Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize()) {
                        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.onPrimaryContainer)
                    }
                }
                Spacer(Modifier.width(8.dp))
                Text(
                    title,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                )
            }
            Spacer(Modifier.height(8.dp))
            Text(
                body,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}
