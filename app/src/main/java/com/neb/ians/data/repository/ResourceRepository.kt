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
import com.neb.ians.data.api.ApiPurchaseResponse
import com.neb.ians.data.api.ReportRequest
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import com.neb.ians.data.network.NetworkMonitor
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
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
    private val appCache: AppCache,
    private val cacheBus: CacheBus
) {
    private val _cachedResources = MutableStateFlow<List<ApiResource>>(emptyList())
    val cachedResources: Flow<List<ApiResource>> = _cachedResources.asStateFlow()
    private val bgScope = CoroutineScope(Dispatchers.IO + SupervisorJob())

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
        forceRefresh: Boolean = false,
        cacheOnly: Boolean = false
    ): Result<ResourcesResult> {
        val currentPage = page ?: 1
        val cacheKey = resourcesCacheKey(subject, grade, type, sort, currentPage)

        if (cacheOnly) {
            val cached = offlineCacheStore.read<ApiPaginatedResources>(cacheKey)
            if (cached != null) return Result.success(applyResourcesResponse(cached, currentPage, append))
            return Result.failure(OfflineException())
        }

        if (forceRefresh) {
            if (!networkMonitor.isOnline()) {
                return cachedResourcesResult(cacheKey, currentPage, append) ?: Result.failure(OfflineException())
            }
            return fetchAndCacheResources(subject, grade, type, sort, page, cacheKey, currentPage, append)
        }

        val cached = offlineCacheStore.read<ApiPaginatedResources>(cacheKey)
        if (cached != null) {
            if (networkMonitor.isOnline()) {
                bgScope.launch {
                    try { fetchAndCacheResources(subject, grade, type, sort, page, cacheKey, currentPage, append) } catch (_: Exception) {}
                }
            }
            return Result.success(applyResourcesResponse(cached, currentPage, append))
        }

        if (!networkMonitor.isOnline()) return Result.failure(OfflineException())
        return fetchAndCacheResources(subject, grade, type, sort, page, cacheKey, currentPage, append)
    }

    private suspend fun fetchAndCacheResources(
        subject: String?, grade: String?, type: String?, sort: String?, page: Int?,
        cacheKey: String, currentPage: Int, append: Boolean
    ): Result<ResourcesResult> {
        val token = getBearerToken()
        return try {
            val response = apiService.getResources(token, subject, grade, type, sort, page, pageSize = 50)
            offlineCacheStore.write(cacheKey, response)
            offlineCacheStore.trim(maxCacheAgeMs)
            cacheBus.publish(cacheKey)
            Result.success(applyResourcesResponse(response, currentPage, append))
        } catch (e: Exception) {
            cachedResourcesResult(cacheKey, currentPage, append) ?: Result.failure(e)
        }
    }

    suspend fun getResource(resourceId: String, forceRefresh: Boolean = false, cacheOnly: Boolean = false): Result<ApiResource> {
        val cacheKey = resourceCacheKey(resourceId)

        if (cacheOnly) {
            val cached = offlineCacheStore.read<ApiResource>(cacheKey)
            if (cached != null) {
                appCache.resourceDetails[resourceId] = cached
                return Result.success(cached)
            }
            return Result.failure(OfflineException())
        }

        peekResource(resourceId)?.let { peeked ->
            refreshResourceInBackground(resourceId, cacheKey)
            return Result.success(peeked)
        }

        val cached = offlineCacheStore.read<ApiResource>(cacheKey)
        if (cached != null && !forceRefresh) {
            appCache.resourceDetails[resourceId] = cached
            refreshResourceInBackground(resourceId, cacheKey)
            return Result.success(cached)
        }

        if (!networkMonitor.isOnline()) return Result.failure(OfflineException())
        return try {
            val token = getBearerToken()
            val resource = apiService.getResource(token, resourceId)
            appCache.resourceDetails[resourceId] = resource
            offlineCacheStore.write(cacheKey, resource)
            cacheBus.publish(cacheKey)
            Result.success(resource)
        } catch (e: Exception) {
            val fallback = offlineCacheStore.read<ApiResource>(cacheKey)
            if (fallback != null) {
                appCache.resourceDetails[resourceId] = fallback
                Result.success(fallback)
            } else {
                Result.failure(e)
            }
        }
    }

    private fun refreshResourceInBackground(resourceId: String, cacheKey: String = resourceCacheKey(resourceId)) {
        if (!networkMonitor.isOnline()) return
        bgScope.launch {
            try {
                val token = getBearerToken()
                val resource = apiService.getResource(token, resourceId)
                appCache.resourceDetails[resourceId] = resource
                offlineCacheStore.write(cacheKey, resource)
                cacheBus.publish(cacheKey)
            } catch (_: Exception) {}
        }
    }

    suspend fun toggleLike(resourceId: String): Result<ResourceLikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleLikeResource(token, resourceId)
            appCache.resourceDetails[resourceId]?.let { resource ->
                val updated = resource.copy(likeCount = response.likeCount, isLiked = response.isLiked)
                appCache.resourceDetails[resourceId] = updated
                offlineCacheStore.write(resourceCacheKey(resourceId), updated)
                cacheBus.publish(resourceCacheKey(resourceId))
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

    suspend fun getComments(resourceId: String, forceRefresh: Boolean = false, cacheOnly: Boolean = false): Result<List<ApiResourceComment>> {
        val cacheKey = commentsCacheKey(resourceId)

        if (cacheOnly) {
            val cached = offlineCacheStore.read<ApiResourceCommentsResponse>(cacheKey)
            if (cached != null) {
                appCache.resourceComments[resourceId] = cached.comments
                return Result.success(cached.comments)
            }
            return Result.failure(OfflineException())
        }

        appCache.resourceComments[resourceId]?.let { peeked ->
            refreshCommentsInBackground(resourceId, cacheKey)
            return Result.success(peeked)
        }

        val cached = offlineCacheStore.read<ApiResourceCommentsResponse>(cacheKey)
        if (cached != null && !forceRefresh) {
            appCache.resourceComments[resourceId] = cached.comments
            refreshCommentsInBackground(resourceId, cacheKey)
            return Result.success(cached.comments)
        }

        if (!networkMonitor.isOnline()) return Result.failure(OfflineException())
        return try {
            val token = getBearerToken()
            val response = apiService.getResourceComments(token, resourceId)
            appCache.resourceComments[resourceId] = response.comments
            offlineCacheStore.write(cacheKey, response)
            cacheBus.publish(cacheKey)
            Result.success(response.comments)
        } catch (e: Exception) {
            val fallback = offlineCacheStore.read<ApiResourceCommentsResponse>(cacheKey)
            if (fallback != null) {
                appCache.resourceComments[resourceId] = fallback.comments
                Result.success(fallback.comments)
            } else {
                Result.failure(e)
            }
        }
    }

    private fun refreshCommentsInBackground(resourceId: String, cacheKey: String = commentsCacheKey(resourceId)) {
        if (!networkMonitor.isOnline()) return
        bgScope.launch {
            try {
                val token = getBearerToken()
                val response = apiService.getResourceComments(token, resourceId)
                appCache.resourceComments[resourceId] = response.comments
                offlineCacheStore.write(cacheKey, response)
                cacheBus.publish(cacheKey)
            } catch (_: Exception) {}
        }
    }

    suspend fun createComment(
        resourceId: String,
        content: String,
        parentCommentId: String? = null,
        attachments: List<com.neb.ians.data.api.ApiMediaAttachmentInput> = emptyList()
    ): Result<ApiResourceComment> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val comment = apiService.createResourceComment(
                token, resourceId,
                ApiResourceCommentCreateRequest(content, parentCommentId, attachments)
            )
            val updated = appCache.resourceComments[resourceId].orEmpty() + comment
            appCache.resourceComments[resourceId] = updated
            offlineCacheStore.write(commentsCacheKey(resourceId), ApiResourceCommentsResponse(updated))
            cacheBus.publish(commentsCacheKey(resourceId))
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
            cacheBus.publish(commentsCacheKey(resourceId))
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
            cacheBus.publish(commentsCacheKey(resourceId))
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

    /**
     * Owner edit — mirrors everything the upload flow can set (metadata, link,
     * file replacement, cover upload/URL/clear). The server resets approval to
     * pending, so the fresh copy goes straight into every cache layer.
     */
    suspend fun updateResource(
        resourceId: String,
        fields: Map<String, RequestBody>,
        filePart: MultipartBody.Part? = null,
        thumbnailPart: MultipartBody.Part? = null
    ): Result<ApiResource> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val updated = apiService.updateResource(token, resourceId, filePart, thumbnailPart, fields)
            appCache.resourceDetails[resourceId] = updated
            offlineCacheStore.write(resourceCacheKey(resourceId), updated)
            cacheBus.publish(resourceCacheKey(resourceId))
            Result.success(updated)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun reportResource(resourceId: String, reason: String, description: String?): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.createReport(
                token,
                ReportRequest(
                    targetType = "resource",
                    targetId = resourceId,
                    reason = reason,
                    description = description?.takeIf { it.isNotBlank() },
                    contextPath = "resource/$resourceId"
                )
            )
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** Fetch the buyer-scoped purchase status for a paid resource (price + access). */
    suspend fun getPurchaseStatus(resourceId: String): Result<ApiPurchaseResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.getResourcePurchaseStatus(token, resourceId)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /** Submit a QR payment proof (transaction id + optional screenshot). The
     *  server creates/updates a pending PaymentVerification. Returns the fresh
     *  status so the caller can refresh the locked/unlocked UI. */
    suspend fun submitPurchase(
        resourceId: String,
        transactionId: String,
        proofFile: java.io.File?
    ): Result<ApiPurchaseResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val txnRequestBody = transactionId.takeIf { it.isNotBlank() }?.toRequestBody("text/plain".toMediaTypeOrNull())
            val proofPart = proofFile?.let { file ->
                MultipartBody.Part.createFormData("payment_proof", file.name, file.asRequestBody(guessImageMime(file.name)))
            }
            val response = apiService.submitResourcePurchase(token, resourceId, txnRequestBody, proofPart)
            if (response.error != null) Result.failure(IllegalStateException(response.error))
            else Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun guessImageMime(name: String): okhttp3.MediaType? {
        val ext = name.substringAfterLast('.', "").lowercase()
        val mime = when (ext) {
            "png" -> "image/png"
            "webp" -> "image/webp"
            "gif" -> "image/gif"
            "bmp" -> "image/bmp"
            else -> "image/jpeg"
        }
        return mime.toMediaTypeOrNull()
    }

    private fun resourceCacheKey(resourceId: String): String = "resource|$resourceId"

    private fun commentsCacheKey(resourceId: String): String = "resource-comments|$resourceId"
}
