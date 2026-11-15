package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Route
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.QuestionAnswer
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.WorkspacePremium
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

internal fun levelShort(id: String) = when (id) { "after8" -> "After 8"; "after10" -> "After SEE"; "after12" -> "After +2"; else -> "Bachelor's" }

internal fun levelNumber(id: String) = when (id) { "after8" -> 1; "after10" -> 2; "after12" -> 3; else -> 4 }

/** Groups of a level ranked by how many roads they open, each with a one line preview built from real route codes. */
private class PwGroupPreview(val group: String, val title: String, val line: String, val stage: String)

private fun previews(d: PwData, stage: String): List<PwGroupPreview> =
    d.routes.filter { it.stage == stage && it.group != "abroad" }.groupBy { it.group }.entries
        .sortedByDescending { e -> e.value.size * 10 + e.value.map { demandScore(d, it) }.average().toFloat() }
        .take(3).map { (g, rs) ->
            val top = rs.sortedByDescending { demandScore(d, it) }
            val codes = top.take(4).joinToString(", ") { shortCode(it.name) }
            PwGroupPreview(g, GROUP_LABEL[g] ?: g, if (rs.size > 4) "$codes and more" else codes, stage)
        }

@Composable
internal fun PwHome(d: PwData, ui: PathwaysUiState, nav: PwNav) {
    var level by rememberSaveable { mutableStateOf("after12") }
    val c = MaterialTheme.colorScheme
    val list = remember(d, level) { previews(d, level) }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 28.dp), verticalArrangement = Arrangement.spacedBy(22.dp)) {
        item("top") {
            Row(Modifier.fillMaxWidth().padding(start = 20.dp, end = 16.dp, top = 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                PwIconTile(Icons.Filled.Route, pwTone(0), 40.dp, solid = true)
                Text("Pathways", Modifier.weight(1f), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                PwIconButton(Icons.Outlined.Search, "Search", { nav.push("search") })
                PwIconButton(Icons.Outlined.BookmarkBorder, "Saved", { nav.push("saved") })
            }
        }
        item("hero") {
            val t = pwTone(0)
            Box(
                Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(32.dp)).background(t.bg)
                    .drawBehind {
                        drawCircle(t.solid.copy(alpha = 0.10f), 120.dp.toPx(), Offset(size.width, 0f))
                        drawCircle(t.solid.copy(alpha = 0.07f), 70.dp.toPx(), Offset(size.width * 0.78f, size.height * 0.15f))
                    },
            ) {
                Column(Modifier.padding(top = 22.dp, bottom = 20.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    PwMono("Where are you now?", Modifier.padding(horizontal = 22.dp))
                    Text(
                        "Pick your level. See every road ahead.", Modifier.padding(horizontal = 22.dp), color = t.fg,
                        fontWeight = FontWeight.ExtraBold, fontSize = 27.sp, lineHeight = 33.sp,
                    )
                    Spacer(Modifier.height(4.dp))
                    PwChipRow(d.stages.map { it.id }, { it == level }, { levelShort(it) }, { level = it }, pad = 22)
                }
            }
        }
        item("popular") {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("Popular next steps", Modifier.weight(1f), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                    PwSurface(color = c.surfaceContainerHigh, radius = 18.dp, onClick = { nav.push("level:$level") }) {
                        Text("All roads", Modifier.padding(horizontal = 14.dp, vertical = 8.dp), style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
                    }
                }
                list.forEachIndexed { i, g ->
                    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 24.dp, onClick = { nav.push("level:${g.stage}:${g.group}") }) {
                        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                            PwTile("0${i + 1}", pwTone(i), 48.dp)
                            Column(Modifier.weight(1f)) {
                                Text(g.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, maxLines = 1)
                                Text(g.line, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 1)
                            }
                            Icon(Icons.Outlined.ChevronRight, null, tint = c.onSurfaceVariant)
                        }
                    }
                }
            }
        }
        item("explore") {
            Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text("Explore everything", Modifier.padding(horizontal = 4.dp), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    ExploreTile("Study and career", "Courses, careers, colleges", Icons.Outlined.School, 0, true, Modifier.weight(1f)) { nav.push("level:$level") }
                    ExploreTile("Study abroad", "Countries, costs, visas", Icons.Outlined.Public, 1, false, Modifier.weight(1f)) { nav.tab("abroad") }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    ExploreTile("Scholarships", "Embassy and more", Icons.Outlined.WorkspacePremium, 2, false, Modifier.weight(1f)) { nav.push("scholarships") }
                    ExploreTile("Govt jobs and exams", "Syllabus, prep paths", Icons.Outlined.AccountBalance, 3, false, Modifier.weight(1f)) { nav.tab("govt") }
                }
                if (d.faq.isNotEmpty()) PwSurface(Modifier.fillMaxWidth(), color = c.surfaceContainer, radius = 24.dp, onClick = { nav.push("faq") }) {
                    Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                        PwIconTile(Icons.Outlined.QuestionAnswer, pwTone(3), 44.dp)
                        Text("Questions, answered plainly", Modifier.weight(1f), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
                        Icon(Icons.Outlined.ChevronRight, null, tint = c.onSurfaceVariant)
                    }
                }
                PwMono("Figures reviewed ${d.reviewed}. Confirm with the institution.", Modifier.padding(horizontal = 4.dp, vertical = 4.dp), color = c.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun ExploreTile(title: String, sub: String, icon: ImageVector, tone: Int, solid: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val t = pwTone(tone)
    PwSurface(modifier, color = if (solid) t.solid else t.bg, radius = 30.dp, onClick = onClick) {
        Column(Modifier.height(168.dp).padding(18.dp), verticalArrangement = Arrangement.SpaceBetween) {
            Box(Modifier.size(40.dp).clip(RoundedCornerShape(20.dp)).background((if (solid) t.onSolid else t.solid).copy(alpha = 0.16f)), contentAlignment = Alignment.Center) {
                Icon(icon, null, Modifier.size(22.dp), tint = if (solid) t.onSolid else t.fg)
            }
            Column {
                Text(title, color = if (solid) t.onSolid else t.fg, fontWeight = FontWeight.Bold, fontSize = 17.sp, lineHeight = 21.sp)
                Text(sub, color = (if (solid) t.onSolid else t.fg).copy(alpha = 0.8f), style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}
