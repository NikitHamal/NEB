package com.agentx.app.worker

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.agentx.app.data.local.dao.ReminderDao
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.tools.AxScheduler
import com.agentx.app.util.AxNotifications
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

@AndroidEntryPoint
class AxAlarmReceiver : BroadcastReceiver() {
    @Inject lateinit var reminderDao: ReminderDao
    @Inject lateinit var routineDao: RoutineDao
    @Inject lateinit var notifications: AxNotifications

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onReceive(context: Context, intent: Intent) {
        val pending = goAsync()
        scope.launch {
            try {
                when (intent.action) {
                    AxScheduler.ACTION_REMINDER -> {
                        val id = intent.getLongExtra(AxScheduler.EXTRA_REMINDER_ID, -1L)
                        if (id > 0) {
                            val reminder = reminderDao.getById(id)
                            if (reminder != null && !reminder.fired) {
                                reminderDao.markFired(id)
                                notifications.showReminder(id, reminder.title, reminder.note)
                            }
                        }
                    }
                    AxScheduler.ACTION_ROUTINE -> {
                        val id = intent.getLongExtra(AxScheduler.EXTRA_ROUTINE_ID, -1L)
                        if (id > 0 && routineDao.getById(id) != null) {
                            RoutineWorker.enqueue(context, id)
                        }
                    }
                }
            } finally {
                pending.finish()
            }
        }
    }
}
