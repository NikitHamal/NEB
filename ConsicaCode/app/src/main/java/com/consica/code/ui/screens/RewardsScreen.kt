package com.consica.code.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.item
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.CardShape
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.PillShape
import com.consica.code.core.model.EcosystemItemType
import com.consica.code.domain.content.BadgeCatalog
import com.consica.code.domain.content.BadgeDef
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.EmptyState
import com.consica.code.ui.components.SectionHeader
import com.consica.code.ui.components.StatChip
import com.consica.code.ui.rewards.badgeIcon
import com.consica.code.ui.rewards.ecosystemIcon

@Composable
fun RewardsScreen(
    viewModel: AppViewModel,
    onOpenStreak: () -> Unit,
) {
    val prefs by viewModel.prefs.collectAsState()
    val badges by viewModel.badges.collectAsState()
    val completedCount by viewModel.completedCount.collectAsState()
    val ecosystem by viewModel.ecosystem.collectAsState()

    val unlocked = badges.map { it.badgeId }.toSet()
    val achievements = BadgeCatalog.all.filter { !it.isCertificate }
    val certificates = BadgeCatalog.all.filter { it.isCertificate }

    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(Dimens.screenPadding),
        verticalArrangement = Arrangement.spacedBy(Dimens.lg),
    ) {
        item {
            Text(
                stringResource(R.string.rewards_title),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
        }

        item {
            Row(horizontalArrangement = Arrangement.spacedBy(Dimens.sm)) {
                StatChip(
                    label = stringResource(R.string.stat_badges),
                    value = unlocked.size.toString(),
                )
                StatChip(
                    label = stringResource(R.string.stat_lessons_done),
                    value = completedCount.toString(),
                )
                StatChip(
                    label = stringResource(R.string.stat_mastery),
                    value = prefs.masteryPoints.toString(),
                )
            }
        }

        // Streak summary (tap to open the full streak dashboard).
        item {
            Surface(
                onClick = onOpenStreak,
                shape = CardShape,
                color = MaterialTheme.colorScheme.surface,
                border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                modifier = Modifier.fillMaxWidth(),
            ) {
                Row(
                    Modifier.padding(Dimens.cardPadding),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Icon(
                        Icons.Filled.LocalFireDepartment,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.tertiary,
                    )
                    Spacer(Modifier.size(Dimens.md))
                    Column(Modifier.weight(1f)) {
                        Text(
                            stringResource(R.string.rewards_streak_title),
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Text(
                            stringResource(R.string.stat_streak_days, prefs.currentStreak),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    Icon(Icons.Filled.ChevronRight, contentDescription = null)
                }
            }
        }

        item { SectionHeader(title = stringResource(R.string.rewards_badges)) }
        badgeRows(achievements, unlocked)

        item { SectionHeader(title = stringResource(R.string.rewards_certificates)) }
        badgeRows(certificates, unlocked)

        item { SectionHeader(title = stringResource(R.string.rewards_decorations)) }
        if (ecosystem.isEmpty()) {
            item { EcoCard { EmptyState(text = stringResource(R.string.rewards_empty)) } }
        } else {
            item {
                Row(
                    Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(Dimens.sm),
                ) {
                    ecosystem.take(20).forEach { eco ->
                        EcoItemChip(EcosystemItemType.from(eco.type))
                    }
                }
            }
        }

        item { Spacer(Modifier.height(Dimens.xl)) }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.badgeRows(
    badges: List<BadgeDef>,
    unlocked: Set<String>,
) {
    badges.chunked(3).forEach { row ->
        item(key = "row_${row.first().id}") {
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(Dimens.sm),
            ) {
                row.forEach { badge ->
                    Box(Modifier.weight(1f)) {
                        BadgeTile(badge = badge, unlocked = badge.id in unlocked)
                    }
                }
                // Pad the final row so tiles keep equal width.
                repeat(3 - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

@Composable
private fun BadgeTile(badge: BadgeDef, unlocked: Boolean) {
    val tint = if (unlocked) MaterialTheme.colorScheme.tertiary else MaterialTheme.colorScheme.outline
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(Dimens.md),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Box(
                Modifier
                    .size(Dimens.iconButton)
                    .clip(PillShape)
                    .background(tint.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center,
            ) {
                Icon(
                    if (unlocked) badgeIcon(badge.iconKey) else Icons.Filled.Lock,
                    contentDescription = null,
                    tint = tint,
                )
            }
            Spacer(Modifier.height(Dimens.xs))
            Text(
                badge.name,
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.onSurface,
                modifier = Modifier.alpha(if (unlocked) 1f else 0.6f),
            )
            if (!unlocked) {
                Text(
                    stringResource(R.string.rewards_locked_badge),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun EcoItemChip(type: EcosystemItemType) {
    Surface(
        shape = PillShape,
        color = MaterialTheme.colorScheme.primary.copy(alpha = 0.12f),
    ) {
        Box(Modifier.padding(Dimens.md)) {
            Icon(
                ecosystemIcon(type),
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
            )
        }
    }
}
