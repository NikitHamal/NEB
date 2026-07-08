package com.neb.ians.ui.screens.forum

import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.ui.components.applyMention
import com.neb.ians.ui.components.mentionQueryAt
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

const val MAX_REPLY_CONTENT = 10_000

data class ReplyUiState(
    val content: TextFieldValue = TextFieldValue(""),
    val isSubmitting: Boolean = false,
    val postTitle: String = "",
    val error: String? = null,
    val mentionSuggestions: List<ApiUserSearchResult> = emptyList()
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

    private var mentionJob: Job? = null

    init {
        viewModelScope.launch {
            forumRepository.getPost(postId)
                .onSuccess { post ->
                    _uiState.update { it.copy(postTitle = post.title) }
                }
        }
    }

    fun onContentChange(content: TextFieldValue) {
        if (content.text.length > MAX_REPLY_CONTENT) return
        _uiState.update { it.copy(content = content) }
        scheduleMentionSearch(content)
    }

    private fun scheduleMentionSearch(content: TextFieldValue) {
        mentionJob?.cancel()
        val query = mentionQueryAt(content)
        if (query == null) {
            if (_uiState.value.mentionSuggestions.isNotEmpty()) {
                _uiState.update { it.copy(mentionSuggestions = emptyList()) }
            }
            return
        }
        mentionJob = viewModelScope.launch {
            delay(300)
            forumRepository.searchUsers(query)
                .onSuccess { users ->
                    if (mentionQueryAt(_uiState.value.content) == query) {
                        _uiState.update { it.copy(mentionSuggestions = users.take(8)) }
                    }
                }
                .onFailure {
                    _uiState.update { it.copy(mentionSuggestions = emptyList()) }
                }
        }
    }

    fun selectMention(user: ApiUserSearchResult) {
        _uiState.update {
            it.copy(
                content = applyMention(it.content, user.username),
                mentionSuggestions = emptyList()
            )
        }
    }

    fun submitReply(onSuccess: () -> Unit) {
        val content = _uiState.value.content.text.trim()
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
                _uiState.update { it.copy(isSubmitting = false, error = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}
