@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.ceil
import kotlin.math.roundToInt

private data class PwDeadline(val key: String, val name: String, val from: Int, val to: Int, val open: () -> Unit)

@Composable
internal fun PwPlan(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    val matchStage = d.stages.firstOrNull { it.id == s.matchStage }?.id ?: d.stages.firstOrNull { it.id == s.stage }?.id ?: d.stages.firstOrNull()?.id.orEmpty()
    val profile = PwProfile(matchStage, vm.set("interests"), vm.set("strengths"), vm.num("budget"), vm.set("priorities"), ui.district)
    val matches = remember(d, profile) { pwMatch(d, profile) }
    val list = androidx.compose.foundation.lazy.rememberLazyListState()
    Box(Modifier.fillMaxSize()) {
    LazyColumn(Modifier.fillMaxSize(), state = list, contentPadding = PaddingValues(bottom = 24.dp)) {
        item("bar") { PwRootBar { nav.push("search") } }
        item("seg") { PwSeg(listOf("plan" to "My plan", "match" to "Match"), s.plan, { s.plan = it }, Modifier.padding(16.dp, 8.dp, 16.dp, 8.dp)) }
        if (s.plan == "match") {
            item("controls") { MatchControls(d, vm, matchStage) }
            if (matches.isEmpty()) item("none") { PwEmpty("No courses at this stage") }
            items(matches, key = { it.route.id }) { m ->
                Box(Modifier.animateItem().padding(horizontal = 16.dp, vertical = 3.dp)) {
                    MatchRow(m, m === matches.first()) { nav.push("route:${m.route.id}") }
                }
            }
        } else {
            item("plan") { MyPlan(d, ui, vm, nav) }
        }
    }
    PwLazyScrim(list)
    }
}

@Composable
private fun MatchControls(d: PwData, vm: PathwaysViewModel, stage: String) {
    val s = vm.sel
    Column {
        PwChipRow(d.stages.map { it.id to it.label }, { it == stage }, { s.matchStage = it }, Modifier.padding(top = 8.dp))
        Column(Modifier.padding(horizontal = 16.dp)) {
            listOf(Triple("I enjoy", "interests", INTERESTS), Triple("I am strong in", "strengths", STRENGTHS), Triple("I care about", "priorities", PRIORITIES)).forEach { (title, set, opts) ->
                PwBigLine(title, modifier = Modifier.padding(top = 12.dp))
                FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    opts.forEach { (k, label) -> PwChip(label, vm.has(set, k), { vm.toggle(set, k) }) }
                }
            }
            val budget = vm.num("budget")
            PwBigLine("My budget is", "NPR ${budget}L", Modifier.padding(top = 12.dp))
            PwSlider(budget.toFloat(), { vm.setNum("budget", it.roundToInt()) }, 1f..60f, 0, "")
            Spacer(Modifier.height(8.dp))
        }
    }
}

