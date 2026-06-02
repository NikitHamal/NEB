package com.neb.ians

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.NEBiansNavHost
import com.neb.ians.ui.theme.NEBiansTheme
import com.neb.ians.ui.screens.settings.SettingsViewModel
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject lateinit var authRepository: AuthRepository

    var pendingOAuthCallback by mutableStateOf<Uri?>(null)
        private set

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        handleIntent(intent)

        setContent {
            val settingsViewModel: SettingsViewModel = hiltViewModel()
            val isDarkMode by settingsViewModel.isDarkMode.collectAsState()

            NEBiansTheme(darkTheme = isDarkMode) {
                NEBiansNavHost(
                    settingsViewModel = settingsViewModel,
                    authRepository = authRepository,
                    pendingOAuthCallback = pendingOAuthCallback
                ) {
                    pendingOAuthCallback = null
                }
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handleIntent(intent)
    }

    private fun handleIntent(intent: Intent?) {
        val uri = intent?.data ?: return
        if (uri.scheme == "nebians" && uri.host == "auth-callback") {
            pendingOAuthCallback = uri
        }
    }
}