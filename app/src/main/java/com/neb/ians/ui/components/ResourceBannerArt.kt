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
import com.neb.ians.ui.theme.SubjectFamily
import com.neb.ians.ui.theme.SubjectTheme
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.ui.theme.subjectFamily
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
 * like a printing error.
 *
 * There are sixty-seven now, and they are not one pool. Each drawing belongs to
 * a [SubjectFamily], and a resource can only be given a drawing from its own
 * family: chemistry gets flasks and benzene rings, computing gets terminals and
 * circuits, social studies gets maps and monuments. A physics past paper will
 * never again come back as a crescent moon.
 *
 * The family a resource lands in is decided by [subjectFamily], which reads
 * free text and answers coarsely. When it cannot place a subject — a blank
 * field, a course name nobody anticipated — the answer is [SubjectFamily.GENERAL],
 * and general has its own set: twelve abstract compositions that carry no
 * subject claim at all. That set is deliberately the descendant of the old
 * universal art. Being about nothing in particular was the one real advantage
 * the single wave drawing had, and it is the right answer for a resource we
 * genuinely cannot classify — it just was not the right answer for all of them.
 *
 * Everything here is drawn from two colours: an ink and a paper, both derived
 * from the subject's own tint against the current surface. That is the whole
 * trick to surviving dark mode — nothing is hardcoded, so the same geometry
 * that reads as navy line-work on a pale field reads as pale line-work on navy
 * without a second set of numbers to keep in sync.
 *
 * Size is the other axis the drawings answer to. A banner is 110dp tall in a
 * rail, taller in a grid, and full-bleed on a detail screen, so nothing here
 * counts elements in absolute numbers. Densities are derived from the box the
 * canvas is actually handed — a wider banner gets more dots, more hatching and
 * more contour rings rather than the same few stretched across it — and stroke
 * weights come off the short side so that line work stays proportionate instead
 * of turning to hairlines on a large card and to slabs on a small one.
 */
@Composable
fun ResourceBannerArt(
    seed: String,
    subject: String,
    modifier: Modifier = Modifier
) {
    val theme = getSubjectTheme(subject)
    val family = remember(subject) { subjectFamily(subject) }
    val surface = MaterialTheme.colorScheme.surface
    val isDark = surface.luminance() < 0.5f
    val palette = remember(theme, surface, isDark) { bannerPalette(theme, surface, isDark) }
    val hash = remember(seed) { stableSeed(seed) }

    Canvas(modifier = modifier.clipToBounds()) {
        drawField(palette)
        drawBannerArt(family, (hash ushr 3) and 0x7FFFFFFF, palette, Rng(hash))
    }
}


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

/** How many drawings a family can offer. Used by tooling and by the sheets. */
fun bannerArtCount(family: SubjectFamily): Int {
    return when (family) {
        SubjectFamily.PHYSICS -> 6
        SubjectFamily.CHEMISTRY -> 6
        SubjectFamily.MATH -> 6
        SubjectFamily.BIOLOGY -> 6
        SubjectFamily.SCIENCE -> 5
        SubjectFamily.LANGUAGE -> 6
        SubjectFamily.COMPUTING -> 6
        SubjectFamily.COMMERCE -> 6
        SubjectFamily.SOCIAL -> 5
        SubjectFamily.HEALTH -> 5
        SubjectFamily.EXAM -> 5
        SubjectFamily.GENERAL -> 12
    }
}

/**
 * Pick the drawing. [index] is a hash of the resource, so the choice is stable
 * for the life of the resource, and [family] is the gate: a drawing is only
 * ever reachable from the subjects it actually describes.
 *
 * A handful appear in two families on purpose. A pulse line is both biology and
 * health; a leaf is both biology and general science; stacked isometric blocks
 * are both mathematics and, in the abstract set, nothing at all. Those are the
 * only overlaps, and each is a case where the same image is honestly true of
 * both subjects.
 */
fun DrawScope.drawBannerArt(family: SubjectFamily, index: Int, p: BannerPalette, r: Rng) {
    val i = index % bannerArtCount(family)
    when (family) {
        SubjectFamily.PHYSICS -> when (i) {
            0 -> artAtom(p, r)
            1 -> artPrism(p, r)
            2 -> artPendulum(p, r)
            3 -> artFieldLines(p, r)
            4 -> artLensRays(p, r)
            else -> artProjectile(p, r)
        }
        SubjectFamily.CHEMISTRY -> when (i) {
            0 -> artMolecule(p, r)
            1 -> artFlask(p, r)
            2 -> artBenzene(p, r)
            3 -> artBurette(p, r)
            4 -> artLattice(p, r)
            else -> artBeaker(p, r)
        }
        SubjectFamily.MATH -> when (i) {
            0 -> artParabola(p, r)
            1 -> artGeometry(p, r)
            2 -> artSigma(p, r)
            3 -> artMatrix(p, r)
            4 -> artVenn(p, r)
            else -> artSteps(p, r)
        }
        SubjectFamily.BIOLOGY -> when (i) {
            0 -> artHelix(p, r)
            1 -> artBloom(p, r)
            2 -> artCell(p, r)
            3 -> artLeaf(p, r)
            4 -> artPulse(p, r)
            else -> artPetri(p, r)
        }
        SubjectFamily.SCIENCE -> when (i) {
            0 -> artFlask(p, r)
            1 -> artAtom(p, r)
            2 -> artLeaf(p, r)
            3 -> artFieldLines(p, r)
            else -> artPetri(p, r)
        }
        SubjectFamily.LANGUAGE -> when (i) {
            0 -> artPages(p, r)
            1 -> artShelf(p, r)
            2 -> artQuill(p, r)
            3 -> artQuotes(p, r)
            4 -> artManuscript(p, r)
            else -> artLetterform(p, r)
        }
        SubjectFamily.COMPUTING -> when (i) {
            0 -> artCircuit(p, r)
            1 -> artTerminal(p, r)
            2 -> artBinary(p, r)
            3 -> artGraph(p, r)
            4 -> artBraces(p, r)
            else -> artChip(p, r)
        }
        SubjectFamily.COMMERCE -> when (i) {
            0 -> artBars(p, r)
            1 -> artLedger(p, r)
            2 -> artCoins(p, r)
            3 -> artSupplyDemand(p, r)
            4 -> artPie(p, r)
            else -> artReceipt(p, r)
        }
        SubjectFamily.SOCIAL -> when (i) {
            0 -> artPeaks(p, r)
            1 -> artContours(p, r)
            2 -> artGlobe(p, r)
            3 -> artMonument(p, r)
            else -> artCompass(p, r)
        }
        SubjectFamily.HEALTH -> when (i) {
            0 -> artPulse(p, r)
            1 -> artRunner(p, r)
            2 -> artApple(p, r)
            3 -> artRings(p, r)
            else -> artDrop(p, r)
        }
        SubjectFamily.EXAM -> when (i) {
            0 -> artChecklist(p, r)
            1 -> artClock(p, r)
            2 -> artTarget(p, r)
            3 -> artCalendar(p, r)
            else -> artTrophy(p, r)
        }
        SubjectFamily.GENERAL -> when (i) {
            0 -> artArcs(p, r)
            1 -> artHorizon(p, r)
            2 -> artDotMatrix(p, r)
            3 -> artWaveform(p, r)
            4 -> artRipple(p, r)
            5 -> artHatch(p, r)
            6 -> artConstellation(p, r)
            7 -> artSineField(p, r)
            8 -> artChevrons(p, r)
            9 -> artEclipse(p, r)
            10 -> artComet(p, r)
            else -> artSteps(p, r)
        }
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
    val span = w + h
    val n = (span / (h * 0.20f)).toInt().coerceIn(8, 34)
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
    drawRect(color = p.field.copy(alpha = 0.94f), topLeft = Offset(bx, by), size = Size(bw, bh))
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

// --------------------------------------------------------------- physics ---

/** Three positions of one bob, and the arc it travels between them. */
private fun DrawScope.artPendulum(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val px = w * 0.52f
    val py = h * 0.07f
    val len = h * 0.66f
    val swing = 0.46f + r.range(0f, 0.22f)
    drawLine(
        color = p.ink.copy(alpha = 0.50f),
        start = Offset(w * 0.5f - len * 0.85f, py),
        end = Offset(w * 0.5f + len * 0.85f, py),
        strokeWidth = unit * 0.026f,
        cap = StrokeCap.Round
    )
    drawArc(
        color = p.ink.copy(alpha = 0.18f),
        startAngle = 90f - swing * 57.2958f,
        sweepAngle = swing * 114.5916f,
        useCenter = false,
        topLeft = Offset(px - len, py - len),
        size = Size(len * 2f, len * 2f),
        style = Stroke(width = unit * 0.016f, cap = StrokeCap.Round)
    )
    for (i in 0 until 3) {
        val a = -swing + swing * i
        val bx = px + sin(a) * len
        val by = py + cos(a) * len
        val lead = i == 2
        val al = if (lead) 0.88f else 0.20f + i * 0.09f
        drawLine(
            color = p.ink.copy(alpha = al * 0.62f),
            start = Offset(px, py),
            end = Offset(bx, by),
            strokeWidth = unit * 0.018f,
            cap = StrokeCap.Round
        )
        drawCircle(color = p.ink.copy(alpha = al), radius = unit * 0.088f, center = Offset(bx, by))
        if (lead) {
            drawCircle(
                color = p.paper.copy(alpha = 0.50f),
                radius = unit * 0.030f,
                center = Offset(bx - unit * 0.026f, by - unit * 0.028f)
            )
        }
    }
    drawCircle(color = p.ink, radius = unit * 0.032f, center = Offset(px, py))
}

/** A bar magnet, and the loops that close around it. */
private fun DrawScope.artFieldLines(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cy = h * 0.52f
    val half = w * 0.13f
    val bar = h * 0.11f
    val loops = ((w / h) * 1.4f).toInt().coerceIn(2, 6)
    for (i in 0 until loops) {
        val f = (i + 1f) / loops
        val rx = half + w * 0.10f + f * w * 0.30f
        val ry = bar * 1.6f + f * h * 0.42f
        drawArc(
            color = p.ink.copy(alpha = 0.34f - f * 0.16f),
            startAngle = 0f,
            sweepAngle = 360f,
            useCenter = false,
            topLeft = Offset(w * 0.5f - rx, cy - ry),
            size = Size(rx * 2f, ry * 2f),
            style = Stroke(width = unit * 0.015f)
        )
    }
    drawRect(
        color = p.ink.copy(alpha = 0.30f),
        topLeft = Offset(w * 0.5f - half, cy - bar),
        size = Size(half, bar * 2f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.88f),
        topLeft = Offset(w * 0.5f, cy - bar),
        size = Size(half, bar * 2f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.72f),
        topLeft = Offset(w * 0.5f - half, cy - bar),
        size = Size(half * 2f, bar * 2f),
        style = Stroke(width = unit * 0.018f)
    )
    val tick = unit * 0.055f
    drawLine(
        color = p.paper.copy(alpha = 0.85f),
        start = Offset(w * 0.5f + half * 0.5f - tick, cy),
        end = Offset(w * 0.5f + half * 0.5f + tick, cy),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.80f),
        start = Offset(w * 0.5f - half * 0.5f, cy - tick),
        end = Offset(w * 0.5f - half * 0.5f, cy + tick),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.80f),
        start = Offset(w * 0.5f - half * 0.5f - tick, cy),
        end = Offset(w * 0.5f - half * 0.5f + tick, cy),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
}

/** Parallel light, a biconvex lens, one focus. */
private fun DrawScope.artLensRays(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val lx = w * 0.42f
    val cy = h * 0.52f
    val lh = h * 0.36f
    val bulge = w * 0.045f
    val fx = lx + w * 0.36f
    val rays = ((h / unit) * 5f).toInt().coerceIn(4, 7)
    for (i in 0 until rays) {
        val t = (i + 0.5f) / rays
        val y = cy - lh + lh * 2f * t
        drawLine(
            color = p.ink.copy(alpha = 0.44f),
            start = Offset(w * 0.03f, y),
            end = Offset(lx, y),
            strokeWidth = unit * 0.015f,
            cap = StrokeCap.Round
        )
        drawLine(
            color = p.ink.copy(alpha = 0.62f),
            start = Offset(lx, y),
            end = Offset(fx, cy),
            strokeWidth = unit * 0.015f,
            cap = StrokeCap.Round
        )
        drawLine(
            color = p.ink.copy(alpha = 0.18f),
            start = Offset(fx, cy),
            end = Offset(fx + (fx - lx) * 0.55f, cy + (cy - y) * 0.55f),
            strokeWidth = unit * 0.013f,
            cap = StrokeCap.Round
        )
    }
    val lens = Path()
    lens.moveTo(lx, cy - lh)
    lens.cubicTo(lx + bulge, cy - lh * 0.4f, lx + bulge, cy + lh * 0.4f, lx, cy + lh)
    lens.cubicTo(lx - bulge, cy + lh * 0.4f, lx - bulge, cy - lh * 0.4f, lx, cy - lh)
    lens.close()
    drawPath(path = lens, color = p.ink.copy(alpha = 0.20f))
    drawPath(path = lens, color = p.ink.copy(alpha = 0.85f), style = Stroke(width = unit * 0.020f))
    drawCircle(color = p.ink, radius = unit * 0.045f, center = Offset(fx, cy))
    drawLine(
        color = p.ink.copy(alpha = 0.22f),
        start = Offset(w * 0.02f, cy),
        end = Offset(w * 0.98f, cy),
        strokeWidth = unit * 0.010f
    )
}

/** One launch, one parabola, the velocity that made it. */
private fun DrawScope.artProjectile(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val gy = h * 0.86f
    val x0 = w * 0.10f
    val x1 = w * 0.90f
    val peak = h * 0.16f
    val steps = (w / (unit * 0.16f)).toInt().coerceIn(12, 64)
    drawLine(
        color = p.ink.copy(alpha = 0.55f),
        start = Offset(w * 0.02f, gy),
        end = Offset(w * 0.98f, gy),
        strokeWidth = unit * 0.018f,
        cap = StrokeCap.Round
    )
    val hatches = (w / (unit * 0.34f)).toInt().coerceIn(4, 22)
    for (i in 0 until hatches) {
        val hx = w * 0.03f + (w * 0.94f) * (i + 0.5f) / hatches
        drawLine(
            color = p.ink.copy(alpha = 0.16f),
            start = Offset(hx, gy),
            end = Offset(hx - unit * 0.07f, gy + unit * 0.09f),
            strokeWidth = unit * 0.011f,
            cap = StrokeCap.Round
        )
    }
    val arc = Path()
    for (i in 0 until steps + 1) {
        val t = i / steps.toFloat()
        val x = x0 + (x1 - x0) * t
        val y = gy - (gy - peak) * 4f * t * (1f - t)
        if (i == 0) {
            arc.moveTo(x, y)
        } else {
            arc.lineTo(x, y)
        }
    }
    drawPath(
        path = arc,
        color = p.ink.copy(alpha = 0.78f),
        style = Stroke(width = unit * 0.020f, cap = StrokeCap.Round)
    )
    val marks = 5
    for (i in 0 until marks) {
        val t = (i + 1f) / (marks + 1f)
        val x = x0 + (x1 - x0) * t
        val y = gy - (gy - peak) * 4f * t * (1f - t)
        drawCircle(color = p.ink.copy(alpha = 0.34f), radius = unit * 0.030f, center = Offset(x, y))
    }
    val vx = x0 + (x1 - x0) * 0.22f
    val vy = gy - (gy - peak) * 4f * 0.22f * 0.78f
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(x0, gy),
        end = Offset(vx, vy),
        strokeWidth = unit * 0.016f,
        cap = StrokeCap.Round
    )
    drawCircle(color = p.ink, radius = unit * 0.062f, center = Offset(x0, gy))
    val apex = (x0 + x1) * 0.5f
    drawCircle(color = p.ink, radius = unit * 0.075f, center = Offset(apex, peak))
    drawCircle(
        color = p.paper.copy(alpha = 0.55f),
        radius = unit * 0.026f,
        center = Offset(apex - unit * 0.022f, peak - unit * 0.024f)
    )
}

