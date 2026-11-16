package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.runtime.getValue
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.log10
import kotlin.math.max
import kotlin.math.min

/** Where one exam stands for the person asking: not eligible, open, or opening later. `o` orders by how soon. */
internal data class PwXst(val kind: String, val text: String, val sub: String, val o: Int)

internal fun xStatus(g: PwGovt, edu: Int, age: Int, woman: Boolean, now: Int): PwXst {
    val w = whyNot(g, edu, age, woman)
    if (w.isNotEmpty()) return PwXst("no", "Not eligible", w, 100)
    if (g.apply.size != 2) return PwXst("open", "Dates vary", "Check the notice", 60)
    val (a, b) = g.apply
    if (a == 1 && b == 12) return PwXst("open", "Open all year", "Book any month", 0)
    if (inWindow(a, b, now)) return PwXst("open", "Open now", "Closes ${MONTHS[b - 1]}", 1)
    val n = (a - now + 12) % 12
    return PwXst("soon", if (n <= 2) "Opens soon" else "Opens ${MONTHS[a - 1]}", "In $n ${if (n == 1) "month" else "months"}", 1 + n)
}

internal fun xOddsScore(g: PwGovt): Float =
    if (g.seats > 0 && g.applicants > 0) max(0.06f, min(1f, (log10(g.seats.toFloat() / g.applicants) + 3f) / 3f)) else 0f

@Composable
internal fun pwNoTone(): PwTone { val c = MaterialTheme.colorScheme; return PwTone(c.surfaceContainerHighest, c.onSurfaceVariant, c.outline, c.surface) }

@Composable
internal fun xTone(kind: String): PwTone = when (kind) { "open" -> pwTone(4); "soon" -> pwTone(2); else -> pwNoTone() }

/** The big "next" card: what closes next, or what opens next. */
@Composable
internal fun PwXNext(g: PwGovt, st: PwXst, closing: Boolean, onClick: () -> Unit) {
    val t = pwTone(0)
    val odds = oddsOf(g)
    PwSurface(Modifier.fillMaxWidth(), color = t.bg, radius = 32.dp, onClick = onClick) {
        Column(Modifier.padding(20.dp, 20.dp, 20.dp, 18.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(if (closing) "Closing next" else "Opens next", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = t.fg.copy(alpha = 0.75f))
            Text(g.name, fontSize = 26.sp, fontWeight = FontWeight.SemiBold, lineHeight = 28.sp, color = t.fg)
            Text(g.body, fontSize = 13.sp, fontWeight = FontWeight.Medium, color = t.fg.copy(alpha = 0.8f))
            if (g.apply.size == 2) { androidx.compose.foundation.layout.Spacer(Modifier.height(4.dp)); PwMonths({ m -> inWindow(g.apply[0], g.apply[1], m) }, fill = t.solid, onFill = t.onSolid) }
            @OptIn(ExperimentalLayoutApi::class)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                val facts = listOfNotNull(st.text, if (g.fee > 0) npr(g.fee) else null, if (g.examMonth > 0) "Exam ${MONTHS[g.examMonth - 1]}" else null, odds?.text)
                facts.forEach { f ->
                    Text(f, Modifier.clip(RoundedCornerShape(12.dp)).background(t.fg.copy(alpha = 0.1f)).padding(11.dp, 5.dp),
                        fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = t.fg)
                }
            }
        }
    }
}

/** Twelve bars: how many exams you can apply to in each month. */
@Composable
internal fun PwXYear(counts: List<Int>, now: Int) {
    val c = MaterialTheme.colorScheme
    val mx = max(1, counts.max())
    PwSurface(Modifier.fillMaxWidth(), radius = 28.dp) {
        Column(Modifier.padding(14.dp, 14.dp, 14.dp, 10.dp)) {
            Text("Applications open each month", fontSize = 11.5.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant, modifier = Modifier.padding(start = 2.dp, bottom = 10.dp))
            Row(Modifier.fillMaxWidth().height(92.dp), horizontalArrangement = Arrangement.spacedBy(4.dp), verticalAlignment = Alignment.Bottom) {
                counts.forEachIndexed { i, n ->
                    val grow = remember { Animatable(0f) }
                    LaunchedEffect(n) { grow.animateTo(1f, tween(600, delayMillis = i * 20, easing = FastOutSlowInEasing)) }
                    val now1 = i + 1 == now
                    Column(Modifier.weight(1f).height(92.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(4.dp, Alignment.Bottom)) {
                        Box(Modifier.fillMaxWidth().weight(1f), contentAlignment = Alignment.BottomCenter) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(2.dp)) {
                                Text("$n", fontSize = 10.sp, fontWeight = FontWeight.SemiBold, color = if (now1) c.primary else c.onSurfaceVariant, lineHeight = 11.sp)
                                Box(Modifier.fillMaxWidth().height(((8f + 52f * n / mx) * grow.value).dp).clip(RoundedCornerShape(8.dp)).background(if (now1) c.primary else c.surfaceContainerHighest))
                            }
                        }
                        Text("${MONTHS[i].take(1)}", fontSize = 10.sp, fontWeight = FontWeight.SemiBold, color = if (now1) c.primary else c.onSurfaceVariant, lineHeight = 11.sp)
                    }
                }
            }
        }
    }
}

