package com.neb.ians.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.graphics.luminance
import com.neb.ians.ui.theme.SubjectTheme
import com.neb.ians.ui.theme.getSubjectTheme
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

/**
 * The illustrated banner a library resource falls back to when it has no
 * thumbnail of its own.
 *
 * There used to be one drawing — three stacked waves — so every card without a
 * thumbnail was the same picture in a different hue, and a shelf of them looked
 * like a printing error. There are twenty-four drawings now, each seeded from
 * the resource itself, so a rail of cards reads as twenty-four different things
 * that happen to share a palette.
 *
 * Everything here is drawn from two colours: an ink and a paper, both derived
 * from the subject's own tint against the current surface. That is the whole
 * trick to surviving dark mode — nothing is hardcoded, so the same geometry
 * that reads as navy line-work on a pale field reads as pale line-work on navy
 * without a second set of numbers to keep in sync.
 */
@Composable
fun ResourceBannerArt(
    seed: String,
    subject: String,
    modifier: Modifier = Modifier
) {
    val theme = getSubjectTheme(subject)
    val surface = MaterialTheme.colorScheme.surface
    val isDark = surface.luminance() < 0.5f
    val palette = remember(theme, surface, isDark) { bannerPalette(theme, surface, isDark) }
    val hash = remember(seed) { stableSeed(seed) }

    Canvas(modifier = modifier.clipToBounds()) {
        drawField(palette)
        drawBannerArt((hash ushr 3) and 0x7FFFFFFF, palette, Rng(hash))
    }
}

/** How many distinct drawings [drawBannerArt] can produce. */
const val BANNER_ART_COUNT = 24

/**
 * The two colours every drawing is made of, plus the field they sit on.
 *
 * [top] and [bottom] are a deliberately shallow gradient: the top of the banner
 * carries the type pill and the price badge, so it stays the quiet end, and the
 * art gathers weight toward the bottom where nothing overlaps it.
 */
class BannerPalette(
    val top: Color,
    val bottom: Color,
    val ink: Color,
    val paper: Color,
    /**
     * The field colour where the art sits, for shapes that need to subtract
     * rather than add — a crescent is a disc with a hole, and the hole has to
     * be the background in both modes, not a highlight in one and a shadow in
     * the other.
     */
    val field: Color
)

/**
 * Light mode pulls the subject container toward white; dark mode pulls it
 * toward the page. Both end up a few percent away from the surface rather than
 * a saturated slab, which is what keeps a grid of these calm instead of loud.
 */
fun bannerPalette(theme: SubjectTheme, surface: Color, isDark: Boolean): BannerPalette {
    return if (isDark) {
        BannerPalette(
            top = lerp(theme.container, surface, 0.58f),
            bottom = lerp(theme.container, surface, 0.12f),
            ink = theme.color,
            // Not a tint of the container. "Paper" means the lightest surface
            // in the drawing, and on navy the lightest thing available is the
            // subject's own light-mode-ish hue pushed toward white. Tinting the
            // container instead gave us highlights darker than the shapes they
            // were meant to lift off, and every cut-out read as a hole.
            paper = lerp(theme.color, Color.White, 0.34f),
            field = lerp(lerp(theme.container, surface, 0.58f), lerp(theme.container, surface, 0.12f), 0.55f)
        )
    } else {
        BannerPalette(
            top = lerp(theme.container, Color.White, 0.62f),
            bottom = lerp(theme.container, Color.White, 0.14f),
            ink = theme.color,
            paper = Color.White,
            field = lerp(lerp(theme.container, Color.White, 0.62f), lerp(theme.container, Color.White, 0.14f), 0.55f)
        )
    }
}

/** The backdrop. Drawn once, under every composition. */
fun DrawScope.drawField(p: BannerPalette) {
    drawRect(brush = Brush.verticalGradient(listOf(p.top, p.bottom)))
}

/**
 * FNV-1a over the seed string. Any stable hash would do; this one is four lines
 * and gives the low bits enough movement that `% 24` is not biased toward the
 * first few drawings.
 */
fun stableSeed(key: String): Int {
    var h = -2128831035
    for (ch in key) {
        h = h xor ch.code
        h *= 16777619
    }
    return h
}

/**
 * xorshift32. Each drawing gets one of these so that two cards landing on the
 * same composition still differ — different peaks on the mountains, different
 * stars in the constellation — without either of them ever changing between
 * two launches of the app.
 */
class Rng(seed: Int) {
    private var s: Int = if (seed == 0) 1 else seed

