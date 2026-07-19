package com.neb.ians.ui.screens.resource

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.util.ResourceDownloadManager
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
    val currentUsername: String = "",
    val authorPhotoUrl: String? = null,
    val comments: List<ApiResourceComment> = emptyList(),
    val commentsLoading: Boolean = false,
    val commentSort: String = "oldest",
    val suggestedVideos: List<ApiResource> = emptyList(),
    val commentDraft: String = "",
    val threadDraft: String = "",
    val isPostingComment: Boolean = false,
    val downloadProgress: Int? = null,
    val isDownloaded: Boolean = false,
    val snackbarMessage: String? = null
) {
    /** Top-level comments in the selected sort order. */
    val topLevelComments: List<ApiResourceComment>
        get() {
            val topLevel = comments.filter { it.parentCommentId.isNullOrBlank() }
            return when (commentSort) {
                "newest" -> topLevel.sortedByDescending { it.createdAt }
                "top" -> topLevel.sortedWith(
                    compareByDescending<ApiResourceComment> { it.likeCount }.thenBy { it.createdAt }
                )
                else -> topLevel.sortedBy { it.createdAt }
            }
        }

    /** Children and descendants of a given comment, oldest first. */
    fun childrenOf(commentId: String): List<ApiResourceComment> {
        val result = mutableListOf<ApiResourceComment>()
        val descendants = mutableSetOf<String>()
        var addedAny: Boolean
        do {
            addedAny = false
            for (c in comments) {
                val parentId = c.parentCommentId
                if (!parentId.isNullOrBlank() && !descendants.contains(c.id)) {
                    if (parentId == commentId || descendants.contains(parentId)) {
                        descendants.add(c.id)
                        result.add(c)
                        addedAny = true
                    }
                }
            }
        } while (addedAny)
        return result.sortedBy { it.createdAt }
    }
}

