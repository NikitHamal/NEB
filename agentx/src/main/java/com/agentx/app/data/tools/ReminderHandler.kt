package com.agentx.app.data.tools

import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.local.dao.ReminderDao
import com.agentx.app.data.local.entity.ReminderEntity
import com.agentx.app.util.TimeParser
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ReminderHandler @Inject constructor(
    private val dao: ReminderDao,
    private val scheduler: AxScheduler
) {
    suspend fun create(spec: ToolCallSpec): ToolExecution {
        val title = spec.arg("title") ?: return ToolExecution.fail("What should I remind you about?")
        val rawWhen = spec.arg("trigger_at")
            ?: return ToolExecution.fail("When? Give a time like 2026-09-19 07:30, tomorrow 7am, or in 20 minutes.")
        val at = TimeParser.parse(rawWhen)
            ?: return ToolExecution(
                ok = false,
                message = "I could not understand that time. Try 2026-09-19 07:30, tomorrow 7am, or in 20 minutes.",
                repairable = true,
                repairHint = "trigger_at must be a future time as YYYY-MM-DD HH:MM in 24-hour time. Try the call again with a valid trigger_at."
            )
        if (at <= System.currentTimeMillis() + 30_000L) {
            return ToolExecution(
                ok = false,
                message = "That time already passed. Pick a future time.",
                repairable = true,
                repairHint = "trigger_at was in the past. Try the call again with a future YYYY-MM-DD HH:MM time."
            )
        }
        val note = spec.arg("note").orEmpty()
        val id = dao.upsert(ReminderEntity(title = title, note = note, triggerAt = at))
        val entity = ReminderEntity(id = id, title = title, note = note, triggerAt = at, requestCode = id.toInt())
        dao.update(entity)
        val exact = scheduler.scheduleReminder(entity)
        val whenText = TimeParser.format(at)
        val suffix = if (exact) "" else " (approximate timing - exact alarms are off)"
        return ToolExecution.done("Reminder saved for " + whenText + suffix)
    }

    suspend fun list(): ToolExecution {
        val now = System.currentTimeMillis()
        val upcoming = dao.pendingAfter(now).take(10)
        if (upcoming.isEmpty()) return ToolExecution.done("No upcoming reminders")
        val lines = StringBuilder()
        for (reminder in upcoming) {
            lines.appendLine(reminder.id.toString() + ". " + reminder.title + " - " + TimeParser.format(reminder.triggerAt))
        }
        return ToolExecution.done(lines.toString().trim())
    }

    suspend fun cancel(spec: ToolCallSpec): ToolExecution {
        val id = spec.argLong("id") ?: return ToolExecution.fail("Which reminder id? List them first.")
        val entity = dao.getById(id) ?: return ToolExecution.fail("No reminder with id " + id)
        scheduler.cancelReminder(entity)
        dao.delete(id)
        return ToolExecution.done("Reminder deleted: " + entity.title)
    }
}
