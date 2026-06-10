package com.neb.ians.ui.screens.resource

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ResourceDetailUiState(
    val resource: ApiResource? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val isLiked: Boolean = false,
    val likeCount: Int = 0,
    val isAuthenticated: Boolean = false,
    val currentUserId: String? = null,
    val comments: List<ApiResourceComment> = emptyList(),
    val commentsLoading: Boolean = false,
    val commentDraft: String = "",
    val isPostingComment: Boolean = false
)

@HiltViewModel
class ResourceDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""

    private val _uiState = MutableStateFlow(ResourceDetailUiState())
    val uiState: StateFlow<ResourceDetailUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    private fun load() {
        viewModelScope.launch {
            val token = authRepository.getToken()
            val userId = authRepository.currentUserIdFlow.first()
            _uiState.update { it.copy(isAuthenticated = token != null, currentUserId = userId) }

            resourceRepository.getResource(resourceId)
                .onSuccess { resource ->
                    _uiState.update {
                        it.copy(
                            resource = resource,
                            isLoading = false,
                            isLiked = resource.isLiked ?: false,
                            likeCount = resource.likeCount
                        )
                    }
                    resourceRepository.viewResource(resourceId)
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
            loadComments()
        }
    }

    private fun loadComments() {
        viewModelScope.launch {
            _uiState.update { it.copy(commentsLoading = true) }
            resourceRepository.getComments(resourceId)
                .onSuccess { comments ->
                    _uiState.update { it.copy(comments = comments, commentsLoading = false) }
                }
                .onFailure {
                    _uiState.update { it.copy(commentsLoading = false) }
                }
        }
    }

    fun toggleLike() {
        if (!_uiState.value.isAuthenticated) return
        // Optimistic update
        val wasLiked = _uiState.value.isLiked
        val prevCount = _uiState.value.likeCount
        _uiState.update {
            it.copy(isLiked = !wasLiked, likeCount = if (wasLiked) (prevCount - 1).coerceAtLeast(0) else prevCount + 1)
        }
        viewModelScope.launch {
            resourceRepository.toggleLike(resourceId)
                .onSuccess { resp ->
                    _uiState.update { it.copy(isLiked = resp.isLiked, likeCount = resp.likeCount) }
                }
                .onFailure {
                    _uiState.update { it.copy(isLiked = wasLiked, likeCount = prevCount) }
                }
        }
    }

    fun onCommentDraftChange(text: String) {
        _uiState.update { it.copy(commentDraft = text) }
    }

    fun postComment() {
        val draft = _uiState.value.commentDraft.trim()
        if (draft.isEmpty() || _uiState.value.isPostingComment) return
        _uiState.update { it.copy(isPostingComment = true) }
        viewModelScope.launch {
            resourceRepository.createComment(resourceId, draft)
                .onSuccess { comment ->
                    _uiState.update {
                        it.copy(
                            comments = it.comments + comment,
                            commentDraft = "",
                            isPostingComment = false
                        )
                    }
                }
                .onFailure {
                    _uiState.update { it.copy(isPostingComment = false) }
                }
        }
    }

    fun deleteComment(commentId: String) {
        viewModelScope.launch {
            resourceRepository.deleteComment(resourceId, commentId)
                .onSuccess {
                    _uiState.update { state ->
                        state.copy(comments = state.comments.filterNot { it.id == commentId })
                    }
                }
        }
    }
}
