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
    val rungYears = ladder.indices.map { if (ladder.size == 1) 0 else it * 12 / (ladder.size - 1) }
    val rung = rungYears.indexOfLast { it <= exp }.coerceAtLeast(0)
    val key = "career:${k.id}"
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(bottom = 32.dp)) {
        PwHero(tone, k.name, "NPR ${money(k.entryMin)}–${money(k.seniorMax)} / month", key in ui.saved, { vm.toggleSaved(key) }, nav.pop) {
            PwBadge(tone, 5) { PwSignal(pct(k.demand), tone.bg, 34.dp) }
        }
        PwMeters(pct(k.demand), pct(k.competition), "NPR ${money(payAt(k, exp.toFloat()).toLong())}", "${if (exp == 0) "Entry" else "Year $exp"} · ${ladder[rung]}")
        val tabs = buildList {
            add("pay" to "Pay"); add("profile" to "Profile"); add("skills" to "Skills"); add("market" to "Market")
        }
        PwTabs(tabs, tab) { tab = it }
        Column(Modifier.padding(16.dp, 18.dp, 16.dp, 20.dp)) {
            when (tab) {
                "profile" -> CareerProfile(d, k)
                "skills" -> CareerSkills(d, k, vm, nav)
                "market" -> CareerMarket(d, k, nav)
                else -> {
                    PayCurve(k, exp.toFloat())
                    Slider(exp.toFloat(), { exp = it.roundToInt() }, valueRange = 0f..12f, steps = 11)
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        ladder.forEachIndexed { i, name ->
                            PwChip(name, i == rung, { exp = rungYears[i] }, Modifier.weight(1f))
                        }
                    }
                    if (k.about.isNotBlank()) {
                        PwH4("About")
                        Text(k.about, fontSize = 15.sp, lineHeight = 23.sp)
                    }
                }
            }
        }
    }
}

@Composable
private fun PayCurve(k: PwCareer, exp: Float) {
    val c = MaterialTheme.colorScheme
    val at by animateFloatAsState(exp, tween(400, easing = FastOutSlowInEasing), label = "payDot")
    val maxPay = maxOf(k.seniorMax.toFloat(), payAt(k, 12f)).coerceAtLeast(1f)
    Canvas(Modifier.fillMaxWidth().height(130.dp)) {
        val left = 10.dp.toPx()
        val w = size.width - 2 * left
        val h = size.height
        fun px(y: Float) = left + y * w / 12f
        fun py(v: Float) = h - 8.dp.toPx() - v / maxPay * (h - 24.dp.toPx())
        val line = Path()
        for (y in 0..24) {
            val yy = y / 2f
            if (y == 0) line.moveTo(px(yy), py(payAt(k, yy))) else line.lineTo(px(yy), py(payAt(k, yy)))
        }
        val area = Path().apply { addPath(line); lineTo(px(12f), h); lineTo(px(0f), h); close() }
        drawPath(area, c.primaryContainer)
        drawPath(line, c.primary, style = Stroke(3.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round))
        val dot = Offset(px(at), py(payAt(k, at)))
        drawCircle(c.surface, 12.dp.toPx(), dot)
        drawCircle(c.primary, 8.dp.toPx(), dot)
    }
}

@Composable
private fun CareerProfile(d: PwData, k: PwCareer) {
    val all = d.careers.values
    fun axes(x: PwCareer): List<Pair<String, Float>> = buildList {
        add("Pay" to ((x.seniorMin + x.seniorMax) / 2f / d.maxSenior * 100f).coerceIn(0f, 100f))
        add("Demand" to pct(x.demand).toFloat())
        add("Entry" to (100 - pct(x.competition)).toFloat())
        add("Abroad" to pct(x.abroad).toFloat())
        TRAITS.forEach { (t, label) -> if (t in k.traits) add(label to (x.traits[t] ?: 50).toFloat()) }
    }
    val mine = axes(k)
    val avg = remember(d, k.id) {
        val rows = all.map { axes(it) }
        mine.indices.map { i -> rows.map { it[i].second }.average().toFloat() }
    }
    PwRadar(mine.map { it.first }, mine.map { it.second }, avg)
    if (k.day.isNotEmpty()) {
        PwH4(if (k.hours > 0) "A ${k.hours}-hour week" else "A week")
        PwSplit(k.day)
    }
}

private val TRAITS = listOf("stability" to "Stability", "flexibility" to "Flexibility", "growth" to "Growth")

