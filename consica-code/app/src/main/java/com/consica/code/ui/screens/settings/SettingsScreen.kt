package com.consica.code.ui.screens.settings

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.BuildConfig
import com.consica.code.R
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.ThemeIntensity
import com.consica.code.data.content.BadgeCatalog
import com.consica.code.data.prefs.PRO_MODE_MASTERY_THRESHOLD
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.common.EcoCard
import com.consica.code.ui.common.appViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class SettingsUiState(
    val user: UserState = UserState(),
    val completedLessons: Int = 0,
    val badgeCount: Int = 0,
)

class SettingsViewModel(private val container: AppContainer) : ViewModel() {

    val state: StateFlow<SettingsUiState> = combine(
        container.prefs.userState,
        container.learning.completedCount,
        container.learning.earnedBadges,
    ) { user, completed, badges ->
        SettingsUiState(user, completed, badges.size)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), SettingsUiState())

    fun setDarkMode(v: Boolean) = viewModelScope.launch { container.prefs.setDarkMode(v) }
    fun setHighContrast(v: Boolean) = viewModelScope.launch { container.prefs.setHighContrast(v) }
    fun setReducedMotion(v: Boolean) = viewModelScope.launch { container.prefs.setReducedMotion(v) }
    fun setSound(v: Boolean) = viewModelScope.launch { container.prefs.setSoundEnabled(v) }
    fun setGuidance(v: GuidanceLevel) = viewModelScope.launch { container.prefs.setGuidance(v) }
    fun setAgeGroup(v: AgeGroup) = viewModelScope.launch { container.prefs.setAgeGroup(v) }
    fun setThemeIntensity(v: ThemeIntensity) = viewModelScope.launch { container.prefs.setThemeIntensity(v) }

    fun unlockProMode() = viewModelScope.launch {
        container.prefs.setProModeManualUnlock(true)
        container.learning.awardProBadge()
    }

    fun resetProgress() = viewModelScope.launch { container.learning.resetAll() }
}