    fun next(): Float {
        s = s xor (s shl 13)
        s = s xor (s ushr 17)
        s = s xor (s shl 5)
        return ((s ushr 8) and 0xFFFFFF) / 16777216f
    }

    fun range(a: Float, b: Float): Float = a + (b - a) * next()

    fun int(n: Int): Int {
        val v = (next() * n).toInt()
        return if (v >= n) n - 1 else v
    }
}

fun DrawScope.drawBannerArt(index: Int, p: BannerPalette, r: Rng) {
    when (index % BANNER_ART_COUNT) {
        0 -> artArcs(p, r)
        1 -> artHorizon(p, r)
        2 -> artDotMatrix(p, r)
        3 -> artAtom(p, r)
        4 -> artBars(p, r)
        5 -> artWaveform(p, r)
        6 -> artContours(p, r)
        7 -> artMolecule(p, r)
        8 -> artPrism(p, r)
        9 -> artPages(p, r)
        10 -> artConstellation(p, r)
        11 -> artSteps(p, r)
        12 -> artCircuit(p, r)
        13 -> artHelix(p, r)
        14 -> artRipple(p, r)
        15 -> artHatch(p, r)
        16 -> artPeaks(p, r)
        17 -> artBloom(p, r)
        18 -> artLedger(p, r)
        19 -> artSineField(p, r)
        20 -> artChevrons(p, r)
        21 -> artEclipse(p, r)
        22 -> artShelf(p, r)
        else -> artComet(p, r)
    }
}

// ---------------------------------------------------------------------------
// The drawings.
//
// Every one of them is written in the same narrow dialect — locals, `for`,
// `if`, explicit `path.` receivers, no `apply`, no helper functions. That is not
// stylistic: /tmp keeps a renderer that parses this file directly to produce
// contact sheets, and the dialect is what it understands. If you reach for a
// language feature here, the previews stop being previews.
// ---------------------------------------------------------------------------

private fun DrawScope.artArcs(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val ox = w * 0.05f
    val oy = h * 1.00f
    for (i in 0 until 6) {
        val rad = h * (0.24f + i * 0.33f)
        drawArc(
            color = p.ink.copy(alpha = 0.42f - i * 0.055f),
            startAngle = -92f,
            sweepAngle = 94f,
            useCenter = false,
            topLeft = Offset(ox - rad, oy - rad),
            size = Size(rad * 2f, rad * 2f),
            style = Stroke(width = h * 0.028f, cap = StrokeCap.Round)
        )
    }
    drawCircle(color = p.ink, radius = h * 0.055f, center = Offset(ox, oy))
    drawCircle(
        color = p.ink.copy(alpha = 0.55f),
        radius = h * 0.048f,
        center = Offset(w * r.range(0.62f, 0.82f), h * 0.26f)
    )
}

private fun DrawScope.artHorizon(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val sunX = w * r.range(0.60f, 0.80f)
    drawCircle(color = p.ink.copy(alpha = 0.80f), radius = h * 0.165f, center = Offset(sunX, h * 0.34f))

    val back = Path()
    back.moveTo(0f, h)
    back.lineTo(0f, h * 0.66f)
    back.cubicTo(w * 0.22f, h * 0.46f, w * 0.38f, h * 0.74f, w * 0.58f, h * 0.60f)
    back.cubicTo(w * 0.76f, h * 0.48f, w * 0.88f, h * 0.66f, w, h * 0.56f)
    back.lineTo(w, h)
    back.close()
    drawPath(path = back, color = p.ink.copy(alpha = 0.26f))

    val front = Path()
    front.moveTo(0f, h)
    front.lineTo(0f, h * 0.86f)
    front.cubicTo(w * 0.24f, h * 0.70f, w * 0.44f, h * 0.94f, w * 0.66f, h * 0.80f)
    front.cubicTo(w * 0.82f, h * 0.70f, w * 0.92f, h * 0.82f, w, h * 0.76f)
    front.lineTo(w, h)
    front.close()
    drawPath(path = front, color = p.ink.copy(alpha = 0.54f))

    for (i in 0 until 2) {
        drawLine(
            color = p.paper.copy(alpha = 0.55f - i * 0.18f),
            start = Offset(w * (0.07f + i * 0.05f), h * (0.22f + i * 0.11f)),
            end = Offset(w * (0.24f - i * 0.04f), h * (0.22f + i * 0.11f)),
            strokeWidth = h * 0.030f,
            cap = StrokeCap.Round
        )
    }
}