// ------------------------------------------------------------- chemistry ---

/** An Erlenmeyer flask, half full, working. */
private fun DrawScope.artFlask(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val top = h * 0.12f
    val bot = h * 0.84f
    val neck = unit * 0.11f
    val base = unit * 0.40f
    val liq = bot - (bot - top) * 0.34f
    val body = Path()
    body.moveTo(cx - neck, top)
    body.lineTo(cx - neck, top + (bot - top) * 0.28f)
    body.lineTo(cx - base, bot - unit * 0.07f)
    body.cubicTo(cx - base, bot, cx - base, bot, cx - base + unit * 0.08f, bot)
    body.lineTo(cx + base - unit * 0.08f, bot)
    body.cubicTo(cx + base, bot, cx + base, bot, cx + base, bot - unit * 0.07f)
    body.lineTo(cx + neck, top + (bot - top) * 0.28f)
    body.lineTo(cx + neck, top)
    drawPath(
        path = body,
        color = p.ink.copy(alpha = 0.82f),
        style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
    )
    val shoulder = top + (bot - top) * 0.28f
    val lw = neck + (base - neck) * (liq - shoulder) / (bot - shoulder)
    val fill = Path()
    fill.moveTo(cx - lw, liq)
    fill.lineTo(cx + lw, liq)
    fill.lineTo(cx + base, bot)
    fill.lineTo(cx - base, bot)
    fill.close()
    drawPath(path = fill, color = p.ink.copy(alpha = 0.24f))
    drawLine(
        color = p.ink.copy(alpha = 0.70f),
        start = Offset(cx - lw, liq),
        end = Offset(cx + lw, liq),
        strokeWidth = unit * 0.018f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.78f),
        start = Offset(cx - neck - unit * 0.05f, top),
        end = Offset(cx + neck + unit * 0.05f, top),
        strokeWidth = unit * 0.024f,
        cap = StrokeCap.Round
    )
    for (i in 0 until 6) {
        val bx = cx + r.range(-0.60f, 0.60f) * base
        val by = liq + r.range(0.08f, 0.82f) * (bot - liq)
        drawCircle(
            color = p.ink.copy(alpha = 0.40f),
            radius = unit * r.range(0.016f, 0.036f),
            center = Offset(bx, by),
            style = Stroke(width = unit * 0.010f)
        )
    }
    for (i in 0 until 3) {
        drawCircle(
            color = p.ink.copy(alpha = 0.30f - i * 0.08f),
            radius = unit * (0.024f + i * 0.012f),
            center = Offset(cx + unit * (0.05f - i * 0.06f), top - unit * (0.06f + i * 0.14f))
        )
    }
}

/** The ring, and the two that keep it company. */
private fun DrawScope.artBenzene(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val spin = r.range(0f, 0.5f)
    val rings = ((w / h) * 1.05f).toInt().coerceIn(1, 4)
    for (k in 0 until rings) {
        val lead = k == 0
        val rad = if (lead) unit * 0.36f else unit * 0.20f
        val cx = if (lead) w * 0.50f else w * (0.16f + k * 0.24f)
        val cy = if (lead) h * 0.50f else h * (0.26f + (k % 2) * 0.48f)
        val al = if (lead) 0.86f else 0.30f
        val ring = Path()
        for (i in 0 until 6) {
            val a = spin + i * (PI.toFloat() / 3f)
            val x = cx + cos(a) * rad
            val y = cy + sin(a) * rad
            if (i == 0) {
                ring.moveTo(x, y)
            } else {
                ring.lineTo(x, y)
            }
        }
        ring.close()
        drawPath(
            path = ring,
            color = p.ink.copy(alpha = al),
            style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
        )
        drawCircle(
            color = p.ink.copy(alpha = al * 0.62f),
            radius = rad * 0.56f,
            center = Offset(cx, cy),
            style = Stroke(width = unit * 0.018f)
        )
        if (lead) {
            for (i in 0 until 6) {
                val a = spin + i * (PI.toFloat() / 3f)
                drawCircle(
                    color = p.ink.copy(alpha = 0.55f),
                    radius = unit * 0.040f,
                    center = Offset(cx + cos(a) * rad, cy + sin(a) * rad)
                )
            }
        }
    }
}

/** A burette, a stopcock, and the drop on its way down. */
private fun DrawScope.artBurette(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val top = h * 0.04f
    val tapY = h * 0.44f
    val tipY = h * 0.54f
    val half = unit * 0.070f
    drawRect(
        color = p.ink.copy(alpha = 0.20f),
        topLeft = Offset(cx - half, top + (tapY - top) * 0.34f),
        size = Size(half * 2f, (tapY - top) * 0.66f)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx - half, top),
        end = Offset(cx - half, tapY),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx + half, top),
        end = Offset(cx + half, tapY),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
    val ticks = ((tapY - top) / (unit * 0.095f)).toInt().coerceIn(4, 12)
    for (i in 0 until ticks) {
        val ty = top + (tapY - top) * (i + 1f) / (ticks + 1f)
        val long = i % 3 == 0
        drawLine(
            color = p.ink.copy(alpha = if (long) 0.62f else 0.32f),
            start = Offset(cx - half, ty),
            end = Offset(cx - half + (if (long) unit * 0.080f else unit * 0.044f), ty),
            strokeWidth = unit * 0.012f,
            cap = StrokeCap.Round
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx - unit * 0.105f, tapY),
        end = Offset(cx + unit * 0.105f, tapY),
        strokeWidth = unit * 0.026f,
        cap = StrokeCap.Round
    )
    drawCircle(color = p.ink.copy(alpha = 0.90f), radius = unit * 0.050f, center = Offset(cx, tapY))
    drawLine(
        color = p.ink.copy(alpha = 0.80f),
        start = Offset(cx, tapY),
        end = Offset(cx, tipY),
        strokeWidth = unit * 0.016f,
        cap = StrokeCap.Round
    )
    val neck = unit * 0.055f
    val fTop = h * 0.66f
    val fBot = h * 0.94f
    val fBase = unit * 0.25f
    for (i in 0 until 2) {
        drawCircle(
            color = p.ink.copy(alpha = 0.70f - i * 0.28f),
            radius = unit * (0.034f - i * 0.009f),
            center = Offset(cx, tipY + unit * (0.07f + i * 0.11f))
        )
    }
    val liq = fBot - (fBot - fTop) * 0.34f
    val lw = neck + (fBase - neck) * (liq - fTop) / (fBot - fTop)
    val pool = Path()
    pool.moveTo(cx - lw, liq)
    pool.lineTo(cx + lw, liq)
    pool.lineTo(cx + fBase, fBot)
    pool.lineTo(cx - fBase, fBot)
    pool.close()
    drawPath(path = pool, color = p.ink.copy(alpha = 0.26f))
    val flask = Path()
    flask.moveTo(cx - neck, fTop)
    flask.lineTo(cx - fBase, fBot)
    flask.lineTo(cx + fBase, fBot)
    flask.lineTo(cx + neck, fTop)
    drawPath(
        path = flask,
        color = p.ink.copy(alpha = 0.82f),
        style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.72f),
        start = Offset(cx - lw, liq),
        end = Offset(cx + lw, liq),
        strokeWidth = unit * 0.018f,
        cap = StrokeCap.Round
    )
    val stands = ((w / h) * 1.2f).toInt().coerceIn(0, 2)
    for (i in 0 until stands) {
        val sx = if (i == 0) cx - unit * 0.52f else cx + unit * 0.52f
        drawLine(
            color = p.ink.copy(alpha = 0.22f),
            start = Offset(sx, h * 0.10f),
            end = Offset(sx, h * 0.94f),
            strokeWidth = unit * 0.022f,
            cap = StrokeCap.Round
        )
        drawLine(
            color = p.ink.copy(alpha = 0.22f),
            start = Offset(sx, h * 0.26f),
            end = Offset(cx - half - unit * 0.01f, h * 0.26f),
            strokeWidth = unit * 0.016f,
            cap = StrokeCap.Round
        )
    }
}

/** A crystal lattice, seen a little from the side. */
private fun DrawScope.artLattice(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val step = unit * 0.36f
    val skewX = step * 0.42f
    val skewY = step * 0.25f
    val cols = ((w - step * 1.4f) / step).toInt().coerceIn(2, 7)
    val rows = if (h > unit * 0.9f) 3 else 2
    val ox = w * 0.5f - (cols - 1) * step * 0.5f - skewX * 0.5f
    val oy = h * 0.5f - (rows - 1) * step * 0.5f + skewY * 0.5f
    for (dep in 0 until 2) {
        val dx = ox + dep * skewX
        val dy = oy - dep * skewY
        val al = if (dep == 0) 0.26f else 0.80f
        for (c in 0 until cols) {
            drawLine(
                color = p.ink.copy(alpha = al * 0.40f),
                start = Offset(dx + c * step, dy),
                end = Offset(dx + c * step, dy + (rows - 1) * step),
                strokeWidth = unit * 0.013f
            )
        }
        for (rw in 0 until rows) {
            drawLine(
                color = p.ink.copy(alpha = al * 0.40f),
                start = Offset(dx, dy + rw * step),
                end = Offset(dx + (cols - 1) * step, dy + rw * step),
                strokeWidth = unit * 0.013f
            )
        }
        for (c in 0 until cols) {
            for (rw in 0 until rows) {
                val big = (c + rw) % 2 == 0
                drawCircle(
                    color = p.ink.copy(alpha = al),
                    radius = if (big) unit * 0.068f else unit * 0.040f,
                    center = Offset(dx + c * step, dy + rw * step)
                )
            }
        }
    }
    for (c in 0 until cols) {
        for (rw in 0 until rows) {
            drawLine(
                color = p.ink.copy(alpha = 0.24f),
                start = Offset(ox + c * step, oy + rw * step),
                end = Offset(ox + skewX + c * step, oy - skewY + rw * step),
                strokeWidth = unit * 0.012f
            )
        }
    }
}

