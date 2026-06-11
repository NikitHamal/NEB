package com.consica.code.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.item
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import com.consica.code.BuildConfig
import com.consica.code.R
import com.consica.code.core.design.Dimens
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.ThemeIntensity
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoButton
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.SectionHeader

@Composable
fun SettingsScreen(viewModel: AppViewModel) {
    val prefs by viewModel.prefs.collectAsState()
    val completedCount by viewModel.completedCount.collectAsState()
    var showResetConfirm by remember { mutableStateOf(false) }

    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(Dimens.screenPadding),
        verticalArrangement = Arrangement.spacedBy(Dimens.lg),
    ) {
        item {
            Text(
                stringResource(R.string.settings_title),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
        }

        // ---- Accessibility ----
        item { SectionHeader(title = stringResource(R.string.settings_section_accessibility)) }
        item {
            EcoCard(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(Dimens.cardPadding), verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
                    ToggleRow(
                        title = stringResource(R.string.settings_high_contrast),
                        description = stringResource(R.string.settings_high_contrast_desc),
                        checked = prefs.highContrast,
                        onChange = viewModel::setHighContrast,
                    )
                    ToggleRow(
                        title = stringResource(R.string.settings_reduced_motion),
                        description = stringResource(R.string.settings_reduced_motion_desc),
                        checked = prefs.reducedMotion,
                        onChange = viewModel::setReducedMotion,
                    )
                    ToggleRow(
                        title = stringResource(R.string.settings_sound),
                        description = null,
                        checked = prefs.soundEnabled,
                        onChange = viewModel::setSound,
                    )
                    Column {
                        Text(
                            stringResource(R.string.settings_font_scale),
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Slider(
                            value = prefs.fontScale,
                            onValueChange = viewModel::setFontScale,
                            valueRange = 0.85f..1.5f,
                            steps = 4,
                        )
                    }
                }
            }
        }

        // ---- Learning ----
        item { SectionHeader(title = stringResource(R.string.settings_section_learning)) }
        item {
            EcoCard(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(Dimens.cardPadding), verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
                    ChipChoiceRow(
                        title = stringResource(R.string.settings_guidance_level),
                        options = listOf(
                            GuidanceLevel.FULL to stringResource(R.string.settings_guidance_full),
                            GuidanceLevel.SOME to stringResource(R.string.settings_guidance_some),
                            GuidanceLevel.MINIMAL to stringResource(R.string.settings_guidance_minimal),
                        ),
                        selected = prefs.guidance,
                        onSelect = viewModel::setGuidance,
                    )
                    ChipChoiceRow(
                        title = stringResource(R.string.settings_age_group),
                        options = listOf(
                            AgeGroup.KIDS to stringResource(R.string.onboarding_age_8_12),
                            AgeGroup.TWEENS to stringResource(R.string.onboarding_age_13_16),
                            AgeGroup.TEENS_PLUS to stringResource(R.string.onboarding_age_16_plus),
                        ),
                        selected = prefs.ageGroup,
                        onSelect = viewModel::setAgeGroup,
                    )
                    ChipChoiceRow(
                        title = stringResource(R.string.settings_theme_intensity),
                        options = listOf(
                            ThemeIntensity.PLAYFUL to stringResource(R.string.intensity_playful),
                            ThemeIntensity.BALANCED to stringResource(R.string.intensity_balanced),
                            ThemeIntensity.FOCUSED to stringResource(R.string.intensity_focused),
                        ),
                        selected = prefs.intensity,
                        onSelect = viewModel::setIntensity,
                    )
                }
            }
        }

        // ---- Professional tools ----
        item { SectionHeader(title = stringResource(R.string.settings_section_pro)) }
        item {
            EcoCard(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(Dimens.cardPadding), verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(
                                stringResource(R.string.settings_pro_mode_status),
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                            )
                            Text(
                                stringResource(
                                    if (prefs.proUnlocked) R.string.settings_pro_unlocked
                                    else R.string.settings_pro_locked
                                ),
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                    Text(
                        stringResource(R.string.settings_pro_unlock_desc),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    if (!prefs.proUnlocked) {
                        EcoButton(
                            text = stringResource(R.string.settings_unlock_pro_now),
                            onClick = viewModel::unlockPro,
                        )
                    }
                }
            }
        }

        // ---- Progress ----
        item { SectionHeader(title = stringResource(R.string.settings_section_progress)) }
        item {
            EcoCard(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(Dimens.cardPadding), verticalArrangement = Arrangement.spacedBy(Dimens.sm)) {
                    Text(
                        stringResource(R.string.settings_progress_summary),
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        stringResource(R.string.stat_level) + " " + prefs.level +
                            " · " + prefs.xp + " " + stringResource(R.string.stat_xp) +
                            " · " + completedCount + " " + stringResource(R.string.stat_lessons_done),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Spacer(Modifier.height(Dimens.sm))
                    EcoButton(
                        text = stringResource(R.string.settings_reset_progress),
                        onClick = { showResetConfirm = true },
                        containerColor = MaterialTheme.colorScheme.error,
                        contentColor = MaterialTheme.colorScheme.onError,
                    )
                }
            }
        }

        // ---- About ----
        item { SectionHeader(title = stringResource(R.string.settings_section_about)) }
        item {
            EcoCard(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(Dimens.cardPadding), verticalArrangement = Arrangement.spacedBy(Dimens.xs)) {
                    Text(
                        stringResource(R.string.settings_language) + ": " +
                            stringResource(R.string.settings_language_english),
                        style = MaterialTheme.typography.bodyLarge,
                    )
                    Text(
                        stringResource(R.string.settings_language_more_soon),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Spacer(Modifier.height(Dimens.xs))
                    Text(
                        stringResource(R.string.settings_version, BuildConfig.VERSION_NAME),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }

        item { Spacer(Modifier.height(Dimens.xl)) }
    }

    if (showResetConfirm) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { showResetConfirm = false },
            title = { Text(stringResource(R.string.settings_reset_progress), fontWeight = FontWeight.Bold) },
            text = { Text(stringResource(R.string.settings_reset_confirm)) },
            confirmButton = {
                androidx.compose.material3.TextButton(
                    onClick = { viewModel.resetProgress(); showResetConfirm = false },
                ) { Text(stringResource(R.string.action_reset)) }
            },
            dismissButton = {
                androidx.compose.material3.TextButton(onClick = { showResetConfirm = false }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
        )
    }
}

@Composable
private fun ToggleRow(
    title: String,
    description: String?,
    checked: Boolean,
    onChange: (Boolean) -> Unit,
) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Column(Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            if (description != null) {
                Text(
                    description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
        Switch(checked = checked, onCheckedChange = onChange)
    }
}

@Composable
private fun <T> ChipChoiceRow(
    title: String,
    options: List<Pair<T, String>>,
    selected: T,
    onSelect: (T) -> Unit,
) {
    Column {
        Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        Spacer(Modifier.height(Dimens.xs))
        Row(horizontalArrangement = Arrangement.spacedBy(Dimens.sm)) {
            options.forEach { (value, label) ->
                FilterChip(
                    selected = selected == value,
                    onClick = { onSelect(value) },
                    label = { Text(label) },
                )
            }
        }
    }
}
