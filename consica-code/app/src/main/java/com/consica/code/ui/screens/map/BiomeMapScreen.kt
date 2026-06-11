package com.consica.code.ui.screens.map

import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.TerraExpression
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.PillButton
import com.consica.code.ui.components.StatChip
import com.consica.code.ui.components.XpProgressBar
import com.consica.code.ui.theme.LocalReducedMotion

@Composable
fun BiomeMapScreen(
    onOpenLesson: (String) -> Unit,
    onOpenRewards: () -> Unit,
    onOpenPaths: () -> Unit,
    onOpenWorkspaces: () -> Unit,
    onOpenSettings: () -> Unit,
    onOpenFreeplay: (String) -> Unit,
    viewModel: BiomeMapViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()

    Scaffold { padding ->
        LazyColumn(
            Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(
                start = 20.dp, end = 20.dp, top = 8.dp, bottom = 32.dp,
            ),
        ) {
            item {
                MapHeader(
                    state = state,
                    onOpenSettings = onOpenSettings,
                    onOpenRewards = onOpenRewards,
                )
            }
            item {
                QuickAccessRow(
                    ageGroup = state.ageGroup,
                    proUnlocked = state.stats.professionalModeUnlocked,
                    onOpenFreeplay = onOpenFreeplay,
                    onOpenWorkspaces = onOpenWorkspaces,
                    onOpenPaths = onOpenPaths,
                )
            }
            state.nextLesson?.let { next ->
                item {
                    PillButton(
                        text = stringResource(R.string.map_continue),
                        onClick = { onOpenLesson(next.id) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 12.dp),
                    )
                }
            }
            items(state.biomes, key = { it.biome.id }) { section ->
                BiomeSectionView(section = section, onOpenLesson = onOpenLesson)
            }
        }
    }
}

@Composable
private fun MapHeader(
    state: MapUiState,
    onOpenSettings: () -> Unit,
    onOpenRewards: () -> Unit,
) {
    Column(Modifier.fillMaxWidth()) {
        Row(
            Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            val terraCd = stringResource(R.string.cd_terra_settings)
            Box(
                Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .clickable(onClick = onOpenSettings)
                    .semantics { contentDescription = terraCd },
            ) {
                TerraAvatar(
                    expression = TerraExpression.HAPPY,
                    modifier = Modifier.fillMaxSize(),
                )
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text(
                    text = stringResource(R.string.map_title),
                    style = MaterialTheme.typography.headlineSmall,
                )
                Text(
                    text = stringResource(R.string.map_level, state.stats.level),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                )
            }
        }
        Spacer(Modifier.height(12.dp))
        Row(
            Modifier
                .fillMaxWidth()
                .clickable(onClick = onOpenRewards),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            StatChip(emoji = "🔥", value = state.stats.streakDays.toString())
            StatChip(emoji = "☀️", value = state.stats.sunCoins.toString())
            StatChip(emoji = "💧", value = state.stats.waterDrops.toString())
            StatChip(emoji = "⭐", value = state.stats.xp.toString())
        }
        Spacer(Modifier.height(10.dp))
        XpProgressBar(progress = state.stats.levelProgress, modifier = Modifier.fillMaxWidth())
        Spacer(Modifier.height(16.dp))
    }
}

@Composable
private fun QuickAccessRow(
    ageGroup: AgeGroup,
    proUnlocked: Boolean,
    onOpenFreeplay: (String) -> Unit,
    onOpenWorkspaces: () -> Unit,
    onOpenPaths: () -> Unit,
) {
    Column(Modifier.fillMaxWidth()) {
        Row(
            Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            QuickCard("🐍", stringResource(R.string.map_quick_python), Modifier.weight(1f)) {
                onOpenFreeplay(TrackLanguage.PYTHON.name)
            }
            QuickCard("🌐", stringResource(R.string.map_quick_web), Modifier.weight(1f)) {
                onOpenFreeplay(TrackLanguage.HTML.name)
            }
        }
        if (ageGroup != AgeGroup.KIDS || proUnlocked) {
            Spacer(Modifier.height(8.dp))
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                QuickCard("📁", stringResource(R.string.map_quick_workspaces), Modifier.weight(1f), onOpenWorkspaces)
                QuickCard("🗺️", stringResource(R.string.path_title), Modifier.weight(1f), onOpenPaths)
            }
        }
        Spacer(Modifier.height(8.dp))
    }
}