@HiltViewModel
class ResourceDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository,
    private val authRepository: AuthRepository,
    private val downloadManager: ResourceDownloadManager
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""
    private val downloadedResource = downloadManager.findDownloaded(resourceId)?.let { item ->
        ApiResource(
            id = item.resourceId,
            title = item.title,
            subject = "Downloaded",
            gradeLevel = "",
            type = item.type,
            fileUrl = item.fileUrl,
            thumbnailUrl = item.thumbnailUrl,
            fileSize = item.sizeBytes
        )
    }
    private val cachedResource = resourceRepository.peekResource(resourceId) ?: downloadedResource
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
        viewModelScope.launch {
            downloadManager.downloads.collect { downloads ->
                _uiState.update { state ->
                    state.copy(isDownloaded = downloads.any { it.resourceId == resourceId })
                }
            }
        }
        viewModelScope.launch {
            downloadManager.downloadProgress.collect { progress ->
                _uiState.update { it.copy(downloadProgress = progress[resourceId]) }
            }
        }
    }

    fun downloadResource() {
        val resource = _uiState.value.resource ?: return
        if (_uiState.value.isDownloaded) {
            _uiState.update { it.copy(snackbarMessage = "Available offline in Downloads") }
            return
        }
        downloadManager.downloadResourceFromApi(resource)
        _uiState.update { it.copy(snackbarMessage = "Downloading inside NEBians") }
    }

    fun load(forceRefresh: Boolean = false) {
        viewModelScope.launch {
            val token = authRepository.getToken()
            val userId = authRepository.currentUserIdFlow.first()
            val usernameHandle = authRepository.currentUsernameHandleFlow.first()
            val hasResource = _uiState.value.resource != null
            _uiState.update { it.copy(isAuthenticated = token != null, currentUserId = userId, currentUsername = usernameHandle, isLoading = !hasResource, error = null) }

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
                    if (resource.type.contains("video", ignoreCase = true) || resource.fileUrl.contains(".mp4", ignoreCase = true)) {
                        loadSuggestedVideos(resource)
                    }
                    val authorUsername = resource.uploadedByUsername
                    if (authorUsername.isNotBlank()) {
                        fetchAuthorPhoto(authorUsername)
                    }
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

    private fun loadSuggestedVideos(resource: ApiResource) {
        viewModelScope.launch {
            val subject = resource.subject.split(",").firstOrNull()?.trim().orEmpty().takeIf { it.isNotBlank() }
            resourceRepository.getResources(subject = subject, type = "Video", sort = "popular")
                .onSuccess { result ->
                    _uiState.update {
                        it.copy(
                            suggestedVideos = result.resources
                                .filterNot { candidate -> candidate.id == resource.id }
                                .filter { candidate -> candidate.type.contains("video", true) || candidate.fileUrl.contains(".mp4", true) }
                                .take(8)
                        )
                    }
                }
        }
    }

    private fun fetchAuthorPhoto(username: String) {
        viewModelScope.launch {
            val profile = authRepository.getPublicProfile(username)
            val photoUrl = profile?.photoUrl?.takeIf { it.isNotBlank() }
            _uiState.update { it.copy(authorPhotoUrl = photoUrl) }
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

    fun onThreadDraftChange(text: String) {
        _uiState.update { it.copy(threadDraft = text) }
    }

    fun setCommentSort(sort: String) {
        _uiState.update { it.copy(commentSort = sort) }
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

    /** Thread composer: posts a reply under the given parent comment. */
    fun postThreadReply(parentCommentId: String, onSuccess: () -> Unit = {}) {
        val draft = _uiState.value.threadDraft.trim()
        if (draft.isEmpty() || _uiState.value.isPostingComment) return
        if (!_uiState.value.isAuthenticated) {
            _uiState.update { it.copy(snackbarMessage = "Please sign in to comment") }
            return
        }
        _uiState.update { it.copy(isPostingComment = true) }
        viewModelScope.launch {
            resourceRepository.createComment(resourceId, draft, parentCommentId)
                .onSuccess { comment ->
                    _uiState.update { state ->
                        val bumped = state.comments.map { existing ->
                            if (existing.id == parentCommentId) {
                                val next = existing.replyCount + 1
                                existing.copy(replyCountSnake = next, replyCountCamel = next)
                            } else existing
                        }
                        val currentResource = state.resource
                        state.copy(
                            comments = bumped.filterNot { it.id == comment.id } + comment,
                            threadDraft = "",
                            isPostingComment = false,
                            resource = currentResource?.copy(commentCount = currentResource.commentCount + 1)
                        )
                    }
                    onSuccess()
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

    // One in-flight like per comment: rapid taps are ignored instead of
    // stacking toggles that flip the server state back and forth.
    private val processingCommentLikes = mutableSetOf<String>()

    fun toggleCommentLike(commentId: String) {
        if (processingCommentLikes.contains(commentId)) return
        val comment = _uiState.value.comments.firstOrNull { it.id == commentId } ?: return
        val wasLiked = comment.isLiked == true
        val nextLiked = !wasLiked
        val nextCount = (comment.likeCount + if (nextLiked) 1 else -1).coerceAtLeast(0)
        processingCommentLikes.add(commentId)
        _uiState.update { state ->
            state.copy(comments = state.comments.map {
                if (it.id == commentId) {
                    it.copy(
                        isLikedSnake = nextLiked,
                        isLikedCamel = nextLiked,
                        likeCountSnake = nextCount,
                        likeCountCamel = nextCount
                    )
                } else it
            })
        }
        viewModelScope.launch {
            resourceRepository.toggleCommentLike(resourceId, commentId)
                .onSuccess { resp ->
                    // Reconcile with the server's truth (state + count).
                    _uiState.update { state ->
                        state.copy(comments = state.comments.map {
                            if (it.id == commentId) {
                                it.copy(
                                    isLikedSnake = resp.isLiked,
                                    isLikedCamel = resp.isLiked,
                                    likeCountSnake = resp.likeCount,
                                    likeCountCamel = resp.likeCount
                                )
                            } else it
                        })
                    }
                }
                .onFailure { e ->
                    _uiState.update { state ->
                        state.copy(
                            comments = state.comments.map { if (it.id == commentId) comment else it },
                            snackbarMessage = ApiErrorMapper.mapException(e)
                        )
                    }
                }
            processingCommentLikes.remove(commentId)
        }
    }

    fun consumeSnackbar() {
        _uiState.update { it.copy(snackbarMessage = null) }
    }
}
