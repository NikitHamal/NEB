package com.consica.code.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.item
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.PlayCircle
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.CardShape
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.PillShape
import com.consica.code.core.model.EcosystemItemType
import com.consica.code.domain.content.Lesson
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.content.LessonStatus
import com.consica.code.domain.content.Progression
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoButton
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.OfflineBanner
import com.consica.code.ui.components.SectionHeader
import com.consica.code.ui.ecosystem.BiomeScene

@Composable
fun HomeScreen(
    viewModel: AppViewModel,
    onOpenLesson: (String) -> Unit,
    onOpenEcosystem: () -> Unit,
    onOpenStreak: () -> Unit,
    onOpenPath: () -> Unit,
) {
    val prefs by viewModel.prefs.collectAsState()
    val completed by viewModel.completedLessonIds.collectAsState()
    val ecosystem by viewModel.ecosystem.collectAsState()

    val config = com.consica.code.core.model.LocalAgeConfig.current
    val ordered = LessonCatalog.ordered
    val suggested = ordered.firstOrNull {
        it.id !in completed && Progression.isUnlocked(it.id, completed, prefs.proUnlocked)
    } ?: ordered.firstOrNull { it.id !in completed }

    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(Dimens.screenPadding),
        verticalArrangement = Arrangement.spacedBy(Dimens.lg),
    ) {
        item {
            Text(
                stringResource(R.string.home_greeting),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
        }
        item { StatsStrip(prefs) }

        // Biome scene (tap to open full ecosystem).
        item {
            Surface(
                onClick = onOpenEcosystem,
                shape = CardShape,
                color = MaterialTheme.colorScheme.surface,
            ) {
                Column {
                    BiomeScene(
                        items = ecosystem.map { EcosystemItemType.from(it.type) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(180.dp),
                    )
                    Text(
                        stringResource(R.string.home_title),
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.padding(Dimens.lg),
                    )
                }
            }
        }

        // Offline reassurance banner (copy adapts to age tone).
        item {
            OfflineBanner(
                text = stringResource(
                    if (config.isPro) R.string.offline_banner_pro else R.string.offline_banner_kid
                ),
            )
        }

        // Continue learning.
        if (suggested != null) {
            item {
                ContinueCard(lesson = suggested, onClick = { onOpenLesson(suggested.id) })
            }
        }

        item {
            SectionHeader(
                title = stringResource(R.string.home_title),
                trailing = {
                    Text(
                        stringResource(R.string.path_title),
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier
                            .clickable { onOpenPath() }
                            .padding(Dimens.xs),
                    )
                },
            )
        }

        // Vertical biome map of lessons.
        items(ordered, key = { it.id }) { lesson ->
            val status = Progression.status(lesson.id, completed, prefs.proUnlocked)
            LessonNode(
                lesson = lesson,
                status = status,
                onClick = { if (status != LessonStatus.LOCKED) onOpenLesson(lesson.id) },
            )
        }

        item { Spacer(Modifier.height(Dimens.xl)) }
    }
}

@Composable
private fun ContinueCard(lesson: Lesson, onClick: () -> Unit) {
    EcoCard(
        modifier = Modifier.fillMaxWidth(),
        color = MaterialTheme.colorScheme.primaryContainer,
        border = null,
    ) {
        Column(Modifier.padding(Dimens.cardPadding)) {
            Text(
                stringResource(R.string.home_continue_learning),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
            )
            Spacer(Modifier.height(Dimens.xs))
            Text(
                stringResource(lesson.titleRes),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
            )
            Spacer(Modifier.height(Dimens.md))
            EcoButton(
                text = stringResource(R.string.action_continue),
                onClick = onClick,
            )
        }
    }
}

@Composable
private fun LessonNode(lesson: Lesson, status: LessonStatus, onClick: () -> Unit) {
    val (icon, tint) = when (status) {
        LessonStatus.COMPLETED -> Icons.Filled.CheckCircle to MaterialTheme.colorScheme.primary
        LessonStatus.ACTIVE -> Icons.Filled.PlayCircle to MaterialTheme.colorScheme.secondary
        LessonStatus.LOCKED -> Icons.Filled.Lock to MaterialTheme.colorScheme.outline
    }
    Surface(
        onClick = onClick,
        enabled = status != LessonStatus.LOCKED,
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Row(
            Modifier.padding(Dimens.cardPadding),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                Modifier
                    .size(Dimens.iconButton)
                    .clip(PillShape)
                    .background(tint.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center,
            ) {
                Icon(icon, contentDescription = null, tint = tint)
            }
            Spacer(Modifier.width(Dimens.lg))
            Column(Modifier.weight(1f)) {
                Text(
                    stringResource(lesson.titleRes),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = if (status == LessonStatus.LOCKED)
                        MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface,
                )
                Text(
                    stringResource(
                        when (status) {
                            LessonStatus.COMPLETED -> R.string.home_completed_node
                            LessonStatus.ACTIVE -> R.string.home_active_node
                            LessonStatus.LOCKED -> R.string.home_locked_node
                        }
                    ),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}
