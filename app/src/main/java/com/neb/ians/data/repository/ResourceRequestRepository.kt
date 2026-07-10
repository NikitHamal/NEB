package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiResourceRequest
import com.neb.ians.data.api.ApiResourceRequestCreate
import com.neb.ians.data.api.ApiResourceRequestUpvoteResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ResourceRequestRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    private suspend fun getBearerToken(): String? = authRepository.getBearerToken()

    suspend fun getResourceRequests(
        status: String?,
        subject: String?,
        grade: String?
    ): Result<List<ApiResourceRequest>> = withContext(Dispatchers.IO) {
        runCatching {
            val token = getBearerToken()
            apiService.getResourceRequests(token, status, subject, grade)
        }
    }

    suspend fun createResourceRequest(
        title: String,
        description: String?,
        subject: String?,
        gradeLevel: String?
    ): Result<ApiResourceRequest> = withContext(Dispatchers.IO) {
        runCatching {
            val token = getBearerToken()
            val requestBody = ApiResourceRequestCreate(
                title = title,
                description = description,
                subject = subject,
                gradeLevel = gradeLevel
            )
            if (token != null) {
                apiService.createResourceRequest(token, requestBody)
            } else {
                apiService.createResourceRequestAnonymous(requestBody)
            }
        }
    }

    suspend fun toggleUpvote(requestId: String): Result<ApiResourceRequestUpvoteResponse> = withContext(Dispatchers.IO) {
        runCatching {
            val token = getBearerToken() ?: throw IllegalStateException("Authentication required to upvote")
            apiService.toggleResourceRequestUpvote(token, requestId)
        }
    }
}
