package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Who the signed-in user already follows, as one shared answer.
 *
 * The list endpoints do not fill in `isFollowingAuthor`, so every screen that
 * asked a post whether the viewer follows its author got `null` and showed a
 * Follow button to people already followed. This holds the real graph — synced
 * once from `users/{me}/following/`, then kept honest by every toggle — so the
 * suggestion rails and the people screen agree with the profile screen.
 *
 * The follow list only carries usernames, so both the id and the handle are
 * tracked and either one is enough to match.
 */
@Singleton
class FollowStateRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {

    data class Graph(
        val ids: Set<String> = emptySet(),
        val handles: Set<String> = emptySet(),
        val loaded: Boolean = false
    ) {
        fun contains(userId: String?, handle: String?): Boolean {
            if (!userId.isNullOrBlank() && userId in ids) return true
            val normalised = handle?.trim()?.lowercase()?.removePrefix("@")
            return !normalised.isNullOrBlank() && normalised in handles
        }
    }

    private val _graph = MutableStateFlow(Graph())
    val graph: StateFlow<Graph> = _graph.asStateFlow()

    private val mutex = Mutex()
    private var lastSyncedAt = 0L
    private var syncedForUserId: String? = null

    suspend fun sync(forceRefresh: Boolean = false) {
        val now = System.currentTimeMillis()
        mutex.withLock {
            val selfId = authRepository.currentUserIdFlow.first()?.takeIf { it.isNotBlank() }
            if (selfId != syncedForUserId) {
                syncedForUserId = selfId
                lastSyncedAt = 0L
                _graph.value = Graph()
            }
            if (selfId == null) return
            if (!forceRefresh && _graph.value.loaded && now - lastSyncedAt < SYNC_INTERVAL_MS) return
            val token = authRepository.getBearerToken() ?: return
            val results = runCatching { apiService.getFollowing(token, selfId) }.getOrNull() ?: return
            val handles = results.results
                .mapNotNull { it.followingUsername?.trim()?.lowercase()?.takeIf { h -> h.isNotEmpty() } }
                .toSet()
            lastSyncedAt = now
            _graph.update { current ->
                current.copy(handles = handles + current.handles, loaded = true)
            }
        }
    }

    fun record(userId: String?, handle: String?, following: Boolean) {
        val id = userId?.trim()?.takeIf { it.isNotEmpty() }
        val name = handle?.trim()?.lowercase()?.removePrefix("@")?.takeIf { it.isNotEmpty() }
        if (id == null && name == null) return
        _graph.update { current ->
            current.copy(
                ids = if (following) current.ids + listOfNotNull(id) else current.ids - listOfNotNull(id).toSet(),
                handles = if (following) current.handles + listOfNotNull(name) else current.handles - listOfNotNull(name).toSet()
            )
        }
    }

    private companion object {
        const val SYNC_INTERVAL_MS = 5 * 60 * 1000L
    }
}
