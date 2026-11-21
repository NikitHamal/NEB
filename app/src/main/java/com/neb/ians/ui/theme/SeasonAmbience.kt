package com.neb.ians.ui.theme

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.runtime.Composable
import androidx.compose.runtime.State
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.unit.dp
import com.neb.ians.util.rememberIsLowEndDevice
import kotlinx.coroutines.delay
import kotlin.math.abs
import kotlin.math.floor
import kotlin.math.sin

/** Keys of the festivals that hang a garland across the top of Home. */
private val GARLAND_KEYS = setOf("tihar", "dashain")

/** True while a festival with a garland is live, so a screen can leave room for it. */
val SiteThemeState.hasGarland: Boolean
    get() = festive && (theme?.key ?: "") in GARLAND_KEYS

/**
 * The festival in the air above Home's feed, drawn once into a layer of its own from one frame
 * clock (no recomposition per frame): a string of diyo lights with a few sparkles at Tihar, a
 * marigold mala with falling petals at Dashain, soft gulal clouds at Holi, gurans petals in
 * spring, rain and snow in their seasons. It lives in a band at the top of the screen, never
 * takes a touch, fades out when the feed scrolls, and holds still for reduced motion.
 * Flat colour only: no shadow, no blue or purple wash.
 */
@Composable
fun HomeSeasonAmbienceOverlay(
    listState: androidx.compose.foundation.lazy.LazyListState,
    modifier: Modifier = Modifier
) {
    val state = LocalSiteTheme.current
    val key = state.theme?.key
    val kind = if (state.festive && key != "exams" && key != "everyday") key else null
    if (kind == null) return
    val active by androidx.compose.runtime.remember(listState) {
        androidx.compose.runtime.derivedStateOf { listState.firstVisibleItemIndex == 0 }
    }
    val reduced = nebAnimationsReduced()
    val fadeState = animateFloatAsState(if (active) 1f else 0f, tween(240), label = "seasonFade")
    val clockState = festiveClock(running = !reduced && active)
    val scratchPath = androidx.compose.runtime.remember { Path() }
    androidx.compose.foundation.Canvas(modifier) {
        val a = fadeState.value
        if (a < 0.01f) return@Canvas
        val t = clockState.value
        when (kind) {
            "tihar" -> { lightsGarland(t, a, scratchPath); sparkles(t, a, scratchPath) }
            "dashain" -> { marigoldGarland(t, a, scratchPath); petals(t, a, DashainPetalColors, 9) }
            "holi" -> gulal(t, a)
            "new-year" -> petals(t, a, NewYearPetalColors, 10)
            "monsoon" -> rain(t, a)
            "winter" -> snow(t, a)
            else -> petals(t, a, DefaultPetalColors, 6)
        }
    }
}

private val DashainPetalColors = listOf(Color(0xFFFFB020), Color(0xFFF97316), Color(0xFFFFD166))
private val NewYearPetalColors = listOf(Color(0xFFE11D48), Color(0xFFFB7185), Color(0xFFBE123C))
private val DefaultPetalColors = listOf(Color(0xFFFFD166))
private val HoliGulalColors = listOf(Color(0xFFFF4FA1), Color(0xFFFFD23F), Color(0xFF28C7A6), Color(0xFFFF8A3D))

/**
 * Seconds since a festival animation started, ticking every frame; a slow phone ticks every other
 * frame, which leaves the frames between to the feed. Stays 0 when not [running].
 */
@Composable
internal fun festiveClock(running: Boolean): State<Float> {
    val lowEnd = rememberIsLowEndDevice()
    return produceState(0f, running, lowEnd) {
        if (!running) return@produceState
        val s0 = withFrameNanos { it }
        while (true) {
            withFrameNanos { value = (it - s0) / 1e9f }
            if (lowEnd) delay(LOW_END_FRAME_GAP_MS)
        }
    }
}

private const val LOW_END_FRAME_GAP_MS = 20L

private fun frac(x: Float) = x - floor(x)

/** The band the festival lives in; everything fades out down it. */
private fun DrawScope.band(): Float = 190.dp.toPx().coerceAtMost(size.height)
private fun fadeDown(y: Float, band: Float) = (1f - y / band).coerceIn(0f, 1f)

private const val SWAGS = 4
private const val TOP_DP = 3f
private const val SAG_DP = 12f

