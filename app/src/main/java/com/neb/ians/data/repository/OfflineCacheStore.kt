package com.neb.ians.data.repository

import android.util.LruCache
import com.neb.ians.data.local.dao.ApiCacheDao
import com.neb.ians.data.local.entity.ApiCacheEntity
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

/**
 * The offline copy of API responses, one JSON row per cache key.
 *
 * A page of posts is tens of kilobytes of JSON, so encoding and decoding run on
 * [Dispatchers.Default], never on the caller's (often main) thread. Decoded values are also kept
 * in memory by key: stale-while-revalidate reads the same page several times in a few seconds
 * (the cached read, the cache-bus re-read after the refresh, the next screen), and only the first
 * of those should pay for a decode.
 */
@Singleton
class OfflineCacheStore @Inject constructor(
    @PublishedApi internal val cacheDao: ApiCacheDao
) {
    @PublishedApi
    internal val json = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    @PublishedApi
    internal class Decoded(val value: Any, val updatedAt: Long, val chars: Int)

    /** Sized by JSON length: about 2 MB of text, a dozen pages and the details opened from them. */
    @PublishedApi
    internal val decoded = object : LruCache<String, Decoded>(1_000_000) {
        override fun sizeOf(key: String, value: Decoded) = value.chars.coerceAtLeast(1)
    }

    @Volatile
    private var lastTrimAt = 0L

    suspend inline fun <reified T> read(cacheKey: String): T? = load(cacheKey, Long.MAX_VALUE)

    suspend inline fun <reified T> readFresh(cacheKey: String, maxAgeMs: Long): T? = load(cacheKey, maxAgeMs)

    @PublishedApi
    internal suspend inline fun <reified T> load(cacheKey: String, maxAgeMs: Long): T? {
        val hit = decoded.get(cacheKey)
        if (hit != null) {
            val value = hit.value
            if (value is T) return if (System.currentTimeMillis() - hit.updatedAt > maxAgeMs) null else value
        }
        return try {
            val entity = cacheDao.get(cacheKey) ?: return null
            if (System.currentTimeMillis() - entity.updatedAt > maxAgeMs) return null
            withContext(Dispatchers.Default) { json.decodeFromString<T>(entity.json) }
                .also { if (it != null) decoded.put(cacheKey, Decoded(it, entity.updatedAt, entity.json.length)) }
        } catch (e: CancellationException) {
            throw e
        } catch (_: Exception) {
            null
        }
    }

    suspend inline fun <reified T> write(cacheKey: String, value: T) {
        try {
            val text = withContext(Dispatchers.Default) { json.encodeToString(value) }
            val now = System.currentTimeMillis()
            if (value != null) decoded.put(cacheKey, Decoded(value, now, text.length))
            cacheDao.upsert(ApiCacheEntity(cacheKey, text, now))
        } catch (e: CancellationException) {
            throw e
        } catch (_: Exception) {
        }
    }

    /**
     * Drops rows older than [maxAgeMs], at most every few hours: the delete reads every row (the
     * age column sits after the JSON), which is too much I/O to repeat after each refresh.
     */
    suspend fun trim(maxAgeMs: Long) {
        val now = System.currentTimeMillis()
        if (now - lastTrimAt < TRIM_EVERY_MS) return
        lastTrimAt = now
        try {
            cacheDao.deleteOlderThan(now - maxAgeMs)
        } catch (e: CancellationException) {
            throw e
        } catch (_: Exception) {
        }
    }

    private companion object {
        const val TRIM_EVERY_MS = 6L * 60L * 60L * 1000L
    }
}
