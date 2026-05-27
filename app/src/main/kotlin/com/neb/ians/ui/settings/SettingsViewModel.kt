package com.neb.ians.ui.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.prefs.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SettingsUi(
    val darkMode: Boolean = false,
    val pushEnabled: Boolean = true,
)

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val repo: SettingsRepository,
) : ViewModel() {

    val uiState: StateFlow<SettingsUi> = combine(repo.darkMode, repo.pushEnabled) { d, p ->
        SettingsUi(darkMode = d, pushEnabled = p)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), SettingsUi())

    fun setDarkMode(on: Boolean) { viewModelScope.launch { repo.setDarkMode(on) } }
    fun setPushEnabled(on: Boolean) { viewModelScope.launch { repo.setPushEnabled(on) } }
}
