package com.neb.ians

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.WindowManager
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.lifecycleScope
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.NEBiansNavHost
import com.neb.ians.ui.theme.NEBiansTheme
import com.neb.ians.ui.screens.settings.SettingsViewModel
import com.neb.ians.util.DeepLinkBus
import com.neb.ians.util.InAppUpdateHelper
import com.neb.ians.util.NotificationDeepLink
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject lateinit var authRepository: AuthRepository
    @Inject lateinit var realtimeClient: RealtimeClient
    @Inject lateinit var inAppUpdateHelper: InAppUpdateHelper

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        configureEdgeToEdge()
        handleIntent(intent)
        scheduleStartupSideEffects()

        lifecycleScope.launch {
            try {
                val token = authRepository.getToken()
                if (token != null && token.isNotBlank()) {
                    authRepository.refreshProfile()
                    authRepository.syncFcmToken()
                }
            } catch (_: Exception) {}
        }

        setContent {
            val settingsViewModel: SettingsViewModel = hiltViewModel()
            val isDarkMode by settingsViewModel.isDarkMode.collectAsState()

            DisposableEffect(isDarkMode) {
                enableEdgeToEdge(
                    statusBarStyle = if (isDarkMode) {
                        SystemBarStyle.dark(android.graphics.Color.TRANSPARENT)
                    } else {
                        SystemBarStyle.light(
                            android.graphics.Color.TRANSPARENT,
                            android.graphics.Color.TRANSPARENT
                        )
                    },
                    navigationBarStyle = if (isDarkMode) {
                        SystemBarStyle.dark(android.graphics.Color.TRANSPARENT)
                    } else {
                        SystemBarStyle.light(
                            android.graphics.Color.TRANSPARENT,
                            android.graphics.Color.TRANSPARENT
                        )
                    }
                )
                val insetsController = WindowInsetsControllerCompat(window, window.decorView)
                insetsController.isAppearanceLightStatusBars = !isDarkMode
                insetsController.isAppearanceLightNavigationBars = !isDarkMode
                onDispose {}
            }

            NEBiansTheme(darkTheme = isDarkMode) {
                NEBiansNavHost(
                    settingsViewModel = settingsViewModel,
                    authRepository = authRepository
                )
            }
        }
    }

    /**
     * Work that has to happen on launch but must not happen *during* it.
     *
     * The update check binds a Play service, and the notification prompt puts a
     * system dialog on the screen. Run from onCreate the first competes with the
     * first frame, and the second lands on top of the splash animation before
     * the user has seen the app at all. Both are held until the splash has
     * finished and handed over to the first real screen.
     */
    private fun scheduleStartupSideEffects() {
        lifecycleScope.launch {
            delay(STARTUP_DEFERRAL_MS)
            inAppUpdateHelper.checkForUpdate(this@MainActivity)
            requestNotificationPermissionIfNeeded()
        }
    }

    private fun requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) return
        val granted = ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.POST_NOTIFICATIONS
        ) == PackageManager.PERMISSION_GRANTED
        if (!granted) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                REQUEST_CODE_NOTIFICATIONS
            )
        }
    }

    private fun configureEdgeToEdge() {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            window.attributes.layoutInDisplayCutoutMode =
                WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
        }
        val controller = WindowInsetsControllerCompat(window, window.decorView)
        controller.systemBarsBehavior =
            WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
    }

    override fun onStart() {
        super.onStart()
        inAppUpdateHelper.onResume(this)
        realtimeClient.start()
    }

    override fun onStop() {
        super.onStop()
        realtimeClient.stop()
    }

    override fun onDestroy() {
        super.onDestroy()
        inAppUpdateHelper.release()
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIntent(intent)
    }

    @Suppress("DEPRECATION")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == InAppUpdateHelper.REQUEST_CODE_UPDATE) {
            inAppUpdateHelper.onActivityResult(resultCode)
        }
    }

    private fun handleIntent(intent: Intent) {
        val data = intent.data
        if (data != null && data.toString().startsWith("nebians://auth-callback")) {
            val error = data.getQueryParameter("error")
            val authToken = data.getQueryParameter("authToken")
            val isNewUser = data.getQueryParameter("isNewUser")?.toBoolean() ?: false
            val username = data.getQueryParameter("username")

            if (authToken != null) {
                lifecycleScope.launch {
                    val success = authRepository.signInWithWebToken(authToken, isNewUser, username)
                    if (!success) {
                        Toast.makeText(this@MainActivity, "Sign-in failed. Please try again.", Toast.LENGTH_SHORT).show()
                    }
                }
            } else if (error != null) {
                if (error != "cancelled") {
                    Toast.makeText(this, "Sign-in error: $error", Toast.LENGTH_LONG).show()
                }
            }

            setIntent(Intent())
            return
        }

        val notificationDeepLink = NotificationDeepLink.fromIntent(intent)
        if (notificationDeepLink != null) {
            DeepLinkBus.emit(notificationDeepLink)
            setIntent(Intent())
        }
    }

    private companion object {
        /**
         * Long enough to clear the splash, which runs just under 4 seconds,
         * with a margin. If the timeline in SplashScreen changes, change this
         * with it.
         */
        const val STARTUP_DEFERRAL_MS = 4_400L
        const val REQUEST_CODE_NOTIFICATIONS = 101
    }
}
