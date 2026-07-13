package com.neb.ians.ui.screens.resource

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
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
    val isBookmarked: Boolean = false,
    val isAuthenticated: Boolean = false,
    val currentUserId: String? = null,
    val comments: List<ApiResourceComment> = emptyList(),
    val commentsLoading: Boolean = false,
    val commentDraft: String = "",
    val isPostingComment: Boolean = false,
    val snackbarMessage: String? = null
)

@HiltViewModel
class ResourceDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""
    private val cachedResource = resourceRepository.peekResource(resourceId)
    private val cachedComments = resourceRepository.peekComments(resourceId).orEmpty()

    private val _uiState = MutableStateFlow(
        ResourceDetailUiState(
            resource = cachedResource,
            isLoading = cachedResource == null,
            isLiked = cachedResource?.isLiked ?: false,
            likeCount = cachedResource?.likeCount ?: 0,
            isBookmarked = cachedResource?.isBookmarked ?: false,
            comments = cachedComments,
            commentsLoading = cachedResource != null && cachedComments.isEmpty()
        )
    )
    val uiState: StateFlow<ResourceDetailUiState> = _uiState.asStateFlow()

    private var likeJob: Job? = null
    private var pendingLikeToggles = 0
    private var bookmarkJob: Job? = null
    private var pendingBookmarkToggles = 0

    init {
        load()
    }

    fun load(forceRefresh: Boolean = false) {
        viewModelScope.launch {
            val token = authRepository.getToken()
            val userId = authRepository.currentUserIdFlow.first()
            val hasResource = _uiState.value.resource != null
            _uiState.update { it.copy(isAuthenticated = token != null, currentUserId = userId, isLoading = !hasResource, error = null) }

            resourceRepository.getResource(resourceId, forceRefresh = forceRefresh)
                .onSuccess { resource ->
                    _uiState.update {
                        it.copy(
                            resource = resource,
                            isLoading = false,
                            isLiked = resource.isLiked ?: false,
                            likeCount = resource.likeCount,
                            isBookmarked = resource.isBookmarked ?: false,
                            error = null
                        )
                    }
                    resourceRepository.viewResource(resourceId)
                }
                .onFailure { e ->
                    val message = ApiErrorMapper.mapException(e)
                    _uiState.update {
                        if (it.resource == null) it.copy(isLoading = false, error = message)
                        else it.copy(isLoading = false, snackbarMessage = message)
                    }
                }
            loadComments(forceRefresh = forceRefresh)
        }
    }

    private fun refreshResourceState() {
        viewModelScope.launch {
            resourceRepository.getResource(resourceId, forceRefresh = true).onSuccess { resource ->
                _uiState.update {
                    it.copy(
                        resource = resource,
                        isLiked = resource.isLiked ?: it.isLiked,
                        likeCount = resource.likeCount,
                        isBookmarked = resource.isBookmarked ?: it.isBookmarked
                    )
                }
            }
        }
    }

    private fun loadComments(forceRefresh: Boolean = false) {
        viewModelScope.launch {
            val hasComments = _uiState.value.comments.isNotEmpty()
            _uiState.update { it.copy(commentsLoading = !hasComments) }
            resourceRepository.getComments(resourceId, forceRefresh = forceRefresh)
                .onSuccess { comments ->
                    _uiState.update { it.copy(comments = comments, commentsLoading = false) }
                }
                .onFailure {
                    _uiState.update { it.copy(commentsLoading = false) }
                }
        }
    }

    fun toggleLike() {
        if (!_uiState.value.isAuthenticated) {
            _uiState.update { it.copy(snackbarMessage = "Please sign in to like resources") }
            return
        }
        val current = _uiState.value
        val nextLiked = !current.isLiked
        _uiState.update {
            it.copy(
                isLiked = nextLiked,
                likeCount = if (nextLiked) it.likeCount + 1 else (it.likeCount - 1).coerceAtLeast(0)
            )
        }
        pendingLikeToggles += 1
        if (likeJob?.isActive != true) {
            likeJob = viewModelScope.launch { drainLikeToggles() }
        }
    }

    private suspend fun drainLikeToggles() {
        while (pendingLikeToggles > 0) {
            pendingLikeToggles -= 1
            resourceRepository.toggleLike(resourceId)
                .onSuccess { resp ->
                    if (pendingLikeToggles == 0) {
                        _uiState.update { it.copy(isLiked = resp.isLiked, likeCount = resp.likeCount) }
                    }
                }
                .onFailure { e ->
                    pendingLikeToggles = 0
                    _uiState.update { it.copy(snackbarMessage = ApiErrorMapper.mapException(e)) }
                    refreshResourceState()
                }
        }
    }

    fun toggleBookmark() {
        if (!_uiState.value.isAuthenticated) {
            _uiState.update { it.copy(snackbarMessage = "Please sign in to save resources") }
            return
        }
        _uiState.update { it.copy(isBookmarked = !it.isBookmarked) }
        pendingBookmarkToggles += 1
        if (bookmarkJob?.isActive != true) {
            bookmarkJob = viewModelScope.launch { drainBookmarkToggles() }
        }
    }

    private suspend fun drainBookmarkToggles() {
        while (pendingBookmarkToggles > 0) {
            pendingBookmarkToggles -= 1
            resourceRepository.toggleBookmark(resourceId)
                .onSuccess { bookmarked ->
                    if (pendingBookmarkToggles == 0) {
                        _uiState.update { it.copy(isBookmarked = bookmarked) }
                    }
                }
                .onFailure { e ->
                    pendingBookmarkToggles = 0
                    _uiState.update { it.copy(snackbarMessage = ApiErrorMapper.mapException(e)) }
                    refreshResourceState()
                }
        }
    }

    fun onCommentDraftChange(text: String) {
        _uiState.update { it.copy(commentDraft = text) }
    }

    fun postComment() {
        val draft = _uiState.value.commentDraft.trim()
        if (draft.isEmpty() || _uiState.value.isPostingComment) return
        if (!_uiState.value.isAuthenticated) {
            _uiState.update { it.copy(snackbarMessage = "Please sign in to comment") }
            return
        }
        _uiState.update { it.copy(isPostingComment = true) }
        viewModelScope.launch {
            resourceRepository.createComment(resourceId, draft)
                .onSuccess { comment ->
                    _uiState.update { state ->
                        val currentResource = state.resource
                        state.copy(
                            comments = state.comments.filterNot { it.id == comment.id } + comment,
                            commentDraft = "",
                            isPostingComment = false,
                            resource = currentResource?.copy(commentCount = currentResource.commentCount + 1)
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(
                            isPostingComment = false,
                            snackbarMessage = ApiErrorMapper.mapException(e)
                        )
                    }
                }
        }
    }

    fun deleteComment(commentId: String) {
        val current = _uiState.value.comments
        _uiState.update { state ->
            state.copy(comments = state.comments.filterNot { it.id == commentId })
        }
        viewModelScope.launch {
            resourceRepository.deleteComment(resourceId, commentId)
                .onFailure { e ->
                    _uiState.update {
                        it.copy(comments = current, snackbarMessage = ApiErrorMapper.mapException(e))
                    }
                }
        }
    }

    fun toggleCommentLike(commentId: String) {
        viewModelScope.launch {
            val comments = _uiState.value.comments
            val comment = comments.firstOrNull { it.id == commentId } ?: return@launch
            val wasLiked = comment.isLiked == true
            val nextLiked = !wasLiked
            val nextCount = (comment.likeCount + if (nextLiked) 1 else -1).coerceAtLeast(0)
            
            val optimistic = comments.map {
                if (it.id == commentId) {
                    it.copy(
                        isLikedSnake = nextLiked,
                        isLikedCamel = nextLiked,
                        likeCountSnake = nextCount,
                        likeCountCamel = nextCount
                    )
                } else it
            }
            _uiState.update { it.copy(comments = optimistic) }
            
            resourceRepository.toggleCommentLike(resourceId, commentId)
                .onFailure { e ->
                    _uiState.update { it.copy(comments = comments, snackbarMessage = ApiErrorMapper.mapException(e)) }
                }
        }
    }

    fun consumeSnackbar() {
        _uiState.update { it.copy(snackbarMessage = null) }
    }
}
