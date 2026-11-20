@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.outlined.LocationOn
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.roundToInt

@Composable
internal fun PwRouteDetail(d: PwData, r: PwRoute, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val m = d.m(r)
    val tone = pwTone(groupToneIndex(r.group))
    var tab by rememberSaveable { mutableStateOf("journey") }
    val nextRoute = r.next.firstNotNullOfOrNull { d.routeById[it] }
    val nextStage = nextRoute?.let { n -> d.stages.firstOrNull { it.id == n.stage } }
    val key = "route:${r.id}"
    Box(Modifier.fillMaxSize()) {
        PwHeroScrollPage(
            tone = tone,
            title = r.name,
            sub = listOf(r.kind, groupLabel(r.group)).filter { it.isNotBlank() }.joinToString(" · "),
            saved = key in ui.saved,
            onSave = { vm.toggleSaved(key) },
            onBack = nav.pop,
            bottom = 96.dp,
            badge = {
                val (big, small) = yearsBadge(m.years)
                PwBadge(tone, 8) {
                    Text(big.ifEmpty { "${r.careers.size}" }, fontSize = 22.sp, fontWeight = FontWeight.SemiBold, lineHeight = 24.sp)
                    Text(small.ifEmpty { "careers" }, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, lineHeight = 12.sp)
                }
            },
            aboveTabs = {
                PwMeters(m.demand, m.competition, if (m.payHi > 0) "${money(m.payLo)}–${money(m.payHi)}" else null, "NPR / month to start")
            },
            stickyTabs = {
                PwTabs(listOf("journey" to "Journey", "careers" to "Careers", "cost" to "Cost", "entry" to "Entry", "compare" to "Compare"), tab) { tab = it }
            },
        ) {
            Column(Modifier.padding(16.dp, 18.dp, 16.dp, 20.dp)) {
                when (tab) {
                    "careers" -> RouteCareers(d, r, nav)
                    "cost" -> RouteCost(r, m)
                    "entry" -> RouteEntry(d, r, m, nav)
                    "compare" -> RouteCompare(d, r)
                    else -> RouteOverview(r)
                }
            }
        }
        PwActions(Modifier.align(Alignment.BottomCenter)) {
            if (r.where.isNotEmpty()) PwButton("Colleges", Icons.Outlined.LocationOn, true, { nav.push("colleges:${r.id}") }, Modifier.weight(1f))
            if (nextRoute != null) PwButton(nextStage?.label ?: "Next", Icons.AutoMirrored.Outlined.ArrowForward, false, {
                val s = vm.sel
                s.trail = (s.trail + r.id).distinct()
                s.stage = nextRoute.stage; s.group = nextRoute.group; s.course = null; s.career = null; s.focus = ""
                nav.tab("explore")
            }, Modifier.weight(1f))
        }
    }
}

@Composable
private fun RouteOverview(r: PwRoute) {
    val c = MaterialTheme.colorScheme
    if (r.plan.isNotEmpty()) PwSteps(r.plan.map { Triple(it, "", "") })
    if (r.about.isNotBlank()) {
        PwH4("About")
        PwLinkText(r.about, fontSize = 14.sp, lineHeight = 21.sp, color = c.onSurface)
    }
    if (r.skills.isNotEmpty()) {
        PwH4("Skills")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { r.skills.forEach { PwOutlineChip(it) } }
    }
}

@Composable
private fun RouteCareers(d: PwData, r: PwRoute, nav: PwNav) {
    val cs = r.careers.mapNotNull { d.careers[it] }
    if (cs.isEmpty()) { PwEmpty("No careers listed"); return }
    val max = cs.maxOf { it.seniorMax }.coerceAtLeast(1L).toFloat()
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        cs.forEach { k ->
            PwRow(k.name, trailing = "${money(k.entryMin)}–${money(k.seniorMax)}", onClick = { nav.push("career:${k.id}") }) {
                Spacer(Modifier.height(10.dp))
                PwBar((k.seniorMax - k.entryMin) / max, start = k.entryMin / max)
            }
        }
    }
}

private val LIVING = listOf(0L, 18_000L, 12_000L)

@Composable
private fun RouteCost(r: PwRoute, m: PwMetrics) {
    var priv by rememberSaveable { mutableStateOf(0) }
    var live by rememberSaveable { mutableStateOf(0) }
    var aid by rememberSaveable { mutableStateOf(0f) }
    val years = m.years.coerceAtLeast(1f)
    val tuition = ((if (priv == 1) r.feeMax else r.feeMin) * (1f - aid / 100f)).toLong()
    val living = (LIVING[live] * 12 * years).toLong()
    val books = (15_000L * years).toLong()
    val total = tuition + living + books
    val avgPay = (m.payLo + m.payHi) / 2
    PwSeg(listOf(0 to "Public", 1 to "Private"), priv, { priv = it })
    Spacer(Modifier.height(8.dp))
    PwSeg(listOf(0 to "Home", 1 to "Hostel", 2 to "Room"), live, { live = it })
    Spacer(Modifier.height(4.dp))
    PwSlider(aid, { aid = it }, 0f..100f, 9, "Aid ${aid.roundToInt()}%")
    Spacer(Modifier.height(8.dp))
    PwBig(npr(total), if (avgPay > 0) "${(total / avgPay.toFloat()).roundToInt()} months of starting pay" else null)
    Spacer(Modifier.height(16.dp))
    PwSplit(listOf(PwPart("Tuition", tuition.toFloat()), PwPart("Living", living.toFloat()), PwPart("Books", books.toFloat()))) { npr(it.toLong()) }
}

