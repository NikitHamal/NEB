package com.neb.ians.ui.screens.library

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Article
import androidx.compose.material.icons.outlined.AutoStories
import androidx.compose.material.icons.outlined.Calculate
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.DownloadDone
import androidx.compose.material.icons.outlined.Eco
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Money
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Science
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Terminal
import androidx.compose.material.icons.outlined.Translate
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.local.entity.ResourceEntity

private val subjectColors = mapOf(
    "Physics" to Color(0xFF1A73E8),
    "Chemistry" to Color(0xFF188038),
    "Mathematics" to Color(0xFFE8710A),
    "Biology" to Color(0xFF9334E6),
    "English" to Color(0xFFD93025),
    "Nepali" to Color(0xFF1967D2),
    "Computer Science" to Color(0xFF185ABC),
    "Economics" to Color(0xFFE37400),
    "Accountancy" to Color(0xFF0D652D)
)

private fun getSubjectColor(subject: String): Color {
    return subjectColors[subject] ?: Color(0xFF5F6368)
}

private fun getSubjectIcon(subject: String): ImageVector {
    return when (subject) {
        "Physics" -> Icons.Outlined.Science
        "Chemistry" -> Icons.Outlined.Science
        "Mathematics" -> Icons.Outlined.Calculate
        "Biology" -> Icons.Outlined.Eco
        "English" -> Icons.Outlined.Language
        "Nepali" -> Icons.Outlined.Translate
        "Computer Science" -> Icons.Outlined.Terminal
        "Economics" -> Icons.Outlined.Money
        "Accountancy" -> Icons.Outlined.MenuBook
        else -> Icons.Outlined.Description
    }
}

private fun getTypeIcon(type: String): ImageVector {
    return when (type.lowercase()) {
        "textbook" -> Icons.Outlined.MenuBook
        "notes" -> Icons.Outlined.Article
        "past papers" -> Icons.Outlined.Description
        "guide" -> Icons.Outlined.AutoStories
        "solution" -> Icons.Outlined.School
        else -> Icons.Outlined.Description
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LibraryScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    viewModel: LibraryViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    val hasActiveFilters = uiState.selectedSubject != null ||
            uiState.selectedGradeLevel != null ||
            uiState.selectedType != null

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Library") },
                actions = {
                    IconButton(onClick = onSearchClick) {
                        Icon(
                            imageVector = Icons.Outlined.Search,
                            contentDescription = "Search"
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Filter section
            Column(
                modifier = Modifier.padding(bottom = 8.dp)
            ) {
                // Subject filter chips
                FilterChipRow(
                    label = "Subject",
                    items = uiState.subjects,
                    selectedItem = uiState.selectedSubject,
                    onItemSelected = viewModel::selectSubject
                )

                // Grade filter chips
                FilterChipRow(
                    label = "Grade",
                    items = uiState.gradeLevels,
                    selectedItem = uiState.selectedGradeLevel,
                    onItemSelected = viewModel::selectGradeLevel
                )

                // Type filter chips
                FilterChipRow(
                    label = "Type",
                    items = uiState.types,
                    selectedItem = uiState.selectedType,
                    onItemSelected = viewModel::selectType
                )

                // Clear filters button
                if (hasActiveFilters) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp),
                        horizontalArrangement = Arrangement.End
                    ) {
                        TextButton(onClick = viewModel::clearFilters) {
                            Text(
                                text = "Clear Filters",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                }
            }

            // Resource grid or empty state
            if (uiState.resources.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = "No resources found",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = if (hasActiveFilters) "Try adjusting your filters."
                            else "Resources will appear here once available.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            } else {
                LazyVerticalGrid(
                    columns = GridCells.Fixed(2),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(uiState.resources, key = { it.id }) { resource ->
                        LibraryResourceCard(
                            resource = resource,
                            onClick = { onResourceClick(resource.id) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun FilterChipRow(
    label: String,
    items: List<String>,
    selectedItem: String?,
    onItemSelected: (String?) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(start = 16.dp, end = 8.dp)
        )
        LazyRow(
            contentPadding = PaddingValues(end = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(items) { item ->
                val isSelected = selectedItem == item
                FilterChip(
                    selected = isSelected,
                    onClick = { onItemSelected(item) },
                    label = {
                        Text(
                            text = item,
                            style = MaterialTheme.typography.labelMedium
                        )
                    },
                    colors = FilterChipDefaults.filterChipColors(
                        containerColor = MaterialTheme.colorScheme.surface,
                        labelColor = MaterialTheme.colorScheme.onSurfaceVariant,
                        selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                        selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer
                    ),
                    border = FilterChipDefaults.filterChipBorder(
                        borderColor = MaterialTheme.colorScheme.outlineVariant,
                        selectedBorderColor = MaterialTheme.colorScheme.primaryContainer,
                        enabled = true,
                        selected = isSelected
                    )
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun LibraryResourceCard(
    resource: ResourceEntity,
    onClick: () -> Unit
) {
    val subjectColor = getSubjectColor(resource.subject)

    OutlinedCard(
        onClick = onClick,
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.outlinedCardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.outlinedCardElevation(
            defaultElevation = 0.dp
        ),
        border = CardDefaults.outlinedCardBorder()
    ) {
        Column {
            // Colored header area
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(88.dp)
                    .background(subjectColor.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = getSubjectIcon(resource.subject),
                    contentDescription = null,
                    modifier = Modifier.size(36.dp),
                    tint = subjectColor.copy(alpha = 0.6f)
                )
            }

            Column(
                modifier = Modifier.padding(12.dp)
            ) {
                // Title
                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    color = MaterialTheme.colorScheme.onSurface
                )

                Spacer(modifier = Modifier.height(8.dp))

                // Subject and type badges row
                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Subject badge
                    Surface(
                        shape = RoundedCornerShape(4.dp),
                        color = subjectColor.copy(alpha = 0.1f)
                    ) {
                        Text(
                            text = resource.subject,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = subjectColor,
                            maxLines = 1
                        )
                    }

                    // Type badge
                    Surface(
                        shape = RoundedCornerShape(4.dp),
                        color = MaterialTheme.colorScheme.surfaceVariant
                    ) {
                        Text(
                            text = resource.type,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                }

                Spacer(modifier = Modifier.height(6.dp))

                // Grade level and download indicator row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = resource.gradeLevel,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )

                    if (resource.isDownloaded) {
                        Icon(
                            imageVector = Icons.Outlined.DownloadDone,
                            contentDescription = "Downloaded",
                            modifier = Modifier.size(16.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }
        }
    }
}
