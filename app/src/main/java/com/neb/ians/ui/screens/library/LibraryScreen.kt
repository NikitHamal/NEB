@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

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
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.CloudUpload
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.ContactSupport
import androidx.compose.material.icons.outlined.Inventory2
import androidx.compose.material.icons.outlined.Tune
import com.neb.ians.ui.components.FilterDialog
import androidx.compose.ui.draw.drawBehind
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
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
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
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebTabRail
import androidx.compose.ui.draw.clip
import androidx.compose.material.icons.outlined.PlayLesson
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.AnimatedVisibility
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebLoader

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
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }
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

    var showFilterDialog by remember { mutableStateOf(false) }

    val activeFilterCount = (if (uiState.selectedSubject != null) 1 else 0) +
        (if (uiState.selectedGradeLevel != null) 1 else 0) +
        (if (uiState.selectedType != null) 1 else 0) +
        (if (uiState.sort != "relevant") 1 else 0)

    if (showFilterDialog) {
        FilterDialog(
            onDismissRequest = { showFilterDialog = false },
            selectedSort = uiState.sort,
            onSortSelected = viewModel::selectSort,
            selectedSubject = uiState.selectedSubject,
            selectedGradeLevel = uiState.selectedGradeLevel,
            selectedType = uiState.selectedType,
            subjects = LibraryUiState.SUBJECTS,
            gradeLevels = LibraryUiState.GRADE_LEVELS,
            types = LibraryUiState.TYPES,
            onSubjectSelected = viewModel::selectSubject,
            onGradeLevelSelected = viewModel::selectGradeLevel,
            onTypeSelected = viewModel::selectType,
            onClearAll = {
                viewModel.clearFilters()
                viewModel.selectSort("relevant")
                showFilterDialog = false
            },
            onApply = { showFilterDialog = false }
        )
    }

    Scaffold(
        topBar = {
            if (!isSyllabusDetailMode) {
            WebTopBar(
                onSearchClick = onSearchClick,
                onNotificationsClick = onNotificationsClick,
                onProfileClick = onProfileClick
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
                    viewModel.refresh().join()
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
                LibraryTabs(
                    currentTab = currentTab,
                    onTabSelected = { currentTab = it },
                    activeFilterCount = activeFilterCount,
                    onFilterClick = { showFilterDialog = true }
                )
            }

            when (currentTab) {
                "library" -> {
                    LibraryContent(
                        uiState = uiState,
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

}

@Composable
private fun LibraryTabs(
    currentTab: String,
    onTabSelected: (String) -> Unit,
    activeFilterCount: Int = 0,
    onFilterClick: () -> Unit = {}
) {
    val keys = remember { listOf("library", "syllabus", "interactive") }
    val tabs = remember {
        listOf(
            NebRailTab("Library", Icons.Outlined.Inventory2),
            NebRailTab("Syllabus", Icons.AutoMirrored.Outlined.MenuBook),
            NebRailTab("Interactive", Icons.Outlined.PlayLesson)
        )
    }
    val selected = keys.indexOf(currentTab).coerceAtLeast(0)

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(end = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        NebTabRail(
            tabs = tabs,
            selectedIndex = selected,
            onSelect = { onTabSelected(keys[it]) },
            modifier = Modifier.weight(1f)
        )
        AnimatedVisibility(visible = currentTab == "library") {
            FilterButton(activeFilterCount = activeFilterCount, onClick = onFilterClick)
        }
    }
}

@Composable
private fun FilterButton(activeFilterCount: Int, onClick: () -> Unit) {
    val active = activeFilterCount > 0
    val container by animateColorAsState(
        targetValue = if (active) {
            MaterialTheme.colorScheme.onSurface
        } else {
            MaterialTheme.colorScheme.surfaceContainerHigh
        },
        animationSpec = nebEffectsSpec(),
        label = "library_filter_bg"
    )
    val content = if (active) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurfaceVariant

    Row(
        modifier = Modifier
            .height(48.dp)
            .clip(CircleShape)
            .background(container)
            .clickable(onClick = onClick)
            .padding(horizontal = if (active) 14.dp else 13.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = Icons.Outlined.Tune,
            contentDescription = "Filters",
            modifier = Modifier.size(20.dp),
            tint = content
        )
        if (active) {
            Text(
                text = activeFilterCount.toString(),
                style = MaterialTheme.typography.labelLargeEmphasized,
                color = content
            )
        }
    }
}

@Composable
private fun LibraryContent(
    uiState: LibraryUiState,
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
                message = "Resources will appear here once available.",
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
                                NebLoader(size = NebLoaderSize.Small)
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
                                    NebButton(
                                        text = "Request a resource",
                                        onClick = onRequestResourceClick,
                                        icon = Icons.Outlined.ContactSupport,
                                        tone = NebButtonTone.Tonal
                                    )
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
