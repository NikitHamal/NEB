package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.data.repository.AppCache
import com.neb.ians.data.repository.NewsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.intOrNull
import javax.inject.Inject

private data class Quad<A, B, C, D>(val first: A, val second: B, val third: C, val fourth: D)

data class HomeUiState(
    val userName: String = "Student",
    val userPhotoUrl: String? = null,
    val currentUserId: String? = null,
    val recentResources: List<ApiResource> = emptyList(),
    val popularResources: List<ApiResource> = emptyList(),
    val recentPosts: List<ApiPost> = emptyList(),
    val latestNews: List<NewsAnnouncement> = emptyList(),
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
    private val newsRepository: NewsRepository,
    private val realtimeClient: RealtimeClient,
    private val appCache: AppCache
) : ViewModel() {

    private val _isLoading = MutableStateFlow(appCache.recentResources.isEmpty() && appCache.recentPosts.isEmpty())
    private val _error = MutableStateFlow<String?>(null)
    private val _recentResources = MutableStateFlow<List<ApiResource>>(appCache.recentResources)
    private val _popularResources = MutableStateFlow<List<ApiResource>>(appCache.popularResources)
    private val _recentPosts = MutableStateFlow<List<ApiPost>>(appCache.recentPosts)
    private val _latestNews = MutableStateFlow<List<NewsAnnouncement>>(appCache.latestNews)
    private val processingPostLikes = mutableSetOf<String>()
    private val processingBookmarks = mutableSetOf<String>()
    private val processingDeletions = mutableSetOf<String>()
    private val _snackbarMessage = MutableSharedFlow<String?>(extraBufferCapacity = 3, onBufferOverflow = BufferOverflow.DROP_OLDEST)
    val snackbarMessage: Flow<String?> = _snackbarMessage.asSharedFlow()
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
                val updated = posts.map { post ->
                    if (post.id == postId) post.copy(thumbsUpCount = count) else post
                }
                appCache.recentPosts = updated
                updated
            }
        } catch (_: Exception) {}
    }

    private fun loadData() {
        viewModelScope.launch {
            _error.value = null
            try {
                val token = authRepository.getBearerToken()
                if (token != null) {
                    try {
                        authRepository.refreshProfile()
                    } catch (_: Exception) {}
                }
                val (resourcesResult, popularResult, postsResult, newsResult) = coroutineScope {
                    val resources = async { apiService.getResources(token, sort = "newest", page = 1, pageSize = 12) }
                    val popular = async { apiService.getResources(token, sort = "relevant", page = 1, pageSize = 12) }
                    val posts = async { apiService.getPosts(token, page = 1, pageSize = 8) }
                    val news = async { newsRepository.getAnnouncements().getOrDefault(appCache.latestNews) }
                    Quad(resources.await(), popular.await(), posts.await(), news.await())
                }

                _recentResources.value = resourcesResult.resources
                _popularResources.value = popularResult.resources
                _recentPosts.value = postsResult.posts
                _latestNews.value = newsResult

                appCache.recentResources = resourcesResult.resources
                appCache.popularResources = popularResult.resources
                appCache.recentPosts = postsResult.posts
                appCache.latestNews = newsResult
            } catch (e: Exception) {
                if (_recentResources.value.isEmpty()) {
                    _error.value = ApiErrorMapper.mapException(e)
                }
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
        _recentPosts.update { posts ->
            val updated = posts.map { if (it.id == postId) optimistic else it }
            appCache.recentPosts = updated
            updated
        }
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    _recentPosts.update { posts ->
                        val updated = posts.map { post ->
                            if (post.id == postId) post.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp) else post
                        }
                        appCache.recentPosts = updated
                        updated
                    }
                }
                .onFailure {
                    _recentPosts.update { posts ->
                        val updated = posts.map { if (it.id == postId) current else it }
                        appCache.recentPosts = updated
                        updated
                    }
                }
            processingPostLikes.remove(postId)
        }
    }

    fun toggleBookmark(postId: String) {
        if (processingBookmarks.contains(postId)) return
        val current = _recentPosts.value.firstOrNull { it.id == postId } ?: return
        processingBookmarks.add(postId)
        val optimistic = current.copy(isBookmarked = !(current.isBookmarked == true))
        _recentPosts.update { posts ->
            val updated = posts.map { if (it.id == postId) optimistic else it }
            appCache.recentPosts = updated
            updated
        }
        viewModelScope.launch {
            forumRepository.toggleBookmark("post", postId)
                .onSuccess { response ->
                    _recentPosts.update { posts ->
                        val updated = posts.map { post ->
                            if (post.id == postId) post.copy(isBookmarked = response.isBookmarked) else post
                        }
                        appCache.recentPosts = updated
                        updated
                    }
                }
                .onFailure {
                    _recentPosts.update { posts ->
                        val updated = posts.map { if (it.id == postId) current else it }
                        appCache.recentPosts = updated
                        updated
                    }
                }
            processingBookmarks.remove(postId)
        }
    }

    fun deletePost(postId: String) {
        if (processingDeletions.contains(postId)) return
        processingDeletions.add(postId)
        viewModelScope.launch {
            forumRepository.deletePost(postId)
                .onSuccess {
                    _recentPosts.update { posts ->
                        val updated = posts.filterNot { it.id == postId }
                        appCache.recentPosts = updated
                        updated
                    }
                    _snackbarMessage.tryEmit("Post deleted")
                }
                .onFailure { e ->
                    _snackbarMessage.tryEmit("Couldn't delete post: ${e.message ?: "Unknown error"}")
                }
            processingDeletions.remove(postId)
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
        _latestNews,
        combine(_isLoading, _error) { isLoading, error -> Pair(isLoading, error) }
    ) { values ->
        val user = values[0] as Triple<String, String?, String?>
        @Suppress("UNCHECKED_CAST") val recentResources = values[1] as List<ApiResource>
        @Suppress("UNCHECKED_CAST") val popularResources = values[2] as List<ApiResource>
        @Suppress("UNCHECKED_CAST") val recentPosts = values[3] as List<ApiPost>
        @Suppress("UNCHECKED_CAST") val latestNews = values[4] as List<NewsAnnouncement>
        @Suppress("UNCHECKED_CAST") val loadingError = values[5] as Pair<Boolean, String?>
        HomeUiState(
            userName = user.first,
            userPhotoUrl = user.second,
            currentUserId = user.third,
            recentResources = recentResources,
            popularResources = popularResources,
            recentPosts = recentPosts,
            latestNews = latestNews,
            isLoading = loadingError.first,
            error = loadingError.second
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}
