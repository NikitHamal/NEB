package com.consica.code.ui.screens.rewards

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.Biome
import com.consica.code.data.content.BadgeCatalog
import com.consica.code.data.content.LessonCatalog
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.prefs.PRO_MODE_MASTERY_THRESHOLD
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.common.EcoCard
import com.consica.code.ui.common.appViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn

data class RewardsUiState(
    val user: UserState = UserState(),
    val badges: List<EarnedBadgeEntity> = emptyList(),
    val progress: Map<String, LessonProgressEntity> = emptyMap(),
)

class RewardsViewModel(container: AppContainer) : ViewModel() {
    val state: StateFlow<RewardsUiState> = combine(
        container.prefs.userState,
        container.learning.earnedBadges,
        container.learning.progressMap,
    ) { user, badges, progress ->
        RewardsUiState(user, badges, progress)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), RewardsUiState())
}

@Composable
fun RewardsScreen() {
    val viewModel = appViewModel { RewardsViewModel(it) }
    val state by viewModel.state.collectAsState()
    val user = state.user
    val earnedIds = state.badges.map { it.badgeId }.toSet()
    val completedLessons = state.progress.values.count { it.completed }
    val isPro = user.ageGroup == AgeGroup.PRO || user.professionalEditor

    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(top = 16.dp, bottom = 32.dp),
    ) {
        item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(2) }) {
            Column {
                Text(stringResource(R.string.rewards_title), style = MaterialTheme.typography.headlineSmall)
                Box(Modifier.height(10.dp))
                // Level progress
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(16.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                stringResource(R.string.home_level_label, user.level),
                                style = MaterialTheme.typography.titleLarge,
                            )
                            Box(Modifier.weight(1f))
                            Text(
                                stringResource(R.string.home_xp_label, user.xp),
                                style = MaterialTheme.typography.titleSmall,
                                color = MaterialTheme.colorScheme.primary,
                            )
                        }
                        Box(Modifier.height(8.dp))
                        LinearProgressIndicator(
                            progress = { user.xpIntoLevel / user.xpPerLevel.toFloat() },
                            modifier = Modifier.fillMaxWidth(),
                        )
                        Box(Modifier.height(4.dp))
                        Text(
                            stringResource(R.string.rewards_next_level_progress, user.xpIntoLevel, user.xpPerLevel),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }

        // Stat tiles
        item { StatTile(stringResource(R.string.rewards_sun_coins), user.sunCoins.toString(), "☀️") }
        item { StatTile(stringResource(R.string.rewards_water_drops), user.waterDrops.toString(), "💧") }
        item { StatTile(stringResource(R.string.rewards_streak), stringResource(R.string.home_streak_days, user.streak), "🔥") }
        item { StatTile(stringResource(R.string.rewards_mastery), user.mastery.toString(), "🌟") }
        item { StatTile(stringResource(R.string.rewards_lessons_completed), completedLessons.toString(), "📗") }
        item {
            StatTile(
                stringResource(R.string.rewards_pro_unlocked),
                stringResource(
                    if (user.professionalEditor) R.string.rewards_pro_unlocked_yes else R.string.rewards_pro_unlocked_no,
                ),
                "💼",
            )
        }

        // Streak card
        item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(2) }) {
            EcoCard(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp)) {
                    Text(stringResource(R.string.rewards_streak_title), style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = stringResource(R.string.rewards_streak_today_done),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.primary,
                    )
                    Text(
                        text = stringResource(R.string.rewards_streak_come_back),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }

        // Mastery certificates (paths completed)
        item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(2) }) {
            Column {
                Text(
                    stringResource(R.string.rewards_certificates),
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(vertical = 6.dp),
                )
                val completedBiomes = Biome.entries.filter { biome ->
                    val lessons = LessonCatalog.lessonsFor(biome)
                    lessons.isNotEmpty() && lessons.all { state.progress[it.id]?.completed == true }
                }
                if (completedBiomes.isEmpty()) {
                    Text(
                        stringResource(R.string.empty_dash),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                } else {
                    completedBiomes.forEach { biome ->
                        EcoCard(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            containerColor = MaterialTheme.colorScheme.tertiaryContainer,
                        ) {
                            Text(
                                stringResource(R.string.rewards_certificate_path, stringResource(biome.titleRes)),
                                style = MaterialTheme.typography.titleSmall,
                                color = MaterialTheme.colorScheme.onTertiaryContainer,
                                modifier = Modifier.padding(16.dp),
                            )
                        }
                    }
                }
            }
        }

        // Pro unlock progress
        if (!user.professionalEditor) {
            item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(2) }) {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(16.dp)) {
                        Text(stringResource(R.string.rewards_pro_unlocked), style = MaterialTheme.typography.titleSmall)
                        Text(
                            stringResource(R.string.rewards_pro_progress, PRO_MODE_MASTERY_THRESHOLD, user.mastery),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        Box(Modifier.height(6.dp))
                        LinearProgressIndicator(
                            progress = { (user.mastery / PRO_MODE_MASTERY_THRESHOLD.toFloat()).coerceIn(0f, 1f) },
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }
            }
        }

        // Badges
        item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(2) }) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 6.dp)) {
                Text(stringResource(R.string.rewards_badges), style = MaterialTheme.typography.titleMedium)
                Box(Modifier.weight(1f))
                Text(
                    stringResource(R.string.rewards_badges_earned, earnedIds.size, BadgeCatalog.all.size),
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }

        items(BadgeCatalog.all.filter { !it.professional || isPro || earnedIds.contains(it.id) }) { badge ->
            val earned = badge.id in earnedIds
            EcoCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .alpha(if (earned) 1f else 0.45f),
                containerColor = if (earned) {
                    MaterialTheme.colorScheme.primaryContainer
                } else {
                    MaterialTheme.colorScheme.surface
                },
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    Text(badge.glyph, style = MaterialTheme.typography.displaySmall)
                    Box(Modifier.height(4.dp))
                    Text(
                        stringResource(badge.nameRes),
                        style = MaterialTheme.typography.titleSmall,
                        textAlign = TextAlign.Center,
                    )
                    Text(
                        stringResource(badge.descriptionRes),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center,
                        minLines = 2,
                    )
                    Text(
                        stringResource(
                            if (earned) R.string.a11y_badge_earned else R.string.a11y_badge_locked,
                        ),
                        style = MaterialTheme.typography.labelSmall,
                        color = if (earned) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline,
                    )
                }
            }
        }
    }
}

@Composable
private fun StatTile(label: String, value: String, glyph: String) {
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp)) {
            Text(glyph, style = MaterialTheme.typography.titleLarge)
            Text(value, style = MaterialTheme.typography.headlineSmall)
            Text(
                label,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}