/** A beaker, graduated, with the column of bubbles a reaction makes. */
private fun DrawScope.artBeaker(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val half = unit * 0.36f
    val top = h * 0.14f
    val bot = h * 0.88f
    val liq = top + (bot - top) * 0.40f
    drawRect(
        color = p.ink.copy(alpha = 0.22f),
        topLeft = Offset(cx - half, liq),
        size = Size(half * 2f, bot - liq)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx - half, top),
        end = Offset(cx - half, bot),
        strokeWidth = unit * 0.022f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx + half, top),
        end = Offset(cx + half, bot),
        strokeWidth = unit * 0.022f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx - half, bot),
        end = Offset(cx + half, bot),
        strokeWidth = unit * 0.022f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx - half - unit * 0.07f, top - unit * 0.03f),
        end = Offset(cx - half, top + unit * 0.02f),
        strokeWidth = unit * 0.022f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.72f),
        start = Offset(cx - half, liq),
        end = Offset(cx + half, liq),
        strokeWidth = unit * 0.018f,
        cap = StrokeCap.Round
    )
    val ticks = ((bot - top) / (unit * 0.13f)).toInt().coerceIn(3, 9)
    for (i in 0 until ticks) {
        val ty = top + (bot - top) * (i + 1f) / (ticks + 1f)
        drawLine(
            color = p.ink.copy(alpha = 0.40f),
            start = Offset(cx + half, ty),
            end = Offset(cx + half - unit * (if (i % 2 == 0) 0.13f else 0.07f), ty),
            strokeWidth = unit * 0.012f,
            cap = StrokeCap.Round
        )
    }
    for (i in 0 until 9) {
        val f = i / 8f
        val bxx = cx + r.range(-0.55f, 0.55f) * half
        val byy = bot - f * (bot - liq) * 0.95f - unit * 0.03f
        drawCircle(
            color = p.ink.copy(alpha = 0.22f + f * 0.34f),
            radius = unit * (0.016f + f * 0.026f),
            center = Offset(bxx, byy),
            style = Stroke(width = unit * 0.010f)
        )
    }
}

// ---------------------------------------------------------- mathematics ---

/** Axes, a curve, and the tangent that touches it once. */
private fun DrawScope.artParabola(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val ox = w * 0.20f
    val oy = h * 0.78f
    val gw = w * 0.70f
    val gh = h * 0.60f
    val grid = (gw / (unit * 0.26f)).toInt().coerceIn(3, 16)
    for (i in 0 until grid + 1) {
        val gx = ox + gw * i / grid
        drawLine(
            color = p.ink.copy(alpha = 0.10f),
            start = Offset(gx, oy - gh),
            end = Offset(gx, oy),
            strokeWidth = unit * 0.008f
        )
    }
    for (i in 0 until 4) {
        val gy = oy - gh * (i + 1f) / 4f
        drawLine(
            color = p.ink.copy(alpha = 0.10f),
            start = Offset(ox, gy),
            end = Offset(ox + gw, gy),
            strokeWidth = unit * 0.008f
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(ox, oy),
        end = Offset(ox + gw + unit * 0.08f, oy),
        strokeWidth = unit * 0.017f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(ox, oy),
        end = Offset(ox, oy - gh - unit * 0.08f),
        strokeWidth = unit * 0.017f,
        cap = StrokeCap.Round
    )
    val vx = ox + gw * r.range(0.24f, 0.40f)
    val steps = (gw / (unit * 0.10f)).toInt().coerceIn(16, 90)
    val curve = Path()
    for (i in 0 until steps + 1) {
        val x = ox + gw * i / steps
        val t = (x - vx) / (gw * 0.52f)
        val y = oy - gh * 0.08f - gh * 0.84f * t * t
        if (y < oy - gh - unit * 0.02f) {
            curve.moveTo(x, oy - gh)
        } else {
            if (i == 0) {
                curve.moveTo(x, y)
            } else {
                curve.lineTo(x, y)
            }
        }
    }
    drawPath(
        path = curve,
        color = p.ink.copy(alpha = 0.82f),
        style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
    )
    drawCircle(color = p.ink, radius = unit * 0.050f, center = Offset(vx, oy - gh * 0.08f))
    val tx = ox + gw * 0.72f
    val tt = (tx - vx) / (gw * 0.52f)
    val ty = oy - gh * 0.08f - gh * 0.84f * tt * tt
    val slope = -gh * 0.84f * 2f * tt / (gw * 0.52f)
    drawLine(
        color = p.ink.copy(alpha = 0.40f),
        start = Offset(tx - gw * 0.22f, ty - slope * gw * 0.22f),
        end = Offset(tx + gw * 0.18f, ty + slope * gw * 0.18f),
        strokeWidth = unit * 0.014f,
        cap = StrokeCap.Round
    )
    drawCircle(color = p.ink.copy(alpha = 0.85f), radius = unit * 0.042f, center = Offset(tx, ty))
}

/** A triangle, its incircle, and the marks a proof leaves behind. */
private fun DrawScope.artGeometry(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val ax = w * 0.50f + r.range(-0.06f, 0.10f) * w
    val ay = h * 0.12f
    val bx = w * 0.22f
    val by = h * 0.86f
    val cx = w * 0.78f
    val cy = h * 0.86f
    val tri = Path()
    tri.moveTo(ax, ay)
    tri.lineTo(cx, cy)
    tri.lineTo(bx, by)
    tri.close()
    drawPath(path = tri, color = p.ink.copy(alpha = 0.14f))
    drawPath(
        path = tri,
        color = p.ink.copy(alpha = 0.86f),
        style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
    )
    val ix = (ax + bx + cx) / 3f
    val iy = (ay + by + cy) / 3f
    val inr = (by - ay) * 0.26f
    drawCircle(
        color = p.ink.copy(alpha = 0.50f),
        radius = inr,
        center = Offset(ix, iy),
        style = Stroke(width = unit * 0.016f)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.34f),
        start = Offset(ax, ay),
        end = Offset((bx + cx) * 0.5f, by),
        strokeWidth = unit * 0.013f
    )
    drawLine(
        color = p.ink.copy(alpha = 0.34f),
        start = Offset(ax, ay),
        end = Offset(ax, by),
        strokeWidth = unit * 0.013f
    )
    val sq = unit * 0.085f
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(ax, by - sq),
        end = Offset(ax + sq, by - sq),
        strokeWidth = unit * 0.014f
    )
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(ax + sq, by - sq),
        end = Offset(ax + sq, by),
        strokeWidth = unit * 0.014f
    )
    drawCircle(color = p.ink, radius = unit * 0.046f, center = Offset(ax, ay))
    drawCircle(color = p.ink, radius = unit * 0.046f, center = Offset(bx, by))
    drawCircle(color = p.ink, radius = unit * 0.046f, center = Offset(cx, cy))
}

/** The summation sign, and what is being summed. */
private fun DrawScope.artSigma(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val left = w * 0.14f
    val right = left + unit * 0.52f
    val top = h * 0.16f
    val bot = h * 0.84f
    val mid = (top + bot) * 0.5f
    val sig = Path()
    sig.moveTo(right, top)
    sig.lineTo(left, top)
    sig.lineTo(left + unit * 0.30f, mid)
    sig.lineTo(left, bot)
    sig.lineTo(right, bot)
    drawPath(
        path = sig,
        color = p.ink.copy(alpha = 0.88f),
        style = Stroke(width = unit * 0.060f, cap = StrokeCap.Round)
    )
    drawCircle(color = p.ink.copy(alpha = 0.50f), radius = unit * 0.038f, center = Offset(right + unit * 0.09f, top - unit * 0.02f))
    drawCircle(color = p.ink.copy(alpha = 0.50f), radius = unit * 0.038f, center = Offset(right + unit * 0.09f, bot + unit * 0.02f))
    val bars = ((w - right) / (unit * 0.20f)).toInt().coerceIn(2, 10)
    for (i in 0 until bars) {
        val bxx = right + unit * 0.24f + i * unit * 0.185f
        if (bxx < w * 0.96f) {
            val fh = (bot - top) * (0.24f + r.range(0f, 0.68f))
            drawLine(
                color = p.ink.copy(alpha = 0.26f + r.range(0f, 0.34f)),
                start = Offset(bxx, bot),
                end = Offset(bxx, bot - fh),
                strokeWidth = unit * 0.075f,
                cap = StrokeCap.Round
            )
        }
    }
    drawLine(
        color = p.ink.copy(alpha = 0.30f),
        start = Offset(right + unit * 0.14f, bot + unit * 0.09f),
        end = Offset(w * 0.96f, bot + unit * 0.09f),
        strokeWidth = unit * 0.012f,
        cap = StrokeCap.Round
    )
}

/** A matrix: brackets, and entries that carry weight. */
private fun DrawScope.artMatrix(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val rows = 3
    val step = unit * 0.24f
    val cols = ((w * 0.74f) / step).toInt().coerceIn(3, 10)
    val gw = (cols - 1) * step
    val gh = (rows - 1) * step
    val ox = w * 0.5f - gw * 0.5f
    val oy = h * 0.5f - gh * 0.5f
    val pad = unit * 0.15f
    val arm = unit * 0.12f
    val lb = Path()
    lb.moveTo(ox - pad + arm, oy - pad)
    lb.lineTo(ox - pad, oy - pad)
    lb.lineTo(ox - pad, oy + gh + pad)
    lb.lineTo(ox - pad + arm, oy + gh + pad)
    drawPath(
        path = lb,
        color = p.ink.copy(alpha = 0.85f),
        style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
    )
    val rb = Path()
    rb.moveTo(ox + gw + pad - arm, oy - pad)
    rb.lineTo(ox + gw + pad, oy - pad)
    rb.lineTo(ox + gw + pad, oy + gh + pad)
    rb.lineTo(ox + gw + pad - arm, oy + gh + pad)
    drawPath(
        path = rb,
        color = p.ink.copy(alpha = 0.85f),
        style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
    )
    val diag = r.int(2) == 0
    for (c in 0 until cols) {
        for (rw in 0 until rows) {
            val on = if (diag) c % rows == rw else r.int(2) == 0
            val cxx = ox + c * step
            val cyy = oy + rw * step
            if (on) {
                drawCircle(color = p.ink.copy(alpha = 0.88f), radius = unit * 0.056f, center = Offset(cxx, cyy))
            } else {
                drawCircle(
                    color = p.ink.copy(alpha = 0.34f),
                    radius = unit * 0.044f,
                    center = Offset(cxx, cyy),
                    style = Stroke(width = unit * 0.014f)
                )
            }
        }
    }
}

/** Three sets, and what they share. */
private fun DrawScope.artVenn(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val rad = unit * 0.34f
    val cx = w * 0.50f
    val cy = h * 0.52f
    val off = rad * 0.62f
    for (i in 0 until 3) {
        val a = -PI.toFloat() / 2f + i * (PI.toFloat() * 2f / 3f) + r.range(0f, 0.3f)
        drawCircle(
            color = p.ink.copy(alpha = 0.17f),
            radius = rad,
            center = Offset(cx + cos(a) * off, cy + sin(a) * off * 0.92f)
        )
    }
    for (i in 0 until 3) {
        val a = -PI.toFloat() / 2f + i * (PI.toFloat() * 2f / 3f)
        drawCircle(
            color = p.ink.copy(alpha = 0.72f),
            radius = rad,
            center = Offset(cx + cos(a) * off, cy + sin(a) * off * 0.92f),
            style = Stroke(width = unit * 0.020f)
        )
    }
    drawCircle(color = p.ink.copy(alpha = 0.55f), radius = unit * 0.048f, center = Offset(cx, cy))
    val dots = ((w / h) * 2f).toInt().coerceIn(2, 8)
    for (i in 0 until dots) {
        drawCircle(
            color = p.ink.copy(alpha = 0.18f + r.range(0f, 0.16f)),
            radius = unit * r.range(0.016f, 0.030f),
            center = Offset(w * r.range(0.03f, 0.97f), h * r.range(0.06f, 0.94f))
        )
    }
}

// --------------------------------------------------------------- biology ---

/** One cell: membrane, nucleus, and the machinery around it. */
private fun DrawScope.artCell(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val cy = h * 0.52f
    val rad = unit * 0.42f
    drawCircle(color = p.ink.copy(alpha = 0.10f), radius = rad, center = Offset(cx, cy))
    drawCircle(
        color = p.ink.copy(alpha = 0.80f),
        radius = rad,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.024f)
    )
    drawCircle(
        color = p.ink.copy(alpha = 0.34f),
        radius = rad * 0.88f,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.013f)
    )
    val nx = cx - rad * 0.16f
    val ny = cy - rad * 0.08f
    drawCircle(color = p.ink.copy(alpha = 0.30f), radius = rad * 0.40f, center = Offset(nx, ny))
    drawCircle(
        color = p.ink.copy(alpha = 0.85f),
        radius = rad * 0.40f,
        center = Offset(nx, ny),
        style = Stroke(width = unit * 0.018f)
    )
    drawCircle(color = p.ink.copy(alpha = 0.90f), radius = rad * 0.15f, center = Offset(nx + rad * 0.08f, ny - rad * 0.06f))
    for (i in 0 until 5) {
        val a = r.range(0f, 6.2832f)
        val dist = rad * r.range(0.52f, 0.82f)
        val ex = cx + cos(a) * dist
        val ey = cy + sin(a) * dist * 0.94f
        drawArc(
            color = p.ink.copy(alpha = 0.52f),
            startAngle = r.range(0f, 360f),
            sweepAngle = 180f + r.range(0f, 120f),
            useCenter = false,
            topLeft = Offset(ex - rad * 0.16f, ey - rad * 0.10f),
            size = Size(rad * 0.32f, rad * 0.20f),
            style = Stroke(width = unit * 0.016f, cap = StrokeCap.Round)
        )
    }
    for (i in 0 until 7) {
        val a = r.range(0f, 6.2832f)
        val dist = rad * r.range(0.30f, 0.90f)
        drawCircle(
            color = p.ink.copy(alpha = 0.34f),
            radius = unit * r.range(0.014f, 0.026f),
            center = Offset(cx + cos(a) * dist, cy + sin(a) * dist * 0.94f)
        )
    }
}