private fun DrawScope.artDotMatrix(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cols = 12
    val rows = 4
    for (yi in 0 until rows) {
        for (xi in 0 until cols) {
            val fx = (xi + 0.5f) / cols
            val fy = (yi + 0.5f) / rows
            val rad = h * 0.034f * (0.50f + fy * 0.95f) * (1.22f - fx * 0.62f)
            drawCircle(
                color = p.ink.copy(alpha = 0.14f + fy * 0.34f),
                radius = rad,
                center = Offset(w * fx, h * (0.16f + fy * 0.74f))
            )
        }
    }
    val ai = r.int(cols - 4) + 2
    val ax = w * ((ai + 0.5f) / cols)
    drawCircle(color = p.ink, radius = h * 0.088f, center = Offset(ax, h * 0.53f))
    drawCircle(color = p.ink.copy(alpha = 0.55f), radius = h * 0.052f, center = Offset(ax, h * 0.16f))
}

private fun DrawScope.artAtom(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cx = w * 0.50f
    val cy = h * 0.54f
    val rx = h * 0.44f
    val ry = h * 0.17f
    val spin = r.range(0f, 60f)
    for (i in 0 until 3) {
        rotate(degrees = spin + i * 60f, pivot = Offset(cx, cy)) {
            drawArc(
                color = p.ink.copy(alpha = 0.58f - i * 0.09f),
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                topLeft = Offset(cx - rx, cy - ry),
                size = Size(rx * 2f, ry * 2f),
                style = Stroke(width = h * 0.024f)
            )
        }
    }
    rotate(degrees = spin, pivot = Offset(cx, cy)) {
        drawCircle(color = p.ink, radius = h * 0.052f, center = Offset(cx + rx, cy))
    }
    drawCircle(color = p.ink, radius = h * 0.090f, center = Offset(cx, cy))
    drawCircle(color = p.paper.copy(alpha = 0.70f), radius = h * 0.034f, center = Offset(cx, cy))
}

private fun DrawScope.artBars(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val n = 7
    val baseY = h * 0.86f
    val bw = w / (n * 2.0f)
    val gap = w / n
    val trend = Path()
    for (i in 0 until n) {
        val f = i / (n - 1f)
        val bh = h * (0.14f + f * 0.46f + r.range(0f, 0.12f))
        val x = gap * i + (gap - bw) * 0.5f
        val topY = baseY - bh
        drawRect(
            color = p.ink.copy(alpha = 0.28f + f * 0.34f),
            topLeft = Offset(x, topY),
            size = Size(bw, bh)
        )
        drawCircle(
            color = p.ink.copy(alpha = 0.28f + f * 0.34f),
            radius = bw * 0.5f,
            center = Offset(x + bw * 0.5f, topY)
        )
        if (i == 0) {
            trend.moveTo(x + bw * 0.5f, topY - h * 0.10f)
        } else {
            trend.lineTo(x + bw * 0.5f, topY - h * 0.10f)
        }
    }
    drawPath(path = trend, color = p.ink, style = Stroke(width = h * 0.026f, cap = StrokeCap.Round))
    drawLine(
        color = p.ink.copy(alpha = 0.30f),
        start = Offset(0f, baseY),
        end = Offset(w, baseY),
        strokeWidth = h * 0.014f
    )
}

private fun DrawScope.artWaveform(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val n = 20
    val mid = h * 0.54f
    val phase = r.range(0f, 6.2f)
    for (i in 0 until n) {
        val f = (i + 0.5f) / n
        val env = abs(sin(f * PI.toFloat() * 2.3f + phase))
        val amp = h * (0.07f + 0.32f * env) + h * r.range(0f, 0.05f)
        val x = w * f
        drawLine(
            color = p.ink.copy(alpha = 0.30f + 0.50f * env),
            start = Offset(x, mid - amp),
            end = Offset(x, mid + amp),
            strokeWidth = w / (n * 3.4f),
            cap = StrokeCap.Round
        )
    }
    drawLine(
        color = p.paper.copy(alpha = 0.45f),
        start = Offset(0f, mid),
        end = Offset(w, mid),
        strokeWidth = h * 0.010f
    )
}

