package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiPaginatedPosts
import com.neb.ians.data.api.LikeResponse
import com.neb.ians.data.api.PostCreateRequest
import com.neb.ians.data.api.ReplyCreateRequest
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject
import javax.inject.Singleton

data class ForumPostsResult(
    val posts: List<ApiPost>,
    val totalCount: Int,
    val page: Int,
    val totalPages: Int
)

@Singleton
class ForumRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    private val _cachedPosts = MutableStateFlow<List<ApiPost>>(emptyList())
    val cachedPosts: Flow<List<ApiPost>> = _cachedPosts.asStateFlow()

    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    suspend fun getPosts(category: String? = null, page: Int? = null): Result<ForumPostsResult> {
        return try {
            val token = getBearerToken()
            val response = apiService.getPosts(token, category, page)
            _cachedPosts.value = response.posts
            val currentPage = page ?: 1
            val totalPages = maxOf(1, (response.totalCount + 49) / 50)
            Result.success(ForumPostsResult(response.posts, response.totalCount, currentPage, totalPages))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getPost(postId: String): Result<ApiPost> {
        return try {
            val token = getBearerToken()
            val post = apiService.getPost(token, postId)
            Result.success(post)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getReplies(postId: String): Result<List<ApiReply>> {
        return try {
            val token = getBearerToken()
            val replies = apiService.getReplies(token, postId)
            Result.success(replies)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createPost(title: String, content: String, category: String): Result<ApiPost> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val post = apiService.createPost(token, PostCreateRequest(title, content, category))
            Result.success(post)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createReply(postId: String, content: String, parentReplyId: String? = null): Result<ApiReply> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val reply = apiService.createReply(token, postId, ReplyCreateRequest(content, parentReplyId))
            Result.success(reply)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleLikePost(postId: String): Result<LikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleLikePost(token, postId)
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

    suspend fun deletePost(postId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.deletePost(token, postId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deleteReply(replyId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.deleteReply(token, replyId)
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
}