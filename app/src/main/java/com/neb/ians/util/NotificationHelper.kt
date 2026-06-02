package com.neb.ians.util

import android.content.Context
import androidx.work.*
import com.neb.ians.worker.NotificationWorker

object NotificationHelper {

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
