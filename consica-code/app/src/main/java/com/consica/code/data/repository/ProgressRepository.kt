package com.consica.code.data.repository

import com.consica.code.data.local.dao.BadgeDao
import com.consica.code.data.local.dao.CodeAttemptDao
import com.consica.code.data.local.dao.EcosystemDao
import com.consica.code.data.local.dao.ProgressDao
import com.consica.code.data.local.dao.StreakDao
import com.consica.code.data.local.entity.CodeAttemptEntity
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.EcosystemItemEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.StreakDayEntity
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.model.LevelSystem
import com.consica.code.domain.model.Lesson
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import java.time.LocalDate
import javax.inject.Inject
import javax.inject.Singleton

/** Everything granted by completing a lesson, used to drive celebration UI. */
data class CompletionRewards(
    val xp: Int,
    val sun: Int,
    val water: Int,
    val mastery: Int,
    val newBadgeIds: List<String>,
    val newEcosystemItemIds: List<String>,
    val leveledUpTo: Int? = null,
    val professionalModeJustUnlocked: Boolean = false,
)

@Singleton
class ProgressRepository @Inject constructor(
    private val progressDao: ProgressDao,
    private val badgeDao: BadgeDao,
    private val ecosystemDao: EcosystemDao,
    private val streakDao: StreakDao,
    private val codeAttemptDao: CodeAttemptDao,
    private val prefs: UserPreferencesRepository,
) {
    val allProgress: Flow<List<LessonProgressEntity>> = progressDao.observeAll()
    val earnedBadges: Flow<List<EarnedBadgeEntity>> = badgeDao.observeAll()
    val ecosystemItems: Flow<List<EcosystemItemEntity>> = ecosystemDao.observeAll()
    val completedCount: Flow<Int> = progressDao.observeCompletedCount()
    val streakDays: Flow<List<StreakDayEntity>> = streakDao.observeAll()

    suspend fun progressFor(lessonId: String): LessonProgressEntity? = progressDao.get(lessonId)

    suspend fun recordAttempt(
        lesson: Lesson?,
        workspaceId: Long?,
        language: String,
        code: String,
        output: String,
        success: Boolean,
    ) {
        codeAttemptDao.insert(
            CodeAttemptEntity(
                lessonId = lesson?.id,
                workspaceId = workspaceId,
                language = language,
                code = code,
                output = output,
                success = success,
                createdAt = System.currentTimeMillis(),
            )
        )
        if (lesson != null) {
            val existing = progressDao.get(lesson.id)
            progressDao.upsert(
                (existing ?: LessonProgressEntity(lessonId = lesson.id)).copy(
                    attempts = (existing?.attempts ?: 0) + 1,
                    lastCode = code,
                )
            )
        }
    }

    /**
     * Marks a lesson complete (idempotent) and grants all associated rewards.
     * Returns null when the lesson was already completed.
     */
    suspend fun completeLesson(lesson: Lesson): CompletionRewards? {
        val existing = progressDao.get(lesson.id)
        if (existing?.completed == true) return null

        val statsBefore = prefs.stats.first()
        val now = System.currentTimeMillis()

        progressDao.upsert(
            (existing ?: LessonProgressEntity(lessonId = lesson.id)).copy(
                completed = true,
                stars = 3,
                completedAt = now,
            )
        )

        prefs.addRewards(
            xp = lesson.xpReward.toLong(),
            sun = lesson.sunReward.toLong(),
            water = lesson.waterReward.toLong(),
            mastery = lesson.masteryReward.toLong(),
        )

        val newBadges = mutableListOf<String>()
        lesson.badgeId?.let { badgeId ->
            if (badgeDao.get(badgeId) == null) {
                badgeDao.insert(EarnedBadgeEntity(badgeId = badgeId, earnedAt = now))
                newBadges += badgeId
            }
        }

        val newItems = mutableListOf<String>()
        lesson.ecosystemItemId?.let { itemId ->
            ecosystemDao.insert(EcosystemItemEntity(itemId = itemId, unlockedAt = now))
            newItems += itemId
        }

        newBadges += grantMasteryBadges(statsBefore.masteryPoints + lesson.masteryReward, now)

        val statsAfter = prefs.stats.first()
        val leveledUpTo = statsAfter.level.takeIf { it > statsBefore.level }

        var proJustUnlocked = false
        if (!statsBefore.professionalModeUnlocked &&
            (statsAfter.masteryPoints >= LevelSystem.PRO_UNLOCK_MASTERY ||
                statsAfter.level >= LevelSystem.PRO_UNLOCK_LEVEL)
        ) {
            prefs.unlockProfessionalMode()
            proJustUnlocked = true
        }

        return CompletionRewards(
            xp = lesson.xpReward,
            sun = lesson.sunReward,
            water = lesson.waterReward,
            mastery = lesson.masteryReward,
            newBadgeIds = newBadges,
            newEcosystemItemIds = newItems,
            leveledUpTo = leveledUpTo,
            professionalModeJustUnlocked = proJustUnlocked,
        )
    }

    private suspend fun grantMasteryBadges(masteryPoints: Long, now: Long): List<String> {
        val tiers = listOf(20L to "mastery_bronze", 60L to "mastery_silver", 120L to "mastery_gold")
        val granted = mutableListOf<String>()
        for ((threshold, badgeId) in tiers) {
            if (masteryPoints >= threshold && badgeDao.get(badgeId) == null) {
                badgeDao.insert(EarnedBadgeEntity(badgeId = badgeId, earnedAt = now))
                granted += badgeId
            }
        }
        return granted
    }

    /**
     * Records today as an active day and recomputes the consecutive-day streak.
     * Grants streak badges at 3, 7 and 30 days. Returns newly earned badge ids.
     */
    suspend fun recordDailyActivity(today: LocalDate = LocalDate.now()): List<String> {
        val epochDay = today.toEpochDay()
        streakDao.insert(StreakDayEntity(epochDay))

        val days = streakDao.recentDays().map { it.epochDay }.toSortedSet()
        var streak = 0
        var cursor = epochDay
        while (cursor in days) {
            streak++
            cursor--
        }
        prefs.updateStreak(streak, epochDay)

        val now = System.currentTimeMillis()
        val newBadges = mutableListOf<String>()
        val streakBadges = listOf(3 to "streak_3", 7 to "streak_7", 30 to "streak_30")
        for ((threshold, badgeId) in streakBadges) {
            if (streak >= threshold && badgeDao.get(badgeId) == null) {
                badgeDao.insert(EarnedBadgeEntity(badgeId = badgeId, earnedAt = now))
                newBadges += badgeId
            }
        }
        return newBadges
    }

    suspend fun markBadgeCelebrated(badgeId: String) = badgeDao.markCelebrated(badgeId)

    /** A lesson unlocks when the previous lesson in its biome is complete. */
    suspend fun isLessonUnlocked(lesson: Lesson): Boolean {
        val biomeLessons = LessonCatalog.byBiome(lesson.biomeId)
        val index = biomeLessons.indexOfFirst { it.id == lesson.id }
        if (index <= 0) return isBiomeUnlocked(lesson.biomeId)
        val previous = biomeLessons[index - 1]
        return progressDao.get(previous.id)?.completed == true
    }

    /** A biome unlocks when at least 60% of the previous biome is complete. */
    suspend fun isBiomeUnlocked(biomeId: String): Boolean {
        val ordered = com.consica.code.domain.content.BiomeCatalog.biomes
        val index = ordered.indexOfFirst { it.id == biomeId }
        if (index <= 0) return true
        val previous = ordered[index - 1]
        val previousLessons = LessonCatalog.byBiome(previous.id)
        if (previousLessons.isEmpty()) return true
        val completed = previousLessons.count { progressDao.get(it.id)?.completed == true }
        return completed.toFloat() / previousLessons.size >= 0.6f
    }

    suspend fun resetAllProgress() {
        progressDao.clearAll()
        badgeDao.clearAll()
        ecosystemDao.clearAll()
        streakDao.clearAll()
        codeAttemptDao.clearAll()
        prefs.resetProgress()
    }

    fun recentAttempts(limit: Int = 30): Flow<List<CodeAttemptEntity>> =
        codeAttemptDao.observeRecent(limit)
}
