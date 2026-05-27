package com.neb.ians

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.staticCompositionLocalOf

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        NotificationHelper.ensureChannel(this)
        requestNotificationPermission()

        val appContainer = NebiansAppContainer(applicationContext)
        setContent {
            val darkMode by appContainer.settings.darkMode.collectAsState(initial = false)
            NEBiansTheme(darkTheme = darkMode) {
                CompositionLocalProvider(LocalNebiansContainer provides appContainer) {
                    NEBiansApp()
                }
            }
        }
    }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) return
        val granted = ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.POST_NOTIFICATIONS
        ) == PackageManager.PERMISSION_GRANTED
        if (!granted) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                1001
            )
        }
    }
}

class NebiansAppContainer(context: Context) {
    val settings = SettingsRepository(context)
    val cache = ResourceCacheManager(context)
    val annotations = AnnotationStore(context)
}

val LocalNebiansContainer = staticCompositionLocalOf<NebiansAppContainer> {
    error("NebiansAppContainer was not provided")
}
