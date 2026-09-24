package com.neb.ians.data.news

import androidx.compose.ui.graphics.Color

/** Lightweight announcement model parsed from the live web news page. */
data class NewsAnnouncement(
    val id: String = "",
    val slug: String = "",
    val title: String = "",
    val summary: String = "",
    val categoryKey: String = "general",
    val categoryLabel: String = "General",
    val categoryIcon: String = "info",
    val categoryColorHex: String = "#6b7280",
    val isPinned: Boolean = false,
    val coverImageUrl: String = "",
    val authorName: String = "NEBians Team",
    val authorPhotoUrl: String = "",
    val publishedAgo: String = "",
    val viewCount: String = ""
) {
    val url: String get() = "https://nebians.consica.com.np/news/$slug/"
}

data class NewsCategory(
    val key: String?,
    val label: String,
    val icon: String,
    val colorHex: String
)

val NewsCategories = listOf(
    NewsCategory(null, "All", "apps", "#004AC6"),
    NewsCategory("exam_results", "Exam Results", "fact_check", "#dc2626"),
    NewsCategory("notice", "Notice", "campaign", "#2563eb"),
    NewsCategory("event", "Event", "event", "#7c3aed"),
    NewsCategory("update", "Update", "upgrade", "#059669"),
    NewsCategory("alert", "Alert", "warning", "#d97706"),
    NewsCategory("general", "General", "info", "#6b7280")
)

fun String.toSafeColor(fallback: Color = Color(0xFF5C5C61)): Color {
    return try {
        val clean = trim().removePrefix("#")
        if (clean.length == 6) Color(android.graphics.Color.parseColor("#$clean")) else fallback
    } catch (_: Exception) {
        fallback
    }
}
