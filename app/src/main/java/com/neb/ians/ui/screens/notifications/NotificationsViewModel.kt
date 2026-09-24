package com.neb.ians.ui.screens.notifications

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiNotification
import com.neb.ians.data.api.ApiNotificationMarkReadRequest
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AppCache
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.decodeFromJsonElement
import javax.inject.Inject

enum class NotificationFilter(val label: String) {
    All("All"),
    Unread("Unread"),
    Mentions("Mentions"),
    Follows("People")
}

data class NotificationsUiState(
    val notifications: List<ApiNotification> = emptyList(),
    val isLoading: Boolean = false,
    val isLoadingMore: Boolean = false,
    val hasMore: Boolean = false,
    val page: Int = 1,
    val error: String? = null,
    val filter: NotificationFilter = NotificationFilter.All
) {
    val hasUnread: Boolean get() = notifications.any { !it.isRead }

    val unreadCount: Int get() = notifications.count { !it.isRead }

    val visible: List<ApiNotification>
        get() = when (filter) {
            NotificationFilter.All -> notifications
            NotificationFilter.Unread -> notifications.filterNot { it.isRead }
            NotificationFilter.Mentions -> notifications.filter {
                val verb = it.verb.lowercase()
                "mention" in verb || "repl" in verb || "comment" in verb
            }
            NotificationFilter.Follows -> notifications.filter { "follow" in it.verb.lowercase() }
        }
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

    fun setFilter(filter: NotificationFilter) {
        _uiState.update { it.copy(filter = filter) }
    }

    fun loadNotifications(): Job {
        val job = viewModelScope.launch {
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
        return job
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