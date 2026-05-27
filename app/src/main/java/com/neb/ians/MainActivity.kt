package com.neb.ians

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neb.ians.di.AppModule
import com.neb.ians.ui.navigation.NEBiansNavHost
import com.neb.ians.ui.screens.settings.SettingsViewModel
import com.neb.ians.ui.theme.NEBiansTheme
import com.neb.ians.util.darkModeFlow

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val settingsVm: SettingsViewModel = viewModel {
                SettingsViewModel(
                    AppModule.provideContentRepository(this@MainActivity),
                    this@MainActivity.darkModeFlow
                )
            }
            val darkMode by settingsVm.darkMode.collectAsState(initial = false)
            NEBiansTheme(darkTheme = darkMode) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    NEBiansNavHost(modifier = Modifier)
                }
            }
        }
    }
}
