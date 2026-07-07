package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.neb.ians.data.local.entity.ApiCacheEntity

@Dao
interface ApiCacheDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(entity: ApiCacheEntity)

    @Query("SELECT * FROM api_cache WHERE cacheKey = :cacheKey LIMIT 1")
    suspend fun get(cacheKey: String): ApiCacheEntity?

    @Query("DELETE FROM api_cache WHERE updatedAt < :cutoff")
    suspend fun deleteOlderThan(cutoff: Long)
}
