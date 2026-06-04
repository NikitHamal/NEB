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
    val normalized = subject.trim().lowercase()
    return when {
        "physics" in normalized -> 0xFF1E88E5
        "chem" in normalized -> 0xFF2E7D32
        "math" in normalized -> 0xFFE65100
        "bio" in normalized -> 0xFF7B1FA2
        "english" in normalized -> 0xFFC62828
        "nepali" in normalized -> 0xFF0277BD
        "computer" in normalized || "programming" in normalized || "python" in normalized -> 0xFF00838F
        "econom" in normalized -> 0xFFF9A825
        "account" in normalized -> 0xFF00796B
        "exam" in normalized || "tip" in normalized -> 0xFFC2185B
        else -> 0xFF5F6368
    }
}
