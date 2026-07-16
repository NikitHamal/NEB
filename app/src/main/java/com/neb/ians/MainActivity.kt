package com.neb.ians

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
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
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject lateinit var authRepository: AuthRepository
    @Inject lateinit var realtimeClient: RealtimeClient
    @Inject lateinit var inAppUpdateHelper: InAppUpdateHelper

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        configureSystemBars()
        handleIntent(intent)
        inAppUpdateHelper.checkForUpdate(this)

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.content.ContextCompat.checkSelfPermission(
                    this,
                    android.Manifest.permission.POST_NOTIFICATIONS
                ) != android.content.pm.PackageManager.PERMISSION_GRANTED
            ) {
                androidx.core.app.ActivityCompat.requestPermissions(
                    this,
                    arrayOf(android.Manifest.permission.POST_NOTIFICATIONS),
                    101
                )
            }
        }

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

            NEBiansTheme(darkTheme = isDarkMode) {
                NEBiansNavHost(
                    settingsViewModel = settingsViewModel,
                    authRepository = authRepository
                )
            }
        }
    }

    private fun configureSystemBars() {
        WindowCompat.setDecorFitsSystemWindows(window, true)
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
}
