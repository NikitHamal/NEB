package com.neb.ians.util

import java.util.concurrent.TimeUnit

fun formatTimeAgo(timestamp: Long): String {
    val now = System.currentTimeMillis()
    val diff = now - timestamp

    return when {
        diff < TimeUnit.MINUTES.toMillis(1) -> "Just now"
        diff < TimeUnit.HOURS.toMillis(1) -> "${TimeUnit.MILLISECONDS.toMinutes(diff)}m ago"
        diff < TimeUnit.DAYS.toMillis(1) -> "${TimeUnit.MILLISECONDS.toHours(diff)}h ago"
        diff < TimeUnit.DAYS.toMillis(7) -> "${TimeUnit.MILLISECONDS.toDays(diff)}d ago"
        diff < TimeUnit.DAYS.toMillis(30) -> "${TimeUnit.MILLISECONDS.toDays(diff) / 7}w ago"
        else -> "${TimeUnit.MILLISECONDS.toDays(diff) / 30}mo ago"
    }
}

fun getSubjectColor(subject: String): Long {
    return when (subject) {
        "Physics" -> 0xFF1A73E8
        "Chemistry" -> 0xFF188038
        "Mathematics" -> 0xFFE8710A
        "Biology" -> 0xFF9334E6
        "English" -> 0xFFD93025
        "Nepali" -> 0xFF1967D2
        "Computer Science" -> 0xFF185ABC
        "Economics" -> 0xFFE37400
        "Accountancy" -> 0xFF0D652D
        "General" -> 0xFF5F6368
        "Exam Tips" -> 0xFFC5221F
        else -> 0xFF5F6368
    }
}
