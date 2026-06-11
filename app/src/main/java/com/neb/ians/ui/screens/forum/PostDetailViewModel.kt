package com.neb.ians.ui.screens.forum

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.ui.components.PollUi
import com.neb.ians.ui.components.toPollUi
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import javax.inject.Inject

data class PostDetailUiState(
    val post: ApiPost? = null,
    val replies: List<ApiReply> = emptyList(),
    val poll: PollUi? = null,
    val replySort: String = "oldest",
    val isLoading: Boolean = true,
    val isVoting: Boolean = false,
    val error: String? = null,
    val snackbarMessage: String? = null,
    val currentUserId: String? = null
) {
    /** Top-level replies in the selected sort order. */
    val topLevelReplies: List<ApiReply>
        get() {
            val topLevel = replies.filter { it.parentReplyId.isNullOrBlank() }
            return when (replySort) {
                "newest" -> topLevel.sortedByDescending { it.createdAt }
                "top" -> topLevel.sortedWith(
                    compareByDescending<ApiReply> { it.thumbsUpCount }.thenBy { it.createdAt }
                )
                else -> topLevel.sortedBy { it.createdAt } // oldest
            }
        }

    /** Children of a given reply, oldest first. */
    fun childrenOf(replyId: String): List<ApiReply> =
        replies.filter { it.parentReplyId == replyId }.sortedBy { it.createdAt }
}

