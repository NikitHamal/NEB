package com.consica.code.data.repository

import com.consica.code.core.model.EcosystemItemType
import com.consica.code.data.local.BadgeDao
import com.consica.code.data.local.BadgeEntity
import com.consica.code.data.local.CodeAttemptDao
import com.consica.code.data.local.CodeAttemptEntity
import com.consica.code.data.local.EcosystemDao
import com.consica.code.data.local.EcosystemItemEntity
import com.consica.code.data.local.LessonProgressDao
import com.consica.code.data.local.LessonProgressEntity
import com.consica.code.data.prefs.SettingsDataStore
import com.consica.code.data.prefs.UserPrefs
import com.consica.code.domain.content.BadgeCatalog
import com.consica.code.domain.content.BadgeDef
import com.consica.code.domain.content.Lesson
import com.consica.code.domain.runner.RunResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import java.util.concurrent.TimeUnit

/** Result of completing a lesson — drives celebration UI. */
data class CompletionResult(
    val xpGained: Int,
    val sunGained: Int,
    val waterGained: Int,
    val leveledUp: Boolean,
    val newLevel: Int,
    val newBadges: List<BadgeDef>,
    val grew: EcosystemItemType,
)

/** Central gameplay repository combining DataStore counters with Room collections. */
class GameRepository(
    private val settings: SettingsDataStore,
    private val lessonProgressDao: LessonProgressDao,
    private val badgeDao: BadgeDao,
    private val ecosystemDao: EcosystemDao,
    private val codeAttemptDao: CodeAttemptDao,
) {
    val prefs: Flow<UserPrefs> = settings.prefs

    val lessonProgress: Flow<List<LessonProgressEntity>> = lessonProgressDao.observeAll()
    val completedLessonIds: Flow<Set<String>> = lessonProgressDao.observeAll()
        .map { list -> list.filter { it.status == "completed" }.map { it.lessonId }.toSet() }
    val completedCount: Flow<Int> = lessonProgressDao.observeCompletedCount()
    val badges: Flow<List<BadgeEntity>> = badgeDao.observeAll()
    val ecosystem: Flow<List<EcosystemItemEntity>> = ecosystemDao.observeAll()
    val ecosystemCount: Flow<Int> = ecosystemDao.observeCount()

    suspend fun startLesson(lessonId: String) {
        if (lessonProgressDao.get(lessonId) == null) {
            lessonProgressDao.upsert(LessonProgressEntity(lessonId = lessonId, status = "in_progress"))
        }
    }

    suspend fun recordAttempt(lesson: Lesson, code: String, result: RunResult) {
        codeAttemptDao.insert(
            CodeAttemptEntity(
                lessonId = lesson.id,
                language = lesson.lang?.id ?: "html",
                code = code,
                output = result.output,
                success = result.success,
            )
        )
        val existing = lessonProgressDao.get(lesson.id)
        lessonProgressDao.upsert(
            (existing ?: LessonProgressEntity(lessonId = lesson.id, status = "in_progress"))
                .copy(attempts = (existing?.attempts ?: 0) + 1)
        )
    }

    /** Mark a lesson complete, award rewards, grow the biome, unlock badges, bump streak. */
    suspend fun completeLesson(lesson: Lesson, code: String, stars: Int = 3): CompletionResult {
        val before = settings.prefs.first()
        val alreadyDone = lessonProgressDao.get(lesson.id)?.status == "completed"

        lessonProgressDao.upsert(
            LessonProgressEntity(
                lessonId = lesson.id, status = "completed", stars = stars,
                bestCode = code, completedAt = System.currentTimeMillis(),
            )
        )
        ecosystemDao.insert(
            EcosystemItemEntity(type = lesson.grow.id, label = lessonGrowLabel(lesson, code), lessonId = lesson.id)
        )

        // Award rewards only the first time a lesson is completed.
        if (!alreadyDone) {
            settings.addRewards(xp = lesson.xp, sun = lesson.sun, water = lesson.water, mastery = lesson.mastery)
        }
        touchDailyStreak()

        val after = settings.prefs.first()
        val newBadges = ArrayList<BadgeDef>()

        // Lesson-specific badge
        lesson.badgeId?.let { id ->
            if (!badgeDao.isUnlocked(id)) {
                badgeDao.unlock(BadgeEntity(id)); BadgeCatalog.byId(id)?.let(newBadges::add)
            }
        }
        // Threshold badges
        val completed = completedCount.first()
        val ecoCount = ecosystemCount.first()
        BadgeCatalog.thresholdUnlocks(completed, after.level, after.currentStreak, ecoCount).forEach { id ->
            if (!badgeDao.isUnlocked(id)) {
                badgeDao.unlock(BadgeEntity(id)); BadgeCatalog.byId(id)?.let(newBadges::add)
            }
        }

        return CompletionResult(
            xpGained = if (alreadyDone) 0 else lesson.xp,
            sunGained = if (alreadyDone) 0 else lesson.sun,
            waterGained = if (alreadyDone) 0 else lesson.water,
            leveledUp = after.level > before.level,
            newLevel = after.level,
            newBadges = newBadges,
            grew = lesson.grow,
        )
    }

    private fun lessonGrowLabel(lesson: Lesson, code: String): String? {
        // For the seed lesson, surface the word the learner grew.
        if (lesson.id == "seed_html_heading") {
            Regex("<h1[^>]*>(.*?)</h1>", RegexOption.IGNORE_CASE).find(code)?.let {
                return it.groupValues[1].trim().ifBlank { null }
            }
        }
        return null
    }

    suspend fun growFreeform(type: EcosystemItemType, label: String?) {
        ecosystemDao.insert(EcosystemItemEntity(type = type.id, label = label))
    }

    suspend fun touchDailyStreak() {
        val today = TimeUnit.MILLISECONDS.toDays(System.currentTimeMillis())
        settings.touchStreak(today)
    }

    suspend fun unlockPro() = settings.setProUnlocked(true)

    suspend fun resetAll() {
        lessonProgressDao.clear()
        badgeDao.clear()
        ecosystemDao.clear()
        codeAttemptDao.clear()
        settings.resetProgress()
    }
}
