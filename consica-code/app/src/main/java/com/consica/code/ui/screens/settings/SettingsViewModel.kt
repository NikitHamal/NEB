package com.consica.code.ui.screens.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.prefs.AppSettings
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.data.repository.WorkspaceRepository
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.GuidanceLevel
import com.consica.code.domain.model.PlayerStats
import com.consica.code.domain.model.ThemeIntensity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SettingsUiState(
    val settings: AppSettings = AppSettings(),
    val stats: PlayerStats = PlayerStats(),
    val ageGroup: AgeGroup = AgeGroup.KIDS,
    val themeIntensity: ThemeIntensity = ThemeIntensity.BALANCED,
)

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val prefs: UserPreferencesRepository,
    private val progressRepository: ProgressRepository,
    private val workspaceRepository: WorkspaceRepository,
) : ViewModel() {

    val uiState: StateFlow<SettingsUiState> = combine(
        prefs.settings,
        prefs.stats,
        prefs.profile,
    ) { settings, stats, profile ->
        SettingsUiState(
            settings = settings,
            stats = stats,
            ageGroup = profile.ageGroup,
            themeIntensity = profile.themeIntensity,
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), SettingsUiState())

    fun setDisplayName(name: String) = launch { prefs.setDisplayName(name) }
    fun setAgeGroup(ageGroup: AgeGroup) = launch { prefs.setAgeGroup(ageGroup) }
    fun setThemeIntensity(intensity: ThemeIntensity) = launch { prefs.setThemeIntensity(intensity) }
    fun setHighContrast(enabled: Boolean) = launch { prefs.setHighContrast(enabled) }
    fun setReducedMotion(enabled: Boolean) = launch { prefs.setReducedMotion(enabled) }
    fun setSoundEnabled(enabled: Boolean) = launch { prefs.setSoundEnabled(enabled) }
    fun setGuidanceLevel(level: GuidanceLevel) = launch { prefs.setGuidanceLevel(level) }
    fun setProfessionalModeEnabled(enabled: Boolean) = launch { prefs.setProfessionalModeEnabled(enabled) }

    fun resetAll() {
        viewModelScope.launch {
            progressRepository.resetAllProgress()
            workspaceRepository.clearAll()
            prefs.resetProgress()
        }
    }

    private fun launch(block: suspend () -> Unit) {
        viewModelScope.launch { block() }
    }
}