private fun DrawScope.artContours(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val k = 0.5523f
    val cx = w * r.range(0.46f, 0.62f)
    val cy = h * 0.54f
    for (i in 0 until 6) {
        val s = 0.13f + i * 0.155f
        val rx = w * 0.52f * s + w * 0.02f
        val ry = h * 1.05f * s + h * 0.04f
        val ox = cx + w * 0.02f * i * r.range(-1f, 1f)
        val oy = cy + h * 0.03f * i * r.range(-1f, 1f)
        val path = Path()
        path.moveTo(ox, oy - ry)
        path.cubicTo(ox + rx * k, oy - ry, ox + rx, oy - ry * k, ox + rx, oy)
        path.cubicTo(ox + rx, oy + ry * k, ox + rx * k, oy + ry, ox, oy + ry)
        path.cubicTo(ox - rx * k, oy + ry, ox - rx, oy + ry * k, ox - rx, oy)
        path.cubicTo(ox - rx, oy - ry * k, ox - rx * k, oy - ry, ox, oy - ry)
        path.close()
        drawPath(
            path = path,
            color = p.ink.copy(alpha = 0.54f - i * 0.070f),
            style = Stroke(width = h * 0.022f)
        )
    }
    drawCircle(color = p.ink, radius = h * 0.045f, center = Offset(cx, cy))
}

private fun DrawScope.artMolecule(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cx = w * 0.52f
    val cy = h * 0.54f
    val rad = h * 0.33f
    val spin = r.range(0f, 1.2f)
    for (i in 0 until 5) {
        val a = spin + i * (PI.toFloat() * 2f / 5f)
        val nx = cx + cos(a) * rad * (w / h) * 0.42f
        val ny = cy + sin(a) * rad
        drawLine(
            color = p.ink.copy(alpha = 0.48f),
            start = Offset(cx, cy),
            end = Offset(nx, ny),
            strokeWidth = h * 0.020f,
            cap = StrokeCap.Round
        )
        drawCircle(color = p.ink.copy(alpha = 0.85f), radius = h * 0.072f, center = Offset(nx, ny))
        drawCircle(color = p.paper.copy(alpha = 0.60f), radius = h * 0.026f, center = Offset(nx, ny))
    }
    drawCircle(color = p.ink, radius = h * 0.105f, center = Offset(cx, cy))
    drawCircle(color = p.paper.copy(alpha = 0.72f), radius = h * 0.038f, center = Offset(cx, cy))
}

private fun DrawScope.artPrism(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cx = w * 0.42f
    val cy = h * 0.52f
    val s = h * 0.34f
    val tri = Path()
    tri.moveTo(cx, cy - s)
    tri.lineTo(cx + s * 0.92f, cy + s * 0.70f)
    tri.lineTo(cx - s * 0.92f, cy + s * 0.70f)
    tri.close()
    drawPath(path = tri, color = p.ink.copy(alpha = 0.20f))
    drawPath(path = tri, color = p.ink.copy(alpha = 0.80f), style = Stroke(width = h * 0.026f))

    drawLine(
        color = p.ink.copy(alpha = 0.68f),
        start = Offset(0f, cy - h * 0.20f),
        end = Offset(cx - s * 0.30f, cy - h * 0.02f),
        strokeWidth = h * 0.024f,
        cap = StrokeCap.Round
    )
    for (i in 0 until 4) {
        val spread = (i - 1.5f) * h * 0.17f + r.range(-0.02f, 0.02f) * h
        drawLine(
            color = p.ink.copy(alpha = 0.62f - i * 0.10f),
            start = Offset(cx + s * 0.30f, cy + h * 0.02f),
            end = Offset(w, cy + spread),
            strokeWidth = h * 0.022f,
            cap = StrokeCap.Round
        )
    }
}

private fun DrawScope.artPages(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val pw = h * 0.46f
    val ph = h * 0.60f
    val cx = w * r.range(0.44f, 0.58f)
    val cy = h * 0.54f
    for (i in 0 until 3) {
        val inset = (2 - i) * h * 0.075f
        val x = cx - pw * 0.5f - inset
        val y = cy - ph * 0.5f - inset * 0.6f
        drawRect(
            color = if (i == 2) p.paper.copy(alpha = 0.92f) else p.ink.copy(alpha = 0.16f + i * 0.08f),
            topLeft = Offset(x, y),
            size = Size(pw, ph)
        )
        drawRect(
            color = p.ink.copy(alpha = 0.55f),
            topLeft = Offset(x, y),
            size = Size(pw, ph),
            style = Stroke(width = h * 0.018f)
        )
    }
    val fx = cx - pw * 0.5f + pw
    val fy = cy - ph * 0.5f
    val fold = Path()
    fold.moveTo(fx - pw * 0.30f, fy)
    fold.lineTo(fx, fy + ph * 0.30f)
    fold.lineTo(fx - pw * 0.30f, fy + ph * 0.30f)
    fold.close()
    drawPath(path = fold, color = p.ink.copy(alpha = 0.46f))
    for (i in 0 until 3) {
        val ly = fy + ph * (0.50f + i * 0.15f)
        drawLine(
            color = p.ink.copy(alpha = 0.50f),
            start = Offset(fx - pw * 0.78f, ly),
            end = Offset(fx - pw * (0.22f + i * 0.14f), ly),
            strokeWidth = h * 0.017f,
            cap = StrokeCap.Round
        )
    }
}

