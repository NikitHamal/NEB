package com.neb.ians.worker

import android.Manifest
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.neb.ians.MainActivity
import com.neb.ians.R
import com.neb.ians.util.NotificationDeepLink
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class NotificationWorker @AssistedInject constructor(
    @Assisted private val context: Context,
    @Assisted workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val title = inputData.getString("title") ?: "NEBians"
        val message = inputData.getString("message") ?: "New activity on your account"
        val channelId = inputData.getString("channel_id") ?: "announcements"

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                return Result.success()
            }
        }

        val hasDeepLink = inputData.getBoolean("has_deep_link", false)
        val deepLink = if (hasDeepLink) {
            val data = mapOf(
                "notification_id" to (inputData.getString("notification_id") ?: ""),
                "verb" to (inputData.getString("verb") ?: ""),
                "target_type" to (inputData.getString("target_type") ?: ""),
                "target_id" to (inputData.getString("target_id") ?: ""),
                "reference_type" to (inputData.getString("reference_type") ?: ""),
                "reference_id" to (inputData.getString("reference_id") ?: ""),
                "actor_username" to (inputData.getString("actor_username") ?: "")
            )
            NotificationDeepLink.fromFcmData(data)
        } else null

        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            if (deepLink != null) {
                putExtras(deepLink.toIntentExtras())
            }
        }

        val notificationId = (System.currentTimeMillis() and 0xFFFFFF).toInt()
        val pendingIntentFlags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        } else {
            PendingIntent.FLAG_UPDATE_CURRENT
        }
        val pendingIntent = PendingIntent.getActivity(
            context, notificationId, intent, pendingIntentFlags
        )

        val notification = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(message)
            .setStyle(NotificationCompat.BigTextStyle().bigText(message))
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(notificationId, notification)

        return Result.success()
    }
}
