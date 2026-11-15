package com.neb.ians.ui.screens.pathways

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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.School
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val STREAMS = listOf("science" to "Science", "management" to "Management", "humanities" to "Humanities")

private fun levelQuestion(id: String) = when (id) {
    "after8" -> "What comes after Class 8?"
    "after10" -> "What will you do after SEE?"
    "after12" -> "What did you study?"
    else -> "What is your next step?"
}

/** arg is "stage" or "stage:group". After +2 filters by stream, every other level by field. */
@Composable
internal fun PwLevel(d: PwData, arg: String, ui: PathwaysUiState, nav: PwNav) {
    val stage = arg.substringBefore(":")
    val c = MaterialTheme.colorScheme
    var pick by rememberSaveable(arg) { mutableStateOf(arg.substringAfter(":", "").ifEmpty { if (stage == "after12") "science" else "" }) }
    val all = remember(d, stage) { d.routes.filter { it.stage == stage && it.group != "abroad" } }
    val groups = remember(all) { all.map { it.group }.distinct() }
    val stream = stage == "after12"
    val shown = remember(all, pick) {
        val base = when {
            stream && pick in STREAMS.map { it.first } -> all.filter { streamOk(it, pick) }
            pick.isNotEmpty() -> all.filter { it.group == pick }
            else -> all
        }
        base.sortedByDescending { demandScore(d, it) }
    }
    val headLabel = if (stream) "+2 ${STREAMS.firstOrNull { it.first == pick }?.second ?: ""}" else (GROUP_LABEL[pick] ?: levelShort(stage))
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 28.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") { PwTopBar(levelShort(stage), nav) }
        item("head") {
            Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                PwMono("Level ${levelNumber(stage)} \u00B7 ${levelShort(stage)}")
                Text(levelQuestion(stage), fontWeight = FontWeight.ExtraBold, fontSize = 30.sp, lineHeight = 36.sp)
            }
        }
        item("chips") {
            if (stream) PwChipRow(STREAMS, { it.first == pick }, { it.second }, { pick = it.first })
            else PwChipRow(listOf("") + groups, { it == pick }, { if (it.isEmpty()) "All" else GROUP_LABEL[it] ?: it }, { pick = it })
        }
        item("root") {
            val t = pwTone(0)
            Row(
                Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(androidx.compose.foundation.shape.RoundedCornerShape(24.dp)).background(t.bg).padding(14.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Box(Modifier.size(40.dp).clip(CircleShape).background(t.solid), contentAlignment = Alignment.Center) { Icon(Icons.Outlined.School, null, Modifier.size(22.dp), tint = t.onSolid) }
                Column {
                    Text(headLabel, fontWeight = FontWeight.Bold, color = t.fg)
                    Text("${shown.size} common ${if (shown.size == 1) "route" else "routes"}", style = MaterialTheme.typography.bodySmall, color = t.fg.copy(alpha = 0.8f))
                }
            }
        }
        items(shown, key = { it.id }) { r -> TimelineRow(d, r, shown.indexOf(r), nav) }
        item("lab") {
            val t = pwTone(1)
            PwSurface(Modifier.padding(horizontal = 16.dp, vertical = 8.dp).fillMaxWidth(), color = t.bg, radius = 32.dp) {
                Row(Modifier.padding(22.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text("Not sure yet?", fontWeight = FontWeight.ExtraBold, fontSize = 19.sp, color = t.fg)
                        Text("Six quick questions, then we match routes to your strengths.", style = MaterialTheme.typography.bodySmall, color = t.fg.copy(alpha = 0.85f))
                    }
                    PwSurface(color = t.solid, radius = 26.dp, onClick = { nav.tab("lab") }) {
                        Text("Start match", Modifier.padding(horizontal = 20.dp, vertical = 14.dp), color = t.onSolid, fontWeight = FontWeight.Bold, maxLines = 1)
                    }
                }
            }
        }
    }
}

@Composable
private fun TimelineRow(d: PwData, r: PwRoute, index: Int, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val dem = demandScore(d, r)
    Row(Modifier.padding(start = 28.dp, end = 16.dp).height(IntrinsicSize.Min), verticalAlignment = Alignment.CenterVertically) {
        Box(Modifier.width(20.dp).fillMaxHeight(), contentAlignment = Alignment.Center) {
            Box(Modifier.width(2.dp).fillMaxHeight().background(c.outlineVariant))
            Box(Modifier.size(12.dp).clip(CircleShape).background(c.primary))
        }
        PwSurface(Modifier.padding(start = 10.dp).weight(1f), color = c.surfaceContainer, radius = 22.dp, onClick = { nav.push("route:${r.id}") }) {
            Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                PwTile(shortCode(r.name), pwTone(index), 50.dp)
                Column(Modifier.weight(1f)) {
                    Text(r.name.substringBefore(" ("), fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis, fontSize = 15.sp)
                    Text("${r.years.substringBefore(" including")} \u00B7 ${GROUP_LABEL[r.group] ?: r.group}", style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                Column(Modifier.width(62.dp), horizontalAlignment = Alignment.End, verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    Text(demandWord(dem), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    PwBar(dem / 5f, c.primary, c.outlineVariant.copy(alpha = 0.6f), Modifier.fillMaxWidth())
                }
            }
        }
    }
}
