package com.consica.code.domain.content

import com.consica.code.R
import com.consica.code.domain.model.BadgeCategory
import com.consica.code.domain.model.BadgeDef

/**
 * Every badge a learner can earn — from the very first sprout to the
 * capstone crown, plus streak and mastery milestones.
 */
object BadgeCatalog {

    val badges: List<BadgeDef> = listOf(

        // ── Special ─────────────────────────────────────────────────────────
        BadgeDef(
            id = "first_sprout",
            nameRes = R.string.badge_first_sprout_name,
            descriptionRes = R.string.badge_first_sprout_desc,
            emoji = "🌱",
            category = BadgeCategory.SPECIAL,
        ),

        // ── Skill badges ────────────────────────────────────────────────────
        BadgeDef(
            id = "web_wanderer",
            nameRes = R.string.badge_web_wanderer_name,
            descriptionRes = R.string.badge_web_wanderer_desc,
            emoji = "🧭",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "html_hero",
            nameRes = R.string.badge_html_hero_name,
            descriptionRes = R.string.badge_html_hero_desc,
            emoji = "🦸",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "css_artist",
            nameRes = R.string.badge_css_artist_name,
            descriptionRes = R.string.badge_css_artist_desc,
            emoji = "🎨",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "python_hatchling",
            nameRes = R.string.badge_python_hatchling_name,
            descriptionRes = R.string.badge_python_hatchling_desc,
            emoji = "🐣",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "loop_ranger",
            nameRes = R.string.badge_loop_ranger_name,
            descriptionRes = R.string.badge_loop_ranger_desc,
            emoji = "🔁",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "function_forester",
            nameRes = R.string.badge_function_forester_name,
            descriptionRes = R.string.badge_function_forester_desc,
            emoji = "🌲",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "bug_squasher",
            nameRes = R.string.badge_bug_squasher_name,
            descriptionRes = R.string.badge_bug_squasher_desc,
            emoji = "🐞",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "river_builder",
            nameRes = R.string.badge_river_builder_name,
            descriptionRes = R.string.badge_river_builder_desc,
            emoji = "🏗️",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "grove_thinker",
            nameRes = R.string.badge_grove_thinker_name,
            descriptionRes = R.string.badge_grove_thinker_desc,
            emoji = "🧠",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "clean_coder",
            nameRes = R.string.badge_clean_coder_name,
            descriptionRes = R.string.badge_clean_coder_desc,
            emoji = "✨",
            category = BadgeCategory.SKILL,
        ),
        BadgeDef(
            id = "algorithm_ace",
            nameRes = R.string.badge_algorithm_ace_name,
            descriptionRes = R.string.badge_algorithm_ace_desc,
            emoji = "🦅",
            category = BadgeCategory.SKILL,
        ),

        // ── Project badges ──────────────────────────────────────────────────
        BadgeDef(
            id = "project_pioneer",
            nameRes = R.string.badge_project_pioneer_name,
            descriptionRes = R.string.badge_project_pioneer_desc,
            emoji = "⛰️",
            category = BadgeCategory.PROJECT,
        ),
        BadgeDef(
            id = "capstone",
            nameRes = R.string.badge_capstone_name,
            descriptionRes = R.string.badge_capstone_desc,
            emoji = "🌈",
            category = BadgeCategory.PROJECT,
        ),

        // ── Streak badges ───────────────────────────────────────────────────
        BadgeDef(
            id = "streak_3",
            nameRes = R.string.badge_streak_3_name,
            descriptionRes = R.string.badge_streak_3_desc,
            emoji = "🔥",
            category = BadgeCategory.STREAK,
        ),
        BadgeDef(
            id = "streak_7",
            nameRes = R.string.badge_streak_7_name,
            descriptionRes = R.string.badge_streak_7_desc,
            emoji = "🌟",
            category = BadgeCategory.STREAK,
        ),
        BadgeDef(
            id = "streak_30",
            nameRes = R.string.badge_streak_30_name,
            descriptionRes = R.string.badge_streak_30_desc,
            emoji = "🏆",
            category = BadgeCategory.STREAK,
        ),

        // ── Mastery badges ──────────────────────────────────────────────────
        BadgeDef(
            id = "mastery_bronze",
            nameRes = R.string.badge_mastery_bronze_name,
            descriptionRes = R.string.badge_mastery_bronze_desc,
            emoji = "🥉",
            category = BadgeCategory.MASTERY,
        ),
        BadgeDef(
            id = "mastery_silver",
            nameRes = R.string.badge_mastery_silver_name,
            descriptionRes = R.string.badge_mastery_silver_desc,
            emoji = "🥈",
            category = BadgeCategory.MASTERY,
        ),
        BadgeDef(
            id = "mastery_gold",
            nameRes = R.string.badge_mastery_gold_name,
            descriptionRes = R.string.badge_mastery_gold_desc,
            emoji = "🥇",
            category = BadgeCategory.MASTERY,
        ),
    )

    private val index: Map<String, BadgeDef> = badges.associateBy { it.id }

    fun byId(id: String): BadgeDef? = index[id]
}
