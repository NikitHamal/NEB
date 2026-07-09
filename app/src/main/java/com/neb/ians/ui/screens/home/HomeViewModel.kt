package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.data.repository.AppCache
import com.neb.ians.data.repository.NewsRepository
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.data.repository.ResourcesResult
import com.neb.ians.data.repository.ForumPostsResult
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.decodeFromJsonElement
import javax.inject.Inject

private data class HomeLoadResults(
    val resources: Result<ResourcesResult>,
    val popular: Result<ResourcesResult>,
    val posts: Result<ForumPostsResult>,
    val news: List<NewsAnnouncement>
)

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
    private val authRepository: AuthRepository,
    private val settingsRepository: SettingsRepository,
    private val forumRepository: ForumRepository,
    private val resourceRepository: ResourceRepository,
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

    private val postJson = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    init {
        loadData()
        unsubscribeForum = realtimeClient.subscribe("forum.public")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                when {
                    event.channel == "forum.public" && event.event == "post.like_changed" ->
                        handleLikeEvent(event.data)
                    event.channel == "forum.public" && event.event == "post.created" ->
                        handlePostCreated(event.data)
                }
            }
        }
    }

    override fun onCleared() {
        unsubscribeForum?.invoke()
        unsubscribeForum = null
        super.onCleared()
    }

    private fun handlePostCreated(data: JsonObject?) {
        try {
            val payload = data ?: return
            val newPost = postJson.decodeFromJsonElement<ApiPost>(payload)
            _recentPosts.update { posts ->
                if (posts.any { it.id == newPost.id }) return@update posts
                val updated = listOf(newPost) + posts
                appCache.recentPosts = updated
                updated
            }
        } catch (_: Exception) {}
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

    private fun loadData(forceRefresh: Boolean = false): Job {
        val job = viewModelScope.launch {
            _error.value = null
            try {
                if (authRepository.getBearerToken() != null) {
                    try {
                        authRepository.refreshProfile()
                    } catch (_: Exception) {}
                }
                val results = coroutineScope {
                    val resources = async { resourceRepository.getResources(sort = "newest", page = 1, forceRefresh = forceRefresh) }
                    val popular = async { resourceRepository.getResources(sort = "relevant", page = 1, forceRefresh = forceRefresh) }
                    val posts = async { forumRepository.getPosts(page = 1, forceRefresh = forceRefresh) }
                    val news = async { newsRepository.getAnnouncements().getOrDefault(appCache.latestNews) }
                    HomeLoadResults(resources.await(), popular.await(), posts.await(), news.await())
                }

                val resources = results.resources.getOrNull()?.resources ?: appCache.recentResources
                val popular = results.popular.getOrNull()?.resources ?: appCache.popularResources
                val posts = results.posts.getOrNull()?.posts ?: appCache.recentPosts
                val news = results.news

                _recentResources.value = resources
                _popularResources.value = popular
                _recentPosts.value = posts
                _latestNews.value = news

                appCache.recentResources = resources
                appCache.popularResources = popular
                appCache.recentPosts = posts
                appCache.latestNews = news

                val firstFailure = listOf(
                    results.resources.exceptionOrNull(),
                    results.popular.exceptionOrNull(),
                    results.posts.exceptionOrNull()
                ).firstOrNull()
                if (resources.isEmpty() && popular.isEmpty() && posts.isEmpty() && firstFailure != null) {
                    _error.value = ApiErrorMapper.mapException(firstFailure)
                }
            } catch (e: Exception) {
                if (_recentResources.value.isEmpty() && _recentPosts.value.isEmpty()) {
                    _error.value = ApiErrorMapper.mapException(e)
                }
            }
            _isLoading.value = false
        }
        return job
    }

    fun refresh(): Job = loadData(forceRefresh = true)

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
                    _snackbarMessage.tryEmit("Couldn't delete post: ${ApiErrorMapper.mapException(e)}")
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