/** The three counters; each one filters the list when tapped. */
@Composable
internal fun PwXSummary(open: Int, soon: Int, no: Int, filter: String, onFilter: (String) -> Unit) {
    val g = pwTone(4); val y = pwTone(2); val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        listOf(Triple("open", open, "Open now"), Triple("soon", soon, "Coming up"), Triple("no", no, "Not eligible")).forEach { (k, n, label) ->
            val on = filter == k
            val tone = when (k) { "open" -> g; "soon" -> y; else -> PwTone(c.surfaceContainerHigh, c.onSurface, c.primary, c.onPrimary) }
            val r by androidx.compose.animation.core.animateDpAsState(if (on) 14.dp else 20.dp, androidx.compose.animation.core.spring(0.5f, 300f), label = "xsr")
            Column(
                Modifier.weight(1f).clip(RoundedCornerShape(r)).background(tone.bg)
                    .border(2.dp, if (on) c.primary else Color.Transparent, RoundedCornerShape(r))
                    .clickable(remember { MutableInteractionSource() }, null) { onFilter(if (on) "all" else k) }.padding(14.dp, 10.dp)
            ) {
                Text("$n", fontSize = 24.sp, fontWeight = FontWeight.SemiBold, lineHeight = 26.sp, color = tone.fg)
                Text(label, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = tone.fg)
            }
        }
    }
}

@Composable
private fun XBar(label: String, v: Float, text: String) {
    val c = MaterialTheme.colorScheme
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(label, Modifier.width(44.dp), fontSize = 11.5.sp, fontWeight = FontWeight.SemiBold)
        PwBar(v, Modifier.weight(1f), height = 6.dp, color = c.primary, track = c.onSurface.copy(alpha = 0.12f))
        Text(text, Modifier.width(74.dp), fontSize = 11.5.sp, fontWeight = FontWeight.SemiBold, textAlign = androidx.compose.ui.text.style.TextAlign.End, maxLines = 1)
    }
}

/** One exam card: name, status pill, month strip, odds and prep bars, fee, exam month. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun PwXCard(g: PwGovt, st: PwXst, prepMax: Int, index: Int, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val no = st.kind == "no"
    val odds = oddsOf(g)
    PwSurface(Modifier.fillMaxWidth().pwRise(index, g.id).then(if (no) Modifier.graphicsLayerAlpha(0.55f) else Modifier), radius = 24.dp, onClick = onClick) {
        Column(Modifier.padding(16.dp, 14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.Top) {
                Column(Modifier.weight(1f)) {
                    Text(g.name, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, lineHeight = 19.sp)
                    Text(g.body, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
                }
                PwTag(st.text, xTone(st.kind))
            }
            if (!no && g.apply.size == 2) PwMonths({ m -> inWindow(g.apply[0], g.apply[1], m) })
            if (!no) Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                if (odds != null) XBar("Odds", xOddsScore(g), odds.text)
                XBar("Prep", prepHoursOf(g) / prepMax.toFloat(), "${prepHoursOf(g)} h")
            }
            FlowRow(horizontalArrangement = Arrangement.spacedBy(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                val m = Modifier
                val meta = listOfNotNull(
                    (if (no) "Fee " else st.sub + " \u00B7 ") + npr(g.fee),
                    if (g.examMonth > 0) "Exam ${MONTHS[g.examMonth - 1]}" else null,
                    if (g.pay > 0) "Starts NPR ${g.pay / 1000}k" else null,
                    if (g.seats > 0) "${money(g.seats.toLong())} seats" else null,
                )
                if (no) Text(st.sub, m, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant)
                else meta.forEach { Text(it, m, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant) }
            }
        }
    }
}

private fun Modifier.graphicsLayerAlpha(a: Float): Modifier = this.then(Modifier.graphicsLayer { alpha = a })