/** Draws the thread of a garland: a chain of [SWAGS] quadratic swags, same curve the web uses. */
private fun DrawScope.garlandThread(color: Color, path: Path) {
    val top = TOP_DP.dp.toPx()
    val sag = SAG_DP.dp.toPx()
    val w = size.width / SWAGS
    path.rewind()
    path.moveTo(0f, top)
    for (k in 0 until SWAGS) path.quadraticTo(w * k + w / 2f, top + 2f * sag, w * (k + 1), top)
    drawPath(path, color, style = Stroke(width = 1.4.dp.toPx(), cap = StrokeCap.Round))
}

/** Point `i` of `n` along the garland: x across the width, y exactly on the thread. */
private fun DrawScope.garlandPoint(i: Int, n: Int): Offset {
    val u = (i + 0.5f) / n * SWAGS
    val f = u - floor(u)
    val x = size.width * (i + 0.5f) / n
    val y = TOP_DP.dp.toPx() + SAG_DP.dp.toPx() * 4f * f * (1f - f)
    return Offset(x, y)
}

private val TiharBulbs = listOf(
    Color(0xFFFFB020), Color(0xFFFF7A18), Color(0xFFE5383B), Color(0xFFFF5C8A), Color(0xFFFFD23F),
)

/** Tihar: bulbs hanging on a thread, each with a little cap, a glass body and a warm glow. */
private fun DrawScope.lightsGarland(t: Float, alpha: Float, path: Path) {
    garlandThread(Color(0xFF7A4B2A).copy(alpha = 0.6f * alpha), path)
    val n = 20
    val capH = 4.dp.toPx()
    val capW = 5.dp.toPx()
    val capCorner = androidx.compose.ui.geometry.CornerRadius(1.5.dp.toPx())
    val gr = 12.dp.toPx()
    for (i in 0 until n) {
        val p = garlandPoint(i, n)
        val tw = 0.7f + 0.3f * sin(t * 2.4f + i * 1.3f)
        val c = TiharBulbs[i % TiharBulbs.size]
        val cx = p.x
        val by = p.y + capH + 5.dp.toPx()
        // cap
        drawRoundRect(
            Color(0xFF5A3A22).copy(alpha = alpha),
            topLeft = Offset(cx - 2.5.dp.toPx(), p.y),
            size = Size(capW, capH),
            cornerRadius = capCorner
        )
        // flat warm halo disc (zero gradient shader allocation)
        drawCircle(c.copy(alpha = 0.18f * tw * alpha), gr, Offset(cx, by))
        // glass body, slightly taller than wide
        drawOval(
            c.copy(alpha = (0.75f + 0.25f * tw) * alpha),
            topLeft = Offset(cx - 3.6.dp.toPx(), by - 4.8.dp.toPx()),
            size = Size(7.2.dp.toPx(), 9.6.dp.toPx())
        )
        // highlight
        drawCircle(Color.White.copy(alpha = 0.7f * alpha), 1.1.dp.toPx(), Offset(cx - 1.2.dp.toPx(), by - 2.2.dp.toPx()))
    }
}

/** A crisp four-point star. */
private fun DrawScope.star(center: Offset, r: Float, color: Color, path: Path) {
    val k = r * 0.28f
    path.rewind()
    path.moveTo(center.x, center.y - r)
    path.quadraticTo(center.x + k, center.y - k, center.x + r, center.y)
    path.quadraticTo(center.x + k, center.y + k, center.x, center.y + r)
    path.quadraticTo(center.x - k, center.y + k, center.x - r, center.y)
    path.quadraticTo(center.x - k, center.y - k, center.x, center.y - r)
    path.close()
    drawPath(path, color)
}

/** Tihar: a handful of small stars that twinkle in place below the lights, not blurred dots. */
private fun DrawScope.sparkles(t: Float, alpha: Float, path: Path) {
    val band = band()
    for (i in 0 until 7) {
        val x = size.width * (0.08f + 0.84f * frac(i * 0.381f + 0.11f))
        val y = 52.dp.toPx() + (band - 70.dp.toPx()) * 0.55f * frac(i * 0.619f + 0.2f)
        val tw = (sin(t * 1.6f + i * 2.1f) * 0.5f + 0.5f)
        val r = (2.6f + tw * 2.4f).dp.toPx()
        star(Offset(x, y), r, Color(0xFFFFB020).copy(alpha = (0.25f + 0.6f * tw) * fadeDown(y, band) * alpha), path)
    }
}

