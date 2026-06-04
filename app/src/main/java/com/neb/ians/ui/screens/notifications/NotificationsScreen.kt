package com.neb.ians.ui.screens.notifications

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.ui.components.UserAvatar
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiNotification
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.util.formatTimeAgo

data class NotificationsUiState(
    val notifications: List<ApiNotification> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class NotificationsViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(NotificationsUiState())
    val uiState: StateFlow<NotificationsUiState> = _uiState.asStateFlow()

    fun loadNotifications() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val token = authRepository.getBearerToken() ?: return@launch
                val response = apiService.getNotifications(token)
                _uiState.value = _uiState.value.copy(notifications = response.notifications, isLoading = false)
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun markAllRead() {
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: return@launch
                apiService.markNotificationsRead(token)
                _uiState.value = _uiState.value.copy(
                    notifications = _uiState.value.notifications.map { it.copy(isRead = true) }
                )
            } catch (_: Exception) { }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotificationsScreen(
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    viewModel: NotificationsViewModel = hiltViewModel()
) {
    LaunchedEffect(Unit) {
        viewModel.loadNotifications()
    }

    val uiState by viewModel.uiState.collectAsState()
    val hasUnread = uiState.notifications.any { !it.isRead }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Notifications") },
                actions = {
                    if (hasUnread) {
                        TextButton(onClick = { viewModel.markAllRead() }) {
                            Icon(Icons.Filled.Check, contentDescription = null, modifier = Modifier.size(18.dp))
                            Spacer(Modifier.width(4.dp))
                            Text("Mark all read")
                        }
                    }
                }
            )
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            when {
                uiState.isLoading -> CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                uiState.error != null -> Text("Error: ${uiState.error}", modifier = Modifier.padding(16.dp))
                uiState.notifications.isEmpty() -> Text(
                    "No notifications yet",
                    modifier = Modifier.align(Alignment.Center).padding(16.dp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                else -> {
                    LazyColumn(modifier = Modifier.fillMaxSize()) {
                        items(uiState.notifications, key = { it.id }) { notification ->
                            NotificationItem(
                                notification = notification,
                                onPostClick = onPostClick,
                                onProfileClick = onProfileClick
                            )
                            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.4f))
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun NotificationItem(
    notification: ApiNotification,
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit
) {
    val postId = when {
        notification.targetType == "post" -> notification.targetId
        notification.referenceType == "post" -> notification.referenceId
        else -> null
    }
    val onClick: () -> Unit = {
        when {
            postId != null -> onPostClick(postId)
            !notification.actorName.isNullOrBlank() -> onProfileClick(notification.actorName)
            else -> {}
        }
    }

    Surface(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick),
        color = if (!notification.isRead) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.18f) else MaterialTheme.colorScheme.surface
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            UserAvatar(
                photoUrl = notification.actorPhotoUrl,
                name = notification.actorName ?: "?",
                size = 44.dp
            )
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    notification.message,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = if (!notification.isRead) FontWeight.SemiBold else FontWeight.Normal
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    formatTimeAgo(notification.createdAt),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (!notification.isRead) {
                Spacer(Modifier.width(8.dp))
                Box(
                    modifier = Modifier
                        .size(8.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.primary)
                )
            }
        }
    }
}