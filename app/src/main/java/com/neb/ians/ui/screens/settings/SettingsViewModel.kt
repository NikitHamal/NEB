package com.neb.ians.ui.screens.settings

import kotlinx.coroutines.flow.Flow

class SettingsViewModel(
    private val repository: com.neb.ians.data.repository.ContentRepository,
    private val darkModeFlow: Flow<Boolean>
) : androidx.lifecycle.ViewModel() {
    val darkMode: Flow<Boolean> = darkModeFlow
}
