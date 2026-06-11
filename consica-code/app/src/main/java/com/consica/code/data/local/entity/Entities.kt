package com.consica.code.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(tableName = "lesson_progress")
data class LessonProgressEntity(
    @PrimaryKey val lessonId: String,
    val completed: Boolean = false,
    val attempts: Int = 0,
    val completedAt: Long? = null,
    val lastCode: String? = null,
)

@Entity(tableName = "workspaces", indices = [Index("updatedAt")])
data class WorkspaceEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    /** CodeLanguage enum name: PYTHON | HTML */
    val language: String,
    val code: String,
    /** Non-null when this workspace is linked to a lesson. */
    val lessonId: String? = null,
    val isFreePlay: Boolean = true,
    val createdAt: Long,
    val updatedAt: Long,
)

@Entity(tableName = "earned_badges")
data class EarnedBadgeEntity(
    @PrimaryKey val badgeId: String,
    val earnedAt: Long,
)

@Entity(tableName = "run_history", indices = [Index("createdAt")])
data class RunHistoryEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val language: String,
    val code: String,
    val output: String,
    val success: Boolean,
    val lessonId: String? = null,
    val workspaceId: Long? = null,
    val createdAt: Long,
)