/** A leaf, and its plumbing. */
private fun DrawScope.artLeaf(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val tipx = w * 0.78f
    val tipy = h * 0.16f
    val basex = w * 0.24f
    val basey = h * 0.86f
    val bow = unit * 0.40f
    val dx = tipx - basex
    val dy = tipy - basey
    val len = sqrt(dx * dx + dy * dy)
    val nx = -dy / len
    val ny = dx / len
    val leaf = Path()
    leaf.moveTo(basex, basey)
    leaf.cubicTo(
        basex + dx * 0.20f + nx * bow, basey + dy * 0.20f + ny * bow,
        basex + dx * 0.72f + nx * bow * 0.82f, basey + dy * 0.72f + ny * bow * 0.82f,
        tipx, tipy
    )
    leaf.cubicTo(
        basex + dx * 0.72f - nx * bow * 0.82f, basey + dy * 0.72f - ny * bow * 0.82f,
        basex + dx * 0.20f - nx * bow, basey + dy * 0.20f - ny * bow,
        basex, basey
    )
    leaf.close()
    drawPath(path = leaf, color = p.ink.copy(alpha = 0.16f))
    drawPath(
        path = leaf,
        color = p.ink.copy(alpha = 0.84f),
        style = Stroke(width = unit * 0.024f, cap = StrokeCap.Round)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.72f),
        start = Offset(basex, basey),
        end = Offset(tipx, tipy),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
    val veins = (len / (unit * 0.20f)).toInt().coerceIn(3, 9)
    for (i in 0 until veins) {
        val t = (i + 0.8f) / (veins + 1f)
        val mx = basex + dx * t
        val my = basey + dy * t
        val reach = bow * (1f - t) * 0.86f
        drawLine(
            color = p.ink.copy(alpha = 0.44f),
            start = Offset(mx, my),
            end = Offset(mx + nx * reach + dx * 0.10f, my + ny * reach + dy * 0.10f),
            strokeWidth = unit * 0.013f,
            cap = StrokeCap.Round
        )
        drawLine(
            color = p.ink.copy(alpha = 0.44f),
            start = Offset(mx, my),
            end = Offset(mx - nx * reach + dx * 0.10f, my - ny * reach + dy * 0.10f),
            strokeWidth = unit * 0.013f,
            cap = StrokeCap.Round
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.66f),
        start = Offset(basex, basey),
        end = Offset(basex - dx * 0.16f, basey - dy * 0.16f),
        strokeWidth = unit * 0.022f,
        cap = StrokeCap.Round
    )
}

/** A trace, beating. */
private fun DrawScope.artPulse(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val base = h * 0.56f
    val amp = h * 0.34f
    val beats = (w / (unit * 1.05f)).toInt().coerceIn(1, 6)
    val span = w / beats
    drawLine(
        color = p.ink.copy(alpha = 0.14f),
        start = Offset(0f, base),
        end = Offset(w, base),
        strokeWidth = unit * 0.010f
    )
    val grid = (w / (unit * 0.22f)).toInt().coerceIn(4, 40)
    for (i in 0 until grid) {
        val gx = w * (i + 0.5f) / grid
        drawLine(
            color = p.ink.copy(alpha = 0.07f),
            start = Offset(gx, h * 0.10f),
            end = Offset(gx, h * 0.92f),
            strokeWidth = unit * 0.007f
        )
    }
    val trace = Path()
    trace.moveTo(0f, base)
    for (b in 0 until beats) {
        val o = b * span
        trace.lineTo(o + span * 0.14f, base)
        trace.lineTo(o + span * 0.22f, base - amp * 0.22f)
        trace.lineTo(o + span * 0.30f, base)
        trace.lineTo(o + span * 0.38f, base + amp * 0.18f)
        trace.lineTo(o + span * 0.44f, base - amp)
        trace.lineTo(o + span * 0.50f, base + amp * 0.46f)
        trace.lineTo(o + span * 0.58f, base)
        trace.lineTo(o + span * 0.74f, base - amp * 0.30f)
        trace.lineTo(o + span * 0.86f, base)
    }
    trace.lineTo(w, base)
    drawPath(
        path = trace,
        color = p.ink.copy(alpha = 0.86f),
        style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
    )
    for (b in 0 until beats) {
        drawCircle(
            color = p.ink,
            radius = unit * 0.044f,
            center = Offset(b * span + span * 0.44f, base - amp)
        )
    }
}

/** A dish left in the incubator. */
private fun DrawScope.artPetri(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val cy = h * 0.52f
    val rad = unit * 0.43f
    drawCircle(color = p.ink.copy(alpha = 0.09f), radius = rad, center = Offset(cx, cy))
    drawCircle(
        color = p.ink.copy(alpha = 0.80f),
        radius = rad,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.024f)
    )
    drawCircle(
        color = p.ink.copy(alpha = 0.30f),
        radius = rad * 0.90f,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.012f)
    )
    val colonies = ((w / h) * 5f).toInt().coerceIn(6, 22)
    for (i in 0 until colonies) {
        val a = r.range(0f, 6.2832f)
        val dist = rad * 0.82f * sqrt(r.range(0.02f, 1f))
        val ccx = cx + cos(a) * dist
        val ccy = cy + sin(a) * dist
        val cr = unit * r.range(0.022f, 0.070f)
        drawCircle(color = p.ink.copy(alpha = 0.26f + r.range(0f, 0.40f)), radius = cr, center = Offset(ccx, ccy))
        if (cr > unit * 0.050f) {
            drawCircle(
                color = p.ink.copy(alpha = 0.30f),
                radius = cr * 1.9f,
                center = Offset(ccx, ccy),
                style = Stroke(width = unit * 0.010f)
            )
        }
    }
    drawArc(
        color = p.paper.copy(alpha = 0.30f),
        startAngle = 200f,
        sweepAngle = 70f,
        useCenter = false,
        topLeft = Offset(cx - rad * 0.76f, cy - rad * 0.76f),
        size = Size(rad * 1.52f, rad * 1.52f),
        style = Stroke(width = unit * 0.034f, cap = StrokeCap.Round)
    )
}

// -------------------------------------------------------------- language ---

/** A quill, and the line it has just finished. */
private fun DrawScope.artQuill(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val tipx = w * 0.30f
    val tipy = h * 0.74f
    val topx = tipx + unit * 0.62f
    val topy = h * 0.10f
    val dx = topx - tipx
    val dy = topy - tipy
    val len = sqrt(dx * dx + dy * dy)
    val nx = -dy / len
    val ny = dx / len
    val bow = unit * 0.20f
    val feather = Path()
    feather.moveTo(tipx, tipy)
    feather.cubicTo(
        tipx + dx * 0.34f + nx * bow, tipy + dy * 0.34f + ny * bow,
        tipx + dx * 0.78f + nx * bow * 1.10f, tipy + dy * 0.78f + ny * bow * 1.10f,
        topx, topy
    )
    feather.cubicTo(
        tipx + dx * 0.70f - nx * bow * 0.34f, tipy + dy * 0.70f - ny * bow * 0.34f,
        tipx + dx * 0.30f - nx * bow * 0.22f, tipy + dy * 0.30f - ny * bow * 0.22f,
        tipx, tipy
    )
    feather.close()
    drawPath(path = feather, color = p.ink.copy(alpha = 0.18f))
    drawPath(
        path = feather,
        color = p.ink.copy(alpha = 0.86f),
        style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.72f),
        start = Offset(tipx, tipy),
        end = Offset(topx, topy),
        strokeWidth = unit * 0.016f,
        cap = StrokeCap.Round
    )
    val barbs = (len / (unit * 0.13f)).toInt().coerceIn(4, 12)
    for (i in 0 until barbs) {
        val t = (i + 1.2f) / (barbs + 2f)
        val mx = tipx + dx * t
        val my = tipy + dy * t
        drawLine(
            color = p.ink.copy(alpha = 0.40f),
            start = Offset(mx, my),
            end = Offset(mx + nx * bow * (1f - t * 0.5f) * 0.82f + dx * 0.07f, my + ny * bow * (1f - t * 0.5f) * 0.82f + dy * 0.07f),
            strokeWidth = unit * 0.011f,
            cap = StrokeCap.Round
        )
    }
    drawCircle(color = p.ink, radius = unit * 0.034f, center = Offset(tipx, tipy))
    val ink = Path()
    ink.moveTo(tipx - unit * 0.04f, tipy + unit * 0.06f)
    ink.cubicTo(
        w * 0.10f, h * 0.90f,
        w * 0.44f, h * 0.99f,
        w * 0.94f, h * 0.84f
    )
    drawPath(
        path = ink,
        color = p.ink.copy(alpha = 0.56f),
        style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.20f),
        start = Offset(w * 0.06f, h * 0.94f),
        end = Offset(w * 0.94f, h * 0.94f),
        strokeWidth = unit * 0.010f
    )
}

/** An epigraph: the mark, then the lines it opens. */
private fun DrawScope.artQuotes(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val qx = w * 0.14f
    val qy = h * 0.34f
    val qr = unit * 0.15f
    for (k in 0 until 2) {
        val ox = qx + k * qr * 2.15f
        val hook = Path()
        hook.moveTo(ox + qr * 0.95f, qy - qr * 0.95f)
        hook.cubicTo(
            ox - qr * 0.55f, qy - qr * 0.95f,
            ox - qr * 0.95f, qy + qr * 0.30f,
            ox + qr * 0.10f, qy + qr * 0.95f
        )
        hook.cubicTo(
            ox + qr * 0.95f, qy + qr * 0.55f,
            ox + qr * 0.55f, qy - qr * 0.20f,
            ox + qr * 0.95f, qy - qr * 0.95f
        )
        hook.close()
        drawPath(path = hook, color = p.ink.copy(alpha = 0.80f - k * 0.16f))
    }
    val lines = ((h * 0.44f) / (unit * 0.16f)).toInt().coerceIn(2, 5)
    for (i in 0 until lines) {
        val ly = h * 0.58f + i * unit * 0.165f
        if (ly < h * 0.95f) {
            val frac = if (i == lines - 1) 0.46f else 0.78f + r.range(0f, 0.16f)
            drawLine(
                color = p.ink.copy(alpha = 0.34f + (if (i == 0) 0.22f else 0f)),
                start = Offset(w * 0.12f, ly),
                end = Offset(w * 0.12f + (w * 0.80f) * frac, ly),
                strokeWidth = unit * 0.034f,
                cap = StrokeCap.Round
            )
        }
    }
    val cq = w * 0.90f
    val cy = h * 0.80f
    drawCircle(color = p.ink.copy(alpha = 0.26f), radius = unit * 0.055f, center = Offset(cq, cy))
    drawCircle(color = p.ink.copy(alpha = 0.26f), radius = unit * 0.038f, center = Offset(cq - unit * 0.13f, cy + unit * 0.03f))
}

/** A page from something older: the initial, and the ruling. */
private fun DrawScope.artManuscript(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val m = unit * 0.13f
    drawRect(
        color = p.ink.copy(alpha = 0.07f),
        topLeft = Offset(w * 0.06f, h * 0.08f),
        size = Size(w * 0.88f, h * 0.84f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.60f),
        topLeft = Offset(w * 0.06f, h * 0.08f),
        size = Size(w * 0.88f, h * 0.84f),
        style = Stroke(width = unit * 0.018f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.22f),
        topLeft = Offset(w * 0.06f + m, h * 0.08f + m),
        size = Size(w * 0.88f - m * 2f, h * 0.84f - m * 2f),
        style = Stroke(width = unit * 0.010f)
    )
    val ix = w * 0.06f + m + unit * 0.02f
    val iy = h * 0.08f + m + unit * 0.02f
    val iw = unit * 0.30f
    drawRect(color = p.ink.copy(alpha = 0.80f), topLeft = Offset(ix, iy), size = Size(iw, iw))
    drawRect(
        color = p.paper.copy(alpha = 0.72f),
        topLeft = Offset(ix + iw * 0.22f, iy + iw * 0.20f),
        size = Size(iw * 0.16f, iw * 0.60f)
    )
    drawRect(
        color = p.paper.copy(alpha = 0.72f),
        topLeft = Offset(ix + iw * 0.60f, iy + iw * 0.20f),
        size = Size(iw * 0.16f, iw * 0.60f)
    )
    drawRect(
        color = p.paper.copy(alpha = 0.72f),
        topLeft = Offset(ix + iw * 0.22f, iy + iw * 0.42f),
        size = Size(iw * 0.54f, iw * 0.15f)
    )
    val rule = unit * 0.125f
    val lines = ((h * 0.84f - m * 2f) / rule).toInt().coerceIn(3, 8)
    for (i in 0 until lines) {
        val ly = iy + rule * (i + 0.7f)
        if (ly < h * 0.92f - m) {
            val startx = if (ly < iy + iw + unit * 0.02f) ix + iw + unit * 0.09f else ix
            val frac = if (i == lines - 1) 0.52f else 0.92f + r.range(-0.10f, 0.06f)
            drawLine(
                color = p.ink.copy(alpha = 0.40f),
                start = Offset(startx, ly),
                end = Offset(startx + (w * 0.88f - m * 2f - (startx - ix)) * frac, ly),
                strokeWidth = unit * 0.026f,
                cap = StrokeCap.Round
            )
        }
    }
}

