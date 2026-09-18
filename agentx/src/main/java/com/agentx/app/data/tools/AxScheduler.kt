package com.agentx.app.data.tools

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import com.agentx.app.data.local.dao.ReminderDao
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.local.entity.ReminderEntity
import com.agentx.app.data.local.entity.RoutineEntity
import com.agentx.app.worker.AxAlarmReceiver
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.qualifiers.ApplicationContext
import java.util.Calendar
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AxScheduler @Inject constructor(
    @ApplicationContext private val context: Context,
    private val reminderDao: ReminderDao,
    private val routineDao: RoutineDao
) {
    companion object {
        const val ACTION_REMINDER = "com.agentx.app.ACTION_REMINDER"
        const val ACTION_ROUTINE = "com.agentx.app.ACTION_ROUTINE"
        const val EXTRA_REMINDER_ID = "reminder_id"
        const val EXTRA_ROUTINE_ID = "routine_id"
    }

    private fun alarms(): AlarmManager =
        context.getSystemService(Context.ALARM_SERVICE) as AlarmManager

    private fun reminderIntent(requestCode: Int, reminderId: Long): PendingIntent {
        val intent = Intent(context, AxAlarmReceiver::class.java).apply {
            action = ACTION_REMINDER
            putExtra(EXTRA_REMINDER_ID, reminderId)
        }
        return PendingIntent.getBroadcast(
            context, requestCode, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }

    private fun routineIntent(routineId: Long): PendingIntent {
        val intent = Intent(context, AxAlarmReceiver::class.java).apply {
            action = ACTION_ROUTINE
            putExtra(EXTRA_ROUTINE_ID, routineId)
        }
        return PendingIntent.getBroadcast(
            context, 500_000 + (routineId % 100_000).toInt(), intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }

    fun scheduleReminder(entity: ReminderEntity): Boolean {
        val manager = alarms()
        val operation = reminderIntent(entity.requestCode, entity.id)
        return if (PermissionUtils.canScheduleExact(context)) {
            manager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, entity.triggerAt, operation)
            true
        } else {
            manager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, entity.triggerAt, operation)
            false
        }
    }

    fun cancelReminder(entity: ReminderEntity) {
        runCatching { alarms().cancel(reminderIntent(entity.requestCode, entity.id)) }
    }

    fun scheduleRoutine(routine: RoutineEntity): Boolean {
        if (routine.scheduleHour < 0) return false
        val next = nextDailyOccurrence(routine.scheduleHour, routine.scheduleMinute, routine.scheduleDays, System.currentTimeMillis())
            ?: return false
        val operation = routineIntent(routine.id)
        if (PermissionUtils.canScheduleExact(context)) {
            alarms().setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, next, operation)
        } else {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                alarms().setWindow(AlarmManager.RTC_WAKEUP, next, 15 * 60_000L, operation)
            } else {
                alarms().set(AlarmManager.RTC_WAKEUP, next, operation)
            }
        }
        return true
    }

    fun cancelRoutine(routineId: Long) {
        runCatching { alarms().cancel(routineIntent(routineId)) }
    }

    suspend fun rescheduleAll() {
        val now = System.currentTimeMillis()
        for (reminder in reminderDao.pendingAfter(now)) {
            runCatching { scheduleReminder(reminder) }
        }
        for (routine in routineDao.scheduled()) {
            runCatching { scheduleRoutine(routine) }
        }
    }

    fun nextDailyOccurrence(hour: Int, minute: Int, daysMask: Int, now: Long): Long? {
        if (hour !in 0..23 || minute !in 0..59) return null
        val cal = Calendar.getInstance()
        for (ahead in 0..8) {
            cal.timeInMillis = now
            cal.add(Calendar.DAY_OF_YEAR, ahead)
            val dow = cal.get(Calendar.DAY_OF_WEEK)
            val bit = when (dow) {
                Calendar.MONDAY -> 0
                Calendar.TUESDAY -> 1
                Calendar.WEDNESDAY -> 2
                Calendar.THURSDAY -> 3
                Calendar.FRIDAY -> 4
                Calendar.SATURDAY -> 5
                else -> 6
            }
            val wanted = if (daysMask == 0) true else (daysMask and (1 shl bit)) != 0
            if (!wanted) continue
            cal.set(Calendar.HOUR_OF_DAY, hour)
            cal.set(Calendar.MINUTE, minute)
            cal.set(Calendar.SECOND, 0)
            cal.set(Calendar.MILLISECOND, 0)
            if (cal.timeInMillis > now) return cal.timeInMillis
        }
        return null
    }
}
