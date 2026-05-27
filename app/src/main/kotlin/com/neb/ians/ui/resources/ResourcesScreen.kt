package com.neb.ians.ui.resources

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.db.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import com.neb.ians.ui.components.ChipRow
import com.neb.ians.ui.components.NebSearchField

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourcesScreen(
    onBack: () -> Unit,
    onOpenResource: (String) -> Unit,
    vm: ResourcesViewModel = hiltViewModel(),
) {
    val filter by vm.filter.collectAsStateWithLifecycle()
    val items by vm.results.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Library") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            NebSearchField(
                value = filter.query,
                onValueChange = vm::setQuery,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
            )
            ChipRow(
                items = Subject.values().toList(),
                selected = filter.subject,
                label = { it.display },
                onSelect = vm::setSubject,
                modifier = Modifier.padding(vertical = 4.dp),
            )
            ChipRow(
                items = Grade.values().toList(),
                selected = filter.grade,
                label = { it.display },
                onSelect = vm::setGrade,
                modifier = Modifier.padding(vertical = 4.dp),
            )
            ChipRow(
                items = ResourceType.values().toList(),
                selected = filter.type,
                label = { it.display },
                onSelect = vm::setType,
                modifier = Modifier.padding(vertical = 4.dp, horizontal = 0.dp),
            )
            LazyColumn(
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                items(items, key = { it.id }) { r ->
                    ResourceRow(
                        item = r,
                        onClick = { onOpenResource(r.id) },
                        onFavorite = { vm.toggleFavorite(r.id) },
                    )
                }
                if (items.isEmpty()) {
                    item {
                        Text(
                            "No matches yet. Try clearing filters.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(top = 32.dp).fillMaxWidth(),
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ResourceRow(
    item: ResourceEntity,
    onClick: () -> Unit,
    onFavorite: () -> Unit,
) {
    Surface(
        onClick = onClick,
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceVariant,
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
    ) {
        Row(
            modifier = Modifier.padding(14.dp).fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(
                Icons.Outlined.PictureAsPdf,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(28.dp),
            )
            Column(
                modifier = Modifier.padding(start = 12.dp).weight(1f),
            ) {
                Text(item.title, style = MaterialTheme.typography.titleSmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
                Text(
                    "${Subject.fromName(item.subject)?.display ?: item.subject} • ${Grade.fromName(item.grade)?.display ?: item.grade} • ${ResourceType.fromName(item.type)?.display ?: item.type}",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            IconButton(onClick = onFavorite) {
                Icon(
                    if (item.isFavorite) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder,
                    contentDescription = "Bookmark",
                    tint = if (item.isFavorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}
