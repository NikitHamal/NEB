package com.consica.code.ui.screens.settings

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.BuildConfig
import com.consica.code.R
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.GuidanceLevel
import com.consica.code.domain.model.LevelSystem
import com.consica.code.domain.model.ThemeIntensity
import com.consica.code.ui.components.EcoCard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onBack: () -> Unit,
    viewModel: SettingsViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()
    var showResetConfirm by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.settings_title), style = MaterialTheme.typography.titleLarge) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
            )
        },
    ) { padding ->
        LazyColumn(
            Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            item { ProfileSection(state, viewModel) }
            item { AppearanceSection(state, viewModel) }
            item { GuidanceSection(state, viewModel) }
            item { ProModeSection(state, viewModel) }
            item { DataSection(onResetClick = { showResetConfirm = true }) }
            item { AboutSection() }
        }
    }

    if (showResetConfirm) {
        AlertDialog(
            onDismissRequest = { showResetConfirm = false },
            title = { Text(stringResource(R.string.settings_reset_confirm_title)) },
            text = { Text(stringResource(R.string.settings_reset_confirm_body)) },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.resetAll()
                    showResetConfirm = false
                }) {
                    Text(
                        stringResource(R.string.settings_reset_confirm_yes),
                        color = MaterialTheme.colorScheme.error,
                    )
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetConfirm = false }) {
                    Text(stringResource(R.string.cancel))
                }
            },
        )
    }
}

@Composable
private fun SectionCard(titleRes: Int, content: @Composable androidx.compose.foundation.layout.ColumnScope.() -> Unit) {
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp)) {
            Text(
                stringResource(titleRes),
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary,
            )
            Spacer(Modifier.height(10.dp))
            content()
        }
    }
}

@Composable
private fun ProfileSection(state: SettingsUiState, viewModel: SettingsViewModel) {
    SectionCard(R.string.settings_profile) {
        var name by remember(state.settings.displayName) {
            mutableStateOf(state.settings.displayName)
        }
        OutlinedTextField(
            value = name,
            onValueChange = { name = it.take(40) },
            label = { Text(stringResource(R.string.settings_display_name)) },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
        )
        LaunchedEffect(name) {
            if (name != state.settings.displayName) {
                kotlinx.coroutines.delay(600)
                viewModel.setDisplayName(name)
            }
        }
        Spacer(Modifier.height(14.dp))
        Text(stringResource(R.string.settings_age_group), style = MaterialTheme.typography.labelLarge)
        Spacer(Modifier.height(6.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            AgeGroup.entries.forEach { ageGroup ->
                FilterChip(
                    selected = state.ageGroup == ageGroup,
                    onClick = { viewModel.setAgeGroup(ageGroup) },
                    label = { Text(stringResource(ageGroup.labelRes())) },
                )
            }
        }
    }
}

@Composable
private fun AppearanceSection(state: SettingsUiState, viewModel: SettingsViewModel) {
    SectionCard(R.string.settings_appearance) {
        Text(stringResource(R.string.settings_theme_intensity), style = MaterialTheme.typography.labelLarge)
        Spacer(Modifier.height(6.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            ThemeIntensity.entries.forEach { intensity ->
                FilterChip(
                    selected = state.themeIntensity == intensity,
                    onClick = { viewModel.setThemeIntensity(intensity) },
                    label = { Text(stringResource(intensity.labelRes())) },
                )
            }
        }
        Spacer(Modifier.height(8.dp))
        SwitchRow(
            titleRes = R.string.settings_high_contrast,
            descRes = R.string.settings_high_contrast_desc,
            checked = state.settings.highContrast,
            onCheckedChange = viewModel::setHighContrast,
        )
        SwitchRow(
            titleRes = R.string.settings_reduced_motion,
            descRes = R.string.settings_reduced_motion_desc,
            checked = state.settings.reducedMotion,
            onCheckedChange = viewModel::setReducedMotion,
        )
        SwitchRow(
            titleRes = R.string.settings_sound,
            descRes = R.string.settings_sound_desc,
            checked = state.settings.soundEnabled,
            onCheckedChange = viewModel::setSoundEnabled,
        )
    }
}

@Composable
private fun GuidanceSection(state: SettingsUiState, viewModel: SettingsViewModel) {
    SectionCard(R.string.settings_guidance) {
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            GuidanceLevel.entries.forEach { level ->
                FilterChip(
                    selected = state.settings.guidanceLevel == level,
                    onClick = { viewModel.setGuidanceLevel(level) },
                    label = { Text(stringResource(level.labelRes())) },
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}

@Composable
private fun ProModeSection(state: SettingsUiState, viewModel: SettingsViewModel) {
    SectionCard(R.string.settings_pro_mode) {
        val unlocked = state.stats.professionalModeUnlocked
        Row(
            Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                stringResource(R.string.settings_pro_mode_desc),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.weight(1f),
            )
            Spacer(Modifier.width(10.dp))
            Switch(
                checked = state.settings.professionalModeEnabled && unlocked,
                onCheckedChange = viewModel::setProfessionalModeEnabled,
                enabled = unlocked,
            )
        }
        if (!unlocked) {
            Spacer(Modifier.height(4.dp))
            Text(
                stringResource(
                    R.string.settings_pro_mode_locked,
                    LevelSystem.PRO_UNLOCK_LEVEL,
                    LevelSystem.PRO_UNLOCK_MASTERY,
                ),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun DataSection(onResetClick: () -> Unit) {
    SectionCard(R.string.settings_data) {
        Row(
            Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(Modifier.weight(1f)) {
                Text(stringResource(R.string.settings_reset), style = MaterialTheme.typography.bodyLarge)
                Text(
                    stringResource(R.string.settings_reset_desc),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            TextButton(onClick = onResetClick) {
                Text(stringResource(R.string.settings_reset), color = MaterialTheme.colorScheme.error)
            }
        }
    }
}

@Composable
private fun AboutSection() {
    SectionCard(R.string.settings_about) {
        Text(
            stringResource(R.string.settings_about_body),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(Modifier.height(6.dp))
        Text(
            stringResource(R.string.settings_version, BuildConfig.VERSION_NAME),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun SwitchRow(
    titleRes: Int,
    descRes: Int,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    enabled: Boolean = true,
) {
    Row(
        Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(Modifier.weight(1f)) {
            Text(stringResource(titleRes), style = MaterialTheme.typography.bodyLarge)
            Text(
                stringResource(descRes),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        Spacer(Modifier.width(10.dp))
        Switch(checked = checked, onCheckedChange = onCheckedChange, enabled = enabled)
    }
}

private fun AgeGroup.labelRes(): Int = when (this) {
    AgeGroup.KIDS -> R.string.onboarding_age_kids
    AgeGroup.TEENS -> R.string.onboarding_age_teens
    AgeGroup.ADULTS -> R.string.onboarding_age_adults
}

private fun ThemeIntensity.labelRes(): Int = when (this) {
    ThemeIntensity.PLAYFUL -> R.string.onboarding_theme_playful
    ThemeIntensity.BALANCED -> R.string.onboarding_theme_balanced
    ThemeIntensity.FOCUSED -> R.string.onboarding_theme_focused
}

private fun GuidanceLevel.labelRes(): Int = when (this) {
    GuidanceLevel.FULL -> R.string.settings_guidance_full
    GuidanceLevel.BALANCED -> R.string.settings_guidance_balanced
    GuidanceLevel.MINIMAL -> R.string.settings_guidance_minimal
}