/** A letterform, large enough to be looked at rather than read. */
private fun DrawScope.artLetterform(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val capTop = h * 0.16f
    val baseline = h * 0.82f
    val xh = capTop + (baseline - capTop) * 0.38f
    drawLine(
        color = p.ink.copy(alpha = 0.20f),
        start = Offset(0f, baseline),
        end = Offset(w, baseline),
        strokeWidth = unit * 0.012f
    )
    drawLine(
        color = p.ink.copy(alpha = 0.13f),
        start = Offset(0f, xh),
        end = Offset(w, xh),
        strokeWidth = unit * 0.010f
    )
    drawLine(
        color = p.ink.copy(alpha = 0.13f),
        start = Offset(0f, capTop),
        end = Offset(w, capTop),
        strokeWidth = unit * 0.010f
    )
    val cx = w * 0.50f
    val spread = unit * 0.30f
    val stem = unit * 0.075f
    val glyph = Path()
    glyph.moveTo(cx - spread, baseline)
    glyph.lineTo(cx - stem * 0.45f, capTop)
    glyph.lineTo(cx + stem * 0.45f, capTop)
    glyph.lineTo(cx + spread, baseline)
    glyph.lineTo(cx + spread - stem * 1.25f, baseline)
    glyph.lineTo(cx + spread * 0.58f, baseline - (baseline - capTop) * 0.30f)
    glyph.lineTo(cx - spread * 0.58f, baseline - (baseline - capTop) * 0.30f)
    glyph.lineTo(cx - spread + stem * 1.25f, baseline)
    glyph.close()
    drawPath(path = glyph, color = p.ink.copy(alpha = 0.86f))
    val bar = Path()
    bar.moveTo(cx - spread * 0.40f, baseline - (baseline - capTop) * 0.46f)
    bar.lineTo(cx + spread * 0.40f, baseline - (baseline - capTop) * 0.46f)
    bar.lineTo(cx + spread * 0.40f, baseline - (baseline - capTop) * 0.46f + stem * 0.9f)
    bar.lineTo(cx - spread * 0.40f, baseline - (baseline - capTop) * 0.46f + stem * 0.9f)
    bar.close()
    drawPath(path = bar, color = p.ink.copy(alpha = 0.86f))
    val ghosts = ((w / h) * 1.3f).toInt().coerceIn(1, 4)
    for (k in 0 until ghosts) {
        val gx = if (k % 2 == 0) cx - spread * (2.4f + k * 1.5f) else cx + spread * (2.4f + (k - 1) * 1.5f)
        if (gx > -spread && gx < w + spread) {
            val g = Path()
            g.moveTo(gx - spread * 0.72f, baseline)
            g.lineTo(gx, capTop + (baseline - capTop) * 0.10f)
            g.lineTo(gx + spread * 0.72f, baseline)
            drawPath(
                path = g,
                color = p.ink.copy(alpha = 0.16f),
                style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
            )
        }
    }
}

// ------------------------------------------------------------- computing ---

/** A shell, mid-session. */
private fun DrawScope.artTerminal(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val x0 = w * 0.08f
    val y0 = h * 0.12f
    val ww = w * 0.84f
    val wh = h * 0.76f
    val chrome = unit * 0.16f
    drawRect(color = p.ink.copy(alpha = 0.10f), topLeft = Offset(x0, y0), size = Size(ww, wh))
    drawRect(color = p.ink.copy(alpha = 0.26f), topLeft = Offset(x0, y0), size = Size(ww, chrome))
    drawRect(
        color = p.ink.copy(alpha = 0.72f),
        topLeft = Offset(x0, y0),
        size = Size(ww, wh),
        style = Stroke(width = unit * 0.020f)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.50f),
        start = Offset(x0, y0 + chrome),
        end = Offset(x0 + ww, y0 + chrome),
        strokeWidth = unit * 0.014f
    )
    for (i in 0 until 3) {
        drawCircle(
            color = p.ink.copy(alpha = 0.60f - i * 0.12f),
            radius = chrome * 0.22f,
            center = Offset(x0 + chrome * (0.42f + i * 0.60f), y0 + chrome * 0.50f)
        )
    }
    val rule = unit * 0.135f
    val lines = ((wh - chrome) / rule).toInt().coerceIn(2, 7)
    for (i in 0 until lines) {
        val ly = y0 + chrome + rule * (i + 0.72f)
        if (ly < y0 + wh - rule * 0.30f) {
            val ind = if (i == 0) 0f else (i % 3) * unit * 0.11f
            if (i == 0) {
                drawLine(
                    color = p.ink.copy(alpha = 0.85f),
                    start = Offset(x0 + unit * 0.09f, ly),
                    end = Offset(x0 + unit * 0.17f, ly),
                    strokeWidth = unit * 0.026f,
                    cap = StrokeCap.Round
                )
            }
            val sx = x0 + unit * (if (i == 0) 0.24f else 0.11f) + ind
            val frac = 0.34f + r.range(0f, 0.52f)
            drawLine(
                color = p.ink.copy(alpha = if (i == 0) 0.62f else 0.34f),
                start = Offset(sx, ly),
                end = Offset(sx + (x0 + ww - unit * 0.10f - sx) * frac, ly),
                strokeWidth = unit * 0.028f,
                cap = StrokeCap.Round
            )
        }
    }
    val cy = y0 + chrome + rule * (lines - 0.28f)
    if (cy < y0 + wh - unit * 0.05f) {
        drawRect(
            color = p.ink.copy(alpha = 0.80f),
            topLeft = Offset(x0 + unit * 0.11f, cy - rule * 0.34f),
            size = Size(unit * 0.045f, rule * 0.62f)
        )
    }
}

/** Bits: a bar is one, a ring is zero. */
private fun DrawScope.artBinary(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val step = unit * 0.20f
    val cols = (w / step).toInt().coerceIn(4, 40)
    val rows = (h / step).toInt().coerceIn(2, 9)
    val ox = (w - (cols - 1) * step) * 0.5f
    val oy = (h - (rows - 1) * step) * 0.5f
    for (c in 0 until cols) {
        val fade = 1f - abs(c / (cols - 1f) - 0.42f) * 0.9f
        for (rw in 0 until rows) {
            val cxx = ox + c * step
            val cyy = oy + rw * step
            val al = (0.14f + 0.46f * fade) * (0.55f + r.range(0f, 0.65f))
            if (r.int(2) == 0) {
                drawLine(
                    color = p.ink.copy(alpha = al),
                    start = Offset(cxx, cyy - step * 0.28f),
                    end = Offset(cxx, cyy + step * 0.28f),
                    strokeWidth = unit * 0.026f,
                    cap = StrokeCap.Round
                )
            } else {
                drawCircle(
                    color = p.ink.copy(alpha = al),
                    radius = step * 0.25f,
                    center = Offset(cxx, cyy),
                    style = Stroke(width = unit * 0.024f)
                )
            }
        }
    }
}

/** A graph, directed, the way a dependency actually looks. */
private fun DrawScope.artGraph(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cols = ((w / h) * 1.5f).toInt().coerceIn(2, 6)
    val step = w * 0.86f / (cols - 1 + 0.001f)
    val ox = w * 0.07f
    for (c in 0 until cols - 1) {
        val n0 = 1 + ((c + r.int(2)) % 2)
        val n1 = 1 + ((c + 1 + r.int(2)) % 2)
        for (a in 0 until n0) {
            for (b in 0 until n1) {
                val y0 = h * (0.5f + (a - (n0 - 1) * 0.5f) * 0.40f)
                val y1 = h * (0.5f + (b - (n1 - 1) * 0.5f) * 0.40f)
                drawLine(
                    color = p.ink.copy(alpha = 0.32f),
                    start = Offset(ox + c * step, y0),
                    end = Offset(ox + (c + 1) * step, y1),
                    strokeWidth = unit * 0.014f,
                    cap = StrokeCap.Round
                )
            }
        }
    }
    for (c in 0 until cols) {
        val n = 1 + ((c + r.int(2)) % 2)
        for (a in 0 until n) {
            val y = h * (0.5f + (a - (n - 1) * 0.5f) * 0.40f)
            val cxx = ox + c * step
            drawCircle(color = p.field, radius = unit * 0.088f, center = Offset(cxx, y))
            drawCircle(color = p.ink.copy(alpha = 0.85f), radius = unit * 0.082f, center = Offset(cxx, y))
            drawCircle(
                color = p.paper.copy(alpha = 0.55f),
                radius = unit * 0.030f,
                center = Offset(cxx - unit * 0.022f, y - unit * 0.024f)
            )
        }
    }
}

/** Braces, and the block they hold. */
private fun DrawScope.artBraces(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val top = h * 0.12f
    val bot = h * 0.88f
    val mid = (top + bot) * 0.5f
    val bw = unit * 0.16f
    for (k in 0 until 2) {
        val s = if (k == 0) 1f else -1f
        val bx = if (k == 0) w * 0.11f else w * 0.89f
        val br = Path()
        br.moveTo(bx + s * bw * 0.75f, top)
        br.cubicTo(
            bx - s * bw * 0.10f, top,
            bx + s * bw * 0.05f, top + (mid - top) * 0.40f,
            bx - s * bw * 0.55f, mid
        )
        br.cubicTo(
            bx + s * bw * 0.05f, mid + (bot - mid) * 0.60f,
            bx - s * bw * 0.10f, bot,
            bx + s * bw * 0.75f, bot
        )
        drawPath(
            path = br,
            color = p.ink.copy(alpha = 0.82f),
            style = Stroke(width = unit * 0.030f, cap = StrokeCap.Round)
        )
    }
    val rule = unit * 0.155f
    val lines = ((bot - top) / rule).toInt().coerceIn(2, 6)
    val innerL = w * 0.11f + bw * 1.2f
    val innerR = w * 0.89f - bw * 1.2f
    for (i in 0 until lines) {
        val ly = top + rule * (i + 0.70f)
        if (ly < bot - rule * 0.2f) {
            val ind = (if (i == 0) 0f else 1f) * unit * 0.14f + (if (i == lines - 1) -unit * 0.14f else 0f)
            val sx = innerL + ind + unit * 0.06f
            val frac = 0.40f + r.range(0f, 0.50f)
            drawLine(
                color = p.ink.copy(alpha = 0.26f + (if (i == 0) 0.26f else 0f)),
                start = Offset(sx, ly),
                end = Offset(sx + (innerR - sx) * frac, ly),
                strokeWidth = unit * 0.034f,
                cap = StrokeCap.Round
            )
        }
    }
}

/** A die, and the legs it stands on. */
private fun DrawScope.artChip(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val half = unit * 0.30f
    val cx = w * 0.50f
    val cy = h * 0.52f
    val pins = 4
    val leg = unit * 0.13f
    for (side in 0 until 4) {
        for (i in 0 until pins) {
            val t = (i + 0.5f) / pins
            val px0 = cx - half + half * 2f * t
            val py0 = cy - half + half * 2f * t
            if (side == 0) {
                drawLine(
                    color = p.ink.copy(alpha = 0.55f),
                    start = Offset(px0, cy - half),
                    end = Offset(px0, cy - half - leg),
                    strokeWidth = unit * 0.024f,
                    cap = StrokeCap.Round
                )
            } else if (side == 1) {
                drawLine(
                    color = p.ink.copy(alpha = 0.55f),
                    start = Offset(px0, cy + half),
                    end = Offset(px0, cy + half + leg),
                    strokeWidth = unit * 0.024f,
                    cap = StrokeCap.Round
                )
            } else if (side == 2) {
                drawLine(
                    color = p.ink.copy(alpha = 0.55f),
                    start = Offset(cx - half, py0),
                    end = Offset(cx - half - leg, py0),
                    strokeWidth = unit * 0.024f,
                    cap = StrokeCap.Round
                )
            } else {
                drawLine(
                    color = p.ink.copy(alpha = 0.55f),
                    start = Offset(cx + half, py0),
                    end = Offset(cx + half + leg, py0),
                    strokeWidth = unit * 0.024f,
                    cap = StrokeCap.Round
                )
            }
        }
    }
    drawRect(
        color = p.ink.copy(alpha = 0.16f),
        topLeft = Offset(cx - half, cy - half),
        size = Size(half * 2f, half * 2f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.85f),
        topLeft = Offset(cx - half, cy - half),
        size = Size(half * 2f, half * 2f),
        style = Stroke(width = unit * 0.024f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.34f),
        topLeft = Offset(cx - half * 0.56f, cy - half * 0.56f),
        size = Size(half * 1.12f, half * 1.12f),
        style = Stroke(width = unit * 0.014f)
    )
    drawCircle(color = p.ink.copy(alpha = 0.70f), radius = unit * 0.034f, center = Offset(cx - half * 0.74f, cy - half * 0.74f))
    for (i in 0 until 3) {
        val ty = cy - half * 0.30f + i * half * 0.30f
        drawLine(
            color = p.ink.copy(alpha = 0.34f),
            start = Offset(cx - half * 0.40f, ty),
            end = Offset(cx + half * 0.40f, ty),
            strokeWidth = unit * 0.013f
        )
    }
    val trace = ((w / h) * 1.6f).toInt().coerceIn(1, 5)
    for (i in 0 until trace) {
        val ty = h * (0.16f + i * 0.18f)
        drawLine(
            color = p.ink.copy(alpha = 0.14f),
            start = Offset(0f, ty),
            end = Offset(w, ty),
            strokeWidth = unit * 0.011f
        )
    }
}

