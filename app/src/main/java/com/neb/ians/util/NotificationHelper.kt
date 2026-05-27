package com.neb.ians.util

import android.content.Context
import androidx.work.*
import com.neb.ians.worker.DataSeederWorker
import com.neb.ians.worker.NotificationWorker
import java.util.concurrent.TimeUnit

object NotificationHelper {
    fun schedulePeriodicNotificationCheck(context: Context) {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()

        val request = PeriodicWorkRequestBuilder<NotificationWorker>(
            6, TimeUnit.HOURS
        ).setConstraints(constraints)
            .setInputData(
                workDataOf(
                    "title" to "NEBians",
                    "message" to "New study resources available! Check them out.",
                    "channel_id" to "announcements"
                )
            )
            .build()

        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            "notification_check",
            ExistingPeriodicWorkPolicy.KEEP,
            request
        )
    }

    fun seedInitialData(context: Context) {
        val request = OneTimeWorkRequestBuilder<DataSeederWorker>()
            .build()

        WorkManager.getInstance(context).enqueueUniqueWork(
            "seed_data",
            ExistingWorkPolicy.KEEP,
            request
        )
    }

    fun sendImmediateNotification(
        context: Context,
        title: String,
        message: String,
        channelId: String = "announcements"
    ) {
        val request = OneTimeWorkRequestBuilder<NotificationWorker>()
            .setInputData(
                workDataOf(
                    "title" to title,
                    "message" to message,
                    "channel_id" to channelId
                )
            )
            .build()

        WorkManager.getInstance(context).enqueue(request)
    }
}
