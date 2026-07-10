package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.border
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.CloudUpload
import androidx.compose.material.icons.outlined.FilterList
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.ContactSupport
import androidx.compose.material.icons.outlined.Inventory2
import androidx.compose.ui.draw.drawBehind
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.launch
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiInteractiveCategory
import com.neb.ians.data.api.ApiInteractiveCourseSummary
import com.neb.ians.data.api.ApiSyllabusSubject
import com.neb.ians.data.api.ApiSyllabusCategory
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.WafWarningBanner
import com.neb.ians.ui.components.ShimmerLibraryGrid
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState

import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.getMaterialIcon

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LibraryScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onUploadClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onInteractiveCourseClick: (String) -> Unit = {},
    onSyllabusDetailChromeChanged: (Boolean) -> Unit = {},
    onRequestResourceClick: () -> Unit = {},
    viewModel: LibraryViewModel = hiltViewModel(),
    interactiveViewModel: InteractiveViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val interactiveState by interactiveViewModel.uiState.collectAsStateWithLifecycle()
    var currentTab by rememberSaveable { mutableStateOf("library") }
    var showFilterSheet by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }
    val hasActiveFilters = uiState.selectedSubject != null || uiState.selectedGradeLevel != null || uiState.selectedType != null
    val isSyllabusDetailMode = currentTab == "syllabus" && (
        uiState.selectedSyllabusDetail != null ||
            uiState.isSyllabusSubjectLoading ||
            uiState.selectedSyllabusGradeSlug != null ||
            uiState.selectedSyllabusSubjectSlug != null
        )

    LaunchedEffect(isSyllabusDetailMode) {
        onSyllabusDetailChromeChanged(isSyllabusDetailMode)
    }
    DisposableEffect(Unit) {
        onDispose { onSyllabusDetailChromeChanged(false) }
    }

    Scaffold(
        topBar = {
            if (!isSyllabusDetailMode) {
                WebTopBar(
                    onSearchClick = onSearchClick,
                    onNotificationsClick = onNotificationsClick,
                    onProfileClick = onProfileClick,
                    avatarInitial = "N"
                )
            }
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        PullToRefreshBox(
            isRefreshing = isRefreshing,
            onRefresh = {
                scope.launch {
                    isRefreshing = true
                    viewModel.refresh()
                    isRefreshing = false
                }
            },
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
        ) {
            if (!isSyllabusDetailMode) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = when (currentTab) {
                                "library" -> "Digital Library"
                                "syllabus" -> "Syllabus"
                                else -> "Interactive"
                            },
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.ExtraBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    if (currentTab == "library") {
                        Surface(
                            shape = CircleShape,
                            color = Color.Transparent,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                            modifier = Modifier.size(40.dp)
                        ) {
                            IconButton(
                                onClick = onUploadClick,
                                modifier = Modifier.size(40.dp)
                            ) {
                                Icon(
                                    Icons.Outlined.CloudUpload,
                                    contentDescription = "Upload",
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                        Surface(
                            shape = CircleShape,
                            color = if (hasActiveFilters) MaterialTheme.colorScheme.primaryContainer else Color.Transparent,
                            border = BorderStroke(1.dp, if (hasActiveFilters) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline),
                            modifier = Modifier.size(40.dp)
                        ) {
                            IconButton(
                                onClick = { showFilterSheet = true },
                                modifier = Modifier.size(40.dp)
                            ) {
                                Icon(
                                    Icons.Outlined.FilterList,
                                    contentDescription = "Filters",
                                    tint = if (hasActiveFilters) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                    }
                }

                LibraryTabs(
                    currentTab = currentTab,
                    onTabSelected = { currentTab = it }
                )
            }

            when (currentTab) {
                "library" -> {
                    if (hasActiveFilters) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 4.dp),
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            uiState.selectedSubject?.let {
                                ActiveFilterChip(label = it, onRemove = { viewModel.selectSubject(it) })
                            }
                            uiState.selectedGradeLevel?.let {
                                ActiveFilterChip(label = it, onRemove = { viewModel.selectGradeLevel(it) })
                            }
                            uiState.selectedType?.let {
                                ActiveFilterChip(label = it, onRemove = { viewModel.selectType(it) })
                            }
                            TextButton(onClick = viewModel::clearFilters) {
                                Text("Clear all", style = MaterialTheme.typography.labelSmall)
                            }
                        }
                    }
                    LibraryContent(
                        uiState = uiState,
                        hasActiveFilters = hasActiveFilters,
                        onResourceClick = onResourceClick,
                        onRetry = { viewModel.refresh() },
                        onSortSelected = viewModel::selectSort,
                        onLoadMore = viewModel::loadNextPage,
                        onRequestResourceClick = onRequestResourceClick
                    )
                }
                "syllabus" -> {
                    SyllabusContent(
                        uiState = uiState,
                        onRetry = { viewModel.loadSyllabusCategories() },
                        onOpenSubject = viewModel::openSyllabusSubject,
                        onCloseSubject = viewModel::closeSyllabusSubject,
                        onSwitchGrade = viewModel::switchSyllabusGrade,
                        onSwitchSubject = viewModel::switchSyllabusSubject,
                        onResourceClick = onResourceClick
                    )
                }
                "interactive" -> {
                    InteractiveContent(
                        state = interactiveState,
                        onCourseClick = onInteractiveCourseClick,
                        onRetry = { interactiveViewModel.loadCategories() }
                    )
                }
            }
        } // end Column
        } // end PullToRefreshBox
    }

    if (showFilterSheet) {
        com.neb.ians.ui.components.FilterDialog(
            onDismissRequest = { showFilterSheet = false },
            selectedSubject = uiState.selectedSubject,
            selectedGradeLevel = uiState.selectedGradeLevel,
            selectedType = uiState.selectedType,
            subjects = LibraryUiState.SUBJECTS,
            gradeLevels = LibraryUiState.GRADE_LEVELS,
            types = LibraryUiState.TYPES,
            onSubjectSelected = viewModel::selectSubject,
            onGradeLevelSelected = viewModel::selectGradeLevel,
            onTypeSelected = viewModel::selectType,
            onClearAll = viewModel::clearFilters,
            onApply = { showFilterSheet = false }
        )
    }
}

