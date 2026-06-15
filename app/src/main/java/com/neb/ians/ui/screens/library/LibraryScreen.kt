package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.border
import androidx.compose.foundation.background
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
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.FilterList
import androidx.compose.material.icons.outlined.ExpandMore
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
                    WebOutlinedButton(
                        text = "Upload",
                        onClick = onUploadClick,
                        modifier = Modifier.heightIn(min = 40.dp)
                    )
                    WebOutlinedButton(
                        text = if (hasActiveFilters) "Filters on" else "Filters",
                        onClick = { showFilterSheet = true },
                        modifier = Modifier.heightIn(min = 40.dp),
                        imageVector = Icons.Outlined.FilterList
                    )
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
                        uiState = uiState,
                        onRetry = { viewModel.loadSyllabusCategories() },
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
    uiState: LibraryUiState,
    onRetry: () -> Unit,
    onSubjectClick: (String) -> Unit
) {
    val categories = uiState.syllabusCategories.ifEmpty {
        LibraryUiState.GRADE_LEVELS.mapIndexed { index, grade ->
            ApiSyllabusCategory(
                grade = grade.replace("Grade", "Class"),
                order = index,
                subjects = LibraryUiState.SUBJECTS.map { ApiSyllabusSubject(name = it) }
            )
        }
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item(key = "syllabus_intro") {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = WebPanelShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(44.dp)
                            .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.10f), WebPillShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            painter = painterResource(id = R.drawable.ic_school),
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(22.dp)
                        )
                    }
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "NEB syllabus by class",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.ExtraBold
                        )
                        Text(
                            text = "Browse class-wise NEB subjects and jump to matching library resources.",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 2,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    if (uiState.isSyllabusLoading) {
                        CircularProgressIndicator(modifier = Modifier.size(22.dp), strokeWidth = 2.dp)
                    }
                }
            }
        }

        if (uiState.syllabusError != null) {
            item(key = "syllabus_error") {
                ErrorCard(
                    message = "Using cached syllabus while the latest syllabus loads.",
                    onRetry = onRetry
                )
            }
        }

        items(count = categories.size, key = { categories[it].grade }) { index ->
            SyllabusAccordionCard(
                category = categories[index],
                initiallyExpanded = index == 0,
                onSubjectClick = onSubjectClick
            )
        }
        item(key = "bottom_spacer") { Spacer(modifier = Modifier.height(92.dp)) }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SyllabusAccordionCard(
    category: ApiSyllabusCategory,
    initiallyExpanded: Boolean,
    onSubjectClick: (String) -> Unit
) {
    var expanded by remember(category.grade) { mutableStateOf(initiallyExpanded) }
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { expanded = !expanded }
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .padding(horizontal = 16.dp, vertical = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Icon(
                    painter = painterResource(id = R.drawable.ic_book),
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = category.grade.ifBlank { "Syllabus" },
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.ExtraBold,
                    modifier = Modifier.weight(1f),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.primary.copy(alpha = 0.10f)) {
                    Text(
                        text = "${category.subjects.size} subjects",
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp)
                    )
                }
                Icon(
                    imageVector = Icons.Outlined.ExpandMore,
                    contentDescription = if (expanded) "Collapse" else "Expand",
                    modifier = Modifier.rotate(if (expanded) 180f else 0f),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (expanded) {
                FlowRow(
                    modifier = Modifier.padding(14.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    category.subjects.forEach { subject ->
                        SyllabusSubjectChip(
                            subject = subject.name,
                            onClick = { onSubjectClick(subject.name) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun SyllabusSubjectChip(subject: String, onClick: () -> Unit) {
    Surface(
        modifier = Modifier.clickable(onClick = onClick),
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Text(
            text = subject,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurface,
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
                                .height(132.dp)
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
                message = "Interactive lessons and simulations will appear here.",
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
                item(key = "interactive_hero") {
                    InteractiveHeroCard(courseCount = state.categories.sumOf { it.courses.size })
                }
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
private fun InteractiveHeroCard(courseCount: Int) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.primaryContainer,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    Brush.linearGradient(
                        listOf(
                            MaterialTheme.colorScheme.primary.copy(alpha = 0.16f),
                            MaterialTheme.colorScheme.tertiary.copy(alpha = 0.08f)
                        )
                    )
                )
                .padding(18.dp)
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(
                    text = "Interactive learning",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
                Text(
                    text = "Explore visual lessons, simulations and guided practice grouped by topic.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.82f)
                )
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.surface.copy(alpha = 0.82f)) {
                    Text(
                        text = "$courseCount live courses",
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun InteractiveCategorySection(
    category: ApiInteractiveCategory,
    onCourseClick: (String) -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                val accent = parseWebColor(category.color)
                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .background(accent.copy(alpha = 0.12f), WebPanelShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = category.icon.ifBlank { "*" },
                        style = MaterialTheme.typography.titleLarge
                    )
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = category.label,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.ExtraBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    if (category.blurb.isNotBlank()) {
                        Text(
                            text = category.blurb,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 2,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
                Text(
                    text = "${category.courses.size}",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = accent
                )
            }
            Spacer(modifier = Modifier.height(14.dp))
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
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
}

@Composable
private fun InteractiveCourseCard(
    course: ApiInteractiveCourseSummary,
    categoryColor: String,
    onClick: () -> Unit
) {
    val accent = parseWebColor(course.color.ifBlank { categoryColor })
    Surface(
        modifier = Modifier
            .widthIn(min = 160.dp, max = 360.dp)
            .fillMaxWidth(0.48f)
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Box(
                    modifier = Modifier
                        .size(42.dp)
                        .background(accent.copy(alpha = 0.12f), WebPanelShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = course.icon.ifBlank { "*" }, style = MaterialTheme.typography.titleMedium)
                }
                Surface(shape = WebPillShape, color = accent.copy(alpha = 0.12f)) {
                    Text(
                        text = course.level.ifBlank { "All levels" },
                        style = MaterialTheme.typography.labelSmall,
                        color = accent,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = course.title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.ExtraBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (course.tagline.isNotBlank()) {
                Spacer(modifier = Modifier.height(5.dp))
                Text(
                    text = course.tagline,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Spacer(modifier = Modifier.height(12.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "${course.lessonCount} lesson${if (course.lessonCount != 1) "s" else ""}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1
                )
                if (course.totalMinutes > 0) {
                    Text(
                        text = "${course.totalMinutes} min",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1
                    )
                }
            }
        }
    }
}

private fun parseWebColor(raw: String): Color {
    return try {
        Color(android.graphics.Color.parseColor(raw))
    } catch (_: Exception) {
        Color(0xFF1B6EF3)
    }
}
