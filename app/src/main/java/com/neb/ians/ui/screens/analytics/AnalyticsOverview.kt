package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Bolt
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.LocalFireDepartment
import androidx.compose.material.icons.outlined.PersonAdd
import androidx.compose.material.icons.outlined.TaskAlt
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.TrendingUp
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.data.api.ApiAnalyticsInsight
import com.neb.ians.data.api.ApiAnalyticsKpi
import com.neb.ians.data.api.ApiAnalyticsStanding
import com.neb.ians.data.api.ApiAnalyticsStreak
import com.neb.ians.data.api.ApiAnalyticsTrendDay
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.compactCount

/** Level, score and the road to the next level, on the brand primary container. */
@Composable
internal fun StandingHero(standing: ApiAnalyticsStanding, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier, container = cs.primaryContainer) {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.SpaceBetween) {
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                    Text(
                        text = "Level ${standing.level}" + if (standing.levelName.isNotBlank()) "  ${standing.levelName}" else "",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = cs.onPrimaryContainer
                    )
                    Text(
                        text = compactCount(standing.score),
                        style = MaterialTheme.typography.displayMedium,
                        fontWeight = FontWeight.Bold,
                        color = cs.onPrimaryContainer
                    )
                    Text(
                        text = "contribution points",
                        style = MaterialTheme.typography.labelLarge,
                        color = cs.onPrimaryContainer
                    )
                }
                if (standing.topPercent != null) {
                    TonalTag(
                        text = "Top ${standing.topPercent}%",
                        container = cs.primary,
                        content = cs.onPrimary,
                        icon = Icons.Outlined.TrendingUp
                    )
                }
            }
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Box(
                    Modifier
                        .fillMaxWidth()
                        .height(10.dp)
                        .clip(WebPillShape)
                        .background(cs.onPrimaryContainer.copy(alpha = 0.16f))
                ) {
                    Box(
                        Modifier
                            .fillMaxWidth((standing.progress / 100f).coerceIn(0.03f, 1f))
                            .height(10.dp)
                            .clip(WebPillShape)
                            .background(cs.primary)
                    )
                }
                val next = standing.nextLevelAt
                Text(
                    text = if (next != null) {
                        "${compactCount((next - standing.score).coerceAtLeast(0))} points to ${standing.nextLevelName.ifBlank { "the next level" }}"
                    } else {
                        "Top level reached"
                    },
                    style = MaterialTheme.typography.labelLarge,
                    color = cs.onPrimaryContainer
                )
            }
        }
    }
}

/** The run of active days, with the last seven as tiles. */
@Composable
internal fun StreakCard(streak: ApiAnalyticsStreak, trend: List<ApiAnalyticsTrendDay>, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    val week = trend.takeLast(7)
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                GlyphTile(
                    icon = Icons.Outlined.LocalFireDepartment,
                    size = 48,
                    polygon = NebGlyphShapes.Sunny,
                    container = cs.tertiaryContainer,
                    tint = cs.onTertiaryContainer
                )
                Column(Modifier.weight(1f)) {
                    Text(
                        text = if (streak.current == 1) "1 day streak" else "${streak.current} day streak",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = cs.onSurface
                    )
                    Text(
                        text = "Longest ${streak.longest}  |  ${streak.activeDays30} active in 30 days",
                        style = MaterialTheme.typography.bodySmall,
                        color = cs.onSurfaceVariant
                    )
                }
                if (streak.atRisk) {
                    TonalTag("Ends today", container = cs.tertiaryContainer, content = cs.onTertiaryContainer)
                }
            }
            if (week.isNotEmpty()) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    week.forEach { day ->
                        val on = day.actions > 0
                        Column(Modifier.weight(1f), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Box(
                                Modifier
                                    .fillMaxWidth()
                                    .height(36.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(if (on) cs.primary else cs.surfaceContainerHighest)
                            )
                            Text(
                                text = day.weekday.take(1),
                                style = MaterialTheme.typography.labelSmall,
                                color = cs.onSurfaceVariant,
                                textAlign = TextAlign.Center
                            )
                        }
                    }
                }
            }
        }
    }
}

private fun toneIcon(tone: String): ImageVector = when (tone) {
    "good" -> Icons.Outlined.TaskAlt
    "action" -> Icons.Outlined.Bolt
    else -> Icons.Outlined.Info
}

/** What the numbers say, most useful first. Tone picks the tile's tonal colour. */
@Composable
internal fun InsightsCard(insights: List<ApiAnalyticsInsight>, modifier: Modifier = Modifier) {
    if (insights.isEmpty()) return
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
            SectionTitle("For you")
            insights.forEachIndexed { i, item ->
                val (fill, ink) = when (item.tone) {
                    "good" -> cs.primaryContainer to cs.onPrimaryContainer
                    "action" -> cs.tertiaryContainer to cs.onTertiaryContainer
                    else -> cs.secondaryContainer to cs.onSecondaryContainer
                }
                val shapes: List<RoundedPolygon> = listOf(NebGlyphShapes.Cookie, NebGlyphShapes.Flower, NebGlyphShapes.Clover, NebGlyphShapes.Sunny)
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.Top) {
                    GlyphTile(toneIcon(item.tone), size = 40, polygon = shapes[i % shapes.size], container = fill, tint = ink)
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(item.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = cs.onSurface)
                        if (item.body.isNotBlank()) {
                            Text(item.body, style = MaterialTheme.typography.bodyMedium, color = cs.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}

private fun kpiIcon(key: String): ImageVector = when (key) {
    "contributions" -> Icons.Outlined.Edit
    "likes" -> Icons.Outlined.ThumbUp
    "responses" -> Icons.Outlined.Forum
    "followers" -> Icons.Outlined.PersonAdd
    "readers" -> Icons.Outlined.Visibility
    else -> Icons.Outlined.CalendarMonth
}

/** Six tiles, two to a row: value, change against the previous period, and a sparkline. */
@Composable
internal fun KpiGrid(kpis: List<ApiAnalyticsKpi>, modifier: Modifier = Modifier) {
    val shapes = listOf(NebGlyphShapes.Cookie, NebGlyphShapes.Sunny, NebGlyphShapes.Flower, NebGlyphShapes.Clover, NebGlyphShapes.Burst, NebGlyphShapes.Pentagon)
    Column(
        modifier = modifier
            .padding(horizontal = AnalyticsGutter)
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        kpis.chunked(2).forEachIndexed { rowIndex, row ->
            Row(
                Modifier
                    .fillMaxWidth()
                    .height(IntrinsicSize.Min),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                row.forEachIndexed { col, kpi ->
                    KpiTile(kpi, shapes[(rowIndex * 2 + col) % shapes.size], Modifier.weight(1f).fillMaxHeight())
                }
                if (row.size == 1) Box(Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun KpiTile(kpi: ApiAnalyticsKpi, polygon: RoundedPolygon, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    Column(
        modifier = modifier
            .clip(RoundedCornerShape(24.dp))
            .background(cs.surfaceContainerLow)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
            GlyphTile(kpiIcon(kpi.key), size = 36, polygon = polygon)
            DeltaTag(kpi.change)
        }
        Column(verticalArrangement = Arrangement.spacedBy(1.dp)) {
            Text(
                text = compactCount(kpi.value),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = cs.onSurface,
                maxLines = 1
            )
            Text(
                text = kpi.label,
                style = MaterialTheme.typography.labelMedium,
                color = cs.onSurfaceVariant,
                maxLines = 1
            )
        }
        Sparkline(kpi.series)
    }
}
