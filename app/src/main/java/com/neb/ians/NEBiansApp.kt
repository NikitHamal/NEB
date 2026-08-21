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
import coil.ImageLoader
import coil.ImageLoaderFactory
import okhttp3.OkHttpClient
import com.neb.ians.data.api.WafChallengeInterceptor

@HiltAndroidApp
class NEBiansApp : Application(), Configuration.Provider, ImageLoaderFactory {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()

    override fun newImageLoader(): ImageLoader {
        return ImageLoader.Builder(this)
            .components {
                add(com.neb.ians.ui.avatar.AvatarMapper())
                add(com.neb.ians.ui.avatar.AvatarFetcher.Factory())
            }
            .okHttpClient {
                OkHttpClient.Builder()
                    .addInterceptor(WafChallengeInterceptor(this))
                    .addInterceptor { chain ->
                        val request = chain.request().newBuilder()
                            .header("User-Agent", "Mozilla/5.0 (Linux; Android 11; Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36")
                            .header("Accept", "image/webp,image/apng,image/*,*/*;q=0.8")
                            .header("Accept-Language", "en-US,en;q=0.9")
                            .header("Connection", "keep-alive")
                            .build()
                        chain.proceed(request)
                    }
                    .build()
            }
            .crossfade(true)
            .build()
    }

    override fun onCreate() {
        super.onCreate()
        com.neb.ians.util.CrashHandler.init(this)
        createNotificationChannels()
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
