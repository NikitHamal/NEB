@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.ceil
import kotlin.math.floor

/** "NPR 4.5L", "NPR 80k" or "Free": a fee given in lakh (one lakh = 100,000 rupees). */
internal fun lakhText(v: Float): String {
    if (v <= 0f) return "Free"
    if (v < 1f) return "NPR ${(v * 100).toInt()}k"
    val t = if (v % 1f == 0f || v >= 10f) "${v.toInt()}" else "%.1f".format(v)
    return "NPR ${t}L"
}

private fun kindFor(r: PwRoute): String = when {
    r.kind == "Diploma" || r.kind == "Technical" -> "institute"
    r.stage == "afterbach" -> "university"
    else -> "college"
}

@Composable
internal fun PwCollegesBody(d: PwData, fixed: String, ui: PathwaysUiState, vm: PathwaysViewModel, showRouteChips: Boolean = true) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    val openInst = com.neb.ians.ui.screens.institutions.LocalOpenInstitution.current
    val withWhere = remember(d) { d.routes.filter { it.where.isNotEmpty() } }
    val rid = listOf(fixed, s.collegeRoute, s.course.orEmpty()).firstOrNull { id -> id.isNotEmpty() && withWhere.any { it.id == id } } ?: withWhere.firstOrNull()?.id
    val r = rid?.let { d.routeById[it] }
    if (r == null) { PwEmpty("No colleges yet"); return }
    val matches = ui.onNeb?.matches.orEmpty()
    PwOnNebSection(ui.onNeb, remember(r.id, matches) { r.where.mapNotNull { matches[it] }.toSet() }, ui.district)
    if (fixed.isEmpty() && showRouteChips) {
        val near = remember(r.id, withWhere) { (listOf(r) + withWhere.filter { it.stage == r.stage && it.group == r.group && it.id != r.id }).take(20) }
        PwChipRow(near.map { it.id to it.name }, { it == r.id }, { s.collegeRoute = it }, Modifier.padding(bottom = 14.dp))
    }
    val all = remember(r.id) { r.where.mapNotNull { d.providers[it] } }
    val feesHi = remember(all) { all.mapNotNull { it.fees[r.id]?.second } }
    val lo = if (feesHi.isEmpty()) 0f else floor(feesHi.min() / 100_000f)
    val hi = if (feesHi.isEmpty()) 0f else ceil(feesHi.max() / 100_000f).coerceAtLeast(lo + 1f)
    var district by rememberSaveable(r.id) { mutableStateOf(ui.district) }
    var filterQ by rememberSaveable(r.id) { mutableStateOf("") }
    LaunchedEffect(ui.district) {
        if (district.isEmpty() && ui.district.isNotEmpty()) district = ui.district
    }
    LaunchedEffect(district, r.id) {
        if (district.isNotEmpty()) vm.setDistrict(district, kindFor(r))
    }
    var cmax by rememberSaveable(r.id) { mutableFloatStateOf(hi) }
    var sort by rememberSaveable { mutableStateOf("fee") }
    var shown by rememberSaveable(r.id) { mutableIntStateOf(30) }
    val isPlus2 = r.id.startsWith("plus2") || r.stage == "after10"
    val counts = remember(all, isPlus2, ui.plus2Counts) {
        val base = all.groupingBy { it.district }.eachCount()
        if (isPlus2 && ui.plus2Counts.isNotEmpty()) {
            (base.keys + ui.plus2Counts.keys).associateWith { k -> maxOf(base[k] ?: 0, ui.plus2Counts[k] ?: 0) }
        } else base
    }
    Column(Modifier.padding(horizontal = 16.dp)) {
        PwNepalMapCard(counts, district, { name ->
            district = if (name.isEmpty() || name == district) "" else name; shown = 30
            if (district.isNotEmpty()) vm.setDistrict(district, kindFor(r)) else vm.setDistrict("", "")
        })
        Spacer(Modifier.height(14.dp))
        androidx.compose.foundation.text.BasicTextField(
            value = filterQ,
            onValueChange = { filterQ = it; shown = 30 },
            singleLine = true,
            textStyle = MaterialTheme.typography.bodyMedium.copy(color = c.onSurface, fontWeight = FontWeight.Medium),
            cursorBrush = androidx.compose.ui.graphics.SolidColor(c.primary),
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 10.dp)
                .height(44.dp)
                .background(c.surfaceContainerLow, RoundedCornerShape(22.dp))
                .padding(horizontal = 16.dp),
            decorationBox = { inner ->
                Box(contentAlignment = Alignment.CenterStart) {
                    if (filterQ.isEmpty()) Text("Filter by college, town or NEB code", color = c.onSurfaceVariant, fontSize = 13.5.sp)
                    inner()
                }
            }
        )
        if (hi > lo) Row(Modifier.padding(bottom = 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            Box(Modifier.weight(1f)) { PwSlider(cmax.coerceIn(lo, hi), { cmax = it; shown = 30 }, lo..hi, 0, lakhText(cmax)) }
            PwSeg(listOf("fee" to "Fee", "seats" to "Seats"), sort, { sort = it }, fill = false, height = 40.dp)
        }
        val inProv = all
        val districts = remember(inProv, isPlus2, ui.plus2Counts) {
            if (isPlus2 && ui.plus2Counts.isNotEmpty()) (inProv.map { it.district } + ui.plus2Counts.keys).distinct().sorted()
            else inProv.map { it.district }.distinct().sorted()
        }
        if (districts.size > 1) PwChipRow(districts.map { it to it }, { it == district }, { district = if (it == district) "" else it; if (district.isNotEmpty()) vm.setDistrict(district, kindFor(r)) else vm.setDistrict("", "") }, inset = 0.dp)
        val needle = filterQ.trim().lowercase()
        val list = remember(inProv, district, cmax, sort, matches, needle) {
            inProv.filter { p ->
                (district.isEmpty() || p.district == district) &&
                    (p.fees[r.id]?.second?.let { it / 100_000f <= cmax } ?: true) &&
                    (needle.isEmpty() || "${p.name} ${p.place} ${p.district}".lowercase().contains(needle))
            }
                .sortedWith(if (sort == "fee") compareBy<PwProvider>({ if (it.id in matches) 0 else 1 }, { it.fees[r.id]?.second ?: Long.MAX_VALUE }, { it.name }) else compareBy<PwProvider>({ if (it.id in matches) 0 else 1 }, { -it.seats }, { it.name }))
        }
        Spacer(Modifier.height(6.dp))
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            if (list.isEmpty() && (!isPlus2 || district.isEmpty() || ui.plus2Schools.isEmpty())) {
                PwEmpty(if (isPlus2 && district.isEmpty()) "Tap a district on the map to see all NEB +2 schools" else "No colleges")
            }
            list.take(shown).forEachIndexed { i, p ->
                val fee = p.fees[r.id]?.second
                PwSurface(Modifier.fillMaxWidth().pwRise(i, r.id), radius = 22.dp, onClick = if (p.id in matches) { { openInst(matches.getValue(p.id)) } } else if (p.website.isNotBlank()) { { runCatching { uri.openUri(p.website) }; Unit } } else null) {
                    Column(Modifier.padding(16.dp, 14.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Column(Modifier.weight(1f)) {
                                Text(p.name, fontSize = 14.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                                Text(listOf(p.place, p.district, if (p.seats > 0) "${p.seats} seats" else "").filter { it.isNotBlank() }.distinct().joinToString(" · "),
                                    fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            }
                            if (p.id in matches) PwTag("On NEBians", pwTone(0))
                            else if (p.sector.isNotBlank()) PwTag(p.sector, pwTone(if (p.sector == "Public") 4 else 1))
                        }
                        if (p.note.isNotBlank()) {
                            Spacer(Modifier.height(4.dp))
                            Text(p.note, fontSize = 12.sp, lineHeight = 16.sp, color = c.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis)
                        }
                        if (fee != null && hi > 0f) {
                            Spacer(Modifier.height(8.dp))
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                PwBar((fee / 100_000f) / hi, Modifier.weight(1f))
                                Text(lakhText(fee / 100_000f), fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                            }
                        }
                    }
                }
            }
            if (list.size > shown) PwButton("Show ${minOf(30, list.size - shown)} more", null, false, { shown += 30 }, Modifier.fillMaxWidth())
        }
        val filteredPlus2 = remember(ui.plus2Schools, needle) {
            if (needle.isEmpty()) ui.plus2Schools
            else ui.plus2Schools.filter { "${it.name} ${it.nameNe} ${it.address} ${it.code}".lowercase().contains(needle) }
        }
        if (isPlus2 && district.isNotEmpty() && ui.district == district && filteredPlus2.isNotEmpty()) {
            PwH4("NEB +2 schools in $district (${if (needle.isEmpty()) ui.plus2Total else filteredPlus2.size})")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                filteredPlus2.take(shown).forEach { sc ->
                    PwSurface(Modifier.fillMaxWidth(), radius = 20.dp) {
                        Row(Modifier.padding(14.dp, 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                            Column(Modifier.weight(1f)) {
                                Text(sc.name, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                                val sub = listOf(sc.nameNe, sc.address, sc.district).filter { it.isNotBlank() }.distinct().joinToString(" · ")
                                if (sub.isNotBlank()) Text(sub, fontSize = 12.sp, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            }
                            if (sc.code.isNotBlank()) PwTag("NEB ${sc.code}", pwTone(1))
                        }
                    }
                }
                if (filteredPlus2.size > shown) PwButton("Show more +2 schools", null, false, { shown += 30 }, Modifier.fillMaxWidth())
            }
        }
        if (district.isNotEmpty() && ui.district == district && ui.live.isNotEmpty()) {
            PwH4("Nearby")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) { ui.live.forEach { PwRow(it.name, it.where) } }
        }
    }
}
