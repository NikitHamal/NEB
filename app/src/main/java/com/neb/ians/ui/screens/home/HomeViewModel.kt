package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.intOrNull
import javax.inject.Inject

data class HomeUiState(
    val userName: String = "Student",
    val userPhotoUrl: String? = null,
    val currentUserId: String? = null,
    val recentResources: List<ApiResource> = emptyList(),
    val popularResources: List<ApiResource> = emptyList(),
    val recentPosts: List<ApiPost> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
) {
    companion object {
        val SUBJECTS = listOf(
            "Physics", "Chemistry", "Mathematics", "Biology",
            "English", "Nepali", "Computer Science", "Economics", "Accountancy"
        )
    }
}

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val settingsRepository: SettingsRepository,
    private val forumRepository: ForumRepository,
    private val realtimeClient: RealtimeClient
) : ViewModel() {

    private val _isLoading = MutableStateFlow(true)
    private val _error = MutableStateFlow<String?>(null)
    private val _recentResources = MutableStateFlow<List<ApiResource>>(emptyList())
    private val _popularResources = MutableStateFlow<List<ApiResource>>(emptyList())
    private val _recentPosts = MutableStateFlow<List<ApiPost>>(emptyList())
    private val processingPostLikes = mutableSetOf<String>()
    private val processingBookmarks = mutableSetOf<String>()
    private var unsubscribeForum: (() -> Unit)? = null

    init {
        loadData()
        unsubscribeForum = realtimeClient.subscribe("forum.public")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                if (event.channel == "forum.public" && event.event == "post.like_changed") {
                    handleLikeEvent(event.data)
                }
            }
        }
    }

    override fun onCleared() {
        unsubscribeForum?.invoke()
        unsubscribeForum = null
        super.onCleared()
    }

    private fun handleLikeEvent(data: kotlinx.serialization.json.JsonObject?) {
        try {
            val payload = data ?: return
            val postId = (payload["post_id"] as? kotlinx.serialization.json.JsonPrimitive)?.contentOrNull ?: return
            val count = (payload["thumbs_up_count"] as? kotlinx.serialization.json.JsonPrimitive)?.intOrNull ?: return
            if (processingPostLikes.contains(postId)) return
            _recentPosts.update { posts ->
                posts.map { post ->
                    if (post.id == postId) post.copy(thumbsUpCount = count) else post
                }
            }
        } catch (_: Exception) {}
    }

    private fun loadData() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            try {
                val token = authRepository.getBearerToken()
                if (token != null) {
                    try {
                        authRepository.refreshProfile()
                    } catch (_: Exception) {}
                }
                val resourcesResult = apiService.getResources(token, sort = "newest", page = 1)
                val popularResult = apiService.getResources(token, sort = "relevant", page = 1)
                val postsResult = apiService.getPosts(token)
                _recentResources.value = resourcesResult.resources
                _popularResources.value = popularResult.resources
                _recentPosts.value = postsResult.posts
            } catch (e: Exception) {
                _error.value = ApiErrorMapper.mapException(e)
            }
            _isLoading.value = false
        }
    }

    fun refresh() {
        loadData()
    }

    fun toggleThumbsUp(postId: String) {
        if (processingPostLikes.contains(postId)) return
        val current = _recentPosts.value.firstOrNull { it.id == postId } ?: return
        processingPostLikes.add(postId)
        val optimistic = current.copy(
            isThumbedUp = !current.isThumbedUp,
            thumbsUpCount = (current.thumbsUpCount + if (current.isThumbedUp) -1 else 1).coerceAtLeast(0)
        )
        _recentPosts.update { posts -> posts.map { if (it.id == postId) optimistic else it } }
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    _recentPosts.update { posts ->
                        posts.map { post ->
                            if (post.id == postId) post.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp) else post
                        }
                    }
                }
                .onFailure { _recentPosts.update { posts -> posts.map { if (it.id == postId) current else it } } }
            processingPostLikes.remove(postId)
        }
    }

    fun toggleBookmark(postId: String) {
        if (processingBookmarks.contains(postId)) return
        val current = _recentPosts.value.firstOrNull { it.id == postId } ?: return
        processingBookmarks.add(postId)
        val optimistic = current.copy(isBookmarked = !(current.isBookmarked == true))
        _recentPosts.update { posts -> posts.map { if (it.id == postId) optimistic else it } }
        viewModelScope.launch {
            forumRepository.toggleBookmark("post", postId)
                .onSuccess { response ->
                    _recentPosts.update { posts ->
                        posts.map { post ->
                            if (post.id == postId) post.copy(isBookmarked = response.isBookmarked) else post
                        }
                    }
                }
                .onFailure { _recentPosts.update { posts -> posts.map { if (it.id == postId) current else it } } }
            processingBookmarks.remove(postId)
        }
    }

    val uiState: StateFlow<HomeUiState> = combine(
        combine(
            authRepository.userProfileFlow.map { it?.displayName?.takeIf { name -> name.isNotBlank() } ?: it?.username ?: "Student" },
            authRepository.currentUserPhotoUrlFlow,
            authRepository.currentUserIdFlow
        ) { name, photo, userId -> Triple(name, photo, userId) },
        _recentResources,
        _popularResources,
        _recentPosts,
        combine(_isLoading, _error) { isLoading, error -> Pair(isLoading, error) }
    ) { user, recentResources, popularResources, recentPosts, loadingError ->
        HomeUiState(
            userName = user.first,
            userPhotoUrl = user.second,
            currentUserId = user.third,
            recentResources = recentResources,
            popularResources = popularResources,
            recentPosts = recentPosts,
            isLoading = loadingError.first,
            error = loadingError.second
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}