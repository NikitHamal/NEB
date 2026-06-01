package com.neb.ians.ui.screens.forum

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ReplyUiState(
    val content: String = "",
    val isSubmitting: Boolean = false,
    val postTitle: String = "",
    val error: String? = null
)

@HiltViewModel
class ReplyViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""
    private val replyToId: String? = savedStateHandle.get<String>("replyToId")?.takeIf { it != "none" }

    private val _uiState = MutableStateFlow(ReplyUiState())
    val uiState: StateFlow<ReplyUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            forumRepository.getPost(postId)
                .onSuccess { post ->
                    _uiState.update { it.copy(postTitle = post.title) }
                }
        }
    }

    fun onContentChange(content: String) {
        _uiState.update { it.copy(content = content) }
    }

    fun submitReply(onSuccess: () -> Unit) {
        val content = _uiState.value.content
        if (content.isBlank()) return

        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, error = null) }
            forumRepository.createReply(
                postId = postId,
                content = content,
                parentReplyId = replyToId
            ).onSuccess {
                _uiState.update { it.copy(isSubmitting = false) }
                onSuccess()
            }.onFailure { e ->
                _uiState.update { it.copy(isSubmitting = false, error = e.message ?: "Failed to submit reply") }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}