@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.search

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.History
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material.icons.rounded.SearchOff
import androidx.compose.material.icons.rounded.Tune
import androidx.compose.material3.ButtonGroup
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.ToggleButton
import androidx.compose.material3.ToggleButtonDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.FilterDialog
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFilterChip
import com.neb.ians.ui.components.NebChipRow
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.ShimmerSearchList
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.screens.library.LibraryUiState
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebSpatialSpec

/**
 * One field, one bank of scopes, one list.
 *
 * The old screen asked the user to read a tab strip before they had results and
 * gave a spinner while they waited. This one keeps the field as the only thing
 * on screen until there is something to show, reveals the scope bank with the
 * counts already in it, and remembers what was searched before so a repeat
 * search is a tap rather than a retype.
 */
@Composable
fun SearchScreen(
    initialQuery: String = "",
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit = {},
    onProfileClick: (String) -> Unit = {},
    onNavigateBack: () -> Unit,
    viewModel: SearchViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val focusRequester = remember { FocusRequester() }
    val keyboard = LocalSoftwareKeyboardController.current
    var showFilters by remember { mutableStateOf(false) }

    BackHandler { onNavigateBack() }

    LaunchedEffect(initialQuery) {
        if (initialQuery.isNotBlank() && uiState.query != initialQuery) {
            viewModel.onQueryChange(initialQuery)
        } else {
            runCatching { focusRequester.requestFocus() }
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface,
        topBar = {
            SearchHeader(
                state = uiState,
                focusRequester = focusRequester,
                onQueryChange = viewModel::onQueryChange,
                onSubmit = {
                    keyboard?.hide()
                    viewModel.submitQuery()
                },
                onClear = viewModel::clearSearch,
                onScopeChange = viewModel::onScopeChange,
                onNavigateBack = onNavigateBack,
                onFilterClick = { showFilters = true }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                uiState.isSearching && uiState.totalCount == 0 -> ShimmerSearchList()

                uiState.error != null -> ErrorCard(
                    message = uiState.error ?: "Search failed",
                    onRetry = viewModel::retry,
                    modifier = Modifier.padding(16.dp)
                )

                uiState.query.trim().length < SearchUiState.MIN_QUERY_LENGTH -> SearchIdleState(
                    recents = uiState.recentQueries,
                    onQueryPick = { picked ->
                        viewModel.onQueryChange(picked)
                        viewModel.submitQuery()
                        keyboard?.hide()
                    },
                    onRemoveRecent = viewModel::removeRecent,
                    onClearRecents = viewModel::clearRecents
                )

                uiState.isEmptyResult -> NebEmptyState(
                    icon = Icons.Rounded.SearchOff,
                    title = "Nothing for “${uiState.query.trim()}”",
                    subtitle = if (uiState.activeFilterCount > 0) {
                        "Try different words, or clear the ${uiState.activeFilterCount} filter" +
                            if (uiState.activeFilterCount > 1) "s." else "."
                    } else {
                        "Try fewer words, or check the spelling."
                    },
                    modifier = Modifier.align(Alignment.Center)
                )

                else -> SearchResultsList(
                    state = uiState,
                    onResourceClick = onResourceClick,
                    onPostClick = onPostClick,
                    onProfileClick = onProfileClick,
                    onScopeChange = viewModel::onScopeChange
                )
            }
        }
    }

    if (showFilters) {
        FilterDialog(
            onDismissRequest = { showFilters = false },
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
            onApply = { showFilters = false }
        )
    }
}

@Composable
private fun SearchHeader(
    state: SearchUiState,
    focusRequester: FocusRequester,
    onQueryChange: (String) -> Unit,
    onSubmit: () -> Unit,
    onClear: () -> Unit,
    onScopeChange: (SearchScope) -> Unit,
    onNavigateBack: () -> Unit,
    onFilterClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surface)
            .windowInsetsPadding(WindowInsets.statusBars)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 4.dp, end = 12.dp, top = 6.dp, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onNavigateBack) {
                Icon(
                    imageVector = Icons.AutoMirrored.Rounded.ArrowBack,
                    contentDescription = "Back",
                    tint = MaterialTheme.colorScheme.onSurface
                )
            }
            SearchField(
                query = state.query,
                activeFilterCount = state.activeFilterCount,
                focusRequester = focusRequester,
                onQueryChange = onQueryChange,
                onSubmit = onSubmit,
                onClear = onClear,
                onFilterClick = onFilterClick,
                modifier = Modifier.weight(1f)
            )
        }

        AnimatedVisibility(
            visible = state.hasSearched && state.totalCount > 0,
            enter = expandVertically(nebSpatialSpec()) + fadeIn(nebEffectsSpec()),
            exit = shrinkVertically(nebSpatialSpec()) + fadeOut(nebEffectsSpec())
        ) {
            SearchScopeBank(
                state = state,
                onScopeChange = onScopeChange,
                modifier = Modifier.padding(start = 14.dp, end = 14.dp, bottom = 10.dp)
            )
        }
    }
}

