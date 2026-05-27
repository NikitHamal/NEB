package com.neb.ians.ui.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.prefs.UserPrefs
import com.neb.ians.data.prefs.UserPrefsRepository
import com.neb.ians.ui.theme.ThemeMode
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val repo: UserPrefsRepository,
) : ViewModel() {
    val prefs: StateFlow<UserPrefs> =
        repo.flow.stateIn(viewModelScope, SharingStarted.Eagerly, UserPrefs())

    fun setTheme(mode: ThemeMode) = viewModelScope.launch { repo.setTheme(mode) }
    fun setDynamic(enabled: Boolean) = viewModelScope.launch { repo.setDynamic(enabled) }
    fun setHandle(handle: String) = viewModelScope.launch { repo.setHandle(handle) }
}
