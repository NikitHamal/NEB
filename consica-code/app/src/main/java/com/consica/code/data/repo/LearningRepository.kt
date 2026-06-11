package com.consica.code.data.repo

import com.consica.code.core.model.Biome
import com.consica.code.core.model.Lesson
import com.consica.code.core.model.LessonStatus
import com.consica.code.data.content.BadgeCatalog
import com.consica.code.data.content.LessonCatalog
import com.consica.code.data.local.CcodeDatabase
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.RunHistoryEntity
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.prefs.UserPreferencesRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

/**
 * Aggregates lesson progress, rewards and badges over Room + DataStore.
 * Everything is local — the app is fully offline.
 */
class LearningRepository(
    private val db: CcodeDatabase,
    private val prefs: UserPreferencesRepository,
) {
    private val progressDao get() = db.progressDao()
    private val badgeDao get() = db.badgeDao()
    private val runHistoryDao get() = db.runHistoryDao()
    private val workspaceDao get() = db.workspaceDao()

    val progressMap: Flow<Map<String, LessonProgressEntity>> =
        progressDao.observeAll().map { list -> list.associateBy { it.lessonId } }

    val completedCount: Flow<Int> = progressDao.observeCompletedCount()

    val earnedBadges: Flow<List<EarnedBadgeEntity>> = badgeDao.observeAll()

    val recentRuns: Flow<List<RunHistoryEntity>> = runHistoryDao.observeRecent(20)

    val recentWorkspaces: Flow<List<WorkspaceEntity>> = workspaceDao.observeRecent(5)

    /**
     * Computes the visible status of each lesson given completion state.
     * The first incomplete lesson of each biome chain is UNLOCKED; the rest are LOCKED.
     * A biome unlocks when the previous biome has at least one completed "gate"
     * (its final lesson) OR is fully complete.
     */
    fun statusFor(
        lesson: Lesson,
        progress: Map<String, LessonProgressEntity>,
    ): LessonStatus {
        if (progress[lesson.id]?.completed == true) return LessonStatus.COMPLETED
        val ordered = LessonCatalog.all
        val idx = ordered.indexOfFirst { it.id == lesson.id }
        if (idx == 0) return LessonStatus.UNLOCKED
        // Unlocked when every earlier lesson in the same biome is complete and
        // the previous biome's final lesson is complete (for the first lesson of a biome).
        val biomeLessons = LessonCatalog.lessonsFor(lesson.biome)
        val posInBiome = biomeLessons.indexOfFirst { it.id == lesson.id }
        return if (posInBiome == 0) {
            val prevBiomeOrdinal = lesson.biome.ordinal - 1
            if (prevBiomeOrdinal < 0) return LessonStatus.UNLOCKED
            val prevBiome = Biome.entries[prevBiomeOrdinal]
            val prevLessons = LessonCatalog.lessonsFor(prevBiome)
            val gate = prevLessons.lastOrNull()
            if (gate != null && progress[gate.id]?.completed == true) LessonStatus.UNLOCKED else LessonStatus.LOCKED
        } else {
            val prev = biomeLessons[posInBiome - 1]
            if (progress[prev.id]?.completed == true) LessonStatus.UNLOCKED else LessonStatus.LOCKED
        }
    }

    /** First unlocked-but-not-completed lesson — the "suggested next step". */
    fun suggestedNext(progress: Map<String, LessonProgressEntity>): Lesson? =
        LessonCatalog.all.firstOrNull { lesson ->
            statusFor(lesson, progress) == LessonStatus.UNLOCKED
        }

    suspend fun recordAttempt(lessonId: String, code: String?) {
        val existing = progressDao.get(lessonId)
        progressDao.upsert(
            existing?.copy(attempts = existing.attempts + 1, lastCode = code ?: existing.lastCode)
                ?: LessonProgressEntity(lessonId = lessonId, attempts = 1, lastCode = code),
        )
    }

    /**
     * Marks a lesson complete, grants its rewards and badge.
     * Returns the list of newly earned badge ids (may be empty).
     */
    suspend fun completeLesson(lesson: Lesson, code: String? = null): List<String> {
        val existing = progressDao.get(lesson.id)
        val alreadyCompleted = existing?.completed == true
        progressDao.upsert(
            (existing ?: LessonProgressEntity(lessonId = lesson.id)).copy(
                completed = true,
                completedAt = System.currentTimeMillis(),
                lastCode = code ?: existing?.lastCode,
            ),
        )
        if (alreadyCompleted) return emptyList()

        prefs.addRewards(
            xp = lesson.xpReward,
            sun = lesson.sunReward,
            water = lesson.waterReward,
            mastery = lesson.masteryReward,
        )
        val newBadges = mutableListOf<String>()
        lesson.badgeId?.let { id ->
            if (badgeDao.insert(EarnedBadgeEntity(id, System.currentTimeMillis())) != -1L) {
                newBadges += id
            }
        }
        return newBadges
    }

    /** Awards streak badges; returns newly earned badge ids. */
    suspend fun checkStreakBadges(streak: Int): List<String> {
        val candidates = buildList {
            if (streak >= 3) add(BadgeCatalog.STREAK_3)
            if (streak >= 7) add(BadgeCatalog.STREAK_7)
            if (streak >= 30) add(BadgeCatalog.STREAK_30)
        }
        val earned = mutableListOf<String>()
        for (id in candidates) {
            if (badgeDao.insert(EarnedBadgeEntity(id, System.currentTimeMillis())) != -1L) earned += id
        }
        return earned
    }

    suspend fun awardProBadge(): Boolean =
        badgeDao.insert(EarnedBadgeEntity(BadgeCatalog.PRO_CODER, System.currentTimeMillis())) != -1L

    suspend fun logRun(
        language: String,
        code: String,
        output: String,
        success: Boolean,
        lessonId: String? = null,
        workspaceId: Long? = null,
    ) {
        runHistoryDao.insert(
            RunHistoryEntity(
                language = language,
                code = code,
                output = output,
                success = success,
                lessonId = lessonId,
                workspaceId = workspaceId,
                createdAt = System.currentTimeMillis(),
            ),
        )
        runHistoryDao.trim()
    }

    suspend fun resetAll() {
        progressDao.clearAll()
        badgeDao.clearAll()
        runHistoryDao.clearAll()
        workspaceDao.clearAll()
        prefs.resetProgress()
    }
}
