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
import coil.decode.SvgDecoder
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
            .components { add(SvgDecoder.Factory()) }
            .allowRgb565(isLowEnd)
            .allowHardware(!isLowEnd)
            .okHttpClient {
                OkHttpClient.Builder()
                    .connectionPool(com.neb.ians.data.api.ApiService.sharedPool)
                    .dispatcher(okhttp3.Dispatcher().apply { maxRequestsPerHost = 12 })
                    .apply {
                        if (!BuildConfig.DEBUG) {
                            proxy(java.net.Proxy.NO_PROXY)
                            connectionSpecs(listOf(okhttp3.ConnectionSpec.MODERN_TLS, okhttp3.ConnectionSpec.COMPATIBLE_TLS))
                        }
                    }
                    .addInterceptor(WafChallengeInterceptor(this))
                    .addNetworkInterceptor { chain ->
                        // M3X art files never change under one name: keep them on disk for a year, no revalidation
                        val response = chain.proceed(chain.request())
                        if (chain.request().url.encodedPath.contains("/img/m3x/")) {
                            response.newBuilder().header("Cache-Control", "public, max-age=31536000, immutable").removeHeader("Pragma").build()
                        } else response
                    }
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
     * Starts, off the main thread, the reads the first screen otherwise waits for on it: the
     * festival theme's prefs file and the preferences DataStore (both read while MainActivity is
     * injected) and the encrypted token (Keystore and Tink setup, the slowest step of a cold
     * start). A later reader finds each cached, or waits for the read already under way.
     */
    private fun warmUp() {
        // getSharedPreferences starts reading the file on a thread of its own; SiteThemeRepository
        // reads the cached festival theme from it on the main thread while MainActivity is injected
        getSharedPreferences(com.neb.ians.data.theme.SiteThemeRepository.PREFS, MODE_PRIVATE)
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
        scope.launch { runCatching { dataStore.data.first() } }
        scope.launch { runCatching { SecurePrefs.getAuthToken(this@NEBiansApp) } }
        scope.launch { com.neb.ians.data.api.ApiService.preconnect() }
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
                    "library_alerts",
                    "Library alerts",
                    NotificationManager.IMPORTANCE_DEFAULT
                ).apply { description = "New resources for your class and subjects" },
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
