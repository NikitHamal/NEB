package com.consica.code.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

/** Per-lesson progress. One row per lesson the user has touched. */
@Entity(tableName = "lesson_progress")
data class LessonProgressEntity(
    @PrimaryKey val lessonId: String,
    val status: String,          // "in_progress" | "completed"
    val stars: Int = 0,          // 0..3 mastery stars
    val bestCode: String? = null,
    val attempts: Int = 0,
    val completedAt: Long? = null,
    val updatedAt: Long = System.currentTimeMillis(),
)

/** Unlocked badges (we only persist a row once unlocked). */
@Entity(tableName = "badges")
data class BadgeEntity(
    @PrimaryKey val badgeId: String,
    val unlockedAt: Long = System.currentTimeMillis(),
)

/** Saved coding workspace / playground. */
@Entity(tableName = "workspaces")
data class WorkspaceEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val language: String,        // "html" | "python"
    val content: String,
    val lessonId: String? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis(),
)

/** A single run of code, kept for run-history (older users) and "revisit previous work". */
@Entity(tableName = "code_attempts")
data class CodeAttemptEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val lessonId: String? = null,
    val workspaceId: Long? = null,
    val language: String,
    val code: String,
    val output: String,
    val success: Boolean,
    val createdAt: Long = System.currentTimeMillis(),
)

/** A grown element in the user's biome (plant, animal, water, decoration). */
@Entity(tableName = "ecosystem_items")
data class EcosystemItemEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val type: String,            // EcosystemItemType id
    val label: String? = null,   // e.g. the word the user grew ("Sprout")
    val lessonId: String? = null,
    val createdAt: Long = System.currentTimeMillis(),
)
