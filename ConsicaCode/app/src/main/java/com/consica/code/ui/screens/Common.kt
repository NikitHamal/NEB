package com.consica.code.ui.screens

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.MilitaryTech
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import com.consica.code.R
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.EcoPalette
import com.consica.code.data.prefs.UserPrefs
import com.consica.code.ui.components.StatChip

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcoTopBar(title: String, onBack: (() -> Unit)? = null) {
    TopAppBar(
        title = { Text(title) },
        navigationIcon = {
            if (onBack != null) {
                IconButton(onClick = onBack) {
                    Icon(
                        Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = stringResource(R.string.cd_back),
                    )
                }
            }
        },
    )
}

/** Horizontal strip of the learner's live currencies. */
@Composable
fun StatsStrip(prefs: UserPrefs, modifier: Modifier = Modifier) {
    Row(
        modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(vertical = Dimens.xs),
        horizontalArrangement = Arrangement.spacedBy(Dimens.sm),
    ) {
        StatChip(
            label = stringResource(R.string.stat_level),
            value = prefs.level.toString(),
            icon = Icons.Filled.MilitaryTech,
            tint = MaterialTheme.colorScheme.primary,
        )
        StatChip(
            label = stringResource(R.string.stat_xp),
            value = prefs.xp.toString(),
            icon = Icons.Filled.Star,
            tint = EcoPalette.ForestGreen,
        )
        StatChip(
            label = stringResource(R.string.stat_streak),
            value = prefs.currentStreak.toString(),
            icon = Icons.Filled.LocalFireDepartment,
            tint = EcoPalette.SunYellowDeep,
        )
        StatChip(
            label = stringResource(R.string.stat_sun),
            value = prefs.sunCoins.toString(),
            icon = Icons.Filled.WbSunny,
            tint = EcoPalette.SunYellowDeep,
        )
        StatChip(
            label = stringResource(R.string.stat_water),
            value = prefs.waterDrops.toString(),
            icon = Icons.Filled.WaterDrop,
            tint = EcoPalette.RiverBlue,
        )
    }
}
