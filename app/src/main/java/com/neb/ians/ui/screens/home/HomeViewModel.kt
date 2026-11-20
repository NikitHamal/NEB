package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.CacheBus
import com.neb.ians.data.repository.FollowStateRepository
import com.neb.ians.data.repository.PeopleSuggestionRepository
import com.neb.ians.data.repository.PersonSuggestion
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

@androidx.compose.runtime.Immutable
data class HomeUiState(
    val userName: String = "Student",
    val userPhotoUrl: String? = null,
    val currentUserId: String? = null,
    val recentResources: List<ApiResource> = emptyList(),
    val popularResources: List<ApiResource> = emptyList(),
    val recentPosts: List<ApiPost> = emptyList(),
    val latestNews: List<NewsAnnouncement> = emptyList(),
    val sort: String = "hot",
    val selectedCategory: String? = null,
    val isLoading: Boolean = true,
    val isFilterRefreshing: Boolean = false,
    val isLoadingMore: Boolean = false,
    val hasMorePosts: Boolean = true,
    val error: String? = null
) {
    companion object {
        val CATEGORIES = listOf(
            "General", "Physics", "Chemistry", "Mathematics",
            "Biology", "Computer Science", "English", "Nepali",
            "Accountancy", "Economics", "Exam Tips"
        )
    }
}

