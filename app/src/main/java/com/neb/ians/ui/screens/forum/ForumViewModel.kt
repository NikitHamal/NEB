package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.intOrNull
import javax.inject.Inject

// Defensive JsonObject readers shared by the forum ViewModels (same package).
internal fun JsonObject.stringField(key: String): String? =
    try { (this[key] as? JsonPrimitive)?.contentOrNull } catch (_: Exception) { null }

internal fun JsonObject.intField(key: String): Int? =
    try { (this[key] as? JsonPrimitive)?.intOrNull } catch (_: Exception) { null }

internal fun JsonObject.boolField(key: String): Boolean? =
    try { (this[key] as? JsonPrimitive)?.let { it.contentOrNull?.toBooleanStrictOrNull() } } catch (_: Exception) { null }

data class ForumUiState(
    val posts: List<ApiPost> = emptyList(),
    val selectedCategory: String? = null,
    val searchQuery: String = "",
    val sort: String = "hot",
    val page: Int = 1,
    val hasMore: Boolean = false,
    val isLoading: Boolean = true,
    val isLoadingMore: Boolean = false,
    val error: String? = null,
    val snackbarMessage: String? = null,
    val currentUserId: String? = null,
    val userName: String = "Student",
    val userPhotoUrl: String? = null
) {
    companion object {
        val CATEGORIES = listOf(
            "General", "Physics", "Chemistry", "Mathematics",
            "Biology", "English", "Computer Science", "Exam Tips"
        )
        val SORTS = listOf("hot", "new", "top", "discussed")
    }
}

