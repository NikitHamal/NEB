package com.consica.code.domain.model

/**
 * Age groups drive adaptive difficulty, tone, guidance, editor complexity and rewards.
 */
enum class AgeGroup {
    KIDS,   // 8-12: playful, highly guided
    TEENS,  // 13-16: capable, structured
    ADULTS; // 16+: professional, powerful

    val isYoung: Boolean get() = this == KIDS
}

enum class LearningGoal {
    FUN, SCHOOL, CAREER, CREATIVE
}

enum class ExperienceLevel {
    BRAND_NEW, SOME_BASICS, CONFIDENT
}

enum class ThemeIntensity {
    PLAYFUL, BALANCED, FOCUSED
}

enum class CodingInterest {
    PYTHON, WEB, GAMES, APPS, AI_BASICS, CREATIVE_CODING
}

/** How much Terra guides the learner. */
enum class GuidanceLevel {
    FULL, BALANCED, MINIMAL
}

data class OnboardingProfile(
    val ageGroup: AgeGroup,
    val goal: LearningGoal,
    val experience: ExperienceLevel,
    val themeIntensity: ThemeIntensity,
    val interests: Set<CodingInterest>,
)

/**
 * Aggregated learner state used across dashboards.
 */
data class PlayerStats(
    val xp: Long = 0,
    val sunCoins: Long = 0,
    val waterDrops: Long = 0,
    val streakDays: Int = 0,
    val masteryPoints: Long = 0,
    val professionalModeUnlocked: Boolean = false,
) {
    val level: Int get() = LevelSystem.levelForXp(xp)
    val xpIntoLevel: Long get() = xp - LevelSystem.totalXpForLevel(level)
    val xpForNextLevel: Long get() = LevelSystem.xpToAdvanceFrom(level)
    val levelProgress: Float
        get() = (xpIntoLevel.toFloat() / xpForNextLevel.toFloat()).coerceIn(0f, 1f)
}

/**
 * Level curve: each level requires a gently increasing amount of XP.
 */
object LevelSystem {
    /** XP needed to advance from [level] to level+1. */
    fun xpToAdvanceFrom(level: Int): Long = 100L + (level - 1) * 50L

    /** Total XP required to reach the start of [level]. */
    fun totalXpForLevel(level: Int): Long {
        var total = 0L
        for (l in 1 until level) total += xpToAdvanceFrom(l)
        return total
    }

    fun levelForXp(xp: Long): Int {
        var level = 1
        var remaining = xp
        while (remaining >= xpToAdvanceFrom(level)) {
            remaining -= xpToAdvanceFrom(level)
            level++
        }
        return level
    }

    /** Mastery points needed to unlock professional tools early (younger learners). */
    const val PRO_UNLOCK_MASTERY: Long = 60L

    /** Level at which professional mode unlocks automatically regardless of mastery. */
    const val PRO_UNLOCK_LEVEL: Int = 5
}
