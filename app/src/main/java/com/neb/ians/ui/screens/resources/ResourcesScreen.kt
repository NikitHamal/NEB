package com.neb.ians.ui.screens.resources

import androidx.compose.animation.AnimatedVisibility
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.FilterList
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neb.ians.data.SampleData
import com.neb.ians.data.local.entity.ResourceEntity

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourcesScreen(
    onOpenResource: (Long) -> Unit,
    onNavigateToSearch: () -> Unit,
    viewModel: ResourcesViewModel = viewModel(),
) {
    val resources by viewModel.filteredResources.collectAsState()
    val selectedSubject by viewModel.selectedSubject.collectAsState()
    val selectedGrade by viewModel.selectedGrade.collectAsState()
    val selectedType by viewModel.selectedType.collectAsState()
    var showFilters by rememberSaveable { mutableStateOf(false) }

    Column(modifier = Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text("Resources") },
            actions = {
                IconButton(onClick = onNavigateToSearch) {
                    Icon(Icons.Filled.Search, contentDescription = "Search")
                }
                IconButton(onClick = { showFilters = !showFilters }) {
                    Icon(Icons.Filled.FilterList, contentDescription = "Filter")
                }
            },
        )

        AnimatedVisibility(visible = showFilters) {
            Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                Text(
                    "Subject",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    contentPadding = PaddingValues(vertical = 4.dp),
                ) {
                    item {
                        FilterChip(
                            selected = selectedSubject.isEmpty(),
                            onClick = { viewModel.setSubject("") },
                            label = { Text("All") },
                        )
                    }
                    items(SampleData.subjects) { subject ->
                        FilterChip(
                            selected = selectedSubject == subject,
                            onClick = { viewModel.setSubject(subject) },
                            label = { Text(subject) },
                        )
                    }
                }

                Spacer(Modifier.height(4.dp))
                Text(
                    "Grade",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    contentPadding = PaddingValues(vertical = 4.dp),
                ) {
                    item {
                        FilterChip(
                            selected = selectedGrade.isEmpty(),
                            onClick = { viewModel.setGrade("") },
                            label = { Text("All") },
                        )
                    }
                    items(SampleData.grades) { grade ->
                        FilterChip(
                            selected = selectedGrade == grade,
                            onClick = { viewModel.setGrade(grade) },
                            label = { Text(grade) },
                        )
                    }
                }

                Spacer(Modifier.height(4.dp))
                Text(
                    "Type",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    contentPadding = PaddingValues(vertical = 4.dp),
                ) {
                    item {
                        FilterChip(
                            selected = selectedType.isEmpty(),
                            onClick = { viewModel.setType("") },
                            label = { Text("All") },
                        )
                    }
                    items(SampleData.resourceTypes) { type ->
                        FilterChip(
                            selected = selectedType == type,
                            onClick = { viewModel.setType(type) },
                            label = { Text(type) },
                        )
                    }
                }
                Spacer(Modifier.height(8.dp))
            }
        }

        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            items(resources, key = { it.id }) { resource ->
                ResourceListItem(
                    resource = resource,
                    onClick = { onOpenResource(resource.id) },
                )
            }

            if (resources.isEmpty()) {
                item {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                    ) {
                        Text(
                            "No resources found",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        Text(
                            "Try adjusting your filters",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ResourceListItem(
    resource: ResourceEntity,
    onClick: () -> Unit,
) {
    Surface(
        onClick = onClick,
        shape = MaterialTheme.shapes.medium,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(
                Icons.Filled.Folder,
                contentDescription = null,
                modifier = Modifier.size(40.dp),
                tint = MaterialTheme.colorScheme.primary,
            )
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    resource.title,
                    style = MaterialTheme.typography.titleSmall,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Spacer(Modifier.height(2.dp))
                Text(
                    "${resource.subject} • ${resource.grade}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.height(4.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Surface(
                        shape = MaterialTheme.shapes.small,
                        color = MaterialTheme.colorScheme.tertiaryContainer,
                    ) {
                        Text(
                            resource.type,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onTertiaryContainer,
                        )
                    }
                    Text(
                        formatFileSize(resource.fileSize),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.align(Alignment.CenterVertically),
                    )
                }
            }
        }
    }
}

private fun formatFileSize(bytes: Long): String {
    return when {
        bytes >= 1_000_000 -> "%.1f MB".format(bytes / 1_000_000.0)
        bytes >= 1_000 -> "%.0f KB".format(bytes / 1_000.0)
        else -> "$bytes B"
    }
}
