package com.neb.ians

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.neb.ians.data.db.AppDatabase
import com.neb.ians.utils.ThemeManager

class NEBiansApp : Application() {

    val database: AppDatabase by lazy { AppDatabase.getDatabase(this) }

    override fun onCreate() {
        super.onCreate()
        ThemeManager.init(this)
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(NotificationManager::class.java) ?: return
            val channels = listOf(
                NotificationChannel(
                    CHANNEL_ANNOUNCEMENTS,
                    getString(R.string.channel_announcements),
                    NotificationManager.IMPORTANCE_HIGH
                ),
                NotificationChannel(
                    CHANNEL_COMMUNITY,
                    getString(R.string.channel_community),
                    NotificationManager.IMPORTANCE_DEFAULT
                )
            )
            manager.createNotificationChannels(channels)
        }
    }

    companion object {
        const val CHANNEL_ANNOUNCEMENTS = "announcements"
        const val CHANNEL_COMMUNITY = "community"
    }
}
