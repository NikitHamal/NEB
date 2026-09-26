package com.neb.ians.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.State
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathMeasure
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.drawscope.translate
import kotlin.math.ceil
import kotlin.math.hypot
import kotlin.math.min
import com.neb.ians.ui.theme.nebAnimationsReduced
import kotlinx.coroutines.delay
import kotlin.math.sin

// ---------------------------------------------------------------------------
// The splash doodle: the word "Nebians", handwritten, drawn on stroke by stroke.
//
// This is the one illustration in the app that is allowed to be blue. The
// journey's art (NebJourneyArt and friends) is strictly ink on paper and stays
// that way — see the note at the top of NebAuthPalette. The splash is different:
// it is the brand introducing itself, so it is written in the brand's own hue.
//
// The letterforms below are hand-authored cubics, not a font. A font rendered
// with a reveal mask looks like a font being uncovered; a pen path replayed at
// pen speed looks like someone writing. Four things do that work:
//
//   1. Time is allocated by arc length, not per letter. A long diagonal takes
//      longer than a short bar because the pen is moving at a roughly constant
//      speed, which is what a hand actually does.
//   2. Pen lifts cost time and draw nothing. Between strokes the clock keeps
//      running while the nib is off the paper, so the word arrives in bursts —
//      letter, lift, letter — instead of as one continuous smear.
//   3. The pen has pressure. A line of constant width is the clearest tell that
//      a machine drew it, and no amount of good timing hides it. Every stroke
//      is thin where the nib touches down and lifts off, full weight through
//      the body, with a slow drift in between and its own overall weight.
//   4. The curves are deliberately not symmetrical. Stems lean by a degree or
//      two and bowls are slightly heavier on one side, because a perfectly even
//      letter reads as vector art no matter how it is animated.
//
// Point 3 is why this file builds outlines instead of stroking paths. Compose
// can only stroke at one width per draw call, so a tapered stroke has to be cut
// into constant-width pieces — and each piece's round cap then bulges past its
// thinner neighbour's body, which scallops the edge into something closer to
// bamboo than to ink. Instead each stroke is sampled along its arc length, the
// centreline is offset by the half-width at each sample, and the resulting
// outline is filled in one call. Smooth at any taper, and cheaper besides: one
// fill and two end caps per stroke, against a hundred-odd stroked chunks.
//
// Coordinates live in a fixed 1000 x 330 viewport and are scaled to whatever box
// the composable is given, so the writing is resolution independent and the
// geometry can be built once and cached.
// ---------------------------------------------------------------------------

private const val ViewportWidth = 1040f
private const val ViewportHeight = 330f

/** Pen width at full pressure, in viewport units. A chisel marker, not a biro. */
private const val PenWidth = 30f

/** Spacing between centreline samples, in viewport units. */
private const val SampleStep = 3.5f

/** Width at the very tip of a letter stroke, as a fraction of full pressure. */
private const val LetterTipWeight = 0.62f

/** …and of the underline, which is a flick and tapers much harder. */
private const val SwashTipWeight = 0.12f

/**
 * The underline is drawn lighter than the letters. At the same weight it stops
 * being a flick of the wrist and becomes a rule ruled under the word.
 */
private const val SwashWeight = 0.68f

/**
 * How far a stroke spends coming up to full pressure, in viewport units.
 *
 * Absolute, not a fraction of the stroke: a hand accelerates the nib over about
 * the same distance whatever it is drawing, so a short bar is proportionally
 * more taper than a long diagonal. Capped at [MaxTaperFraction] of the stroke so
 * the two ends of a very short mark cannot overlap and fight.
 */
private const val LetterTaperUnits = 26f
private const val SwashTaperUnits = 260f
private const val MaxTaperFraction = 0.4f

/**
 * How long the nib spends off the paper between strokes, as a multiple of the
 * average stroke length. Tuned by eye: below about 0.15 the letters run into
 * each other, above about 0.35 the word feels hesitant.
 */
private const val PenLiftRatio = 0.22f

