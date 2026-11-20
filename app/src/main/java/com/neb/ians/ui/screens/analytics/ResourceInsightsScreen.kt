package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
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
import com.neb.ians.data.api.ApiResourceInsights
import com.neb.ians.data.api.InsKpi
import com.neb.ians.data.api.InsSplit
import com.neb.ians.data.api.ResRow
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChoiceChips
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.compactCount
import kotlin.math.roundToInt

/** Where "See insights" goes. Set by the navigation host; null hides the entry. A null id means all uploads. */
object ResourceInsightsNav {
    var open: ((String?) -> Unit)? = null
}

private fun resReadTime(sec: Double): String {
    val s = sec.roundToInt()
    return if (s < 60) "${s}s" else "${s / 60}m ${s % 60}s"
}

private fun resPercent(v: Double?): String = if (v == null) "None" else "${(v * 10).roundToInt() / 10.0}%"

/**
 * Insights for the uploader, the web's insights sheet in the app. Opened for one resource from
 * its menu, or for everything the member uploaded from Analytics. Every number is an aggregate.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourceInsightsScreen(
    onNavigateBack: () -> Unit,
    onResourceClick: (String) -> Unit = {},
    onPostClick: (String) -> Unit = {},
    viewModel: ResourceInsightsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val data = uiState.data

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = {
                        Text(
                            if (viewModel.isSingle) "Resource insights" else "Library insights",
                            fontWeight = FontWeight.SemiBold
                        )
                    },
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
            data != null -> ResInsightsContent(
                data = data,
                single = viewModel.isSingle,
                days = uiState.days,
                onRange = viewModel::selectRange,
                onResourceClick = onResourceClick,
                onPostClick = onPostClick,
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

@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
private fun ResInsightsContent(
    data: ApiResourceInsights,
    single: Boolean,
    days: Int,
    onRange: (Int) -> Unit,
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(top = 4.dp, bottom = 40.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item(key = "head") { ResHeadCard(data, single) }
        stickyHeader(key = "range") {
            Box(
                Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(horizontal = AnalyticsGutter, vertical = 6.dp)
            ) {
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
                        "Nothing tracked in this range yet. Opens, reads and downloads are counted from the moment a resource goes live.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
        item(key = "kpis") { ResKpiCard(data) }
        if (data.insights.isNotEmpty()) item(key = "tips") { ResTipsCard(data) }
        item(key = "trend") { ResTrendCard(data) }
        item(key = "funnel") { ResFunnelCard(data) }
        if (data.push.announced > 0) item(key = "push") { ResPushCard(data) }
        if (!single && data.resources.isNotEmpty()) item(key = "table") { ResTableCard(data.resources, onResourceClick) }
        if (!single) data.posts?.takeIf { it.count > 0 }?.let { posts ->
            item(key = "posts") { ResPostsCard(posts, onPostClick) }
        }
        item(key = "audience") { ResAudienceCard(data) }
        if (data.classes.isNotEmpty()) item(key = "classes") { ResSplitCard("Classes reading it", data.classes) }
        if (data.subjects.isNotEmpty()) item(key = "subjects") { ResSplitCard("Subjects", data.subjects) }
        if (data.surfaces.isNotEmpty()) item(key = "surfaces") { ResSplitCard("Where they found it", data.surfaces) }
        if (data.devices.isNotEmpty()) item(key = "devices") { ResSplitCard("Devices", data.devices) }
        if (data.sources.isNotEmpty()) item(key = "sources") { ResSplitCard("Website and app", data.sources) }
        if (data.dwell.buckets.isNotEmpty()) item(key = "dwell") { ResDwellCard(data) }
        item(key = "hours") { ResHoursCard(data) }
        if (data.countries.isNotEmpty()) item(key = "countries") { ResSplitCard("Countries", data.countries) }
        data.lifetime?.let { life ->
            item(key = "lifetime") {
                AnalyticsCard {
                    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                        SectionTitle("All time")
                        StatGrid(
                            listOf(
                                compactCount(life.views) to "Opens",
                                compactCount(life.uniqueViewers) to "People",
                                compactCount(life.impressions) to "Impressions",
                                compactCount(life.downloads) to "Downloads",
                                compactCount(life.likes) to "Likes",
                                compactCount(life.comments) to "Comments",
                                compactCount(life.bookmarks) to "Saves"
                            )
                        )
                    }
                }
            }
        }
        data.totals?.let { t ->
            item(key = "totals") {
                AnalyticsCard {
                    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                        SectionTitle("All time")
                        StatGrid(
                            listOf(
                                t.resources.toString() to "Resources",
                                t.live.toString() to "Live",
                                compactCount(t.views) to "Opens",
                                compactCount(t.downloads) to "Downloads",
                                compactCount(t.likes) to "Likes",
                                compactCount(t.comments) to "Comments"
                            ) + if (t.pending > 0) listOf(t.pending.toString() to "Waiting for review") else emptyList()
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ResHeadCard(data: ApiResourceInsights, single: Boolean) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                text = if (single) data.title else "Everything you shared",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = cs.onSurface,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
            if (single) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                    TonalTag(if (data.ageDays == 0) "Added today" else "${data.ageDays} days old")
                    if (data.subject.isNotBlank()) TonalTag(data.subject)
                    data.standing?.takeIf { it.of > 1 }?.let {
                        TonalTag(
                            "No. ${it.rank} of ${it.of} of your uploads",
                            container = cs.primaryContainer,
                            content = cs.onPrimaryContainer
                        )
                    }
                }
                val st = data.standing
                val vs = st?.vsMedian
                if (st != null && vs != null) {
                    val v = vs.roundToInt()
                    Text(
                        text = when {
                            v > 0 -> "$v% above the median of your uploads (${compactCount(st.medianViews)} opens)."
                            v < 0 -> "${-v}% below the median of your uploads (${compactCount(st.medianViews)} opens)."
                            else -> "Right on the median of your uploads."
                        },
                        style = MaterialTheme.typography.bodyMedium,
                        color = cs.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun ResKpiCard(data: ApiResourceInsights) {
    val k = data.kpis
    val tiles: List<Triple<String, InsKpi, String>> = listOf(
        Triple("Opens", k.views, compactCount(k.views.value.roundToInt())),
        Triple("People", k.uniqueViewers, compactCount(k.uniqueViewers.value.roundToInt())),
        Triple("Impressions", k.impressions, compactCount(k.impressions.value.roundToInt())),
        Triple("Reads", k.reads, compactCount(k.reads.value.roundToInt())),
        Triple("Downloads", k.downloads, compactCount(k.downloads.value.roundToInt())),
        Triple("Shares", k.shares, compactCount(k.shares.value.roundToInt())),
        Triple("Saves", k.saves, compactCount(k.saves.value.roundToInt())),
        Triple("Avg time on page", k.avgDwellSec, resReadTime(k.avgDwellSec.value))
    )
    Column(
        modifier = Modifier
            .padding(horizontal = AnalyticsGutter)
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        tiles.chunked(2).forEach { row ->
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                row.forEach { (label, kpi, shown) ->
                    Column(
                        Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(24.dp))
                            .background(MaterialTheme.colorScheme.surfaceContainerLow)
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        StatBlock(shown, label)
                        DeltaTag(kpi.change?.roundToInt())
                    }
                }
                if (row.size == 1) Box(Modifier.weight(1f).height(1.dp))
            }
        }
    }
}

@Composable
private fun ResTipsCard(data: ApiResourceInsights) {
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
                    if (tip.body.isNotBlank()) Text(tip.body, style = MaterialTheme.typography.bodyMedium, color = ink)
                }
            }
        }
    }
}

@Composable
private fun ResTrendCard(data: ApiResourceInsights) {
    if (data.series.isEmpty()) return
    val (picked, setPicked) = rememberPicked(data.series.size, data.days)
    val day = data.series[picked]
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Opens per day")
            BarChart(
                values = data.series.map { it.views },
                selected = picked,
                onSelect = setPicked,
                description = "Opens per day"
            )
            Text(day.date, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
            StatGrid(
                listOf(
                    day.views.toString() to "Opens",
                    day.unique.toString() to "People",
                    day.reads.toString() to "Reads",
                    day.downloads.toString() to "Downloads"
                )
            )
        }
    }
}

@Composable
private fun ResFunnelCard(data: ApiResourceInsights) {
    val top = data.funnel.maxOfOrNull { it.count } ?: 0
    if (top == 0) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("From list to download")
            data.funnel.forEach { step ->
                BarRow(step.label, step.count, step.count.toFloat() / top)
            }
            StatGrid(
                listOf(
                    resPercent(data.ctr) to "Opened after seeing it",
                    resPercent(data.readRate) to "Of opens were read",
                    resPercent(data.downloadRate) to "Of opens downloaded"
                )
            )
        }
    }
}

@Composable
private fun ResPushCard(data: ApiResourceInsights) {
    val p = data.push
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("New resource alerts")
            StatGrid(
                listOf(
                    compactCount(p.notified) to "Notified",
                    compactCount(p.taps) to "Tapped the alert",
                    compactCount(p.views) to "Opens from alerts",
                    resPercent(p.shareOfViews) to "Of all opens"
                )
            )
        }
    }
}

@Composable
private fun ResTableCard(rows: List<ResRow>, onResourceClick: (String) -> Unit) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            SectionTitle("Your uploads")
            rows.take(15).forEach { r ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .clickable { onResourceClick(r.id) }
                        .padding(vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    Text(
                        r.title,
                        style = MaterialTheme.typography.bodyLarge,
                        fontWeight = FontWeight.Medium,
                        color = cs.onSurface,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        "${compactCount(r.views)} opens  \u00B7  ${compactCount(r.unique)} people  \u00B7  " +
                            "${compactCount(r.reads)} reads  \u00B7  ${compactCount(r.downloads)} downloads",
                        style = MaterialTheme.typography.labelMedium,
                        color = cs.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun ResPostsCard(posts: com.neb.ians.data.api.ResPosts, onPostClick: (String) -> Unit) {
    val cs = MaterialTheme.colorScheme
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Your posts")
            StatGrid(
                listOf(
                    compactCount(posts.views) to "Views in range",
                    posts.count.toString() to "Posts",
                    compactCount(posts.likes) to "Likes",
                    compactCount(posts.replies) to "Replies"
                )
            )
            posts.top.forEach { p ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .clickable { onPostClick(p.id) }
                        .padding(vertical = 6.dp),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    Text(p.title, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium, color = cs.onSurface, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    Text(
                        "${compactCount(p.views)} views  \u00B7  ${p.likes} likes  \u00B7  ${p.replies} replies",
                        style = MaterialTheme.typography.labelMedium,
                        color = cs.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun ResAudienceCard(data: ApiResourceInsights) {
    val a = data.audience
    if (a.members + a.guests == 0) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            SectionTitle("Who opened it")
            StatGrid(
                listOf(
                    a.members.toString() to "Signed-in members",
                    a.guests.toString() to "Guests",
                    a.newViewers.toString() to "First time",
                    a.returning.toString() to "Came back"
                )
            )
        }
    }
}

@Composable
private fun ResSplitCard(title: String, rows: List<InsSplit>) {
    if (rows.isEmpty()) return
    val top = rows.maxOf { it.count }.coerceAtLeast(1)
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            SectionTitle(title)
            rows.forEach { BarRow(it.label.ifBlank { "Unknown" }, it.count, it.count.toFloat() / top) }
        }
    }
}

@Composable
private fun ResDwellCard(data: ApiResourceInsights) {
    val top = data.dwell.buckets.maxOfOrNull { it.count } ?: 0
    if (top == 0) return
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            SectionTitle("Time on the page")
            Text(
                "Average ${resReadTime(data.dwell.avgSec)}, median ${resReadTime(data.dwell.medianSec)}.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            data.dwell.buckets.forEach { BarRow(it.label, it.count, it.count.toFloat() / top) }
        }
    }
}

@Composable
private fun ResHoursCard(data: ApiResourceInsights) {
    if (data.hourly.size != 24 || data.hourly.all { it == 0 }) return
    val (picked, setPicked) = rememberPicked(24, data.days)
    AnalyticsCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            SectionTitle("When people open it")
            BarChart(
                values = data.hourly,
                selected = picked,
                onSelect = setPicked,
                height = 110.dp,
                gap = 2.dp,
                description = "Opens by hour of day"
            )
            val label = "${(picked % 12).let { if (it == 0) 12 else it }} ${if (picked < 12) "AM" else "PM"}"
            Text(
                "$label: ${data.hourly[picked]} opens" +
                    if (data.peakHourLabel.isNotBlank()) ". Busiest at ${data.peakHourLabel}." else "",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
