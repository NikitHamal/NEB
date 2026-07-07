package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiEditHistory
import com.neb.ians.data.api.ApiPollVoteResponse
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.api.BookmarkResponse
import com.neb.ians.data.api.BookmarkToggleRequest
import com.neb.ians.data.api.LikeResponse
import com.neb.ians.data.api.PollVoteRequest
import com.neb.ians.data.api.PostCreateRequest
import com.neb.ians.data.api.PostUpdateRequest
import com.neb.ians.data.api.ReplyCreateRequest
import com.neb.ians.data.api.ReplyUpdateRequest
import com.neb.ians.data.api.ReportRequest
import com.neb.ians.data.api.WebPostCreateRequest
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
    private val authRepository: AuthRepository
) {
    private val _cachedPosts = MutableStateFlow<List<ApiPost>>(emptyList())
    val cachedPosts: Flow<List<ApiPost>> = _cachedPosts.asStateFlow()

    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    /**
     * Paginated post listing matching the web forum.
     * @param sort one of "hot", "new", "top", "discussed" (server-side).
     * @param search free-text search query.
     */
    suspend fun getPosts(
        category: String? = null,
        page: Int? = null,
        sort: String? = null,
        search: String? = null
    ): Result<ForumPostsResult> {
        return try {
            val token = getBearerToken()
            val response = apiService.getPosts(
                bearerToken = token,
                category = category,
                page = page,
                sort = sort,
                search = search?.takeIf { it.isNotBlank() }
            )
            val currentPage = page ?: 1
            if (currentPage == 1) _cachedPosts.value = response.posts
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
            val response = apiService.getReplies(token, postId)
            Result.success(response.replies)
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

    /** Full-featured create (images + poll) via the web AJAX endpoint. */
    suspend fun createPostWeb(request: WebPostCreateRequest): Result<ApiPost> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val post = apiService.createPostWeb(token, request)
            Result.success(post)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** Uploads one post image, returning its hosted URL. */
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

    suspend fun updateReply(replyId: String, content: String): Result<ApiReply> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val reply = apiService.updateReply(token, replyId, ReplyUpdateRequest(content))
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

    /** Toggle a bookmark on a post or reply. targetType: "post" | "reply". */
    suspend fun toggleBookmark(targetType: String, targetId: String): Result<BookmarkResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleBookmark(token, BookmarkToggleRequest(targetType, targetId))
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** Submit a content report. reason: spam|abuse|inappropriate|misinformation|other. */
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

    /** Vote on a poll. Single-choice polls send option_id; multi-select send option_ids. */
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

    /** User search for @mention autocomplete. */
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
