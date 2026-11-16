package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
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
import kotlin.math.min
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Shape of a career on four to seven scales (0 to 100). Rings at 25, 50, 75 and 100, spokes, a dashed outline for the
 * average career, a filled outline for this one, a dot and number at each corner, labels placed away from the centre.
 */
@Composable
internal fun PwProfileChart(labels: List<String>, values: List<Float>, avg: List<Float>) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val name = MaterialTheme.typography.labelMedium.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
    val num = MaterialTheme.typography.labelLarge.copy(color = c.onSurface, fontWeight = FontWeight.Bold)
    val grow = remember(values) { Animatable(0f) }
    LaunchedEffect(values) { grow.animateTo(1f, spring(0.72f, Spring.StiffnessLow)) }
    val n = labels.size
    val desc = labels.indices.joinToString(", ") { "${labels[it]} ${values[it].roundToInt()}" }
    Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow).padding(bottom = 14.dp)) {
        Canvas(Modifier.fillMaxWidth().aspectRatio(1.18f).semantics { contentDescription = "Profile: $desc" }) {
            val cx = size.width / 2f
            val cy = size.height / 2f
            val rad = min(size.width / 2f - 56.dp.toPx(), size.height / 2f - 34.dp.toPx())
            fun pt(v: Float, i: Int, r: Float = rad): Offset {
                val a = (i * 2.0 * PI / n - PI / 2.0).toFloat()
                return Offset(cx + r * v / 100f * cos(a), cy + r * v / 100f * sin(a))
            }
            fun poly(vs: List<Float>, f: Float = 1f) = Path().apply {
                vs.forEachIndexed { i, v -> val p = pt(v * f, i); if (i == 0) moveTo(p.x, p.y) else lineTo(p.x, p.y) }
                close()
            }
            listOf(25f, 50f, 75f, 100f).forEach { g ->
                drawPath(poly(List(n) { g }), if (g == 100f) c.outline else c.outlineVariant, style = Stroke(if (g == 100f) 1.5.dp.toPx() else 1.dp.toPx(), join = StrokeJoin.Round))
            }
            for (i in 0 until n) drawLine(c.outlineVariant, Offset(cx, cy), pt(100f, i), 1.dp.toPx())
            drawPath(poly(avg, grow.value), c.onSurfaceVariant.copy(alpha = 0.7f), style = Stroke(1.75.dp.toPx(), join = StrokeJoin.Round, pathEffect = PathEffect.dashPathEffect(floatArrayOf(6.dp.toPx(), 5.dp.toPx()))))
            val me = poly(values, grow.value)
            drawPath(me, c.primary.copy(alpha = 0.2f))
            drawPath(me, c.primary, style = Stroke(3.dp.toPx(), join = StrokeJoin.Round))
            for (i in 0 until n) {
                val p = pt(values[i] * grow.value, i)
                drawCircle(c.surfaceContainerLow, 7.dp.toPx(), p)
                drawCircle(c.primary, 5.dp.toPx(), p)
                val a = (i * 2.0 * PI / n - PI / 2.0).toFloat()
                val out = pt(100f, i, rad + 14.dp.toPx())
                val t1 = tm.measure(labels[i], name)
                val t2 = tm.measure("${values[i].roundToInt()}", num)
                val ca = cos(a)
                val w = maxOf(t1.size.width, t2.size.width).toFloat()
                // right of the chart the text starts at the spoke, left of it ends there, top and bottom centre on it
                val x = when { ca > 0.3f -> out.x; ca < -0.3f -> out.x - w; else -> out.x - w / 2f }
                val h = t1.size.height + t2.size.height
                val y = when { sin(a) < -0.5f -> out.y - h; sin(a) > 0.5f -> out.y; else -> out.y - h / 2f }
                val al = when { ca > 0.3f -> 0f; ca < -0.3f -> w - t1.size.width; else -> (w - t1.size.width) / 2f }
                val bl = when { ca > 0.3f -> 0f; ca < -0.3f -> w - t2.size.width; else -> (w - t2.size.width) / 2f }
                drawText(t1, topLeft = Offset(x + al, y))
                drawText(t2, topLeft = Offset(x + bl, y + t1.size.height))
            }
        }
        Row(Modifier.padding(horizontal = 20.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Key("This career", c.primary)
            Key("Average", c.onSurfaceVariant.copy(alpha = 0.7f))
        }
    }
}

@Composable
private fun Key(text: String, color: androidx.compose.ui.graphics.Color) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        Box(Modifier.size(12.dp).clip(RoundedCornerShape(4.dp)).background(color))
        Text(text, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
