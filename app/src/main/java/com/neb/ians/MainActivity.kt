package com.neb.ians

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.lifecycleScope
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.NEBiansNavHost
import com.neb.ians.ui.theme.NEBiansTheme
import com.neb.ians.ui.screens.settings.SettingsViewModel
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject lateinit var authRepository: AuthRepository

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
                    authRepository = authRepository
                )
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIntent(intent)
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
            
            // Clear the intent data so it doesn't re-trigger on configuration changes
            setIntent(Intent())
        }
    }
}