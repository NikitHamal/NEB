package com.neb.ians.ui.screens.library

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
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.ShimmerLibraryGrid
import com.neb.ians.ui.components.WebResourceCard

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
                    Text(
                        text = "Library",
                        fontWeight = FontWeight.Bold
                    )
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
                            columns = GridCells.Fixed(2),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(uiState.resources, key = { it.id }) { resource ->
                                WebResourceCard(
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