/**
 * What kind of mark a stroke is. The three differ only in how the pen is
 * loaded: a letter tapers gently at both ends, the swash is a lighter, harder
 * tapered flick, and a dot is a single press with no taper at all.
 */
private enum class Nib(val weight: Float, val tip: Float, val taper: Float) {
    Letter(1f, LetterTipWeight, LetterTaperUnits),
    Swash(SwashWeight, SwashTipWeight, SwashTaperUnits),
    Dot(0.88f, 1f, 0f)
}

private class StrokeSpec(val path: Path, val nib: Nib)

private fun wordmarkStrokes(): List<StrokeSpec> {
    val strokes = mutableListOf<StrokeSpec>()

    fun stroke(nib: Nib = Nib.Letter, build: Path.() -> Unit) {
        strokes += StrokeSpec(Path().apply(build), nib)
    }

    // N — one movement: up the left stem, down the diagonal, up the right stem.
    stroke {
        moveTo(46f, 254f)
        cubicTo(41f, 198f, 43f, 124f, 52f, 48f)
        cubicTo(85f, 108f, 122f, 172f, 160f, 246f)
        cubicTo(166f, 182f, 170f, 114f, 172f, 48f)
    }

    // e — the open bowl, then the bar across it. The bowl is drawn wide and the
    // bar sits high, because at this pen weight a tighter e fills in solid.
    stroke {
        moveTo(324f, 160f)
        cubicTo(304f, 122f, 252f, 117f, 228f, 150f)
        cubicTo(208f, 180f, 214f, 228f, 246f, 246f)
        cubicTo(268f, 258f, 304f, 248f, 322f, 230f)
    }
    stroke {
        moveTo(232f, 198f)
        cubicTo(260f, 191f, 294f, 191f, 320f, 196f)
    }

    // b — the ascender, then the bowl hung off it.
    stroke {
        moveTo(372f, 46f)
        cubicTo(368f, 120f, 366f, 188f, 369f, 254f)
    }
    stroke {
        moveTo(369f, 158f)
        cubicTo(402f, 130f, 452f, 138f, 470f, 170f)
        cubicTo(486f, 200f, 472f, 238f, 440f, 250f)
        cubicTo(408f, 260f, 380f, 246f, 368f, 226f)
    }

    // i — the stem, then the dot dropped on top.
    //
    // The dot is a short press, not a little circle. Drawn as a closed loop it
    // would be a ring tighter than the pen is wide, and offsetting the pen
    // inwards past the centre turns the outline inside out.
    stroke {
        moveTo(528f, 126f)
        cubicTo(525f, 168f, 524f, 214f, 527f, 254f)
    }
    stroke(nib = Nib.Dot) {
        moveTo(527f, 62f)
        cubicTo(527f, 66f, 527f, 71f, 528f, 76f)
    }

    // a — the bowl, then the stem down its right side.
    stroke {
        moveTo(696f, 162f)
        cubicTo(674f, 128f, 618f, 124f, 592f, 154f)
        cubicTo(570f, 180f, 574f, 226f, 604f, 244f)
        cubicTo(632f, 258f, 678f, 248f, 696f, 228f)
    }
    stroke {
        moveTo(698f, 126f)
        cubicTo(694f, 170f, 692f, 214f, 696f, 254f)
    }

    // n — the stem, then the arch over to the second leg.
    stroke {
        moveTo(744f, 254f)
        cubicTo(741f, 212f, 740f, 168f, 743f, 126f)
    }
    stroke {
        moveTo(743f, 158f)
        cubicTo(762f, 128f, 808f, 120f, 834f, 144f)
        cubicTo(852f, 161f, 854f, 208f, 852f, 254f)
    }

    // s — one movement, the spine reversing twice.
    stroke {
        moveTo(990f, 164f)
        cubicTo(974f, 134f, 938f, 128f, 920f, 144f)
        cubicTo(904f, 158f, 912f, 182f, 938f, 192f)
        cubicTo(964f, 202f, 982f, 210f, 982f, 230f)
        cubicTo(982f, 252f, 944f, 260f, 920f, 242f)
    }

    // The swash under the word. Short, so it arrives fast, and tapered hard at
    // both ends — the flick of the wrist that finishes a signature.
    stroke(nib = Nib.Swash) {
        moveTo(66f, 304f)
        cubicTo(280f, 286f, 660f, 286f, 986f, 300f)
    }

    return strokes
}


