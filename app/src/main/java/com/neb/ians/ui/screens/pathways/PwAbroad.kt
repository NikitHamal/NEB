@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material3.Icon
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.roundToInt

private fun lakhs(v: Float): String = if (v >= 10f) "${v.roundToInt()}" else "%.1f".format(v).removeSuffix(".0")

@Composable
private fun Legend() {
    val c = MaterialTheme.colorScheme
    Row(Modifier.padding(bottom = 10.dp), horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.CenterVertically) {
        listOf("Tuition" to c.primary, "Living" to c.outlineVariant).forEach { (t, col) ->
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(10.dp).clip(RoundedCornerShape(3.dp)).background(col))
                Text(t, fontSize = 11.5.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
            }
        }
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(Modifier.width(2.dp).height(12.dp).background(c.onSurface))
            Text("Your budget", fontSize = 11.5.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
        }
    }
}

/** Tuition and living as one bar on a shared scale, with a tick where the student's budget sits. */
@Composable
private fun CostBar(tuition: Float, living: Float, mx: Float, budget: Float) {
    val c = MaterialTheme.colorScheme
    val track = c.surfaceContainerHighest
    Box(
        Modifier.fillMaxWidth().height(10.dp).drawBehind {
            val h = size.height; val w = size.width; val r = CornerRadius(h / 2)
            drawRoundRect(track, size = size, cornerRadius = r)
            val aw = (w * tuition / mx).coerceIn(0f, w); val bw = (w * living / mx).coerceIn(0f, w - aw)
            drawPath(Path().apply { addRoundRect(RoundRect(0f, 0f, aw, h, r, CornerRadius.Zero, CornerRadius.Zero, r)) }, c.primary)
            drawPath(Path().apply { addRoundRect(RoundRect(aw, 0f, aw + bw, h, CornerRadius.Zero, r, r, CornerRadius.Zero)) }, c.outlineVariant)
            drawRoundRect(c.onSurface, Offset(w * budget / mx - 1.dp.toPx(), -3.dp.toPx()), Size(2.dp.toPx(), 16.dp.toPx()), CornerRadius(1.dp.toPx()))
        },
    )
}

