package com.consica.code.data.prefs

import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.ExperienceLevel
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.Interest
import com.consica.code.core.model.LearningGoal
import com.consica.code.core.model.ThemeIntensity

/** Immutable snapshot of everything stored in DataStore. */
data class UserPrefs(
    val onboardingComplete: Boolean = false,
    val ageGroup: AgeGroup = AgeGroup.KIDS,
    val goal: LearningGoal = LearningGoal.BASICS,
    val experience: ExperienceLevel = ExperienceLevel.NONE,
    val intensity: ThemeIntensity = ThemeIntensity.BALANCED,
    val interests: Set<Interest> = emptySet(),
    val guidance: GuidanceLevel = GuidanceLevel.FULL,
    // Accessibility / app settings
    val highContrast: Boolean = false,
    val reducedMotion: Boolean = false,
    val soundEnabled: Boolean = true,
    val fontScale: Float = 1f,
    val darkMode: DarkMode = DarkMode.SYSTEM,
    val proUnlocked: Boolean = false,
    // Gamification counters
    val xp: Int = 0,
    val sunCoins: Int = 0,
    val waterDrops: Int = 0,
    val masteryPoints: Int = 0,
    val currentStreak: Int = 0,
    val bestStreak: Int = 0,
    val lastActiveEpochDay: Long = 0L,
) {
    /** XP curve: each level needs a bit more than the last. */
    val level: Int get() = levelForXp(xp)

    val xpIntoLevel: Int get() = xp - xpForLevel(level)
    val xpForNextLevel: Int get() = xpForLevel(level + 1) - xpForLevel(level)

    companion object {
        fun xpForLevel(level: Int): Int {
            // Level 1 starts at 0 XP. Cumulative cost grows ~quadratically.
            if (level <= 1) return 0
            val n = level - 1
            return 50 * n * (n + 1) / 2 + 50 * n
        }

        fun levelForXp(xp: Int): Int {
            var lvl = 1
            while (xpForLevel(lvl + 1) <= xp) lvl++
            return lvl
        }
    }
}

enum class DarkMode(val id: String) {
    SYSTEM("system"), LIGHT("light"), DARK("dark");
    companion object { fun from(id: String?) = entries.firstOrNull { it.id == id } ?: SYSTEM }
}
