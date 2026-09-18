package com.agentx.app.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import com.agentx.app.data.local.entity.ActivityEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ActivityDao {
    @Query("SELECT * FROM activity_log ORDER BY ts DESC LIMIT 300")
    fun observeRecent(): Flow<List<ActivityEntity>>

    @Insert
    suspend fun insert(entry: ActivityEntity): Long

    @Query("DELETE FROM activity_log")
    suspend fun clear()

    @Query("DELETE FROM activity_log WHERE id NOT IN (SELECT id FROM activity_log ORDER BY ts DESC LIMIT 300)")
    suspend fun trim()
}