// -------------------------------------------------------------- commerce ---

/** Stacks of coins, counted. */
private fun DrawScope.artCoins(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val rx = unit * 0.22f
    val ry = rx * 0.34f
    val thick = ry * 0.85f
    val stacks = (w / (rx * 2.6f)).toInt().coerceIn(2, 6)
    val gap = w / (stacks + 0.6f)
    val ground = h * 0.88f
    for (s in 0 until stacks) {
        val cx = gap * (s + 0.8f)
        val n = 2 + r.int(4)
        for (i in 0 until n) {
            val cy = ground - ry - i * thick
            drawArc(
                color = p.ink.copy(alpha = 0.20f),
                startAngle = 0f,
                sweepAngle = 180f,
                useCenter = true,
                topLeft = Offset(cx - rx, cy - ry),
                size = Size(rx * 2f, ry * 2f)
            )
            drawLine(
                color = p.ink.copy(alpha = 0.70f),
                start = Offset(cx - rx, cy),
                end = Offset(cx - rx, cy - thick * 0.02f),
                strokeWidth = unit * 0.016f
            )
            drawArc(
                color = p.ink.copy(alpha = 0.78f),
                startAngle = 0f,
                sweepAngle = 180f,
                useCenter = false,
                topLeft = Offset(cx - rx, cy - ry),
                size = Size(rx * 2f, ry * 2f),
                style = Stroke(width = unit * 0.018f, cap = StrokeCap.Round)
            )
            if (i == n - 1) {
                drawArc(
                    color = p.ink.copy(alpha = 0.14f),
                    startAngle = 0f,
                    sweepAngle = 360f,
                    useCenter = false,
                    topLeft = Offset(cx - rx, cy - ry - thick),
                    size = Size(rx * 2f, ry * 2f)
                )
                drawArc(
                    color = p.ink.copy(alpha = 0.85f),
                    startAngle = 0f,
                    sweepAngle = 360f,
                    useCenter = false,
                    topLeft = Offset(cx - rx, cy - ry - thick),
                    size = Size(rx * 2f, ry * 2f),
                    style = Stroke(width = unit * 0.020f)
                )
                drawArc(
                    color = p.ink.copy(alpha = 0.40f),
                    startAngle = 0f,
                    sweepAngle = 360f,
                    useCenter = false,
                    topLeft = Offset(cx - rx * 0.52f, cy - ry * 0.52f - thick),
                    size = Size(rx * 1.04f, ry * 1.04f),
                    style = Stroke(width = unit * 0.013f)
                )
            }
        }
    }
    drawLine(
        color = p.ink.copy(alpha = 0.30f),
        start = Offset(w * 0.02f, ground + ry * 0.3f),
        end = Offset(w * 0.98f, ground + ry * 0.3f),
        strokeWidth = unit * 0.012f
    )
}

/** Supply, demand, and the price where they meet. */
private fun DrawScope.artSupplyDemand(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val ox = w * 0.16f
    val oy = h * 0.84f
    val gw = w * 0.74f
    val gh = h * 0.68f
    val grid = (gw / (unit * 0.26f)).toInt().coerceIn(3, 14)
    for (i in 0 until grid + 1) {
        drawLine(
            color = p.ink.copy(alpha = 0.08f),
            start = Offset(ox + gw * i / grid, oy - gh),
            end = Offset(ox + gw * i / grid, oy),
            strokeWidth = unit * 0.008f
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(ox, oy),
        end = Offset(ox + gw + unit * 0.07f, oy),
        strokeWidth = unit * 0.017f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.60f),
        start = Offset(ox, oy),
        end = Offset(ox, oy - gh - unit * 0.07f),
        strokeWidth = unit * 0.017f,
        cap = StrokeCap.Round
    )
    val ex = ox + gw * (0.46f + r.range(0f, 0.12f))
    val ey = oy - gh * (0.46f + r.range(0f, 0.12f))
    drawLine(
        color = p.ink.copy(alpha = 0.80f),
        start = Offset(ox + gw * 0.06f, oy - gh * 0.12f),
        end = Offset(ox + gw * 0.94f, oy - gh * 0.92f),
        strokeWidth = unit * 0.024f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.52f),
        start = Offset(ox + gw * 0.06f, oy - gh * 0.92f),
        end = Offset(ox + gw * 0.94f, oy - gh * 0.12f),
        strokeWidth = unit * 0.024f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.26f),
        start = Offset(ox, ey),
        end = Offset(ex, ey),
        strokeWidth = unit * 0.012f
    )
    drawLine(
        color = p.ink.copy(alpha = 0.26f),
        start = Offset(ex, oy),
        end = Offset(ex, ey),
        strokeWidth = unit * 0.012f
    )
    drawCircle(color = p.field, radius = unit * 0.082f, center = Offset(ex, ey))
    drawCircle(color = p.ink, radius = unit * 0.060f, center = Offset(ex, ey))
    drawCircle(color = p.paper.copy(alpha = 0.70f), radius = unit * 0.022f, center = Offset(ex, ey))
}

/** A share of the whole, with one slice pulled out. */
private fun DrawScope.artPie(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val rad = unit * 0.40f
    val cx = w * 0.42f
    val cy = h * 0.52f
    val start = r.range(-120f, -40f)
    val a0 = 96f + r.range(0f, 40f)
    val a1 = 78f + r.range(0f, 40f)
    val a2 = 360f - a0 - a1
    drawArc(
        color = p.ink.copy(alpha = 0.16f),
        startAngle = start + a0,
        sweepAngle = a1,
        useCenter = true,
        topLeft = Offset(cx - rad, cy - rad),
        size = Size(rad * 2f, rad * 2f)
    )
    drawArc(
        color = p.ink.copy(alpha = 0.40f),
        startAngle = start + a0 + a1,
        sweepAngle = a2,
        useCenter = true,
        topLeft = Offset(cx - rad, cy - rad),
        size = Size(rad * 2f, rad * 2f)
    )
    drawArc(
        color = p.ink.copy(alpha = 0.78f),
        startAngle = start,
        sweepAngle = 360f,
        useCenter = false,
        topLeft = Offset(cx - rad, cy - rad),
        size = Size(rad * 2f, rad * 2f),
        style = Stroke(width = unit * 0.020f)
    )
    val mid = (start + a0 * 0.5f) * PI.toFloat() / 180f
    val push = rad * 0.16f
    val px0 = cx + cos(mid) * push
    val py0 = cy + sin(mid) * push
    drawArc(
        color = p.ink.copy(alpha = 0.86f),
        startAngle = start,
        sweepAngle = a0,
        useCenter = true,
        topLeft = Offset(px0 - rad, py0 - rad),
        size = Size(rad * 2f, rad * 2f)
    )
    drawArc(
        color = p.paper.copy(alpha = 0.40f),
        startAngle = start,
        sweepAngle = a0,
        useCenter = true,
        topLeft = Offset(px0 - rad * 0.30f, py0 - rad * 0.30f),
        size = Size(rad * 0.60f, rad * 0.60f)
    )
    val keys = ((w - cx - rad) / (unit * 0.22f)).toInt().coerceIn(0, 3)
    for (i in 0 until keys) {
        val ky = cy - unit * 0.22f + i * unit * 0.22f
        val kx = cx + rad + unit * 0.22f
        drawCircle(color = p.ink.copy(alpha = 0.85f - i * 0.26f), radius = unit * 0.045f, center = Offset(kx, ky))
        drawLine(
            color = p.ink.copy(alpha = 0.28f),
            start = Offset(kx + unit * 0.10f, ky),
            end = Offset(kx + unit * 0.10f + (w * 0.96f - kx - unit * 0.10f) * (0.55f + r.range(0f, 0.40f)), ky),
            strokeWidth = unit * 0.026f,
            cap = StrokeCap.Round
        )
    }
}

/** A receipt, torn off. */
private fun DrawScope.artReceipt(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val half = unit * 0.34f
    val top = h * 0.08f
    val bot = h * 0.86f
    val teeth = 7
    val tz = unit * 0.07f
    drawRect(
        color = p.ink.copy(alpha = 0.10f),
        topLeft = Offset(cx - half, top),
        size = Size(half * 2f, bot - top)
    )
    val edge = Path()
    edge.moveTo(cx - half, bot)
    for (i in 0 until teeth) {
        edge.lineTo(cx - half + half * 2f * (i + 0.5f) / teeth, bot + (if (i % 2 == 0) tz else -tz * 0.2f))
    }
    edge.lineTo(cx + half, bot)
    edge.lineTo(cx + half, top)
    edge.lineTo(cx - half, top)
    edge.close()
    drawPath(
        path = edge,
        color = p.ink.copy(alpha = 0.80f),
        style = Stroke(width = unit * 0.020f, cap = StrokeCap.Round)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.70f),
        start = Offset(cx - half * 0.54f, top + unit * 0.13f),
        end = Offset(cx + half * 0.54f, top + unit * 0.13f),
        strokeWidth = unit * 0.036f,
        cap = StrokeCap.Round
    )
    val rule = unit * 0.115f
    val rows = ((bot - top - unit * 0.42f) / rule).toInt().coerceIn(2, 6)
    for (i in 0 until rows) {
        val ly = top + unit * 0.30f + rule * (i + 0.6f)
        if (ly < bot - unit * 0.14f) {
            drawLine(
                color = p.ink.copy(alpha = 0.32f),
                start = Offset(cx - half * 0.76f, ly),
                end = Offset(cx - half * 0.76f + half * 0.86f * (0.5f + r.range(0f, 0.5f)), ly),
                strokeWidth = unit * 0.024f,
                cap = StrokeCap.Round
            )
            drawLine(
                color = p.ink.copy(alpha = 0.46f),
                start = Offset(cx + half * 0.30f, ly),
                end = Offset(cx + half * 0.76f, ly),
                strokeWidth = unit * 0.024f,
                cap = StrokeCap.Round
            )
        }
    }
    val sumy = top + unit * 0.30f + rule * (rows + 0.35f)
    if (sumy < bot - unit * 0.06f) {
        drawLine(
            color = p.ink.copy(alpha = 0.40f),
            start = Offset(cx - half * 0.76f, sumy - rule * 0.45f),
            end = Offset(cx + half * 0.76f, sumy - rule * 0.45f),
            strokeWidth = unit * 0.011f
        )
        drawLine(
            color = p.ink.copy(alpha = 0.85f),
            start = Offset(cx + half * 0.16f, sumy),
            end = Offset(cx + half * 0.76f, sumy),
            strokeWidth = unit * 0.030f,
            cap = StrokeCap.Round
        )
    }
}

// ---------------------------------------------------------------- social ---

/** A globe, with the graticule that makes it one. */
private fun DrawScope.artGlobe(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val cy = h * 0.52f
    val rad = unit * 0.42f
    drawCircle(color = p.ink.copy(alpha = 0.10f), radius = rad, center = Offset(cx, cy))
    drawCircle(
        color = p.ink.copy(alpha = 0.84f),
        radius = rad,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.024f)
    )
    for (i in 0 until 3) {
        val f = (i + 1f) / 4f
        val yy = cy - rad * 0.66f + rad * 1.32f * f
        val rr = sqrt(rad * rad - (yy - cy) * (yy - cy))
        drawLine(
            color = p.ink.copy(alpha = 0.40f),
            start = Offset(cx - rr, yy),
            end = Offset(cx + rr, yy),
            strokeWidth = unit * 0.014f,
            cap = StrokeCap.Round
        )
    }
    for (i in 0 until 3) {
        val f = (i + 0.5f) / 3f
        val rx = rad * abs(cos(f * PI.toFloat()))
        drawArc(
            color = p.ink.copy(alpha = 0.40f),
            startAngle = 0f,
            sweepAngle = 360f,
            useCenter = false,
            topLeft = Offset(cx - rx, cy - rad),
            size = Size(rx * 2f, rad * 2f),
            style = Stroke(width = unit * 0.014f)
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.55f),
        start = Offset(cx, cy - rad),
        end = Offset(cx, cy + rad),
        strokeWidth = unit * 0.014f
    )
    for (i in 0 until 3) {
        val a = r.range(0f, 6.2832f)
        val dist = rad * r.range(0.20f, 0.74f)
        drawCircle(color = p.ink.copy(alpha = 0.66f), radius = unit * 0.036f, center = Offset(cx + cos(a) * dist, cy + sin(a) * dist))
    }
}