@Composable
private fun MatchRow(m: PwMatch, top: Boolean, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val bg = if (top) c.primaryContainer else c.surfaceContainerLow
    val fg = if (top) c.onPrimaryContainer else c.onSurface
    PwSurface(Modifier.fillMaxWidth(), color = bg, radius = 24.dp, onClick = onClick) {
        Row(Modifier.padding(12.dp, 10.dp, 16.dp, 10.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            PwRing(m.score, null, 46.dp, fg, fg.copy(alpha = 0.14f), fg)
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(m.route.name, color = fg, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                if (m.reasons.isNotEmpty()) Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    m.reasons.forEach { r ->
                        Box(Modifier.clip(RoundedCornerShape(8.dp)).background(fg.copy(alpha = 0.1f)).padding(horizontal = 8.dp, vertical = 2.dp)) {
                            Text(r, color = fg, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
                        }
                    }
                }
            }
            Icon(Icons.AutoMirrored.Outlined.ArrowForward, null, tint = fg)
        }
    }
}

@Composable
private fun MyPlan(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val age = vm.num("age")
    val route = (s.trail + listOfNotNull(s.course)).distinct().mapNotNull { d.routeById[it] }
    Column(Modifier.padding(horizontal = 16.dp)) {
        PwBigLine("I am", "$age")
        PwSlider(age.toFloat(), { vm.setNum("age", it.roundToInt()) }, 13f..40f, 0, "")
        if (route.isNotEmpty()) {
            val last = route.last()
            val career = d.careers[s.career?.takeIf { it in last.careers } ?: last.careers.firstOrNull().orEmpty()]
            val years = route.sumOf { d.m(it).years.toDouble() }.toFloat()
            val end = ceil(age + years).toInt()
            val tone = pwTone(0)
            Column(Modifier.fillMaxWidth().padding(top = 14.dp).clip(RoundedCornerShape(32.dp)).background(tone.bg).padding(20.dp)) {
                Text("${career?.name ?: last.name} at $end", color = tone.fg, fontSize = 20.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.4).sp, lineHeight = 22.sp)
                Row(Modifier.fillMaxWidth().padding(vertical = 14.dp).height(56.dp), horizontalArrangement = Arrangement.spacedBy(3.dp)) {
                    route.forEachIndexed { i, r ->
                        PwSurface(
                            Modifier.weight(d.m(r).years.coerceAtLeast(0.5f)).height(56.dp),
                            color = tone.fg.copy(alpha = 0.1f), radius = if (i == 0) 28.dp else 10.dp, onClick = { nav.push("route:${r.id}") },
                        ) {
                            Column(Modifier.padding(horizontal = 12.dp), verticalArrangement = Arrangement.Center) {
                                Text(r.name, color = tone.fg, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                Text(yearsText(d.m(r).years), color = tone.fg.copy(alpha = 0.75f), fontSize = 10.5.sp, fontWeight = FontWeight.Medium, maxLines = 1)
                            }
                        }
                    }
                    Box(Modifier.height(56.dp).clip(RoundedCornerShape(topStart = 10.dp, bottomStart = 10.dp, topEnd = 28.dp, bottomEnd = 28.dp)).background(tone.fg).padding(horizontal = 18.dp), contentAlignment = Alignment.Center) {
                        Text("$end", color = tone.bg, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
                PwFacts(
                    buildList {
                        add("Years" to trim(years.toDouble()))
                        add("Cost" to "${money(route.sumOf { it.feeMin })}–${money(route.sumOf { it.feeMax })}")
                        if (career != null) add("First pay" to npr(career.entryMin))
                    },
                    container = tone.fg.copy(alpha = 0.08f), ink = tone.fg,
                )
            }
        }

        val deadlines = buildList {
            route.mapNotNull { d.govtById[it.examId] }.forEach { g -> if (g.apply.size == 2) add(PwDeadline("exam:${g.id}", g.name, g.apply[0], g.apply[1]) { nav.push("exam:${g.id}") }) }
            ui.saved.forEach { k ->
                val id = k.substringAfter(":")
                when (k.substringBefore(":")) {
                    "exam" -> d.govtById[id]?.takeIf { it.apply.size == 2 }?.let { g -> add(PwDeadline(k, g.name, g.apply[0], g.apply[1]) { nav.push("exam:${g.id}") }) }
                    "sch" -> d.scholarships.firstOrNull { it.id == id && it.open.size == 2 }?.let { x ->
                        add(PwDeadline(k, x.name, x.open[0], x.open[1]) { s.study = "funding"; s.schCountry = ""; s.schOpen = x.id; nav.tab("study") })
                    }
                }
            }
        }.distinctBy { it.key }.sortedBy { monthsUntil(it.from, it.to) }
        if (deadlines.isNotEmpty()) {
            PwH4("Deadlines")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                deadlines.forEach { dl ->
                    val live = inWindow(dl.from, dl.to, nowMonth())
                    PwRow(dl.name, trailing = windowLabel(dl.from, dl.to), onClick = dl.open) {
                        Spacer(Modifier.height(10.dp))
                        if (live) PwMonths({ inWindow(dl.from, dl.to, it) })
                        else PwMonths({ inWindow(dl.from, dl.to, it) }, fill = c.onPrimaryContainer, onFill = c.onPrimaryContainer, cellBg = c.primaryContainer)
                    }
                }
            }
        }

        val guides = d.guides.filter { "guide:${it.id}" in ui.saved || guideDone(vm, it) > 0 }
        if (guides.isNotEmpty()) {
            PwH4("Guides")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                guides.forEach { g ->
                    val done = guideDone(vm, g)
                    PwRow(g.name, trailing = "$done of ${g.steps.size}", onClick = { nav.push("guide:${g.id}") }) {
                        Spacer(Modifier.height(10.dp))
                        PwBar(if (g.steps.isEmpty()) 0f else done / g.steps.size.toFloat())
                    }
                }
            }
        }

        val saved = ui.saved.mapNotNull { k ->
            val id = k.substringAfter(":")
            when (k.substringBefore(":")) {
                "route" -> d.routeById[id]?.let { Triple(it.name, "Course") { nav.push(k) } }
                "career" -> d.careers[id]?.let { Triple(it.name, "Career") { nav.push(k) } }
                "exam" -> d.govtById[id]?.let { Triple(it.name, "Exam") { nav.push(k) } }
                else -> null
            }
        }
        if (saved.isNotEmpty()) {
            PwH4("Saved")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) { saved.forEach { (name, kind, go) -> PwRow(name, trailing = kind, onClick = go) } }
        }

        if (route.isEmpty() && deadlines.isEmpty() && guides.isEmpty() && saved.isEmpty()) {
            PwEmpty("Nothing planned")
            PwButton("Explore", Icons.AutoMirrored.Outlined.ArrowForward, true, { nav.tab("explore") }, Modifier.fillMaxWidth())
        }
    }
}
