@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.ceil
import kotlin.math.min
import kotlin.math.roundToInt

@Composable
internal fun PwExams(d: PwData, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    val tracks = d.govtTracks.filter { t -> d.govt.any { it.track == t.id } }.ifEmpty { d.govt.map { it.track }.distinct().map { PwTopic(it, it) } }
    val track = tracks.firstOrNull { it.id == s.track }?.id ?: tracks.firstOrNull()?.id.orEmpty()
    val edu = vm.num("edu")
    val age = vm.num("age")
    val woman = vm.num("woman") == 1
    PwScrollPage(24.dp) {
        PwRootBar { nav.push("search") }
        if (tracks.isEmpty()) { PwEmpty("No exams yet"); return@PwScrollPage }
        if (tracks.size <= 4) PwSeg(tracks.map { it.id to it.label }, track, { s.track = it }, Modifier.padding(16.dp, 8.dp, 16.dp, 12.dp))
        else PwChipRow(tracks.map { it.id to it.label }, { it == track }, { s.track = it }, Modifier.padding(top = 8.dp, bottom = 12.dp))
        PwChipRow((1..4).map { "$it" to EDU_LABELS[it] }, { it == "$edu" }, { vm.setNum("edu", it.toInt()) })
        Row(Modifier.padding(16.dp, 4.dp, 16.dp, 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(Modifier.weight(1f)) { PwSlider(age.toFloat(), { vm.setNum("age", it.roundToInt()) }, 14f..45f, 30, "Age $age") }
            PwSeg(listOf(1 to "Woman", 0 to "Man"), if (woman) 1 else 0, { vm.setNum("woman", it) }, fill = false, height = 40.dp)
        }
        Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            d.govt.filter { it.track == track }.sortedBy { whyNot(it, edu, age, woman).isNotEmpty() }.forEachIndexed { gi, g ->
                val why = whyNot(g, edu, age, woman)
                val odds = oddsOf(g)
                PwRow(
                    g.name, why.ifEmpty { g.level.ifBlank { g.body } },
                    odds?.text ?: if (g.fee > 0) npr(g.fee) else "",
                    onClick = { nav.push("exam:${g.id}") }, dim = why.isNotEmpty(), strong = true, rise = gi,
                )
            }
        }
    }
}