/** A stupa on its plinth: the shape a heritage chapter is about. */
private fun DrawScope.artMonument(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val ground = h * 0.90f
    val domeR = unit * 0.30f
    val domeY = ground - unit * 0.34f
    val steps = 3
    for (i in 0 until steps) {
        val sw = domeR * (1.85f - i * 0.28f)
        val sy = ground - i * unit * 0.075f
        drawRect(
            color = p.ink.copy(alpha = 0.22f + i * 0.10f),
            topLeft = Offset(cx - sw, sy - unit * 0.075f),
            size = Size(sw * 2f, unit * 0.075f)
        )
        drawRect(
            color = p.ink.copy(alpha = 0.70f),
            topLeft = Offset(cx - sw, sy - unit * 0.075f),
            size = Size(sw * 2f, unit * 0.075f),
            style = Stroke(width = unit * 0.014f)
        )
    }
    drawArc(
        color = p.ink.copy(alpha = 0.22f),
        startAngle = 180f,
        sweepAngle = 180f,
        useCenter = true,
        topLeft = Offset(cx - domeR, domeY - domeR),
        size = Size(domeR * 2f, domeR * 2f)
    )
    drawArc(
        color = p.ink.copy(alpha = 0.85f),
        startAngle = 180f,
        sweepAngle = 180f,
        useCenter = false,
        topLeft = Offset(cx - domeR, domeY - domeR),
        size = Size(domeR * 2f, domeR * 2f),
        style = Stroke(width = unit * 0.022f, cap = StrokeCap.Round)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.80f),
        topLeft = Offset(cx - domeR * 0.40f, domeY - domeR - unit * 0.14f),
        size = Size(domeR * 0.80f, unit * 0.14f)
    )
    val spireBase = domeY - domeR - unit * 0.14f
    val tiers = 4
    for (i in 0 until tiers) {
        val tw = domeR * (0.34f - i * 0.055f)
        drawLine(
            color = p.ink.copy(alpha = 0.78f),
            start = Offset(cx - tw, spireBase - i * unit * 0.055f),
            end = Offset(cx + tw, spireBase - i * unit * 0.055f),
            strokeWidth = unit * 0.026f,
            cap = StrokeCap.Round
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(cx, spireBase - tiers * unit * 0.055f),
        end = Offset(cx, spireBase - tiers * unit * 0.055f - unit * 0.12f),
        strokeWidth = unit * 0.020f,
        cap = StrokeCap.Round
    )
    drawCircle(color = p.ink, radius = unit * 0.038f, center = Offset(cx, spireBase - tiers * unit * 0.055f - unit * 0.15f))
    val flags = ((w / h) * 0.9f).toInt().coerceIn(0, 2)
    for (i in 0 until flags) {
        val s = if (i == 0) -1f else 1f
        val ex = cx + s * (domeR * 2.6f)
        if (ex > unit * 0.10f && ex < w - unit * 0.10f) {
            drawLine(
                color = p.ink.copy(alpha = 0.20f),
                start = Offset(cx + s * domeR * 0.20f, spireBase - unit * 0.02f),
                end = Offset(ex, domeY - domeR * 0.30f),
                strokeWidth = unit * 0.010f
            )
            for (j in 0 until 4) {
                val t = (j + 1f) / 5f
                val fx = cx + s * domeR * 0.20f + (ex - cx - s * domeR * 0.20f) * t
                val fy = spireBase - unit * 0.02f + (domeY - domeR * 0.30f - spireBase + unit * 0.02f) * t
                drawRect(
                    color = p.ink.copy(alpha = 0.26f),
                    topLeft = Offset(fx - unit * 0.020f, fy),
                    size = Size(unit * 0.040f, unit * 0.055f)
                )
            }
        }
    }
    drawLine(
        color = p.ink.copy(alpha = 0.30f),
        start = Offset(0f, ground),
        end = Offset(w, ground),
        strokeWidth = unit * 0.012f
    )
}

/** A rose, and the needle that keeps finding north. */
private fun DrawScope.artCompass(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val cy = h * 0.52f
    val rad = unit * 0.42f
    drawCircle(color = p.ink.copy(alpha = 0.09f), radius = rad, center = Offset(cx, cy))
    drawCircle(
        color = p.ink.copy(alpha = 0.80f),
        radius = rad,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.022f)
    )
    drawCircle(
        color = p.ink.copy(alpha = 0.26f),
        radius = rad * 0.86f,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.011f)
    )
    val ticks = 16
    for (i in 0 until ticks) {
        val a = i * (PI.toFloat() * 2f / ticks)
        val major = i % 4 == 0
        val r0 = rad * (if (major) 0.70f else 0.80f)
        drawLine(
            color = p.ink.copy(alpha = if (major) 0.62f else 0.30f),
            start = Offset(cx + cos(a) * r0, cy + sin(a) * r0),
            end = Offset(cx + cos(a) * rad * 0.92f, cy + sin(a) * rad * 0.92f),
            strokeWidth = unit * (if (major) 0.018f else 0.011f),
            cap = StrokeCap.Round
        )
    }
    val spin = r.range(-0.5f, 0.5f) - PI.toFloat() / 2f
    val nx = cos(spin)
    val ny = sin(spin)
    val wing = rad * 0.20f
    val nd = Path()
    nd.moveTo(cx + nx * rad * 0.80f, cy + ny * rad * 0.80f)
    nd.lineTo(cx - ny * wing, cy + nx * wing)
    nd.lineTo(cx + ny * wing, cy - nx * wing)
    nd.close()
    drawPath(path = nd, color = p.ink.copy(alpha = 0.88f))
    val sd = Path()
    sd.moveTo(cx - nx * rad * 0.80f, cy - ny * rad * 0.80f)
    sd.lineTo(cx - ny * wing, cy + nx * wing)
    sd.lineTo(cx + ny * wing, cy - nx * wing)
    sd.close()
    drawPath(path = sd, color = p.ink.copy(alpha = 0.30f))
    drawCircle(color = p.field, radius = unit * 0.060f, center = Offset(cx, cy))
    drawCircle(
        color = p.ink.copy(alpha = 0.85f),
        radius = unit * 0.052f,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.018f)
    )
}

// ---------------------------------------------------------------- health ---

/** A figure, running, reduced to the lines that carry the motion. */
private fun DrawScope.artRunner(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.52f
    val hipY = h * 0.56f
    val s = unit * 0.20f
    val stroke = unit * 0.034f
    drawCircle(color = p.ink.copy(alpha = 0.88f), radius = s * 0.40f, center = Offset(cx + s * 0.55f, hipY - s * 1.70f))
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx + s * 0.35f, hipY - s * 1.25f),
        end = Offset(cx - s * 0.10f, hipY),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx + s * 0.22f, hipY - s * 1.00f),
        end = Offset(cx + s * 1.05f, hipY - s * 1.30f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx + s * 1.05f, hipY - s * 1.30f),
        end = Offset(cx + s * 1.30f, hipY - s * 0.66f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx + s * 0.22f, hipY - s * 1.00f),
        end = Offset(cx - s * 0.80f, hipY - s * 1.10f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx - s * 0.80f, hipY - s * 1.10f),
        end = Offset(cx - s * 1.00f, hipY - s * 0.46f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx - s * 0.10f, hipY),
        end = Offset(cx + s * 0.60f, hipY + s * 0.66f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx + s * 0.60f, hipY + s * 0.66f),
        end = Offset(cx + s * 0.44f, hipY + s * 1.60f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx - s * 0.10f, hipY),
        end = Offset(cx - s * 1.10f, hipY + s * 0.30f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx - s * 1.10f, hipY + s * 0.30f),
        end = Offset(cx - s * 1.34f, hipY + s * 1.30f),
        strokeWidth = stroke,
        cap = StrokeCap.Round
    )
    val trails = ((w / h) * 2f).toInt().coerceIn(2, 6)
    for (i in 0 until trails) {
        val ty = hipY - s * (1.30f - i * 0.62f)
        drawLine(
            color = p.ink.copy(alpha = 0.22f),
            start = Offset(cx - s * (2.0f + i * 0.5f), ty),
            end = Offset(cx - s * (3.4f + i * 0.9f), ty),
            strokeWidth = unit * 0.020f,
            cap = StrokeCap.Round
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.30f),
        start = Offset(0f, hipY + s * 1.72f),
        end = Offset(w, hipY + s * 1.72f),
        strokeWidth = unit * 0.012f
    )
}

/** One apple, and the seeds of the next. */
private fun DrawScope.artApple(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val extras = ((w / h) * 1.1f).toInt().coerceIn(0, 3)
    for (k in 0 until extras + 1) {
        val lead = k == 0
        val sc = if (lead) 1f else 0.46f + r.range(0f, 0.12f)
        val side = if (k % 2 == 1) -1f else 1f
        val tier = (k + 1) / 2
        val rad = unit * 0.32f * sc
        val cx = if (lead) w * 0.50f else w * 0.50f + side * unit * (0.62f + tier * 0.40f)
        val cy = if (lead) h * 0.60f else h * 0.66f
        val al = if (lead) 0.86f else 0.34f
        if (cx > rad && cx < w - rad) {
            val body = Path()
            body.moveTo(cx, cy - rad * 0.72f)
            body.cubicTo(cx - rad * 0.50f, cy - rad * 1.24f, cx - rad * 1.36f, cy - rad * 0.50f, cx - rad * 1.00f, cy + rad * 0.44f)
            body.cubicTo(cx - rad * 0.78f, cy + rad * 1.20f, cx - rad * 0.18f, cy + rad * 1.28f, cx, cy + rad * 0.96f)
            body.cubicTo(cx + rad * 0.18f, cy + rad * 1.28f, cx + rad * 0.78f, cy + rad * 1.20f, cx + rad * 1.00f, cy + rad * 0.44f)
            body.cubicTo(cx + rad * 1.36f, cy - rad * 0.50f, cx + rad * 0.50f, cy - rad * 1.24f, cx, cy - rad * 0.72f)
            body.close()
            drawPath(path = body, color = p.ink.copy(alpha = al * 0.22f))
            drawPath(
                path = body,
                color = p.ink.copy(alpha = al),
                style = Stroke(width = unit * 0.024f * (0.62f + sc * 0.38f), cap = StrokeCap.Round)
            )
            drawLine(
                color = p.ink.copy(alpha = al),
                start = Offset(cx, cy - rad * 0.72f),
                end = Offset(cx + rad * 0.10f, cy - rad * 1.34f),
                strokeWidth = unit * 0.024f * (0.62f + sc * 0.38f),
                cap = StrokeCap.Round
            )
            if (lead) {
                val leaf = Path()
                leaf.moveTo(cx + rad * 0.08f, cy - rad * 1.16f)
                leaf.cubicTo(cx + rad * 0.62f, cy - rad * 1.52f, cx + rad * 0.92f, cy - rad * 1.16f, cx + rad * 0.86f, cy - rad * 0.86f)
                leaf.cubicTo(cx + rad * 0.56f, cy - rad * 0.80f, cx + rad * 0.20f, cy - rad * 0.96f, cx + rad * 0.08f, cy - rad * 1.16f)
                leaf.close()
                drawPath(path = leaf, color = p.ink.copy(alpha = 0.60f))
                drawArc(
                    color = p.paper.copy(alpha = 0.34f),
                    startAngle = 185f,
                    sweepAngle = 62f,
                    useCenter = false,
                    topLeft = Offset(cx - rad * 0.74f, cy - rad * 0.50f),
                    size = Size(rad * 1.0f, rad * 1.2f),
                    style = Stroke(width = unit * 0.030f, cap = StrokeCap.Round)
                )
            }
        }
    }
}

/** Closing the rings. */
private fun DrawScope.artRings(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val cy = h * 0.52f
    val outer = unit * 0.42f
    val band = unit * 0.075f
    for (i in 0 until 3) {
        val rad = outer - i * (band * 1.55f)
        drawCircle(
            color = p.ink.copy(alpha = 0.14f),
            radius = rad,
            center = Offset(cx, cy),
            style = Stroke(width = band)
        )
        val sweep = 200f + r.range(0f, 150f)
        drawArc(
            color = p.ink.copy(alpha = 0.86f - i * 0.20f),
            startAngle = -90f,
            sweepAngle = sweep,
            useCenter = false,
            topLeft = Offset(cx - rad, cy - rad),
            size = Size(rad * 2f, rad * 2f),
            style = Stroke(width = band, cap = StrokeCap.Round)
        )
        val ea = (-90f + sweep) * PI.toFloat() / 180f
        drawCircle(
            color = p.paper.copy(alpha = 0.40f),
            radius = band * 0.22f,
            center = Offset(cx + cos(ea) * rad, cy + sin(ea) * rad)
        )
    }
    val pips = ((w / h) * 2.2f).toInt().coerceIn(0, 6)
    for (i in 0 until pips) {
        val s = if (i % 2 == 0) -1f else 1f
        val k = i / 2
        drawCircle(
            color = p.ink.copy(alpha = 0.22f),
            radius = unit * (0.030f - k * 0.006f),
            center = Offset(cx + s * (outer + unit * (0.20f + k * 0.18f)), cy + (if (k % 2 == 0) -unit * 0.14f else unit * 0.16f))
        )
    }
}

