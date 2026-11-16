package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
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
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/** Years at which each ladder step starts. Four steps use the concept's 0, 3, 7, 12; any other count is spread over twelve years. */
internal fun rungStarts(n: Int): List<Int> = when {
    n <= 1 -> listOf(0)
    n == 4 -> listOf(0, 3, 7, 12)
    else -> List(n) { it * 12 / (n - 1) }
}

private fun rungRange(st: List<Int>, i: Int): String = when {
    i == st.lastIndex -> "Year ${st[i]}+"
    st[i + 1] - 1 > st[i] -> "Year ${st[i]}\u2013${st[i + 1] - 1}"
    else -> "Year ${st[i]}"
}

/** Pay ladder as in the concept: one row per step with its pay and a bar, the step for the chosen year lit, and a year slider. */
@Composable
internal fun PwPayLadder(k: PwCareer, names: List<String>, exp: Int, onExp: (Int) -> Unit) {
    val st = remember(names.size) { rungStarts(names.size) }
    val top = remember(k) { payAt(k, 12f).coerceAtLeast(1f) }
    val at = st.indexOfLast { it <= exp }.coerceAtLeast(0)
    PwH4("How your monthly pay grows")
    Column(Modifier.padding(bottom = 14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        names.forEachIndexed { i, n ->
            val v = payAt(k, st[i].toFloat())
            LadderRow(i + 1, n, rungRange(st, i), "NPR ${money(v.toLong())}", v / top, i == at, Modifier.pwRise(i, k.id)) { onExp(st[i]) }
        }
    }
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text("Try a year", fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        Spacer(Modifier.width(12.dp))
        Box(Modifier.weight(1f)) { PwSlider(exp.toFloat(), { onExp(it.roundToInt()) }, 0f..12f, 11, if (exp == 0) "Entry" else "Year $exp") }
    }
    PwNote("Monthly salary before tax. Tap a step or drag the slider.")
}

@Composable
private fun LadderRow(n: Int, name: String, years: String, pay: String, fill: Float, on: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val bg by animateColorAsState(if (on) c.primaryContainer else c.surfaceContainerLow, tween(200), label = "rungBg")
    val ink = if (on) c.onPrimaryContainer else c.onSurface
    PwSurface(modifier.fillMaxWidth(), color = bg, radius = 20.dp, onClick = onClick) {
        Row(Modifier.padding(14.dp, 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(Modifier.size(28.dp).clip(CircleShape).background(if (on) c.primary else c.surfaceContainerHighest), contentAlignment = Alignment.Center) {
                Text("$n", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = if (on) c.onPrimary else c.onSurface)
            }
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text(name, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = ink, maxLines = 2, lineHeight = 18.sp)
                        Text(years, fontSize = 12.sp, color = if (on) ink.copy(alpha = 0.75f) else c.onSurfaceVariant)
                    }
                    Text(pay, Modifier.padding(start = 8.dp), fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = ink, maxLines = 1)
                }
                PwBar(fill, Modifier.fillMaxWidth(), 6.dp, c.primary, if (on) c.onPrimaryContainer.copy(alpha = 0.14f) else c.surfaceContainerHighest)
            }
        }
    }
}

@Composable
internal fun PwNote(text: String) {
    Text(text, Modifier.padding(start = 2.dp, top = 8.dp), fontSize = 11.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = 15.sp)
}

private val RADAR_AXES = listOf("Pay", "Demand", "Entry", "Stability", "Flexibility", "Growth")

/** The six scales of one career against the average of all careers, drawn like the concept (three rings, soft average, tinted outline). */
internal fun careerAxes(d: PwData, x: PwCareer, avgTrait: Map<String, Float>): List<Float> = listOf(
    ((x.seniorMin + x.seniorMax) / 2f / d.maxSenior.coerceAtLeast(1L) * 100f).coerceIn(0f, 100f),
    pct(x.demand).toFloat(),
    (100 - pct(x.competition)).toFloat(),
    (x.traits["stability"] ?: avgTrait["stability"]?.roundToInt() ?: 50).toFloat(),
    (x.traits["flexibility"] ?: avgTrait["flexibility"]?.roundToInt() ?: 50).toFloat(),
    (x.traits["growth"] ?: avgTrait["growth"]?.roundToInt() ?: 50).toFloat(),
)

