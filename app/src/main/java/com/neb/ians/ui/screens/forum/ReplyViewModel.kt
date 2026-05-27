package com.neb.ians.ui.screens.forum

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ReplyUiState(
    val content: String = "",
    val isSubmitting: Boolean = false,
    val postTitle: String = ""
)

@HiltViewModel
class ReplyViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository,
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""
    private val replyToId: String? = savedStateHandle.get<String>("replyToId")?.takeIf { it != "none" }

    private val _uiState = MutableStateFlow(ReplyUiState())
    val uiState: StateFlow<ReplyUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            forumRepository.getPostById(postId).collect { post ->
                _uiState.update { it.copy(postTitle = post?.title ?: "") }
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
            _uiState.update { it.copy(isSubmitting = true) }
            val userName = settingsRepository.userName.first()
            forumRepository.createReply(
                postId = postId,
                content = content,
                authorName = userName,
                parentReplyId = replyToId
            )
            _uiState.update { it.copy(isSubmitting = false) }
            onSuccess()
        }
    }
}