@Composable
private fun Detail(k: String, v: String, modifier: Modifier = Modifier) {
    Column(modifier) {
        Text(k, fontSize = 11.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(v, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
    }
}

/** The student visa as a timeline. Tap a step to tick it off; the tick state survives rotation and a restart of the screen. */
@Composable
private fun VisaSteps(v: PwVisa, id: String) {
    val c = MaterialTheme.colorScheme
    var done by rememberSaveable(id) { mutableIntStateOf(0) }
    val n = v.steps.size
    Column {
        Row(Modifier.fillMaxWidth()) {
            Text("Visa steps · ${v.name}", Modifier.weight(1f), fontSize = 11.sp, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Text("${Integer.bitCount(done)}/$n", fontSize = 11.sp, color = c.onSurfaceVariant)
        }
        Spacer(Modifier.height(6.dp))
        v.steps.forEachIndexed { i, s ->
            val on = done and (1 shl i) != 0
            val r by animateDpAsState(if (on) 16.dp else 12.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "vsR")
            val bg by animateColorAsState(if (on) c.primary else c.primaryContainer, label = "vsBg")
            Row(
                Modifier.fillMaxWidth().pwRise(i, id).clip(RoundedCornerShape(12.dp)).clickable { done = done xor (1 shl i) }
                    .drawBehind { if (i < n - 1) drawRect(c.primaryContainer, Offset(15.dp.toPx(), 32.dp.toPx()), Size(2.dp.toPx(), size.height - 32.dp.toPx())) }
                    .padding(bottom = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Box(Modifier.size(32.dp).clip(RoundedCornerShape(r)).background(bg), contentAlignment = Alignment.Center) {
                    if (on) Icon(Icons.Outlined.Check, "Done", Modifier.size(16.dp), tint = c.onPrimary)
                    else Text("${i + 1}", fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = c.onPrimaryContainer)
                }
                Column(Modifier.weight(1f).padding(top = 5.dp).graphicsLayer { alpha = if (on) 0.55f else 1f }) {
                    Text(s.name, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                    val meta = listOfNotNull(if (s.days > 0) "${s.days} ${if (s.days == 1) "day" else "days"}" else null, s.cost.ifBlank { null }, s.mode.ifBlank { null }).joinToString(" · ")
                    if (meta.isNotEmpty()) Text(meta, fontSize = 12.sp, color = c.onSurfaceVariant)
                    if (s.note.isNotBlank()) PwLinkText(s.note, fontSize = 12.sp, lineHeight = 16.sp, color = c.onSurfaceVariant)
                }
            }
        }
    }
}

@Composable
private fun AbroadCard(d: PwData, a: PwAbroad, i: Int, mx: Float, budget: Int, open: Boolean, saved: Boolean, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val t = (a.tuitionMin + a.tuitionMax) / 200_000f
    val l = (a.livingMin + a.livingMax) / 200_000f
    val total = t + l
    val ok = total <= budget
    val fade by animateFloatAsState(if (!ok && !open) 0.6f else 1f, label = "abA")
    val pill = pwTone(if (ok) 4 else 5)
    val months = remember(a.intakes) { monthsIn(a.intakes) }
    PwSurface(
        Modifier.fillMaxWidth().pwRise(i).graphicsLayer { alpha = fade }.animateContentSize(spring(0.8f, Spring.StiffnessMediumLow)),
        radius = 22.dp, onClick = { vm.sel.abroadOpen = if (open) "" else a.id },
    ) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(Modifier.size(40.dp).clip(RoundedCornerShape(12.dp)).background(c.primaryContainer), contentAlignment = Alignment.Center) {
                    Text(a.code.ifBlank { a.country.take(2) }.uppercase(), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = c.onPrimaryContainer)
                }
                Column(Modifier.weight(1f)) {
                    Text(a.country, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Tuition ${lakhs(t)}L + living ${lakhs(l)}L", fontSize = 11.5.sp, color = c.onSurfaceVariant, maxLines = 1)
                }
                Column(horizontalAlignment = Alignment.End) {
                    Text("NPR ${lakhs(total)}L", fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
                    Text("per year", fontSize = 11.5.sp, color = c.onSurfaceVariant)
                }
            }
            CostBar(t, l, mx, budget.toFloat())
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.weight(1f, false).clip(RoundedCornerShape(10.dp)).background(pill.bg).padding(horizontal = 10.dp, vertical = 3.dp)) {
                    Text(if (ok) "Within budget" else "NPR ${lakhs(total - budget)}L over budget", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = pill.fg, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                }
                Spacer(Modifier.weight(1f))
                if (a.visaRate >= 0) Text("Visa approval ${a.visaRate}%", fontSize = 12.sp, color = c.onSurfaceVariant, maxLines = 1)
            }
            if (open) {
                Box(Modifier.fillMaxWidth().height(1.dp).background(c.surfaceContainerHighest))
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Detail("Work allowed", if (a.workHours > 0) "${a.workHours} h / week" else if (a.workHours == 0) "None" else "See notes", Modifier.weight(1f))
                    Detail("Stay after study", a.stayBack.ifBlank { "See notes" }, Modifier.weight(1f))
                }
                if (a.exams.isNotEmpty()) Detail("Entry test", a.exams.joinToString(", "))
                if (a.fields.isNotEmpty()) Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text("Popular fields", fontSize = 11.sp, color = c.onSurfaceVariant)
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        a.fields.forEach { PwOutlineChip(it) }
                    }
                }
                if (a.work.isNotBlank()) Column {
                    Text("Work rules", fontSize = 11.sp, color = c.onSurfaceVariant)
                    PwLinkText(a.work, fontSize = 13.sp, lineHeight = 19.sp, color = c.onSurface)
                }
                if (a.note.isNotBlank()) Column {
                    Text("Visa & funding notes", fontSize = 11.sp, color = c.onSurfaceVariant)
                    PwLinkText(a.note, fontSize = 13.sp, lineHeight = 19.sp, color = c.onSurfaceVariant)
                }
                if (months.isNotEmpty()) Column {
                    Text("Intake months", fontSize = 11.sp, color = c.onSurfaceVariant, modifier = Modifier.padding(bottom = 4.dp))
                    PwMonths({ it in months })
                } else if (a.intakes.isNotBlank()) Detail("Intakes", a.intakes)
                a.visa?.takeIf { it.steps.isNotEmpty() }?.let { VisaSteps(it, a.id) }
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (a.scholarships.isNotEmpty()) PwChip("Scholarships", false, { vm.sel.schCountry = a.id; vm.sel.study = "funding" }, height = 40.dp)
                    Spacer(Modifier.weight(1f))
                    val saveKey = "abroad:${a.id}"
                    PwIconButton(
                        if (saved) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder,
                        "Save",
                        { vm.toggleSaved(saveKey) },
                        if (saved) c.onSurface else c.surfaceContainerHigh,
                        if (saved) c.surface else c.onSurface,
                    )
                }
            }
        }
    }
}

@Composable
internal fun PwAbroadBody(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val budget = vm.num("abroadBudget").coerceIn(5, 60)
    val rows = remember(d.abroad) { d.abroad.sortedBy { (it.tuitionMin + it.tuitionMax + it.livingMin + it.livingMax) / 200_000f } }
    val mx = remember(rows) { maxOf(60f, rows.maxOfOrNull { (it.tuitionMin + it.tuitionMax + it.livingMin + it.livingMax) / 200_000f } ?: 60f) }
    Column(Modifier.padding(horizontal = 16.dp)) {
        Text("Your budget for one year", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        Text("Tuition plus living costs", fontSize = 12.sp, color = c.onSurfaceVariant)
        Spacer(Modifier.height(4.dp))
        PwSlider(budget.toFloat(), { vm.setNum("abroadBudget", (it / 5f).roundToInt() * 5) }, 5f..60f, 10, "NPR ${budget}L")
        Spacer(Modifier.height(6.dp))
        Legend()
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            rows.forEachIndexed { i, a -> AbroadCard(d, a, i, mx, budget, vm.sel.abroadOpen == a.id, "abroad:${a.id}" in ui.saved, vm, nav) }
        }
    }
}
