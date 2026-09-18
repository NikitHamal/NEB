package com.agentx.app.util

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object FormatUtils {
    fun formatBytes(bytes: Long): String {
        if (bytes < 1024) return "$bytes B"
        val kb = bytes / 1024.0
        if (kb < 1024) return "%.1f KB".format(kb)
        val mb = kb / 1024.0
        if (mb < 1024) return "%.1f MB".format(mb)
        return "%.2f GB".format(mb / 1024.0)
    }

    fun formatDateTime(ts: Long): String =
        SimpleDateFormat("MMM d, yyyy HH:mm", Locale.US).format(Date(ts))

    fun formatTimeAgo(ts: Long, now: Long = System.currentTimeMillis()): String {
        val diff = (now - ts).coerceAtLeast(0)
        val minutes = diff / 60_000
        if (minutes < 1) return "just now"
        if (minutes < 60) return "$minutes min ago"
        val hours = minutes / 60
        if (hours < 24) return "$hours hr ago"
        val days = hours / 24
        if (days < 30) return "$days d ago"
        return formatDateTime(ts)
    }
}