@Composable
private fun PwRadar(labels: List<String>, values: List<Float>, avg: List<Float>) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val style = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
    val grow = remember(values) { Animatable(0f) }
    LaunchedEffect(values) { grow.animateTo(1f, tween(800, easing = FastOutSlowInEasing)) }
    val n = labels.size
    Canvas(Modifier.fillMaxWidth().aspectRatio(1.35f)) {
        val cx = size.width / 2
        val cy = size.height / 2 + 4.dp.toPx()
        val rad = min(size.width, size.height) / 2 - 28.dp.toPx()
        fun pt(v: Float, i: Int, r: Float = rad): Offset {
            val a = ((i * 360f / n - 90f) * PI / 180.0).toFloat()
            return Offset(cx + r * v / 100f * cos(a), cy + r * v / 100f * sin(a))
        }
        fun poly(vs: List<Float>): Path = Path().apply {
            vs.forEachIndexed { i, v -> val p = pt(v, i); if (i == 0) moveTo(p.x, p.y) else lineTo(p.x, p.y) }
            close()
        }
        listOf(33f, 66f, 100f).forEach { g -> drawPath(poly(List(n) { g }), c.outlineVariant, style = Stroke(1.dp.toPx())) }
        drawPath(poly(avg), c.surfaceContainerHighest)
        val me = poly(values.map { it * grow.value })
        drawPath(me, c.primary.copy(alpha = 0.22f))
        drawPath(me, c.primary, style = Stroke(2.5.dp.toPx(), join = StrokeJoin.Round))
        labels.forEachIndexed { i, label ->
            val lay = tm.measure(label, style)
            val p = pt(100f, i, rad + 16.dp.toPx())
            drawText(lay, topLeft = Offset(p.x - lay.size.width / 2f, p.y - lay.size.height / 2f))
        }
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
    PwH4("Demand, 5 years", Modifier.padding(top = 0.dp))
    Sparkline(k)
    PwH4("Demand against competition")
    Scatter(d, k) { nav.push("career:$it") }
    if (k.jobs.isNotEmpty()) {
        PwH4("Where the jobs are")
        PwSplit(k.jobs)
    }
    if (k.employers.isNotEmpty()) {
        PwH4("Employers")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { k.employers.forEach { PwOutlineChip(it) } }
    }
}

@Composable
private fun Sparkline(k: PwCareer) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val style = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
    val year = remember { Calendar.getInstance().get(Calendar.YEAR) }
    val vals = remember(k) {
        if (k.history.size >= 2) k.history.map { pct(it).toFloat() }
        else {
            val slope = when (k.trend.lowercase()) { "rising" -> 3f; "falling" -> -3f; else -> 0f }
            List(6) { i -> (pct(k.demand) - slope * (5 - i)).coerceIn(5f, 99f) }
        }
    }
    Canvas(Modifier.fillMaxWidth().height(110.dp).clip(RoundedCornerShape(24.dp))) {
        drawRect(c.surfaceContainerLow)
        val lo = vals.min() - 8f
        val hi = vals.max() + 8f
        val left = 16.dp.toPx()
        val w = size.width - 2 * left
        val base = size.height - 22.dp.toPx()
        fun px(i: Int) = left + i * w / (vals.size - 1)
        fun py(v: Float) = base - (v - lo) / (hi - lo) * (base - 14.dp.toPx())
        val line = Path().apply { vals.forEachIndexed { i, v -> if (i == 0) moveTo(px(i), py(v)) else lineTo(px(i), py(v)) } }
        val area = Path().apply { addPath(line); lineTo(px(vals.lastIndex), base); lineTo(px(0), base); close() }
        drawPath(area, c.primaryContainer)
        drawPath(line, c.primary, style = Stroke(3.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round))
        drawCircle(c.primary, 6.dp.toPx(), Offset(px(vals.lastIndex), py(vals.last())))
        val a = tm.measure("${year - vals.size + 1}", style)
        val b = tm.measure("$year", style)
        drawText(a, topLeft = Offset(left, size.height - a.size.height - 4.dp.toPx()))
        drawText(b, topLeft = Offset(size.width - left - b.size.width, size.height - b.size.height - 4.dp.toPx()))
    }
}

@Composable
private fun Scatter(d: PwData, k: PwCareer, onPick: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    val good = pwTone(4).bg
    val tm = rememberTextMeasurer()
    val style = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
    // ratings are whole steps, so a stable per-id jitter keeps careers on the same step from hiding each other
    val points = remember(d) {
        d.careers.values.map { x ->
            val h = abs(x.id.hashCode())
            Triple(x.id, (pct(x.competition) + (h % 13 - 6)).toFloat(), (pct(x.demand) + (h / 13 % 13 - 6)).toFloat())
        }
    }
    fun toPt(sz: Size, comp: Float, dem: Float): Offset {
        val pad = 16f * (sz.width / 320f)
        return Offset(pad + comp / 100f * (sz.width - 2 * pad), sz.height - pad - dem / 100f * (sz.height - 2 * pad))
    }
    Canvas(
        Modifier.fillMaxWidth().aspectRatio(1.7f).clip(RoundedCornerShape(24.dp))
            .pointerInput(points) {
                detectTapGestures { pos ->
                    val sz = Size(size.width.toFloat(), size.height.toFloat())
                    points.minByOrNull { (_, x, y) -> (toPt(sz, x, y) - pos).getDistance() }
                        ?.takeIf { (_, x, y) -> (toPt(sz, x, y) - pos).getDistance() < 28.dp.toPx() }
                        ?.let { onPick(it.first) }
                }
            },
    ) {
        drawRect(c.surfaceContainerLow)
        drawRoundRect(good, Offset(8.dp.toPx(), 8.dp.toPx()), Size(size.width / 2 - 8.dp.toPx(), size.height / 2 - 8.dp.toPx()), CornerRadius(16.dp.toPx()))
        points.forEach { (id, x, y) -> if (id != k.id) drawCircle(c.outline, 4.dp.toPx(), toPt(size, x, y)) }
        points.firstOrNull { it.first == k.id }?.let { (_, x, y) -> drawCircle(c.primary, 9.dp.toPx(), toPt(size, x, y)) }
        label(tm.measure("Demand", style), Offset(14.dp.toPx(), 12.dp.toPx()))
        val comp = tm.measure("Competition", style)
        label(comp, Offset(size.width - comp.size.width - 14.dp.toPx(), size.height - comp.size.height - 10.dp.toPx()))
    }
}

private fun DrawScope.label(t: androidx.compose.ui.text.TextLayoutResult, at: Offset) = drawText(t, topLeft = at)

