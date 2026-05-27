package com.neb.ians

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import com.neb.ians.ui.NEBiansAppRoot
import com.neb.ians.ui.theme.NEBiansTheme
import com.neb.ians.utils.ThemePreference
import com.neb.ians.utils.ThemeSettings

class MainActivity : ComponentActivity() {

    private lateinit var themeSettings: ThemeSettings

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        themeSettings = ThemeSettings(this)

        setContent {
            val themePreference by themeSettings.themePreference.collectAsState(
                initial = ThemePreference.SYSTEM
            )
            val isDark = when (themePreference) {
                ThemePreference.LIGHT -> false
                ThemePreference.DARK -> true
                ThemePreference.SYSTEM -> isSystemInDarkTheme()
            }

            NEBiansTheme(darkTheme = isDark) {
                NEBiansAppRoot(
                    themeSettings = themeSettings,
                    currentTheme = themePreference
                )
            }
        }
    }
}
