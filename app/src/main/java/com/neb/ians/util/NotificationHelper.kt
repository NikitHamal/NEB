package com.neb.ians.util

import android.content.Context
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import com.neb.ians.worker.NotificationWorker

object NotificationHelper {

    fun sendImmediateNotification(
        context: Context,
        title: String,
        message: String,
        channelId: String = "announcements",
        deepLink: NotificationDeepLink? = null
    ) {
        val data = mutableListOf<Pair<String, Any>>(
            "title" to title,
            "message" to message,
            "channel_id" to channelId
        )
        if (deepLink != null) {
            data.add("notification_id" to (deepLink.notificationId ?: ""))
            data.add("verb" to deepLink.verb)
            data.add("target_type" to deepLink.targetType)
            data.add("target_id" to deepLink.targetId)
            data.add("reference_type" to deepLink.referenceType)
            data.add("reference_id" to deepLink.referenceId)
            data.add("actor_username" to (deepLink.actorUsername ?: ""))
            data.add("has_deep_link" to true)
        }

        val request = OneTimeWorkRequestBuilder<NotificationWorker>()
            .setInputData(workDataOf(*data.toTypedArray()))
            .build()

        WorkManager.getInstance(context).enqueue(request)
    }
}
