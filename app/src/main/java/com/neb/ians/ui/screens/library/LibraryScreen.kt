package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.FilterList
import androidx.compose.material3.CircularProgressIndicator
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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import kotlinx.coroutines.flow.distinctUntilChanged
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiInteractiveCategory
import com.neb.ians.data.api.ApiInteractiveCourseSummary
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.WafWarningBanner
import com.neb.ians.ui.components.ShimmerLibraryGrid
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.WebTopBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LibraryScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onUploadClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onInteractiveCourseClick: (String) -> Unit = {},
    viewModel: LibraryViewModel = hiltViewModel(),
    interactiveViewModel: InteractiveViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val interactiveState by interactiveViewModel.uiState.collectAsStateWithLifecycle()
    var currentTab by remember { mutableStateOf("library") }
    var showFilterSheet by remember { mutableStateOf(false) }
    val hasActiveFilters = uiState.selectedSubject != null || uiState.selectedGradeLevel != null || uiState.selectedType != null
    val sheetState = rememberModalBottomSheetState()

    Scaffold(
        topBar = {
            WebTopBar(
                onSearchClick = onSearchClick,
                onNotificationsClick = onNotificationsClick,
                onProfileClick = onProfileClick,
                avatarInitial = "N"
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
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
                    IconButton(
                        onClick = { showFilterSheet = true },
                        modifier = Modifier.size(40.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.FilterList,
                            contentDescription = "Filter",
                            tint = if (hasActiveFilters) MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }

            LibraryTabs(
                currentTab = currentTab,
                onTabSelected = { currentTab = it }
            )

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
                        onLoadMore = viewModel::loadNextPage
                    )
                }
                "syllabus" -> {
                    SyllabusContent(
                        onSubjectClick = { subject ->
                            currentTab = "library"
                            viewModel.selectSubject(subject)
                        }
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
        }
    }

    if (showFilterSheet) {
        ModalBottomSheet(
            onDismissRequest = { showFilterSheet = false },
            sheetState = sheetState,
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
        ) {
            FilterSheetContent(
                uiState = uiState,
                viewModel = viewModel,
                onApply = { showFilterSheet = false }
            )
        }
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

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
private fun FilterSheetContent(
    uiState: LibraryUiState,
    viewModel: LibraryViewModel,
    onApply: () -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Filters",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                TextButton(onClick = {
                    viewModel.clearFilters()
                    onApply()
                }) {
                    Text("Clear all")
                }
            }
        }

        item {
            Text(
                text = "Subject",
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        item {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                LibraryUiState.SUBJECTS.forEach { subject ->
                    WebChip(
                        text = subject,
                        selected = uiState.selectedSubject == subject,
                        onClick = { viewModel.selectSubject(subject) }
                    )
                }
            }
        }

        item {
            Text(
                text = "Grade",
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        item {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                LibraryUiState.GRADE_LEVELS.forEach { grade ->
                    WebChip(
                        text = grade,
                        selected = uiState.selectedGradeLevel == grade,
                        onClick = { viewModel.selectGradeLevel(grade) }
                    )
                }
            }
        }

        item {
            Text(
                text = "Type",
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        item {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                LibraryUiState.TYPES.forEach { type ->
                    WebChip(
                        text = type,
                        selected = uiState.selectedType == type,
                        onClick = { viewModel.selectType(type) }
                    )
                }
            }
        }

        item { Spacer(modifier = Modifier.height(16.dp)) }
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
    onLoadMore: () -> Unit
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

@Composable
private fun SyllabusContent(
    onSubjectClick: (String) -> Unit
) {
    val leftSubjects = remember { LibraryUiState.SUBJECTS.filterIndexed { index, _ -> index % 2 == 0 } }
    val rightSubjects = remember { LibraryUiState.SUBJECTS.filterIndexed { index, _ -> index % 2 == 1 } }
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(count = LibraryUiState.GRADE_LEVELS.size, key = { LibraryUiState.GRADE_LEVELS[it] }) { index ->
            val grade = LibraryUiState.GRADE_LEVELS[index]
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = WebPanelShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            painter = painterResource(id = R.drawable.ic_school),
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(22.dp)
                        )
                        Spacer(modifier = Modifier.size(8.dp))
                        Text(
                            text = grade,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.weight(1f)
                        )
                        Text(
                            text = "${LibraryUiState.SUBJECTS.size} subjects",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.weight(1f)) {
                            leftSubjects.forEach { subject ->
                                SyllabusSubjectChip(subject = subject, onClick = { onSubjectClick(subject) })
                            }
                        }
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.weight(1f)) {
                            rightSubjects.forEach { subject ->
                                SyllabusSubjectChip(subject = subject, onClick = { onSubjectClick(subject) })
                            }
                        }
                    }
                }
            }
        }
        item(key = "bottom_spacer") { Spacer(modifier = Modifier.height(92.dp)) }
    }
}

