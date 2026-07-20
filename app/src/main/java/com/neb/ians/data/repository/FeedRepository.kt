package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiSuggestedFeedResponse
import com.neb.ians.data.api.ApiSuggestedItem
import com.neb.ians.data.api.OfflineException
import com.neb.ians.data.network.NetworkMonitor
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Backs the "Suggested for you" deck (home). Stale-while-revalidate:
 * cached deck renders instantly, a background fetch refreshes it and
 * publishes through the [CacheBus] so open screens update silently.
 */
@Singleton
class FeedRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val offlineCacheStore: OfflineCacheStore,
    private val networkMonitor: NetworkMonitor,
    private val appCache: AppCache,
    private val cacheBus: CacheBus
) {
    private val bgScope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private val cacheKey = CacheBus.PREFIX_SUGGESTED + "home|v1"

    suspend fun getSuggestedFeed(
        limit: Int = 18,
        forceRefresh: Boolean = false,
        cacheOnly: Boolean = false
    ): Result<List<ApiSuggestedItem>> {
        if (cacheOnly) {
            val cached = offlineCacheStore.read<ApiSuggestedFeedResponse>(cacheKey)
            val items = cached?.items?.filter { it.isUsable() }.orEmpty()
            if (items.isNotEmpty()) {
                appCache.suggestedItems = items
                return Result.success(items)
            }
            if (appCache.suggestedItems.isNotEmpty()) return Result.success(appCache.suggestedItems)
            return Result.failure(OfflineException())
        }

        if (!forceRefresh) {
            val cached = offlineCacheStore.read<ApiSuggestedFeedResponse>(cacheKey)
            val items = cached?.items?.filter { it.isUsable() }.orEmpty()
            if (items.isNotEmpty()) {
                appCache.suggestedItems = items
                refreshInBackground(limit)
                return Result.success(items)
            }
            if (appCache.suggestedItems.isNotEmpty()) {
                refreshInBackground(limit)
                return Result.success(appCache.suggestedItems)
            }
        }

        if (!networkMonitor.isOnline()) {
            if (appCache.suggestedItems.isNotEmpty()) return Result.success(appCache.suggestedItems)
            return Result.failure(OfflineException())
        }
        return fetchAndCache(limit)
    }

    fun refreshInBackground(limit: Int = 18) {
        if (!networkMonitor.isOnline()) return
        bgScope.launch {
            try {
                val response = apiService.getSuggestedFeed(authRepository.getBearerToken(), limit)
                val items = response.items.filter { it.isUsable() }
                if (response.ok && items.isNotEmpty()) {
                    appCache.suggestedItems = items
                    offlineCacheStore.write(cacheKey, response)
                    cacheBus.publish(cacheKey)
                }
            } catch (_: Exception) {}
        }
    }

    private suspend fun fetchAndCache(limit: Int): Result<List<ApiSuggestedItem>> {
        return try {
            val response = apiService.getSuggestedFeed(authRepository.getBearerToken(), limit)
            val items = response.items.filter { it.isUsable() }
            if (items.isNotEmpty()) {
                appCache.suggestedItems = items
                offlineCacheStore.write(cacheKey, response)
                cacheBus.publish(cacheKey)
                Result.success(items)
            } else {
                Result.failure(IllegalStateException("No suggestions available yet"))
            }
        } catch (e: Exception) {
            val cached = offlineCacheStore.read<ApiSuggestedFeedResponse>(cacheKey)
            val items = cached?.items?.filter { it.isUsable() }.orEmpty()
            when {
                items.isNotEmpty() -> Result.success(items)
                appCache.suggestedItems.isNotEmpty() -> Result.success(appCache.suggestedItems)
                else -> Result.failure(e)
            }
        }
    }

    private fun ApiSuggestedItem.isUsable(): Boolean =
        (type == "post" && post != null) || (type == "resource" && resource != null)
}
