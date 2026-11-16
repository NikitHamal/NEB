@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
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
internal fun PwCollegesBody(d: PwData, fixed: String, ui: PathwaysUiState, vm: PathwaysViewModel) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    val withWhere = remember(d) { d.routes.filter { it.where.isNotEmpty() } }
    val rid = listOf(fixed, s.collegeRoute, s.course.orEmpty()).firstOrNull { id -> id.isNotEmpty() && withWhere.any { it.id == id } } ?: withWhere.firstOrNull()?.id
    val r = rid?.let { d.routeById[it] }
    if (r == null) { PwEmpty("No colleges yet"); return }
    com.neb.ians.ui.screens.institutions.PwOnNebRow()
    if (fixed.isEmpty()) {
        val near = remember(r.id, withWhere) { (listOf(r) + withWhere.filter { it.stage == r.stage && it.group == r.group && it.id != r.id }).take(20) }
        PwChipRow(near.map { it.id to it.name }, { it == r.id }, { s.collegeRoute = it }, Modifier.padding(bottom = 14.dp))
    }
    val all = remember(r.id) { r.where.mapNotNull { d.providers[it] } }
    val feesHi = remember(all) { all.mapNotNull { it.fees[r.id]?.second } }
    val lo = if (feesHi.isEmpty()) 0f else floor(feesHi.min() / 100_000f)
    val hi = if (feesHi.isEmpty()) 0f else ceil(feesHi.max() / 100_000f).coerceAtLeast(lo + 1f)
    var district by rememberSaveable(r.id) { mutableStateOf("") }
    var cmax by rememberSaveable(r.id) { mutableFloatStateOf(hi) }
    var sort by rememberSaveable { mutableStateOf("fee") }
    var shown by rememberSaveable(r.id) { mutableIntStateOf(30) }
    val counts = remember(all) { all.groupingBy { it.district }.eachCount() }
    Column(Modifier.padding(horizontal = 16.dp)) {
        PwNepalMapCard(counts, district, { name ->
            district = if (name.isEmpty() || name == district) "" else name; shown = 30
            if (district.isNotEmpty()) vm.setDistrict(district, kindFor(r))
        })
        Spacer(Modifier.height(14.dp))
        if (hi > lo) Row(Modifier.padding(bottom = 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            Box(Modifier.weight(1f)) { PwSlider(cmax.coerceIn(lo, hi), { cmax = it; shown = 30 }, lo..hi, 0, lakhText(cmax)) }
            PwSeg(listOf("fee" to "Fee", "seats" to "Seats"), sort, { sort = it }, fill = false, height = 40.dp)
        }
        val inProv = all
        val districts = inProv.map { it.district }.distinct().sorted()
        if (districts.size > 1) PwChipRow(districts.map { it to it }, { it == district }, { district = if (it == district) "" else it; if (district.isNotEmpty()) vm.setDistrict(district, kindFor(r)) }, inset = 0.dp)
        val list = remember(inProv, district, cmax, sort) {
            inProv.filter { p -> (district.isEmpty() || p.district == district) && (p.fees[r.id]?.second?.let { it / 100_000f <= cmax } ?: true) }
                .sortedWith(if (sort == "fee") compareBy({ it.fees[r.id]?.second ?: Long.MAX_VALUE }, { it.name }) else compareBy({ -it.seats }, { it.name }))
        }
        Spacer(Modifier.height(6.dp))
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            if (list.isEmpty()) PwEmpty("No colleges")
            list.take(shown).forEachIndexed { i, p ->
                val fee = p.fees[r.id]?.second
                PwSurface(Modifier.fillMaxWidth().pwRise(i, r.id), radius = 22.dp, onClick = if (p.website.isNotBlank()) { { runCatching { uri.openUri(p.website) }; Unit } } else null) {
                    Column(Modifier.padding(16.dp, 14.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Column(Modifier.weight(1f)) {
                                Text(p.name, fontSize = 14.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                                Text(listOf(p.place, p.district, if (p.seats > 0) "${p.seats} seats" else "").filter { it.isNotBlank() }.distinct().joinToString(" · "),
                                    fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            }
                            if (p.sector.isNotBlank()) PwTag(p.sector, pwTone(if (p.sector == "Public") 4 else 1))
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
        if (district.isNotEmpty() && ui.district == district && ui.live.isNotEmpty()) {
            PwH4("Nearby")
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) { ui.live.forEach { PwRow(it.name, it.where) } }
        }
    }
}
