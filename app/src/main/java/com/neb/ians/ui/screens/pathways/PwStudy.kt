@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.OpenInNew
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
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
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
internal fun PwStudy(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    PwScrollPage(24.dp) {
        PwRootBar { nav.push("search") }
        PwSeg(listOf("colleges" to "Colleges", "abroad" to "Abroad", "funding" to "Funding"), s.study, { s.study = it }, Modifier.padding(16.dp, 8.dp, 16.dp, 14.dp))
        when (s.study) {
            "abroad" -> PwAbroadBody(d, vm)
            "funding" -> PwFundingBody(d, ui, vm)
            else -> PwCollegesBody(d, "", ui, vm)
        }
    }
}

@Composable
internal fun PwCollegesPage(d: PwData, routeId: String, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    PwScrollPage(24.dp) {
        PwBackBar(d.routeById[routeId]?.name ?: "Colleges", nav.pop)
        PwCollegesBody(d, routeId, ui, vm)
    }
}

private fun kindFor(r: PwRoute): String = when {
    r.kind == "Diploma" || r.kind == "Technical" -> "institute"
    r.stage == "afterbach" -> "university"
    else -> "college"
}

@Composable
private fun PwCollegesBody(d: PwData, fixed: String, ui: PathwaysUiState, vm: PathwaysViewModel) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    val withWhere = remember(d) { d.routes.filter { it.where.isNotEmpty() } }
    val rid = listOf(fixed, s.collegeRoute, s.course.orEmpty()).firstOrNull { id -> id.isNotEmpty() && withWhere.any { it.id == id } }
        ?: withWhere.firstOrNull()?.id
    val r = rid?.let { d.routeById[it] }
    if (r == null) { PwEmpty("No colleges yet"); return }
    if (fixed.isEmpty()) {
        val near = remember(r.id, withWhere) { (listOf(r) + withWhere.filter { it.stage == r.stage && it.group == r.group && it.id != r.id }).take(20) }
        PwChipRow(near.map { it.id to it.name }, { it == r.id }, { s.collegeRoute = it }, Modifier.padding(bottom = 14.dp))
    }
    val all = remember(r.id) { r.where.mapNotNull { d.providers[it] } }
    var district by rememberSaveable(r.id) { mutableStateOf("") }
    var sector by rememberSaveable { mutableStateOf("All") }
    val counts = remember(all) { all.groupingBy { it.district }.eachCount() }
    val pickDistrict: (String) -> Unit = { pick ->
        district = if (pick == district) "" else pick
        if (district.isNotEmpty()) vm.setDistrict(district, kindFor(r))
    }
    Column(Modifier.padding(horizontal = 16.dp)) {
        PwNepalMapCard(counts, district, pickDistrict)
        val districts = all.map { it.district }.distinct().sorted()
        if (districts.size > 1 || district.isNotEmpty()) {
            Spacer(Modifier.height(12.dp))
            PwChipRow(districts.map { it to it }, { it == district }, pickDistrict, inset = 0.dp)
        }
        Spacer(Modifier.height(12.dp))
        PwSeg(listOf("All" to "All", "Public" to "Public", "Private" to "Private"), sector, { sector = it })
        Spacer(Modifier.height(12.dp))
        val list = all.filter { p ->
            (district.isEmpty() || p.district == district) && (sector == "All" || p.sector == sector)
        }.sortedWith(compareBy({ if (it.sector == "Public") 0 else 1 }, { it.name }))
        val maxFee = all.mapNotNull { it.fees[r.id]?.second }.maxOrNull()?.coerceAtLeast(1L)?.toFloat()
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            if (list.isEmpty()) PwEmpty("No colleges")
            list.forEach { p ->
                val fee = p.fees[r.id]
                PwSurface(Modifier.fillMaxWidth(), radius = 22.dp, onClick = if (p.website.isNotBlank()) { { runCatching { uri.openUri(p.website) }; Unit } } else null) {
                    Column(Modifier.padding(16.dp, 14.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Column(Modifier.weight(1f)) {
                                Text(p.name, fontSize = 14.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                                Text(
                                    listOf(p.place, p.district, if (p.seats > 0) "${p.seats} seats" else "").filter { it.isNotBlank() }.distinct().joinToString(" · "),
                                    fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis,
                                )
                            }
                            if (p.sector.isNotBlank()) PwTag(p.sector, pwTone(if (p.sector == "Public") 4 else 1))
                        }
                        if (fee != null && maxFee != null) {
                            Spacer(Modifier.height(10.dp))
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                PwBar(fee.second / maxFee, Modifier.weight(1f))
                                Text(npr(fee.second), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }
        if (district.isNotEmpty() && ui.district == district && ui.live.isNotEmpty()) {
            PwH4("Nearby")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) { ui.live.forEach { PwRow(it.name, it.where) } }
        }
    }
}

@Composable
private fun PwAbroadBody(d: PwData, vm: PathwaysViewModel) {
    val s = vm.sel
    val budget = vm.num("abroadBudget")
    Column(Modifier.padding(horizontal = 16.dp)) {
        PwSlider(budget.toFloat(), { vm.setNum("abroadBudget", it.toInt()) }, 5f..100f, 0, "NPR ${budget}L / yr")
        Spacer(Modifier.height(6.dp))
        // an opened card takes a full row; the rest pair up two by two
        val rows = remember(d.abroad, s.abroadOpen) {
            val out = mutableListOf<List<PwAbroad>>()
            var pending: PwAbroad? = null
            d.abroad.forEach { a ->
                if (a.id == s.abroadOpen) out += listOf(a)
                else if (pending == null) pending = a
                else { out += listOfNotNull(pending, a); pending = null }
            }
            pending?.let { out += listOf(it) }
            out
        }
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            rows.forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    row.forEach { a ->
                        val i = d.abroad.indexOf(a)
                        CountryCard(d, a, i, a.id == s.abroadOpen, (a.tuitionMin + a.livingMin) / 100_000 > budget, vm, Modifier.weight(1f))
                    }
                    if (row.size == 1 && row.first().id != s.abroadOpen) Spacer(Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun CountryCard(d: PwData, a: PwAbroad, i: Int, open: Boolean, over: Boolean, vm: PathwaysViewModel, modifier: Modifier) {
    val s = vm.sel
    val tone = pwTone(listOf(0, 1, 2, 4, 5)[i % 5])
    val alpha by animateFloatAsState(if (over && !open) 0.3f else 1f, label = "ccA")
    val months = remember(a.intakes) { monthsIn(a.intakes) }
    PwSurface(
        modifier.graphicsLayer { this.alpha = alpha }.animateContentSize(spring(0.7f, Spring.StiffnessMediumLow)),
        color = tone.bg, radius = if (open) 36.dp else 28.dp, onClick = { s.abroadOpen = if (open) "" else a.id },
    ) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(Modifier.size(48.dp).background(tone.fg, ScallopShape(if (i % 2 == 0) 6 else 8)), contentAlignment = Alignment.Center) {
                    Text(a.code.ifBlank { a.country.take(2) }.uppercase(), color = tone.bg, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
                Column {
                    Text(money(a.tuitionMin + a.livingMin).replace(" lakh", "L"), color = tone.fg, fontSize = 22.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-0.6).sp, lineHeight = 24.sp)
                    Text("per year", color = tone.fg.copy(alpha = 0.75f), fontSize = 10.5.sp, fontWeight = FontWeight.Medium)
                }
            }
            Text(a.country, color = tone.fg, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
            if (months.isNotEmpty()) PwMonths({ it in months }, fill = tone.fg, onFill = tone.bg)
            if (open) {
                val facts = buildList {
                    add("Tuition" to "${money(a.tuitionMin)}–${money(a.tuitionMax)}")
                    add("Living" to "${money(a.livingMin)}–${money(a.livingMax)}")
                    if (a.workHours > 0) add("Work" to "${a.workHours} h / week")
                    if (a.stayBack.isNotBlank()) add("Stay-back" to a.stayBack)
                    if (a.visaRate >= 0) add("Visa rate" to "${a.visaRate}%")
                    if (a.intakes.isNotBlank() && months.isEmpty()) add("Intakes" to a.intakes)
                }
                PwFacts(facts, container = tone.fg.copy(alpha = 0.08f), ink = tone.fg)
                val chips = a.exams + a.fields
                if (chips.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    a.exams.forEach { TonedChip(it, tone, solid = true) }
                    a.fields.forEach { TonedChip(it, tone, solid = false) }
                }
                if (a.scholarships.isNotEmpty()) PwButton("Scholarships", null, true, { s.schCountry = a.id; s.study = "funding" }, Modifier.fillMaxWidth())
            }
        }
    }
}

@Composable
private fun TonedChip(text: String, tone: PwTone, solid: Boolean) {
    Box(
        Modifier.height(32.dp).clip(RoundedCornerShape(16.dp)).background(if (solid) tone.fg else tone.fg.copy(alpha = 0.1f)).padding(horizontal = 12.dp),
        contentAlignment = Alignment.Center,
    ) { Text(text, color = if (solid) tone.bg else tone.fg, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, maxLines = 1) }
}

private fun levelLabel(l: String): String = when (l.lowercase()) {
    "phd" -> "PhD"
    "plus2", "+2" -> "+2"
    else -> l.replaceFirstChar { it.uppercase() }
}

@Composable
private fun PwFundingBody(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    var scope by rememberSaveable { mutableStateOf("All") }
    var level by rememberSaveable { mutableStateOf("All") }
    val country = d.abroad.firstOrNull { it.id == s.schCountry }
    val scopes = remember(d) { d.scholarships.map { it.scope }.filter { it.isNotBlank() }.distinct() }
    val levels = remember(d) { d.scholarships.flatMap { it.levels }.distinct().take(3) }
    val list = d.scholarships.filter { x ->
        (country == null || x.id in country.scholarships || x.country == country.id) &&
            (scope == "All" || x.scope == scope) && (level == "All" || level in x.levels)
    }.sortedWith(compareBy({ if (it.open.size == 2) monthsUntil(it.open[0], it.open[1]) else 99 }, { it.name }))
    val chips = buildList {
        if (country != null) add("x" to country.country)
        add("All" to "All"); scopes.forEach { add(it to levelLabel(it)) }
    }
    PwChipRow(chips, { it == "x" || it == scope }, { k -> if (k == "x") s.schCountry = "" else scope = k }, Modifier.padding(bottom = 10.dp))
    Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        if (levels.size > 1) {
            PwSeg((listOf("All") + levels).map { it to levelLabel(it) }, level, { level = it })
            Spacer(Modifier.height(6.dp))
        }
        if (list.isEmpty()) PwEmpty("No match")
        list.forEach { x ->
            val open = s.schOpen == x.id
            val live = x.open.size == 2 && inWindow(x.open[0], x.open[1], nowMonth())
            PwSurface(Modifier.fillMaxWidth().animateContentSize(), radius = 22.dp, onClick = { s.schOpen = if (open) "" else x.id }) {
                Column(Modifier.padding(16.dp, 14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Column(Modifier.weight(1f)) {
                            Text(x.name, fontSize = 14.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                            Text(x.by, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                        Text(
                            if (x.open.size == 2) windowLabel(x.open[0], x.open[1]) else x.levels.joinToString(", ") { levelLabel(it) },
                            fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = if (live) c.primary else c.onSurfaceVariant, maxLines = 1,
                        )
                    }
                    if (x.open.size == 2) {
                        if (live) PwMonths({ inWindow(x.open[0], x.open[1], it) })
                        else PwMonths({ inWindow(x.open[0], x.open[1], it) }, fill = c.onPrimaryContainer, onFill = c.primaryContainer)
                    }
                    if (open) {
                        listOf("Covers" to x.covers, "Who" to x.who, "How" to x.how).filter { it.second.isNotBlank() }.forEach { (k, v) ->
                            Column {
                                Text(k, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant)
                                Text(v, fontSize = 14.sp, lineHeight = 20.sp)
                            }
                        }
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            if (x.awards > 0) Text("${x.awards} awards", Modifier.weight(1f), fontSize = 13.sp, fontWeight = FontWeight.SemiBold) else Spacer(Modifier.weight(1f))
                            val key = "sch:${x.id}"
                            val saved = key in ui.saved
                            PwIconButton(if (saved) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, "Save", { vm.toggleSaved(key) },
                                if (saved) c.onSurface else c.surfaceContainerHigh, if (saved) c.surface else c.onSurface)
                            if (x.link.isNotBlank()) PwButton("Website", Icons.AutoMirrored.Outlined.OpenInNew, false, { runCatching { uri.openUri(x.link) } })
                        }
                    }
                }
            }
        }
    }
}