/** Water: the thing every health chapter starts with. */
private fun DrawScope.artDrop(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val drops = ((w / h) * 1.6f).toInt().coerceIn(1, 5)
    for (k in 0 until drops) {
        val lead = k == 0
        val sc = if (lead) 1f else 0.42f + r.range(0f, 0.22f)
        val cx = if (lead) w * 0.46f else w * (0.10f + k * 0.21f)
        val cy = if (lead) h * 0.56f else h * (0.24f + (k % 2) * 0.50f)
        val rad = unit * 0.28f * sc
        val al = if (lead) 0.86f else 0.30f
        val shape = Path()
        shape.moveTo(cx, cy - rad * 1.70f)
        shape.cubicTo(cx + rad * 0.52f, cy - rad * 0.86f, cx + rad, cy - rad * 0.30f, cx + rad, cy + rad * 0.18f)
        shape.cubicTo(cx + rad, cy + rad * 1.02f, cx - rad, cy + rad * 1.02f, cx - rad, cy + rad * 0.18f)
        shape.cubicTo(cx - rad, cy - rad * 0.30f, cx - rad * 0.52f, cy - rad * 0.86f, cx, cy - rad * 1.70f)
        shape.close()
        drawPath(path = shape, color = p.ink.copy(alpha = al * 0.22f))
        drawPath(
            path = shape,
            color = p.ink.copy(alpha = al),
            style = Stroke(width = unit * 0.022f * (0.6f + sc * 0.4f), cap = StrokeCap.Round)
        )
        if (lead) {
            drawArc(
                color = p.paper.copy(alpha = 0.42f),
                startAngle = 130f,
                sweepAngle = 80f,
                useCenter = false,
                topLeft = Offset(cx - rad * 0.58f, cy - rad * 0.50f),
                size = Size(rad * 1.16f, rad * 1.16f),
                style = Stroke(width = unit * 0.028f, cap = StrokeCap.Round)
            )
            for (i in 0 until 3) {
                drawArc(
                    color = p.ink.copy(alpha = 0.22f - i * 0.05f),
                    startAngle = 200f,
                    sweepAngle = 140f,
                    useCenter = false,
                    topLeft = Offset(cx - rad * (1.5f + i * 0.5f), cy + rad * (0.80f - (0.24f + i * 0.10f))),
                    size = Size(rad * (3.0f + i * 1.0f), rad * (0.48f + i * 0.20f)),
                    style = Stroke(width = unit * 0.013f, cap = StrokeCap.Round)
                )
            }
        }
    }
}

// ------------------------------------------------------------------ exam ---

/** A list, being worked through. */
private fun DrawScope.artChecklist(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val box = unit * 0.17f
    val rule = box * 1.55f
    val rows = (h * 0.84f / rule).toInt().coerceIn(2, 5)
    val ox = w * 0.12f
    val oy = h * 0.5f - (rows - 1) * rule * 0.5f
    for (i in 0 until rows) {
        val cy = oy + i * rule
        val done = i < rows - 1
        drawRect(
            color = p.ink.copy(alpha = if (done) 0.80f else 0.16f),
            topLeft = Offset(ox, cy - box * 0.5f),
            size = Size(box, box)
        )
        drawRect(
            color = p.ink.copy(alpha = if (done) 0.88f else 0.55f),
            topLeft = Offset(ox, cy - box * 0.5f),
            size = Size(box, box),
            style = Stroke(width = unit * 0.018f)
        )
        if (done) {
            val tick = Path()
            tick.moveTo(ox + box * 0.22f, cy + box * 0.02f)
            tick.lineTo(ox + box * 0.44f, cy + box * 0.24f)
            tick.lineTo(ox + box * 0.80f, cy - box * 0.26f)
            drawPath(
                path = tick,
                color = p.paper.copy(alpha = 0.92f),
                style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
            )
        }
        val sx = ox + box * 1.55f
        val frac = if (i == rows - 1) 0.52f else 0.72f + r.range(0f, 0.24f)
        drawLine(
            color = p.ink.copy(alpha = if (done) 0.30f else 0.50f),
            start = Offset(sx, cy),
            end = Offset(sx + (w * 0.92f - sx) * frac, cy),
            strokeWidth = unit * 0.032f,
            cap = StrokeCap.Round
        )
        if (done) {
            drawLine(
                color = p.ink.copy(alpha = 0.55f),
                start = Offset(sx, cy),
                end = Offset(sx + (w * 0.92f - sx) * frac, cy),
                strokeWidth = unit * 0.010f
            )
        }
    }
}

/** The clock, and how much of it is left. */
private fun DrawScope.artClock(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val cy = h * 0.52f
    val rad = unit * 0.40f
    drawCircle(color = p.ink.copy(alpha = 0.09f), radius = rad, center = Offset(cx, cy))
    val spent = 120f + r.range(0f, 160f)
    drawArc(
        color = p.ink.copy(alpha = 0.26f),
        startAngle = -90f,
        sweepAngle = spent,
        useCenter = true,
        topLeft = Offset(cx - rad * 0.94f, cy - rad * 0.94f),
        size = Size(rad * 1.88f, rad * 1.88f)
    )
    drawCircle(
        color = p.ink.copy(alpha = 0.84f),
        radius = rad,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.024f)
    )
    for (i in 0 until 12) {
        val a = i * (PI.toFloat() / 6f)
        val major = i % 3 == 0
        drawLine(
            color = p.ink.copy(alpha = if (major) 0.66f else 0.30f),
            start = Offset(cx + cos(a) * rad * (if (major) 0.76f else 0.84f), cy + sin(a) * rad * (if (major) 0.76f else 0.84f)),
            end = Offset(cx + cos(a) * rad * 0.92f, cy + sin(a) * rad * 0.92f),
            strokeWidth = unit * (if (major) 0.020f else 0.012f),
            cap = StrokeCap.Round
        )
    }
    val ha = (-90f + spent * 0.34f) * PI.toFloat() / 180f
    val ma = (-90f + spent) * PI.toFloat() / 180f
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx, cy),
        end = Offset(cx + cos(ha) * rad * 0.48f, cy + sin(ha) * rad * 0.48f),
        strokeWidth = unit * 0.030f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.88f),
        start = Offset(cx, cy),
        end = Offset(cx + cos(ma) * rad * 0.72f, cy + sin(ma) * rad * 0.72f),
        strokeWidth = unit * 0.022f,
        cap = StrokeCap.Round
    )
    drawCircle(color = p.ink, radius = unit * 0.040f, center = Offset(cx, cy))
    drawCircle(color = p.paper.copy(alpha = 0.80f), radius = unit * 0.014f, center = Offset(cx, cy))
}

/** The bullseye, and the one that found it. */
private fun DrawScope.artTarget(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.52f
    val cy = h * 0.50f
    val outer = unit * 0.42f
    for (i in 0 until 4) {
        val rad = outer * (1f - i * 0.235f)
        if (i % 2 == 0) {
            drawCircle(color = p.ink.copy(alpha = 0.13f), radius = rad, center = Offset(cx, cy))
        }
        drawCircle(
            color = p.ink.copy(alpha = 0.34f + i * 0.14f),
            radius = rad,
            center = Offset(cx, cy),
            style = Stroke(width = unit * 0.018f)
        )
    }
    drawCircle(color = p.ink, radius = outer * 0.10f, center = Offset(cx, cy))
    val a = r.range(2.5f, 3.6f)
    val ax = cx + cos(a) * outer * 2.1f
    val ay = cy + sin(a) * outer * 2.1f
    drawLine(
        color = p.ink.copy(alpha = 0.85f),
        start = Offset(ax, ay),
        end = Offset(cx - cos(a) * outer * 0.04f, cy - sin(a) * outer * 0.04f),
        strokeWidth = unit * 0.024f,
        cap = StrokeCap.Round
    )
    for (i in 0 until 2) {
        val s = if (i == 0) 1f else -1f
        drawLine(
            color = p.ink.copy(alpha = 0.70f),
            start = Offset(ax, ay),
            end = Offset(ax - cos(a) * outer * 0.40f - s * sin(a) * outer * 0.22f, ay - sin(a) * outer * 0.40f + s * cos(a) * outer * 0.22f),
            strokeWidth = unit * 0.020f,
            cap = StrokeCap.Round
        )
    }
    drawArc(
        color = p.ink.copy(alpha = 0.22f),
        startAngle = (a * 180f / PI.toFloat()) - 40f,
        sweepAngle = 80f,
        useCenter = false,
        topLeft = Offset(cx - outer * 1.70f, cy - outer * 1.70f),
        size = Size(outer * 3.40f, outer * 3.40f),
        style = Stroke(width = unit * 0.011f)
    )
}

/** A month with one date circled. */
private fun DrawScope.artCalendar(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cw = unit * 0.80f
    val ch = unit * 0.76f
    val ox = w * 0.5f - cw * 0.5f
    val oy = h * 0.5f - ch * 0.5f + unit * 0.03f
    val head = ch * 0.24f
    drawRect(color = p.ink.copy(alpha = 0.08f), topLeft = Offset(ox, oy), size = Size(cw, ch))
    drawRect(color = p.ink.copy(alpha = 0.72f), topLeft = Offset(ox, oy), size = Size(cw, head))
    drawRect(
        color = p.ink.copy(alpha = 0.82f),
        topLeft = Offset(ox, oy),
        size = Size(cw, ch),
        style = Stroke(width = unit * 0.020f)
    )
    for (i in 0 until 2) {
        val rx = ox + cw * (0.26f + i * 0.48f)
        drawLine(
            color = p.ink.copy(alpha = 0.85f),
            start = Offset(rx, oy - unit * 0.07f),
            end = Offset(rx, oy + head * 0.40f),
            strokeWidth = unit * 0.024f,
            cap = StrokeCap.Round
        )
    }
    val cols = 5
    val rows = 3
    val gx = cw / (cols + 1f)
    val gy = (ch - head) / (rows + 1f)
    val mark = 1 + r.int(cols * rows - 2)
    for (c in 0 until cols) {
        for (rw in 0 until rows) {
            val dx = ox + gx * (c + 1f)
            val dy = oy + head + gy * (rw + 1f)
            val idx = rw * cols + c
            if (idx == mark) {
                drawCircle(color = p.ink.copy(alpha = 0.88f), radius = unit * 0.055f, center = Offset(dx, dy))
                drawCircle(
                    color = p.ink.copy(alpha = 0.50f),
                    radius = unit * 0.090f,
                    center = Offset(dx, dy),
                    style = Stroke(width = unit * 0.014f)
                )
            } else {
                drawCircle(color = p.ink.copy(alpha = if (idx < mark) 0.20f else 0.40f), radius = unit * 0.032f, center = Offset(dx, dy))
            }
        }
    }
}

/** What the last thirty days are for. */
private fun DrawScope.artTrophy(p: BannerPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * 0.50f
    val top = h * 0.20f
    val cupH = unit * 0.36f
    val half = unit * 0.24f
    val cup = Path()
    cup.moveTo(cx - half, top)
    cup.cubicTo(cx - half, top + cupH * 0.70f, cx - half * 0.52f, top + cupH, cx, top + cupH)
    cup.cubicTo(cx + half * 0.52f, top + cupH, cx + half, top + cupH * 0.70f, cx + half, top)
    cup.close()
    drawPath(path = cup, color = p.ink.copy(alpha = 0.20f))
    drawPath(
        path = cup,
        color = p.ink.copy(alpha = 0.86f),
        style = Stroke(width = unit * 0.024f, cap = StrokeCap.Round)
    )
    drawLine(
        color = p.ink.copy(alpha = 0.86f),
        start = Offset(cx - half - unit * 0.04f, top),
        end = Offset(cx + half + unit * 0.04f, top),
        strokeWidth = unit * 0.026f,
        cap = StrokeCap.Round
    )
    for (i in 0 until 2) {
        val s = if (i == 0) -1f else 1f
        drawArc(
            color = p.ink.copy(alpha = 0.66f),
            startAngle = if (i == 0) 90f else -90f,
            sweepAngle = if (i == 0) 180f else 180f,
            useCenter = false,
            topLeft = Offset(cx + s * half - (if (i == 0) half * 0.52f else 0f), top + unit * 0.02f),
            size = Size(half * 0.52f, cupH * 0.52f),
            style = Stroke(width = unit * 0.020f, cap = StrokeCap.Round)
        )
    }
    drawLine(
        color = p.ink.copy(alpha = 0.86f),
        start = Offset(cx, top + cupH),
        end = Offset(cx, top + cupH + unit * 0.14f),
        strokeWidth = unit * 0.036f,
        cap = StrokeCap.Round
    )
    drawRect(
        color = p.ink.copy(alpha = 0.70f),
        topLeft = Offset(cx - half * 0.72f, top + cupH + unit * 0.14f),
        size = Size(half * 1.44f, unit * 0.070f)
    )
    drawRect(
        color = p.ink.copy(alpha = 0.34f),
        topLeft = Offset(cx - half * 1.00f, top + cupH + unit * 0.21f),
        size = Size(half * 2.00f, unit * 0.060f)
    )
    val stars = ((w / h) * 1.8f).toInt().coerceIn(2, 8)
    for (i in 0 until stars) {
        val s = if (i % 2 == 0) -1f else 1f
        val k = i / 2
        val sx = cx + s * (half * 1.7f + k * unit * 0.30f)
        val sy = h * (0.22f + (i % 3) * 0.22f)
        if (sx > unit * 0.05f && sx < w - unit * 0.05f) {
            val sr = unit * (0.055f - k * 0.008f)
            for (j in 0 until 2) {
                val a = j * (PI.toFloat() / 2f)
                drawLine(
                    color = p.ink.copy(alpha = 0.30f),
                    start = Offset(sx - cos(a) * sr, sy - sin(a) * sr),
                    end = Offset(sx + cos(a) * sr, sy + sin(a) * sr),
                    strokeWidth = unit * 0.014f,
                    cap = StrokeCap.Round
                )
            }
        }
    }
    drawArc(
        color = p.paper.copy(alpha = 0.36f),
        startAngle = 120f,
        sweepAngle = 70f,
        useCenter = false,
        topLeft = Offset(cx - half * 0.60f, top + cupH * 0.10f),
        size = Size(half * 0.70f, cupH * 0.80f),
        style = Stroke(width = unit * 0.026f, cap = StrokeCap.Round)
    )
}
