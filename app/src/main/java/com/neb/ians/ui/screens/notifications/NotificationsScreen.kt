package com.neb.ians.ui.screens.notifications

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.PersonAdd
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import kotlinx.coroutines.launch
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiNotification
import com.neb.ians.data.api.ApiNotificationMarkReadRequest
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AppCache
import com.neb.ians.ui.components.Avatar
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.decodeFromJsonElement
import javax.inject.Inject

data class NotificationsUiState(
    val notifications: List<ApiNotification> = emptyList(),
    val isLoading: Boolean = false,
    val isLoadingMore: Boolean = false,
    val hasMore: Boolean = false,
    val page: Int = 1,
    val error: String? = null
) {
    val hasUnread: Boolean get() = notifications.any { !it.isRead }
}

@HiltViewModel
class NotificationsViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val realtimeClient: RealtimeClient,
    private val appCache: AppCache
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        NotificationsUiState(
            notifications = appCache.notifications,
            hasMore = appCache.notificationsHasMore,
            page = appCache.notificationsPage,
            isLoading = appCache.notifications.isEmpty()
        )
    )
    val uiState: StateFlow<NotificationsUiState> = _uiState.asStateFlow()
    private var unsubscribeUser: (() -> Unit)? = null
    private val notifJson = Json { ignoreUnknownKeys = true }

    init {
        unsubscribeUser = realtimeClient.subscribe("user")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                if (event.channel == "user") handleUserEvent(event.event, event.data)
            }
        }
    }

    override fun onCleared() {
        unsubscribeUser?.invoke()
        unsubscribeUser = null
        super.onCleared()
    }

    private fun handleUserEvent(event: String, data: JsonObject?) {
        when (event) {
            "notification.new" -> {
                try {
                    val notif = notifJson.decodeFromJsonElement<ApiNotification>(data ?: return)
                    _uiState.update { state ->
                        val updated = listOf(notif) + state.notifications
                        appCache.notifications = updated
                        appCache.notificationsHasMore = true
                        state.copy(notifications = updated, hasMore = true)
                    }
                } catch (_: Exception) {}
            }
        }
    }

    fun loadNotifications() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = it.notifications.isEmpty(), error = null) }
            try {
                val token = authRepository.getBearerToken()
                if (token == null) {
                    _uiState.update { it.copy(isLoading = false, error = "Not signed in") }
                    return@launch
                }
                val response = apiService.getNotifications(token, page = 1)
                _uiState.update {
                    it.copy(
                        notifications = response.notifications,
                        isLoading = false,
                        page = 1,
                        hasMore = response.hasMore
                    )
                }
                appCache.notifications = response.notifications
                appCache.notificationsHasMore = response.hasMore
                appCache.notificationsPage = 1
            } catch (e: Exception) {
                if (_uiState.value.notifications.isEmpty()) {
                    _uiState.update { it.copy(isLoading = false, error = e.localizedMessage) }
                } else {
                    _uiState.update { it.copy(isLoading = false) }
                }
            }
            realtimeClient.refreshUnreadCount()
        }
    }

    fun loadNextPage() {
        val state = _uiState.value
        if (state.isLoading || state.isLoadingMore || !state.hasMore) return
        viewModelScope.launch {
            _uiState.update { it.copy(isLoadingMore = true) }
            try {
                val token = authRepository.getBearerToken()
                if (token == null) {
                    _uiState.update { it.copy(isLoadingMore = false) }
                    return@launch
                }
                val nextPage = state.page + 1
                val response = apiService.getNotifications(token, page = nextPage)
                _uiState.update { current ->
                    val existingIds = current.notifications.mapTo(HashSet()) { it.id }
                    val merged = current.notifications +
                        response.notifications.filterNot { it.id in existingIds }
                    
                    appCache.notifications = merged
                    appCache.notificationsHasMore = response.hasMore
                    appCache.notificationsPage = nextPage
                    
                    current.copy(
                        notifications = merged,
                        page = nextPage,
                        hasMore = response.hasMore,
                        isLoadingMore = false
                    )
                }
            } catch (_: Exception) {
                _uiState.update { it.copy(isLoadingMore = false) }
            }
        }
    }

    fun markAllRead() {
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: return@launch
                apiService.markNotificationsRead(token, ApiNotificationMarkReadRequest(markAll = true))
                _uiState.update { current ->
                    val updated = current.notifications.map { it.copy(isRead = true) }
                    appCache.notifications = updated
                    current.copy(notifications = updated)
                }
                realtimeClient.setUnreadCount(0)
            } catch (_: Exception) {
            }
        }
    }

    /** Marks a single notification read — optimistic UI, then refresh badge from server. */
    fun markOneRead(notificationId: String) {
        val target = _uiState.value.notifications.firstOrNull { it.id == notificationId }
        if (target == null || target.isRead) return
        // Optimistic: tint change immediately + drop badge locally.
        _uiState.update { current ->
            val updated = current.notifications.map {
                if (it.id == notificationId) it.copy(isRead = true) else it
            }
            appCache.notifications = updated
            current.copy(notifications = updated)
        }
        realtimeClient.setUnreadCount(realtimeClient.unreadCount.value - 1)
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: return@launch
                apiService.markNotificationsRead(
                    token,
                    ApiNotificationMarkReadRequest(notificationIds = listOf(notificationId))
                )
            } catch (_: Exception) {
            }
            realtimeClient.refreshUnreadCount()
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotificationsScreen(
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    onResourceClick: (String) -> Unit = {},
    viewModel: NotificationsViewModel = hiltViewModel()
) {
    LaunchedEffect(Unit) {
        viewModel.loadNotifications()
    }

    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }

    // Infinite scroll: load the next page when the last loaded item becomes visible.
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
                title = { Text("Notifications") },
                actions = {
                    if (uiState.hasUnread) {
                        TextButton(onClick = viewModel::markAllRead) {
                            Text(
                                text = "Mark all read",
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                }
            )
        }
    ) { padding ->
        PullToRefreshBox(
            isRefreshing = isRefreshing,
            onRefresh = {
                scope.launch {
                    isRefreshing = true
                    viewModel.loadNotifications()
                    isRefreshing = false
                }
            },
            modifier = Modifier.fillMaxSize().padding(padding)
        ) {
            Box(modifier = Modifier.fillMaxSize()) {
                when {
                    uiState.isLoading && uiState.notifications.isEmpty() ->
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                    uiState.error != null && uiState.notifications.isEmpty() ->
                        Text("Error: ${uiState.error}", modifier = Modifier.padding(16.dp))
                    uiState.notifications.isEmpty() ->
                        Text("No notifications yet", modifier = Modifier.padding(16.dp))
                    else -> {
                        LazyColumn(
                            state = listState,
                            modifier = Modifier.fillMaxSize()
                        ) {
                            items(uiState.notifications, key = { it.id }) { notification ->
                                NotificationItem(
                                    notification = notification,
                                    onClick = {
                                        viewModel.markOneRead(notification.id)
                                        handleNotificationClick(notification, onPostClick, onProfileClick, onResourceClick)
                                    },
                                    onAvatarClick = {
                                        notification.actorName?.takeIf { it.isNotBlank() }?.let(onProfileClick)
                                    }
                                )
                                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                            }
                            if (uiState.isLoadingMore) {
                                item(key = "loading_footer") {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(vertical = 16.dp),
                                        contentAlignment = Alignment.Center
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
    }
}

/** Maps a notification verb to a leading icon (web parity). */
private fun verbIcon(verb: String): ImageVector {
    val v = verb.lowercase()
    return when {
        "like" in v || "thumb" in v -> Icons.Outlined.ThumbUp
        "repl" in v || "comment" in v -> Icons.AutoMirrored.Outlined.Reply
        "follow" in v -> Icons.Outlined.PersonAdd
        "mention" in v -> Icons.Outlined.AlternateEmail
        else -> Icons.Outlined.Notifications
    }
}

private fun handleNotificationClick(
    notification: ApiNotification,
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    onResourceClick: (String) -> Unit
) {
    val verb = notification.verb
    val targetType = notification.targetType ?: ""
    val targetId = notification.targetId ?: ""
    val referenceType = notification.referenceType ?: ""
    val referenceId = notification.referenceId ?: ""
    val actorUsername = notification.actorName

    when (verb) {
        "follow", "follow_request" -> {
            if (!actorUsername.isNullOrBlank()) onProfileClick(actorUsername)
        }
        else -> when (targetType) {
            "post" -> if (targetId.isNotBlank()) onPostClick(targetId)
            "reply" -> {
                val postId = if (referenceType == "post") referenceId else ""
                if (postId.isNotBlank()) onPostClick(postId)
            }
            "resource" -> if (targetId.isNotBlank()) onResourceClick(targetId)
            "resource_comment" -> {
                val resourceId = if (referenceType == "resource") referenceId else ""
                if (resourceId.isNotBlank()) onResourceClick(resourceId)
            }
            "user" -> {
                if (!actorUsername.isNullOrBlank()) onProfileClick(actorUsername)
            }
            else -> {}
        }
    }
}

@Composable
fun NotificationItem(
    notification: ApiNotification,
    onClick: () -> Unit,
    onAvatarClick: () -> Unit = {}
) {
    val isSystem = notification.actorName.isNullOrBlank() ||
                   notification.actorName.equals("System", ignoreCase = true) ||
                   notification.verb.equals("system", ignoreCase = true)

    val displayMessage = if (notification.message.isNotBlank()) {
        notification.message
    } else {
        val actor = notification.actorName?.takeIf { it.isNotBlank() } ?: "Someone"
        when (notification.verb.lowercase()) {
            "like_post" -> "$actor liked your post"
            "like_reply" -> "$actor liked your reply"
            "reply" -> "$actor replied to your post"
            "reply_reply" -> "$actor replied to your comment"
            "follow" -> "$actor started following you"
            "follow_request" -> "$actor requested to follow you"
            "mention" -> "$actor mentioned you"
            "like_resource" -> "$actor liked your resource"
            "like_resource_comment" -> "$actor liked your comment"
            "resource_comment" -> "$actor commented on your resource"
            "resource_comment_reply" -> "$actor replied to your comment"
            else -> "New activity on your account"
        }
    }

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        color = if (!notification.isRead) {
            MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f)
        } else {
            MaterialTheme.colorScheme.surface
        },
        tonalElevation = if (!notification.isRead) 1.dp else 0.dp
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (isSystem) {
                Surface(
                    modifier = Modifier.size(40.dp),
                    shape = CircleShape,
                    color = MaterialTheme.colorScheme.primaryContainer
                ) {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Notifications,
                            contentDescription = "System Notification",
                            modifier = Modifier.size(20.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            } else {
                Avatar(
                    name = notification.actorName ?: "?",
                    imageUrl = notification.actorPhotoUrl,
                    size = 40.dp,
                    modifier = Modifier.clickable(onClick = onAvatarClick)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = displayMessage,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = if (!notification.isRead) FontWeight.SemiBold else FontWeight.Normal,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(5.dp)
                ) {
                    Icon(
                        imageVector = verbIcon(notification.verb),
                        contentDescription = null,
                        modifier = Modifier.size(14.dp),
                        tint = if (!notification.isRead) {
                            MaterialTheme.colorScheme.primary
                        } else {
                            MaterialTheme.colorScheme.onSurfaceVariant
                        }
                    )
                    Text(
                        text = formatTimeAgo(notification.createdAt),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1
                    )
                }
            }
            if (!notification.isRead) {
                Box(
                    modifier = Modifier
                        .padding(top = 6.dp)
                        .size(8.dp)
                        .background(MaterialTheme.colorScheme.primary, CircleShape)
                )
            }
        }
    }
}
