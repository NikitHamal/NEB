package com.consica.code.domain.content

/** Pure unlocking rules for the linear biome path. */
object Progression {

    /**
     * A lesson is unlocked when it is the first lesson, when the previous lesson in the ordered
     * path is completed, or when professional tools have been unlocked (mastery/age/parent
     * approval) — younger users are never *permanently* blocked from advanced content.
     */
    fun isUnlocked(
        lessonId: String,
        completedLessonIds: Set<String>,
        proUnlocked: Boolean,
    ): Boolean {
        val ordered = LessonCatalog.ordered
        val idx = ordered.indexOfFirst { it.id == lessonId }
        if (idx <= 0) return true
        val prev = ordered[idx - 1]
        if (prev.id in completedLessonIds) return true
        // Pro unlock opens the advanced track even if the chain isn't fully complete.
        val lesson = LessonCatalog.byId(lessonId)
        return proUnlocked && lesson?.trackId == "advanced"
    }

    fun status(
        lessonId: String,
        completedLessonIds: Set<String>,
        proUnlocked: Boolean,
    ): LessonStatus = when {
        lessonId in completedLessonIds -> LessonStatus.COMPLETED
        isUnlocked(lessonId, completedLessonIds, proUnlocked) -> LessonStatus.ACTIVE
        else -> LessonStatus.LOCKED
    }

    /** Heuristic for surfacing the "professional tools" unlock prompt by mastery. */
    fun proUnlockEligible(completedCount: Int, level: Int): Boolean =
        completedCount >= 6 || level >= 4
}

enum class LessonStatus { LOCKED, ACTIVE, COMPLETED }
