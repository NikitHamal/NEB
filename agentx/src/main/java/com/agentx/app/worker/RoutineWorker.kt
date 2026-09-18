package com.agentx.app.worker

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.Data
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.tools.AxScheduler
import com.agentx.app.data.tools.RoutineRunner
import com.agentx.app.util.AxNotifications
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class RoutineWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val runner: RoutineRunner,
    private val routineDao: RoutineDao,
    private val scheduler: AxScheduler,
    private val notifications: AxNotifications
) : CoroutineWorker(context, params) {

    companion object {
        private const val KEY_ROUTINE_ID = "routine_id"

        fun enqueue(context: Context, routineId: Long) {
            val request = OneTimeWorkRequestBuilder<RoutineWorker>()
                .setInputData(Data.Builder().putLong(KEY_ROUTINE_ID, routineId).build())
                .build()
            WorkManager.getInstance(context).enqueue(request)
        }
    }

    override suspend fun doWork(): Result {
        val id = inputData.getLong(KEY_ROUTINE_ID, -1L)
        if (id <= 0) return Result.failure()
        val routine = routineDao.getById(id) ?: return Result.failure()
        val outcomes = runner.runNow(id, background = true)
        val done = outcomes.count { it.ok }
        val summary = done.toString() + "/" + outcomes.size + " steps done" +
            if (done < outcomes.size) {
                ": " + outcomes.filter { !it.ok }.take(2).joinToString("; ") { it.tool + " " + it.message }
            } else ""
        notifications.showRoutineFinished(routine.name, summary, done == outcomes.size)
        runCatching { scheduler.scheduleRoutine(routineDao.getById(id) ?: routine) }
        return Result.success()
    }
}