@HiltViewModel
class PostDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository,
    private val authRepository: AuthRepository,
    private val realtimeClient: RealtimeClient
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""

    private val _state = MutableStateFlow(PostDetailUiState())
    private var unsubscribePost: (() -> Unit)? = null
    private val lenientJson = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    val uiState: StateFlow<PostDetailUiState> = combine(
        _state,
        authRepository.currentUserIdFlow
    ) { state, userId ->
        state.copy(currentUserId = userId)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), PostDetailUiState())

    init {
        loadPost()
        unsubscribePost = realtimeClient.subscribe("post.$postId")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                if (event.channel == "forum.post.$postId" || event.channel == "post.$postId") {
                    handleRealtimeEvent(event.event, event.data)
                }
            }
        }
    }

    override fun onCleared() {
        unsubscribePost?.invoke()
        unsubscribePost = null
        super.onCleared()
    }

    private fun handleRealtimeEvent(event: String, data: JsonObject?) {
        try {
            val payload = data ?: return
            when (event) {
                "reply.created" -> {
                    val reply = try {
                        lenientJson.decodeFromJsonElement(ApiReply.serializer(), payload)
                    } catch (_: Exception) {
                        null
                    }
                    if (reply != null) {
                        _state.update { state ->
                            if (state.replies.any { it.id == reply.id }) state
                            else state.copy(replies = state.replies + reply)
                        }
                    } else {
                        quietRefreshReplies()
                    }
                }
                "reply.like_changed" -> {
                    val replyId = payload.stringField("reply_id") ?: return
                    val count = payload.intField("thumbs_up_count") ?: return
                    _state.update { state ->
                        state.copy(replies = state.replies.map { reply ->
                            if (reply.id == replyId) reply.copy(thumbsUpCount = count) else reply
                        })
                    }
                }
                "post.like_changed" -> {
                    val changedId = payload.stringField("post_id") ?: return
                    val count = payload.intField("thumbs_up_count") ?: return
                    if (changedId != postId) return
                    _state.update { state ->
                        state.copy(post = state.post?.copy(thumbsUpCount = count))
                    }
                }
                "reply.deleted" -> {
                    val replyId = payload.stringField("reply_id") ?: payload.stringField("id") ?: return
                    _state.update { state ->
                        state.copy(replies = state.replies.filterNot { it.id == replyId || it.parentReplyId == replyId })
                    }
                }
            }
        } catch (_: Exception) {
        }
    }

    private fun quietRefreshReplies() {
        viewModelScope.launch {
            forumRepository.getReplies(postId).onSuccess { replies ->
                _state.update { it.copy(replies = replies) }
            }
        }
    }

    private fun loadPost() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            forumRepository.getPost(postId)
                .onSuccess { post ->
                    _state.update { it.copy(post = post, poll = post.poll?.toPollUi()) }
                }
                .onFailure { e ->
                    _state.update { it.copy(error = e.message ?: "Failed to load post", isLoading = false) }
                }
            forumRepository.getReplies(postId)
                .onSuccess { replies ->
                    _state.update { it.copy(replies = replies, isLoading = false) }
                }
                .onFailure {
                    _state.update { it.copy(isLoading = false) }
                }
        }
    }

    fun refresh() = loadPost()

    fun setReplySort(sort: String) {
        _state.update { it.copy(replySort = sort) }
    }

    // ----- Likes (optimistic) -----

    fun toggleThumbsUp() {
        val current = _state.value.post ?: return
        val optimistic = current.copy(
            isThumbedUp = !current.isThumbedUp,
            thumbsUpCount = (current.thumbsUpCount + if (current.isThumbedUp) -1 else 1).coerceAtLeast(0)
        )
        _state.update { it.copy(post = optimistic) }
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    _state.update { state ->
                        state.copy(post = state.post?.copy(
                            thumbsUpCount = response.thumbsUpCount,
                            isThumbedUp = response.isThumbedUp
                        ))
                    }
                }
                .onFailure { _state.update { it.copy(post = current) } }
        }
    }

    fun toggleReplyThumbsUp(replyId: String) {
        val current = _state.value.replies.firstOrNull { it.id == replyId } ?: return
        val optimistic = current.copy(
            isThumbedUp = !current.isThumbedUp,
            thumbsUpCount = (current.thumbsUpCount + if (current.isThumbedUp) -1 else 1).coerceAtLeast(0)
        )
        replaceReply(optimistic)
        viewModelScope.launch {
            forumRepository.toggleLikeReply(replyId)
                .onSuccess { response ->
                    _state.update { state ->
                        state.copy(replies = state.replies.map { reply ->
                            if (reply.id == replyId) {
                                reply.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp)
                            } else reply
                        })
                    }
                }
                .onFailure { replaceReply(current) }
        }
    }

    // ----- Bookmarks (optimistic) -----

    fun togglePostBookmark() {
        val current = _state.value.post ?: return
        val optimistic = current.copy(isBookmarked = !(current.isBookmarked == true))
        _state.update { it.copy(post = optimistic) }
        viewModelScope.launch {
            forumRepository.toggleBookmark("post", postId)
                .onSuccess { response ->
                    _state.update { state ->
                        state.copy(post = state.post?.copy(isBookmarked = response.isBookmarked))
                    }
                }
                .onFailure { _state.update { it.copy(post = current) } }
        }
    }

    fun toggleReplyBookmark(replyId: String) {
        val current = _state.value.replies.firstOrNull { it.id == replyId } ?: return
        val optimistic = current.copy(isBookmarked = !(current.isBookmarked == true))
        replaceReply(optimistic)
        viewModelScope.launch {
            forumRepository.toggleBookmark("reply", replyId)
                .onSuccess { response ->
                    _state.update { state ->
                        state.copy(replies = state.replies.map { reply ->
                            if (reply.id == replyId) reply.copy(isBookmarked = response.isBookmarked) else reply
                        })
                    }
                }
                .onFailure { replaceReply(current) }
        }
    }

    // ----- Poll voting -----

    fun votePoll(optionIds: List<String>) {
        val poll = _state.value.poll ?: return
        if (poll.hasVoted || poll.isExpired || optionIds.isEmpty() || _state.value.isVoting) return
        _state.update { it.copy(isVoting = true) }
        viewModelScope.launch {
            forumRepository.votePoll(poll.id, optionIds, poll.allowMultiple)
                .onSuccess { response ->
                    _state.update { state ->
                        state.copy(
                            poll = response.toPollUi(votedIds = optionIds.toSet()),
                            isVoting = false
                        )
                    }
                }
                .onFailure {
                    _state.update { it.copy(isVoting = false, snackbarMessage = "Couldn't submit vote") }
                }
        }
    }

    // ----- Edit / archive / delete -----

    fun editPost(title: String, content: String) {
        viewModelScope.launch {
            forumRepository.updatePost(postId, title = title, content = content)
                .onSuccess { updated ->
                    _state.update { it.copy(post = updated, poll = updated.poll?.toPollUi() ?: it.poll) }
                }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't save changes") } }
        }
    }

    fun editReply(replyId: String, content: String) {
        viewModelScope.launch {
            forumRepository.updateReply(replyId, content)
                .onSuccess { updated -> replaceReply(updated) }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't save changes") } }
        }
    }

    fun archivePost() {
        val current = _state.value.post ?: return
        viewModelScope.launch {
            forumRepository.archivePost(postId)
                .onSuccess {
                    _state.update { state ->
                        state.copy(post = state.post?.copy(isArchived = !(current.isArchived == true)))
                    }
                }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't archive post") } }
        }
    }

    fun archiveReply(replyId: String) {
        val current = _state.value.replies.firstOrNull { it.id == replyId } ?: return
        viewModelScope.launch {
            forumRepository.archiveReply(replyId)
                .onSuccess {
                    replaceReply(current.copy(isArchived = !(current.isArchived == true)))
                }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't archive reply") } }
        }
    }

    fun deletePost(onDeleted: () -> Unit) {
        viewModelScope.launch {
            forumRepository.deletePost(postId)
                .onSuccess { onDeleted() }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't delete post") } }
        }
    }

    fun deleteReply(replyId: String) {
        viewModelScope.launch {
            forumRepository.deleteReply(replyId)
                .onSuccess {
                    _state.update { state ->
                        state.copy(
                            replies = state.replies.filterNot { it.id == replyId || it.parentReplyId == replyId },
                            snackbarMessage = "Reply deleted"
                        )
                    }
                }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't delete reply") } }
        }
    }

    // ----- Reports -----

    fun report(targetType: String, targetId: String, reason: String, description: String) {
        viewModelScope.launch {
            forumRepository.createReport(targetType, targetId, reason, description)
                .onSuccess { _state.update { it.copy(snackbarMessage = "Report submitted") } }
                .onFailure { _state.update { it.copy(snackbarMessage = "Couldn't submit report") } }
        }
    }

    fun consumeSnackbar() {
        _state.update { it.copy(snackbarMessage = null) }
    }

    private fun replaceReply(updated: ApiReply) {
        _state.update { state ->
            state.copy(replies = state.replies.map { if (it.id == updated.id) updated else it })
        }
    }
}
