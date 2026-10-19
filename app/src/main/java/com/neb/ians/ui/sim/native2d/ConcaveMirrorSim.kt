package com.neb.ians.ui.sim.native2d

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.sim.SimPanel
import com.neb.ians.ui.sim.SimReadouts
import com.neb.ians.ui.sim.SimSlider
import kotlin.math.abs
import kotlin.math.sqrt

/**
 * Concave mirror ray diagram natively. Real-is-positive convention: 1/u + 1/v = 1/f, m = −v/u.
 * The three principal rays are drawn from the tip of the object (parallel then through F, through
 * F then parallel, through C and back on itself); behind the mirror their extensions meet for a
 * virtual image. Drag the object along the axis.
 */
@Composable
fun NativeConcaveMirror(modifier: Modifier = Modifier) {
    var f by remember { mutableFloatStateOf(15f) }
    var u by remember { mutableFloatStateOf(40f) }
    val measurer = rememberTextMeasurer()
    val v = if (abs(u - f) < 0.05f) Float.POSITIVE_INFINITY else u * f / (u - f)
    val m = if (v.isInfinite()) Float.POSITIVE_INFINITY else -v / u
    val nature = when {
        v.isInfinite() -> "At infinity (object at F)"
        v > 0 && abs(m) > 1.01f -> "Real, inverted, magnified"
        v > 0 && abs(m) < 0.99f -> "Real, inverted, diminished"
        v > 0 -> "Real, inverted, same size (at C)"
        else -> "Virtual, upright, magnified"
    }
    Column(modifier) {
        Canvas(Modifier.fillMaxWidth().aspectRatio(16f / 10f).pointerInput(Unit) {
            detectDragGestures { change, _ ->
                val mirrorX = size.width * 0.82f; val s = size.width * 0.78f / 100f
                u = ((mirrorX - change.position.x) / s).coerceIn(3f, 100f)
            }
        }) {
            val w = size.width; val h = size.height; val axis = h * 0.55f; val mirrorX = w * 0.82f; val s = w * 0.78f / 100f
            drawRect(Color(0xFFF8FAFC))
            drawLine(Color(0xFF94A3B8), Offset(0f, axis), Offset(w, axis), 1.5f)
            // the mirror: a shallow arc of radius 2f, silvered on the back
            val R = 2 * f * s; val half = h * 0.42f
            val mp = Path(); val n = 40
            for (i in 0..n) { val y = -half + 2 * half * i / n; val sag = if (R > abs(y)) R - sqrt(R * R - y * y) else 0f; val x = mirrorX - sag; if (i == 0) mp.moveTo(x, axis + y) else mp.lineTo(x, axis + y) }
            drawPath(mp, Color(0xFF1E2A4A), style = Stroke(4f, cap = StrokeCap.Round))
            for (i in 0..14) { val y = -half + 2 * half * i / 14; val sag = if (R > abs(y)) R - sqrt(R * R - y * y) else 0f; drawLine(Color(0xFF64748B), Offset(mirrorX - sag + 2f, axis + y), Offset(mirrorX - sag + 9f, axis + y - 6f), 1.5f) }
            fun mark(x: Float, label: String) { drawCircle(Color(0xFF1E2A4A), 4f, Offset(x, axis)); drawText(measurer, label, Offset(x - 4f, axis + 6f), TextStyle(fontSize = 12.sp, color = Color(0xFF1E2A4A))) }
            mark(mirrorX - f * s, "F"); mark(mirrorX - 2 * f * s, "C"); mark(mirrorX, "P")
            val objH = h * 0.16f; val ox = mirrorX - u * s; val tip = Offset(ox, axis - objH)
            arrow(this, Offset(ox, axis), tip, Color(0xFF2F64D6), 4f)
            val hasImage = !v.isInfinite()
            val ix = mirrorX - v * s; val iTip = Offset(ix, axis + objH * v / u)
            val ray = Color(0xFFE5484D); val ext = PathEffect.dashPathEffect(floatArrayOf(8f, 7f))
            val far = 3000f
            // ray 1: parallel, then through F
            val p1 = Offset(mirrorX, tip.y); drawLine(ray, tip, p1, 2f)
            val dir1 = Offset(mirrorX - f * s - p1.x, axis - p1.y); drawLine(ray, p1, p1 + dir1 * (far / dir1.getDistance()), 2f)
            // ray 2: through F, then parallel
            val toF = Offset(mirrorX - f * s - tip.x, axis - tip.y)
            if (u > f + 0.05f) {
                val tHit = (mirrorX - tip.x) / toF.x; val p2 = tip + toF * tHit
                drawLine(Color(0xFF16A34A), tip, p2, 2f); drawLine(Color(0xFF16A34A), p2, Offset(-far, p2.y), 2f)
            } else {
                val away = Offset(tip.x - (mirrorX - f * s), tip.y - axis); val tHit = (mirrorX - tip.x) / away.x; val p2 = tip + away * tHit
                drawLine(Color(0xFF16A34A), tip, p2, 2f); drawLine(Color(0xFF16A34A), p2, Offset(-far, p2.y), 2f)
                drawLine(Color(0xFF16A34A).copy(alpha = 0.6f), p2, Offset(far, p2.y), 1.5f, pathEffect = ext)
            }
            if (hasImage && v < 0) {
                drawLine(ray.copy(alpha = 0.6f), p1, p1 - dir1 * (far / dir1.getDistance()), 1.5f, pathEffect = ext)
            }
            if (hasImage) arrow(this, Offset(ix, axis), iTip, Color(0xFF7C3AED), if (v > 0) 4f else 3f, dashed = v < 0)
            drawText(measurer, "object", Offset(ox - 20f, axis + 18f), TextStyle(fontSize = 11.sp, color = Color(0xFF2F64D6)))
            if (hasImage && abs(ix) < w * 2) drawText(measurer, if (v > 0) "real image" else "virtual image", Offset(ix - 30f, if (iTip.y > axis) iTip.y + 6f else axis + 18f), TextStyle(fontSize = 11.sp, color = Color(0xFF7C3AED)))
        }
        SimPanel {
            SimReadouts(listOf(
                "u" to "%.1f cm".format(u),
                "v" to if (v.isInfinite()) "∞" else "%.1f cm".format(v),
                "Magnification m = −v/u" to if (m.isInfinite()) "∞" else "%.2f".format(m),
                "Image" to nature
            ))
            SimSlider("Focal length f", f, 5f..30f, { "%.0f cm".format(it) }, { f = it })
            SimSlider("Object distance u (or drag the object)", u, 3f..100f, { "%.1f cm".format(it) }, { u = it })
        }
    }
}

private fun arrow(d: DrawScope, from: Offset, to: Offset, c: Color, width: Float, dashed: Boolean = false) = with(d) {
    val pe = if (dashed) PathEffect.dashPathEffect(floatArrayOf(8f, 6f)) else null
    drawLine(c, from, to, width, cap = StrokeCap.Round, pathEffect = pe)
    val dir = (to - from); val l = dir.getDistance().coerceAtLeast(1f); val ux = dir.x / l; val uy = dir.y / l
    val head = 12f
    drawLine(c, to, Offset(to.x - ux * head - uy * head * 0.5f, to.y - uy * head + ux * head * 0.5f), width, cap = StrokeCap.Round)
    drawLine(c, to, Offset(to.x - ux * head + uy * head * 0.5f, to.y - uy * head - ux * head * 0.5f), width, cap = StrokeCap.Round)
}