@Composable
internal fun PwExamDetail(d: PwData, g: PwGovt, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val ti = d.govtTracks.indexOfFirst { it.id == g.track }.coerceAtLeast(0)
    val tone = pwTone(listOf(2, 0, 4, 1)[ti % 4])
    val odds = oddsOf(g)
    var tab by rememberSaveable { mutableStateOf("stages") }
    val tabs = buildList {
        add("stages" to "Stages")
        if (g.syllabus.isNotEmpty() || g.subjects.isNotEmpty()) add("syllabus" to "Syllabus")
        if (odds != null) add("odds" to "Odds")
        add("prepare" to "Prepare")
        if (g.ladder.isNotEmpty()) add("ladder" to "Ladder")
    }
    val shown = if (tabs.any { it.first == tab }) tab else "stages"
    val key = "exam:${g.id}"
    val career = d.careers[g.career]
    Box(Modifier.fillMaxSize()) {
        PwScrollPage(if (career != null) 96.dp else 24.dp) {
            PwHero(tone, g.name, g.body, key in ui.saved, { vm.toggleSaved(key) }, nav.pop) {
                PwBadge(tone, 7) {
                    if (odds != null) {
                        if (odds.pre.isNotEmpty()) Text(odds.pre, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, lineHeight = 12.sp)
                        Text(odds.big, fontSize = 22.sp, fontWeight = FontWeight.SemiBold, lineHeight = 24.sp)
                        if (odds.post.isNotEmpty()) Text(odds.post, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, lineHeight = 12.sp)
                    } else {
                        Text("${g.stages.size}", fontSize = 22.sp, fontWeight = FontWeight.SemiBold, lineHeight = 24.sp)
                        Text("stages", fontSize = 11.sp, fontWeight = FontWeight.SemiBold, lineHeight = 12.sp)
                    }
                }
            }
            val facts = buildList {
                if (g.seats > 0) add("Seats" to money(g.seats.toLong()))
                if (g.applicants > 0) add("Applicants" to money(g.applicants.toLong()))
                if (g.fee > 0) add("Fee" to npr(g.fee))
                if (g.need.isNotBlank()) add("Needs" to eduOf(g.need).let { if (it > 0) EDU_LABELS[it] else g.need })
                if (g.age.isNotBlank()) add("Age" to ageText(g.age))
                if (g.pay > 0) add("Starting pay" to npr(g.pay))
            }
            if (facts.isNotEmpty()) PwFacts(facts, Modifier.padding(16.dp, 16.dp, 16.dp, 4.dp))
            val cal = examCalendar(g)
            if (cal.isNotEmpty()) Box(Modifier.padding(16.dp, 12.dp, 16.dp, 4.dp)) { PwCalendar(cal) }
            Spacer(Modifier.height(12.dp))
            PwTabs(tabs, shown) { tab = it }
            Column(Modifier.padding(16.dp, 18.dp, 16.dp, 20.dp)) {
                when (shown) {
                    "syllabus" -> if (g.syllabus.isNotEmpty()) PwSplit(g.syllabus) else FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp),
                    ) { g.subjects.forEach { PwOutlineChip(it) } }
                    "odds" -> odds?.let { ExamOdds(g, it) }
                    "prepare" -> ExamPrepare(g, vm)
                    "ladder" -> ExamLadder(g)
                    else -> {
                        PwSteps(g.stages.map { Triple(it.name, it.detail, it.marks) })
                        if (g.note.isNotBlank()) {
                            Spacer(Modifier.height(12.dp))
                            Text(g.note, fontSize = 13.sp, lineHeight = 19.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
        if (career != null) PwActions(Modifier.align(Alignment.BottomCenter)) {
            PwButton(career.name, Icons.AutoMirrored.Outlined.ArrowForward, true, { nav.push("career:${career.id}") }, Modifier.weight(1f))
        }
    }
}

@Composable
private fun ExamOdds(g: PwGovt, odds: PwOdds) {
    val c = MaterialTheme.colorScheme
    PwBigLine(odds.text)
    // one dot per applicant for a seat; the lit dot is you
    val one = odds.ratio >= 20f
    val n = if (one) min(odds.ratio.roundToInt(), 400) else 100
    val lit = if (one) 1 else odds.big.toIntOrNull() ?: 0
    val rows = ceil(n / 25f).toInt().coerceAtLeast(1)
    Canvas(Modifier.fillMaxWidth().aspectRatio(25f / rows)) {
        val cell = size.width / 25f
        val me = (n * 0.37f).toInt()
        for (i in 0 until n) {
            val center = Offset(cell * (i % 25) + cell / 2, cell * (i / 25) + cell / 2)
            val on = if (one) i == me else i < lit
            drawCircle(if (on) c.primary else c.surfaceContainerHighest, cell * (if (one && on) 0.5f else 0.36f), center)
        }
    }
    if (g.quota.isNotEmpty()) {
        PwH4("Seats by category")
        PwSplit(g.quota)
    }
}

@Composable
private fun ExamPrepare(g: PwGovt, vm: PathwaysViewModel) {
    val hours = vm.num("hours").coerceIn(1, 10)
    val days = ceil(prepHoursOf(g) / hours.toFloat()).toInt()
    PwBigLine("$hours", "h a day")
    PwSlider(hours.toFloat(), { vm.setNum("hours", it.roundToInt()) }, 1f..10f, 8, "")
    Spacer(Modifier.height(8.dp))
    val startBy = if (g.examMonth > 0) MONTHS[((g.examMonth - 1 - ceil(days / 30f).toInt()) % 12 + 12) % 12] else null
    PwBig("$days days", startBy?.let { "Start by $it" })
    val parts = g.syllabus.ifEmpty { g.subjects.map { PwPart(it, 1f) } }
    if (parts.isNotEmpty()) {
        PwH4("Hours a week")
        val total = parts.sumOf { it.value.toDouble() }.toFloat().coerceAtLeast(0.01f)
        val max = parts.maxOf { it.value }.coerceAtLeast(0.01f)
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            parts.forEach { p ->
                PwRow(p.label, trailing = "${trim((hours * 7 * p.value / total).toDouble())} h") {
                    Spacer(Modifier.height(10.dp))
                    PwBar(p.value / max)
                }
            }
        }
    }
    if (g.prep.isNotEmpty()) {
        PwH4("Checklist")
        PwSteps(g.prep.map { Triple(it, "", "") }, { vm.has("done", "prep:${g.id}:$it") }) { vm.toggle("done", "prep:${g.id}:$it") }
    }
}

@Composable
private fun ExamLadder(g: PwGovt) {
    val c = MaterialTheme.colorScheme
    val n = g.ladder.size
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        g.ladder.indices.reversed().forEach { i ->
            val p = g.ladder[i]
            val on = i == g.rung
            Row(
                Modifier.fillMaxWidth(if (n > 1) 0.55f + 0.45f * i / (n - 1) else 1f).height(48.dp)
                    .clip(RoundedCornerShape(if (on) 24.dp else 16.dp))
                    .background(if (on) c.primary else c.surfaceContainerHigh).padding(horizontal = 18.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                val ink = if (on) c.onPrimary else c.onSurface.copy(alpha = if (g.rung >= 0 && i < g.rung) 0.45f else 1f)
                Text(p.label, Modifier.weight(1f), color = ink, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
                if (p.value > 0f) Text(npr(p.value.toLong()), color = ink, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
            }
        }
    }
}

