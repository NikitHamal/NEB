package com.consica.code.domain.model

import androidx.annotation.StringRes

/** Languages/tracks supported by the playground and lessons. */
enum class TrackLanguage {
    PYTHON, HTML, LOGIC
}

enum class LessonType {
    TUTORIAL,   // Terra-led conversation only
    CODE,       // playground challenge
    PUZZLE,     // drag-and-drop block ordering
    PROJECT     // workspace-based, multi-step (older learners)
}

enum class LearningPath {
    BEGINNER_WEB, BEGINNER_PYTHON, INTERMEDIATE, ADVANCED
}

enum class BadgeCategory {
    SKILL, STREAK, MASTERY, PROJECT, SPECIAL
}

/** Terra the Owl's expressions used by the CharacterGuide system. */
enum class TerraExpression {
    HAPPY, EXCITED, THINKING, CONFUSED, PROUD, SLEEPY, FOCUSED, PROFESSIONAL, ENCOURAGING
}

/**
 * One step of Terra's dialogue. Text adapts to the learner's age group via
 * separate string resources, all of which are localizable.
 */
data class LessonStep(
    @StringRes val kidTextRes: Int,
    @StringRes val teenTextRes: Int = kidTextRes,
    @StringRes val adultTextRes: Int = teenTextRes,
    val expression: TerraExpression = TerraExpression.HAPPY,
    /** Optional code snippet rendered in a monospace card under the dialogue. */
    val codeSnippet: String? = null,
) {
    @StringRes
    fun textFor(ageGroup: AgeGroup): Int = when (ageGroup) {
        AgeGroup.KIDS -> kidTextRes
        AgeGroup.TEENS -> teenTextRes
        AgeGroup.ADULTS -> adultTextRes
    }
}

/** Validation rules evaluated against code and/or execution output. */
sealed interface ChallengeValidation {
    data class OutputContains(val needles: List<String>, val ignoreCase: Boolean = true) : ChallengeValidation
    data class CodeMatches(val pattern: String) : ChallengeValidation
    data class HtmlHasTag(val tag: String, val textContains: String? = null) : ChallengeValidation
    data class All(val rules: List<ChallengeValidation>) : ChallengeValidation
    data class AnyOf(val rules: List<ChallengeValidation>) : ChallengeValidation
}

data class CodeChallenge(
    val language: TrackLanguage,
    val starterCode: String,
    @StringRes val instructionRes: Int,
    @StringRes val hintRes: Int,
    val validation: ChallengeValidation,
    /** Sample stdin lines for Python challenges that use input(). */
    val stdin: List<String> = emptyList(),
)

/** A single draggable code block in a puzzle. */
data class PuzzleBlock(
    val code: String,
    val indent: Int = 0,
)

data class BlockPuzzle(
    @StringRes val promptRes: Int,
    @StringRes val hintRes: Int,
    val language: TrackLanguage,
    /** Blocks listed in the CORRECT order; the UI shuffles them deterministically. */
    val blocks: List<PuzzleBlock>,
    /** Wrong blocks mixed in for harder (older-learner) puzzles. */
    val distractors: List<PuzzleBlock> = emptyList(),
)

data class Lesson(
    val id: String,
    val biomeId: String,
    @StringRes val titleRes: Int,
    @StringRes val descriptionRes: Int,
    val type: LessonType,
    val language: TrackLanguage,
    val path: LearningPath,
    /** Global ordering inside its biome. */
    val order: Int,
    val xpReward: Int,
    val sunReward: Int = 0,
    val waterReward: Int = 0,
    val masteryReward: Int = 1,
    /** Badge granted on completion, if any. */
    val badgeId: String? = null,
    /** Ecosystem decoration unlocked on completion, if any. */
    val ecosystemItemId: String? = null,
    val steps: List<LessonStep> = emptyList(),
    val challenge: CodeChallenge? = null,
    val puzzle: BlockPuzzle? = null,
    /** Lessons restricted to capable learners unless professional mode is unlocked. */
    val advanced: Boolean = false,
)

data class Biome(
    val id: String,
    @StringRes val nameRes: Int,
    @StringRes val taglineRes: Int,
    /** Decorative glyph for the map node (purely visual, not localized). */
    val emoji: String,
    val order: Int,
    val path: LearningPath,
    /** Brand accent used for this biome's nodes. */
    val colorHex: Long,
)

data class BadgeDef(
    val id: String,
    @StringRes val nameRes: Int,
    @StringRes val descriptionRes: Int,
    val emoji: String,
    val category: BadgeCategory,
)

/** Decorative ecosystem element earned through learning. */
data class EcosystemItemDef(
    val id: String,
    @StringRes val nameRes: Int,
    val emoji: String,
)
