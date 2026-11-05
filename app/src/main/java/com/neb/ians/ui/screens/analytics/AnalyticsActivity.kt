package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiAnalyticsHeatmap
import com.neb.ians.data.api.ApiAnalyticsMix
import com.neb.ians.data.api.ApiAnalyticsRhythm
import com.neb.ians.data.api.ApiAnalyticsTrendDay
import com.neb.ians.ui.components.NebChoiceChips
import com.neb.ians.ui.components.compactCount

private val TrendMetrics = listOf("Activity", "Likes", "Replies", "Reading", "Followers")

private fun metricValue(day: ApiAnalyticsTrendDay, metric: Int): Int = when (metric) {
    0 -> day.actions
    1 -> day.likes
    2 -> day.responses
    3 -> day.reads
    else -> day.followers
}

private fun metricNoun(metric: Int, n: Int): String = when (metric) {
    0 -> if (n == 1) "action" else "actions"
    1 -> if (n == 1) "like received" else "likes received"
    2 -> if (n == 1) "reply received" else "replies received"
    3 -> if (n == 1) "post read" else "posts read"
    else -> if (n == 1) "follower" else "followers"
}

/** One bar per day of the range, for the metric picked in the chips. Tap a bar for its day. */
@Composable
internal fun TrendCard(trend: List<ApiAnalyticsTrendDay>, days: Int, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    var metric by rememberSaveable { mutableStateOf(0) }
    val values = remember(trend, metric) { trend.map { metricValue(it, metric) } }
    val (picked, pick) = rememberPicked(values.size, key = metric to days)
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
            SectionTitle("Trend")
            NebChoiceChips(TrendMetrics, metric, { metric = it })
            if (values.isNotEmpty()) {
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.SpaceBetween) {
                    Column {
                        Text(
                            text = compactCount(values[picked]),
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold,
                            color = cs.onSurface
                        )
                        Text(
                            text = "${metricNoun(metric, values[picked])}  ${trend[picked].label}",
                            style = MaterialTheme.typography.labelMedium,
                            color = cs.onSurfaceVariant
                        )
                    }
                    Column(horizontalAlignment = Alignment.End) {
                        Text(
                            text = compactCount(values.sum()),
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = cs.onSurface
                        )
                        Text(
                            text = "last $days days",
                            style = MaterialTheme.typography.labelMedium,
                            color = cs.onSurfaceVariant
                        )
                    }
                }
                BarChart(
                    values = values,
                    selected = picked,
                    onSelect = pick,
                    gap = if (values.size > 45) 1.dp else if (values.size > 14) 2.dp else 5.dp,
                    description = "${TrendMetrics[metric]} per day"
                )
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(trend.first().label, style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                    Text(trend.last().label, style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                }
            }
        }
    }
}

/** Seventeen weeks of days, Monday first. A tap names the day and its count. */
@Composable
internal fun ConsistencyCard(heatmap: ApiAnalyticsHeatmap, activeDays30: Int, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (heatmap.cells.isEmpty()) return
    var selected by remember { mutableIntStateOf(-1) }
    val cell = heatmap.cells.getOrNull(selected)
    val rowLabels = listOf("M", "", "W", "", "F", "", "S")
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Consistency")
            Text(
                text = if (cell != null) {
                    val n = cell.count
                    "${cell.date.takeLast(5).replace('-', '/')}  $n ${if (n == 1) "action" else "actions"}"
                } else {
                    "$activeDays30 active ${if (activeDays30 == 1) "day" else "days"} in the last 30"
                },
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                color = cs.onSurface
            )
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Column(Modifier.width(12.dp).height(18.dp * 7 + 4.dp * 6)) {
                    rowLabels.forEach { label ->
                        Box(Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                            Text(label, style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                        }
                    }
                }
                HeatmapGrid(
                    cells = heatmap.cells,
                    weeks = heatmap.weeks,
                    selected = selected.takeIf { it >= 0 },
                    onSelect = { selected = if (selected == it) -1 else it },
                    modifier = Modifier.weight(1f)
                )
            }
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.End) {
                Text("Less", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                Spacer8()
                listOf(
                    cs.surfaceContainerHighest,
                    cs.primary.copy(alpha = 0.28f),
                    cs.primary.copy(alpha = 0.52f),
                    cs.primary.copy(alpha = 0.78f),
                    cs.primary
                ).forEach { tone ->
                    Box(
                        Modifier
                            .padding(horizontal = 2.dp)
                            .size(12.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .background(tone)
                    )
                }
                Spacer8()
                Text("More", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun Spacer8() = Box(Modifier.width(8.dp))

/** Activity by hour and by weekday over the last 90 days; the peaks are named and drawn solid. */
@Composable
internal fun RhythmCard(rhythm: ApiAnalyticsRhythm, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (rhythm.total <= 0 || rhythm.hours.size != 24 || rhythm.weekdays.size != 7) return
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
            SectionTitle("When you are active")
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                StatBlock(rhythm.peakHourLabel.ifBlank { "-" }, "Peak hour", Modifier.weight(1f))
                StatBlock(rhythm.peakWeekdayLabel.ifBlank { "-" }, "Busiest day", Modifier.weight(1f))
            }
            BarChart(
                values = rhythm.hours,
                selected = rhythm.peakHour,
                height = 96.dp,
                gap = 2.dp,
                description = "Activity by hour"
            )
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                listOf("12 AM", "6 AM", "12 PM", "6 PM", "11 PM").forEach {
                    Text(it, style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                }
            }
            BarChart(
                values = rhythm.weekdays,
                selected = rhythm.peakWeekday,
                height = 80.dp,
                gap = 8.dp,
                description = "Activity by weekday"
            )
            Row(Modifier.fillMaxWidth()) {
                listOf("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun").forEach {
                    Text(
                        text = it,
                        modifier = Modifier.weight(1f),
                        textAlign = TextAlign.Center,
                        style = MaterialTheme.typography.labelSmall,
                        color = cs.onSurfaceVariant
                    )
                }
            }
        }
    }
}

/** What the member did in the range, as bars scaled to the busiest kind. */
@Composable
internal fun MixCard(mix: List<ApiAnalyticsMix>, days: Int, modifier: Modifier = Modifier) {
    val peak = (mix.maxOfOrNull { it.count } ?: 0).coerceAtLeast(1)
    if (mix.all { it.count == 0 }) return
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("What you did, last $days days")
            mix.forEach { BarRow(it.label, it.count, it.count.toFloat() / peak) }
        }
    }
}
