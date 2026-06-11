package com.consica.code.core.model

import androidx.compose.runtime.compositionLocalOf

/**
 * The single place that translates an [AgeGroup] (plus theme intensity) into concrete UI/behavior
 * knobs. Every screen reads [LocalAgeConfig] instead of branching on the age group directly, so
 * the adaptation rules live in one auditable spot and stay consistent across the app.
 */
data class AgeConfig(
    val ageGroup: AgeGroup,
    val intensity: ThemeIntensity,
    /** Larger interface density / bigger touch targets for younger users. */
    val spacious: Boolean,
    /** Show character-led guidance prominently. */
    val heavyMascot: Boolean,
    /** Default editor mode before any pro unlock. */
    val defaultEditorMode: EditorMode,
    /** Beginner editors hide line numbers & error panels by default. */
    val showLineNumbers: Boolean,
    val showErrorPanel: Boolean,
    val showRunHistory: Boolean,
    val allowMultiFile: Boolean,
    /** Use "Grow" instead of "Run", celebratory rewards, leaf confetti, etc. */
    val growLabel: Boolean,
    val celebratoryRewards: Boolean,
    /** Typewriter reveal for mascot dialogue (kids/tweens). */
    val typewriterDialogue: Boolean,
    /** Tone bucket used to pick mascot dialogue variants: "kid" | "teen" | "pro". */
    val toneBucket: String,
    /** Suggested challenge difficulty floor (1 easiest .. 3 hardest). */
    val difficultyFloor: Int,
) {
    val isKid get() = ageGroup == AgeGroup.KIDS
    val isPro get() = ageGroup == AgeGroup.TEENS_PLUS

    companion object {
        fun forUser(ageGroup: AgeGroup, intensity: ThemeIntensity): AgeConfig = when (ageGroup) {
            AgeGroup.KIDS -> AgeConfig(
                ageGroup = ageGroup, intensity = intensity,
                spacious = true, heavyMascot = intensity != ThemeIntensity.FOCUSED,
                defaultEditorMode = EditorMode.BEGINNER,
                showLineNumbers = false, showErrorPanel = false, showRunHistory = false,
                allowMultiFile = false, growLabel = true, celebratoryRewards = true,
                typewriterDialogue = intensity != ThemeIntensity.FOCUSED,
                toneBucket = "kid", difficultyFloor = 1,
            )
            AgeGroup.TWEENS -> AgeConfig(
                ageGroup = ageGroup, intensity = intensity,
                spacious = false, heavyMascot = intensity == ThemeIntensity.PLAYFUL,
                defaultEditorMode = EditorMode.BEGINNER,
                showLineNumbers = true, showErrorPanel = true, showRunHistory = true,
                allowMultiFile = false, growLabel = intensity == ThemeIntensity.PLAYFUL,
                celebratoryRewards = intensity != ThemeIntensity.FOCUSED,
                typewriterDialogue = false, toneBucket = "teen", difficultyFloor = 2,
            )
            AgeGroup.TEENS_PLUS -> AgeConfig(
                ageGroup = ageGroup, intensity = intensity,
                spacious = false, heavyMascot = false,
                defaultEditorMode = EditorMode.PRO,
                showLineNumbers = true, showErrorPanel = true, showRunHistory = true,
                allowMultiFile = true, growLabel = false,
                celebratoryRewards = intensity == ThemeIntensity.PLAYFUL,
                typewriterDialogue = false, toneBucket = "pro", difficultyFloor = 2,
            )
        }
    }
}

val LocalAgeConfig = compositionLocalOf {
    AgeConfig.forUser(AgeGroup.KIDS, ThemeIntensity.BALANCED)
}
