package com.neb.ians.ui.screens.resource

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResourceRequest
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRequestRepository
import com.neb.ians.data.repository.AuthState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ResourceRequestsUiState(
    val requests: List<ApiResourceRequest> = emptyList(),
    val statusFilter: String? = "open", // default to open status as in Web
    val isLoading: Boolean = false,
    val isSubmitting: Boolean = false,
    val error: String? = null,
    val isAuthenticated: Boolean = false
)

@HiltViewModel
class ResourceRequestsViewModel @Inject constructor(
    private val repository: ResourceRequestRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ResourceRequestsUiState())
    val uiState: StateFlow<ResourceRequestsUiState> = _uiState.asStateFlow()

    init {
        // Track auth state
        viewModelScope.launch {
            authRepository.authState.collect { authState ->
                _uiState.update { it.copy(isAuthenticated = authState is AuthState.Authenticated) }
            }
        }
        loadRequests()
    }

    fun loadRequests(status: String? = _uiState.value.statusFilter) {
        _uiState.update { it.copy(isLoading = true, statusFilter = status, error = null) }
        viewModelScope.launch {
            repository.getResourceRequests(status, null, null)
                .onSuccess { list ->
                    _uiState.update { it.copy(requests = list, isLoading = false) }
                }
                .onFailure { err ->
                    _uiState.update { it.copy(error = err.message ?: "Failed to load requests", isLoading = false) }
                }
        }
    }

    fun toggleUpvote(requestId: String) {
        if (!_uiState.value.isAuthenticated) {
            _uiState.update { it.copy(error = "Authentication required to upvote") }
            return
        }

        val currentList = _uiState.value.requests
        val targetIndex = currentList.indexOfFirst { it.id == requestId }
        if (targetIndex == -1) return

        val targetRequest = currentList[targetIndex]
        val wasUpvoted = targetRequest.isUpvoted
        val newUpvoteCount = if (wasUpvoted) targetRequest.upvoteCount - 1 else targetRequest.upvoteCount + 1
        
        // Optimistic update
        val updatedRequests = currentList.toMutableList()
        updatedRequests[targetIndex] = targetRequest.copy(
            isUpvoted = !wasUpvoted,
            upvoteCount = newUpvoteCount
        )
        _uiState.update { it.copy(requests = updatedRequests) }

        viewModelScope.launch {
            repository.toggleUpvote(requestId)
                .onSuccess { response ->
                    // Sync with actual response
                    val syncList = _uiState.value.requests.toMutableList()
                    val idx = syncList.indexOfFirst { it.id == requestId }
                    if (idx != -1) {
                        syncList[idx] = syncList[idx].copy(
                            isUpvoted = response.upvoted,
                            upvoteCount = response.upvoteCount
                        )
                        _uiState.update { it.copy(requests = syncList) }
                    }
                }
                .onFailure { err ->
                    // Rollback optimistic update
                    val rollbackList = _uiState.value.requests.toMutableList()
                    val idx = rollbackList.indexOfFirst { it.id == requestId }
                    if (idx != -1) {
                        rollbackList[idx] = rollbackList[idx].copy(
                            isUpvoted = wasUpvoted,
                            upvoteCount = targetRequest.upvoteCount
                        )
                        _uiState.update { 
                            it.copy(
                                requests = rollbackList,
                                error = err.message ?: "Failed to upvote"
                            )
                        }
                    }
                }
        }
    }

    fun createRequest(
        title: String,
        description: String?,
        subject: String?,
        gradeLevel: String?,
        onSuccess: () -> Unit
    ) {
        if (title.isBlank()) return
        _uiState.update { it.copy(isSubmitting = true, error = null) }
        viewModelScope.launch {
            repository.createResourceRequest(title, description, subject, gradeLevel)
                .onSuccess {
                    _uiState.update { it.copy(isSubmitting = false) }
                    loadRequests() // reload requests list
                    onSuccess()
                }
                .onFailure { err ->
                    _uiState.update { it.copy(error = err.message ?: "Failed to create request", isSubmitting = false) }
                }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}
