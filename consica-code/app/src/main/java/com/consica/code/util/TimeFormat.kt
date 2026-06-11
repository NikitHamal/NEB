package com.consica.code.util

import java.text.DateFormat
import java.util.Date

object TimeFormat {
    /** Locale-aware short date/time for "edited at" labels. */
    fun relative(epochMillis: Long): String {
        val now = System.currentTimeMillis()
        val diff = now - epochMillis
        return when {
            diff < 60_000 -> "now"
            diff < 3_600_000 -> "${diff / 60_000}m"
            diff < 86_400_000 -> "${diff / 3_600_000}h"
            diff < 7 * 86_400_000L -> "${diff / 86_400_000}d"
            else -> DateFormat.getDateInstance(DateFormat.SHORT).format(Date(epochMillis))
        }
    }
}
