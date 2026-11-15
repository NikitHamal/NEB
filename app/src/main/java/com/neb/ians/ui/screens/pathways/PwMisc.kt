@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Search
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
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
private fun Row2(title: String, sub: String, code: String, tone: Int, onClick: (() -> Unit)?) {
    val c = MaterialTheme.colorScheme
    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 22.dp, onClick = onClick) {
        Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            PwTile(code, pwTone(tone), 46.dp)
            Column(Modifier.weight(1f)) {
                Text(title, fontWeight = FontWeight.Bold, maxLines = 1)
                Text(sub, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 1)
            }
        }
    }
}

@Composable
internal fun PwSearch(d: PwData, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    var q by rememberSaveable { mutableStateOf("") }
    val hits = remember(d, q) { pwSearch(d, q) }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") {
            Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                PwIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", nav.pop)
                Row(Modifier.weight(1f).height(48.dp).clip(RoundedCornerShape(24.dp)).background(c.surfaceContainerHigh), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Outlined.Search, null, Modifier.padding(start = 16.dp, end = 10.dp).size(20.dp), tint = c.onSurfaceVariant)
                    BasicTextField(q, { q = it }, Modifier.weight(1f), singleLine = true, textStyle = TextStyle(color = c.onSurface, fontSize = 15.sp), cursorBrush = SolidColor(c.primary),
                        decorationBox = { inner -> Column { if (q.isEmpty()) Text("Courses, careers, colleges", color = c.onSurfaceVariant); inner() } })
                }
            }
        }
        if (q.isBlank()) item("hint") {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                PwHeading("Try")
                PwChipRow(listOf("Engineering", "Nursing", "Business", "Law", "Teaching", "Agriculture", "Kathmandu"), { false }, { it }, { q = it })
            }
        } else if (hits.empty) item("none") { Note("Nothing matches \"$q\". Try a course, a career or a district.") }
        if (hits.routes.isNotEmpty()) item("h1") { PwHeading("Courses") }
        items(hits.routes, key = { "r" + it.id }) { r -> Row2(r.name.substringBefore(" ("), "${levelShort(r.stage)} \u00B7 ${r.years.substringBefore(" including")}", shortCode(r.name), 0) { nav.push("route:${r.id}") } }
        if (hits.careers.isNotEmpty()) item("h2") { PwHeading("Careers") }
        items(hits.careers, key = { "c" + it.id }) { k ->
            val via = d.routes.firstOrNull { k.id in it.careers }
            Row2(k.name, "Demand ${demandWord(k.demand.toFloat())} \u00B7 NPR ${money(k.entryMin)} to ${money(k.entryMax)} a month", k.name.take(2).uppercase(), 1, via?.let { v -> { nav.push("route:${v.id}") } })
        }
        if (hits.govt.isNotEmpty()) item("h3") { PwHeading("Govt jobs") }
        items(hits.govt, key = { "g" + it.id }) { g -> Row2(g.name, g.body, "GOV", 3) { nav.push("job:${g.id}") } }
        if (hits.providers.isNotEmpty()) item("h4") { PwHeading("Colleges") }
        items(hits.providers, key = { "p" + it.id }) { p -> Row2(p.name, "${p.place} \u00B7 ${p.district} \u00B7 ${p.sector}", p.name.take(1).uppercase(), 2, null) }
    }
}

@Composable
internal fun PwSaved(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val keys = ui.saved.toList().sorted()
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") { PwTopBar("Saved", nav) }
        if (keys.isEmpty()) item("none") { Note("Tap the bookmark on a course, country or job to keep it here.") }
        items(keys, key = { it }) { key ->
            val id = key.substringAfter(":")
            when (key.substringBefore(":")) {
                "route" -> d.routeById[id]?.let { r -> Row2(r.name.substringBefore(" ("), levelShort(r.stage), shortCode(r.name), 0) { nav.push(key) } }
                "country" -> d.abroad.firstOrNull { it.id == id }?.let { a -> Row2(a.country, "Study abroad", a.id.uppercase(), 1) { nav.push(key) } }
                "job" -> d.govt.firstOrNull { it.id == id }?.let { g -> Row2(g.name, g.body, "GOV", 3) { nav.push(key) } }
            }
        }
    }
}

@Composable
internal fun PwFaqScreen(d: PwData, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    var topic by rememberSaveable { mutableStateOf("") }
    var openId by rememberSaveable { mutableStateOf("") }
    val list = remember(d, topic) { d.faq.filter { topic.isEmpty() || it.topic == topic } }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") { PwTopBar("Questions", nav) }
        item("chips") { PwChipRow(listOf("") + d.topics.map { it.id }, { it == topic }, { id -> if (id.isEmpty()) "All" else d.topics.first { it.id == id }.label }, { topic = it }) }
        items(list, key = { it.id }) { f ->
            val open = openId == f.id
            val turn by animateFloatAsState(if (open) 180f else 0f, label = "faqTurn")
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth().animateContentSize(), color = c.surfaceContainer, radius = 22.dp, onClick = { openId = if (open) "" else f.id }) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(f.q, Modifier.weight(1f), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                        Icon(Icons.Outlined.ExpandMore, null, Modifier.rotate(turn), tint = c.onSurfaceVariant)
                    }
                    if (open) {
                        Text(f.a, style = MaterialTheme.typography.bodyMedium)
                        val rs = f.go.mapNotNull { d.routeById[it] }
                        if (rs.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            rs.forEach { r -> PwChip(r.name.substringBefore(" ("), false, { nav.push("route:${r.id}") }) }
                        }
                    }
                }
            }
        }
    }
}
