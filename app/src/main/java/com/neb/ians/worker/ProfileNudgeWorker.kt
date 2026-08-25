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
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.util.NotificationDeepLink
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

/**
 * Daily periodic worker that reminds users who skipped onboarding to finish
 * their profile. Throttled to one notification per [AuthRepository.NUDGE_INTERVAL_MS]
 * so the cadence lives in a single place.
 */
@HiltWorker
class ProfileNudgeWorker @AssistedInject constructor(
    @Assisted private val context: Context,
    @Assisted workerParams: WorkerParameters,
    private val authRepository: AuthRepository
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        if (!authRepository.nudgeDue()) return Result.success()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                return Result.success()
            }
        }

        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            putExtra(NotificationDeepLink.EXTRA_IS_NOTIFICATION, true)
            putExtra(NotificationDeepLink.EXTRA_VERB, "profile_nudge")
        }
        val notificationId = (System.currentTimeMillis() and 0xFFFFFF).toInt()
        val pendingIntentFlags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        val pendingIntent = PendingIntent.getActivity(
            context, notificationId, intent, pendingIntentFlags
        )

        val notification = NotificationCompat.Builder(context, "announcements")
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("Customize your profile")
            .setContentText("Add your name, class and interests so the community knows you.")
            .setStyle(
                NotificationCompat.BigTextStyle()
                    .bigText("Add your name, class and interests so others can find you and share the right materials.")
            )
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(notificationId, notification)
        authRepository.markNudged()

        return Result.success()
    }
}
