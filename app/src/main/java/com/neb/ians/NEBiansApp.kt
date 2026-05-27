package com.neb.ians

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.neb.ians.service.NotificationHelper

class NEBiansApp : Application() {
    override fun onCreate() {
        super.onCreate()
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
            val channels = listOf(
                NotificationChannel(
                    NotificationHelper.CHANNEL_ANNOUNCEMENTS,
                    "Announcements",
                    NotificationManager.IMPORTANCE_HIGH
                ),
                NotificationChannel(
                    NotificationHelper.CHANNEL_COMMUNITY,
                    "Community Activity",
                    NotificationManager.IMPORTANCE_DEFAULT
                )
            )
            manager.createNotificationChannels(channels)
        }
    }
}