@Composable
private fun ActiveFilterChip(label: String, onRemove: () -> Unit) {
    Surface(
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.primaryContainer,
        modifier = Modifier.clickable { onRemove() }
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                fontWeight = FontWeight.Medium
            )
        }
    }
}

@Composable
private fun LibraryTabs(
    currentTab: String,
    onTabSelected: (String) -> Unit
) {
    val tabs = listOf("library" to "Library", "syllabus" to "Syllabus", "interactive" to "Interactive")
    val scrollState = rememberScrollState()
    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(scrollState),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            tabs.forEach { (key, label) ->
                TabButton(
                    text = label,
                    selected = currentTab == key,
                    onClick = { onTabSelected(key) }
                )
            }
        }
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
    }
}

@Composable
private fun TabButton(text: String, selected: Boolean, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.labelLarge,
            fontWeight = FontWeight.Bold,
            color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(modifier = Modifier.height(8.dp))
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .height(3.dp),
            color = if (selected) MaterialTheme.colorScheme.primary else Color.Transparent,
            shape = WebPillShape
        ) {}
    }
}

@Composable
private fun LibraryContent(
    uiState: LibraryUiState,
    hasActiveFilters: Boolean,
    onResourceClick: (String) -> Unit,
    onRetry: () -> Unit,
    onSortSelected: (String) -> Unit,
    onLoadMore: () -> Unit,
    onRequestResourceClick: () -> Unit
) {
    when {
        uiState.isLoading -> ShimmerLibraryGrid()
        uiState.error != null && uiState.resources.isEmpty() -> {
            ErrorCard(
                message = uiState.error ?: "Something went wrong",
                onRetry = onRetry,
                modifier = Modifier.padding(16.dp)
            )
        }
        uiState.resources.isEmpty() -> {
            WebEmptyState(
                title = "No resources found",
                message = if (hasActiveFilters) "Try adjusting your filters." else "Resources will appear here once available.",
                icon = painterResource(id = R.drawable.ic_document),
                modifier = Modifier.padding(16.dp)
            )
        }
        else -> {
            Column(modifier = Modifier.fillMaxSize()) {
                if (uiState.error != null) {
                    if (uiState.error == ApiErrorMapper.WAF_ERROR_MESSAGE) {
                        WafWarningBanner(modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp))
                    } else {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = onRetry,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                        )
                    }
                }
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    shape = WebPanelShape,
                    color = MaterialTheme.colorScheme.surfaceContainerLowest,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Row(
                        modifier = Modifier.padding(start = 14.dp, top = 4.dp, end = 8.dp, bottom = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val total = uiState.totalCount.coerceAtLeast(uiState.resources.size)
                        Text(
                            text = "Showing 1\u2013${uiState.resources.size} of $total resources",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.weight(1f),
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        LibrarySortDropdown(
                            sort = uiState.sort,
                            onSortSelected = onSortSelected
                        )
                    }
                }

                val gridState = rememberLazyGridState()
                LaunchedEffect(gridState) {
                    snapshotFlow {
                        val layoutInfo = gridState.layoutInfo
                        val lastVisible = layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: -1
                        lastVisible to layoutInfo.totalItemsCount
                    }
                        .distinctUntilChanged()
                        .collect { (lastVisible, total) ->
                            if (total > 0 && lastVisible >= total - 4 && uiState.error != ApiErrorMapper.WAF_ERROR_MESSAGE) onLoadMore()
                        }
                }

                LazyVerticalGrid(
                    state = gridState,
                    columns = GridCells.Adaptive(minSize = 174.dp),
                    contentPadding = PaddingValues(start = 16.dp, top = 6.dp, end = 16.dp, bottom = 110.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(uiState.resources, key = { it.id }) { resource ->
                        WebResourceCard(
                            resource = resource,
                            onClick = { onResourceClick(resource.id) },
                            minWidth = null
                        )
                    }
                    if (uiState.isLoadingMore) {
                        item(key = "loading_footer", span = { GridItemSpan(maxLineSpan) }) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 14.dp),
                                horizontalArrangement = Arrangement.Center,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                CircularProgressIndicator(modifier = Modifier.size(26.dp))
                            }
                        }
                    } else if (!uiState.hasMore && !uiState.isLoading) {
                        item(key = "coming_soon_footer", span = { GridItemSpan(maxLineSpan) }) {
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 16.dp),
                                shape = RoundedCornerShape(16.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)
                                ),
                                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(24.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally,
                                    verticalArrangement = Arrangement.Center
                                ) {
                                    Surface(
                                        shape = CircleShape,
                                        color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f),
                                        modifier = Modifier.size(48.dp)
                                    ) {
                                        Box(contentAlignment = Alignment.Center) {
                                            Icon(
                                                imageVector = Icons.Outlined.Inventory2,
                                                contentDescription = null,
                                                tint = MaterialTheme.colorScheme.primary,
                                                modifier = Modifier.size(24.dp)
                                            )
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(12.dp))
                                    Text(
                                        text = "More coming soon",
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = "Our academic team is actively compiling new resources.",
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        textAlign = TextAlign.Center
                                    )
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Button(
                                        onClick = onRequestResourceClick,
                                        shape = WebPillShape,
                                        colors = ButtonDefaults.buttonColors(
                                            containerColor = MaterialTheme.colorScheme.primaryContainer,
                                            contentColor = MaterialTheme.colorScheme.onPrimaryContainer
                                        )
                                    ) {
                                        Icon(
                                            imageVector = Icons.Outlined.ContactSupport,
                                            contentDescription = null,
                                            modifier = Modifier.size(18.dp)
                                        )
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("Request a Resource", fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun LibrarySortDropdown(
    sort: String,
    onSortSelected: (String) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    val selectedLabel = LibraryUiState.SORT_OPTIONS.firstOrNull { it.key == sort }?.label
        ?: LibraryUiState.SORT_OPTIONS.first().label

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = it }
    ) {
        Row(
            modifier = Modifier
                .menuAnchor(MenuAnchorType.PrimaryNotEditable)
                .clickable { expanded = true }
                .padding(horizontal = 6.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = selectedLabel,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold,
                maxLines = 1
            )
            ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded)
        }
        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            LibraryUiState.SORT_OPTIONS.forEach { option ->
                DropdownMenuItem(
                    text = {
                        Text(
                            text = option.label,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = if (option.key == sort) FontWeight.Bold else FontWeight.Normal,
                            color = if (option.key == sort) {
                                MaterialTheme.colorScheme.primary
                            } else {
                                MaterialTheme.colorScheme.onSurface
                            }
                        )
                    },
                    onClick = {
                        expanded = false
                        onSortSelected(option.key)
                    }
                )
            }
        }
    }
}
