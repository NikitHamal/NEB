package com.neb.ians.ui.sim.native2d

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import com.neb.ians.ui.sim.SimChips
import com.neb.ians.ui.sim.SimPanel
import com.neb.ians.ui.sim.SimReadouts
import com.neb.ians.ui.sim.SimSlider
import com.neb.ians.ui.sim.SimToggle
import com.neb.ians.ui.theme.nebAnimationsReduced
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.sin

/**
 * Waves natively: a travelling wave y = A sin(kx − ωt), a standing wave from two equal waves
 * running opposite ways (2A sin kx cos ωt, with fixed nodes every λ/2), and interference of two
 * waves of different frequency (beats in the envelope). The string is 4 m long on screen.
 */
@Composable
fun NativeWavesLab(modifier: Modifier = Modifier) {
    var mode by remember { mutableStateOf(0) }
    var f by remember { mutableFloatStateOf(1.0f) }
    var a by remember { mutableFloatStateOf(0.6f) }
    var v by remember { mutableFloatStateOf(2.0f) }
    var f2 by remember { mutableFloatStateOf(1.2f) }
    var a2 by remember { mutableFloatStateOf(0.6f) }
    var comps by remember { mutableStateOf(true) }
    val reduced = nebAnimationsReduced()
    val clock by produceState(0f, reduced) { if (!reduced) { val s = withFrameNanos { it }; while (true) withFrameNanos { value = (it - s) / 1e9f } } }
    val lambda = v / f
    Column(modifier) {
        Canvas(Modifier.fillMaxWidth().aspectRatio(16f / 9f)) {
            val t = clock
            drawRect(Color(0xFF0E1726))
            val w = size.width; val h = size.height; val mid = h / 2; val L = 4f; val s = w / L; val ay = h * 0.18f
            for (i in 0..8) { val x = i * w / 8; drawLine(Color(0x22FFFFFF), Offset(x, 0f), Offset(x, h), 1f) }
            drawLine(Color(0x44FFFFFF), Offset(0f, mid), Offset(w, mid), 1f)
            val k = (2 * PI / lambda).toFloat(); val om = (2 * PI * f).toFloat()
            fun curve(fn: (Float) -> Float, color: Color, width: Float, dash: Boolean = false) {
                val p = Path(); val n = 240
                for (i in 0..n) { val x = L * i / n; val y = fn(x); val px = x * s; val py = mid - y * ay; if (i == 0) p.moveTo(px, py) else p.lineTo(px, py) }
                drawPath(p, color, style = Stroke(width, cap = StrokeCap.Round, pathEffect = if (dash) PathEffect.dashPathEffect(floatArrayOf(8f, 8f)) else null))
            }
            when (mode) {
                0 -> {
                    curve({ x -> a * sin(k * x - om * t) }, Color(0xFF60A5FA), 4f)
                    val x0 = ((v * t) % L); val crest = Offset(x0 * s, mid - a * ay)
                    drawCircle(Color(0xFFFFCE5C), 6f, Offset(0.5f * s, mid - a * sin(k * 0.5f - om * t) * ay))
                    drawLine(Color(0x55FFCE5C), Offset(crest.x, 0f), Offset(crest.x, h), 1.5f, pathEffect = PathEffect.dashPathEffect(floatArrayOf(6f, 6f)))
                    drawLambda(this, lambda * s, mid + ay * 1.4f)
                }
                1 -> {
                    if (comps) { curve({ x -> a * sin(k * x - om * t) }, Color(0x6660A5FA), 2f, true); curve({ x -> a * sin(k * x + om * t) }, Color(0x66F472B6), 2f, true) }
                    curve({ x -> 2 * a * sin(k * x) * kotlin.math.cos(om * t) }, Color(0xFFFFFFFF), 4f)
                    var xn = 0f
                    while (xn <= L + 1e-3f) { drawCircle(Color(0xFFE5484D), 6f, Offset(xn * s, mid)); xn += lambda / 2 }
                }
                else -> {
                    val k2 = (2 * PI * f2 / v).toFloat(); val om2 = (2 * PI * f2).toFloat()
                    if (comps) { curve({ x -> a * sin(k * x - om * t) }, Color(0x6660A5FA), 2f, true); curve({ x -> a2 * sin(k2 * x - om2 * t) }, Color(0x66F472B6), 2f, true) }
                    curve({ x -> a * sin(k * x - om * t) + a2 * sin(k2 * x - om2 * t) }, Color(0xFFFFFFFF), 4f)
                }
            }
        }
        SimPanel {
            SimChips(listOf(0 to "Travelling wave", 1 to "Standing wave", 2 to "Interference"), mode) { mode = it }
            SimReadouts(listOf(
                "Wavelength λ = v/f" to "%.2f m".format(lambda),
                "Period T = 1/f" to "%.2f s".format(1 / f),
                if (mode == 2) "Beat frequency" to "%.2f Hz".format(abs(f2 - f)) else "Wave speed" to "%.1f m/s".format(v),
                if (mode == 1) "Node spacing λ/2" to "%.2f m".format(lambda / 2) else "Amplitude" to "%.2f".format(a)
            ))
            SimSlider("Frequency f", f, 0.2f..3f, { "%.2f Hz".format(it) }, { f = it })
            SimSlider("Amplitude A", a, 0.1f..1f, { "%.2f".format(it) }, { a = it })
            SimSlider("Wave speed v", v, 0.5f..4f, { "%.1f m/s".format(it) }, { v = it })
            if (mode == 2) {
                SimSlider("Wave 2 frequency", f2, 0.2f..3f, { "%.2f Hz".format(it) }, { f2 = it })
                SimSlider("Wave 2 amplitude", a2, 0.1f..1f, { "%.2f".format(it) }, { a2 = it })
            }
            if (mode != 0) SimToggle("Show components", comps) { comps = it }
        }
    }
}

private fun drawLambda(d: DrawScope, px: Float, y: Float) = with(d) {
    if (px > size.width * 0.95f) return@with
    val x0 = size.width * 0.1f
    drawLine(Color(0xFFFFCE5C), Offset(x0, y), Offset(x0 + px, y), 2f)
    drawLine(Color(0xFFFFCE5C), Offset(x0, y - 6f), Offset(x0, y + 6f), 2f)
    drawLine(Color(0xFFFFCE5C), Offset(x0 + px, y - 6f), Offset(x0 + px, y + 6f), 2f)
}
