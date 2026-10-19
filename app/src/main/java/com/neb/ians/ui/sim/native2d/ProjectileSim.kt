package com.neb.ians.ui.sim.native2d

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.sim.SimButton
import com.neb.ians.ui.sim.SimPanel
import com.neb.ians.ui.sim.SimReadouts
import com.neb.ians.ui.sim.SimSlider
import kotlin.math.atan2
import kotlin.math.ceil
import kotlin.math.cos
import kotlin.math.max
import kotlin.math.sin
import kotlin.math.sqrt

/** One flight: sampled points (x, y in metres) and its summary. */
private class Flight(val pts: List<Offset>, val range: Float, val height: Float, val time: Float, val hue: Color)

private val HUES = listOf(Color(0xFF2F64D6), Color(0xFFE5484D), Color(0xFF16A34A), Color(0xFFD97706), Color(0xFF7C3AED))

/**
 * Projectile motion natively. Flights are integrated with RK4 including quadratic air drag
 * (F = ½ρC_dAv², a 0.43 kg ball when drag is on), so without drag the range matches v²sin2θ/g
 * exactly and with it the path is the lopsided curve a real ball follows. Drag the cannon to aim.
 */
@Composable
fun NativeProjectileMotion(modifier: Modifier = Modifier) {
    var speed by remember { mutableFloatStateOf(20f) }
    var angle by remember { mutableFloatStateOf(45f) }
    var g by remember { mutableFloatStateOf(9.81f) }
    var drag by remember { mutableFloatStateOf(0f) }
    val flights = remember { mutableStateListOf<Flight>() }
    var flying by remember { mutableStateOf<Flight?>(null) }
    var tNow by remember { mutableFloatStateOf(0f) }
    var shots by remember { mutableIntStateOf(0) }
    val measurer = rememberTextMeasurer()

    fun simulate(): Flight {
        val k = drag * 0.5f * 1.2f * 0.47f * 0.0227f / 0.43f
        var x = 0.0; var y = 0.0
        val a = Math.toRadians(angle.toDouble())
        var vx = speed * cos(a); var vy = speed * sin(a)
        val pts = ArrayList<Offset>(); var maxY = 0.0; var t = 0.0; val h = 0.004
        fun acc(vx: Double, vy: Double): Pair<Double, Double> { val v = sqrt(vx * vx + vy * vy); return (-k * v * vx) to (-g - k * v * vy) }
        while (t < 60) {
            pts.add(Offset(x.toFloat(), y.toFloat()))
            val (ax1, ay1) = acc(vx, vy); val (ax2, ay2) = acc(vx + ax1 * h / 2, vy + ay1 * h / 2)
            val (ax3, ay3) = acc(vx + ax2 * h / 2, vy + ay2 * h / 2); val (ax4, ay4) = acc(vx + ax3 * h, vy + ay3 * h)
            val nx = x + h * (vx + h / 6 * (ax1 + ax2 + ax3)); val ny = y + h * (vy + h / 6 * (ay1 + ay2 + ay3))
            vx += h / 6 * (ax1 + 2 * ax2 + 2 * ax3 + ax4); vy += h / 6 * (ay1 + 2 * ay2 + 2 * ay3 + ay4)
            t += h
            if (ny < 0 && t > h) { val f = y / (y - ny); x += (nx - x) * f; pts.add(Offset(x.toFloat(), 0f)); t -= h * (1 - f); break }
            x = nx; y = ny; maxY = max(maxY, y)
        }
        // keep about 400 points for drawing
        val step = max(1, pts.size / 400)
        return Flight(pts.filterIndexed { i, _ -> i % step == 0 || i == pts.size - 1 }, x.toFloat(), maxY.toFloat(), t.toFloat(), HUES[shots % HUES.size])
    }

    LaunchedEffect(flying) {
        val f = flying ?: return@LaunchedEffect
        val start = withFrameNanos { it }
        while (true) {
            val done = withFrameNanos { now -> tNow = (now - start) / 1e9f * 1.2f; tNow >= f.time }
            if (done) break
        }
        flights.add(0, f); if (flights.size > 5) flights.removeAt(flights.size - 1); flying = null
    }

    val latest = flying ?: flights.firstOrNull()
    Column(modifier) {
        Canvas(
            Modifier.fillMaxWidth().aspectRatio(16f / 10f).pointerInput(Unit) {
                detectDragGestures { change, _ ->
                    val p = change.position
                    val ox = size.width * 0.07f; val oy = size.height * 0.86f
                    angle = Math.toDegrees(atan2((oy - p.y).toDouble(), (p.x - ox).toDouble())).toFloat().coerceIn(5f, 85f)
                }
            }
        ) {
            val w = size.width; val h = size.height
            drawRect(Brush.verticalGradient(listOf(Color(0xFFDCE9FA), Color(0xFFF6F8FC))))
            val groundY = h * 0.86f; val ox = w * 0.07f
            // scale: fit the furthest flight with margin, in whole 10 m steps
            val reach = max(listOf(speed * speed / g, (flights.maxOfOrNull { it.range } ?: 0f), (latest?.range ?: 0f)).maxOrNull() ?: 10f, 10f)
            val span = (ceil(reach / 10f) * 10f).coerceAtLeast(10f)
            val s = (w * 0.86f) / span
            // grid
            val stepM = if (span > 80) 20f else 10f
            var gx = 0f
            while (gx <= span) {
                val x = ox + gx * s
                drawLine(Color(0x22334466), Offset(x, groundY), Offset(x, 0f), 1f)
                drawText(measurer, "${gx.toInt()} m", Offset(x + 3f, groundY + 6f), TextStyle(fontSize = 10.sp, color = Color(0xFF475569)))
                gx += stepM
            }
            drawRect(Color(0xFF8FB39A), Offset(0f, groundY), Size(w, h - groundY))
            drawLine(Color(0xFF5E8A6B), Offset(0f, groundY), Offset(w, groundY), 2f)
            fun toPx(p: Offset) = Offset(ox + p.x * s, groundY - p.y * s)
            flights.forEachIndexed { i, f ->
                val path = Path(); f.pts.forEachIndexed { k, p -> val q = toPx(p); if (k == 0) path.moveTo(q.x, q.y) else path.lineTo(q.x, q.y) }
                drawPath(path, f.hue.copy(alpha = 0.35f + 0.5f / (i + 1)), style = Stroke(2.5f, cap = StrokeCap.Round, pathEffect = if (i > 0) PathEffect.dashPathEffect(floatArrayOf(10f, 8f)) else null))
                drawCircle(f.hue, 5f, toPx(f.pts.last()))
            }
            flying?.let { f ->
                val frac = (tNow / f.time).coerceIn(0f, 1f); val n = max(1, (f.pts.size * frac).toInt())
                val path = Path(); for (k in 0 until n) { val q = toPx(f.pts[k]); if (k == 0) path.moveTo(q.x, q.y) else path.lineTo(q.x, q.y) }
                drawPath(path, f.hue, style = Stroke(3f, cap = StrokeCap.Round))
                val ball = toPx(f.pts[n - 1])
                drawCircle(Color(0x33000000), 9f, Offset(ball.x, groundY))
                drawCircle(Color(0xFF1E2A4A), 9f, ball); drawCircle(Color.White.copy(alpha = 0.6f), 3f, Offset(ball.x - 3f, ball.y - 3f))
                if (f.height > 0f) { val top = f.pts.maxByOrNull { it.y }!!; drawLine(f.hue.copy(alpha = 0.4f), toPx(top), Offset(toPx(top).x, groundY), 1.5f, pathEffect = PathEffect.dashPathEffect(floatArrayOf(6f, 6f))) }
            }
            // the cannon
            rotate(-angle, Offset(ox, groundY - 6f)) {
                drawRoundRect(Color(0xFF1E2A4A), Offset(ox - 4f, groundY - 15f), Size(46f, 18f), androidx.compose.ui.geometry.CornerRadius(6f))
                drawRect(Color(0xFF3A4560), Offset(ox + 34f, groundY - 17f), Size(10f, 22f))
            }
            drawCircle(Color(0xFF6B4F2A), 13f, Offset(ox, groundY - 4f)); drawCircle(Color(0xFF3B2A16), 5f, Offset(ox, groundY - 4f))
            drawArc(Color(0xFF1E2A4A).copy(alpha = 0.5f), -angle, angle, false, Offset(ox - 40f, groundY - 46f), Size(80f, 80f), style = Stroke(1.5f))
            drawText(measurer, "${angle.toInt()}°", Offset(ox + 44f, groundY - 30f), TextStyle(fontSize = 11.sp, color = Color(0xFF1E2A4A)))
        }
        SimPanel {
            SimReadouts(listOf(
                "Range" to (latest?.let { "%.1f m".format(it.range) } ?: "—"),
                "Max height" to (latest?.let { "%.1f m".format(it.height) } ?: "—"),
                "Flight time" to (latest?.let { "%.2f s".format(it.time) } ?: "—"),
                "Ideal range v²sin2θ/g" to "%.1f m".format(speed * speed * sin(Math.toRadians(2.0 * angle)).toFloat() / g)
            ))
            SimSlider("Launch speed", speed, 5f..40f, { "%.0f m/s".format(it) }, { speed = it })
            SimSlider("Launch angle (or drag the cannon)", angle, 5f..85f, { "%.0f°".format(it) }, { angle = it })
            SimSlider("Gravity g", g, 1.6f..25f, { "%.2f m/s²".format(it) }, { g = it })
            SimSlider("Air resistance", drag, 0f..1f, { if (it == 0f) "off" else "%.0f %%".format(it * 100) }, { drag = it })
            Row {
                SimButton("Fire!") { if (flying == null) { flying = simulate(); shots++ } }
                Spacer(Modifier.width(10.dp))
                SimButton("Clear", primary = false) { flights.clear() }
            }
        }
    }
}