/**
 * A stroke, sampled along its centreline, with its outline already built.
 *
 * Everything that could be rebuilt per frame is not. A finished stroke keeps its
 * outline and is drawn straight from it; only the one stroke currently under the
 * nib is rebuilt, and it is rebuilt into a scratch Path that is allocated once
 * and reset. So a frame in the middle of the word touches one stroke's geometry
 * and reads the other twelve — which matters on the one screen where the user is
 * waiting for the app to start, and the first dropped frame is the first thing
 * they ever see of it.
 */
private class MeasuredStroke(path: Path, nib: Nib, index: Int) {
    private val measure: PathMeasure = PathMeasure().apply { setPath(path, false) }
    val length: Float = measure.length

    private val count: Int = maxOf(2, ceil(length / SampleStep).toInt() + 1)
    private val step: Float = length / (count - 1)

    private val xs = FloatArray(count)
    private val ys = FloatArray(count)

    /** Unit normal to the centreline at each sample. */
    private val nx = FloatArray(count)
    private val ny = FloatArray(count)

    /** Half the pen width at each sample. */
    private val hw = FloatArray(count)

    /** The finished stroke, built once. */
    private val full: Path = Path()

    /** Scratch for the stroke currently under the nib. */
    private val partial: Path = Path()

    init {
        for (i in 0 until count) {
            val p = measure.getPosition(i * step)
            xs[i] = p.x
            ys[i] = p.y
        }

        // Normals by central difference. Taking them from the samples rather
        // than from the curve keeps the offset consistent with the polyline we
        // are actually going to fill.
        for (i in 0 until count) {
            val a = if (i == 0) 0 else i - 1
            val b = if (i == count - 1) count - 1 else i + 1
            val dx = xs[b] - xs[a]
            val dy = ys[b] - ys[a]
            val len = hypot(dx, dy)
            if (len > 0.0001f) {
                nx[i] = -dy / len
                ny[i] = dx / len
            }
        }

        // Each stroke sits at a slightly different overall weight, and drifts
        // slowly along its own length. Two adjacent letters at identical
        // pressure look printed; the eye notices the sameness long before it
        // could name it.
        val bias = 1f + 0.055f * sin(index * 2.399f)
        val phase = index * 1.7f
        val taper = min(nib.taper, length * MaxTaperFraction)
        for (i in 0 until count) {
            val travelled = i * step
            // Distance from the nearer end, normalised over the taper, then
            // smootherstepped. The extra degree over the usual smoothstep
            // matters here: smoothstep still meets full pressure at a visible
            // angle, and on a stroke as short as the i it reads as a shoulder
            // rather than as a nib settling.
            val t =
                if (taper <= 0f) 1f
                else (min(travelled, length - travelled) / taper).coerceIn(0f, 1f)
            val eased = t * t * t * (t * (t * 6f - 15f) + 10f)
            val pressure = nib.tip + (1f - nib.tip) * eased
            val u = if (length > 0f) travelled / length else 0f
            val drift = 1f + 0.03f * sin(u * 2.4f + phase)
            hw[i] = PenWidth * nib.weight * bias * pressure * drift * 0.5f
        }

        buildOutline(full, count, hasTip = false)
    }

