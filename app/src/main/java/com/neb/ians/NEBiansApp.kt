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
import coil.disk.DiskCache
import coil.memory.MemoryCache
import okhttp3.OkHttpClient
import com.neb.ians.data.api.WafChallengeInterceptor
import com.neb.ians.util.DevicePerformance
import com.neb.ians.data.repository.SecurePrefs
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@HiltAndroidApp
class NEBiansApp : Application(), Configuration.Provider, ImageLoaderFactory {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    @Inject
    lateinit var dataStore: DataStore<Preferences>

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()

    override fun newImageLoader(): ImageLoader {
        val isLowEnd = DevicePerformance.isLowEndDevice(this)
        return ImageLoader.Builder(this)
            .components {
                add(com.neb.ians.ui.avatar.AvatarMapper())
                add(com.neb.ians.ui.avatar.AvatarKeyer())
                add(com.neb.ians.ui.avatar.AvatarFetcher.Factory())
            }
            .memoryCache {
                MemoryCache.Builder(this)
                    .maxSizePercent(if (isLowEnd) 0.15 else 0.25)
                    .strongReferencesEnabled(true)
                    .build()
            }
            .diskCache {
                DiskCache.Builder()
                    .directory(cacheDir.resolve("image_cache"))
                    .maxSizeBytes(if (isLowEnd) 50L * 1024 * 1024 else 120L * 1024 * 1024)
                    .build()
            }
            .allowRgb565(isLowEnd)
            .allowHardware(!isLowEnd)
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
            .crossfade(150)
            .build()
    }

    override fun onCreate() {
        super.onCreate()
        com.neb.ians.util.CrashHandler.init(this)
        createNotificationChannels()
        warmUp()
    }

    /**
     * Starts, off the main thread, the two reads the first screen otherwise waits for on it: the
     * preferences file (AuthRepository reads it while MainActivity is injected) and the encrypted
     * token (Keystore and Tink setup, the slowest step of a cold start). A later reader finds
     * either one cached, or waits for the read already under way rather than starting its own.
     */
    private fun warmUp() {
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
        scope.launch { runCatching { dataStore.data.first() } }
        scope.launch { runCatching { SecurePrefs.getAuthToken(this@NEBiansApp) } }
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
