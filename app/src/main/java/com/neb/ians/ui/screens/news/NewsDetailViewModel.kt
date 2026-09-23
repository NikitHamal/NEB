package com.neb.ians.ui.screens.news

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.news.NewsComment
import com.neb.ians.data.news.NewsDetail
import com.neb.ians.data.repository.CacheBus
import com.neb.ians.data.repository.NewsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.net.URLDecoder
import javax.inject.Inject

data class NewsDetailUiState(
    val slug: String = "",
    val detail: NewsDetail? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val isAuthenticated: Boolean = false,
    val comments: List<NewsComment> = emptyList(),
    val commentsLoading: Boolean = true,
    val commentSort: String = "oldest",
    val commentDraft: String = "",
    val threadDraft: String = "",
    val isPostingComment: Boolean = false,
    val snackbarMessage: String? = null
) {
    /** Top-level comments in the selected sort order (same rule as forum replies). */
    val topLevelComments: List<NewsComment>
        get() {
            val topLevel = comments.filter { it.parentCommentId.isBlank() }
            return when (commentSort) {
                "newest" -> topLevel.sortedByDescending { it.createdAt }
                "top" -> topLevel.sortedWith(
                    compareByDescending<NewsComment> { it.thumbsUpCount }.thenBy { it.createdAt }
                )
                else -> topLevel.sortedBy { it.createdAt }
            }
        }

    /** Children and deeper descendants of a comment, oldest first (same rule as the forum thread sheet). */
    fun childrenOf(commentId: String): List<NewsComment> {
        val result = mutableListOf<NewsComment>()
        val descendants = mutableSetOf<String>()
        var addedAny: Boolean
        do {
            addedAny = false
            for (c in comments) {
                val parentId = c.parentCommentId
                if (parentId.isNotBlank() && !descendants.contains(c.id)) {
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
class NewsDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val newsRepository: NewsRepository,
    private val cacheBus: CacheBus,
    private val authRepository: com.neb.ians.data.repository.AuthRepository
) : ViewModel() {
    private val slug: String = savedStateHandle.get<String>("slug")?.let { URLDecoder.decode(it, "UTF-8") }.orEmpty()
    private val _uiState = MutableStateFlow(NewsDetailUiState(slug = slug))
    val uiState: StateFlow<NewsDetailUiState> = _uiState.asStateFlow()

    // One in-flight like per comment: rapid taps are ignored instead of
    // stacking server toggles that flip the liked state back and forth.
    private val processingCommentLikes = mutableSetOf<String>()

    init {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            _uiState.update { it.copy(isAuthenticated = token != null) }
        }
        load()
        collectCacheSignals()
    }

    /** Cache-first with silent background updates: when the repository's SWR
     * refresh lands fresher detail/comments, re-read them (cache-only). */
    @OptIn(FlowPreview::class)
    private fun collectCacheSignals() {
        viewModelScope.launch {
            cacheBus.signals
                .debounce(400)
                .collect { key ->
                    when (key) {
                        CacheBus.PREFIX_NEWS_DETAIL + slug ->
                            newsRepository.getAnnouncementDetail(slug, cacheOnly = true).onSuccess { detail ->
                                _uiState.update { it.copy(detail = detail, isLoading = false, error = null) }
                            }
                        CacheBus.PREFIX_NEWS_COMMENTS + slug ->
                            newsRepository.getComments(slug, cacheOnly = true).onSuccess { comments ->
                                _uiState.update { it.copy(comments = comments, commentsLoading = false) }
                            }
                    }
                }
        }
    }

    fun retry() = load(forceRefresh = true)

    fun onCommentDraftChange(value: String) {
        _uiState.update { it.copy(commentDraft = value.take(4000)) }
    }

    fun onThreadDraftChange(value: String) {
        _uiState.update { it.copy(threadDraft = value.take(4000)) }
    }

    fun setCommentSort(sort: String) {
        _uiState.update { it.copy(commentSort = sort) }
    }

    fun postComment() {
        val text = _uiState.value.commentDraft.trim()
        if (text.isBlank() || _uiState.value.isPostingComment) return
        viewModelScope.launch {
            _uiState.update { it.copy(isPostingComment = true) }
            newsRepository.postComment(slug, text)
                .onSuccess { comment ->
                    _uiState.update {
                        it.copy(
                            comments = it.comments.filterNot { current -> current.id == comment.id } + comment,
                            commentDraft = "",
                            isPostingComment = false
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(
                            isPostingComment = false,
                            snackbarMessage = error.message ?: "Couldn't post comment"
                        )
                    }
                }
        }
    }

    /** Thread composer: posts a reply under the given parent comment. */
    fun postThreadReply(parentCommentId: String, onSuccess: () -> Unit = {}) {
        val text = _uiState.value.threadDraft.trim()
        if (text.isBlank() || _uiState.value.isPostingComment) return
        viewModelScope.launch {
            _uiState.update { it.copy(isPostingComment = true) }
            newsRepository.postComment(slug, text, parentCommentId)
                .onSuccess { comment ->
                    _uiState.update { state ->
                        val bumped = state.comments.map { existing ->
                            if (existing.id == parentCommentId) {
                                existing.copy(childCount = existing.childCount + 1)
                            } else existing
                        }
                        state.copy(
                            comments = bumped.filterNot { current -> current.id == comment.id } + comment,
                            threadDraft = "",
                            isPostingComment = false
                        )
                    }
                    onSuccess()
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(
                            isPostingComment = false,
                            snackbarMessage = error.message ?: "Couldn't post reply"
                        )
                    }
                }
        }
    }

    fun toggleCommentLike(commentId: String) {
        if (processingCommentLikes.contains(commentId)) return
        val comment = _uiState.value.comments.firstOrNull { it.id == commentId } ?: return
        val wasLiked = comment.isThumbedUp
        val nextLiked = !wasLiked
        val nextCount = (comment.thumbsUpCount + if (nextLiked) 1 else -1).coerceAtLeast(0)
        processingCommentLikes.add(commentId)
        _uiState.update { state ->
            state.copy(comments = state.comments.map {
                if (it.id == commentId) it.copy(isThumbedUp = nextLiked, thumbsUpCount = nextCount) else it
            })
        }
        viewModelScope.launch {
            newsRepository.toggleCommentLike(commentId)
                .onSuccess { resp ->
                    // Reconcile with the server's truth (state + count).
                    _uiState.update { state ->
                        state.copy(comments = state.comments.map {
                            if (it.id == commentId) {
                                it.copy(
                                    isThumbedUp = resp.resolvedIsLiked,
                                    thumbsUpCount = resp.resolvedLikeCount
                                )
                            } else it
                        })
                    }
                }
                .onFailure { error ->
                    _uiState.update { state ->
                        state.copy(
                            comments = state.comments.map { if (it.id == commentId) comment else it },
                            snackbarMessage = error.message ?: "Couldn't update like"
                        )
                    }
                }
            processingCommentLikes.remove(commentId)
        }
    }

    fun deleteComment(commentId: String) {
        val current = _uiState.value.comments
        _uiState.update { state ->
            state.copy(comments = state.comments.filterNot { it.id == commentId })
        }
        viewModelScope.launch {
            newsRepository.deleteComment(commentId)
                .onFailure { error ->
                    _uiState.update {
                        it.copy(
                            comments = current,
                            snackbarMessage = error.message ?: "Couldn't delete comment"
                        )
                    }
                }
        }
    }

    fun consumeSnackbar() {
        _uiState.update { it.copy(snackbarMessage = null) }
    }

    private fun load(forceRefresh: Boolean = false) {
        if (slug.isBlank()) {
            _uiState.update { it.copy(isLoading = false, commentsLoading = false, error = "Blog post not found") }
            return
        }
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            newsRepository.getAnnouncementDetail(slug, forceRefresh)
                .onSuccess { detail -> _uiState.update { it.copy(detail = detail, isLoading = false, error = null) } }
                .onFailure { error -> _uiState.update { it.copy(isLoading = false, error = error.message ?: "Couldn't load blog post") } }
        }
        viewModelScope.launch {
            _uiState.update { it.copy(commentsLoading = true) }
            newsRepository.getComments(slug)
                .onSuccess { comments -> _uiState.update { it.copy(comments = comments, commentsLoading = false) } }
                .onFailure { _uiState.update { it.copy(commentsLoading = false) } }
        }
    }
}
