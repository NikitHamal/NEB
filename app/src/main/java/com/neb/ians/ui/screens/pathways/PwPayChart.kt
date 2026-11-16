package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.ceil
import kotlin.math.pow
import kotlin.math.roundToInt

/** Same shape as [payAt], for any start and end figure: slow first five years, then the climb to senior pay. */
private fun curve(e: Float, s: Float, y: Float): Float {
    val mid = e + (s - e) * 0.45f
    return if (y <= 5f) e + (mid - e) * y / 5f else mid + (s - mid) * ((y - 5f) / 7f).coerceAtMost(1f)
}

/** A round step (1, 2, 5 x 10^n) that gives about three grid lines. */
private fun niceStep(hi: Float): Float {
    val raw = (hi / 3f).coerceAtLeast(1f)
    val p = 10f.pow(kotlin.math.floor(kotlin.math.log10(raw)))
    return listOf(1f, 2f, 2.5f, 5f, 10f).map { it * p }.first { it >= raw }
}

/** Pay by years of work: a typical line, the shaded range around it, grid in rupees, and a scrubber you drag or tap. */
@Composable
internal fun PwPayChart(k: PwCareer, exp: Int, rungYears: List<Int>, onExp: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val tick = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.Medium)
    val tip = MaterialTheme.typography.labelLarge.copy(color = c.surface, fontWeight = FontWeight.SemiBold)
    val at by animateFloatAsState(exp.toFloat(), spring(0.8f, Spring.StiffnessMediumLow), label = "payAt")
    val reveal = remember(k.id) { Animatable(0f) }
    LaunchedEffect(k.id) { reveal.animateTo(1f, tween(750, easing = FastOutSlowInEasing)) }
    val lo = remember(k) { { y: Float -> curve(k.entryMin.toFloat(), k.seniorMin.toFloat(), y) } }
    val hi = remember(k) { { y: Float -> curve(k.entryMax.toFloat(), k.seniorMax.toFloat(), y) } }
    val mid = remember(k) { { y: Float -> payAt(k, y) } }
    val step = remember(k) { niceStep(maxOf(hi(12f), mid(12f), 1f)) }
    val top = remember(k) { step * ceil(maxOf(hi(12f), 1f) / step).coerceAtLeast(2f) }
    val onPick by rememberUpdatedState(onExp)
    Column2(
        Modifier.fillMaxWidth().clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow).padding(top = 4.dp, bottom = 12.dp),
    ) {
        Canvas(
            Modifier.fillMaxWidth().height(220.dp)
                .semantics { contentDescription = "Pay at year $exp is about NPR ${money(mid(exp.toFloat()).toLong())} a month" }
                .pointerInput(Unit) {
                    val l = 16.dp.toPx(); val w = size.width - 2 * l
                    detectTapGestures { onPick(((it.x - l) / w * 12f).roundToInt().coerceIn(0, 12)) }
                }
                .pointerInput(Unit) {
                    val l = 16.dp.toPx(); val w = size.width - 2 * l
                    detectHorizontalDragGestures { ch, _ -> onPick(((ch.position.x - l) / w * 12f).roundToInt().coerceIn(0, 12)) }
                },
        ) {
            val l = 16.dp.toPx(); val w = size.width - 2 * l
            val t = 34.dp.toPx(); val b = size.height - 26.dp.toPx()
            fun px(y: Float) = l + y * w / 12f
            fun py(v: Float) = b - (v / top).coerceIn(0f, 1f) * (b - t)
            val dash = PathEffect.dashPathEffect(floatArrayOf(5.dp.toPx(), 5.dp.toPx()))
            var g = step
            while (g <= top + 1f) {
                val y = py(g)
                drawLine(c.outlineVariant, Offset(l, y), Offset(l + w, y), 1.dp.toPx(), pathEffect = dash)
                val lab = tm.measure("NPR ${money(g.toLong())}", tick)
                drawText(lab, topLeft = Offset(l, y - lab.size.height - 1.dp.toPx()))
                g += step
            }
            drawLine(c.outline, Offset(l, b), Offset(l + w, b), 1.5.dp.toPx(), StrokeCap.Round)
            clipRect(0f, 0f, l + w * reveal.value + 8.dp.toPx(), size.height) {
                val band = Path().apply {
                    for (i in 0..48) { val yy = i / 4f; if (i == 0) moveTo(px(yy), py(hi(yy))) else lineTo(px(yy), py(hi(yy))) }
                    for (i in 48 downTo 0) { val yy = i / 4f; lineTo(px(yy), py(lo(yy))) }
                    close()
                }
                drawPath(band, c.primary.copy(alpha = 0.13f))
                val line = Path().apply { for (i in 0..48) { val yy = i / 4f; if (i == 0) moveTo(px(yy), py(mid(yy))) else lineTo(px(yy), py(mid(yy))) } }
                drawPath(line, c.primary, style = Stroke(3.5.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round))
            }
            rungYears.forEach { y ->
                val p = Offset(px(y.toFloat()), py(mid(y.toFloat())))
                drawCircle(c.surfaceContainerLow, 5.5.dp.toPx(), p)
                drawCircle(c.primary, 4.dp.toPx(), p, style = Stroke(2.dp.toPx()))
            }
            listOf(0, 3, 6, 9, 12).forEach { y ->
                val lab = tm.measure(if (y == 0) "Start" else "${y}y", tick)
                val x = (px(y.toFloat()) - lab.size.width / 2f).coerceIn(2.dp.toPx(), size.width - lab.size.width - 2.dp.toPx())
                drawText(lab, topLeft = Offset(x, b + 6.dp.toPx()))
            }
            val dot = Offset(px(at), py(mid(at)))
            drawLine(c.primary.copy(alpha = 0.4f), Offset(dot.x, dot.y), Offset(dot.x, b), 1.5.dp.toPx(), pathEffect = dash)
            drawCircle(c.surfaceContainerLow, 12.dp.toPx(), dot)
            drawCircle(c.primary, 8.dp.toPx(), dot)
            val txt = tm.measure("NPR ${money(mid(at).toLong())}", tip)
            val pw = txt.size.width + 24.dp.toPx(); val ph = 28.dp.toPx()
            val bx = (dot.x - pw / 2f).coerceIn(2.dp.toPx(), size.width - pw - 2.dp.toPx())
            val by = if (dot.y - ph - 18.dp.toPx() < 0f) dot.y + 18.dp.toPx() else dot.y - ph - 16.dp.toPx()
            drawRoundRect(c.onSurface, Offset(bx, by), Size(pw, ph), CornerRadius(ph / 2f))
            drawText(txt, topLeft = Offset(bx + 12.dp.toPx(), by + (ph - txt.size.height) / 2f))
        }
        Row(Modifier.padding(horizontal = 20.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Legend("Typical", c.primary, true)
            Legend("Range", c.primary.copy(alpha = 0.22f), false)
        }
    }
}

