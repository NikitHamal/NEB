package com.neb.ians

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.neb.ians.data.local.database.NEBiansDatabase

class NEBiansApp : Application() {

    lateinit var database: NEBiansDatabase
        private set

    override fun onCreate() {
        super.onCreate()
        instance = this
        database = NEBiansDatabase.getInstance(this)
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(NotificationManager::class.java)

            val announcementChannel = NotificationChannel(
                CHANNEL_ANNOUNCEMENTS,
                "Announcements",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Important announcements and updates"
            }

            val communityChannel = NotificationChannel(
                CHANNEL_COMMUNITY,
                "Community",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Forum replies and community activity"
            }

            manager.createNotificationChannel(announcementChannel)
            manager.createNotificationChannel(communityChannel)
        }
    }

    companion object {
        const val CHANNEL_ANNOUNCEMENTS = "announcements"
        const val CHANNEL_COMMUNITY = "community"

        lateinit var instance: NEBiansApp
            private set
    }
}
