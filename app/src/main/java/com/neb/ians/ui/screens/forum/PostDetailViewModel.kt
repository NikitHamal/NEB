package com.neb.ians.ui.screens.forum

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PostDetailUiState(
    val post: ApiPost? = null,
    val replies: List<ApiReply> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class PostDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""

    private val _uiState = MutableStateFlow(PostDetailUiState())
    val uiState: StateFlow<PostDetailUiState> = _uiState.asStateFlow()

    init {
        loadPost()
    }

    private fun loadPost() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            forumRepository.getPost(postId)
                .onSuccess { post ->
                    _uiState.update { it.copy(post = post) }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(error = e.message ?: "Failed to load post", isLoading = false) }
                }
            forumRepository.getReplies(postId)
                .onSuccess { replies ->
                    _uiState.update { it.copy(replies = replies, isLoading = false) }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false) }
                }
        }
    }

    fun toggleThumbsUp() {
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    _uiState.value.post?.let { post ->
                        _uiState.update {
                            it.copy(post = post.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp))
                        }
                    }
                }
        }
    }

    fun toggleReplyThumbsUp(replyId: String) {
        viewModelScope.launch {
            forumRepository.toggleLikeReply(replyId)
                .onSuccess { response ->
                    val updatedReplies = _uiState.value.replies.map { reply ->
                        if (reply.id == replyId) {
                            reply.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp)
                        } else reply
                    }
                    _uiState.update { it.copy(replies = updatedReplies) }
                }
        }
    }

    fun refresh() {
        loadPost()
    }
}