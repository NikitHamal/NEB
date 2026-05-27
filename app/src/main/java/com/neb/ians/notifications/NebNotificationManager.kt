package com.neb.ians.notifications

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.neb.ians.R

object NebNotificationManager {
    private const val ANNOUNCEMENTS_CHANNEL = "neb_announcements"
    private const val COMMUNITY_CHANNEL = "neb_community"

    fun createChannels(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = context.getSystemService(NotificationManager::class.java)
        manager.createNotificationChannels(
            listOf(
                NotificationChannel(
                    ANNOUNCEMENTS_CHANNEL,
                    "Important announcements",
                    NotificationManager.IMPORTANCE_HIGH
                ).apply {
                    description = "NEB routine updates, new resources, and urgent study alerts"
                },
                NotificationChannel(
                    COMMUNITY_CHANNEL,
                    "Community activity",
                    NotificationManager.IMPORTANCE_DEFAULT
                ).apply {
                    description = "Forum answers and learning discussions"
                }
            )
        )
    }

    fun showAnnouncement(context: Context, title: String, body: String) {
        show(context, ANNOUNCEMENTS_CHANNEL, title, body, 1100)
    }

    fun showCommunity(context: Context, title: String, body: String) {
        show(context, COMMUNITY_CHANNEL, title, body, 1200)
    }

    private fun show(context: Context, channel: String, title: String, body: String, id: Int) {
        if (!canNotify(context)) return
        val notification = NotificationCompat.Builder(context, channel)
            .setSmallIcon(R.drawable.ic_nebians_foreground)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()
        NotificationManagerCompat.from(context).notify(id + title.hashCode().mod(899), notification)
    }

    fun canNotify(context: Context): Boolean {
        return Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU ||
            ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED
    }
}
