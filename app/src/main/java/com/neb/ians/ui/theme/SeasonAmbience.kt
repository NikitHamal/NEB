package com.neb.ians.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.unit.dp
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.sin

/**
 * The festival in the air above Home's feed: a band at the top of the screen where marigold
 * petals tumble at Dashain, lights twinkle and fireflies drift at Tihar, gulal puffs burst at
 * Holi, gurans petals fall in spring, rain and snow in their seasons. A dozen or so shapes drawn
 * in the draw phase from one frame clock (no recomposition per frame), fading out down the band,
 * never touched by the pointer, and still for reduced motion or on an ordinary day.
 */
@Composable
fun Modifier.seasonAmbience(active: Boolean = true): Modifier {
    val state = LocalSiteTheme.current
    val key = state.theme?.key
    val kind = if (state.festive && key != "exams" && key != "everyday") key else null
    val reduced = nebAnimationsReduced()
    if (kind == null || reduced || !active) return this
    val clock by produceState(0f, kind) {
        val s0 = withFrameNanos { it }
        while (true) withFrameNanos { value = (it - s0) / 1e9f }
    }
    return this.drawWithContent {
        drawContent()
        val band = 260.dp.toPx().coerceAtMost(size.height)
        when (kind) {
            "dashain" -> petals(clock, band, listOf(Color(0xFFFFB020), Color(0xFFF97316), Color(0xFFFFD166)), 14)
            "tihar" -> { lights(clock); fireflies(clock, band) }
            "holi" -> puffs(clock, band)
            "new-year" -> petals(clock, band, listOf(Color(0xFFE11D48), Color(0xFFFB7185)), 12)
            "monsoon" -> rain(clock, band)
            "winter" -> snow(clock, band)
            else -> petals(clock, band, listOf(Color(0xFFFFD166)), 8)
        }
    }
}

private fun frac(x: Float) = x - kotlin.math.floor(x)
private fun fade(y: Float, band: Float) = (1f - y / band).coerceIn(0f, 1f)

private fun DrawScope.petals(t: Float, band: Float, colors: List<Color>, n: Int) {
    for (i in 0 until n) {
        val speed = 0.08f + (i % 4) * 0.02f
        val p = frac(t * speed + i * 0.37f)
        val y = p * band * 1.1f - 10f
        val x = size.width * frac(i * 0.173f + 0.05f) + sin(t * 0.9f + i) * 18.dp.toPx()
        val a = fade(y, band) * 0.85f
        val s = (5 + i % 3 * 2).dp.toPx()
        rotate(t * 90f + i * 40f, Offset(x, y)) {
            drawOval(colors[i % colors.size].copy(alpha = a), Offset(x - s / 2, y - s / 3), Size(s, s * 0.66f))
        }
    }
}

private fun DrawScope.lights(t: Float) {
    val n = 14; val y0 = 6.dp.toPx(); val sag = 14.dp.toPx()
    for (i in 0 until n) {
        val u = (i + 0.5f) / n
        val x = size.width * u
        val y = y0 + sag * sin(PI.toFloat() * frac(u * 3f))
        val tw = 0.55f + 0.45f * sin(t * 3f + i * 1.7f)
        val c = when (i % 3) { 0 -> Color(0xFFFFCF5C); 1 -> Color(0xFFFF8A65); else -> Color(0xFFC4B5FD) }
        drawCircle(Brush.radialGradient(listOf(c.copy(alpha = 0.5f * tw), Color.Transparent), Offset(x, y), 10.dp.toPx()), 10.dp.toPx(), Offset(x, y))
        drawCircle(c.copy(alpha = 0.6f + 0.4f * tw), 3.dp.toPx(), Offset(x, y))
    }
}

private fun DrawScope.fireflies(t: Float, band: Float) {
    for (i in 0 until 10) {
        val x = size.width * frac(i * 0.29f + 0.1f) + sin(t * 0.6f + i * 2f) * 24.dp.toPx()
        val y = band * (0.25f + 0.6f * frac(i * 0.41f)) + sin(t * 0.8f + i) * 14.dp.toPx()
        val a = (0.4f + 0.6f * abs(sin(t * 1.4f + i * 0.9f))) * fade(y, band * 1.1f)
        drawCircle(Brush.radialGradient(listOf(Color(0xFFFFE066).copy(alpha = 0.55f * a), Color.Transparent), Offset(x, y), 9.dp.toPx()), 9.dp.toPx(), Offset(x, y))
        drawCircle(Color(0xFFFFF3B0).copy(alpha = a), 1.8.dp.toPx(), Offset(x, y))
    }
}

private fun DrawScope.puffs(t: Float, band: Float) {
    val cs = listOf(Color(0xFFFF4FA1), Color(0xFFFFD23F), Color(0xFF28C7A6), Color(0xFF7C5CFF))
    for (i in 0 until 6) {
        val p = frac(t / 6f + i / 6f)
        val x = size.width * frac(i * 0.31f + 0.12f); val y = band * (0.2f + 0.5f * frac(i * 0.53f))
        val r = (24 + 70 * p).dp.toPx(); val a = (if (p < 0.12f) p / 0.12f else (1f - p)) * 0.28f
        drawCircle(Brush.radialGradient(listOf(cs[i % 4].copy(alpha = a), Color.Transparent), Offset(x, y), r), r, Offset(x, y))
    }
}

private fun DrawScope.rain(t: Float, band: Float) {
    for (i in 0 until 18) {
        val p = frac(t * 0.9f + i * 0.13f); val x = size.width * frac(i * 0.057f) - p * 20f; val y = p * band
        drawLine(Color(0xFF1565C0).copy(alpha = 0.35f * fade(y, band)), Offset(x, y), Offset(x - 6f, y + 22.dp.toPx()), 1.5f)
    }
}

private fun DrawScope.snow(t: Float, band: Float) {
    for (i in 0 until 16) {
        val p = frac(t * 0.07f + i * 0.21f); val y = p * band; val x = size.width * frac(i * 0.149f) + sin(t + i) * 10.dp.toPx()
        drawCircle(Color.White.copy(alpha = 0.9f * fade(y, band)), (2 + i % 3).dp.toPx(), Offset(x, y))
    }
}
