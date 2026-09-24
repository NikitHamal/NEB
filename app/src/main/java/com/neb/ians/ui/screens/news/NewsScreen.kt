@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.news

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material.icons.outlined.Newspaper
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.news.NewsCategories
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebTabRail

// ---------------------------------------------------------------------------
// Blog.
//
// The list is the page: a filter rail, a lead story, then the archive. No
// surface under the rows, so the only edges on screen belong to the covers.
// ---------------------------------------------------------------------------

@Composable
fun NewsScreen(
    onNewsClick: (String) -> Unit,
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit,
    onNotificationsClick: () -> Unit,
    onProfileClick: () -> Unit,
    viewModel: NewsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var isRefreshing by remember { mutableStateOf(false) }

    LaunchedEffect(uiState.isLoading) {
        if (!uiState.isLoading) isRefreshing = false
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Blog", fontWeight = FontWeight.SemiBold)
                        Text(
                            text = "News, notices and updates",
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
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            NewsCategoryRail(
                selected = uiState.selectedCategory,
                onSelect = viewModel::selectCategory
            )
            PullToRefreshBox(
                isRefreshing = isRefreshing,
                onRefresh = {
                    isRefreshing = true
                    viewModel.retry()
                },
                modifier = Modifier.fillMaxSize()
            ) {
                NewsIndex(
                    uiState = uiState,
                    onRetry = viewModel::retry,
                    onOpen = onNewsClick
                )
            }
        }
    }
}

@Composable
private fun NewsCategoryRail(
    selected: String?,
    onSelect: (String?) -> Unit
) {
    val tabs = remember { NewsCategories.map { NebRailTab(label = it.label) } }
    NebTabRail(
        tabs = tabs,
        selectedIndex = NewsCategories.indexOfFirst { it.key == selected }.coerceAtLeast(0),
        onSelect = { onSelect(NewsCategories[it].key) }
    )
}

@Composable
private fun NewsIndex(
    uiState: NewsUiState,
    onRetry: () -> Unit,
    onOpen: (String) -> Unit
) {
    when {
        uiState.isLoading && uiState.items.isEmpty() -> {
            Column(modifier = Modifier.fillMaxSize()) {
                NewsIndexSkeleton(lead = true)
                repeat(3) { NewsIndexSkeleton(lead = false) }
            }
        }

        uiState.error != null && uiState.items.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.CloudOff,
                    title = "Couldn't load the blog",
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

        uiState.items.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.Newspaper,
                    title = "Nothing published here yet",
                    subtitle = "New articles and notices will show up on this shelf."
                )
            }
        }

        else -> {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(bottom = 112.dp)
            ) {
                itemsIndexed(uiState.items, key = { _, item -> item.id }) { index, item ->
                    if (index == 0) {
                        NewsLeadStory(item = item, onClick = { onOpen(item.slug) })
                        Spacer(modifier = Modifier.height(4.dp))
                    } else {
                        NewsIndexRow(
                            item = item,
                            onClick = { onOpen(item.slug) },
                            showDivider = index < uiState.items.lastIndex
                        )
                    }
                }
            }
        }
    }
}
