package com.neb.ians.ui.screens.forum

import android.net.Uri
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
    val mediaAttachments: List<PendingForumAttachment> = emptyList(),
    val isAnonymous: Boolean = false,
    val mentionSuggestions: List<ApiUserSearchResult> = emptyList()
)

@HiltViewModel
class ReplyViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository,
    private val mediaUploadHelper: ForumMediaUploadHelper
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
            val results = mutableListOf<ApiUserSearchResult>()
            if (query == "all") {
                results.add(ApiUserSearchResult(id = "@all", username = "all", displayName = "Everyone"))
            }
            forumRepository.searchUsers(query)
                .onSuccess { users -> results.addAll(users.take(8)) }
            if (mentionQueryAt(_uiState.value.content) == query) {
                _uiState.update { it.copy(mentionSuggestions = results) }
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

    // ----- Media attachments (video / audio / files) -----

    fun setAnonymous(anonymous: Boolean) {
        _uiState.update { it.copy(isAnonymous = anonymous) }
    }

    fun addMediaAttachments(uris: List<Uri>) {
        uris.forEach { uri -> addMediaAttachment(uri) }
    }

    fun addMediaAttachment(uri: Uri?) {
        if (uri == null) return
        val state = _uiState.value
        if (state.mediaAttachments.size >= ForumMediaUploadHelper.MAX_ATTACHMENTS) {
            _uiState.update { it.copy(error = "Maximum ${ForumMediaUploadHelper.MAX_ATTACHMENTS} attachments") }
            return
        }
        val kind = mediaUploadHelper.guessKind(uri)
        if (kind == "video" && state.mediaAttachments.any { it.kind == "video" }) {
            _uiState.update { it.copy(error = "Maximum 1 video per reply") }
            return
        }
        val size = mediaUploadHelper.sizeOf(uri)
        if (size > ForumMediaUploadHelper.limitFor(kind)) {
            _uiState.update { it.copy(error = ForumMediaUploadHelper.limitLabel(kind)) }
            return
        }
        val pending = PendingForumAttachment(
            name = mediaUploadHelper.displayName(uri),
            kind = kind,
            sizeBytes = size,
            uri = uri
        )
        _uiState.update { it.copy(mediaAttachments = it.mediaAttachments + pending, error = null) }
        viewModelScope.launch {
            val result = mediaUploadHelper.upload(uri, kind, pending.name)
            _uiState.update { current ->
                current.copy(mediaAttachments = current.mediaAttachments.map { att ->
                    if (att.localId != pending.localId) att
                    else result.fold(
                        onSuccess = { descriptor -> att.copy(uploading = false, uploaded = descriptor) },
                        onFailure = { e -> att.copy(uploading = false, error = e.message ?: "Upload failed") }
                    )
                })
            }
            result.exceptionOrNull()?.let { e ->
                _uiState.update { it.copy(error = e.message ?: "Couldn't upload ${pending.name}") }
            }
        }
    }

    fun removeMediaAttachment(localId: String) {
        _uiState.update { current ->
            current.copy(mediaAttachments = current.mediaAttachments.filterNot { it.localId == localId })
        }
    }

    fun submitReply(onSuccess: () -> Unit) {
        val state = _uiState.value
        val content = state.content.text.trim()
        if (content.isBlank()) return
        if (state.mediaAttachments.any { it.uploading }) {
            _uiState.update { it.copy(error = "Wait for attachments to finish uploading") }
            return
        }
        val attachments = state.mediaAttachments.mapNotNull { it.uploaded }

        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, error = null) }
            forumRepository.createReply(
                postId = postId,
                content = content,
                parentReplyId = replyToId,
                isAnonymous = state.isAnonymous,
                attachments = attachments
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