private fun DrawScope.artConstellation(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val link = Path()
    var bx = 0f
    var by = 0f
    for (i in 0 until 6) {
        val f = (i + 0.5f) / 6f
        val x = w * (0.10f + f * 0.80f) + w * r.range(-0.035f, 0.035f)
        val y = h * (0.34f + sin(f * 5.4f) * 0.22f) + h * r.range(-0.06f, 0.06f)
        if (i == 0) {
            link.moveTo(x, y)
        } else {
            link.lineTo(x, y)
        }
        drawCircle(color = p.ink.copy(alpha = 0.90f), radius = h * (0.030f + r.range(0f, 0.026f)), center = Offset(x, y))
        if (i == 3) {
            bx = x
            by = y
        }
    }
    drawPath(path = link, color = p.ink.copy(alpha = 0.44f), style = Stroke(width = h * 0.016f))
    drawCircle(color = p.ink, radius = h * 0.062f, center = Offset(bx, by))
    drawCircle(
        color = p.ink.copy(alpha = 0.35f),
        radius = h * 0.135f,
        center = Offset(bx, by),
        style = Stroke(width = h * 0.014f)
    )
    for (i in 0 until 9) {
        drawCircle(
            color = p.ink.copy(alpha = 0.16f + r.range(0f, 0.14f)),
            radius = h * 0.013f,
            center = Offset(w * r.range(0.02f, 0.98f), h * r.range(0.06f, 0.94f))
        )
    }
}

private fun DrawScope.artSteps(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val bw = w * 0.15f
    val rise = h * 0.15f
    val skew = h * 0.16f
    val baseY = h * 0.92f
    val x0 = w * r.range(0.10f, 0.20f)
    for (i in 0 until 4) {
        val x = x0 + i * bw * 0.82f
        val y = baseY - i * rise
        val top = Path()
        top.moveTo(x, y)
        top.lineTo(x + bw * 0.62f, y - skew)
        top.lineTo(x + bw, y)
        top.lineTo(x + bw * 0.38f, y + skew)
        top.close()
        drawPath(path = top, color = p.ink.copy(alpha = 0.66f - i * 0.06f))
        val face = Path()
        face.moveTo(x, y)
        face.lineTo(x + bw * 0.38f, y + skew)
        face.lineTo(x + bw * 0.38f, y + skew + rise)
        face.lineTo(x, y + rise)
        face.close()
        drawPath(path = face, color = p.ink.copy(alpha = 0.36f))
        val side = Path()
        side.moveTo(x + bw * 0.38f, y + skew)
        side.lineTo(x + bw, y)
        side.lineTo(x + bw, y + rise)
        side.lineTo(x + bw * 0.38f, y + skew + rise)
        side.close()
        drawPath(path = side, color = p.ink.copy(alpha = 0.18f))
    }
}

private fun DrawScope.artCircuit(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    for (i in 0 until 3) {
        val y = h * (0.26f + i * 0.24f)
        val turn = w * r.range(0.30f, 0.62f)
        val y2 = y + h * (r.range(0.10f, 0.22f))
        val trace = Path()
        trace.moveTo(0f, y)
        trace.lineTo(turn, y)
        trace.lineTo(turn + h * 0.16f, y2)
        trace.lineTo(w, y2)
        drawPath(
            path = trace,
            color = p.ink.copy(alpha = 0.55f - i * 0.08f),
            style = Stroke(width = h * 0.022f, cap = StrokeCap.Round)
        )
        drawCircle(color = p.ink.copy(alpha = 0.80f), radius = h * 0.042f, center = Offset(turn, y))
        drawCircle(color = p.paper.copy(alpha = 0.75f), radius = h * 0.016f, center = Offset(turn, y))
    }
    val bx = w * 0.72f
    val by = h * 0.62f
    drawRect(
        color = p.ink.copy(alpha = 0.24f),
        topLeft = Offset(bx, by),
        size = Size(h * 0.34f, h * 0.30f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.75f),
        topLeft = Offset(bx, by),
        size = Size(h * 0.34f, h * 0.30f),
        style = Stroke(width = h * 0.020f)
    )
}