@Composable
private fun Legend(text: String, color: androidx.compose.ui.graphics.Color, line: Boolean) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        Box(Modifier.size(if (line) 16.dp else 12.dp, if (line) 4.dp else 12.dp).clip(RoundedCornerShape(if (line) 2.dp else 4.dp)).background(color))
        Text(text, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun Column2(modifier: Modifier, content: @Composable androidx.compose.foundation.layout.ColumnScope.() -> Unit) =
    androidx.compose.foundation.layout.Column(modifier, verticalArrangement = Arrangement.spacedBy(6.dp), content = content)

/** The career ladder as four tiles under the chart: the year it starts and the step name, which may take two lines. */
@Composable
internal fun PwRungs(names: List<String>, years: List<Int>, selected: Int, onPick: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        names.forEachIndexed { i, n ->
            val on = i == selected
            androidx.compose.material3.Surface(
                onClick = { onPick(i) }, modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(18.dp), color = if (on) c.onSurface else c.surfaceContainerHigh,
                contentColor = if (on) c.surface else c.onSurface,
            ) {
                Column(Modifier.padding(horizontal = 8.dp, vertical = 10.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(2.dp)) {
                    Text(if (years[i] == 0) "Start" else "Year ${years[i]}", fontSize = 11.sp, fontWeight = FontWeight.Medium, color = (if (on) c.surface else c.onSurfaceVariant))
                    Text(n, fontSize = 12.5.sp, lineHeight = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                }
            }
        }
    }
}