@Composable
fun SettingsScreen() {
    val viewModel = appViewModel { SettingsViewModel(it) }
    val state by viewModel.state.collectAsState()
    val user = state.user

    var showResetDialog by remember { mutableStateOf(false) }
    var showSummary by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 16.dp),
    ) {
        Text(
            stringResource(R.string.settings_title),
            style = MaterialTheme.typography.headlineSmall,
            modifier = Modifier.padding(vertical = 16.dp),
        )

        // ---- Appearance ----
        SectionLabel(stringResource(R.string.settings_section_appearance))
        EcoCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(vertical = 4.dp)) {
                ToggleRow(
                    title = stringResource(R.string.settings_dark_mode),
                    subtitle = stringResource(R.string.settings_dark_mode_desc),
                    checked = user.darkMode,
                    onChange = viewModel::setDarkMode,
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                ToggleRow(
                    title = stringResource(R.string.settings_high_contrast),
                    subtitle = stringResource(R.string.settings_high_contrast_desc),
                    checked = user.highContrast,
                    onChange = viewModel::setHighContrast,
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                Column(Modifier.padding(16.dp)) {
                    Text(stringResource(R.string.settings_theme_intensity), style = MaterialTheme.typography.titleSmall)
                    Box(Modifier.height(8.dp))
                    Row(horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(8.dp)) {
                        ThemeIntensity.entries.forEach { intensity ->
                            FilterChip(
                                selected = user.themeIntensity == intensity,
                                onClick = { viewModel.setThemeIntensity(intensity) },
                                label = {
                                    Text(
                                        stringResource(
                                            when (intensity) {
                                                ThemeIntensity.PLAYFUL -> R.string.onboarding_theme_playful
                                                ThemeIntensity.BALANCED -> R.string.onboarding_theme_balanced
                                                ThemeIntensity.FOCUSED -> R.string.onboarding_theme_focused
                                            },
                                        ),
                                    )
                                },
                                shape = PillShape,
                            )
                        }
                    }
                }
            }
        }

        // ---- Sound & motion ----
        SectionLabel(stringResource(R.string.settings_section_sound))
        EcoCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(vertical = 4.dp)) {
                ToggleRow(
                    title = stringResource(R.string.settings_sound),
                    subtitle = stringResource(R.string.settings_sound_desc),
                    checked = user.soundEnabled,
                    onChange = viewModel::setSound,
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                ToggleRow(
                    title = stringResource(R.string.settings_reduced_motion),
                    subtitle = stringResource(R.string.settings_reduced_motion_desc),
                    checked = user.reducedMotion,
                    onChange = viewModel::setReducedMotion,
                )
            }
        }

        // ---- Learning ----
        SectionLabel(stringResource(R.string.settings_section_learning))
        EcoCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp)) {
                Text(stringResource(R.string.settings_age_group), style = MaterialTheme.typography.titleSmall)
                Box(Modifier.height(8.dp))
                Row(horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = user.ageGroup == AgeGroup.KIDS,
                        onClick = { viewModel.setAgeGroup(AgeGroup.KIDS) },
                        label = { Text(stringResource(R.string.onboarding_age_kids)) },
                        shape = PillShape,
                    )
                    FilterChip(
                        selected = user.ageGroup == AgeGroup.TEENS,
                        onClick = { viewModel.setAgeGroup(AgeGroup.TEENS) },
                        label = { Text(stringResource(R.string.onboarding_age_teens)) },
                        shape = PillShape,
                    )
                    FilterChip(
                        selected = user.ageGroup == AgeGroup.PRO,
                        onClick = { viewModel.setAgeGroup(AgeGroup.PRO) },
                        label = { Text(stringResource(R.string.onboarding_age_pro)) },
                        shape = PillShape,
                    )
                }

                Box(Modifier.height(16.dp))
                Text(stringResource(R.string.settings_guidance), style = MaterialTheme.typography.titleSmall)
                Box(Modifier.height(8.dp))
                Column(verticalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(4.dp)) {
                    GuidanceLevel.entries.forEach { level ->
                        FilterChip(
                            selected = user.guidance == level,
                            onClick = { viewModel.setGuidance(level) },
                            label = {
                                Text(
                                    stringResource(
                                        when (level) {
                                            GuidanceLevel.FULL -> R.string.settings_guidance_full
                                            GuidanceLevel.BALANCED -> R.string.settings_guidance_balanced
                                            GuidanceLevel.MINIMAL -> R.string.settings_guidance_minimal
                                        },
                                    ),
                                )
                            },
                            shape = PillShape,
                        )
                    }
                }

                Box(Modifier.height(16.dp))
                Text(stringResource(R.string.settings_language), style = MaterialTheme.typography.titleSmall)
                Text(
                    stringResource(R.string.settings_language_english) + "  ·  " +
                        stringResource(R.string.settings_language_nepali_soon),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }

        // ---- Professional mode ----
        SectionLabel(stringResource(R.string.settings_pro_mode))
        EcoCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp)) {
                Text(
                    stringResource(R.string.settings_pro_mode_desc),
                    style = MaterialTheme.typography.bodyMedium,
                )
                Box(Modifier.height(8.dp))
                if (user.professionalEditor) {
                    Text(
                        stringResource(R.string.settings_pro_mode_unlocked),
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.primary,
                    )
                } else {
                    Text(
                        stringResource(R.string.settings_pro_mode_locked_desc, PRO_MODE_MASTERY_THRESHOLD),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    TextButton(onClick = viewModel::unlockProMode) {
                        Text(stringResource(R.string.settings_pro_mode_parent_unlock))
                    }
                }
            }
        }

        // ---- Progress ----
        SectionLabel(stringResource(R.string.settings_section_progress))
        EcoCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp)) {
                TextButton(onClick = { showSummary = true }) {
                    Column(horizontalAlignment = Alignment.Start) {
                        Text(stringResource(R.string.settings_progress_summary))
                        Text(
                            stringResource(R.string.settings_progress_summary_desc),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                TextButton(onClick = { showResetDialog = true }) {
                    Text(
                        stringResource(R.string.settings_reset_progress),
                        color = MaterialTheme.colorScheme.error,
                    )
                }
            }
        }

        // ---- About ----
        SectionLabel(stringResource(R.string.settings_section_about))
        EcoCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp)) {
                Text(
                    stringResource(R.string.settings_about_version, BuildConfig.VERSION_NAME),
                    style = MaterialTheme.typography.titleSmall,
                )
                Text(
                    stringResource(R.string.settings_about_body),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }

        Box(Modifier.height(32.dp))
    }

    if (showResetDialog) {
        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text(stringResource(R.string.settings_reset_confirm_title)) },
            text = { Text(stringResource(R.string.settings_reset_confirm_body)) },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.resetProgress()
                        showResetDialog = false
                    },
                ) { Text(stringResource(R.string.action_reset), color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = {
                TextButton(onClick = { showResetDialog = false }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
        )
    }

    if (showSummary) {
        AlertDialog(
            onDismissRequest = { showSummary = false },
            title = { Text(stringResource(R.string.summary_title)) },
            text = {
                Column {
                    Text(stringResource(R.string.summary_lessons, state.completedLessons))
                    Text(stringResource(R.string.summary_xp, user.xp))
                    Text(stringResource(R.string.summary_badges, state.badgeCount))
                    Text(stringResource(R.string.summary_streak, user.streak))
                    Text(stringResource(R.string.summary_best_streak, user.bestStreak))
                    Text(stringResource(R.string.summary_mastery, user.mastery))
                }
            },
            confirmButton = {
                TextButton(onClick = { showSummary = false }) {
                    Text(stringResource(R.string.action_ok))
                }
            },
        )
    }
}

@Composable
private fun SectionLabel(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.primary,
        modifier = Modifier.padding(top = 16.dp, bottom = 8.dp),
    )
}

@Composable
private fun ToggleRow(
    title: String,
    subtitle: String,
    checked: Boolean,
    onChange: (Boolean) -> Unit,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleSmall)
            Text(
                subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        Switch(checked = checked, onCheckedChange = onChange)
    }
}
