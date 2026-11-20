@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.util.Calendar
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.roundToInt
import kotlin.math.sin

@Composable
internal fun PwCareerDetail(d: PwData, k: PwCareer, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val tone = pwTone(3)
    var tab by rememberSaveable { mutableStateOf("pay") }
    var exp by rememberSaveable { mutableStateOf(3) }
    val ladder = k.ladder.ifEmpty { listOf("Entry", "Mid-level", "Senior", "Lead") }
    val starts = rungStarts(ladder.size)
    val rung = starts.indexOfLast { it <= exp }.coerceAtLeast(0)
    val key = "career:${k.id}"
    PwHeroScrollPage(
        tone = tone,
        title = k.name,
        sub = "NPR ${money(k.entryMin)}\u2013${money(k.seniorMax)} / month",
        saved = key in ui.saved,
        onSave = { vm.toggleSaved(key) },
        onBack = nav.pop,
        bottom = 32.dp,
        badge = { PwBadge(tone, 5) { PwSignal(pct(k.demand), tone.bg, 34.dp) } },
    ) {
        PwMeters(pct(k.demand), pct(k.competition), "NPR ${money(payAt(k, exp.toFloat()).toLong())}", "${if (exp == 0) "Entry" else "Year $exp"} \u00b7 ${ladder[rung]}")
        PwTabs(listOf("pay" to "Pay", "profile" to "Profile", "skills" to "Skills", "market" to "Market"), tab) { tab = it }
        Column(Modifier.padding(16.dp, 18.dp, 16.dp, 20.dp)) {
            when (tab) {
                "profile" -> CareerProfile(d, k)
                "skills" -> CareerSkills(d, k, vm, nav)
                "market" -> CareerMarket(d, k, nav)
                else -> PwPayLadder(k, ladder, exp) { exp = it }
            }
        }
    }
}

@Composable
private fun CareerProfile(d: PwData, k: PwCareer) {
    PwRadar(d, k)
    if (k.day.isNotEmpty()) {
        PwH4(if (k.hours > 0) "A ${k.hours}-hour week" else "A week")
        PwSplit(k.day)
    }
    if (k.about.isNotBlank()) {
        PwH4("About")
        PwLinkText(k.about, fontSize = 15.sp, lineHeight = 23.sp)
    }
}

@Composable
private fun CareerSkills(d: PwData, k: PwCareer, vm: PathwaysViewModel, nav: PwNav) {
    val skills = k.skills.ifEmpty { d.careerRoutes[k.id].orEmpty().flatMap { it.skills }.distinct().take(8) }
    if (skills.isNotEmpty()) {
        val have = skills.count { vm.has("have", it) }
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            PwRing((have * 100f / skills.size).roundToInt(), "Ready")
            FlowRow(Modifier.weight(1f), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                skills.forEach { s -> PwChip(s, vm.has("have", s), { vm.toggle("have", s) }) }
            }
        }
    }
    if (k.licence.isNotBlank()) {
        PwH4("Licence")
        val exam = d.govtById[k.licenceExam]
        PwRow(k.licence, exam?.body.orEmpty(), if (exam != null) "Exam" else "", onClick = exam?.let { e -> { nav.push("exam:${e.id}") } })
    }
    val routes = d.careerRoutes[k.id].orEmpty()
    if (routes.isNotEmpty()) {
        PwH4("Routes in")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            routes.forEach { r -> PwChip(r.name, false, { nav.push("route:${r.id}") }) }
        }
    }
}

@Composable
private fun CareerMarket(d: PwData, k: PwCareer, nav: PwNav) {
    if (k.history.size >= 3) {
        val year = remember { Calendar.getInstance().get(Calendar.YEAR) }
        PwH4("Demand, ${k.history.size} years")
        PwSpark(k.history.map { pct(it).toFloat() }, year)
    }
    PwH4("Your chances")
    PwMarket(d, k, nav)
    if (k.jobs.isNotEmpty()) {
        PwH4("Where the jobs are")
        PwSplit(k.jobs)
    }
    if (k.employers.isNotEmpty()) {
        PwH4("Employers")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { k.employers.forEach { PwOutlineChip(it) } }
    }
}