private fun DrawScope.artHelix(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val mid = h * 0.52f
    val amp = h * 0.28f
    val phase = r.range(0f, 3.1f)
    val turns = 2.4f
    val a = Path()
    val b = Path()
    for (i in 0 until 41) {
        val f = i / 40f
        val t = phase + f * turns * PI.toFloat() * 2f
        val x = w * f
        if (i == 0) {
            a.moveTo(x, mid + sin(t) * amp)
            b.moveTo(x, mid - sin(t) * amp)
        } else {
            a.lineTo(x, mid + sin(t) * amp)
            b.lineTo(x, mid - sin(t) * amp)
        }
    }
    drawPath(path = a, color = p.ink.copy(alpha = 0.72f), style = Stroke(width = h * 0.026f, cap = StrokeCap.Round))
    drawPath(path = b, color = p.ink.copy(alpha = 0.38f), style = Stroke(width = h * 0.026f, cap = StrokeCap.Round))
    for (i in 0 until 11) {
        val f = (i + 0.5f) / 11f
        val t = phase + f * turns * PI.toFloat() * 2f
        val x = w * f
        drawLine(
            color = p.ink.copy(alpha = 0.30f),
            start = Offset(x, mid + sin(t) * amp),
            end = Offset(x, mid - sin(t) * amp),
            strokeWidth = h * 0.016f,
            cap = StrokeCap.Round
        )
    }
}

private fun DrawScope.artRipple(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cx = w * r.range(0.74f, 0.90f)
    val cy = h * 0.52f
    for (i in 0 until 7) {
        val rad = h * (0.10f + i * 0.20f)
        drawCircle(
            color = p.ink.copy(alpha = 0.52f - i * 0.062f),
            radius = rad,
            center = Offset(cx, cy),
            style = Stroke(width = h * 0.024f)
        )
    }
    drawCircle(color = p.ink, radius = h * 0.062f, center = Offset(cx, cy))
    drawCircle(color = p.ink.copy(alpha = 0.30f), radius = h * 0.030f, center = Offset(w * 0.12f, h * 0.30f))
    drawCircle(color = p.ink.copy(alpha = 0.22f), radius = h * 0.020f, center = Offset(w * 0.20f, h * 0.72f))
}

private fun DrawScope.artHatch(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val n = 15
    val span = w + h
    val off = r.range(0f, 1f)
    for (i in 0 until n) {
        val f = (i + off) / n
        val x = f * span - h
        drawLine(
            color = p.ink.copy(alpha = 0.09f + 0.19f * (1f - f)),
            start = Offset(x, 0f),
            end = Offset(x + h, h),
            strokeWidth = h * 0.022f
        )
    }
    val bx = w * 0.56f
    val by = h * 0.24f
    val bw = w * 0.34f
    val bh = h * 0.52f
    drawRect(color = p.paper.copy(alpha = 0.90f), topLeft = Offset(bx, by), size = Size(bw, bh))
    drawRect(
        color = p.ink.copy(alpha = 0.70f),
        topLeft = Offset(bx, by),
        size = Size(bw, bh),
        style = Stroke(width = h * 0.020f)
    )
    for (i in 0 until 3) {
        drawLine(
            color = p.ink.copy(alpha = 0.52f),
            start = Offset(bx + bw * 0.14f, by + bh * (0.28f + i * 0.22f)),
            end = Offset(bx + bw * (0.86f - i * 0.18f), by + bh * (0.28f + i * 0.22f)),
            strokeWidth = h * 0.017f,
            cap = StrokeCap.Round
        )
    }
}

private fun DrawScope.artPeaks(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val baseY = h * 0.94f
    val back = Path()
    back.moveTo(0f, baseY)
    for (i in 0 until 5) {
        val f = i / 4f
        back.lineTo(w * (f + 0.06f), baseY - h * (0.30f + r.range(0f, 0.26f)))
        back.lineTo(w * (f + 0.14f), baseY - h * 0.10f)
    }
    back.lineTo(w, baseY)
    back.close()
    drawPath(path = back, color = p.ink.copy(alpha = 0.28f))

    val px = w * r.range(0.36f, 0.56f)
    val peakY = baseY - h * 0.66f
    val front = Path()
    front.moveTo(w * 0.04f, baseY)
    front.lineTo(px, peakY)
    front.lineTo(w * 0.82f, baseY)
    front.close()
    drawPath(path = front, color = p.ink.copy(alpha = 0.58f))

    // The cap has to land on the mountain's own edges or it floats. Both
    // sides are solved for the height we drop to rather than guessed at.
    val drop = h * 0.24f
    val t = drop / (h * 0.66f)
    val lx = px - (px - w * 0.04f) * t
    val rx = px + (w * 0.82f - px) * t
    val span = rx - lx
    val cap = Path()
    cap.moveTo(px, peakY)
    cap.lineTo(rx, peakY + drop)
    cap.lineTo(rx - span * 0.20f, peakY + drop * 0.62f)
    cap.lineTo(rx - span * 0.42f, peakY + drop * 1.00f)
    cap.lineTo(rx - span * 0.68f, peakY + drop * 0.58f)
    cap.lineTo(lx, peakY + drop * 0.90f)
    cap.close()
    drawPath(path = cap, color = p.paper.copy(alpha = 0.85f))
    drawCircle(color = p.ink.copy(alpha = 0.55f), radius = h * 0.075f, center = Offset(w * 0.86f, h * 0.28f))
}

