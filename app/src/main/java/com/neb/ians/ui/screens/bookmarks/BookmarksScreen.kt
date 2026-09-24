@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.bookmarks

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebTabRail
import kotlinx.coroutines.launch
import java.util.Calendar
import java.util.concurrent.TimeUnit

// ---------------------------------------------------------------------------
// Bookmarks.
//
// A reading list, not a gallery: grouped by when it was saved, one row per
// thing, and the newest at the top where you left it. The list itself is the
// only container on the screen.
// ---------------------------------------------------------------------------

@Composable
fun BookmarksScreen(
    onNavigateBack: () -> Unit,
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: BookmarksViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val scope = rememberCoroutineScope()
    val snackbarHostState = remember { SnackbarHostState() }
    var isRefreshing by remember { mutableStateOf(false) }

    val message = uiState.message
    LaunchedEffect(message) {
        if (message == null) return@LaunchedEffect
        val canUndo = uiState.undoTarget != null
        val result = snackbarHostState.showSnackbar(
            message = message,
            actionLabel = if (canUndo) "Undo" else null,
            duration = SnackbarDuration.Short
        )
        if (result == SnackbarResult.ActionPerformed) viewModel.undoRemove() else viewModel.consumeMessage()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Bookmarks", fontWeight = FontWeight.SemiBold)
                        Text(
                            text = savedLabel(uiState.totalCount),
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = onSearchClick) {
                        Icon(Icons.Outlined.Search, contentDescription = "Search")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            BookmarkFilterRow(
                state = uiState,
                onSelect = viewModel::selectType
            )
            PullToRefreshBox(
                isRefreshing = isRefreshing,
                onRefresh = {
                    scope.launch {
                        isRefreshing = true
                        viewModel.load().join()
                        isRefreshing = false
                    }
                },
                modifier = Modifier.fillMaxSize()
            ) {
                BookmarksBody(
                    uiState = uiState,
                    onRetry = { viewModel.load() },
                    onOpen = { item ->
                        when (item.bookmark.targetType) {
                            "resource" -> onResourceClick(item.bookmark.targetId)
                            "post", "reply" -> onPostClick(item.bookmark.targetId)
                        }
                    },
                    onRemove = viewModel::remove
                )
            }
        }
    }
}

@Composable
private fun BookmarkFilterRow(
    state: BookmarksUiState,
    onSelect: (String) -> Unit
) {
    val kinds = BookmarkKind.entries
    val tabs = kinds.map { kind ->
        NebRailTab(label = kind.label, count = state.countOf(kind))
    }
    NebTabRail(
        tabs = tabs,
        selectedIndex = kinds.indexOfFirst { it.key == state.selectedType }.coerceAtLeast(0),
        onSelect = { onSelect(kinds[it].key) }
    )
}

@Composable
private fun BookmarksBody(
    uiState: BookmarksUiState,
    onRetry: () -> Unit,
    onOpen: (BookmarkListItem) -> Unit,
    onRemove: (BookmarkListItem) -> Unit
) {
    val visible = uiState.visibleItems

    when {
        uiState.isLoading && uiState.items.isEmpty() -> {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(2.dp)
            ) {
                repeat(6) { BookmarkRowSkeleton() }
            }
        }

        uiState.error != null && uiState.items.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.CloudOff,
                    title = "Couldn't load bookmarks",
                    subtitle = uiState.error,
                    action = {
                        NebButton(
                            text = "Try again",
                            onClick = onRetry,
                            tone = NebButtonTone.Outlined,
                            size = NebButtonSize.Small
                        )
                    }
                )
            }
        }

        visible.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.BookmarkBorder,
                    title = emptyTitle(uiState.selectedType),
                    subtitle = emptySubtitle(uiState.selectedType)
                )
            }
        }

        else -> {
            val sections = remember(visible) { groupByDay(visible) }
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 2.dp, bottom = 28.dp)
            ) {
                sections.forEach { (label, items) ->
                    item(key = "header_$label") { BookmarkSectionHeader(label) }
                    itemsIndexed(items, key = { _, item -> item.bookmark.id }) { index, item ->
                        BookmarkRow(
                            item = item,
                            onClick = { onOpen(item) },
                            onRemove = { onRemove(item) },
                            showDivider = index < items.lastIndex
                        )
                    }
                }
                item { Spacer(modifier = Modifier.height(8.dp)) }
            }
        }
    }
}

private fun savedLabel(count: Int): String = when (count) {
    0 -> "Nothing saved yet"
    1 -> "1 saved"
    else -> "$count saved"
}

private fun emptyTitle(type: String): String = when (type) {
    BookmarkKind.Posts.key -> "No saved posts"
    BookmarkKind.Replies.key -> "No saved replies"
    BookmarkKind.Resources.key -> "No saved resources"
    else -> "Nothing saved yet"
}

private fun emptySubtitle(type: String): String = when (type) {
    BookmarkKind.Posts.key -> "Bookmark a discussion and it waits for you here."
    BookmarkKind.Replies.key -> "Keep an answer worth coming back to."
    BookmarkKind.Resources.key -> "Save notes and past papers to read later."
    else -> "Tap the bookmark on any post or resource to keep it."
}

private fun groupByDay(items: List<BookmarkListItem>): List<Pair<String, List<BookmarkListItem>>> {
    val ordered = items.sortedByDescending { it.bookmark.createdAt }
    val buckets = LinkedHashMap<String, MutableList<BookmarkListItem>>()
    ordered.forEach { item ->
        buckets.getOrPut(dayBucket(item.bookmark.createdAt)) { mutableListOf() }.add(item)
    }
    return buckets.map { it.key to it.value }
}

private fun dayBucket(timestamp: Long): String {
    val now = Calendar.getInstance()
    val then = Calendar.getInstance().apply { timeInMillis = timestamp }
    val sameYear = now.get(Calendar.YEAR) == then.get(Calendar.YEAR)
    val dayDiff = if (sameYear) {
        now.get(Calendar.DAY_OF_YEAR) - then.get(Calendar.DAY_OF_YEAR)
    } else {
        TimeUnit.MILLISECONDS.toDays(now.timeInMillis - timestamp).toInt() + 1
    }
    return when {
        dayDiff <= 0 -> "Today"
        dayDiff == 1 -> "Yesterday"
        dayDiff < 7 -> "This week"
        dayDiff < 30 -> "This month"
        else -> "Earlier"
    }
}
