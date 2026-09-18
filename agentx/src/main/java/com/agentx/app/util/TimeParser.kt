package com.agentx.app.util

import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

object TimeParser {
    private val isoFormats = listOf("yyyy-MM-dd HH:mm", "yyyy-MM-dd'T'HH:mm", "yyyy-MM-dd HH:mm:ss")

    fun parse(input: String, now: Long = System.currentTimeMillis()): Long? {
        val text = input.trim()
        if (text.isEmpty()) return null
        parseIso(text)?.let { return it }
        parseRelative(text, now)?.let { return it }
        parseTodayTomorrow(text, now)?.let { return it }
        parseClockTime(text, now)?.let { return it }
        return null
    }

    private fun parseIso(text: String): Long? {
        for (pattern in isoFormats) {
            val parsed = runCatching {
                SimpleDateFormat(pattern, Locale.US).apply { isLenient = false }.parse(text)?.time
            }.getOrNull()
            if (parsed != null) return parsed
        }
        return null
    }

    private fun parseRelative(text: String, now: Long): Long? {
        val lower = text.lowercase()
        if (!lower.startsWith("in ")) return null
        val rest = lower.removePrefix("in ").trim().split(' ').filter { it.isNotEmpty() }
        if (rest.size < 2) return null
        val amount = rest[0].toIntOrNull() ?: return null
        if (amount <= 0 || amount > 100000) return null
        val unit = rest[1]
        val millis = when {
            unit.startsWith("minute") || unit == "min" || unit == "mins" -> amount * 60_000L
            unit.startsWith("hour") || unit == "hr" || unit == "hrs" -> amount * 3_600_000L
            unit.startsWith("day") -> amount * 86_400_000L
            unit.startsWith("second") || unit == "sec" || unit == "secs" -> amount * 1_000L
            else -> return null
        }
        return now + millis
    }

    private fun parseTodayTomorrow(text: String, now: Long): Long? {
        val lower = text.lowercase()
        val dayOffset = when {
            lower.startsWith("tomorrow") -> 1
            lower.startsWith("today") -> 0
            else -> return null
        }
        var remainder = lower.removePrefix(if (dayOffset == 1) "tomorrow" else "today").trim()
        if (remainder.startsWith("at ")) remainder = remainder.removePrefix("at ").trim()
        if (remainder.startsWith("morning")) remainder = "8am"
        if (remainder.startsWith("afternoon")) remainder = "2pm"
        if (remainder.startsWith("evening")) remainder = "7pm"
        if (remainder.startsWith("night") || remainder.startsWith("tonight")) remainder = "9pm"
        if (remainder.startsWith("noon") || remainder.startsWith("midday")) remainder = "12pm"
        val (hour, minute) = parseClockToken(remainder) ?: return null
        val cal = Calendar.getInstance()
        cal.timeInMillis = now
        cal.add(Calendar.DAY_OF_YEAR, dayOffset)
        cal.set(Calendar.HOUR_OF_DAY, hour)
        cal.set(Calendar.MINUTE, minute)
        cal.set(Calendar.SECOND, 0)
        cal.set(Calendar.MILLISECOND, 0)
        return cal.timeInMillis
    }

    private fun parseClockTime(text: String, now: Long): Long? {
        val (hour, minute) = parseClockToken(text.lowercase()) ?: return null
        val cal = Calendar.getInstance()
        cal.timeInMillis = now
        cal.set(Calendar.HOUR_OF_DAY, hour)
        cal.set(Calendar.MINUTE, minute)
        cal.set(Calendar.SECOND, 0)
        cal.set(Calendar.MILLISECOND, 0)
        if (cal.timeInMillis <= now) cal.add(Calendar.DAY_OF_YEAR, 1)
        return cal.timeInMillis
    }

    private fun parseClockToken(token: String): Pair<Int, Int>? {
        val t = token.trim()
        if (t.isEmpty()) return null
        var ampm = 0
        var core = t
        if (core.endsWith("am") || core.endsWith("a.m.")) {
            ampm = 1
            core = core.removeSuffix("am").removeSuffix("a.m.").trim()
        } else if (core.endsWith("pm") || core.endsWith("p.m.")) {
            ampm = 2
            core = core.removeSuffix("pm").removeSuffix("p.m.").trim()
        }
        val parts = core.split(':')
        val hourRaw = parts.getOrNull(0)?.trim()?.toIntOrNull() ?: return null
        val minute = parts.getOrNull(1)?.trim()?.take(2)?.toIntOrNull() ?: 0
        if (minute !in 0..59) return null
        val hour = when (ampm) {
            1 -> if (hourRaw == 12) 0 else hourRaw
            2 -> if (hourRaw == 12) 12 else hourRaw + 12
            else -> hourRaw
        }
        if (hour !in 0..23) return null
        return hour to minute
    }

    fun format(ts: Long): String =
        SimpleDateFormat("MMM d, HH:mm", Locale.US).format(java.util.Date(ts))
}
