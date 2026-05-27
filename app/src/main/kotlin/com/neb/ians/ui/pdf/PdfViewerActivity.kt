package com.neb.ians.ui.pdf

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.settings.SettingsViewModel
import com.neb.ians.ui.theme.NEBiansTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class PdfViewerActivity : ComponentActivity() {
    companion object {
        const val EXTRA_RESOURCE_ID = "resourceId"
        const val EXTRA_LOCAL_PATH = "localPath"
        const val EXTRA_TITLE = "title"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        val resourceId = intent.getStringExtra(EXTRA_RESOURCE_ID).orEmpty()
        val localPath = intent.getStringExtra(EXTRA_LOCAL_PATH).orEmpty()
        val title = intent.getStringExtra(EXTRA_TITLE) ?: "Document"
        setContent {
            val settingsVm: SettingsViewModel = hiltViewModel()
            val prefs by settingsVm.uiState.collectAsStateWithLifecycle()
            NEBiansTheme(darkTheme = prefs.darkMode) {
                PdfViewerScreen(
                    resourceId = resourceId,
                    localPath = localPath,
                    title = title,
                    onBack = { finish() },
                )
            }
        }
    }
}