    /**
     * Fill [into] with the outline of the first [upTo] samples, optionally
     * ending at an extra interpolated tip.
     *
     * The left side is walked forwards and the right side back, so the result
     * is a single closed ring. The round ends are drawn separately as discs:
     * cheaper than arcs, and exactly circular at any taper.
     */
    private fun buildOutline(
        into: Path,
        upTo: Int,
        hasTip: Boolean,
        tipX: Float = 0f,
        tipY: Float = 0f,
        tipNxHw: Float = 0f,
        tipNyHw: Float = 0f
    ) {
        into.reset()
        into.moveTo(xs[0] + nx[0] * hw[0], ys[0] + ny[0] * hw[0])
        for (i in 1 until upTo) {
            into.lineTo(xs[i] + nx[i] * hw[i], ys[i] + ny[i] * hw[i])
        }
        if (hasTip) {
            into.lineTo(tipX + tipNxHw, tipY + tipNyHw)
            into.lineTo(tipX - tipNxHw, tipY - tipNyHw)
        }
        for (i in upTo - 1 downTo 0) {
            into.lineTo(xs[i] - nx[i] * hw[i], ys[i] - ny[i] * hw[i])
        }
        into.close()
    }

    /** Draw this stroke as far as [covered] units of its length have been written. */
    fun draw(scope: DrawScope, covered: Float, color: Color) {
        if (covered <= 0f) return

        if (covered >= length) {
            scope.drawPath(full, color)
            scope.drawCircle(color, hw[0], Offset(xs[0], ys[0]))
            scope.drawCircle(color, hw[count - 1], Offset(xs[count - 1], ys[count - 1]))
            return
        }

        // Samples fully written so far — 0..whole — then an interpolated tip at
        // exactly the pen position. Snapping the tip to the nearest sample would
        // make the nib advance in visible steps on a slow stroke.
        val whole = (covered / step).toInt().coerceIn(0, count - 2)
        val tip = measure.getPosition(covered)
        val frac = ((covered - whole * step) / step).coerceIn(0f, 1f)
        val next = min(whole + 1, count - 1)
        val tipHw = hw[whole] + (hw[next] - hw[whole]) * frac
        val tipNx = nx[whole] + (nx[next] - nx[whole]) * frac
        val tipNy = ny[whole] + (ny[next] - ny[whole]) * frac

        if (whole < 1) {
            // Barely touched down: just the nib.
            scope.drawCircle(color, tipHw, tip)
            return
        }

        buildOutline(partial, whole + 1, true, tip.x, tip.y, tipNx * tipHw, tipNy * tipHw)
        scope.drawPath(partial, color)
        scope.drawCircle(color, hw[0], Offset(xs[0], ys[0]))
        scope.drawCircle(color, tipHw, tip)
    }
}

private class Handwriting(source: List<StrokeSpec>) {
    val strokes: List<MeasuredStroke> =
        source.mapIndexed { i, spec -> MeasuredStroke(spec.path, spec.nib, i) }

    /**
     * The writing timeline, in arc-length units, with the pen lifts folded in.
     * `starts` is where a stroke begins on that timeline; the gap between one
     * stroke's end and the next one's start is the lift.
     */
    private val starts: FloatArray
    val total: Float

    init {
        val inkLength = strokes.sumOf { it.length.toDouble() }.toFloat()
        val lift = if (strokes.size > 1) (inkLength / strokes.size) * PenLiftRatio else 0f

        starts = FloatArray(strokes.size)
        var cursor = 0f
        strokes.forEachIndexed { index, stroke ->
            starts[index] = cursor
            cursor += stroke.length
            if (index != strokes.lastIndex) cursor += lift
        }
        total = cursor
    }

    /** How much of [index] has been written by the time the pen has travelled [travelled]. */
    fun drawn(index: Int, travelled: Float): Float =
        (travelled - starts[index]).coerceIn(0f, strokes[index].length)
}

/**
 * The word "Nebians" in [color], written on as [progress] runs 0 → 1.
 *
 * [progress] is read inside the draw lambda on purpose: a state read there
 * invalidates the draw phase only, so the whole splash animates without a single
 * recomposition. Pass the animated value as a [State], not as a plain `Float`,
 * or every frame will recompose this composable and rebuild nothing useful.
 */
