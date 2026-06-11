package com.consica.code

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.lifecycle.viewmodel.compose.viewModel
import com.consica.code.core.audio.LocalSoundController
import com.consica.code.core.audio.SoundController
import com.consica.code.core.design.ConsicaTheme
import com.consica.code.core.model.AgeConfig
import com.consica.code.core.model.LocalAgeConfig
import com.consica.code.data.prefs.DarkMode
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.ConsicaRoot

/**
 * Single Activity. Reads persisted prefs to drive the theme (dark/high-contrast/reduced-motion/
 * text-scale), publishes the derived [AgeConfig] and a [SoundController], then renders the nav
 * root (onboarding or the main shell).
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val container = (application as ConsicaApp).container

        setContent {
            val viewModel: AppViewModel = viewModel(factory = AppViewModel.Factory(container))
            val prefs by viewModel.prefs.collectAsState()

            val darkTheme = when (prefs.darkMode) {
                DarkMode.SYSTEM -> isSystemInDarkTheme()
                DarkMode.LIGHT -> false
                DarkMode.DARK -> true
            }

            val ageConfig = AgeConfig.forUser(prefs.ageGroup, prefs.intensity)

            val soundController = remember { SoundController() }
            soundController.enabled = prefs.soundEnabled
            DisposableEffect(Unit) {
                onDispose { soundController.release() }
            }

            ConsicaTheme(
                darkTheme = darkTheme,
                highContrast = prefs.highContrast,
                reducedMotion = prefs.reducedMotion,
                fontScale = prefs.fontScale,
            ) {
                CompositionLocalProvider(
                    LocalAgeConfig provides ageConfig,
                    LocalSoundController provides soundController,
                ) {
                    ConsicaRoot(viewModel)
                }
            }
        }
    }
}