private fun DrawScope.artBloom(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cx = w * 0.50f
    val cy = h * 0.56f
    val len = h * 0.42f
    val spin = r.range(0f, 60f)
    for (i in 0 until 6) {
        rotate(degrees = spin + i * 60f, pivot = Offset(cx, cy)) {
            val petal = Path()
            petal.moveTo(cx + len * 0.16f, cy)
            petal.cubicTo(cx + len * 0.46f, cy - len * 0.30f, cx + len * 0.88f, cy - len * 0.18f, cx + len, cy)
            petal.cubicTo(cx + len * 0.88f, cy + len * 0.18f, cx + len * 0.46f, cy + len * 0.30f, cx + len * 0.16f, cy)
            petal.close()
            drawPath(path = petal, color = p.ink.copy(alpha = 0.20f + (i % 2) * 0.12f))
            drawPath(path = petal, color = p.ink.copy(alpha = 0.52f), style = Stroke(width = h * 0.016f))
        }
    }
    drawCircle(color = p.ink, radius = h * 0.072f, center = Offset(cx, cy))
    drawCircle(color = p.paper.copy(alpha = 0.70f), radius = h * 0.026f, center = Offset(cx, cy))
}

private fun DrawScope.artLedger(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val left = w * 0.13f
    val right = w * 0.90f
    val rule = left - w * 0.045f
    drawLine(
        color = p.ink.copy(alpha = 0.30f),
        start = Offset(rule, h * 0.12f),
        end = Offset(rule, h * 0.90f),
        strokeWidth = h * 0.016f
    )
    val hot = r.int(4) + 1
    for (i in 0 until 6) {
        val y = h * (0.19f + i * 0.126f)
        val end = left + (right - left) * r.range(0.42f, 1.0f)
        if (i == hot) {
            drawRect(
                color = p.ink.copy(alpha = 0.18f),
                topLeft = Offset(left - w * 0.014f, y - h * 0.055f),
                size = Size(end - left + w * 0.028f, h * 0.110f)
            )
        }
        drawLine(
            color = p.ink.copy(alpha = if (i == hot) 0.88f else 0.36f),
            start = Offset(left, y),
            end = Offset(end, y),
            strokeWidth = h * 0.036f,
            cap = StrokeCap.Round
        )
    }
    drawCircle(color = p.ink, radius = h * 0.034f, center = Offset(rule, h * (0.19f + hot * 0.126f)))
}

private fun DrawScope.artSineField(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val phase = r.range(0f, 6.2f)
    for (k in 0 until 5) {
        val line = Path()
        val amp = h * (0.10f + k * 0.030f)
        val mid = h * (0.22f + k * 0.15f)
        for (i in 0 until 33) {
            val f = i / 32f
            val y = mid + sin(f * PI.toFloat() * 2.6f + phase + k * 0.55f) * amp
            if (i == 0) {
                line.moveTo(w * f, y)
            } else {
                line.lineTo(w * f, y)
            }
        }
        drawPath(
            path = line,
            color = p.ink.copy(alpha = 0.22f + k * 0.13f),
            style = Stroke(width = h * 0.022f, cap = StrokeCap.Round)
        )
    }
}

private fun DrawScope.artChevrons(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cy = h * 0.52f
    val x0 = w * r.range(0.06f, 0.16f)
    val step = w * 0.13f
    val arm = h * 0.34f
    for (i in 0 until 6) {
        val x = x0 + i * step
        val chev = Path()
        chev.moveTo(x, cy - arm)
        chev.lineTo(x + h * 0.26f, cy)
        chev.lineTo(x, cy + arm)
        drawPath(
            path = chev,
            color = p.ink.copy(alpha = 0.16f + i * 0.115f),
            style = Stroke(width = h * 0.034f, cap = StrokeCap.Round)
        )
    }
}

