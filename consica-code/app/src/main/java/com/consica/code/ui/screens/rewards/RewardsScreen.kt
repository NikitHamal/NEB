package com.consica.code.ui.screens.rewards

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.content.BadgeCatalog
import com.consica.code.domain.content.EcosystemCatalog
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.XpProgressBar
import java.time.LocalDate

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RewardsScreen(
    onBack: () -> Unit,
    viewModel: RewardsViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.rewards_title), style = MaterialTheme.typography.titleLarge) },
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
            contentPadding = androidx.compose.foundation.layout.PaddingValues(
                start = 20.dp, end = 20.dp, bottom = 32.dp,
            ),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            item { LevelCard(state) }
            item { StreakCard(state) }
            item {
                Text(
                    stringResource(R.string.rewards_badges),
                    style = MaterialTheme.typography.titleLarge,
                )
            }
            item { BadgeGrid(state) }
            item {
                Text(
                    stringResource(R.string.rewards_ecosystem),
                    style = MaterialTheme.typography.titleLarge,
                )
            }
            item { EcosystemGarden(state) }
        }
    }
}

@Composable
private fun LevelCard(state: RewardsUiState) {
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp)) {
            Text(
                text = stringResource(
                    R.string.rewards_level_progress,
                    state.stats.level,
                    state.stats.xpIntoLevel,
                    state.stats.xpForNextLevel,
                ),
                style = MaterialTheme.typography.titleMedium,
            )
            Spacer(Modifier.height(8.dp))
            XpProgressBar(progress = state.stats.levelProgress, modifier = Modifier.fillMaxWidth())
            Spacer(Modifier.height(8.dp))
            Text(
                text = stringResource(R.string.rewards_mastery, state.stats.masteryPoints),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun StreakCard(state: RewardsUiState) {
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("🔥", style = MaterialTheme.typography.headlineMedium)
                Spacer(Modifier.size(8.dp))
                Text(
                    text = stringResource(R.string.rewards_streak_days, state.stats.streakDays),
                    style = MaterialTheme.typography.titleMedium,
                )
            }
            Spacer(Modifier.height(10.dp))
            // Last 7 days, oldest to newest
            val today = LocalDate.now().toEpochDay()
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                for (offset in 6 downTo 0) {
                    val day = today - offset
                    val active = day in state.activeEpochDays
                    Box(
                        Modifier
                            .size(34.dp)
                            .clip(CircleShape)
                            .background(
                                if (active) MaterialTheme.colorScheme.primary
                                else MaterialTheme.colorScheme.surfaceContainerHighest
                            ),
                        contentAlignment = Alignment.Center,
                    ) {
                        if (active) Text("🌱", style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
            Spacer(Modifier.height(10.dp))
            Text(
                text = stringResource(
                    if (state.activeToday) R.string.rewards_active_today
                    else R.string.rewards_come_back
                ),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun BadgeGrid(state: RewardsUiState) {
    if (state.earnedBadgeIds.isEmpty()) {
        Text(
            stringResource(R.string.rewards_no_badges),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(Modifier.height(4.dp))
    }
    LazyVerticalGrid(
        columns = GridCells.Fixed(3),
        modifier = Modifier
            .fillMaxWidth()
            .height(((BadgeCatalog.badges.size + 2) / 3 * 132).dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        userScrollEnabled = false,
    ) {
        items(BadgeCatalog.badges, key = { it.id }) { badge ->
            val earned = badge.id in state.earnedBadgeIds
            EcoCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .alpha(if (earned) 1f else 0.4f),
            ) {
                Column(
                    Modifier
                        .fillMaxWidth()
                        .padding(10.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    Text(
                        text = if (earned) badge.emoji else "🔒",
                        style = MaterialTheme.typography.headlineMedium,
                    )
                    Text(
                        text = stringResource(badge.nameRes),
                        style = MaterialTheme.typography.labelMedium,
                        textAlign = TextAlign.Center,
                        maxLines = 2,
                    )
                    Text(
                        text = if (earned) stringResource(badge.descriptionRes)
                        else stringResource(R.string.rewards_badge_locked),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center,
                        maxLines = 2,
                    )
                }
            }
        }
    }
}

@Composable
private fun EcosystemGarden(state: RewardsUiState) {
    val unlocked = EcosystemCatalog.items.filter { it.id in state.unlockedItemIds }
    if (unlocked.isEmpty()) {
        Text(
            stringResource(R.string.rewards_no_items),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        return
    }
    EcoCard(
        modifier = Modifier.fillMaxWidth(),
        containerColor = MaterialTheme.colorScheme.primaryContainer,
    ) {
        Column(Modifier.padding(16.dp)) {
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                // Garden row: items grow side by side
                unlocked.take(8).forEach { item ->
                    Text(item.emoji, style = MaterialTheme.typography.headlineMedium)
                }
            }
            if (unlocked.size > 8) {
                Spacer(Modifier.height(4.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    unlocked.drop(8).forEach { item ->
                        Text(item.emoji, style = MaterialTheme.typography.headlineMedium)
                    }
                }
            }
            Spacer(Modifier.height(8.dp))
            Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                unlocked.forEach { item ->
                    Text(
                        text = "${item.emoji} " + stringResource(item.nameRes),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer,
                    )
                }
            }
        }
    }
}
