package com.neb.ians.ui.screens.forum

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PostDetailUiState(
    val post: ForumPostEntity? = null,
    val replies: List<ForumReplyEntity> = emptyList(),
    val isLoading: Boolean = true
)

@HiltViewModel
class PostDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""

    val uiState: StateFlow<PostDetailUiState> = combine(
        forumRepository.getPostById(postId),
        forumRepository.getRepliesForPost(postId)
    ) { post, replies ->
        PostDetailUiState(
            post = post,
            replies = replies.sortedByDescending { it.createdAt },
            isLoading = false
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), PostDetailUiState())

    fun toggleThumbsUp() {
        viewModelScope.launch {
            forumRepository.toggleThumbsUp(postId)
        }
    }

    fun toggleReplyThumbsUp(replyId: String) {
        viewModelScope.launch {
            forumRepository.toggleReplyThumbsUp(replyId)
        }
    }
}
