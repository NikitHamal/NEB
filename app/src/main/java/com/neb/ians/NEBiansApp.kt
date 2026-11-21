package com.neb.ians

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
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
class NEBiansApp : Application(), ImageLoaderFactory {

    @Inject
    lateinit var dataStore: DataStore<Preferences>

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
                    .addNetworkInterceptor { chain ->
                        // M3X art files never change under one name: keep them on disk for a year, no revalidation
                        val response = chain.proceed(chain.request())
                        if (chain.request().url.encodedPath.contains("/img/m3x/")) {
                            response.newBuilder().header("Cache-Control", "public, max-age=31536000, immutable").removeHeader("Pragma").build()
                        } else response
                    }
                    .addInterceptor { chain ->
                        val cookies = WafChallengeInterceptor.cachedCookieHeader()
                        val request = chain.request().newBuilder()
                            .header("User-Agent", "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36")
                            .header("Accept", "image/webp,image/apng,image/*,*/*;q=0.8")
                            .header("Accept-Language", "en-US,en;q=0.9")
                            .header("Connection", "keep-alive")
                            .header("Referer", "https://nebians.consica.com.np/")
                            .apply {
                                if (!cookies.isNullOrBlank()) header("Cookie", cookies)
                            }
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

    override fun onTrimMemory(level: Int) {
        super.onTrimMemory(level)
        if (level >= TRIM_MEMORY_UI_HIDDEN || level >= TRIM_MEMORY_RUNNING_LOW) {
            com.neb.ians.ui.pixel.art.PixelOnboardingCache.trim()
            com.neb.ians.ui.components.v3art.V3Cache.trim(empty = level >= TRIM_MEMORY_BACKGROUND)
            if (level >= TRIM_MEMORY_BACKGROUND) com.neb.ians.ui.components.M3xArt.trimMemory()
        }
    }

    override fun onLowMemory() {
        super.onLowMemory()
        com.neb.ians.ui.pixel.art.PixelOnboardingCache.trim()
        com.neb.ians.ui.components.v3art.V3Cache.trim(empty = true)
        com.neb.ians.ui.components.M3xArt.trimMemory()
    }

    /**
     * Starts, off the main thread, the reads the first screen otherwise waits for on it: the
     * festival theme's prefs file and the preferences DataStore (both read while MainActivity is
     * injected) and the encrypted token (Keystore and Tink setup, the slowest step of a cold
     * start). A later reader finds each cached, or waits for the read already under way.
     */
    private fun warmUp() {
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
        scope.launch {
            runCatching { getSharedPreferences(com.neb.ians.data.theme.SiteThemeRepository.PREFS, MODE_PRIVATE) }
            runCatching { dataStore.data.first() }
        }
        scope.launch { runCatching { SecurePrefs.getAuthToken(this@NEBiansApp) } }
        scope.launch { com.neb.ians.data.api.ApiService.preconnect() }
        scope.launch {
            runCatching {
                com.neb.ians.ui.components.M3xArt.covers(this@NEBiansApp)
                com.neb.ians.ui.components.M3xArt.noteRecipe(this@NEBiansApp, 0)
            }
        }
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
