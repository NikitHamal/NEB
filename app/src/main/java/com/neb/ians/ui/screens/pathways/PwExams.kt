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
import androidx.compose.runtime.remember
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
    val groups = d.govtGroups.filter { g -> tracks.any { it.group == g.id } }.ifEmpty { listOf(PwTopic("gov", "Government")) }
    val group = tracks.firstOrNull { it.id == track }?.group ?: groups.first().id
    val inGroup = tracks.filter { it.group == group }
    val scroll = rememberScrollState()
    androidx.compose.runtime.LaunchedEffect(track) { scroll.scrollTo(0) }
    PwScrollPage(
        bottom = 24.dp,
        state = scroll,
        topBar = { scrolled -> PwRootBar({ nav.push("search") }, nav.pop, scrolled) },
        stickyHeader = if (tracks.isNotEmpty() && (groups.size > 1 || inGroup.size > 1)) ({
            if (groups.size > 1) PwSeg(groups.map { it.id to it.label }, group, { g -> tracks.firstOrNull { it.group == g }?.let { t -> s.track = t.id } }, Modifier.padding(16.dp, 4.dp, 16.dp, if (inGroup.size > 1) 4.dp else 10.dp))
            if (inGroup.size > 1) PwChipRow(inGroup.map { it.id to it.label }, { it == track }, { s.track = it }, Modifier.padding(top = if (groups.size > 1) 2.dp else 4.dp, bottom = 10.dp))
        }) else null,
    ) {
        if (tracks.isEmpty()) { PwEmpty("No exams yet"); return@PwScrollPage }
        Spacer(Modifier.height(8.dp))
        PwSurface(Modifier.padding(16.dp, 0.dp, 16.dp, 12.dp).fillMaxWidth(), radius = 28.dp) {
            Column(Modifier.padding(0.dp, 14.dp, 0.dp, 14.dp)) {
                Text("Eligibility is checked against your profile", Modifier.padding(start = 16.dp, bottom = 10.dp), fontSize = 11.5.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                PwChipRow((1..4).map { "$it" to EDU_LABELS[it] }, { it == "$edu" }, { vm.setNum("edu", it.toInt()) }, inset = 14.dp)
                Row(Modifier.padding(14.dp, 6.dp, 14.dp, 0.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Box(Modifier.weight(1f)) { PwSlider(age.toFloat(), { vm.setNum("age", it.roundToInt()) }, 14f..45f, 30, "Age $age") }
                    if (group == "gov") PwSeg(listOf(1 to "Woman", 0 to "Man"), if (woman) 1 else 0, { vm.setNum("woman", it) }, fill = false, height = 40.dp)
                }
            }
        }
        var filter by rememberSaveable { mutableStateOf("all") }
        var sort by rememberSaveable { mutableStateOf("soon") }
        val now = remember { nowMonth() }
        val all = remember(d, track, edu, age, woman) { d.govt.filter { it.track == track }.map { it to xStatus(it, edu, age, woman, now) } }
        val prepMax = remember(d) { d.govt.maxOfOrNull { prepHoursOf(it) } ?: 1 }
        Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            val ok = all.filter { it.second.kind != "no" }
            val closing = ok.filter { it.second.kind == "open" && it.second.o == 1 && it.first.apply.size == 2 }.minByOrNull { (it.first.apply[1] - now + 12) % 12 }
            val next = closing ?: ok.filter { it.second.o >= 1 }.minByOrNull { it.second.o } ?: ok.firstOrNull()
            if (next != null) PwXNext(next.first, next.second, closing != null) { nav.push("exam:${next.first.id}") }
            PwXYear(MONTHS.indices.map { i -> ok.count { it.first.apply.size == 2 && inWindow(it.first.apply[0], it.first.apply[1], i + 1) } }, now)
            PwXSummary(all.count { it.second.kind == "open" }, all.count { it.second.kind == "soon" }, all.count { it.second.kind == "no" }, filter) { filter = it }
            PwSeg(listOf("soon" to "Soonest", "odds" to "Best odds", "fee" to "Lowest fee"), sort, { sort = it })
            val list = remember(all, filter, sort) {
                all.filter { filter == "all" || it.second.kind == filter }.sortedWith(
                    when (sort) {
                        "odds" -> compareByDescending<Pair<PwGovt, PwXst>> { xOddsScore(it.first).takeIf { s -> s > 0f } ?: 0.5f }
                        "fee" -> compareBy { it.first.fee }
                        else -> compareBy { it.second.o }
                    }
                )
            }
            if (list.isEmpty()) PwEmpty("Nothing here")
            list.forEachIndexed { i, (g, st) -> PwXCard(g, st, prepMax, i) { nav.push("exam:${g.id}") } }
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
        PwHeroScrollPage(
            tone = tone,
            title = g.name,
            sub = g.body,
            saved = key in ui.saved,
            onSave = { vm.toggleSaved(key) },
            onBack = nav.pop,
            bottom = if (career != null) 96.dp else 24.dp,
            badge = {
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
            },
            tabKey = shown,
            aboveTabs = {
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
            },
            stickyTabs = {
                PwTabs(tabs, shown) { tab = it }
            },
        ) {
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
                            PwLinkText(g.note, fontSize = 13.sp, lineHeight = 19.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
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

