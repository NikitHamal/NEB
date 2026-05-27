package com.neb.ians

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import androidx.hilt.work.HiltWorkerFactory
import androidx.work.Configuration
import com.neb.ians.util.NotificationHelper
import dagger.hilt.android.HiltAndroidApp
import javax.inject.Inject

@HiltAndroidApp
class NEBiansApp : Application(), Configuration.Provider {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()

    override fun onCreate() {
        super.onCreate()
        createNotificationChannels()
        NotificationHelper.seedInitialData(this)
        NotificationHelper.schedulePeriodicNotificationCheck(this)
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channels = listOf(
                NotificationChannel(
                    "announcements",
                    "Announcements",
                    NotificationManager.IMPORTANCE_HIGH
                ).apply { description = "Important announcements and updates" },
                NotificationChannel(
                    "forum_activity",
                    "Forum Activity",
                    NotificationManager.IMPORTANCE_DEFAULT
                ).apply { description = "Replies and activity on your forum posts" },
                NotificationChannel(
                    "downloads",
                    "Downloads",
                    NotificationManager.IMPORTANCE_LOW
                ).apply { description = "Download progress notifications" }
            )
            val manager = getSystemService(NotificationManager::class.java)
            channels.forEach { manager.createNotificationChannel(it) }
        }
    }
}
