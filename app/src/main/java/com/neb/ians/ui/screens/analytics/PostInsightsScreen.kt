package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiPostInsights
import com.neb.ians.data.api.InsKpi
import com.neb.ians.data.api.InsPoll
import com.neb.ians.data.api.InsSplit
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChoiceChips
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.compactCount
import kotlin.math.roundToInt

private fun readTime(sec: Double): String {
    val s = sec.roundToInt()
    return if (s < 60) "${s}s" else "${s / 60}m ${s % 60}s"
}

private fun percent(v: Double?): String = if (v == null) "No data" else "${(v * 10).roundToInt() / 10.0}%"

/**
 * Insights for one post, as the web's insights sheet draws them. Author only; every number is an
 * aggregate, no reader is ever named.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PostInsightsScreen(
    onNavigateBack: () -> Unit,
    viewModel: PostInsightsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val data = uiState.data

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = { Text("Post insights", fontWeight = FontWeight.SemiBold) },
                    navigationIcon = {
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
                )
                if (uiState.isRefreshing) {
                    LinearProgressIndicator(Modifier.fillMaxWidth().height(2.dp))
                } else {
                    Box(Modifier.height(2.dp))
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        when {
            data != null -> InsightsContent(
                data = data,
                days = uiState.days,
                onRange = viewModel::selectRange,
                modifier = Modifier.padding(padding)
            )
            uiState.isLoading -> Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) { NebLoader() }
            else -> Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.CloudOff,
                    title = "Insights unavailable",
                    subtitle = uiState.error ?: "Try again in a moment.",
                    action = {
                        NebButton(
                            text = "Try again",
                            onClick = viewModel::load,
                            tone = NebButtonTone.Outlined,
                            size = NebButtonSize.Small
                        )
                    }
                )
            }
        }
    }
}

@Composable
private fun InsightsContent(
    data: ApiPostInsights,
    days: Int,
    onRange: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(top = 4.dp, bottom = 40.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item(key = "head") { HeadCard(data) }
        item(key = "range") {
            Box(Modifier.padding(horizontal = AnalyticsGutter)) {
                NebChoiceChips(
                    options = AnalyticsRanges.map { "$it days" },
                    selectedIndex = AnalyticsRanges.indexOf(days).coerceAtLeast(0),
                    onSelect = { onRange(AnalyticsRanges[it]) }
                )
            }
        }
        if (!data.hasData) {
            item(key = "empty") {
                AnalyticsCard {
                    Text(
                        "Nothing tracked yet. Views and impressions are counted from now on, so check back after a few readers open this post.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
        item(key = "kpis") { KpiRows(data) }
        item(key = "trend") { TrendCard(data) }
        if (data.insights.isNotEmpty()) item(key = "tips") { TipsCard(data) }
        item(key = "audience") { AudienceCard(data) }
        item(key = "sources") { SourcesCard(data) }
        item(key = "devices") { DevicesCard(data) }
        item(key = "read") { ReadCard(data) }
        item(key = "hours") { HoursCard(data) }
        if (data.countries.isNotEmpty()) item(key = "countries") {
            SplitCard("Countries", data.countries)
        }
        data.poll?.let { poll -> item(key = "poll") { PollInsightsCard(poll) } }
        item(key = "lifetime") { LifetimeCard(data) }
    }
}

@Composable
private fun HeadCard(data: ApiPostInsights) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                text = data.title,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = cs.onSurface,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                TonalTag(if (data.ageDays == 0) "Posted today" else "${data.ageDays} days old")
                if (data.standing.total > 1) {
                    TonalTag(
                        "No. ${data.standing.rank} of ${data.standing.total} of your posts",
                        container = cs.primaryContainer,
                        content = cs.onPrimaryContainer
                    )
                }
            }
            data.standing.vsMedian?.let {
                val v = it.roundToInt()
                Text(
                    text = when {
                        v > 0 -> "$v% above the median of your posts (${compactCount(data.standing.medianViews)} views)."
                        v < 0 -> "${-v}% below the median of your posts (${compactCount(data.standing.medianViews)} views)."
                        else -> "Right on the median of your posts."
                    },
                    style = MaterialTheme.typography.bodyMedium,
                    color = cs.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun KpiRows(data: ApiPostInsights) {
    val k = data.kpis
    val tiles: List<Triple<String, InsKpi, String>> = listOf(
        Triple("Views", k.views, compactCount(k.views.value.roundToInt())),
        Triple("Readers", k.uniqueViewers, compactCount(k.uniqueViewers.value.roundToInt())),
        Triple("Impressions", k.impressions, compactCount(k.impressions.value.roundToInt())),
        Triple("Reactions", k.reactions, compactCount(k.reactions.value.roundToInt())),
        Triple("Likes", k.likes, compactCount(k.likes.value.roundToInt())),
        Triple("Replies", k.replies, compactCount(k.replies.value.roundToInt())),
        Triple("Avg read time", k.avgDwellSec, readTime(k.avgDwellSec.value)),
    )
    Column(
        modifier = Modifier
            .padding(horizontal = AnalyticsGutter)
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        tiles.chunked(2).forEach { row ->
            Row(
                Modifier
                    .fillMaxWidth()
                    .height(IntrinsicSize.Min),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                row.forEach { (label, kpi, shown) ->
                    Column(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                            .clip(RoundedCornerShape(24.dp))
                            .background(MaterialTheme.colorScheme.surfaceContainerLow)
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Row(
                            Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                label,
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            DeltaTag(kpi.change?.roundToInt())
                        }
                        Text(
                            shown,
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            maxLines = 1
                        )
                    }
                }
                if (row.size == 1) Box(Modifier.weight(1f))
            }
        }
        Row(
            Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(24.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .padding(16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            StatBlock(percent(data.ctr), "Opened from feed", Modifier.weight(1f))
            StatBlock(percent(data.engagementRate), "Engagement", Modifier.weight(1f))
            if (data.bookmarkRate != null) {
                StatBlock(percent(data.bookmarkRate), "Save rate", Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun TrendCard(data: ApiPostInsights) {
    if (data.series.isEmpty()) return
    val (picked, setPicked) = rememberPicked(data.series.size, data.days)
    val day = data.series[picked]
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Views per day")
            BarChart(
                values = data.series.map { it.views },
                selected = picked,
                onSelect = setPicked,
                description = "Views per day"
            )
            Text(
                day.date,
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            StatGrid(
                listOf(
                    day.views.toString() to "Views",
                    day.unique.toString() to "Readers",
                    day.impressions.toString() to "Impressions",
                    (day.likes + day.replies + day.votes).toString() to "Reactions"
                )
            )
        }
    }
}

@Composable
private fun TipsCard(data: ApiPostInsights) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
            SectionTitle("What stands out")
            data.insights.forEach { tip ->
                val (fill, ink) = when (tip.tone) {
                    "up", "good" -> cs.primaryContainer to cs.onPrimaryContainer
                    "down" -> cs.errorContainer to cs.onErrorContainer
                    "action" -> cs.tertiaryContainer to cs.onTertiaryContainer
                    else -> cs.secondaryContainer to cs.onSecondaryContainer
                }
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(20.dp))
                        .background(fill)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    Text(tip.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = ink)
                    if (tip.body.isNotBlank()) {
                        Text(tip.body, style = MaterialTheme.typography.bodyMedium, color = ink)
                    }
                }
            }
        }
    }
}

@Composable
private fun SplitRow(row: InsSplit) {
    val cs = MaterialTheme.colorScheme
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text(
                row.label.ifBlank { "Unknown" },
                style = MaterialTheme.typography.bodyMedium,
                color = cs.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f)
            )
            Text(
                "${(row.pct * 10).roundToInt() / 10.0}%  \u00B7  ${compactCount(row.count)}",
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = cs.onSurface
            )
        }
        Box(
            Modifier
                .fillMaxWidth()
                .height(8.dp)
                .clip(WebPillShape)
                .background(cs.surfaceContainerHighest)
        ) {
            if (row.count > 0) {
                Box(
                    Modifier
                        .fillMaxWidth((row.pct.toFloat() / 100f).coerceIn(0.04f, 1f))
                        .height(8.dp)
                        .clip(WebPillShape)
                        .background(cs.primary)
                )
            }
        }
    }
}

@Composable
private fun SplitCard(title: String, rows: List<InsSplit>) {
    if (rows.isEmpty()) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle(title)
            rows.forEach { SplitRow(it) }
        }
    }
}

private fun share(count: Int, total: Int): Double = if (total > 0) count * 100.0 / total else 0.0

@Composable
private fun AudienceCard(data: ApiPostInsights) {
    val a = data.audience
    val total = a.members + a.guests
    if (total == 0) return
    val rows = listOf(
        InsSplit("members", "Signed in", a.members, share(a.members, total)),
        InsSplit("guests", "Guests", a.guests, share(a.guests, total)),
        InsSplit("followers", "Follow you", a.followers, share(a.followers, total)),
        InsSplit("returning", "Came back", a.returning, share(a.returning, total)),
        InsSplit("new", "First time", a.newViewers, share(a.newViewers, total))
    )
    SplitCard("Audience", rows)
}

@Composable
private fun SourcesCard(data: ApiPostInsights) {
    val cs = MaterialTheme.colorScheme
    if (data.surfaces.isEmpty() && data.channels.isEmpty() && data.sources.isEmpty()) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Where readers came from")
            if (data.sources.isNotEmpty()) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    data.sources.forEach { TonalTag("${it.label}  ${it.pct.roundToInt()}%") }
                }
            }
            if (data.surfaces.isNotEmpty()) {
                Text("Inside NEBians", style = MaterialTheme.typography.labelLarge, color = cs.onSurfaceVariant)
                data.surfaces.forEach { SplitRow(it) }
            }
            if (data.channels.isNotEmpty()) {
                Text("On the web", style = MaterialTheme.typography.labelLarge, color = cs.onSurfaceVariant)
                data.channels.forEach { SplitRow(it) }
            }
        }
    }
}

@Composable
private fun DevicesCard(data: ApiPostInsights) {
    val cs = MaterialTheme.colorScheme
    if (data.devices.isEmpty() && data.os.isEmpty()) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Devices")
            if (data.devices.isNotEmpty()) {
                Text("Reading on", style = MaterialTheme.typography.labelLarge, color = cs.onSurfaceVariant)
                data.devices.forEach { SplitRow(it) }
            }
            if (data.os.isNotEmpty()) {
                Text("System", style = MaterialTheme.typography.labelLarge, color = cs.onSurfaceVariant)
                data.os.forEach { SplitRow(it) }
            }
            val names = mapOf("like" to "Likes from", "reply" to "Replies from", "vote" to "Votes from")
            names.forEach { (kind, label) ->
                val rows = data.actionsByDevice[kind].orEmpty()
                if (rows.isNotEmpty()) {
                    Text(label, style = MaterialTheme.typography.labelLarge, color = cs.onSurfaceVariant)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        rows.forEach { TonalTag("${it.label}  ${it.count}") }
                    }
                }
            }
        }
    }
}

@Composable
private fun ReadCard(data: ApiPostInsights) {
    val d = data.dwell
    if (d.samples == 0) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Time on the post")
            StatGrid(
                listOf(
                    readTime(d.avgSec) to "Average",
                    readTime(d.medianSec) to "Median"
                )
            )
            d.buckets.forEach { SplitRow(it) }
        }
    }
}

@Composable
private fun HoursCard(data: ApiPostInsights) {
    if (data.hourly.size != 24 || data.hourly.all { it == 0 }) return
    val (picked, setPicked) = rememberPicked(24, data.days)
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            SectionTitle("When people read")
            BarChart(
                values = data.hourly,
                selected = picked,
                onSelect = setPicked,
                height = 110.dp,
                gap = 2.dp,
                description = "Views by hour of day"
            )
            val h = picked
            val label = "${(h % 12).let { if (it == 0) 12 else it }} ${if (h < 12) "AM" else "PM"}"
            Text(
                "$label: ${data.hourly[h]} views" +
                    if (data.peakHourLabel.isNotBlank()) ". Busiest at ${data.peakHourLabel}." else "",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
private fun PollInsightsCard(poll: InsPoll) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Poll results")
            if (poll.question.isNotBlank()) {
                Text(poll.question, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = cs.onSurface)
            }
            StatGrid(
                listOf(
                    poll.totalVotes.toString() to "Votes",
                    poll.voters.toString() to "Voters",
                    (poll.participation?.let { "${(it * 10).roundToInt() / 10.0}%" } ?: "None") to "Of readers voted",
                    poll.options.count { it.added }.toString() to "Options added by members"
                )
            )
            poll.options.forEach { option ->
                SplitRow(InsSplit(option.id, option.text + if (option.added) " (member)" else "", option.votes, option.pct))
                if (option.devices.isNotEmpty()) {
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        option.devices.forEach { TonalTag("${it.label} ${it.count}") }
                    }
                }
            }
        }
    }
}

@Composable
private fun LifetimeCard(data: ApiPostInsights) {
    val l = data.lifetime
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("All time")
            StatGrid(
                listOf(
                    compactCount(l.views) to "Views",
                    compactCount(l.uniqueViewers) to "Readers",
                    compactCount(l.impressions) to "Impressions",
                    compactCount(l.likes) to "Likes",
                    compactCount(l.replies) to "Replies",
                    compactCount(l.bookmarks) to "Saves",
                    compactCount(l.pollVotes) to "Poll votes"
                )
            )
        }
    }
}