@Composable
fun NebDoodleWordmark(
    progress: State<Float>,
    color: Color,
    modifier: Modifier = Modifier
) {
    val handwriting = remember { Handwriting(wordmarkStrokes()) }

    Canvas(modifier = modifier) {
        val scale = min(size.width / ViewportWidth, size.height / ViewportHeight)
        if (scale <= 0f) return@Canvas

        // Centre the viewport in whatever box we were handed.
        val drawn = Size(ViewportWidth * scale, ViewportHeight * scale)
        val dx = (size.width - drawn.width) / 2f
        val dy = (size.height - drawn.height) / 2f

        val travelled = progress.value.coerceIn(0f, 1f) * handwriting.total

        translate(left = dx, top = dy) {
            scale(scale = scale, pivot = Offset.Zero) {
                handwriting.strokes.forEachIndexed { index, stroke ->
                    stroke.draw(this, handwriting.drawn(index, travelled), color)
                }
            }
        }
    }
}

/**
 * How long the word takes to write, in milliseconds.
 *
 * Exposed so the splash can lay its own timeline out against it, and so
 * MainActivity knows how long to hold its startup side effects back.
 */
const val NEB_DOODLE_WRITE_MS = 2050

/**
 * The wordmark's aspect ratio. Give [NebDoodleWordmark] a box of any other
 * shape and it will letterbox itself inside it rather than distort, but the
 * spare space is then dead weight in the layout.
 */
const val NEB_DOODLE_ASPECT = ViewportWidth / ViewportHeight

/**
 * The writing clock, on its own.
 *
 * [NebDoodleWordmark] only knows how to draw the word at a given progress; it
 * has no opinion about time. This is the other half: an [Animatable] that runs
 * the pen once, honours the system's reduce-motion setting by jumping straight
 * to the finished word, and hands back a [State] so the caller can put it
 * straight into a draw lambda without recomposing.
 *
 * Pulled out of the splash because the splash is no longer the only place the
 * word is written by hand — anything that wants the signature (an onboarding
 * page, an about screen, a share card) needs the timing, not just the shape.
 *
 * @param replayKey change it to write the word again from blank.
 */
@Composable
fun rememberNebDoodleWriting(
    durationMillis: Int = NEB_DOODLE_WRITE_MS,
    startDelayMillis: Long = 0L,
    replayKey: Any? = Unit,
    onFinished: () -> Unit = {}
): State<Float> {
    val writing = remember { Animatable(0f) }
    val reducedMotion = nebAnimationsReduced()
    val finished by rememberUpdatedState(onFinished)

    LaunchedEffect(replayKey, durationMillis, startDelayMillis, reducedMotion) {
        writing.snapTo(0f)
        if (reducedMotion) {
            writing.snapTo(1f)
        } else {
            if (startDelayMillis > 0L) delay(startDelayMillis)
            // Linear on purpose: the rhythm lives in the stroke timeline and
            // the pen lifts baked into it, not in an easing curve over the top.
            writing.animateTo(1f, tween(durationMillis, easing = LinearEasing))
        }
        finished()
    }

    return remember(writing) { writing.asState() }
}

/**
 * The doodle, playing itself — the drop-in form.
 *
 * Sizes itself to [NEB_DOODLE_ASPECT], so give it a width and let the height
 * follow. If you need to drive the progress yourself (to interleave it with
 * other moves, the way the splash does), use [rememberNebDoodleWriting] and
 * [NebDoodleWordmark] directly instead.
 */
@Composable
fun NebDoodleSignature(
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colorScheme.primary,
    durationMillis: Int = NEB_DOODLE_WRITE_MS,
    startDelayMillis: Long = 0L,
    replayKey: Any? = Unit,
    onFinished: () -> Unit = {}
) {
    val progress = rememberNebDoodleWriting(
        durationMillis = durationMillis,
        startDelayMillis = startDelayMillis,
        replayKey = replayKey,
        onFinished = onFinished
    )
    NebDoodleWordmark(
        progress = progress,
        color = color,
        modifier = modifier.aspectRatio(NEB_DOODLE_ASPECT)
    )
}
