package com.consica.code.core.model

/**
 * Persisted onboarding / settings enums. Stored by stable [id] strings in DataStore so the
 * underlying ordinal order can change freely without corrupting saved data.
 */

enum class AgeGroup(val id: String) {
    KIDS("8_12"),        // 8–12: playful, highly guided
    TWEENS("13_16"),     // 13–16: capable, structured
    TEENS_PLUS("16_19"); // 16+: professional, powerful

    companion object {
        fun from(id: String?): AgeGroup = entries.firstOrNull { it.id == id } ?: KIDS
    }
}

enum class ThemeIntensity(val id: String) {
    PLAYFUL("playful"), BALANCED("balanced"), FOCUSED("focused");
    companion object { fun from(id: String?) = entries.firstOrNull { it.id == id } ?: BALANCED }
}

enum class GuidanceLevel(val id: String) {
    FULL("full"), SOME("some"), MINIMAL("minimal");
    companion object { fun from(id: String?) = entries.firstOrNull { it.id == id } ?: FULL }
}

enum class LearningGoal(val id: String) {
    BASICS("basics"), WEBSITES("websites"), GAMES("games"), PUZZLES("puzzles"), EXPLORE("explore");
    companion object { fun from(id: String?) = entries.firstOrNull { it.id == id } ?: BASICS }
}

enum class ExperienceLevel(val id: String) {
    NONE("none"), SOME("some"), LOTS("lots");
    companion object { fun from(id: String?) = entries.firstOrNull { it.id == id } ?: NONE }
}

enum class Interest(val id: String) {
    PYTHON("python"), WEB("web"), GAMES("games"), APPS("apps"), AI("ai"), CREATIVE("creative");
    companion object { fun from(id: String?) = entries.firstOrNull { it.id == id } }
}

/** Which editor experience to present. Younger users start in BEGINNER and unlock PRO. */
enum class EditorMode { BEGINNER, PRO }