@Composable
internal fun PwRadar(d: PwData, k: PwCareer) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val label = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.SemiBold, fontSize = 10.sp)
    val (mine, avg) = remember(d, k.id) {
        val tr = listOf("stability", "flexibility", "growth").associateWith { t -> d.careers.values.mapNotNull { it.traits[t] }.let { if (it.isEmpty()) 50f else it.average().toFloat() } }
        val rows = d.careers.values.map { careerAxes(d, it, tr) }
        careerAxes(d, k, tr) to RADAR_AXES.indices.map { i -> rows.map { it[i] }.average().toFloat() }
    }
    val grow = remember(k.id) { Animatable(0f) }
    LaunchedEffect(k.id) { grow.animateTo(1f, tween(650, easing = FastOutSlowInEasing)) }
    Canvas(
        Modifier.fillMaxWidth().aspectRatio(320f / 236f)
            .semantics { contentDescription = "Profile: " + RADAR_AXES.indices.joinToString(", ") { "${RADAR_AXES[it]} ${mine[it].roundToInt()}" } },
    ) {
        val sc = size.width / 320f
        fun pt(v: Float, i: Int, r: Float = 84f): Offset {
            val a = ((i * 60 - 90) * PI / 180.0).toFloat()
            val rr = r * v / 100f
            return Offset((160f + rr * cos(a)) * sc, (118f + rr * sin(a)) * sc)
        }
        fun poly(vs: List<Float>, f: Float = 1f) = Path().apply { vs.forEachIndexed { i, v -> val p = pt(v * f, i); if (i == 0) moveTo(p.x, p.y) else lineTo(p.x, p.y) }; close() }
        listOf(33f, 66f, 100f).forEach { drawPath(poly(List(6) { _ -> it }), c.outlineVariant, style = Stroke(1.dp.toPx(), join = StrokeJoin.Round)) }
        drawPath(poly(avg, grow.value), c.surfaceContainerHighest)
        val me = poly(mine, grow.value)
        drawPath(me, c.primary.copy(alpha = 0.22f))
        drawPath(me, c.primary, style = Stroke(2.5.dp.toPx(), join = StrokeJoin.Round))
        RADAR_AXES.forEachIndexed { i, t ->
            val p = pt(100f, i, 102f)
            val m = tm.measure(t, label)
            val x = when { i % 3 == 0 -> p.x - m.size.width / 2f; i < 3 -> p.x; else -> p.x - m.size.width }
            drawText(m, topLeft = Offset(x, p.y + 4 * sc - m.size.height * 0.78f))
        }
        drawCircle(c.surfaceContainerHighest, 5.dp.toPx(), Offset(14f * sc, 12f * sc))
        val lg = tm.measure("Average", label)
        drawText(lg, topLeft = Offset(24f * sc, 16f * sc - lg.size.height * 0.78f))
    }
}

