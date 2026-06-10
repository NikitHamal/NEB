package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiBookmark
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.BookmarkToggleRequest
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ContentBookmarkRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    suspend fun getBookmarks(targetType: String? = null, page: Int? = null): Result<List<ApiBookmark>> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.getBookmarks(token, targetType, page)
            Result.success(response.results)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun toggle(targetType: String, targetId: String): Result<Boolean> {
        return try {
            val token = getBearerToken() ?: return Result.failure(IllegalStateException("Not authenticated"))
            val response = apiService.toggleBookmark(token, BookmarkToggleRequest(targetType, targetId))
            Result.success(response.isBookmarked)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
