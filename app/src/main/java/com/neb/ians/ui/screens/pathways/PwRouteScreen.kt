@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Compare
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.Schedule
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
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val RTABS = listOf("Careers", "Skills", "Cost", "Entry")

@Composable
internal fun PwRouteScreen(d: PwData, r: PwRoute, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    var tab by rememberSaveable { mutableStateOf("Careers") }
    var open by rememberSaveable { mutableStateOf("") }
    var more by rememberSaveable { mutableStateOf(false) }
    val dem = demandScore(d, r); val comp = competitionScore(d, r)
    val careers = remember(r) { routeCareers(d, r) }
    val like = remember(r) { d.routes.filter { it.stage == r.stage && it.group == r.group && it.id != r.id }.sortedByDescending { demandScore(d, it) }.take(6) }
    Box(Modifier.fillMaxSize()) {
        LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 110.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            item("bar") { PwTopBar("", nav, trailing = { PwSaveButton("route:${r.id}", ui, vm) }) }
            item("hero") {
                val t = pwTone(0)
                Column(
                    Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(30.dp)).background(t.bg)
                        .drawBehind { drawCircle(t.solid.copy(alpha = 0.10f), 90.dp.toPx(), Offset(size.width, 0f)) }
                        .padding(22.dp).animateContentSize(),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    PwMono("${levelShort(r.stage)} \u00B7 ${GROUP_LABEL[r.group] ?: r.group}")
                    Text(r.name.substringBefore(" ("), color = t.fg, fontWeight = FontWeight.ExtraBold, fontSize = 31.sp, lineHeight = 36.sp)
                    Text(r.about, color = t.fg.copy(alpha = 0.88f), style = MaterialTheme.typography.bodyMedium, maxLines = if (more) 30 else 3, overflow = TextOverflow.Ellipsis)
                    if (r.about.length > 140) Text(if (more) "See less" else "See more", color = t.solid, fontWeight = FontWeight.SemiBold, modifier = Modifier.clip(RoundedCornerShape(12.dp)).padding(vertical = 4.dp).clickable { more = !more })
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                        Row(Modifier.clip(RoundedCornerShape(18.dp)).background(c.surface.copy(alpha = 0.7f)).padding(horizontal = 12.dp, vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Outlined.Schedule, null, Modifier.size(16.dp), tint = t.fg)
                            Text(r.years.substringBefore(" including"), color = t.fg, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, maxLines = 1)
                        }
                        Text(r.kind, Modifier.clip(RoundedCornerShape(18.dp)).background(c.surface.copy(alpha = 0.7f)).padding(horizontal = 12.dp, vertical = 8.dp), color = t.fg, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
            item("stats") {
                Row(Modifier.padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    StatTile("Demand", demandWord(dem), 0, true, dem / 5f, Modifier.weight(1f))
                    StatTile("Competition", competitionWord(comp), 1, false, comp / 5f, Modifier.weight(1f))
                    StatTile("Start pay", payText(d, r), 2, false, -1f, Modifier.weight(1f), "NPR per month")
                }
            }
            item("tabs") { PwChipRow(RTABS, { it == tab }, { it }, { tab = it }) }
            when (tab) {
                "Careers" -> {
                    if (careers.isEmpty()) item("none") { Note("No careers are listed for this route yet.") }
                    careers.forEachIndexed { i, k ->
                        item("career-${k.id}") { CareerRow(k, i, open == k.id) { open = if (open == k.id) "" else k.id } }
                    }
                }
                "Skills" -> item("skills") { Pills(r.skills.ifEmpty { listOf("Not listed yet") }) }
                "Cost" -> item("cost") {
                    Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        PwMono("Total programme cost", color = c.onSurfaceVariant)
                        Text(feeText(r.feeMin, r.feeMax), fontWeight = FontWeight.ExtraBold, fontSize = 26.sp)
                        val y = yearsNum(r.years).coerceAtLeast(0.5f)
                        if (r.feeMax > 0) Text("About NPR ${money((r.feeMin / y).toLong())} to ${money((r.feeMax / y).toLong())} a year. Public and scholarship seats sit at the low end, private colleges at the high end.", style = MaterialTheme.typography.bodyMedium, color = c.onSurfaceVariant)
                    }
                }
                else -> item("entry") {
                    Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        PwMono("Who can apply", color = c.onSurfaceVariant); Text(r.entry, style = MaterialTheme.typography.bodyLarge)
                        PwMono("Entrance", color = c.onSurfaceVariant); Text(r.exam, style = MaterialTheme.typography.bodyLarge)
                    }
                }
            }
            val nexts = r.next.mapNotNull { d.routeById[it] }
            if (nexts.isNotEmpty()) item("next") { Related("What comes next", nexts, nav) }
            if (like.isNotEmpty()) item("like") { Related("People also explore", like, nav) }
        }
        Row(Modifier.align(Alignment.BottomCenter).fillMaxWidth().background(c.surface.copy(alpha = 0.94f)).padding(horizontal = 16.dp, vertical = 12.dp), horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            PwSurface(Modifier.weight(1f), color = c.primary, radius = 28.dp, onClick = { nav.push("where:${r.id}") }) {
                Row(Modifier.height(56.dp), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Outlined.LocationOn, null, Modifier.size(22.dp), tint = c.onPrimary)
                    Text("  Find colleges", color = c.onPrimary, fontWeight = FontWeight.Bold)
                }
            }
            PwSurface(color = c.surfaceContainerHigh, radius = 28.dp, onClick = { nav.tab("lab:cmp:${r.id}") }) {
                Box(Modifier.size(56.dp), contentAlignment = Alignment.Center) { Icon(Icons.Outlined.Compare, "Compare", Modifier.size(24.dp)) }
            }
        }
    }
}

@Composable
private fun StatTile(label: String, value: String, tone: Int, solid: Boolean, bar: Float, modifier: Modifier, foot: String = "") {
    val t = pwTone(tone)
    val ink = if (solid) t.onSolid else t.fg
    PwSurface(modifier, color = if (solid) t.solid else t.bg, radius = 24.dp) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            PwMono(label, color = ink.copy(alpha = 0.85f))
            Text(value, color = ink, fontWeight = FontWeight.ExtraBold, fontSize = if (value.length > 8) 17.sp else 22.sp, maxLines = 1)
            if (bar >= 0f) PwBar(bar, ink, ink.copy(alpha = 0.25f)) else Text(foot, color = ink.copy(alpha = 0.85f), fontSize = 11.sp, maxLines = 1)
        }
    }
}