/** Years of demand as a soft area, one line and a dot on the latest year, like the concept's plot. */
@Composable
internal fun PwSpark(vals: List<Float>, lastYear: Int) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val label = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.SemiBold, fontSize = 10.sp)
    val reveal = remember(vals) { Animatable(0f) }
    LaunchedEffect(vals) { reveal.animateTo(1f, tween(700, easing = FastOutSlowInEasing)) }
    val n = vals.size
    Canvas(
        Modifier.fillMaxWidth().aspectRatio(320f / 104f).clip(RoundedCornerShape(24.dp)).background(c.surfaceContainerLow)
            .semantics { contentDescription = "Demand from ${lastYear - n + 1} to $lastYear, now ${vals.last().roundToInt()}" },
    ) {
        val sc = size.width / 320f
        val lo = vals.min() - 8f; val hi = vals.max() + 8f
        fun px(i: Int) = (16f + i * 288f / (n - 1)) * sc
        fun py(v: Float) = (78f - (v - lo) / (hi - lo) * 60f) * sc
        val line = Path().apply { vals.forEachIndexed { i, v -> if (i == 0) moveTo(px(i), py(v)) else lineTo(px(i), py(v)) } }
        val area = Path().apply { addPath(line); lineTo(304f * sc, 92f * sc); lineTo(16f * sc, 92f * sc); close() }
        androidx.compose.ui.graphics.drawscope.clipRect(0f, 0f, size.width * reveal.value, size.height) {
            drawPath(area, c.primaryContainer)
            drawPath(line, c.primary, style = Stroke(3.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round))
        }
        if (reveal.value > 0.95f) drawCircle(c.primary, 6.dp.toPx(), Offset(304f * sc, py(vals.last())))
        val a = tm.measure("${lastYear - n + 1}", label); val b = tm.measure("$lastYear", label)
        drawText(a, topLeft = Offset(16f * sc, 102f * sc - a.size.height * 0.85f))
        drawText(b, topLeft = Offset(304f * sc - b.size.width, 102f * sc - b.size.height * 0.85f))
    }
}

private fun odds(k: PwCareer) = pct(k.demand) - pct(k.competition)

/** Verdict, the two bars, and the five careers around this one in the odds ranking, as in the concept. */
@Composable
internal fun PwMarket(d: PwData, k: PwCareer, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val all = remember(d) { d.careers.values.sortedByDescending { odds(it) } }
    val rank = all.indexOfFirst { it.id == k.id } + 1
    val g = odds(k)
    val (title, line, toneIx) = when {
        g >= 30 -> Triple("Great odds", "Lots of jobs, few rivals", 4)
        g >= 10 -> Triple("Good odds", "More jobs than rivals", 4)
        g >= -10 -> Triple("Competitive", "Jobs and rivals are about equal", 2)
        else -> Triple("Tough to enter", "Many more rivals than jobs", 5)
    }
    val tone = pwTone(toneIx)
    Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(24.dp)).background(tone.bg).padding(18.dp, 16.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(title, fontSize = 18.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.3).sp, color = tone.fg)
        Text(line, fontSize = 13.sp, fontWeight = FontWeight.Medium, color = tone.fg)
        Text("#$rank of ${all.size} careers", Modifier.padding(top = 4.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = tone.fg.copy(alpha = 0.75f))
    }
    Spacer(Modifier.height(14.dp))
    MarketBar("Jobs available", pct(k.demand), c.primary)
    MarketBar("People competing", pct(k.competition), c.onSurfaceVariant)
    Text("Easiest careers to get into", Modifier.padding(top = 18.dp, bottom = 6.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant)
    val lo = (rank - 3).coerceIn(0, (all.size - 5).coerceAtLeast(0))
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        all.drop(lo).take(5).forEachIndexed { j, o ->
            val me = o.id == k.id
            val ink = if (me) c.onPrimaryContainer else c.onSurface
            PwSurface(Modifier.fillMaxWidth().pwRise(j, k.id), color = if (me) c.primaryContainer else c.surfaceContainerLow, radius = 16.dp, onClick = if (me) null else ({ nav.push("career:${o.id}") })) {
                Row(Modifier.padding(12.dp, 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("${lo + j + 1}", Modifier.width(22.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = if (me) ink else c.onSurfaceVariant)
                    Text(o.name, Modifier.weight(1f), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = ink, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                    PwBar(((odds(o) + 50) / 110f).coerceIn(0.06f, 1f), Modifier.width(84.dp), 8.dp, c.primary, if (me) c.onPrimaryContainer.copy(alpha = 0.14f) else c.surfaceContainerHighest)
                }
            }
        }
    }
    PwNote("Bar length shows jobs minus competition. Longer means easier to get a job.")
}

@Composable
private fun MarketBar(label: String, v: Int, color: androidx.compose.ui.graphics.Color) {
    Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(label, Modifier.width(128.dp), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
        PwBar(v / 100f, Modifier.weight(1f), 12.dp, color)
        Text("$v", Modifier.width(26.dp), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, textAlign = androidx.compose.ui.text.style.TextAlign.End)
    }
}
