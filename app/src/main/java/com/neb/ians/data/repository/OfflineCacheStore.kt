package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.ApiCacheDao
import com.neb.ians.data.local.entity.ApiCacheEntity
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class OfflineCacheStore @Inject constructor(
    @PublishedApi internal val cacheDao: ApiCacheDao
) {
    @PublishedApi
    internal val json = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    suspend inline fun <reified T> read(cacheKey: String): T? {
        return try {
            cacheDao.get(cacheKey)?.let { json.decodeFromString<T>(it.json) }
        } catch (_: Exception) {
            null
        }
    }

    suspend inline fun <reified T> readFresh(cacheKey: String, maxAgeMs: Long): T? {
        return try {
            val entity = cacheDao.get(cacheKey) ?: return null
            if (System.currentTimeMillis() - entity.updatedAt > maxAgeMs) return null
            json.decodeFromString<T>(entity.json)
        } catch (_: Exception) {
            null
        }
    }

    suspend inline fun <reified T> write(cacheKey: String, value: T) {
        try {
            cacheDao.upsert(ApiCacheEntity(cacheKey, json.encodeToString(value), System.currentTimeMillis()))
        } catch (_: Exception) {
        }
    }

    suspend fun trim(maxAgeMs: Long) {
        try {
            cacheDao.deleteOlderThan(System.currentTimeMillis() - maxAgeMs)
        } catch (_: Exception) {
        }
    }
}
