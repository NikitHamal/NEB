package com.neb.ians.ui.screens.forum

import android.net.Uri
import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiMediaAttachmentInput
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.CacheBus
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.ui.components.PollUi
import com.neb.ians.ui.components.toPollUi
import com.neb.ians.ui.components.applyMention
import com.neb.ians.ui.components.mentionQueryAt
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
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

    /** Children and descendants of a given reply, oldest first. */
    fun childrenOf(replyId: String): List<ApiReply> {
        val result = mutableListOf<ApiReply>()
        val descendants = mutableSetOf<String>()
        var addedAny: Boolean
        do {
            addedAny = false
            for (r in replies) {
                if (r.parentReplyId != null && !descendants.contains(r.id)) {
                    if (r.parentReplyId == replyId || descendants.contains(r.parentReplyId)) {
                        descendants.add(r.id)
                        result.add(r)
                        addedAny = true
                    }
                }
            }
        } while (addedAny)
        return result.sortedBy { it.createdAt }
    }
}

@HiltViewModel
class PostDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository,
    private val authRepository: AuthRepository,
    private val realtimeClient: RealtimeClient,
    private val cacheBus: CacheBus,
    private val mediaUploadHelper: ForumMediaUploadHelper
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""
    private val cachedPost = forumRepository.peekPost(postId)
    private val cachedReplies = forumRepository.peekReplies(postId).orEmpty()

    private val _state = MutableStateFlow(
        PostDetailUiState(
            post = cachedPost,
            replies = cachedReplies,
            poll = cachedPost?.poll?.toPollUi(),
            isLoading = cachedPost == null
        )
    )
    private var unsubscribePost: (() -> Unit)? = null
    private var isPostLikeBusy = false
    private var isPostBookmarkBusy = false
    private val processingReplyLikes = mutableSetOf<String>()
    private val processingReplyBookmarks = mutableSetOf<String>()
    private val lenientJson = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    val uiState: StateFlow<PostDetailUiState> = combine(
        _state,
        authRepository.currentUserIdFlow
    ) { state, userId ->
        state.copy(currentUserId = userId)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), _state.value)

    init {
        loadPost()
        unsubscribePost = realtimeClient.subscribe("forum.post.$postId")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                if (event.channel == "forum.post.$postId" || event.channel == "post.$postId") {
                    handleRealtimeEvent(event.event, event.data)
                }
            }
        }
        collectCacheSignals()
    }

    /**
     * Cache-first with silent background updates: when the repository's SWR
     * refresh (or anyone's realtime write) lands fresher post/reply data in
     * the offline cache, this flow re-reads it without user interaction.
     */
    @OptIn(FlowPreview::class)
    private fun collectCacheSignals() {
        viewModelScope.launch {
            cacheBus.signals
                .debounce(400)
                .collect { key ->
                    when (key) {
                        CacheBus.PREFIX_POST + postId ->
                            forumRepository.getPost(postId, cacheOnly = true).onSuccess { post ->
                                _state.update { it.copy(post = post, poll = post.poll?.toPollUi()) }
                            }
                        CacheBus.PREFIX_POST_REPLIES + postId ->
                            forumRepository.getReplies(postId, cacheOnly = true).onSuccess { replies ->
                                _state.update { it.copy(replies = replies, isLoading = false) }
                            }
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
                    if (processingReplyLikes.contains(replyId)) return
                    val isThumbedUp = payload.boolField("isThumbedUp")
                    _state.update { state ->
                        state.copy(replies = state.replies.map { reply ->
                            if (reply.id == replyId) {
                                if (isThumbedUp != null) reply.copy(thumbsUpCount = count, isThumbedUp = isThumbedUp)
                                else reply.copy(thumbsUpCount = count)
                            } else reply
                        })
                    }
                }
                "post.like_changed" -> {
                    val changedId = payload.stringField("post_id") ?: return
                    val count = payload.intField("thumbs_up_count") ?: return
                    if (changedId != postId) return
                    if (isPostLikeBusy) return
                    val isThumbedUp = payload.boolField("isThumbedUp")
                    _state.update { state ->
                        if (isThumbedUp != null) state.copy(post = state.post?.copy(thumbsUpCount = count, isThumbedUp = isThumbedUp))
                        else state.copy(post = state.post?.copy(thumbsUpCount = count))
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
            forumRepository.getReplies(postId, forceRefresh = true).onSuccess { replies ->
                _state.update { it.copy(replies = replies) }
            }
        }
    }

    private fun loadPost(forceRefresh: Boolean = false): Job =
        viewModelScope.launch {
            val hasPost = _state.value.post != null
            _state.update { it.copy(isLoading = !hasPost, error = null) }

            if (!forceRefresh) {
                forumRepository.getPost(postId, cacheOnly = true)
                    .onSuccess { post ->
                        _state.update { it.copy(post = post, poll = post.poll?.toPollUi(), error = null) }
                    }
                forumRepository.getReplies(postId, cacheOnly = true)
                    .onSuccess { replies ->
                        _state.update { it.copy(replies = replies, isLoading = false) }
                    }
            }

            if (!forceRefresh && !hasPost) {
                forumRepository.viewPost(postId)
            }
            forumRepository.getPost(postId, forceRefresh = forceRefresh)
                .onSuccess { post ->
                    _state.update { it.copy(post = post, poll = post.poll?.toPollUi(), error = null) }
                }
                .onFailure { e ->
                    val message = ApiErrorMapper.mapException(e)
                    _state.update {
                        if (it.post == null) it.copy(error = message, isLoading = false)
                        else it.copy(snackbarMessage = message, isLoading = false)
                    }
                }
            forumRepository.getReplies(postId, forceRefresh = forceRefresh)
                .onSuccess { replies ->
                    _state.update { it.copy(replies = replies, isLoading = false) }
                }
                .onFailure {
                    _state.update { it.copy(isLoading = false) }
                }
        }

    fun refresh(): Job = loadPost(forceRefresh = true)

    fun setReplySort(sort: String) {
        _state.update { it.copy(replySort = sort) }
    }

    // ----- Likes (optimistic) -----

    fun toggleThumbsUp() {
        if (isPostLikeBusy) return
        val current = _state.value.post ?: return
        isPostLikeBusy = true
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
            isPostLikeBusy = false
        }
    }

    fun toggleReplyThumbsUp(replyId: String) {
        if (processingReplyLikes.contains(replyId)) return
        val current = _state.value.replies.firstOrNull { it.id == replyId } ?: return
        processingReplyLikes.add(replyId)
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
            processingReplyLikes.remove(replyId)
        }
    }

    // ----- Bookmarks (optimistic) -----

    fun togglePostBookmark() {
        if (isPostBookmarkBusy) return
        val current = _state.value.post ?: return
        isPostBookmarkBusy = true
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
            isPostBookmarkBusy = false
        }
    }

    fun toggleReplyBookmark(replyId: String) {
        if (processingReplyBookmarks.contains(replyId)) return
        val current = _state.value.replies.firstOrNull { it.id == replyId } ?: return
        processingReplyBookmarks.add(replyId)
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
            processingReplyBookmarks.remove(replyId)
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

    // ----- Reply Compose State and Methods -----
    private val _mainReplyText = MutableStateFlow(TextFieldValue(""))
    val mainReplyText: StateFlow<TextFieldValue> = _mainReplyText.asStateFlow()

    private val _mainMentionSuggestions = MutableStateFlow<List<ApiUserSearchResult>>(emptyList())
    val mainMentionSuggestions: StateFlow<List<ApiUserSearchResult>> = _mainMentionSuggestions.asStateFlow()

    private var mainMentionJob: Job? = null

    private val _threadReplyText = MutableStateFlow(TextFieldValue(""))
    val threadReplyText: StateFlow<TextFieldValue> = _threadReplyText.asStateFlow()

    private val _threadMentionSuggestions = MutableStateFlow<List<ApiUserSearchResult>>(emptyList())
    val threadMentionSuggestions: StateFlow<List<ApiUserSearchResult>> = _threadMentionSuggestions.asStateFlow()

    private var threadMentionJob: Job? = null

    private val _isSubmittingReply = MutableStateFlow(false)
    val isSubmittingReply: StateFlow<Boolean> = _isSubmittingReply.asStateFlow()

    // ----- Inline composer media attachments + anonymous mode -----
    // Shared by the main bottom-bar composer and the thread-reply composers:
    // only one of them is actively used at a time on this screen.

    private val _mediaAttachments = MutableStateFlow<List<PendingForumAttachment>>(emptyList())
    val mediaAttachments: StateFlow<List<PendingForumAttachment>> = _mediaAttachments.asStateFlow()

    private val _composerAnonymous = MutableStateFlow(false)
    val composerAnonymous: StateFlow<Boolean> = _composerAnonymous.asStateFlow()

    fun setComposerAnonymous(anonymous: Boolean) {
        _composerAnonymous.value = anonymous
    }

    fun addMediaAttachments(uris: List<Uri>) {
        uris.forEach { uri -> addMediaAttachment(uri) }
    }

    fun addMediaAttachment(uri: Uri?) {
        if (uri == null) return
        val current = _mediaAttachments.value
        if (current.size >= ForumMediaUploadHelper.MAX_ATTACHMENTS) {
            _state.update { it.copy(snackbarMessage = "Maximum ${ForumMediaUploadHelper.MAX_ATTACHMENTS} attachments") }
            return
        }
        val kind = mediaUploadHelper.guessKind(uri)
        if (kind == "video" && current.any { it.kind == "video" }) {
            _state.update { it.copy(snackbarMessage = "Maximum 1 video per reply") }
            return
        }
        val size = mediaUploadHelper.sizeOf(uri)
        if (size > ForumMediaUploadHelper.limitFor(kind)) {
            _state.update { it.copy(snackbarMessage = ForumMediaUploadHelper.limitLabel(kind)) }
            return
        }
        val pending = PendingForumAttachment(
            name = mediaUploadHelper.displayName(uri),
            kind = kind,
            sizeBytes = size,
            uri = uri
        )
        _mediaAttachments.update { it + pending }
        viewModelScope.launch {
            val result = mediaUploadHelper.upload(uri, kind, pending.name)
            _mediaAttachments.update { attachments ->
                attachments.map { att ->
                    if (att.localId != pending.localId) att
                    else result.fold(
                        onSuccess = { descriptor -> att.copy(uploading = false, uploaded = descriptor) },
                        onFailure = { e -> att.copy(uploading = false, error = e.message ?: "Upload failed") }
                    )
                }
            }
            result.exceptionOrNull()?.let { e ->
                _state.update { it.copy(snackbarMessage = e.message ?: "Couldn't upload ${pending.name}") }
            }
        }
    }

    fun removeMediaAttachment(localId: String) {
        _mediaAttachments.update { attachments -> attachments.filterNot { it.localId == localId } }
    }

    fun onMainReplyChange(value: TextFieldValue) {
        if (value.text.length > 10000) return
        _mainReplyText.value = value
        
        mainMentionJob?.cancel()
        val query = mentionQueryAt(value)
        if (query == null) {
            _mainMentionSuggestions.value = emptyList()
            return
        }
        mainMentionJob = viewModelScope.launch {
            delay(300)
            val results = mutableListOf<ApiUserSearchResult>()
            if (query == "all") {
                results.add(ApiUserSearchResult(id = "@all", username = "all", displayName = "Everyone"))
            }
            forumRepository.searchUsers(query)
                .onSuccess { users -> results.addAll(users.take(8)) }
            if (mentionQueryAt(_mainReplyText.value) == query) {
                _mainMentionSuggestions.value = results
            }
        }
    }

    fun selectMainMention(user: ApiUserSearchResult) {
        _mainReplyText.value = applyMention(_mainReplyText.value, user.username)
        _mainMentionSuggestions.value = emptyList()
    }

    fun onThreadReplyChange(value: TextFieldValue) {
        if (value.text.length > 10000) return
        _threadReplyText.value = value

        threadMentionJob?.cancel()
        val query = mentionQueryAt(value)
        if (query == null) {
            _threadMentionSuggestions.value = emptyList()
            return
        }
        threadMentionJob = viewModelScope.launch {
            delay(300)
            val results = mutableListOf<ApiUserSearchResult>()
            if (query == "all") {
                results.add(ApiUserSearchResult(id = "@all", username = "all", displayName = "Everyone"))
            }
            forumRepository.searchUsers(query)
                .onSuccess { users -> results.addAll(users.take(8)) }
            if (mentionQueryAt(_threadReplyText.value) == query) {
                _threadMentionSuggestions.value = results
            }
        }
    }

    fun selectThreadMention(user: ApiUserSearchResult) {
        _threadReplyText.value = applyMention(_threadReplyText.value, user.username)
        _threadMentionSuggestions.value = emptyList()
    }

    fun submitReply(
        content: String,
        parentReplyId: String?,
        onSuccess: () -> Unit
    ) {
        if (content.isBlank() || _isSubmittingReply.value) return
        val staged = _mediaAttachments.value
        if (staged.any { it.uploading }) {
            _state.update { it.copy(snackbarMessage = "Wait for attachments to finish uploading") }
            return
        }
        val attachments: List<ApiMediaAttachmentInput> = staged.mapNotNull { it.uploaded }
        val isAnonymous = _composerAnonymous.value
        viewModelScope.launch {
            _isSubmittingReply.value = true
            forumRepository.createReply(
                postId = postId,
                content = content,
                parentReplyId = parentReplyId,
                isAnonymous = isAnonymous,
                attachments = attachments
            ).onSuccess { reply ->
                _isSubmittingReply.value = false
                _mediaAttachments.value = emptyList()
                if (parentReplyId.isNullOrBlank()) {
                    _mainReplyText.value = TextFieldValue("")
                } else {
                    _threadReplyText.value = TextFieldValue("")
                }
                // Add the newly created reply to state if not already there,
                // matching the websocket event.
                _state.update { state ->
                    if (state.replies.any { it.id == reply.id }) state
                    else state.copy(replies = state.replies + reply)
                }
                onSuccess()
            }.onFailure { e ->
                _isSubmittingReply.value = false
                _state.update { it.copy(snackbarMessage = ApiErrorMapper.mapException(e)) }
            }
        }
    }
}
