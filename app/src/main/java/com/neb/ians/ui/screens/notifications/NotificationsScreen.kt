package com.neb.ians.ui.screens.notifications

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
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

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Notifications") })
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            when {
                uiState.isLoading -> CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                uiState.error != null -> Text("Error: ${uiState.error}", modifier = Modifier.padding(16.dp))
                uiState.notifications.isEmpty() -> Text("No notifications yet", modifier = Modifier.padding(16.dp))
                else -> {
                    LazyColumn(modifier = Modifier.fillMaxSize()) {
                        items(uiState.notifications) { notification ->
                            NotificationItem(
                                notification = notification,
                                onPostClick = onPostClick,
                                onProfileClick = onProfileClick
                            )
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
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = if (!notification.isRead) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f) else MaterialTheme.colorScheme.surface,
        tonalElevation = if (!notification.isRead) 1.dp else 0.dp
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(notification.message, style = MaterialTheme.typography.bodyMedium)
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                formatTimeAgo(notification.createdAt),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}