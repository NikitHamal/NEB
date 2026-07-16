package com.neb.ians.ui.screens.news

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.news.NewsComment
import com.neb.ians.data.news.NewsDetail
import com.neb.ians.data.repository.NewsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.net.URLDecoder
import javax.inject.Inject

data class NewsDetailUiState(
    val slug: String = "",
    val detail: NewsDetail? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val comments: List<NewsComment> = emptyList(),
    val commentsLoading: Boolean = true,
    val commentDraft: String = "",
    val isPostingComment: Boolean = false,
    val snackbarMessage: String? = null
)

@HiltViewModel
class NewsDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val newsRepository: NewsRepository
) : ViewModel() {
    private val slug: String = savedStateHandle.get<String>("slug")?.let { URLDecoder.decode(it, "UTF-8") }.orEmpty()
    private val _uiState = MutableStateFlow(NewsDetailUiState(slug = slug))
    val uiState: StateFlow<NewsDetailUiState> = _uiState.asStateFlow()

    init { load() }

    fun retry() = load(forceRefresh = true)

    fun onCommentDraftChange(value: String) {
        _uiState.update { it.copy(commentDraft = value.take(4000)) }
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
