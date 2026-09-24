package com.neb.ians.ui.screens.profile

import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.data.api.UserProfileResponse
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

// ---------------------------------------------------------------------------
// The pure text of the profile: what to call someone, what to call their
// province, and how to say when they arrived. No composables here, so the
// screen files stay about layout.
// ---------------------------------------------------------------------------

internal fun buildBadgeInfo(p: UserProfileResponse): ApiBadgeInfo? = when {
    p.isBot -> ApiBadgeInfo(type = "bot", label = "AI", color = "#7C4DFF")
    p.isAdmin -> ApiBadgeInfo(type = "admin", label = "Admin", color = "#F59E0B")
    p.moderatorLevel > 0 -> when (p.moderatorLevel) {
        1 -> ApiBadgeInfo(type = "moderator", label = "Community Mod", color = "#1B9AF0")
        2 -> ApiBadgeInfo(type = "moderator", label = "Senior Mod", color = "#00897B")
        else -> ApiBadgeInfo(type = "moderator", label = "Community Lead", color = "#7B1FA2")
    }
    p.role == "teacher" -> ApiBadgeInfo(
        type = "teacher",
        label = if (p.verificationLevel > 0) "Verified Teacher" else "Teacher",
        color = "#10B981"
    )
    p.role == "institution" -> ApiBadgeInfo(type = "institution", label = "Institution", color = "#6366F1")
    p.role == "explorer" -> ApiBadgeInfo(type = "explorer", label = "Explorer", color = "#F59E0B")
    p.verificationLevel > 0 -> when (p.verificationLevel) {
        1 -> ApiBadgeInfo(type = "verified", label = "Verified", color = "#1B9AF0")
        2 -> ApiBadgeInfo(type = "verified", label = "Expert Verified", color = "#2E7D32")
        3 -> ApiBadgeInfo(type = "verified", label = "Premium Verified", color = "#F59E0B")
        else -> ApiBadgeInfo(type = "verified", label = "Elite Verified", color = "#1a1a1a")
    }
    else -> null
}

data class AchievementPill(val key: String, val label: String)

fun parseAchievements(raw: String?): List<AchievementPill> {
    if (raw.isNullOrBlank()) return emptyList()
    return raw.split(",")
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .mapNotNull { key ->
            when (key) {
                "top_contributor" -> AchievementPill(key, "Top Contributor")
                "helpful" -> AchievementPill(key, "Helpful")
                "scholar" -> AchievementPill(key, "Scholar")
                "streak" -> AchievementPill(key, "Streak")
                "first_post" -> AchievementPill(key, "First Post")
                "100_likes" -> AchievementPill(key, "100 Likes")
                "bookworm" -> AchievementPill(key, "Bookworm")
                "problem_solver" -> AchievementPill(key, "Problem Solver")
                else -> null
            }
        }
}

fun plainTextPreview(content: String): String {
    return content
        .replace(Regex("!\\[[^\\]]*\\]\\([^)]*\\)"), "")
        .replace(Regex("\\[([^\\]]*)\\]\\([^)]*\\)"), "$1")
        .replace(Regex("[*_`#>~]"), "")
        .replace(Regex("\\s+"), " ")
        .trim()
}

fun formatJoined(createdAtMs: Long): String {
    if (createdAtMs <= 0) return ""
    return try {
        "Joined " + SimpleDateFormat("MMM yyyy", Locale.US).format(Date(createdAtMs))
    } catch (_: Exception) {
        ""
    }
}

/** Province names as people say them, not as the form stores them. */
internal fun shortProvince(raw: String): String = when (raw) {
    "Province 1", "Koshi Province" -> "Koshi"
    "Madhesh Province", "Province 2" -> "Madhesh"
    "Bagmati Province", "Province 3" -> "Bagmati"
    "Gandaki Province", "Province 4" -> "Gandaki"
    "Lumbini Province", "Province 5" -> "Lumbini"
    "Karnali Province", "Province 6" -> "Karnali"
    "Sudurpashchim Province", "Province 7", "Sudurpaschim Province", "Sudurpashchim" -> "Sudurpashchim"
    else -> raw
}

internal fun profileLocation(profile: UserProfileResponse): String {
    val parts = mutableListOf<String>()
    profile.district?.takeIf { it.isNotBlank() }?.let { parts.add(it) }
    profile.pradesh?.takeIf { it.isNotBlank() }?.let { parts.add(shortProvince(it)) }
    return parts.joinToString(", ")
}

internal fun classLabel(raw: String?): String = when (raw) {
    "11" -> "Class 11"
    "12" -> "Class 12"
    "Teacher" -> "Teacher / Educator"
    else -> raw.orEmpty()
}

internal fun subjectList(raw: String?): String =
    raw?.split(",")?.map { it.trim() }?.filter { it.isNotBlank() }?.joinToString(", ").orEmpty()

fun formatRoleHeadline(profile: UserProfileResponse): String {
    if (profile.isBot) return "AI Study Companion"
    return when (profile.role) {
        "teacher" -> {
            val parts = mutableListOf("Teacher")
            subjectList(profile.teachingSubjects).takeIf { it.isNotBlank() }?.let { parts.add(it) }
            profile.school?.takeIf { it.isNotBlank() }?.let { parts.add(it) }
            parts.joinToString(" · ")
        }
        "institution" -> {
            val type = when (profile.institutionType) {
                "school" -> "School"
                "college" -> "College"
                "academy" -> "Academy"
                else -> "Institution"
            }
            val parts = mutableListOf(type)
            profile.school?.takeIf { it.isNotBlank() }?.let { parts.add(it) }
            parts.joinToString(" · ")
        }
        "explorer" -> profile.school?.takeIf { it.isNotBlank() }
            ?: profile.classLevel?.takeIf { it.isNotBlank() }
            ?: "Explorer"
        else -> {
            val parts = mutableListOf<String>()
            classLabel(profile.classLevel).takeIf { it.isNotBlank() }?.let { parts.add(it) }
            subjectList(profile.subjects).takeIf { it.isNotBlank() }?.let { parts.add(it) }
            if (parts.isEmpty()) "NEBians Member" else parts.joinToString(" · ")
        }
    }
}

/** The fallback "about" line for a profile that never wrote a bio. */
internal fun fallbackBio(profile: UserProfileResponse): String = when {
    !profile.bio.isNullOrBlank() -> profile.bio
    profile.isBot -> "Your friendly AI study buddy. Always learning, always here to help."
    profile.role == "institution" -> "${profile.displayName ?: "An institution"} on NEBians."
    else -> buildString {
        append(profile.displayName?.takeIf { it.isNotBlank() } ?: "A NEBians member")
        profile.school?.takeIf { it.isNotBlank() }?.let { append(" at $it") }
        subjectList(profile.subjects).takeIf { it.isNotBlank() }?.let { append(". Focusing on $it") }
        append(".")
    }
}

internal fun joinedLine(profile: UserProfileResponse): String {
    val dateStr = formatJoined(profile.createdAt)
    if (dateStr.isBlank()) return ""
    return if (profile.isBot) "Online since " + dateStr.removePrefix("Joined ") else dateStr
}
