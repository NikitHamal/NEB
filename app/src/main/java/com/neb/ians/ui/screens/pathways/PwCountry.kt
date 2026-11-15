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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private fun range(min: Long, max: Long) = if (max == 0L) "Free" else "${money(min)} to ${money(max)}"

@Composable
internal fun PwCountry(d: PwData, a: PwAbroad, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val sch = a.scholarships.mapNotNull { id -> d.scholarships.firstOrNull { it.id == id } }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 28.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item("bar") { PwTopBar("Study abroad", nav, trailing = { PwSaveButton("country:${a.id}", ui, vm) }) }
        item("hero") {
            val t = pwTone(1)
            Column(
                Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(30.dp)).background(t.bg)
                    .drawBehind { drawCircle(t.solid.copy(alpha = 0.10f), 90.dp.toPx(), Offset(size.width, 0f)) }.padding(22.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                PwMono("Intakes \u00B7 ${a.intakes}", color = t.fg)
                Text(a.country, color = t.fg, fontWeight = FontWeight.ExtraBold, fontSize = 34.sp, lineHeight = 38.sp)
                Text(a.work + ".", color = t.fg.copy(alpha = 0.88f), style = MaterialTheme.typography.bodyMedium)
            }
        }
        item("stats") {
            Row(Modifier.padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                Stat("Tuition a year", range(a.tuitionMin, a.tuitionMax), 0, true, Modifier.weight(1f))
                Stat("Living a year", range(a.livingMin, a.livingMax), 2, false, Modifier.weight(1f))
            }
        }
        item("total") {
            Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                PwMono("Plan for about", color = c.onSurfaceVariant)
                Text("NPR ${money(a.tuitionMin + a.livingMin)} to ${money(a.tuitionMax + a.livingMax)} a year", fontWeight = FontWeight.ExtraBold, fontSize = 22.sp)
                Text("Tuition and living together. Scholarships can cut this sharply.", style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant)
            }
        }
        item("fields") { Column(verticalArrangement = Arrangement.spacedBy(10.dp)) { PwHeading("Popular fields"); Pills(a.fields) } }
        item("exams") { Column(verticalArrangement = Arrangement.spacedBy(10.dp)) { PwHeading("Tests you may need"); Pills(a.exams) } }
        item("note") {
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = pwTone(2).bg, radius = 24.dp) {
                Text(a.note, Modifier.padding(18.dp), color = pwTone(2).fg, style = MaterialTheme.typography.bodyMedium)
            }
        }
        if (sch.isNotEmpty()) item("sh") { PwHeading("Scholarships for this country") }
        sch.forEachIndexed { i, s -> item("s-${s.id}") { ScholarshipRow(s, i) } }
    }
}

@Composable
private fun Stat(label: String, value: String, tone: Int, solid: Boolean, modifier: Modifier) {
    val t = pwTone(tone)
    val ink = if (solid) t.onSolid else t.fg
    PwSurface(modifier, color = if (solid) t.solid else t.bg, radius = 24.dp) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            PwMono(label, color = ink.copy(alpha = 0.85f))
            Text("NPR $value", color = ink, fontWeight = FontWeight.ExtraBold, fontSize = 17.sp, maxLines = 2, lineHeight = 21.sp)
        }
    }
}
