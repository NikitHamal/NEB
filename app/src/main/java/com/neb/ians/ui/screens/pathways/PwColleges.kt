package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.OpenInNew
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp

/** Colleges tab (route == null) or "Where to study" for one route. Map, district chips and search all read the same list. */
@Composable
internal fun PwColleges(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav, route: PwRoute?) {
    val c = MaterialTheme.colorScheme
    var q by rememberSaveable { mutableStateOf("") }
    var open by rememberSaveable { mutableStateOf("") }
    val kind = if (route != null && (route.kind == "Diploma" || route.kind == "Technical")) "institute" else if (route?.stage == "afterbach") "university" else "college"
    val pool = remember(d, route) { if (route != null) route.where.mapNotNull { d.providers[it] } else d.providers.values.toList() }
    val counts = remember(pool) { pool.groupingBy { it.district }.eachCount() }
    val district = ui.district
    val chips = remember(counts, district) {
        val top = counts.entries.sortedByDescending { it.value }.map { it.key }.take(12)
        listOf("") + (if (district.isNotEmpty() && district !in top) listOf(district) else emptyList()) + top
    }
    val words = q.lowercase().split(" ").filter { it.length >= 2 }
    val list = remember(pool, district, q) {
        pool.filter { p ->
            (district.isEmpty() || p.district == district) && words.all { w -> w in (p.name + " " + p.place + " " + p.district).lowercase() }
        }.sortedWith(compareBy({ if (it.sector == "Public") 0 else 1 }, { it.name }))
    }
    LaunchedEffect(district, kind) { if (district.isNotEmpty() && ui.live.isEmpty()) vm.setDistrict(district, kind) }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("bar") {
            if (route != null) PwTopBar("Where to study", nav, caption = route.name.substringBefore(" ("))
            else Text("Colleges", Modifier.padding(start = 20.dp, top = 16.dp), style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.ExtraBold)
        }
        item("search") {
            Row(Modifier.padding(horizontal = 16.dp).fillMaxWidth().height(54.dp).background56(c.surfaceContainerHigh), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Outlined.Search, null, Modifier.padding(start = 18.dp, end = 12.dp).size(22.dp), tint = c.onSurfaceVariant)
                BasicTextField(
                    q, { q = it }, Modifier.weight(1f), singleLine = true, textStyle = TextStyle(color = c.onSurface, fontSize = androidx.compose.ui.unit.TextUnit(15f, androidx.compose.ui.unit.TextUnitType.Sp)),
                    cursorBrush = SolidColor(c.primary),
                    decorationBox = { inner -> Box { if (q.isEmpty()) Text("Search district, city or college", color = c.onSurfaceVariant); inner() } },
                )
            }
        }
        item("chips") { PwChipRow(chips, { it == district }, { it.ifEmpty { "All" } }, { vm.setDistrict(it, kind) }) }
        item("map") {
            Box(Modifier.padding(horizontal = 16.dp)) {
                PwNepalMap(counts, district, { vm.setDistrict(it, kind) })
                val n = list.size
                PwSurface(Modifier.align(Alignment.BottomStart).padding(12.dp), color = c.surface, radius = 20.dp) {
                    Row(Modifier.padding(horizontal = 12.dp, vertical = 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Icon(Icons.Outlined.LocationOn, null, Modifier.size(16.dp), tint = c.primary)
                        Text("$n ${if (n == 1) "college" else "colleges"}" + if (district.isNotEmpty()) " in $district" else " listed", style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }
        item("title") { PwHeading(if (route != null) "Colleges offering ${route.name.substringBefore(" (")}" else "Colleges and campuses", trailing = if (route != null && route.feeMax > 0) feeText(route.feeMin, route.feeMax).removePrefix("NPR ") else "") }
        itemsIndexed(list, key = { _, p -> p.id }) { i, p -> ProviderRow(p, i, open == p.id) { open = if (open == p.id) "" else p.id } }
        if (list.isEmpty()) item("empty") {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Note(if (district.isEmpty()) "Nothing matches that search." else "No listed college in $district yet. Institutions found there:")
                ui.live.forEachIndexed { i, p ->
                    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 22.dp) {
                        Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            PwTile(p.name.take(1).uppercase(), pwTone(i), 44.dp)
                            Column { Text(p.name, fontWeight = FontWeight.Bold, maxLines = 2); Text(p.where, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant) }
                        }
                    }
                }
            }
        }
    }
}

private fun Modifier.background56(color: androidx.compose.ui.graphics.Color) =
    this.then(Modifier.clip(androidx.compose.foundation.shape.RoundedCornerShape(27.dp)).background(color))

@Composable
private fun ProviderRow(p: PwProvider, index: Int, open: Boolean, onToggle: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth().animateContentSize(), color = c.surfaceContainer, radius = 22.dp, onClick = onToggle) {
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                PwTile(p.name.take(1).uppercase(), pwTone(index), 46.dp)
                Column(Modifier.weight(1f)) {
                    Text(p.name, fontWeight = FontWeight.Bold, maxLines = if (open) 4 else 1, overflow = TextOverflow.Ellipsis)
                    Text("${p.place} \u00B7 ${p.district}", style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 1)
                }
                Column(horizontalAlignment = Alignment.End) { PwMono(p.sector, color = c.onSurface); PwMono(p.kind, color = c.onSurfaceVariant) }
            }
            if (open) {
                if (p.note.isNotBlank()) Text(p.note, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant)
                if (p.website.isNotBlank()) PwSurface(color = c.primaryContainer, radius = 18.dp, onClick = { uri.openUri(p.website) }) {
                    Row(Modifier.padding(horizontal = 14.dp, vertical = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("Website", color = c.onPrimaryContainer, fontWeight = FontWeight.SemiBold)
                        Icon(Icons.Outlined.OpenInNew, null, Modifier.size(16.dp), tint = c.onPrimaryContainer)
                    }
                }
            }
        }
    }
}
