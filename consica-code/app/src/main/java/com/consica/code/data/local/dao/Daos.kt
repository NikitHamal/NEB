package com.consica.code.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.consica.code.data.local.entity.CodeAttemptEntity
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.EcosystemItemEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.StreakDayEntity
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.local.entity.WorkspaceFileEntity
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
interface BadgeDao {
    @Query("SELECT * FROM earned_badges ORDER BY earnedAt DESC")
    fun observeAll(): Flow<List<EarnedBadgeEntity>>

    @Query("SELECT * FROM earned_badges WHERE badgeId = :badgeId")
    suspend fun get(badgeId: String): EarnedBadgeEntity?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(badge: EarnedBadgeEntity)

    @Query("UPDATE earned_badges SET celebrationPending = 0 WHERE badgeId = :badgeId")
    suspend fun markCelebrated(badgeId: String)

    @Query("DELETE FROM earned_badges")
    suspend fun clearAll()
}

@Dao
interface EcosystemDao {
    @Query("SELECT * FROM ecosystem_items ORDER BY unlockedAt ASC")
    fun observeAll(): Flow<List<EcosystemItemEntity>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(item: EcosystemItemEntity)

    @Query("DELETE FROM ecosystem_items")
    suspend fun clearAll()
}

@Dao
interface StreakDao {
    @Query("SELECT * FROM streak_days ORDER BY epochDay DESC")
    fun observeAll(): Flow<List<StreakDayEntity>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(day: StreakDayEntity)

    @Query("SELECT * FROM streak_days ORDER BY epochDay DESC LIMIT 60")
    suspend fun recentDays(): List<StreakDayEntity>

    @Query("DELETE FROM streak_days")
    suspend fun clearAll()
}

@Dao
interface WorkspaceDao {
    @Query("SELECT * FROM workspaces ORDER BY updatedAt DESC")
    fun observeAll(): Flow<List<WorkspaceEntity>>

    @Query("SELECT * FROM workspaces WHERE id = :id")
    suspend fun get(id: Long): WorkspaceEntity?

    @Query("SELECT * FROM workspaces WHERE id = :id")
    fun observe(id: Long): Flow<WorkspaceEntity?>

    @Insert
    suspend fun insert(workspace: WorkspaceEntity): Long

    @Update
    suspend fun update(workspace: WorkspaceEntity)

    @Query("DELETE FROM workspaces WHERE id = :id")
    suspend fun delete(id: Long)

    @Query("SELECT * FROM workspace_files WHERE workspaceId = :workspaceId ORDER BY id ASC")
    fun observeFiles(workspaceId: Long): Flow<List<WorkspaceFileEntity>>

    @Query("SELECT * FROM workspace_files WHERE workspaceId = :workspaceId ORDER BY id ASC")
    suspend fun files(workspaceId: Long): List<WorkspaceFileEntity>

    @Insert
    suspend fun insertFile(file: WorkspaceFileEntity): Long

    @Update
    suspend fun updateFile(file: WorkspaceFileEntity)

    @Query("DELETE FROM workspace_files WHERE id = :fileId")
    suspend fun deleteFile(fileId: Long)

    @Query("DELETE FROM workspace_files WHERE workspaceId = :workspaceId")
    suspend fun deleteFilesFor(workspaceId: Long)

    @Query("DELETE FROM workspaces")
    suspend fun clearAll()

    @Query("DELETE FROM workspace_files")
    suspend fun clearAllFiles()
}

@Dao
interface CodeAttemptDao {
    @Insert
    suspend fun insert(attempt: CodeAttemptEntity)

    @Query("SELECT * FROM code_attempts ORDER BY createdAt DESC LIMIT :limit")
    fun observeRecent(limit: Int = 30): Flow<List<CodeAttemptEntity>>

    @Query("SELECT * FROM code_attempts WHERE lessonId = :lessonId ORDER BY createdAt DESC LIMIT 1")
    suspend fun latestForLesson(lessonId: String): CodeAttemptEntity?

    @Query("DELETE FROM code_attempts")
    suspend fun clearAll()
}
