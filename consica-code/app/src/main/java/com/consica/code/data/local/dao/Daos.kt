package com.consica.code.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.RunHistoryEntity
import com.consica.code.data.local.entity.WorkspaceEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ProgressDao {
    @Query("SELECT * FROM lesson_progress")
    fun observeAll(): Flow<List<LessonProgressEntity>>

    @Query("SELECT * FROM lesson_progress WHERE lessonId = :lessonId")
    suspend fun get(lessonId: String): LessonProgressEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(progress: LessonProgressEntity)

    @Query("SELECT COUNT(*) FROM lesson_progress WHERE completed = 1")
    fun observeCompletedCount(): Flow<Int>

    @Query("DELETE FROM lesson_progress")
    suspend fun clearAll()
}

@Dao
interface WorkspaceDao {
    @Query("SELECT * FROM workspaces ORDER BY updatedAt DESC")
    fun observeAll(): Flow<List<WorkspaceEntity>>

    @Query("SELECT * FROM workspaces ORDER BY updatedAt DESC LIMIT :limit")
    fun observeRecent(limit: Int): Flow<List<WorkspaceEntity>>

    @Query("SELECT * FROM workspaces WHERE id = :id")
    suspend fun get(id: Long): WorkspaceEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(workspace: WorkspaceEntity): Long

    @Update
    suspend fun update(workspace: WorkspaceEntity)

    @Query("DELETE FROM workspaces WHERE id = :id")
    suspend fun delete(id: Long)

    @Query("DELETE FROM workspaces")
    suspend fun clearAll()
}

@Dao
interface BadgeDao {
    @Query("SELECT * FROM earned_badges")
    fun observeAll(): Flow<List<EarnedBadgeEntity>>

    @Query("SELECT * FROM earned_badges WHERE badgeId = :badgeId")
    suspend fun get(badgeId: String): EarnedBadgeEntity?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(badge: EarnedBadgeEntity): Long

    @Query("DELETE FROM earned_badges")
    suspend fun clearAll()
}

@Dao
interface RunHistoryDao {
    @Query("SELECT * FROM run_history ORDER BY createdAt DESC LIMIT :limit")
    fun observeRecent(limit: Int): Flow<List<RunHistoryEntity>>

    @Insert
    suspend fun insert(run: RunHistoryEntity)

    @Query("DELETE FROM run_history WHERE id NOT IN (SELECT id FROM run_history ORDER BY createdAt DESC LIMIT 200)")
    suspend fun trim()

    @Query("DELETE FROM run_history")
    suspend fun clearAll()
}