@Composable
private fun SearchField(
    query: String,
    activeFilterCount: Int,
    focusRequester: FocusRequester,
    onQueryChange: (String) -> Unit,
    onSubmit: () -> Unit,
    onClear: () -> Unit,
    onFilterClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val corner by animateDpAsState(
        targetValue = if (focused) 18.dp else 26.dp,
        animationSpec = nebFastSpatialSpec(),
        label = "search_field_corner"
    )
    val container by animateColorAsState(
        targetValue = if (focused) {
            MaterialTheme.colorScheme.surfaceContainerHighest
        } else {
            MaterialTheme.colorScheme.surfaceContainerHigh
        },
        animationSpec = nebEffectsSpec(),
        label = "search_field_container"
    )

    Row(
        modifier = modifier
            .heightIn(min = 52.dp)
            .clip(RoundedCornerShape(corner))
            .background(container)
            .padding(start = 16.dp, end = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Rounded.Search,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(20.dp)
        )
        Box(
            modifier = Modifier
                .weight(1f)
                .padding(start = 12.dp, end = 6.dp),
            contentAlignment = Alignment.CenterStart
        ) {
            if (query.isEmpty()) {
                Text(
                    text = "Search notes, posts, people",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            BasicTextField(
                value = query,
                onValueChange = onQueryChange,
                singleLine = true,
                textStyle = MaterialTheme.typography.bodyLarge.copy(
                    color = MaterialTheme.colorScheme.onSurface
                ),
                cursorBrush = SolidColor(MaterialTheme.colorScheme.onSurface),
                interactionSource = interaction,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(onSearch = { onSubmit() }),
                modifier = Modifier
                    .fillMaxWidth()
                    .focusRequester(focusRequester)
            )
        }
        AnimatedVisibility(
            visible = query.isNotEmpty(),
            enter = fadeIn(nebEffectsSpec()),
            exit = fadeOut(nebEffectsSpec())
        ) {
            IconButton(onClick = onClear, modifier = Modifier.size(40.dp)) {
                Icon(
                    imageVector = Icons.Rounded.Close,
                    contentDescription = "Clear search",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
        FilterAction(count = activeFilterCount, onClick = onFilterClick)
    }
}

@Composable
private fun FilterAction(count: Int, onClick: () -> Unit) {
    val active = count > 0
    val container by animateColorAsState(
        targetValue = if (active) {
            MaterialTheme.colorScheme.onSurface
        } else {
            MaterialTheme.colorScheme.surfaceContainerLowest
        },
        animationSpec = nebEffectsSpec(),
        label = "search_filter_container"
    )
    val content by animateColorAsState(
        targetValue = if (active) {
            MaterialTheme.colorScheme.surface
        } else {
            MaterialTheme.colorScheme.onSurfaceVariant
        },
        animationSpec = nebEffectsSpec(),
        label = "search_filter_content"
    )

    Row(
        modifier = Modifier
            .heightIn(min = 40.dp)
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(50))
            .background(container)
            .padding(horizontal = if (active) 12.dp else 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = Icons.Rounded.Tune,
            contentDescription = "Filters",
            tint = content,
            modifier = Modifier.size(18.dp)
        )
        if (active) {
            Text(
                text = count.toString(),
                style = MaterialTheme.typography.labelLargeEmphasized,
                color = content
            )
        }
    }
}

@Composable
private fun SearchScopeBank(
    state: SearchUiState,
    onScopeChange: (SearchScope) -> Unit,
    modifier: Modifier = Modifier
) {
    val scopes = remember { SearchScope.entries.toList() }
    val interactions = remember { scopes.map { MutableInteractionSource() } }
    val colors = ToggleButtonDefaults.toggleButtonColors(
        containerColor = Color.Transparent,
        contentColor = MaterialTheme.colorScheme.onSurfaceVariant,
        checkedContainerColor = MaterialTheme.colorScheme.onSurface,
        checkedContentColor = MaterialTheme.colorScheme.surface
    )

    ButtonGroup(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(3.dp),
        horizontalArrangement = Arrangement.spacedBy(0.dp)
    ) {
        scopes.forEachIndexed { index, scope ->
            val count = state.countFor(scope)
            ToggleButton(
                checked = state.scope == scope,
                onCheckedChange = { onScopeChange(scope) },
                modifier = Modifier
                    .weight(1f)
                    .heightIn(min = 40.dp)
                    .animateWidth(interactions[index]),
                shapes = ToggleButtonDefaults.shapes(),
                colors = colors,
                interactionSource = interactions[index],
                contentPadding = PaddingValues(horizontal = 6.dp, vertical = 8.dp)
            ) {
                Text(
                    text = if (count > 0) "${scope.label} $count" else scope.label,
                    style = MaterialTheme.typography.labelMediumEmphasized,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

@Composable
private fun SearchIdleState(
    recents: List<String>,
    onQueryPick: (String) -> Unit,
    onRemoveRecent: (String) -> Unit,
    onClearRecents: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 16.dp)
            .padding(top = 10.dp, bottom = 32.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        if (recents.isNotEmpty()) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                NebSectionLabel(text = "Recent", modifier = Modifier.weight(1f))
                Text(
                    text = "Clear",
                    style = MaterialTheme.typography.labelLargeEmphasized,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier
                        .nebPressable(onClick = onClearRecents)
                        .clip(RoundedCornerShape(50))
                        .padding(horizontal = 10.dp, vertical = 6.dp)
                )
            }
            recents.forEach { entry ->
                RecentQueryRow(
                    query = entry,
                    onClick = { onQueryPick(entry) },
                    onRemove = { onRemoveRecent(entry) }
                )
            }
            Spacer(modifier = Modifier.height(10.dp))
        }

        NebSectionLabel(text = "Popular right now")
        NebChipRow {
            SearchUiState.SUGGESTIONS.forEach { suggestion ->
                NebFilterChip(
                    label = suggestion,
                    selected = false,
                    onClick = { onQueryPick(suggestion) }
                )
            }
        }
    }
}

@Composable
private fun RecentQueryRow(
    query: String,
    onClick: () -> Unit,
    onRemove: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 52.dp)
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(18.dp))
            .padding(start = 4.dp, end = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Rounded.History,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(19.dp)
        )
        Spacer(modifier = Modifier.width(14.dp))
        Text(
            text = query,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        IconButton(onClick = onRemove, modifier = Modifier.size(40.dp)) {
            Icon(
                imageVector = Icons.Rounded.Close,
                contentDescription = "Remove “$query” from recent searches",
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(16.dp)
            )
        }
    }
}
