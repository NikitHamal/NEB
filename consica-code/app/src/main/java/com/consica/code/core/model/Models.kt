package com.consica.code.core.model

import androidx.annotation.StringRes

/**
 * Age groups chosen during onboarding. The whole app adapts tone, density,
 * tooling and rewards based on this value.
 */
enum class AgeGroup {
    /** 8-12: bright, playful, heavily guided. */
    KIDS,

    /** 13-16: capable, structured, less childish. */
    TEENS,

    /** 16+: professional tools, mature interface. */
    PRO;

    val isKid: Boolean get() = this == KIDS
    val isPro: Boolean get() = this == PRO
}

enum class ExperienceLevel { BRAND_NEW, SOME_BASICS, CONFIDENT }

enum class LearningGoal { FOR_FUN, SCHOOL, FUTURE_CAREER, BUILD_THINGS }

enum class ThemeIntensity { PLAYFUL, BALANCED, FOCUSED }

enum class CodingInterest { PYTHON, WEB, GAMES, APPS, AI_BASICS, CREATIVE }

enum class GuidanceLevel { FULL, BALANCED, MINIMAL }

enum class CodeLanguage { PYTHON, HTML }

/** Expressions supported by Terra the Owl. */
enum class TerraExpression {
    HAPPY, EXCITED, THINKING, CONFUSED, PROUD, SLEEPY, FOCUSED, PROFESSIONAL, ENCOURAGING
}

/**
 * Biomes are the themed environments of the vertical progression map.
 * Each biome maps to a learning path section.
 */
enum class Biome(
    @StringRes val titleRes: Int,
    @StringRes val subtitleRes: Int,
) {
    FOREST_FLOOR(com.consica.code.R.string.biome_forest_floor, com.consica.code.R.string.biome_forest_floor_sub),
    SUNNY_MEADOW(com.consica.code.R.string.biome_sunny_meadow, com.consica.code.R.string.biome_sunny_meadow_sub),
    RIVERBANK(com.consica.code.R.string.biome_riverbank, com.consica.code.R.string.biome_riverbank_sub),
    CANOPY(com.consica.code.R.string.biome_canopy, com.consica.code.R.string.biome_canopy_sub),
}

enum class LessonType { TUTORIAL, CODE, PUZZLE }

/**
 * A piece of dialogue/text that adapts to the learner's age group.
 * The same resource id may be reused across slots when no variant is needed,
 * which keeps every string localizable without duplicating UI logic.
 */
data class AgeAdaptiveText(
    @StringRes val kids: Int,
    @StringRes val teens: Int,
    @StringRes val pro: Int,
) {
    constructor(@StringRes single: Int) : this(single, single, single)

    @StringRes
    fun resFor(ageGroup: AgeGroup): Int = when (ageGroup) {
        AgeGroup.KIDS -> kids
        AgeGroup.TEENS -> teens
        AgeGroup.PRO -> pro
    }
}

/** One step of Terra-guided dialogue inside a lesson. */
data class LessonStep(
    val text: AgeAdaptiveText,
    val expression: TerraExpression = TerraExpression.HAPPY,
    /** Optional short code snippet rendered under the dialogue bubble. */
    val codeSnippet: String? = null,
)

/** Declarative validation of a code challenge, kept serializable-friendly. */
sealed class ChallengeCheck {
    /** Console output (Python) must contain [needle] (case-insensitive optional). */
    data class OutputContains(val needle: String, val ignoreCase: Boolean = true) : ChallengeCheck()

    /** HTML source must contain tag [tag] (e.g. "h1") with optional [content]. */
    data class HtmlHasTag(val tag: String, val content: String? = null) : ChallengeCheck()

    /** Raw code must contain [needle]. */
    data class CodeContains(val needle: String, val ignoreCase: Boolean = true) : ChallengeCheck()

    /** Python program must run without errors. */
    object RunsCleanly : ChallengeCheck()
}

data class CodeChallenge(
    val language: CodeLanguage,
    val starterCode: String,
    val instruction: AgeAdaptiveText,
    val hint: AgeAdaptiveText,
    val checks: List<ChallengeCheck>,
    /** Shown floating in the ecosystem view on success, e.g. "Sprout". */
    val successLabel: String? = null,
)

/** A drag-and-drop ordering puzzle. */
data class BlockPuzzle(
    val prompt: AgeAdaptiveText,
    val language: CodeLanguage,
    /** Lines in the correct order. */
    val solution: List<String>,
    /** Extra wrong blocks mixed in (advanced puzzles / debugging). */
    val distractors: List<String> = emptyList(),
)

data class Lesson(
    val id: String,
    val biome: Biome,
    val order: Int,
    val type: LessonType,
    val language: CodeLanguage?,
    @StringRes val titleRes: Int,
    @StringRes val descriptionRes: Int,
    val xpReward: Int,
    val sunReward: Int,
    val waterReward: Int,
    val masteryReward: Int = 1,
    val badgeId: String? = null,
    val steps: List<LessonStep> = emptyList(),
    val challenge: CodeChallenge? = null,
    val puzzle: BlockPuzzle? = null,
    /** When true the lesson only appears for TEENS/PRO (or kids who unlocked pro tools). */
    val advanced: Boolean = false,
)

data class BadgeDef(
    val id: String,
    @StringRes val nameRes: Int,
    @StringRes val descriptionRes: Int,
    /** Emoji glyph keeps badges colorful without bundling artwork; trivially localizable. */
    val glyph: String,
    val professional: Boolean = false,
)

/** Lesson progress status used by the biome map. */
enum class LessonStatus { LOCKED, UNLOCKED, COMPLETED }

/** Result of running code in the playground. */
data class RunResult(
    val success: Boolean,
    val output: String,
    val errorLine: Int? = null,
    val friendlyError: String? = null,
    val technicalError: String? = null,
)