private fun DrawScope.artEclipse(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val cx = w * r.range(0.42f, 0.58f)
    val cy = h * 0.52f
    val rad = h * 0.34f
    drawCircle(color = p.ink.copy(alpha = 0.88f), radius = rad, center = Offset(cx, cy))
    drawCircle(
        color = p.field,
        radius = rad * 0.88f,
        center = Offset(cx + rad * 0.52f, cy - rad * 0.30f)
    )
    drawCircle(
        color = p.ink.copy(alpha = 0.42f),
        radius = rad * 1.42f,
        center = Offset(cx, cy),
        style = Stroke(width = h * 0.018f)
    )
    drawCircle(
        color = p.ink.copy(alpha = 0.24f),
        radius = rad * 1.86f,
        center = Offset(cx, cy),
        style = Stroke(width = h * 0.014f)
    )
}

private fun DrawScope.artShelf(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val baseY = h * 0.88f
    val n = 11
    var x = w * 0.07f
    for (i in 0 until n) {
        val bw = w * r.range(0.028f, 0.055f)
        val bh = h * r.range(0.30f, 0.58f)
        val lean = if (i == n - 4) 14f else 0f
        rotate(degrees = lean, pivot = Offset(x + bw, baseY)) {
            drawRect(
                color = if (i % 4 == 1) p.paper.copy(alpha = 0.85f) else p.ink.copy(alpha = 0.34f + r.range(0f, 0.42f)),
                topLeft = Offset(x, baseY - bh),
                size = Size(bw, bh)
            )
            drawLine(
                color = p.ink.copy(alpha = 0.48f),
                start = Offset(x + bw * 0.5f, baseY - bh * 0.78f),
                end = Offset(x + bw * 0.5f, baseY - bh * 0.30f),
                strokeWidth = bw * 0.22f,
                cap = StrokeCap.Round
            )
        }
        x = x + bw + w * 0.016f
    }
    drawLine(
        color = p.ink.copy(alpha = 0.65f),
        start = Offset(w * 0.04f, baseY),
        end = Offset(w * 0.78f, baseY),
        strokeWidth = h * 0.024f,
        cap = StrokeCap.Round
    )
}

private fun DrawScope.artComet(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val x0 = w * 0.02f
    val y0 = h * 0.92f
    val x1 = w * 0.40f
    val y1 = h * 0.88f
    val x2 = w * (0.72f + r.range(-0.05f, 0.05f))
    val y2 = h * 0.30f
    // Walked out along one side of the centreline and back along the other.
    // Compose strokes at a single width, and a comet is the one shape in the
    // set that has to start at nothing and end at something.
    val tail = Path()
    for (i in 0 until 26) {
        val f = i / 25f
        val u = 1f - f
        val cxp = u * u * x0 + 2f * u * f * x1 + f * f * x2
        val cyp = u * u * y0 + 2f * u * f * y1 + f * f * y2
        val dx = 2f * (u * (x1 - x0) + f * (x2 - x1))
        val dy = 2f * (u * (y1 - y0) + f * (y2 - y1))
        val len = sqrt(dx * dx + dy * dy)
        val hw = h * 0.155f * f * f
        if (i == 0) {
            tail.moveTo(cxp - dy / len * hw, cyp + dx / len * hw)
        } else {
            tail.lineTo(cxp - dy / len * hw, cyp + dx / len * hw)
        }
    }
    for (i in 0 until 26) {
        val f = (25 - i) / 25f
        val u = 1f - f
        val cxp = u * u * x0 + 2f * u * f * x1 + f * f * x2
        val cyp = u * u * y0 + 2f * u * f * y1 + f * f * y2
        val dx = 2f * (u * (x1 - x0) + f * (x2 - x1))
        val dy = 2f * (u * (y1 - y0) + f * (y2 - y1))
        val len = sqrt(dx * dx + dy * dy)
        val hw = h * 0.155f * f * f
        tail.lineTo(cxp + dy / len * hw, cyp - dx / len * hw)
    }
    tail.close()
    drawPath(path = tail, color = p.ink.copy(alpha = 0.52f))
    drawCircle(color = p.ink, radius = h * 0.105f, center = Offset(x2, y2))
    drawCircle(
        color = p.ink.copy(alpha = 0.42f),
        radius = h * 0.200f,
        center = Offset(x2, y2),
        style = Stroke(width = h * 0.016f)
    )
    for (i in 0 until 5) {
        drawCircle(
            color = p.ink.copy(alpha = 0.16f + r.range(0f, 0.20f)),
            radius = h * 0.018f,
            center = Offset(w * r.range(0.04f, 0.96f), h * r.range(0.06f, 0.92f))
        )
    }
}