/** One marigold: eight petals around a dark eye. */
private fun DrawScope.marigold(center: Offset, r: Float, petal: Color, eye: Color, turn: Float, alpha: Float) {
    for (j in 0 until 8) {
        rotate(j * 45f + turn, center) {
            drawOval(
                petal.copy(alpha = alpha),
                topLeft = Offset(center.x - r * 0.3f, center.y - r),
                size = Size(r * 0.6f, r * 0.95f)
            )
        }
    }
    drawCircle(eye.copy(alpha = alpha), r * 0.34f, center)
}

/** Dashain: a mala of marigolds strung on the thread, each swaying a little on its own beat. */
private fun DrawScope.marigoldGarland(t: Float, alpha: Float, path: Path) {
    garlandThread(Color(0xFF6B8E23).copy(alpha = 0.7f * alpha), path)
    val n = 24
    for (i in 0 until n) {
        val p = garlandPoint(i, n)
        val warm = i % 2 == 0
        marigold(
            center = Offset(p.x, p.y + 4.dp.toPx()),
            r = 7.dp.toPx(),
            petal = if (warm) Color(0xFFFFB020) else Color(0xFFF97316),
            eye = if (warm) Color(0xFF9A3412) else Color(0xFF7C2D12),
            turn = sin(t * 0.9f + i * 0.7f) * 8f + i * 11f,
            alpha = alpha
        )
    }
}

/** Petals tumbling down the band: flat ovals, turning, fading as they fall. */
private fun DrawScope.petals(t: Float, alpha: Float, colors: List<Color>, n: Int) {
    val band = band()
    for (i in 0 until n) {
        val speed = 0.07f + (i % 4) * 0.018f
        val p = frac(t * speed + i * 0.37f)
        val y = 30.dp.toPx() + p * (band - 30.dp.toPx())
        val x = size.width * frac(i * 0.173f + 0.05f) + sin(t * 0.9f + i) * 16.dp.toPx()
        val a = fadeDown(y, band) * 0.9f * alpha
        val s = (6 + i % 3 * 2).dp.toPx()
        rotate(t * 70f + i * 40f, Offset(x, y)) {
            drawOval(colors[i % colors.size].copy(alpha = a), Offset(x - s / 2, y - s / 3), Size(s, s * 0.66f))
        }
    }
}

/** Holi: soft flat discs of gulal drifting in from the top corners. */
private fun DrawScope.gulal(t: Float, alpha: Float) {
    val band = band()
    for (i in 0 until 4) {
        val p = frac(t / 14f + i / 4f)
        val x = size.width * (0.1f + 0.8f * frac(i * 0.37f + 0.1f)) + sin(t * 0.4f + i) * 18.dp.toPx()
        val y = band * (0.1f + 0.35f * frac(i * 0.53f))
        val r = (48 + 38 * abs(sin(p * 6.2831f))).dp.toPx()
        drawCircle(HoliGulalColors[i].copy(alpha = 0.14f * alpha), r, Offset(x, y))
    }
}

/** Monsoon: thin slanted streaks of rain. */
private fun DrawScope.rain(t: Float, alpha: Float) {
    val band = band()
    for (i in 0 until 20) {
        val p = frac(t * 0.9f + i * 0.13f)
        val x = size.width * frac(i * 0.057f + 0.02f) - p * 20f
        val y = p * band
        drawLine(
            Color(0xFF3B7DB5).copy(alpha = 0.5f * fadeDown(y, band) * alpha),
            Offset(x, y), Offset(x - 6f, y + 20.dp.toPx()), 1.6.dp.toPx(), StrokeCap.Round
        )
    }
}

/** Winter: slow flakes, tinted so they read on a white page. */
private fun DrawScope.snow(t: Float, alpha: Float) {
    val band = band()
    for (i in 0 until 18) {
        val p = frac(t * 0.07f + i * 0.21f)
        val y = p * band
        val x = size.width * frac(i * 0.149f) + sin(t + i) * 10.dp.toPx()
        drawCircle(Color(0xFF8FB0D6).copy(alpha = 0.85f * fadeDown(y, band) * alpha), (2 + i % 3).dp.toPx(), Offset(x, y))
    }
}
