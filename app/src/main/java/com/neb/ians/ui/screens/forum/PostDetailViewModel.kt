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
import com.neb.ians.ui.components.PostReachHints
import com.neb.ians.data.api.ApiPoll
import com.neb.ians.data.api.ApiPollCreate
import com.neb.ians.ui.components.applyMention
import com.neb.ians.ui.components.formatVoiceTime
import com.neb.ians.ui.components.mentionQueryAt
import dagger.hilt.android.lifecycle.HiltViewModel
import java.io.File
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.intOrNull
import javax.inject.Inject

internal fun JsonObject.stringField(key: String): String? =
    try { (this[key] as? JsonPrimitive)?.contentOrNull } catch (_: Exception) { null }

internal fun JsonObject.intField(key: String): Int? =
    try { (this[key] as? JsonPrimitive)?.intOrNull } catch (_: Exception) { null }

internal fun JsonObject.boolField(key: String): Boolean? =
    try { (this[key] as? JsonPrimitive)?.let { it.contentOrNull?.toBooleanStrictOrNull() } } catch (_: Exception) { null }

/** Lower ranks first; the same table the web uses for its reply list. */
internal fun replyRank(label: String): Int = when (label) {
    "accepted" -> 0
    "correct" -> 1
    "helpful" -> 2
    "partial" -> 3
    "incorrect" -> 5
    "spam" -> 6
    else -> 4
}

