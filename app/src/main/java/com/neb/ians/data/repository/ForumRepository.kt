package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiEditHistory
import com.neb.ians.data.api.ApiPaginatedPosts
import com.neb.ians.data.api.ApiPaginatedReplies
import com.neb.ians.data.api.ApiPollVoteResponse
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.api.BookmarkResponse
import com.neb.ians.data.api.BookmarkToggleRequest
import com.neb.ians.data.api.LikeResponse
import com.neb.ians.data.api.OfflineException
import com.neb.ians.data.api.PollVoteRequest
import com.neb.ians.data.api.PostCreateRequest
import com.neb.ians.data.api.PostUpdateRequest
import com.neb.ians.data.api.ReplyCreateRequest
import com.neb.ians.data.api.ReplyUpdateRequest
import com.neb.ians.data.api.ReportRequest
import com.neb.ians.data.api.WebPostCreateRequest
import com.neb.ians.data.network.NetworkMonitor
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import okhttp3.MultipartBody
import javax.inject.Inject
import javax.inject.Singleton

data class ForumPostsResult(
    val posts: List<ApiPost>,
    val totalCount: Int,
    val page: Int,
    val totalPages: Int
) {
    val hasMore: Boolean get() = page < totalPages
}

@Singleton
class ForumRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val offlineCacheStore: OfflineCacheStore,
    private val networkMonitor: NetworkMonitor,
    private val appCache: AppCache
) {
    private val _cachedPosts = MutableStateFlow<List<ApiPost>>(emptyList())
    val cachedPosts: Flow<List<ApiPost>> = _cachedPosts.asStateFlow()

    private val listTtlMs = 90 * 1000L
    private val detailTtlMs = 5 * 60 * 1000L
    private val repliesTtlMs = 90 * 1000L
    private val maxCacheAgeMs = 14L * 24L * 60L * 60L * 1000L

    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    fun peekPost(postId: String): ApiPost? {
        return appCache.postDetails[postId]
            ?: _cachedPosts.value.firstOrNull { it.id == postId }
            ?: appCache.recentPosts.firstOrNull { it.id == postId }
            ?: appCache.forumPosts.firstOrNull { it.id == postId }
            ?: appCache.lastProfilePosts.firstOrNull { it.id == postId }
    }

    fun peekReplies(postId: String): List<ApiReply>? = appCache.postReplies[postId]

    suspend fun getPosts(
        category: String? = null,
        page: Int? = null,
        sort: String? = null,
        search: String? = null,
        forceRefresh: Boolean = false
    ): Result<ForumPostsResult> {
        val currentPage = page ?: 1
        val normalizedSearch = search?.takeIf { it.isNotBlank() }
        val cacheKey = postsCacheKey(category, currentPage, sort, normalizedSearch)
        if (!forceRefresh) {
            offlineCacheStore.readFresh<ApiPaginatedPosts>(cacheKey, listTtlMs)?.let { response ->
                return Result.success(applyPostsResponse(response, currentPage))
            }
        }
        if (!networkMonitor.isOnline()) {
            return cachedPostsResult(cacheKey, currentPage) ?: Result.failure(OfflineException())
        }
        return try {
            val token = getBearerToken()
            val response = apiService.getPosts(
                bearerToken = token,
                category = category,
                page = page,
                sort = sort,
                search = normalizedSearch
            )
            offlineCacheStore.write(cacheKey, response)
            offlineCacheStore.trim(maxCacheAgeMs)
            Result.success(applyPostsResponse(response, currentPage))
        } catch (e: Exception) {
            cachedPostsResult(cacheKey, currentPage) ?: Result.failure(e)
        }
    }

    suspend fun getPost(postId: String, forceRefresh: Boolean = false): Result<ApiPost> {
        val cacheKey = postCacheKey(postId)
        if (!forceRefresh) {
            peekPost(postId)?.let { return Result.success(it) }
            offlineCacheStore.readFresh<ApiPost>(cacheKey, detailTtlMs)?.let { post ->
                appCache.postDetails[postId] = post
                return Result.success(post)
            }
        }
        if (!networkMonitor.isOnline()) {
            val cached = offlineCacheStore.read<ApiPost>(cacheKey)
            if (cached != null) {
                appCache.postDetails[postId] = cached
                return Result.success(cached)
            }
            return Result.failure(OfflineException())
        }
        return try {
            val token = getBearerToken()
            val post = apiService.getPost(token, postId)
            appCache.postDetails[postId] = post
            offlineCacheStore.write(cacheKey, post)
            Result.success(post)
        } catch (e: Exception) {
            val cached = offlineCacheStore.read<ApiPost>(cacheKey)
            if (cached != null) {
                appCache.postDetails[postId] = cached
                Result.success(cached)
            } else {
                Result.failure(e)
            }
        }
    }

    suspend fun viewPost(postId: String): Result<Unit> {
        if (!networkMonitor.isOnline()) {
            return Result.failure(OfflineException())
        }
        return try {
            apiService.viewPost(postId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getReplies(postId: String, forceRefresh: Boolean = false): Result<List<ApiReply>> {
        val cacheKey = repliesCacheKey(postId)
        if (!forceRefresh) {
            appCache.postReplies[postId]?.let { return Result.success(it) }
            offlineCacheStore.readFresh<ApiPaginatedReplies>(cacheKey, repliesTtlMs)?.let { response ->
                appCache.postReplies[postId] = response.replies
                return Result.success(response.replies)
            }
        }
        if (!networkMonitor.isOnline()) {
            val cached = offlineCacheStore.read<ApiPaginatedReplies>(cacheKey)
            if (cached != null) {
                appCache.postReplies[postId] = cached.replies
                return Result.success(cached.replies)
            }
            return Result.failure(OfflineException())
        }
        return try {
            val token = getBearerToken()
            val response = apiService.getReplies(token, postId)
            appCache.postReplies[postId] = response.replies
            offlineCacheStore.write(cacheKey, response)
            Result.success(response.replies)
        } catch (e: Exception) {
            val cached = offlineCacheStore.read<ApiPaginatedReplies>(cacheKey)
            if (cached != null) {
                appCache.postReplies[postId] = cached.replies
                Result.success(cached.replies)
            } else {
                Result.failure(e)
            }
        }
    }

    suspend fun createPost(title: String, content: String, category: String): Result<ApiPost> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val post = apiService.createPost(token, PostCreateRequest(title, content, category))
            appCache.postDetails[post.id] = post
            Result.success(post)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createPostWeb(request: WebPostCreateRequest): Result<ApiPost> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val post = apiService.createPostWeb(token, request)
            appCache.postDetails[post.id] = post
            Result.success(post)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun uploadPostImage(part: MultipartBody.Part): Result<String> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.uploadPostImage(token, part)
            if (response.url.isNotBlank()) Result.success(response.url)
            else Result.failure(IllegalStateException(response.error ?: "Upload failed"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updatePost(
        postId: String,
        title: String? = null,
        content: String? = null,
        category: String? = null,
        imageUrls: List<String>? = null
    ): Result<ApiPost> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val post = apiService.updatePost(token, postId, PostUpdateRequest(title, content, category, imageUrls))
            appCache.postDetails[post.id] = post
            offlineCacheStore.write(postCacheKey(post.id), post)
            Result.success(post)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createReply(postId: String, content: String, parentReplyId: String? = null): Result<ApiReply> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val reply = apiService.createReply(token, postId, ReplyCreateRequest(content, parentReplyId))
            val current = appCache.postReplies[postId].orEmpty()
            if (current.none { it.id == reply.id }) {
                val updated = current + reply
                appCache.postReplies[postId] = updated
                offlineCacheStore.write(repliesCacheKey(postId), ApiPaginatedReplies(replies = updated, totalCount = updated.size))
            }
            Result.success(reply)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateReply(replyId: String, content: String): Result<ApiReply> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val reply = apiService.updateReply(token, replyId, ReplyUpdateRequest(content))
            val postId = reply.postId
            val updated = appCache.postReplies[postId].orEmpty().map { if (it.id == replyId) reply else it }
            appCache.postReplies[postId] = updated
            offlineCacheStore.write(repliesCacheKey(postId), ApiPaginatedReplies(replies = updated, totalCount = updated.size))
            Result.success(reply)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleLikePost(postId: String): Result<LikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleLikePost(token, postId)
            appCache.postDetails[postId]?.let { post ->
                appCache.postDetails[postId] = post.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp)
            }
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleLikeReply(replyId: String): Result<LikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleLikeReply(token, replyId)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleBookmark(targetType: String, targetId: String): Result<BookmarkResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleBookmark(token, BookmarkToggleRequest(targetType, targetId))
            if (targetType == "post") {
                appCache.postDetails[targetId]?.let { post ->
                    appCache.postDetails[targetId] = post.copy(isBookmarked = response.isBookmarked)
                }
            }
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createReport(
        targetType: String,
        targetId: String,
        reason: String,
        description: String? = null
    ): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.createReport(
                token,
                ReportRequest(
                    targetType = targetType,
                    targetId = targetId,
                    reason = reason,
                    description = description?.takeIf { it.isNotBlank() },
                    contextPath = "$targetType/$targetId"
                )
            )
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getEditHistory(targetType: String, targetId: String): Result<List<ApiEditHistory>> {
        return try {
            val token = getBearerToken()
            Result.success(apiService.getEditHistory(token, targetType, targetId))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun votePoll(pollId: String, optionIds: List<String>, allowMultiple: Boolean): Result<ApiPollVoteResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val request = if (allowMultiple) {
                PollVoteRequest(optionIds = optionIds)
            } else {
                PollVoteRequest(optionId = optionIds.firstOrNull())
            }
            val response = apiService.votePoll(token, pollId, request)
            if (response.error != null) Result.failure(IllegalStateException(response.error))
            else Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun searchUsers(query: String): Result<List<ApiUserSearchResult>> {
        return try {
            val token = getBearerToken()
            Result.success(apiService.searchUsers(token, query))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deletePost(postId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.deletePost(token, postId)
            appCache.postDetails.remove(postId)
            appCache.postReplies.remove(postId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deleteReply(replyId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.deleteReply(token, replyId)
            appCache.postReplies.keys.toList().forEach { postId ->
                appCache.postReplies[postId] = appCache.postReplies[postId].orEmpty().filterNot { it.id == replyId || it.parentReplyId == replyId }
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun archivePost(postId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.archivePost(token, postId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun archiveReply(replyId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.archiveReply(token, replyId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private suspend fun cachedPostsResult(cacheKey: String, page: Int): Result<ForumPostsResult>? {
        val cached = offlineCacheStore.read<ApiPaginatedPosts>(cacheKey) ?: return null
        return Result.success(applyPostsResponse(cached, page))
    }

    private fun applyPostsResponse(response: ApiPaginatedPosts, page: Int): ForumPostsResult {
        if (page == 1) _cachedPosts.value = response.posts
        response.posts.forEach { appCache.postDetails[it.id] = it }
        val totalPages = maxOf(1, (response.totalCount + 49) / 50)
        return ForumPostsResult(response.posts, response.totalCount, page, totalPages)
    }

    private fun postsCacheKey(category: String?, page: Int, sort: String?, search: String?): String {
        return listOf("posts", category.orEmpty(), page.toString(), sort.orEmpty(), search.orEmpty()).joinToString("|")
    }

    private fun postCacheKey(postId: String): String = "post|$postId"

    private fun repliesCacheKey(postId: String): String = "post-replies|$postId"
}
