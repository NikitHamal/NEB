package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
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

private fun jobCode(n: String) = n.split(" ", "(").filter { it.firstOrNull()?.isUpperCase() == true }.take(2).joinToString("") { it.take(1) }.ifEmpty { "GV" }

/** Lok Sewa tab: every public service route with its stages, who can apply and a prep path. */
@Composable
internal fun PwGovtHome(d: PwData, nav: PwNav) {
    var track by rememberSaveable { mutableStateOf("") }
    val list = remember(d, track) { d.govt.filter { track.isEmpty() || it.track == track } }
    val c = MaterialTheme.colorScheme
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("title") { Text("Govt jobs and exams", Modifier.padding(start = 20.dp, top = 16.dp), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.ExtraBold) }
        item("hero") {
            val t = pwTone(3)
            Column(
                Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(30.dp)).background(t.bg)
                    .drawBehind { drawCircle(t.solid.copy(alpha = 0.10f), 90.dp.toPx(), Offset(size.width, 0f)) }.padding(22.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                PwMono("Public service", color = t.fg)
                Text("Know the exam before you prepare.", color = t.fg, fontWeight = FontWeight.ExtraBold, fontSize = 27.sp, lineHeight = 32.sp)
                Text("Eligibility, stages and a study path for each route.", color = t.fg.copy(alpha = 0.85f), style = MaterialTheme.typography.bodyMedium)
            }
        }
        item("tracks") { PwChipRow(listOf(PwTopic("", "All")) + d.govtTracks, { it.id == track }, { it.label }, { track = it.id }) }
        items(list, key = { it.id }) { g ->
            val i = d.govt.indexOf(g)
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 24.dp, onClick = { nav.push("job:${g.id}") }) {
                Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    PwTile(jobCode(g.name), pwTone(i), 50.dp)
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(g.name, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(g.level, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(g.need, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    }
                }
            }
        }
        item("foot") { PwMono("Confirm dates and rules in the official notice.", Modifier.padding(horizontal = 20.dp), color = c.onSurfaceVariant) }
    }
}

@Composable
internal fun PwGovtDetail(g: PwGovt, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 28.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item("bar") { PwTopBar("", nav, trailing = { PwSaveButton("job:${g.id}", ui, vm) }) }
        item("hero") {
            val t = pwTone(3)
            Column(Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(30.dp)).background(t.bg).padding(22.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                PwMono(g.body, color = t.fg)
                Text(g.name, color = t.fg, fontWeight = FontWeight.ExtraBold, fontSize = 31.sp, lineHeight = 36.sp)
                Text(g.level, color = t.fg.copy(alpha = 0.85f), style = MaterialTheme.typography.bodyMedium)
            }
        }
        item("who") {
            Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                PwMono("Qualification", color = c.onSurfaceVariant); Text(g.need)
                PwMono("Age", color = c.onSurfaceVariant); Text(g.age)
            }
        }
        item("sh") { PwHeading("Exam stages") }
        items(g.stages.size, key = { "st$it" }) { i ->
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 22.dp) {
                Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    PwTile("0${i + 1}", pwTone(i), 44.dp)
                    Column { Text(g.stages[i].first, fontWeight = FontWeight.Bold); Text(g.stages[i].second, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant) }
                }
            }
        }
        item("subj") { Column(verticalArrangement = Arrangement.spacedBy(10.dp)) { PwHeading("What gets tested"); Pills(g.subjects) } }
        item("ph") { PwHeading("Prep path") }
        items(g.prep.size, key = { "pp$it" }) { i ->
            Row(Modifier.padding(horizontal = 20.dp), verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                PwTile("${i + 1}", pwTone(i + 1), 30.dp, solid = true)
                Text(g.prep[i], Modifier.padding(top = 4.dp), style = MaterialTheme.typography.bodyMedium)
            }
        }
        item("note") { Note(g.note) }
    }
}
