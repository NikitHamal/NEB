package com.consica.code.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(tableName = "lesson_progress")
data class LessonProgressEntity(
    @PrimaryKey val lessonId: String,
    val completed: Boolean = false,
    val stars: Int = 0,
    val attempts: Int = 0,
    val completedAt: Long? = null,
    val lastCode: String? = null,
)

@Entity(tableName = "earned_badges")
data class EarnedBadgeEntity(
    @PrimaryKey val badgeId: String,
    val earnedAt: Long,
    /** True until the celebration animation has been shown once. */
    val celebrationPending: Boolean = true,
)

@Entity(tableName = "ecosystem_items")
data class EcosystemItemEntity(
    @PrimaryKey val itemId: String,
    val unlockedAt: Long,
)

@Entity(tableName = "streak_days")
data class StreakDayEntity(
    /** Local date as epoch day (days since 1970-01-01). */
    @PrimaryKey val epochDay: Long,
)

@Entity(tableName = "workspaces")
data class WorkspaceEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    /** TrackLanguage name: PYTHON or HTML. */
    val language: String,
    val createdAt: Long,
    val updatedAt: Long,
    /** Lesson this workspace was started from, if any. */
    val lessonId: String? = null,
    val templateId: String? = null,
)

@Entity(
    tableName = "workspace_files",
    indices = [Index("workspaceId")],
)
data class WorkspaceFileEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val workspaceId: Long,
    val name: String,
    val content: String,
    val updatedAt: Long,
)

@Entity(
    tableName = "code_attempts",
    indices = [Index("lessonId"), Index("workspaceId")],
)
data class CodeAttemptEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val lessonId: String? = null,
    val workspaceId: Long? = null,
    val language: String,
    val code: String,
    val output: String,
    val success: Boolean,
    val createdAt: Long,
)
