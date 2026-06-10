package com.neb.ians.ui.screens.library

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Search
import androidx.compose.ui.res.painterResource
import com.neb.ians.R
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NEBiansLogoWordmark
import com.neb.ians.ui.components.ShimmerLibraryGrid
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.theme.getSubjectTheme

private fun getSubjectIcon(subject: String): Int {
    return when (subject) {
        "Physics" -> R.drawable.ic_science
        "Chemistry" -> R.drawable.ic_science
        "Mathematics" -> R.drawable.ic_science
        "Biology" -> R.drawable.ic_science
        "English" -> R.drawable.ic_globe
        "Nepali" -> R.drawable.ic_globe
        "Computer Science" -> R.drawable.ic_science
        "Economics" -> R.drawable.ic_globe
        "Accountancy" -> R.drawable.ic_book
        else -> R.drawable.ic_document
    }
}

private fun getTypeIcon(type: String): Int {
    return when (type.lowercase()) {
        "textbook" -> R.drawable.ic_book
        "notes" -> R.drawable.ic_document
        "past papers" -> R.drawable.ic_document
        "guide" -> R.drawable.ic_book
        "solution" -> R.drawable.ic_school
        else -> R.drawable.ic_document
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
    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()

    val hasActiveFilters = uiState.selectedSubject != null ||
            uiState.selectedGradeLevel != null ||
            uiState.selectedType != null

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            LargeTopAppBar(
                title = {
                    NEBiansLogoWordmark()
                },
                actions = {
                    FilledTonalIconButton(onClick = onSearchClick) {
                        Icon(
                            imageVector = Icons.Outlined.Search,
                            contentDescription = "Search"
                        )
                    }
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.largeTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    scrolledContainerColor = MaterialTheme.colorScheme.surfaceContainer
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            if (uiState.isLoading) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                ) {
                    FilterSection(
                        hasActiveFilters = hasActiveFilters,
                        uiState = uiState,
                        viewModel = viewModel
                    )
                    ShimmerLibraryGrid()
                }
            } else if (uiState.error != null && uiState.resources.isEmpty()) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState()),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    FilterSection(
                        hasActiveFilters = hasActiveFilters,
                        uiState = uiState,
                        viewModel = viewModel
                    )
                    ErrorCard(
                        message = uiState.error ?: "Something went wrong",
                        onRetry = { viewModel.refresh() }
                    )
                }
            } else {
                Column(
                    modifier = Modifier.fillMaxSize()
                ) {
                    FilterSection(
                        hasActiveFilters = hasActiveFilters,
                        uiState = uiState,
                        viewModel = viewModel
                    )

                    if (uiState.error != null) {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = { viewModel.refresh() }
                        )
                    }

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
                            columns = GridCells.Adaptive(minSize = 164.dp),
                            contentPadding = PaddingValues(horizontal = 24.dp, vertical = 8.dp),
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
    }
}

@Composable
private fun FilterSection(
    hasActiveFilters: Boolean,
    uiState: LibraryUiState,
    viewModel: LibraryViewModel
) {
    Column(
        modifier = Modifier.padding(bottom = 8.dp)
    ) {
        FilterChipRow(
            label = "Subject",
            items = LibraryUiState.SUBJECTS,
            selectedItem = uiState.selectedSubject,
            onItemSelected = viewModel::selectSubject
        )

        FilterChipRow(
            label = "Grade",
            items = LibraryUiState.GRADE_LEVELS,
            selectedItem = uiState.selectedGradeLevel,
            onItemSelected = viewModel::selectGradeLevel
        )

        FilterChipRow(
            label = "Type",
            items = LibraryUiState.TYPES,
            selectedItem = uiState.selectedType,
            onItemSelected = viewModel::selectType
        )

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
                    .padding(vertical = 5.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(start = 24.dp, end = 8.dp)
        )
        LazyRow(
            contentPadding = PaddingValues(end = 24.dp),
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
                            style = MaterialTheme.typography.labelMedium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    },
                    shape = RoundedCornerShape(50),
                    colors = FilterChipDefaults.filterChipColors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                        labelColor = MaterialTheme.colorScheme.onSurface,
                        selectedContainerColor = MaterialTheme.colorScheme.secondaryContainer,
                        selectedLabelColor = MaterialTheme.colorScheme.onSecondaryContainer
                    ),
                    border = FilterChipDefaults.filterChipBorder(
                        borderColor = MaterialTheme.colorScheme.outlineVariant,
                        selectedBorderColor = MaterialTheme.colorScheme.secondaryContainer,
                        enabled = true,
                        selected = isSelected
                    )
                )
            }
        }
    }
}

@Composable
private fun LibraryResourceCard(
    resource: ApiResource,
    onClick: () -> Unit
) {
    WebResourceCard(resource = resource, onClick = onClick)
}