private data class HomeStatusState(
    val isLoading: Boolean,
    val isFilterRefreshing: Boolean,
    val error: String?,
    val sort: String,
    val selectedCategory: String?,
    val isLoadingMore: Boolean,
    val hasMorePosts: Boolean
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val apiService: ApiService,
    private val settingsRepository: SettingsRepository,
    private val forumRepository: ForumRepository,
    private val resourceRepository: ResourceRepository,
    private val newsRepository: NewsRepository,
    private val followStateRepository: FollowStateRepository,
    private val peopleSuggestionRepository: PeopleSuggestionRepository,
    private val realtimeClient: RealtimeClient,
    private val appCache: AppCache,
    private val cacheBus: CacheBus
) : ViewModel() {

    private val _isLoading = MutableStateFlow(appCache.recentResources.isEmpty() && appCache.recentPosts.isEmpty())
    private val _error = MutableStateFlow<String?>(null)
    private val _recentResources = MutableStateFlow<List<ApiResource>>(appCache.recentResources)
    private val _popularResources = MutableStateFlow<List<ApiResource>>(appCache.popularResources)
    private val _recentPosts = MutableStateFlow<List<ApiPost>>(appCache.recentPosts)
    private val _latestNews = MutableStateFlow<List<NewsAnnouncement>>(appCache.latestNews)
    private val _sort = MutableStateFlow("hot")
    private val _selectedCategory = MutableStateFlow<String?>(null)
    private val _isFilterRefreshing = MutableStateFlow(false)
    private val _isLoadingMore = MutableStateFlow(false)
    private val _hasMorePosts = MutableStateFlow(true)
    private var currentPostPage = 1
    private var currentResourcePage = 1
    private var hasMoreResources = true
    private var filterJob: Job? = null
    private val postSlices = java.util.concurrent.ConcurrentHashMap<String, Pair<List<ApiPost>, Boolean>>()
    private val processingPostLikes = mutableSetOf<String>()
    private val processingBookmarks = mutableSetOf<String>()
    private val processingDeletions = mutableSetOf<String>()
    private val _snackbarMessage = MutableSharedFlow<String?>(extraBufferCapacity = 3, onBufferOverflow = BufferOverflow.DROP_OLDEST)
    val snackbarMessage: Flow<String?> = _snackbarMessage.asSharedFlow()
    private var unsubscribeForum: (() -> Unit)? = null

    private val postJson = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    val suggestedPeers: StateFlow<List<PersonSuggestion>> = peopleSuggestionRepository.suggestions

    @Volatile
    private var cachedCurrentUserId: String? = null

    private fun sliceKey(sort: String = _sort.value, category: String? = _selectedCategory.value): String =
        "$sort|${category.orEmpty()}"

    private fun currentUid(): String? = cachedCurrentUserId

    init {
        viewModelScope.launch {
            authRepository.currentUserIdFlow.collect { cachedCurrentUserId = it }
        }
        if (appCache.recentPosts.isNotEmpty()) {
            postSlices[sliceKey("hot", null)] = appCache.recentPosts to true
        }
        loadData()
        viewModelScope.launch { peopleSuggestionRepository.load() }
        unsubscribeForum = realtimeClient.subscribe("forum.public")
        viewModelScope.launch {
            realtimeClient.events.collect { event ->
                when {
                    event.channel == "forum.public" && event.event == "post.like_changed" ->
                        handleLikeEvent(event.data)
                    event.channel == "forum.public" && event.event == "post.created" ->
                        handlePostCreated(event.data)
                    event.channel == "forum.public" && event.event == "post.deleted" ->
                        handlePostDeleted(event.data)
                }
            }
        }
        collectCacheSignals()
    }

    /**
     * Stale-while-revalidate glue: when a repository background-refresh writes
     * fresher data into the offline cache, quietly re-read it and update the
     * UI — no manual pull-to-refresh needed.
     */
    private fun collectCacheSignals() {
        viewModelScope.launch {
            cacheBus.batches()
                .collect { keys ->
                    if (keys.any { it.startsWith(CacheBus.PREFIX_RESOURCES) }) {
                        resourceRepository.getResources(sort = "newest", page = 1, cacheOnly = true)
                            .onSuccess { result ->
                                _recentResources.update { current ->
                                    val merged = mergeHead(result.resources, current) { it.id }
                                    if (merged == current) current else merged.also { appCache.recentResources = it }
                                }
                            }
                        resourceRepository.getResources(sort = "trending", page = 1, cacheOnly = true)
                            .onSuccess { result ->
                                appCache.popularResources = result.resources
                                _popularResources.value = result.resources
                            }
                    }
                    if (keys.any { it.startsWith(CacheBus.PREFIX_POSTS_LIST) }) {
                        val activeSort = _sort.value
                        val activeCat = _selectedCategory.value
                        forumRepository.getPosts(category = activeCat, page = 1, sort = activeSort, cacheOnly = true)
                            .onSuccess { result ->
                                val uid = currentUid()
                                val ranked = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Default) {
                                    rankHomeFeedPosts(result.posts, activeSort, uid)
                                }
                                _recentPosts.update { current ->
                                    val merged = mergeHead(ranked, current) { it.id }
                                    if (merged == current) current else merged.also {
                                        postSlices[sliceKey(activeSort, activeCat)] = it to result.hasMore
                                        if (activeSort == "hot" && activeCat == null) appCache.recentPosts = it
                                    }
                                }
                            }
                    }
                    val updatedPostIds = keys.mapNotNull { k ->
                        if (k.startsWith("post_v1_")) k.removePrefix("post_v1_") else null
                    }
                    if (updatedPostIds.isNotEmpty()) {
                        val nowMs = System.currentTimeMillis()
                        val activeCat = _selectedCategory.value
                        _recentPosts.update { current ->
                            var list = current
                            for (pid in updatedPostIds) {
                                val detail = appCache.postDetails[pid] ?: continue
                                val idx = list.indexOfFirst { it.id == pid }
                                if (idx >= 0) {
                                    if (list[idx] != detail) {
                                        list = list.toMutableList().also { it[idx] = detail }
                                    }
                                } else if (nowMs - detail.createdAt in 0..60_000L &&
                                    (activeCat == null || detail.category.equals(activeCat, ignoreCase = true))
                                ) {
                                    list = listOf(detail) + list
                                }
                            }
                            if (list !== current) {
                                postSlices[sliceKey()] = list to _hasMorePosts.value
                                if (_sort.value == "hot" && activeCat == null) appCache.recentPosts = list
                            }
                            list
                        }
                    }
                }
        }
    }

    /**
     * Replaces the head of a paged list with a fresher first page while keeping
     * everything the user has already scrolled past. A straight assignment here
     * would truncate the feed back to page one under them.
     */
    private inline fun <T> mergeHead(fresh: List<T>, current: List<T>, id: (T) -> String): List<T> {
        if (fresh.isEmpty()) return current
        val seen = fresh.mapTo(HashSet(fresh.size), id)
        val tail = current.filter { id(it) !in seen }
        return fresh + tail
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
            val activeCat = _selectedCategory.value
            if (activeCat != null && !newPost.category.equals(activeCat, ignoreCase = true)) return
            _recentPosts.update { posts ->
                if (posts.any { it.id == newPost.id }) return@update posts
                val updated = listOf(newPost) + posts
                postSlices[sliceKey()] = updated to _hasMorePosts.value
                if (_sort.value == "hot" && activeCat == null) appCache.recentPosts = updated
                updated
            }
        } catch (_: Exception) {}
    }

    private fun handlePostDeleted(data: JsonObject?) {
        try {
            val payload = data ?: return
            val postId = (payload["post_id"] as? kotlinx.serialization.json.JsonPrimitive)?.contentOrNull
                ?: (payload["id"] as? kotlinx.serialization.json.JsonPrimitive)?.contentOrNull
                ?: return
            _recentPosts.update { posts ->
                if (posts.none { it.id == postId }) return@update posts
                val updated = posts.filterNot { it.id == postId }
                postSlices[sliceKey()] = updated to _hasMorePosts.value
                if (_sort.value == "hot" && _selectedCategory.value == null) appCache.recentPosts = updated
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
            // likes arrive for posts all over the site; most are not in this feed
            _recentPosts.update { posts ->
                val i = posts.indexOfFirst { it.id == postId }
                if (i < 0 || posts[i].thumbsUpCount == count) return@update posts
                val updated = posts.toMutableList().also { it[i] = posts[i].copy(thumbsUpCount = count) }
                appCache.recentPosts = updated
                updated
            }
        } catch (_: Exception) {}
    }

    private fun loadData(forceRefresh: Boolean = false): Job {
        val job = viewModelScope.launch {
            _error.value = null

            if (!forceRefresh) {
                coroutineScope {
                    val activeSort = _sort.value
                    val activeCat = _selectedCategory.value
                    val cachedResources = async { resourceRepository.getResources(sort = "newest", page = 1, cacheOnly = true) }
                    val cachedPopular = async { resourceRepository.getResources(sort = "trending", page = 1, cacheOnly = true) }
                    val cachedPosts = async {
                        forumRepository.getPosts(category = activeCat, page = 1, sort = activeSort, cacheOnly = true)
                            .recoverCatching { forumRepository.getPosts(page = 1, cacheOnly = true).getOrThrow() }
                    }

                    cachedResources.await().onSuccess { result ->
                        appCache.recentResources = result.resources
                        _recentResources.value = result.resources
                    }
                    cachedPopular.await().onSuccess { result ->
                        appCache.popularResources = result.resources
                        _popularResources.value = result.resources
                    }
                    cachedPosts.await().onSuccess { result ->
                        val uid = currentUid()
                        val posts = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Default) {
                            com.neb.ians.ui.components.prewarmCardPreviewsNow(result.posts.map { it.content })
                            result.posts.forEach { com.neb.ians.ui.components.extractPostAttachments(it) }
                            com.neb.ians.ui.components.v3art.V3Cache.prewarm(_popularResources.value + _recentResources.value)
                            rankHomeFeedPosts(result.posts, activeSort, uid)
                        }
                        postSlices[sliceKey(activeSort, activeCat)] = posts to result.hasMore
                        if (activeSort == "hot" && activeCat == null) appCache.recentPosts = posts
                        _recentPosts.value = posts
                    }
                }
                if (_recentResources.value.isNotEmpty() || _recentPosts.value.isNotEmpty()) {
                    _isLoading.value = false
                }
            }

            try {
                // MainActivity refreshes the profile at launch and signing in caches it, so only a
                // pull-to-refresh asks again, and the feed requests never wait behind it
                if (forceRefresh && authRepository.getBearerToken() != null) {
                    viewModelScope.launch { authRepository.refreshProfile() }
                }
                val activeSort = _sort.value
                val activeCat = _selectedCategory.value
                val results = coroutineScope {
                    val resources = async { resourceRepository.getResources(sort = "newest", page = 1, forceRefresh = forceRefresh) }
                    val popular = async { resourceRepository.getResources(sort = "trending", page = 1, forceRefresh = forceRefresh) }
                    val posts = async { forumRepository.getPosts(category = activeCat, page = 1, sort = activeSort, forceRefresh = forceRefresh) }
                    val news = async { newsRepository.getAnnouncements().getOrDefault(appCache.latestNews) }
                    HomeLoadResults(resources.await(), popular.await(), posts.await(), news.await())
                }

                val resources = results.resources.getOrNull()?.resources ?: appCache.recentResources
                val popular = results.popular.getOrNull()?.resources ?: appCache.popularResources
                val postResult = results.posts.getOrNull()
                val rawPosts = (postResult?.posts ?: _recentPosts.value).distinctBy { it.id }
                val uid = currentUid()
                val posts = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Default) {
                    com.neb.ians.ui.components.prewarmCardPreviewsNow(rawPosts.map { it.content })
                    rawPosts.forEach { com.neb.ians.ui.components.extractPostAttachments(it) }
                    com.neb.ians.ui.components.v3art.V3Cache.prewarm(popular + resources)
                    rankHomeFeedPosts(rawPosts, activeSort, uid)
                }
                val news = results.news

                _recentResources.value = resources
                _popularResources.value = popular
                _recentPosts.value = posts
                _hasMorePosts.value = postResult?.hasMore ?: _hasMorePosts.value
                _latestNews.value = news

                postSlices[sliceKey(activeSort, activeCat)] = posts to _hasMorePosts.value
                appCache.recentResources = resources
                appCache.popularResources = popular
                if (activeSort == "hot" && activeCat == null) {
                    appCache.recentPosts = posts
                }
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

    fun refresh(): Job {
        currentPostPage = 1
        currentResourcePage = 1
        _hasMorePosts.value = true
        hasMoreResources = true
        return loadData(forceRefresh = true)
    }

    fun selectSort(sort: String) {
        if (_sort.value == sort) return
        _sort.value = sort
        reloadFilteredPosts()
    }

    fun selectCategory(category: String?) {
        val next = if (_selectedCategory.value == category) null else category
        _selectedCategory.value = next
        reloadFilteredPosts()
    }

    fun clearFilters() {
        if (_sort.value == "hot" && _selectedCategory.value == null) return
        _sort.value = "hot"
        _selectedCategory.value = null
        reloadFilteredPosts()
    }

    private fun reloadFilteredPosts() {
        filterJob?.cancel()
        val targetSort = _sort.value
        val targetCat = _selectedCategory.value
        val key = sliceKey(targetSort, targetCat)
        currentPostPage = 1

        postSlices[key]?.let { (cachedSlice, cachedHasMore) ->
            _recentPosts.value = cachedSlice
            _hasMorePosts.value = cachedHasMore
        }

        filterJob = viewModelScope.launch {
            _error.value = null
            _isFilterRefreshing.value = true
            if (postSlices[key] == null) {
                forumRepository.getPosts(category = targetCat, page = 1, sort = targetSort, cacheOnly = true)
                    .onSuccess { cached ->
                        val uid = currentUid()
                        val ranked = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Default) {
                            com.neb.ians.ui.components.prewarmCardPreviewsNow(cached.posts.map { it.content })
                            rankHomeFeedPosts(cached.posts, targetSort, uid)
                        }
                        postSlices[key] = ranked to cached.hasMore
                        _recentPosts.value = ranked
                        _hasMorePosts.value = cached.hasMore
                    }
            }
            forumRepository.getPosts(category = targetCat, page = 1, sort = targetSort, forceRefresh = false)
                .onSuccess { fresh ->
                    val uid = currentUid()
                    val ranked = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Default) {
                        com.neb.ians.ui.components.prewarmCardPreviewsNow(fresh.posts.map { it.content })
                        rankHomeFeedPosts(fresh.posts, targetSort, uid)
                    }
                    postSlices[key] = ranked to fresh.hasMore
                    _recentPosts.value = ranked
                    _hasMorePosts.value = fresh.hasMore
                    if (targetSort == "hot" && targetCat == null) {
                        appCache.recentPosts = ranked
                    }
                }
                .onFailure {
                    if (postSlices[key] == null) {
                        _snackbarMessage.tryEmit("Couldn't load filtered posts")
                    }
                }
            _isFilterRefreshing.value = false
        }
    }

    fun loadMore() {
        if (_isLoadingMore.value || !_hasMorePosts.value || _isFilterRefreshing.value) return
        viewModelScope.launch {
            _isLoadingMore.value = true
            val activeSort = _sort.value
            val activeCat = _selectedCategory.value
            val nextPostPage = currentPostPage + 1
            val nextResPage = currentResourcePage + 1
            coroutineScope {
                val morePosts = async { forumRepository.getPosts(category = activeCat, page = nextPostPage, sort = activeSort) }
                val moreResources = async {
                    if (hasMoreResources) {
                        resourceRepository.getResources(sort = "newest", page = nextResPage)
                    } else null
                }

                morePosts.await().fold(
                    onSuccess = { result ->
                        currentPostPage = nextPostPage
                        _hasMorePosts.value = result.hasMore
                        val uid = currentUid()
                        val rankedNew = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Default) {
                            com.neb.ians.ui.components.prewarmCardPreviewsNow(result.posts.map { it.content })
                            rankHomeFeedPosts(result.posts, activeSort, uid)
                        }
                        _recentPosts.update { current ->
                            val existingIds = current.mapTo(HashSet(current.size)) { it.id }
                            val newOnes = rankedNew.filter { existingIds.add(it.id) }
                            val updated = if (newOnes.isEmpty()) current else current + newOnes
                            postSlices[sliceKey(activeSort, activeCat)] = updated to result.hasMore
                            updated
                        }
                    },
                    onFailure = {
                        _hasMorePosts.value = false
                    }
                )

                moreResources.await()?.fold(
                    onSuccess = { result ->
                        currentResourcePage = nextResPage
                        hasMoreResources = result.page < result.totalPages
                        _recentResources.update { current ->
                            val existingIds = current.mapTo(HashSet(current.size)) { it.id }
                            val newOnes = result.resources.filter { existingIds.add(it.id) }
                            if (newOnes.isEmpty()) current else current + newOnes
                        }
                    },
                    onFailure = {
                        hasMoreResources = false
                    }
                )
            }
            _isLoadingMore.value = false
        }
    }

    /** Posts that scrolled into view; the server counts one impression per viewer per day. */
    fun reportImpressions(ids: List<String>) {
        viewModelScope.launch { forumRepository.reportImpressions(ids) }
    }

    fun toggleThumbsUp(postId: String) {
        if (processingPostLikes.contains(postId)) return
        val current = _recentPosts.value.firstOrNull { it.id == postId } ?: return
        processingPostLikes.add(postId)
        val optimistic = current.copy(
            isThumbedUp = !current.isThumbedUp,
            thumbsUpCount = (current.thumbsUpCount + if (current.isThumbedUp) -1 else 1).coerceAtLeast(0)
        )
        updatePostEverywhere(optimistic)
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    updatePostEverywhere(
                        current.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp)
                    )
                }
                .onFailure { updatePostEverywhere(current) }
            processingPostLikes.remove(postId)
        }
    }

    private fun updatePostEverywhere(updatedPost: ApiPost) {
        _recentPosts.update { posts ->
            val updated = posts.map { if (it.id == updatedPost.id) updatedPost else it }
            postSlices[sliceKey()] = updated to _hasMorePosts.value
            if (_sort.value == "hot" && _selectedCategory.value == null) {
                appCache.recentPosts = updated
            }
            updated
        }
    }

    fun toggleBookmark(postId: String) {
        if (processingBookmarks.contains(postId)) return
        val current = _recentPosts.value.firstOrNull { it.id == postId } ?: return
        processingBookmarks.add(postId)
        val optimistic = current.copy(isBookmarked = !(current.isBookmarked == true))
        updatePostEverywhere(optimistic)
        viewModelScope.launch {
            forumRepository.toggleBookmark("post", postId)
                .onSuccess { response ->
                    updatePostEverywhere(current.copy(isBookmarked = response.isBookmarked))
                }
                .onFailure {
                    updatePostEverywhere(current)
                }
            processingBookmarks.remove(postId)
        }
    }

    fun reportPost(postId: String, reason: String, description: String) {
        viewModelScope.launch {
            forumRepository.createReport("post", postId, reason, description)
                .onSuccess { _snackbarMessage.tryEmit("Report submitted") }
                .onFailure { _snackbarMessage.tryEmit("Couldn't submit report") }
        }
    }

    fun archivePost(postId: String) {
        val current = _recentPosts.value.firstOrNull { it.id == postId } ?: return
        viewModelScope.launch {
            forumRepository.archivePost(postId)
                .onSuccess {
                    updatePostEverywhere(current.copy(isArchived = !(current.isArchived == true)))
                }
                .onFailure { _snackbarMessage.tryEmit("Couldn't archive post") }
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
                        postSlices[sliceKey()] = updated to _hasMorePosts.value
                        if (_sort.value == "hot" && _selectedCategory.value == null) {
                            appCache.recentPosts = updated
                        }
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

    private val processingFollows = mutableSetOf<String>()

    fun toggleFollowUser(userId: String) {
        if (userId.isBlank() || processingFollows.contains(userId)) return
        processingFollows.add(userId)
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken()
                if (token == null) {
                    processingFollows.remove(userId)
                    return@launch
                }
                val response = apiService.toggleFollow(token, userId)
                var handle: String? = null
                _recentPosts.update { posts ->
                    val updated = posts.map { post ->
                        if (post.authorId == userId) {
                            handle = post.authorName
                            post.copy(isFollowingAuthor = response.isFollowing)
                        } else post
                    }
                    appCache.recentPosts = updated
                    updated
                }
                followStateRepository.record(userId, handle, response.isFollowing)
                peopleSuggestionRepository.record(userId, handle, response.isFollowing)
                if (response.isFollowing) {
                    _snackbarMessage.tryEmit("Followed")
                } else {
                    _snackbarMessage.tryEmit("Unfollowed")
                }
            } catch (e: Exception) {
                _snackbarMessage.tryEmit("Couldn't update follow status")
            } finally {
                processingFollows.remove(userId)
            }
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
        combine(
            combine(_isLoading, _isFilterRefreshing, _error) { l, fr, err -> Triple(l, fr, err) },
            combine(_sort, _selectedCategory) { s, c -> s to c },
            combine(_isLoadingMore, _hasMorePosts) { lm, hm -> lm to hm }
        ) { loadingErr, filterPair, pagingPair ->
            HomeStatusState(
                isLoading = loadingErr.first,
                isFilterRefreshing = loadingErr.second,
                error = loadingErr.third,
                sort = filterPair.first,
                selectedCategory = filterPair.second,
                isLoadingMore = pagingPair.first,
                hasMorePosts = pagingPair.second
            )
        }
    ) { values ->
        val user = values[0] as Triple<String, String?, String?>
        @Suppress("UNCHECKED_CAST") val recentResources = values[1] as List<ApiResource>
        @Suppress("UNCHECKED_CAST") val popularResources = values[2] as List<ApiResource>
        @Suppress("UNCHECKED_CAST") val recentPosts = values[3] as List<ApiPost>
        @Suppress("UNCHECKED_CAST") val latestNews = values[4] as List<NewsAnnouncement>
        val status = values[5] as HomeStatusState
        HomeUiState(
            userName = user.first,
            userPhotoUrl = user.second,
            currentUserId = user.third,
            recentResources = recentResources,
            popularResources = popularResources,
            recentPosts = recentPosts,
            latestNews = latestNews,
            sort = status.sort,
            selectedCategory = status.selectedCategory,
            isLoading = status.isLoading,
            isFilterRefreshing = status.isFilterRefreshing,
            isLoadingMore = status.isLoadingMore,
            hasMorePosts = status.hasMorePosts,
            error = status.error
        )
    }.stateIn(viewModelScope, SharingStarted.Eagerly, HomeUiState(
        userName = (authRepository.currentUserNameFlow as StateFlow).value
    ))
}
