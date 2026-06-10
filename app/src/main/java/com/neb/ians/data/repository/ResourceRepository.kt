package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPaginatedResources
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.data.api.ApiResourceCommentCreateRequest
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ResourceLikeResponse
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
    private val authRepository: AuthRepository
) {
    private val _cachedResources = MutableStateFlow<List<ApiResource>>(emptyList())
    val cachedResources: Flow<List<ApiResource>> = _cachedResources.asStateFlow()

    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    suspend fun getResources(
        subject: String? = null,
        grade: String? = null,
        type: String? = null,
        sort: String? = null,
        page: Int? = null
    ): Result<ResourcesResult> {
        return try {
            val token = getBearerToken()
            val response = apiService.getResources(token, subject, grade, type, sort, page)
            _cachedResources.value = response.resources
            val currentPage = page ?: 1
            val totalPages = maxOf(1, (response.totalCount + 49) / 50)
            Result.success(ResourcesResult(response.resources, response.totalCount, currentPage, totalPages))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getResource(resourceId: String): Result<ApiResource> {
        return try {
            val token = getBearerToken()
            val resource = apiService.getResource(token, resourceId)
            Result.success(resource)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggleLike(resourceId: String): Result<ResourceLikeResponse> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleLikeResource(token, resourceId)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun viewResource(resourceId: String): Result<Unit> {
        return try {
            apiService.viewResource(resourceId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getComments(resourceId: String): Result<List<ApiResourceComment>> {
        return try {
            val token = getBearerToken()
            val response = apiService.getResourceComments(token, resourceId)
            Result.success(response.comments)
        } catch (e: Exception) {
            Result.failure(e)
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
            Result.success(comment)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deleteComment(resourceId: String, commentId: String): Result<Unit> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            apiService.deleteResourceComment(token, resourceId, commentId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}