@Composable
private fun SyllabusSubjectChip(subject: String, onClick: () -> Unit) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Text(
            text = subject,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
private fun InteractiveContent(
    state: InteractiveUiState,
    onCourseClick: (String) -> Unit,
    onRetry: () -> Unit
) {
    when {
        state.isLoading -> {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(3) {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        shape = WebPanelShape,
                        color = MaterialTheme.colorScheme.surfaceContainerLowest,
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(120.dp)
                        ) {
                            CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                        }
                    }
                }
            }
        }
        state.error != null -> {
            ErrorCard(
                message = state.error ?: "Failed to load interactive content",
                onRetry = onRetry,
                modifier = Modifier.padding(16.dp)
            )
        }
        state.categories.isEmpty() -> {
            WebEmptyState(
                title = "No interactive content yet",
                message = "Interactive simulations will appear here.",
                icon = painterResource(id = R.drawable.ic_document),
                modifier = Modifier.padding(16.dp)
            )
        }
        else -> {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                state.categories.forEach { category ->
                    if (category.courses.isNotEmpty()) {
                        item(key = "cat_${category.key}") {
                            InteractiveCategorySection(
                                category = category,
                                onCourseClick = onCourseClick
                            )
                        }
                    }
                }
                item(key = "bottom_spacer") { Spacer(modifier = Modifier.height(92.dp)) }
            }
        }
    }
}

@Composable
private fun InteractiveCategorySection(
    category: ApiInteractiveCategory,
    onCourseClick: (String) -> Unit
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = category.label,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = "${category.courses.size} course${if (category.courses.size != 1) "s" else ""}",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        if (category.blurb.isNotBlank()) {
            Text(
                text = category.blurb,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.padding(bottom = 8.dp)
            )
        }
        val scrollState = rememberScrollState()
        Row(
            modifier = Modifier.horizontalScroll(scrollState),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            category.courses.forEach { course ->
                InteractiveCourseCard(
                    course = course,
                    categoryColor = category.color,
                    onClick = { onCourseClick(course.slug) }
                )
            }
        }
    }
}

@Composable
private fun InteractiveCourseCard(
    course: ApiInteractiveCourseSummary,
    categoryColor: String,
    onClick: () -> Unit
) {
    val cardColor = try {
        Color(android.graphics.Color.parseColor(categoryColor))
    } catch (_: Exception) {
        MaterialTheme.colorScheme.primary
    }
    val surfaceColor = MaterialTheme.colorScheme.surfaceContainerLowest
    Surface(
        modifier = Modifier
            .width(220.dp)
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        color = surfaceColor,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Surface(
                shape = WebPillShape,
                color = cardColor.copy(alpha = 0.12f),
                modifier = Modifier.align(Alignment.Start)
            ) {
                Text(
                    text = course.level.ifBlank { "All levels" },
                    style = MaterialTheme.typography.labelSmall,
                    color = cardColor,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = course.title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (course.tagline.isNotBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = course.tagline,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "${course.lessonCount} lesson${if (course.lessonCount != 1) "s" else ""}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                if (course.totalMinutes > 0) {
                    Text(
                        text = "\u00B7",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f)
                    )
                    Text(
                        text = "${course.totalMinutes} min",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
            }
        }
    }
}