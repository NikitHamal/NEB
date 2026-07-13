package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiPaginatedResources
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.data.api.ApiResourceCommentCreateRequest
import com.neb.ians.data.api.ApiResourceCommentsResponse
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.BookmarkToggleRequest
import com.neb.ians.data.api.OfflineException
import com.neb.ians.data.api.ResourceLikeResponse
import com.neb.ians.data.api.ApiResourceCommentLikeResponse
import com.neb.ians.data.network.NetworkMonitor
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject
import javax.inject.Singleton

data class ResourcesResult(
    val resources: List<ApiResource>,
    val totalCount: Int,
    val page: Int,
    val totalPages: Int
)

@Singleton
class ResourceRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val offlineCacheStore: OfflineCacheStore,
    private val networkMonitor: NetworkMonitor,
    private val appCache: AppCache
) {
    private val _cachedResources = MutableStateFlow<List<ApiResource>>(emptyList())
    val cachedResources: Flow<List<ApiResource>> = _cachedResources.asStateFlow()

    private val listTtlMs = 2 * 60 * 1000L
    private val detailTtlMs = 5 * 60 * 1000L
    private val commentTtlMs = 2 * 60 * 1000L
    private val maxCacheAgeMs = 14L * 24L * 60L * 60L * 1000L

    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    fun peekResource(resourceId: String): ApiResource? {
        return appCache.resourceDetails[resourceId]
            ?: _cachedResources.value.firstOrNull { it.id == resourceId }
            ?: appCache.recentResources.firstOrNull { it.id == resourceId }
            ?: appCache.popularResources.firstOrNull { it.id == resourceId }
            ?: appCache.libraryResources.firstOrNull { it.id == resourceId }
            ?: appCache.lastProfileResources.firstOrNull { it.id == resourceId }
    }

    fun peekComments(resourceId: String): List<ApiResourceComment>? = appCache.resourceComments[resourceId]

    suspend fun getResources(
        subject: String? = null,
        grade: String? = null,
        type: String? = null,
        sort: String? = null,
        page: Int? = null,
        append: Boolean = false,
        forceRefresh: Boolean = false
    ): Result<ResourcesResult> {
        val currentPage = page ?: 1
        val cacheKey = resourcesCacheKey(subject, grade, type, sort, currentPage)
        if (!forceRefresh) {
            offlineCacheStore.readFresh<ApiPaginatedResources>(cacheKey, listTtlMs)?.let { response ->
                return Result.success(applyResourcesResponse(response, currentPage, append))
            }
        }
        if (!networkMonitor.isOnline()) {
            return cachedResourcesResult(cacheKey, currentPage, append) ?: Result.failure(OfflineException())
        }
        return try {
            val token = getBearerToken()
            val response = apiService.getResources(token, subject, grade, type, sort, page, pageSize = 50)
            offlineCacheStore.write(cacheKey, response)
            offlineCacheStore.trim(maxCacheAgeMs)
            Result.success(applyResourcesResponse(response, currentPage, append))
        } catch (e: Exception) {
            cachedResourcesResult(cacheKey, currentPage, append) ?: Result.failure(e)
        }
    }

    suspend fun getResource(resourceId: String, forceRefresh: Boolean = false): Result<ApiResource> {
        val cacheKey = resourceCacheKey(resourceId)
        if (!forceRefresh) {
            peekResource(resourceId)?.let { return Result.success(it) }
            offlineCacheStore.readFresh<ApiResource>(cacheKey, detailTtlMs)?.let { resource ->
                appCache.resourceDetails[resourceId] = resource
                return Result.success(resource)
            }
        }
        if (!networkMonitor.isOnline()) {
            val cached = offlineCacheStore.read<ApiResource>(cacheKey)
            if (cached != null) {
                appCache.resourceDetails[resourceId] = cached
                return Result.success(cached)
            }
            return Result.failure(OfflineException())
        }
        return try {
            val token = getBearerToken()
            val resource = apiService.getResource(token, resourceId)
            appCache.resourceDetails[resourceId] = resource
            offlineCacheStore.write(cacheKey, resource)
            Result.success(resource)
        } catch (e: Exception) {
            val cached = offlineCacheStore.read<ApiResource>(cacheKey)
            if (cached != null) {
                appCache.resourceDetails[resourceId] = cached
                Result.success(cached)
            } else {
                Result.failure(e)
            }
        }
    }

    suspend fun toggleLike(resourceId: String): Result<ResourceLikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleLikeResource(token, resourceId)
            appCache.resourceDetails[resourceId]?.let { resource ->
                appCache.resourceDetails[resourceId] = resource.copy(likeCount = response.likeCount, isLiked = response.isLiked)
            }
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleBookmark(resourceId: String): Result<Boolean> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleBookmark(
                token,
                BookmarkToggleRequest(targetType = "resource", targetId = resourceId)
            )
            appCache.resourceDetails[resourceId]?.let { resource ->
                appCache.resourceDetails[resourceId] = resource.copy(isBookmarked = response.isBookmarked)
            }
            Result.success(response.isBookmarked)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun viewResource(resourceId: String): Result<Unit> {
        if (!networkMonitor.isOnline()) return Result.success(Unit)
        return try {
            apiService.viewResource(resourceId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getComments(resourceId: String, forceRefresh: Boolean = false): Result<List<ApiResourceComment>> {
        val cacheKey = commentsCacheKey(resourceId)
        if (!forceRefresh) {
            appCache.resourceComments[resourceId]?.let { return Result.success(it) }
            offlineCacheStore.readFresh<ApiResourceCommentsResponse>(cacheKey, commentTtlMs)?.let { response ->
                appCache.resourceComments[resourceId] = response.comments
                return Result.success(response.comments)
            }
        }
        if (!networkMonitor.isOnline()) {
            val cached = offlineCacheStore.read<ApiResourceCommentsResponse>(cacheKey)
            if (cached != null) {
                appCache.resourceComments[resourceId] = cached.comments
                return Result.success(cached.comments)
            }
            return Result.failure(OfflineException())
        }
        return try {
            val token = getBearerToken()
            val response = apiService.getResourceComments(token, resourceId)
            appCache.resourceComments[resourceId] = response.comments
            offlineCacheStore.write(cacheKey, response)
            Result.success(response.comments)
        } catch (e: Exception) {
            val cached = offlineCacheStore.read<ApiResourceCommentsResponse>(cacheKey)
            if (cached != null) {
                appCache.resourceComments[resourceId] = cached.comments
                Result.success(cached.comments)
            } else {
                Result.failure(e)
            }
        }
    }

    suspend fun createComment(
        resourceId: String,
        content: String,
        parentCommentId: String? = null
    ): Result<ApiResourceComment> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val comment = apiService.createResourceComment(
                token, resourceId, ApiResourceCommentCreateRequest(content, parentCommentId)
            )
            val updated = appCache.resourceComments[resourceId].orEmpty() + comment
            appCache.resourceComments[resourceId] = updated
            offlineCacheStore.write(commentsCacheKey(resourceId), ApiResourceCommentsResponse(updated))
            Result.success(comment)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deleteComment(resourceId: String, commentId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.deleteResourceComment(token, resourceId, commentId)
            val updated = appCache.resourceComments[resourceId].orEmpty().filterNot { it.id == commentId }
            appCache.resourceComments[resourceId] = updated
            offlineCacheStore.write(commentsCacheKey(resourceId), ApiResourceCommentsResponse(updated))
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleCommentLike(resourceId: String, commentId: String): Result<ApiResourceCommentLikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleResourceCommentLike(token, resourceId, commentId)
            val currentList = appCache.resourceComments[resourceId].orEmpty()
            val updatedList = currentList.map { comment ->
                if (comment.id == commentId) {
                    comment.copy(
                        likeCountSnake = response.likeCount,
                        likeCountCamel = response.likeCount,
                        isLikedSnake = response.isLiked,
                        isLikedCamel = response.isLiked
                    )
                } else comment
            }
            appCache.resourceComments[resourceId] = updatedList
            offlineCacheStore.write(commentsCacheKey(resourceId), ApiResourceCommentsResponse(updatedList))
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private suspend fun cachedResourcesResult(cacheKey: String, page: Int, append: Boolean): Result<ResourcesResult>? {
        val cached = offlineCacheStore.read<ApiPaginatedResources>(cacheKey) ?: return null
        return Result.success(applyResourcesResponse(cached, page, append))
    }

    private fun applyResourcesResponse(response: ApiPaginatedResources, page: Int, append: Boolean): ResourcesResult {
        _cachedResources.value = if (append) {
            val existingIds = _cachedResources.value.mapTo(HashSet()) { it.id }
            _cachedResources.value + response.resources.filterNot { it.id in existingIds }
        } else {
            response.resources
        }
        response.resources.forEach { appCache.resourceDetails[it.id] = it }
        val totalPages = maxOf(1, (response.totalCount + 49) / 50)
        return ResourcesResult(response.resources, response.totalCount, page, totalPages)
    }

    private fun resourcesCacheKey(subject: String?, grade: String?, type: String?, sort: String?, page: Int): String {
        return listOf("resources", subject.orEmpty(), grade.orEmpty(), type.orEmpty(), sort.orEmpty(), page.toString()).joinToString("|")
    }

    private fun resourceCacheKey(resourceId: String): String = "resource|$resourceId"

    private fun commentsCacheKey(resourceId: String): String = "resource-comments|$resourceId"
}
