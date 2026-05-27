package com.neb.ians.notifications

import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat
import androidx.core.content.getSystemService
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.neb.ians.MainActivity
import com.neb.ians.R

/**
 * Receives Firebase Cloud Messaging payloads and surfaces them as system notifications.
 * Wired via the manifest; no Google services config file is bundled, so this is a stub
 * that becomes active when google-services.json is added at build time.
 */
class NebFcmService : FirebaseMessagingService() {
    override fun onMessageReceived(message: RemoteMessage) {
        val title = message.notification?.title ?: message.data["title"] ?: "NEBians"
        val body = message.notification?.body ?: message.data["body"] ?: return
        showNotification(this, title, body)
    }

    override fun onNewToken(token: String) {
        // Token registration would happen here. Left intentionally simple.
    }

    private fun showNotification(ctx: Context, title: String, body: String) {
        val pending = PendingIntent.getActivity(
            ctx, 0,
            Intent(ctx, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )
        val n = NotificationCompat.Builder(ctx, ctx.getString(R.string.default_notification_channel_id))
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setAutoCancel(true)
            .setContentIntent(pending)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
        ctx.getSystemService<NotificationManager>()?.notify(System.currentTimeMillis().toInt(), n)
    }
}
