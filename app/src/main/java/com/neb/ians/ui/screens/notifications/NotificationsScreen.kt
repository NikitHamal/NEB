@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.notifications

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material.icons.outlined.NotificationsNone
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
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiNotification
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFilterChip
import com.neb.ians.ui.components.NebLoadingIndicator
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.launch
import java.util.Calendar
import java.util.concurrent.TimeUnit

@Composable
fun NotificationsScreen(
    onNavigateBack: () -> Unit,
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    onResourceClick: (String) -> Unit = {},
    viewModel: NotificationsViewModel = hiltViewModel()
) {
    LaunchedEffect(Unit) { viewModel.loadNotifications() }

    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }

    LaunchedEffect(listState) {
        snapshotFlow {
            val layoutInfo = listState.layoutInfo
            val lastVisible = layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: -1
            lastVisible to layoutInfo.totalItemsCount
        }
            .distinctUntilChanged()
            .collect { (lastVisible, total) ->
                if (total > 0 && lastVisible >= total - 3) viewModel.loadNextPage()
            }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Notifications", fontWeight = FontWeight.SemiBold)
                        if (uiState.unreadCount > 0) {
                            Text(
                                text = "${uiState.unreadCount} new",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (uiState.hasUnread) {
                        NebButton(
                            text = "Mark all read",
                            onClick = viewModel::markAllRead,
                            tone = NebButtonTone.Text,
                            size = NebButtonSize.Small
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            FilterRow(
                selected = uiState.filter,
                onSelect = viewModel::setFilter,
                unreadCount = uiState.unreadCount
            )
            PullToRefreshBox(
                isRefreshing = isRefreshing,
                onRefresh = {
                    scope.launch {
                        isRefreshing = true
                        viewModel.loadNotifications().join()
                        isRefreshing = false
                    }
                },
                modifier = Modifier.fillMaxSize()
            ) {
                NotificationsBody(
                    uiState = uiState,
                    listState = listState,
                    onRetry = { viewModel.loadNotifications() },
                    onOpen = { notification ->
                        viewModel.markOneRead(notification.id)
                        handleNotificationClick(
                            notification,
                            onPostClick,
                            onProfileClick,
                            onResourceClick
                        )
                    },
                    onProfileClick = onProfileClick
                )
            }
        }
    }
}

@Composable
private fun FilterRow(
    selected: NotificationFilter,
    onSelect: (NotificationFilter) -> Unit,
    unreadCount: Int
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(horizontal = 16.dp, vertical = 6.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        NotificationFilter.entries.forEach { filter ->
            val label = if (filter == NotificationFilter.Unread && unreadCount > 0) {
                "Unread ($unreadCount)"
            } else {
                filter.label
            }
            NebFilterChip(
                label = label,
                selected = selected == filter,
                onClick = { onSelect(filter) }
            )
        }
    }
}

@Composable
private fun NotificationsBody(
    uiState: NotificationsUiState,
    listState: LazyListState,
    onRetry: () -> Unit,
    onOpen: (ApiNotification) -> Unit,
    onProfileClick: (String) -> Unit
) {
    val visible = uiState.visible

    when {
        uiState.isLoading && uiState.notifications.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebLoadingIndicator()
            }
        }

        uiState.error != null && uiState.notifications.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.CloudOff,
                    title = "Couldn't load notifications",
                    subtitle = uiState.error,
                    action = {
                        NebButton(
                            text = "Try again",
                            onClick = onRetry,
                            tone = NebButtonTone.Outlined
                        )
                    }
                )
            }
        }

        visible.isEmpty() -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.NotificationsNone,
                    title = emptyTitle(uiState.filter),
                    subtitle = emptySubtitle(uiState.filter)
                )
            }
        }

        else -> {
            LazyColumn(
                state = listState,
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(start = 14.dp, end = 14.dp, top = 6.dp, bottom = 24.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                var lastBucket: String? = null
                visible.forEach { notification ->
                    val bucket = dayBucket(notification.createdAt)
                    if (bucket != lastBucket) {
                        lastBucket = bucket
                        item(key = "header_$bucket") {
                            Text(
                                text = bucket,
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(start = 6.dp, top = 12.dp, bottom = 2.dp)
                            )
                        }
                    }
                    item(key = notification.id) {
                        NotificationItem(
                            notification = notification,
                            onClick = { onOpen(notification) },
                            onAvatarClick = {
                                notification.actorName
                                    ?.takeIf { it.isNotBlank() }
                                    ?.let(onProfileClick)
                            }
                        )
                    }
                }
                if (uiState.isLoadingMore) {
                    item(key = "loading_footer") {
                        Box(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            NebLoadingIndicator(modifier = Modifier.size(28.dp))
                        }
                    }
                }
            }
        }
    }
}

private fun emptyTitle(filter: NotificationFilter): String = when (filter) {
    NotificationFilter.All -> "Nothing here yet"
    NotificationFilter.Unread -> "You're all caught up"
    NotificationFilter.Mentions -> "No replies or mentions"
    NotificationFilter.Follows -> "No new followers"
}

private fun emptySubtitle(filter: NotificationFilter): String = when (filter) {
    NotificationFilter.All -> "Likes, replies and follows will land here."
    NotificationFilter.Unread -> "Every notification has been read."
    NotificationFilter.Mentions -> "When someone talks to you, you'll see it here."
    NotificationFilter.Follows -> "Share your profile to grow your circle."
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
