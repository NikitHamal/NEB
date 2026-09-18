package com.agentx.app.data.tools

import android.content.Context
import android.content.Intent
import android.provider.AlarmClock
import com.agentx.app.data.engine.ToolCallSpec
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class TimeHandler @Inject constructor(
    @ApplicationContext private val context: Context
) {
    fun setAlarm(spec: ToolCallSpec): ToolExecution {
        val hour = spec.argInt("hour") ?: return ToolExecution.fail("What hour? Use 0-23.")
        val minute = spec.argInt("minute") ?: 0
        if (hour !in 0..23 || minute !in 0..59) {
            return ToolExecution(
                ok = false,
                message = "That time is out of range",
                repairable = true,
                repairHint = "hour must be 0-23 and minute 0-59 in 24-hour time (2:57 pm is hour 14, minute 57). Try the call again with valid numbers."
            )
        }
        val intent = Intent(AlarmClock.ACTION_SET_ALARM).apply {
            putExtra(AlarmClock.EXTRA_HOUR, hour)
            putExtra(AlarmClock.EXTRA_MINUTES, minute)
            spec.arg("label")?.let { putExtra(AlarmClock.EXTRA_MESSAGE, it) }
            val days = parseDays(spec.arg("days"))
            if (days.isNotEmpty()) putExtra(AlarmClock.EXTRA_DAYS, days)
            putExtra(AlarmClock.EXTRA_SKIP_UI, false)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }.onFailure {
            return ToolExecution.fail("No clock app found to set the alarm")
        }
        return ToolExecution.done("Alarm set for " + hour.toString().padStart(2, '0') + ":" + minute.toString().padStart(2, '0'))
    }

    fun setTimer(spec: ToolCallSpec): ToolExecution {
        val seconds = (spec.argInt("seconds") ?: return ToolExecution.fail("How long? Give seconds.")).coerceIn(1, 86_399)
        val intent = Intent(AlarmClock.ACTION_SET_TIMER).apply {
            putExtra(AlarmClock.EXTRA_LENGTH, seconds)
            spec.arg("label")?.let { putExtra(AlarmClock.EXTRA_MESSAGE, it) }
            putExtra(AlarmClock.EXTRA_SKIP_UI, false)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }.onFailure {
            return ToolExecution.fail("No clock app found to start the timer")
        }
        return ToolExecution.done("Timer started for " + describeDuration(seconds))
    }

    private fun parseDays(raw: String?): ArrayList<Int> {
        val out = ArrayList<Int>()
        if (raw.isNullOrBlank()) return out
        val map = mapOf(
            "mon" to java.util.Calendar.MONDAY, "tue" to java.util.Calendar.TUESDAY,
            "wed" to java.util.Calendar.WEDNESDAY, "thu" to java.util.Calendar.THURSDAY,
            "fri" to java.util.Calendar.FRIDAY, "sat" to java.util.Calendar.SATURDAY,
            "sun" to java.util.Calendar.SUNDAY
        )
        for (part in raw.lowercase().split(',', ' ')) {
            val key = part.trim().take(3)
            map[key]?.let { if (!out.contains(it)) out.add(it) }
        }
        return out
    }

    private fun describeDuration(seconds: Int): String {
        if (seconds < 60) return seconds.toString() + " seconds"
        if (seconds < 3600) {
            val m = seconds / 60
            val s = seconds % 60
            return if (s == 0) m.toString() + " minutes" else m.toString() + " min " + s + " sec"
        }
        val h = seconds / 3600
        val m = (seconds % 3600) / 60
        return if (m == 0) h.toString() + " hours" else h.toString() + " hr " + m + " min"
    }
}