@Composable
private fun QuickCard(
    emoji: String,
    label: String,
    modifier: Modifier = Modifier,
    onClick: () -> Unit,
) {
    EcoCard(modifier = modifier, onClick = onClick) {
        Row(
            Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(emoji, style = MaterialTheme.typography.titleMedium)
            Text(
                label,
                style = MaterialTheme.typography.labelLarge,
                maxLines = 2,
            )
        }
    }
}

@Composable
private fun BiomeSectionView(
    section: BiomeSection,
    onOpenLesson: (String) -> Unit,
) {
    val biomeColor = Color(section.biome.colorHex)
    Column(
        Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp)
            .alpha(if (section.unlocked) 1f else 0.5f),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(section.biome.emoji, style = MaterialTheme.typography.headlineMedium)
            Spacer(Modifier.width(10.dp))
            Column {
                Text(
                    stringResource(section.biome.nameRes),
                    style = MaterialTheme.typography.titleLarge,
                )
                Text(
                    text = if (section.unlocked) {
                        stringResource(R.string.map_lessons_done, section.completedCount, section.lessons.size)
                    } else {
                        stringResource(R.string.map_locked_biome)
                    },
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
        Spacer(Modifier.height(8.dp))
        Column {
            section.lessons.forEachIndexed { index, node ->
                LessonNodeRow(
                    node = node,
                    accent = biomeColor,
                    isLast = index == section.lessons.lastIndex,
                    onClick = { if (node.unlocked) onOpenLesson(node.lesson.id) },
                )
            }
        }
    }
}

@Composable
private fun LessonNodeRow(
    node: LessonNode,
    accent: Color,
    isLast: Boolean,
    onClick: () -> Unit,
) {
    val reducedMotion = LocalReducedMotion.current
    val isNext = node.unlocked && !node.completed
    val pulse: Float = if (isNext && !reducedMotion) {
        val transition = rememberInfiniteTransition(label = "nodePulse")
        val value by transition.animateFloat(
            initialValue = 1f,
            targetValue = 1.12f,
            animationSpec = infiniteRepeatable(tween(900), RepeatMode.Reverse),
            label = "nodePulseValue",
        )
        value
    } else 1f

    val title = stringResource(node.lesson.titleRes)
    val nodeDescription = when {
        node.completed -> stringResource(R.string.cd_lesson_completed)
        !node.unlocked -> stringResource(R.string.cd_lesson_locked)
        else -> stringResource(R.string.cd_lesson_node, title)
    }

    Row(
        Modifier
            .fillMaxWidth()
            .clickable(enabled = node.unlocked, onClick = onClick)
            .padding(vertical = 4.dp)
            .semantics { contentDescription = nodeDescription },
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Box(
                Modifier
                    .size(44.dp)
                    .scale(pulse)
                    .clip(CircleShape)
                    .background(
                        when {
                            node.completed -> accent
                            node.unlocked -> MaterialTheme.colorScheme.surface
                            else -> MaterialTheme.colorScheme.surfaceContainerHighest
                        }
                    ),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = when {
                        node.completed -> "✓"
                        !node.unlocked -> "🔒"
                        else -> when (node.lesson.type.name) {
                            "PUZZLE" -> "🧩"
                            "PROJECT" -> "🛠️"
                            else -> "🌱"
                        }
                    },
                    style = MaterialTheme.typography.titleMedium,
                    color = if (node.completed) Color.White else MaterialTheme.colorScheme.onSurface,
                )
            }
            if (!isLast) {
                Box(
                    Modifier
                        .width(3.dp)
                        .height(18.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant),
                )
            }
        }
        Spacer(Modifier.width(14.dp))
        Column(Modifier.weight(1f)) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = if (node.unlocked) MaterialTheme.colorScheme.onSurface
                else MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                text = stringResource(node.lesson.descriptionRes),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
            )
        }
    }
}
