package com.consica.code.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface LessonProgressDao {
    @Query("SELECT * FROM lesson_progress")
    fun observeAll(): Flow<List<LessonProgressEntity>>

    @Query("SELECT * FROM lesson_progress WHERE lessonId = :id")
    suspend fun get(id: String): LessonProgressEntity?

    @Query("SELECT COUNT(*) FROM lesson_progress WHERE status = 'completed'")
    fun observeCompletedCount(): Flow<Int>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(entity: LessonProgressEntity)

    @Query("DELETE FROM lesson_progress")
    suspend fun clear()
}

@Dao
interface BadgeDao {
    @Query("SELECT * FROM badges ORDER BY unlockedAt DESC")
    fun observeAll(): Flow<List<BadgeEntity>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun unlock(entity: BadgeEntity)

    @Query("SELECT EXISTS(SELECT 1 FROM badges WHERE badgeId = :id)")
    suspend fun isUnlocked(id: String): Boolean

    @Query("DELETE FROM badges")
    suspend fun clear()
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
    suspend fun upsert(entity: WorkspaceEntity): Long

    @Query("DELETE FROM workspaces WHERE id = :id")
    suspend fun delete(id: Long)

    @Query("DELETE FROM workspaces")
    suspend fun clear()
}

@Dao
interface CodeAttemptDao {
    @Query("SELECT * FROM code_attempts WHERE lessonId = :lessonId ORDER BY createdAt DESC LIMIT :limit")
    fun observeForLesson(lessonId: String, limit: Int): Flow<List<CodeAttemptEntity>>

    @Query("SELECT * FROM code_attempts ORDER BY createdAt DESC LIMIT :limit")
    fun observeRecent(limit: Int): Flow<List<CodeAttemptEntity>>

    @Insert
    suspend fun insert(entity: CodeAttemptEntity): Long

    @Query("DELETE FROM code_attempts")
    suspend fun clear()
}

@Dao
interface EcosystemDao {
    @Query("SELECT * FROM ecosystem_items ORDER BY createdAt ASC")
    fun observeAll(): Flow<List<EcosystemItemEntity>>

    @Query("SELECT COUNT(*) FROM ecosystem_items")
    fun observeCount(): Flow<Int>

    @Insert
    suspend fun insert(entity: EcosystemItemEntity): Long

    @Query("DELETE FROM ecosystem_items")
    suspend fun clear()
}