@HiltViewModel
class ForumViewModel @Inject constructor(
    private val forumRepository: ForumRepository,
    private val authRepository: AuthRepository,
    private val realtimeClient: RealtimeClient
) : ViewModel() {

    private val _forumState = MutableStateFlow(ForumUiState())
    private var searchJob: Job? = null
    private val processingPostLikes = mutableSetOf<String>()
    private var loadJob: Job? = null
    private var unsubscribeForum: (() -> Unit)? = null

    val uiState: StateFlow<ForumUiState> = combine(
        _forumState,
        authRepository.currentUserNameFlow,
        authRepository.currentUserPhotoUrlFlow,
        authRepository.currentUserIdFlow
    ) { state, name, photo, userId ->
        state.copy(userName = name, userPhotoUrl = photo, currentUserId = userId)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ForumUiState())

    init {
        loadPosts(reset = true)
        unsubscribeForum = realtimeClient.subscribe("forum.public")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                if (event.channel == "forum.public") handleRealtimeEvent(event.event, event.data)
            }
        }
    }

    override fun onCleared() {
        unsubscribeForum?.invoke()
        unsubscribeForum = null
        super.onCleared()
    }

    private fun handleRealtimeEvent(event: String, data: JsonObject?) {
        try {
            val payload = data ?: return
            when (event) {
                "post.like_changed" -> {
                    val postId = payload.stringField("post_id") ?: return
                    val count = payload.intField("thumbs_up_count") ?: return
                    if (processingPostLikes.contains(postId)) return
                    val isThumbedUp = payload.boolField("isThumbedUp")
                    _forumState.update { state ->
                        state.copy(posts = state.posts.map { post ->
                            if (post.id == postId) {
                                if (isThumbedUp != null) post.copy(thumbsUpCount = count, isThumbedUp = isThumbedUp)
                                else post.copy(thumbsUpCount = count)
                            } else post
                        })
                    }
                }
                "post.deleted" -> {
                    val postId = payload.stringField("post_id") ?: payload.stringField("id") ?: return
                    _forumState.update { state ->
                        state.copy(posts = state.posts.filterNot { it.id == postId })
                    }
                }
            }
        } catch (_: Exception) {
        }
    }

    private fun loadPosts(reset: Boolean) {
        loadJob?.cancel()
        loadJob = viewModelScope.launch {
            val state = _forumState.value
            val targetPage = if (reset) 1 else state.page + 1
            if (reset) {
                _forumState.update { it.copy(isLoading = it.posts.isEmpty(), error = null, page = 1) }
            } else {
                _forumState.update { it.copy(isLoadingMore = true) }
            }
            forumRepository.getPosts(
                category = state.selectedCategory,
                page = targetPage,
                sort = state.sort,
                search = state.searchQuery
            ).onSuccess { result ->
                _forumState.update { current ->
                    current.copy(
                        posts = if (reset) result.posts else current.posts + result.posts.filter { newPost ->
                            current.posts.none { it.id == newPost.id }
                        },
                        page = result.page,
                        hasMore = result.hasMore,
                        isLoading = false,
                        isLoadingMore = false,
                        error = null
                    )
                }
            }.onFailure { e ->
                _forumState.update {
                    it.copy(
                        isLoading = false,
                        isLoadingMore = false,
                        error = ApiErrorMapper.mapException(e)
                    )
                }
            }
        }
    }

    fun refresh() = loadPosts(reset = true)

    fun syncLikeStates() {
        viewModelScope.launch {
            val state = _forumState.value
            if (state.posts.isEmpty()) return@launch
            try {
                forumRepository.getPosts(
                    category = state.selectedCategory,
                    page = state.page,
                    sort = state.sort,
                    search = state.searchQuery
                ).onSuccess { result ->
                    _forumState.update { current ->
                        val merged = current.posts.map { existing ->
                            val fresh = result.posts.firstOrNull { it.id == existing.id }
                            fresh ?: existing
                        }
                        current.copy(posts = merged)
                    }
                }
            } catch (_: Exception) {}
        }
    }

    fun loadMore() {
        val state = _forumState.value
        if (state.isLoading || state.isLoadingMore || !state.hasMore) return
        loadPosts(reset = false)
    }

    fun selectSort(sort: String) {
        if (_forumState.value.sort == sort) return
        _forumState.update { it.copy(sort = sort, isLoading = true, posts = it.posts) }
        loadPosts(reset = true)
    }

    fun selectCategory(category: String?) {
        val newCategory = if (_forumState.value.selectedCategory == category) null else category
        _forumState.update { it.copy(selectedCategory = newCategory, isLoading = true) }
        loadPosts(reset = true)
    }

    fun onSearchQueryChange(query: String) {
        _forumState.update { it.copy(searchQuery = query) }
        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            delay(400)
            loadPosts(reset = true)
        }
    }

    /** Optimistic like toggle — flip immediately, revert on failure. */
    fun toggleThumbsUp(postId: String) {
        if (processingPostLikes.contains(postId)) return
        val current = _forumState.value.posts.firstOrNull { it.id == postId } ?: return
        processingPostLikes.add(postId)
        val optimistic = current.copy(
            isThumbedUp = !current.isThumbedUp,
            thumbsUpCount = (current.thumbsUpCount + if (current.isThumbedUp) -1 else 1).coerceAtLeast(0)
        )
        updatePostInList(optimistic)
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    _forumState.update { state ->
                        state.copy(posts = state.posts.map { post ->
                            if (post.id == postId) {
                                post.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp)
                            } else post
                        })
                    }
                }
                .onFailure { updatePostInList(current) }
            processingPostLikes.remove(postId)
        }
    }

    /** Optimistic bookmark toggle — flip immediately, revert on failure. */
    fun toggleBookmark(postId: String) {
        val current = _forumState.value.posts.firstOrNull { it.id == postId } ?: return
        val optimistic = current.copy(isBookmarked = !(current.isBookmarked == true))
        updatePostInList(optimistic)
        viewModelScope.launch {
            forumRepository.toggleBookmark("post", postId)
                .onSuccess { response ->
                    _forumState.update { state ->
                        state.copy(posts = state.posts.map { post ->
                            if (post.id == postId) post.copy(isBookmarked = response.isBookmarked) else post
                        })
                    }
                }
                .onFailure { updatePostInList(current) }
        }
    }

    fun reportPost(postId: String, reason: String, description: String) {
        viewModelScope.launch {
            forumRepository.createReport("post", postId, reason, description)
                .onSuccess { _forumState.update { it.copy(snackbarMessage = "Report submitted") } }
                .onFailure { _forumState.update { it.copy(snackbarMessage = "Couldn't submit report") } }
        }
    }

    fun editPost(postId: String, title: String, content: String) {
        viewModelScope.launch {
            forumRepository.updatePost(postId, title = title, content = content)
                .onSuccess { updated -> updatePostInList(updated) }
                .onFailure { _forumState.update { it.copy(snackbarMessage = "Couldn't save changes") } }
        }
    }

    fun archivePost(postId: String) {
        val current = _forumState.value.posts.firstOrNull { it.id == postId } ?: return
        viewModelScope.launch {
            forumRepository.archivePost(postId)
                .onSuccess {
                    updatePostInList(current.copy(isArchived = !(current.isArchived == true)))
                }
                .onFailure { _forumState.update { it.copy(snackbarMessage = "Couldn't archive post") } }
        }
    }

    fun deletePost(postId: String) {
        viewModelScope.launch {
            forumRepository.deletePost(postId)
                .onSuccess {
                    _forumState.update { state ->
                        state.copy(
                            posts = state.posts.filterNot { it.id == postId },
                            snackbarMessage = "Post deleted"
                        )
                    }
                }
                .onFailure { _forumState.update { it.copy(snackbarMessage = "Couldn't delete post") } }
        }
    }

    fun consumeSnackbar() {
        _forumState.update { it.copy(snackbarMessage = null) }
    }

    private fun updatePostInList(updated: ApiPost) {
        _forumState.update { state ->
            state.copy(posts = state.posts.map { if (it.id == updated.id) updated else it })
        }
    }
}
