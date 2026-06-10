package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ArenaModel
import com.neb.ians.data.api.ArenaSession
import com.neb.ians.data.api.ArenaSessionCreateRequest
import com.neb.ians.data.api.ArenaSessionDetailResponse
import com.neb.ians.data.api.ArenaSessionUpdateRequest
import com.neb.ians.data.api.NebyStreamClient
import com.neb.ians.data.api.NebyStreamEvent
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class NebyRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val streamClient: NebyStreamClient
) {
    private suspend fun token(): String? = authRepository.getBearerToken()

    suspend fun getModels(): Result<List<ArenaModel>> = runCatching {
        val t = token() ?: error("Not authenticated")
        apiService.getArenaModels(t).models
    }

    suspend fun getSessions(): Result<List<ArenaSession>> = runCatching {
        val t = token() ?: error("Not authenticated")
        apiService.getArenaSessions(t).sessions
    }

    suspend fun createSession(modelId: String, title: String? = null): Result<ArenaSession> = runCatching {
        val t = token() ?: error("Not authenticated")
        apiService.createArenaSession(t, ArenaSessionCreateRequest(modelId, title)).session
    }

    suspend fun getSession(sessionId: String): Result<ArenaSessionDetailResponse> = runCatching {
        val t = token() ?: error("Not authenticated")
        apiService.getArenaSession(t, sessionId)
    }

    suspend fun renameSession(sessionId: String, title: String): Result<Unit> = runCatching {
        val t = token() ?: error("Not authenticated")
        apiService.updateArenaSession(t, sessionId, ArenaSessionUpdateRequest(title = title))
        Unit
    }

    suspend fun deleteSession(sessionId: String): Result<Unit> = runCatching {
        val t = token() ?: error("Not authenticated")
        apiService.deleteArenaSession(t, sessionId)
        Unit
    }

    fun sendMessage(sessionId: String, content: String): Flow<NebyStreamEvent> =
        streamClient.sendMessage(sessionId, content)

    fun regenerate(messageId: String): Flow<NebyStreamEvent> =
        streamClient.regenerate(messageId)
}
