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
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
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
    val showMatch = s.plan == "match" && vm.num("mdone") == 1
    val profile = if (showMatch) pwProfile(d, vm, ui.district) else null
    // ranking a whole stage touches every route and its careers, so it runs off the main thread and only when the answers change
    val result by produceState<PwMatchResult?>(null, d, profile) {
        if (profile != null) value = withContext(Dispatchers.Default) { pwMatch(d, profile) }
    }
    val list = androidx.compose.foundation.lazy.rememberLazyListState()
    Box(Modifier.fillMaxSize()) {
    LazyColumn(Modifier.fillMaxSize(), state = list, contentPadding = PaddingValues(bottom = 24.dp)) {
        item("bar") { PwRootBar { nav.push("search") } }
        item("seg") { PwSeg(listOf("match" to "Match", "plan" to "My plan"), s.plan, { s.plan = it }, Modifier.padding(16.dp, 8.dp, 16.dp, 8.dp)) }
        if (s.plan == "match") pwMatchItems(d, ui, vm, nav, result)
        else item("plan") { MyPlan(d, ui, vm, nav) }
    }
    PwLazyScrim(list)
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
                "sch" -> d.scholarships.firstOrNull { it.id == id }?.let { x -> Triple(x.name, "Scholarship") { s.study = "funding"; s.schCountry = ""; s.schOpen = x.id; nav.tab("study") } }
                "abroad" -> d.abroad.firstOrNull { it.id == id }?.let { a -> Triple(a.country, "Country") { s.study = "abroad"; s.abroadOpen = a.id; nav.tab("study") } }
                "faq" -> d.faq.firstOrNull { it.id == id }?.let { f -> Triple(f.q, "Question") { vm.sel.faqOpen = f.id; nav.tab("guides") } }
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
