package com.consica.code.domain.content

/**
 * Badge metadata (content layer). Names/descriptions are English literals for v1 and are kept
 * here, away from UI, so they can be localized later. [iconKey] is mapped to a Compose icon in
 * the UI layer (see RewardIcons) to keep this layer free of Android UI types.
 */
data class BadgeDef(
    val id: String,
    val name: String,
    val description: String,
    val iconKey: String,
    /** Mature "skill/mastery/certificate" framing for older learners. */
    val isCertificate: Boolean = false,
)

object BadgeCatalog {
    val all: List<BadgeDef> = listOf(
        BadgeDef("first_sprout", "First Sprout", "You grew your very first seed.", "sprout"),
        BadgeDef("first_print", "Hello, World", "Your first line of Python ran.", "terminal"),
        BadgeDef("web_explorer", "Web Explorer", "Completed the beginner web basics.", "language", isCertificate = true),
        BadgeDef("python_explorer", "Python Explorer", "Completed the beginner Python basics.", "code", isCertificate = true),
        BadgeDef("logician", "Logician", "Mastered data structures & logic.", "psychology", isCertificate = true),
        BadgeDef("capstone", "Capstone Builder", "Finished an advanced project.", "workspace", isCertificate = true),
        BadgeDef("streak_3", "3-Day Streak", "Learned three days in a row.", "streak"),
        BadgeDef("streak_7", "7-Day Streak", "A full week of growing.", "streak"),
        BadgeDef("level_5", "Level 5 Gardener", "Reached level 5.", "level"),
        BadgeDef("ten_lessons", "Ten Sprouts", "Completed ten lessons.", "lessons"),
        BadgeDef("grower_25", "Flourishing Biome", "Grew 25 ecosystem items.", "eco", isCertificate = true),
    )

    private val byId = all.associateBy { it.id }
    fun byId(id: String): BadgeDef? = byId[id]

    /**
     * Pure evaluation of threshold badges from current state. Returns badge ids that should be
     * unlocked. The caller is responsible for ignoring already-unlocked ones.
     */
    fun thresholdUnlocks(
        completedLessons: Int,
        level: Int,
        currentStreak: Int,
        ecosystemCount: Int,
    ): List<String> = buildList {
        if (currentStreak >= 3) add("streak_3")
        if (currentStreak >= 7) add("streak_7")
        if (level >= 5) add("level_5")
        if (completedLessons >= 10) add("ten_lessons")
        if (ecosystemCount >= 25) add("grower_25")
    }
}