data class PostDetailUiState(
    val post: ApiPost? = null,
    val replies: List<ApiReply> = emptyList(),
    val poll: PollUi? = null,
    val replySort: String = "oldest",
    val isLoading: Boolean = true,
    val busyPollId: String? = null,
    val error: String? = null,
    val snackbarMessage: String? = null,
    val currentUserId: String? = null
) {
    /** Whether any reply carries the accepted label: the web's `post.isResolved`. */
    val isSolved: Boolean get() = replies.any { it.label == "accepted" }

    /**
     * Top-level replies in the selected sort order, marked ones first like the web: accepted,
     * correct, helpful, partly correct, then unmarked; incorrect and spam sink. The sort is
     * stable, so the chosen order still decides within each group.
     */
    val topLevelReplies: List<ApiReply>
        get() {
            val topLevel = replies.filter { it.parentReplyId.isNullOrBlank() }
            val ordered = when (replySort) {
                "newest" -> topLevel.sortedByDescending { it.createdAt }
                "top" -> topLevel.sortedWith(
                    compareByDescending<ApiReply> { it.thumbsUpCount }.thenBy { it.createdAt }
                )
                else -> topLevel.sortedBy { it.createdAt } // oldest
            }
            return ordered.sortedBy { replyRank(it.label) }
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

    /** Who a reply goes out as, for the identity avatar in the reply composer. */
    val userName: StateFlow<String> = authRepository.currentUserNameFlow
    val userPhotoUrl: StateFlow<String?> =
        authRepository.currentUserPhotoUrlFlow.stateIn(viewModelScope, SharingStarted.Eagerly, null)
    val userHandle: StateFlow<String> =
        authRepository.currentUsernameHandleFlow.stateIn(viewModelScope, SharingStarted.Eagerly, "")
    val anonTag: StateFlow<String> =
        authRepository.currentUserIdFlow
            .map { com.neb.ians.ui.components.anonTagFor(it) }
            .stateIn(viewModelScope, SharingStarted.Eagerly, "Anonymous")

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
    private fun collectCacheSignals() {
        viewModelScope.launch {
            cacheBus.batches()
                .collect { keys ->
                    if (CacheBus.PREFIX_POST + postId in keys) {
                        forumRepository.getPost(postId, cacheOnly = true).onSuccess { post ->
                            _state.update { it.copy(post = post, poll = post.poll?.toPollUi()) }
                        }
                    }
                    if (CacheBus.PREFIX_POST_REPLIES + postId in keys) {
                        forumRepository.getReplies(postId, cacheOnly = true).onSuccess { replies ->
                            _state.update { it.copy(replies = replies, isLoading = false) }
                        }
                    }
                }
        }
    }

    private var openedAt = 0L
    private var viewCounted = false

    @OptIn(kotlinx.coroutines.DelicateCoroutinesApi::class)
    override fun onCleared() {
        if (viewCounted && openedAt > 0L) {
            val dwell = android.os.SystemClock.elapsedRealtime() - openedAt
            val repo = forumRepository
            val id = postId
            // The view model's scope is already gone here; this is one tiny best-effort request.
            kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                repo.reportPostView(id, "", dwell.coerceIn(0L, 30 * 60_000L))
            }
        }
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

            if (!viewCounted) {
                openedAt = android.os.SystemClock.elapsedRealtime()
                viewCounted = true
                forumRepository.reportPostView(postId, PostReachHints.take(postId))
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

    /** Folds a fresh poll payload into the post card or the comment it belongs to. */
    private fun applyPoll(poll: ApiPoll) {
        _state.update { state ->
            if (state.poll?.id == poll.id) {
                state.copy(poll = poll.toPollUi(), post = state.post?.copy(poll = poll), busyPollId = null)
            } else {
                state.copy(
                    replies = state.replies.map { if (it.poll?.id == poll.id) it.copy(poll = poll) else it },
                    busyPollId = null
                )
            }
        }
    }

    private fun pollFailure(e: Throwable, fallback: String) {
        val message = ApiErrorMapper.mapException(e).ifBlank { fallback }
        _state.update { it.copy(busyPollId = null, snackbarMessage = message) }
    }

    fun votePoll(pollId: String, optionIds: List<String>, allowMultiple: Boolean) {
        if (optionIds.isEmpty() || _state.value.busyPollId != null) return
        _state.update { it.copy(busyPollId = pollId) }
        viewModelScope.launch {
            forumRepository.votePoll(pollId, optionIds, allowMultiple)
                .onSuccess { applyPoll(it) }
                .onFailure { pollFailure(it, "Couldn't submit vote") }
        }
    }

    fun addPollOption(pollId: String, text: String) {
        if (text.isBlank() || _state.value.busyPollId != null) return
        _state.update { it.copy(busyPollId = pollId) }
        viewModelScope.launch {
            forumRepository.addPollOption(pollId, text)
                .onSuccess { applyPoll(it) }
                .onFailure { pollFailure(it, "Couldn't add that option") }
        }
    }

    fun retractPollVote(pollId: String) {
        if (_state.value.busyPollId != null) return
        _state.update { it.copy(busyPollId = pollId) }
        viewModelScope.launch {
            forumRepository.retractPollVote(pollId)
                .onSuccess { applyPoll(it) }
                .onFailure { pollFailure(it, "Couldn't change your vote") }
        }
    }

    // ----- Edit / archive / delete -----

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

    /** The poll being written in the main comment bar, or null when the builder is closed. */
    private val _composerPoll = MutableStateFlow<com.neb.ians.ui.screens.forum.CommentPollDraft?>(null)
    val composerPoll: StateFlow<com.neb.ians.ui.screens.forum.CommentPollDraft?> = _composerPoll.asStateFlow()

    fun toggleComposerPoll() {
        _composerPoll.value = if (_composerPoll.value == null) com.neb.ians.ui.screens.forum.CommentPollDraft() else null
    }

    fun updateComposerPoll(draft: com.neb.ians.ui.screens.forum.CommentPollDraft) {
        _composerPoll.value = draft
    }

    private val _composerKind = MutableStateFlow("comment")
    val composerKind: StateFlow<String> = _composerKind.asStateFlow()

    fun setComposerKind(kind: String) {
        _composerKind.value = kind
    }

    fun labelReply(replyId: String, label: String) {
        val before = _state.value.replies
        val current = before.firstOrNull { it.id == replyId } ?: return
        _state.update { state ->
            state.copy(replies = state.replies.map {
                when {
                    it.id == replyId -> it.copy(label = label)
                    label == "accepted" && it.label == "accepted" -> it.copy(label = "")
                    else -> it
                }
            })
        }
        viewModelScope.launch {
            forumRepository.labelReply(current.id, label).onFailure { e ->
                _state.update { it.copy(replies = before, snackbarMessage = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    private val _composerAnonymous = MutableStateFlow(false)
    val composerAnonymous: StateFlow<Boolean> = _composerAnonymous.asStateFlow()

    fun setComposerAnonymous(anonymous: Boolean) {
        _composerAnonymous.value = anonymous
    }

    fun showSnackbar(message: String) {
        _state.update { it.copy(snackbarMessage = message) }
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

    /** Stage a finished voice-note recording as an audio attachment on the reply composer. */
    fun addVoiceNote(file: File, durationMs: Long) {
        val current = _mediaAttachments.value
        if (current.size >= ForumMediaUploadHelper.MAX_ATTACHMENTS) {
            _state.update { it.copy(snackbarMessage = "Maximum ${ForumMediaUploadHelper.MAX_ATTACHMENTS} attachments") }
            return
        }
        val uri = Uri.fromFile(file)
        val name = "Voice note (${formatVoiceTime(durationMs)})"
        val pending = PendingForumAttachment(
            name = name,
            kind = "audio",
            sizeBytes = file.length(),
            uri = uri,
            durationMs = durationMs
        )
        _mediaAttachments.update { it + pending }
        viewModelScope.launch {
            val result = mediaUploadHelper.upload(uri, "audio", name)
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
                _state.update { it.copy(snackbarMessage = e.message ?: "Couldn't upload voice note") }
            }
        }
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
        val staged = _mediaAttachments.value
        val pollDraft = if (parentReplyId.isNullOrBlank()) _composerPoll.value else null
        if (pollDraft != null && !pollDraft.isReady) {
            _state.update { it.copy(snackbarMessage = "A poll needs a question and two different options") }
            return
        }
        if ((content.isBlank() && staged.isEmpty() && pollDraft == null) || _isSubmittingReply.value) return
        if (staged.any { it.uploading }) {
            _state.update { it.copy(snackbarMessage = "Wait for attachments to finish uploading") }
            return
        }
        val attachments: List<ApiMediaAttachmentInput> = staged.mapNotNull { it.uploaded }
        val isAnonymous = _composerAnonymous.value
        val kind = if (parentReplyId.isNullOrBlank()) _composerKind.value else "comment"
        viewModelScope.launch {
            _isSubmittingReply.value = true
            forumRepository.createReply(
                postId = postId,
                content = content.trim(),
                parentReplyId = parentReplyId,
                isAnonymous = isAnonymous,
                attachments = attachments,
                kind = kind,
                poll = pollDraft?.toRequest()
            ).onSuccess { reply ->
                _isSubmittingReply.value = false
                if (pollDraft != null) _composerPoll.value = null
                _composerKind.value = "comment"
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
