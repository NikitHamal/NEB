package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp

/** Side by side: up to three routes of any level, the same rows for each so the eye can run across. */
@Composable
internal fun PwCompare(d: PwData, nav: PwNav, pre: String, onBack: () -> Unit) {
    val c = MaterialTheme.colorScheme
    var ids by rememberSaveable(pre) { mutableStateOf(pre) }
    var stage by rememberSaveable { mutableStateOf(d.routeById[pre]?.stage ?: "after12") }
    val chosen = ids.split(",").filter { it.isNotEmpty() }.mapNotNull { d.routeById[it] }
    val pool = remember(d, stage) { d.routes.filter { it.stage == stage && it.group != "abroad" }.sortedBy { it.name } }
    fun toggle(id: String) {
        val cur = ids.split(",").filter { it.isNotEmpty() }
        ids = (if (id in cur) cur - id else if (cur.size < 3) cur + id else cur).joinToString(",")
    }
    val rows: List<Pair<String, (PwRoute) -> String>> = listOf(
        "Duration" to { r: PwRoute -> r.years.substringBefore(" including") },
        "Cost" to { r: PwRoute -> feeText(r.feeMin, r.feeMax).removePrefix("NPR ") },
        "Demand" to { r: PwRoute -> demandWord(demandScore(d, r)) },
        "Competition" to { r: PwRoute -> competitionWord(competitionScore(d, r)) },
        "Start pay a month" to { r: PwRoute -> payText(d, r) },
        "Entry" to { r: PwRoute -> r.entry },
    )
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") { PwTopBar("Compare", PwNav({}, onBack, {}), caption = if (chosen.size < 2) "Pick two or three" else "${chosen.size} routes") }
        if (chosen.size >= 2) {
            item("names") {
                Row(Modifier.padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    chosen.forEachIndexed { i, r -> PwSurface(Modifier.weight(1f), color = pwTone(i).bg, radius = 20.dp, onClick = { toggle(r.id) }) {
                        Text(r.name.substringBefore(" ("), Modifier.padding(12.dp), color = pwTone(i).fg, fontWeight = FontWeight.Bold, maxLines = 3, overflow = TextOverflow.Ellipsis)
                    } }
                }
            }
            items(rows.size, key = { rows[it].first }) { i ->
                Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    PwMono(rows[i].first, color = c.onSurfaceVariant)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        chosen.forEach { r -> Text(rows[i].second(r), Modifier.weight(1f), style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, maxLines = 5) }
                    }
                }
            }
        }
        item("lvl") { PwChipRow(d.stages.map { it.id }, { it == stage }, { levelShort(it) }, { stage = it }) }
        items(pool, key = { it.id }) { r ->
            val on = r.id in ids.split(",")
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = if (on) c.primaryContainer else c.surfaceContainer, radius = 20.dp, onClick = { toggle(r.id) }) {
                Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    PwTile(shortCode(r.name), pwTone(pool.indexOf(r)), 42.dp, solid = on)
                    Text(r.name.substringBefore(" ("), Modifier.weight(1f), fontWeight = FontWeight.SemiBold, maxLines = 2)
                    if (on) PwMono("Added", color = c.onPrimaryContainer)
                }
            }
        }
    }
}
