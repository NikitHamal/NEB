@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val RISK_NAME = mapOf("safe" to "Safe", "mid" to "Balanced", "bold" to "Aim high")

/** Everything the Match tab shows in the Plan list: the intro before the first run, the ranked results after it. */
internal fun LazyListScope.pwMatchItems(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav, r: PwMatchResult?) {
    val s = vm.sel
    fun run(step: Int, edit: Boolean) { s.matchEdit = edit; vm.setNum("mstep", step); nav.push("match") }
    if (vm.num("mdone") == 0) { item("mintro") { MatchIntro(vm.num("mstep")) { run(if (vm.num("mstep") > 1) vm.num("mstep") else 1, false) } }
        if (vm.num("mstep") > 1) item("mover") { Box(Modifier.padding(horizontal = 16.dp)) { QButton("Start over", true, false) { vm.clearMatch(); run(1, false) } } }
        item("mskills") { FlowRow(Modifier.padding(16.dp, 14.dp), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { listOf("Interests", "Strengths", "Budget", "Priorities", "Competition").forEach { PwOutlineChip(it) } } }
        return
    }
    if (r == null) { item("mwait") { Box(Modifier.fillMaxWidth().height(160.dp)) }; return }
    item("mhead") { MatchHead(d, vm, r, ui.district, { vm.clearMatch(); run(1, false) }) { step -> run(step, true) } }
    if (r.good == 0) { item("mnone") { NoMatch(d, vm, r) { step -> run(step, true) } }; return }
    val open = s.matchOpen ?: r.all.firstOrNull()?.route?.id
    if (r.strong.isEmpty()) item("mnote") { MatchNote() }
    fun section(key: String, title: String, list: List<PwMatch>, from: Int) {
        if (list.isEmpty()) return
        item("h$key") { PwH4(title, Modifier.padding(horizontal = 16.dp)) }
        items(list.size, key = { "m${list[it].route.id}" }) { i ->
            val m = list[i]
            PwMatchCard(
                d, m, from + i == 0, open == m.route.id, "route:${m.route.id}" in ui.saved,
                { s.matchOpen = if (open == m.route.id) "" else m.route.id }, { nav.push("route:${m.route.id}") }, { vm.toggleSaved("route:${m.route.id}") },
                Modifier.padding(horizontal = 16.dp, vertical = 4.dp).pwRise(from + i),
            )
        }
    }
    section("s", "Best fit", r.strong, 0)
    section("p", if (r.strong.isEmpty()) "Closest options" else "Worth a look", r.possible, r.strong.size)
    if (r.weak.isNotEmpty()) {
        item("mweak") { WeakToggle(r.weak.size, s.matchWeak) { s.matchWeak = !s.matchWeak } }
        if (s.matchWeak) items(r.weak.size, key = { "w${r.weak[it].route.id}" }) { i ->
            val m = r.weak[i]
            Box(Modifier.padding(horizontal = 16.dp, vertical = 3.dp)) { PwRow(m.route.name, m.neg.joinToString(" · ").ifEmpty { groupLabel(m.route.group) }, "${m.score}", { nav.push("route:${m.route.id}") }, strong = true) }
        }
    }
}

@Composable
private fun MatchIntro(step: Int, onGo: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val prog = step > 1
    Column(Modifier.padding(16.dp, 6.dp, 16.dp, 12.dp).fillMaxWidth().clip(RoundedCornerShape(32.dp)).background(c.primaryContainer).padding(22.dp, 26.dp, 22.dp, 22.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        PwBadge(PwTone(c.onPrimary, c.primary, c.primary, c.onPrimary), 8, 120.dp) { Text("Match", fontSize = 26.sp, fontWeight = FontWeight.Bold, color = c.onPrimary) }
        Text(if (prog) "Pick up where you left off" else "Find the course that fits you", fontSize = 27.sp, lineHeight = 29.sp, fontWeight = FontWeight.Bold, letterSpacing = (-0.8).sp, color = c.onPrimaryContainer)
        Text(
            if (prog) "You are on step $step of 6. Your answers so far are kept." else "Six quick questions, about a minute. We rank every course for your stage by your interests, strengths, budget and goals.",
            fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight.Medium, color = c.onPrimaryContainer.copy(alpha = 0.85f),
        )
        QButton(if (prog) "Continue" else "Start matching", true, true, onClick = onGo)
    }
}

@Composable
private fun MatchHead(d: PwData, vm: PathwaysViewModel, r: PwMatchResult, district: String, retake: () -> Unit, edit: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    val p = pwProfile(d, vm, district)
    val stageLabel = d.stages.firstOrNull { it.id == p.stage }?.label.orEmpty()
    fun names(set: Set<String>, all: List<Pair<String, String>>) = if (set.isEmpty()) "Any" else set.joinToString(", ") { k -> all.firstOrNull { it.first == k }?.second ?: k }
    val chips = listOf(
        1 to "Stage: $stageLabel" + (STREAMS.firstOrNull { it.first == p.knownStream }?.let { " · ${it.second}" } ?: ""), 2 to "Enjoy: ${names(p.interests, INTERESTS)}", 3 to "Good at: ${names(p.strengths, STRENGTHS)}",
        4 to "Care about: ${names(p.priorities, PRIORITIES)}", 5 to "Budget: NPR ${p.budgetLakh}L" + (if (p.maxYears > 0) " · ${p.maxYears} yr" else ""),
        6 to "Style: ${RISK_NAME[p.risk] ?: "Balanced"}",
    )
    Column {
        Row(Modifier.padding(16.dp, 6.dp, 16.dp, 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Column(Modifier.weight(1f)) {
                Text(if (r.good > 0) "Your matches" else "No matches yet", fontSize = 24.sp, lineHeight = 26.sp, fontWeight = FontWeight.Bold, letterSpacing = (-0.7).sp)
                Text("${r.strong.size} strong · ${r.possible.size} possible · ${p.answers} answers", fontSize = 12.5.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
            }
            Box(Modifier.height(40.dp).clip(RoundedCornerShape(20.dp)).background(c.primaryContainer).clickable(onClick = retake).padding(horizontal = 16.dp), contentAlignment = Alignment.Center) {
                Text("Retake", fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = c.onPrimaryContainer)
            }
        }
        PwChipRow(chips.map { it.first.toString() to it.second }, { false }, { k -> edit(k.toInt()) })
    }
}

@Composable
private fun MatchNote() {
    val t = pwTone(2)
    Text("No strong match, but these are the closest. Tap one to see why.", Modifier.padding(16.dp, 10.dp, 16.dp, 0.dp).fillMaxWidth().clip(RoundedCornerShape(20.dp)).background(t.bg).padding(16.dp, 12.dp), color = t.fg, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
}

@Composable
private fun WeakToggle(n: Int, open: Boolean, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val turn by animateFloatAsState(if (open) 90f else 0f, tween(300, easing = FastOutSlowInEasing), label = "weak")
    Row(Modifier.fillMaxWidth().clickable(onClick = onClick).padding(22.dp, 14.dp), verticalAlignment = Alignment.CenterVertically) {
        Text("Not a good fit ($n)", Modifier.weight(1f), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant)
        Icon(Icons.AutoMirrored.Outlined.ArrowForward, null, Modifier.size(18.dp).graphicsLayer { rotationZ = turn }, tint = c.onSurfaceVariant)
    }
}

@Composable
private fun NoMatch(d: PwData, vm: PathwaysViewModel, r: PwMatchResult, edit: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    val p = pwProfile(d, vm, "")
    val cheapest = d.routes.filter { it.stage == p.stage }.minOfOrNull { it.feeMin } ?: 0L
    val tips = buildList {
        if (cheapest > p.budgetLakh * 100_000L) add("Cheapest course here starts at ${npr(cheapest)}. Your budget is NPR ${p.budgetLakh}L.")
        if (p.maxYears > 0) add("You limited study to ${p.maxYears} years. Try any length.")
        if (p.interests.isNotEmpty() && p.strengths.isNotEmpty()) add("Your interests and strengths point in different directions. Try fewer picks.")
        add("Try a different stage, or loosen one answer.")
    }.take(3)
    Column(Modifier.padding(16.dp, 12.dp).fillMaxWidth().clip(RoundedCornerShape(32.dp)).background(c.surfaceContainerLow).padding(18.dp, 30.dp, 18.dp, 22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Box(Modifier.size(84.dp).background(c.surfaceContainerHigh, ScallopShape(6)))
        Text("Nothing fits well", fontSize = 22.sp, fontWeight = FontWeight.Bold, letterSpacing = (-0.4).sp)
        Text("None of the ${r.pool} courses at this stage scored well on your answers.", fontSize = 13.5.sp, lineHeight = 19.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, textAlign = TextAlign.Center)
        tips.forEach { Text(it, Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(c.surfaceContainer).padding(14.dp, 10.dp), fontSize = 13.sp, lineHeight = 17.sp, fontWeight = FontWeight.Medium) }
        QButton("Change budget", true, true) { edit(5) }
        QButton("Try another stage", true, false) { edit(1) }
    }
}