@Composable
private fun RouteEntry(d: PwData, r: PwRoute, m: PwMetrics, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val exam = d.govtById[r.examId]
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        if (r.entry.isNotBlank()) Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(22.dp)).background(c.primaryContainer).padding(16.dp, 14.dp)) {
            Text("Needs", fontSize = 11.sp, fontWeight = FontWeight.Medium, color = c.onPrimaryContainer.copy(alpha = 0.7f))
            Text(r.entry, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = c.onPrimaryContainer, lineHeight = 21.sp)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (r.exam.isNotBlank()) PwSurface(Modifier.weight(1f).fillMaxHeight(), onClick = exam?.let { e -> { nav.push("exam:${e.id}") } }) {
                Row(Modifier.padding(16.dp, 14.dp), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("Entrance", fontSize = 11.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
                        Text(r.exam, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                    }
                    if (exam != null) Icon(Icons.AutoMirrored.Outlined.ArrowForward, null)
                }
            }
            if (m.years > 0f) Column(Modifier.width(110.dp).clip(RoundedCornerShape(22.dp)).background(c.surfaceContainerLow).padding(16.dp, 14.dp)) {
                Text("Duration", fontSize = 11.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
                Text(yearsText(m.years), fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            }
        }
        if (exam != null && (exam.apply.size == 2 || exam.examMonth > 0)) {
            Spacer(Modifier.height(8.dp))
            PwCalendar(examCalendar(exam))
        }
    }
}

internal fun examCalendar(g: PwGovt): List<Pair<String, (Int) -> Boolean>> = buildList {
    if (g.apply.size == 2) add("Apply" to { m: Int -> inWindow(g.apply[0], g.apply[1], m) })
    if (g.examMonth > 0) add("Exam" to { m: Int -> m == g.examMonth })
}

@Composable
private fun RouteCompare(d: PwData, r: PwRoute) {
    val c = MaterialTheme.colorScheme
    val sib = remember(d, r) {
        val same = d.routes.filter { it.stage == r.stage && it.group == r.group && it.id != r.id }
        (same + d.routes.filter { it.stage == r.stage && it.id != r.id && it !in same }).take(12)
    }
    if (sib.isEmpty()) { PwEmpty("Nothing to compare"); return }
    var pick by rememberSaveable(r.id) { mutableStateOf(sib.first().id) }
    val b = sib.firstOrNull { it.id == pick } ?: sib.first()
    val ma = d.m(r)
    val mb = d.m(b)
    PwChipRow(sib.map { it.id to it.name }, { it == b.id }, { pick = it }, Modifier.padding(bottom = 14.dp), inset = 0.dp)
    Row(Modifier.fillMaxWidth().padding(bottom = 12.dp)) {
        Text(r.name, Modifier.weight(1f), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(b.name, Modifier.weight(1f), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = c.primary, textAlign = TextAlign.End, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
    val rows = listOf(
        Triple("Demand", ma.demand.toFloat(), mb.demand.toFloat()) to "",
        Triple("Competition", ma.competition.toFloat(), mb.competition.toFloat()) to "",
        Triple("Start pay", (ma.payLo + ma.payHi) / 2000f, (mb.payLo + mb.payHi) / 2000f) to "k",
        Triple("Fee", (r.feeMin + r.feeMax) / 200_000f, (b.feeMin + b.feeMax) / 200_000f) to "L",
        Triple("Years", ma.years, mb.years) to "",
    )
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        rows.forEach { (t, unit) ->
            val (label, a, v) = t
            val max = maxOf(a, v).coerceAtLeast(0.01f)
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("${trim(a.toDouble())}$unit", Modifier.width(44.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                Box(Modifier.weight(1f).height(14.dp), contentAlignment = Alignment.CenterEnd) {
                    Box(Modifier.fillMaxWidth(a / max).height(14.dp).clip(RoundedCornerShape(7.dp)).background(c.onSurface))
                }
                Text(label, Modifier.width(86.dp), fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, textAlign = TextAlign.Center, maxLines = 1)
                Box(Modifier.weight(1f).height(14.dp), contentAlignment = Alignment.CenterStart) {
                    Box(Modifier.fillMaxWidth(v / max).height(14.dp).clip(RoundedCornerShape(7.dp)).background(c.primary))
                }
                Text("${trim(v.toDouble())}$unit", Modifier.width(44.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = c.primary, textAlign = TextAlign.End)
            }
        }
    }
}
