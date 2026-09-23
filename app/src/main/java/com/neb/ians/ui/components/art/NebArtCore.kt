package com.neb.ians.ui.components.art

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.runtime.Composable
import androidx.compose.runtime.State
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

// ---------------------------------------------------------------------------
// The drawing kit every journey illustration is built from.
//
// All of the art is drawn rather than bundled: it costs no APK weight, stays
// sharp on any density, follows the palette into dark mode, and animates on the
// render thread because every moving value is read inside a draw lambda instead
// of a composable body.
// ---------------------------------------------------------------------------

/**
 * One slow looping 0..1 clock, shared by every moving part of an illustration.
 * A single transition per illustration keeps the frame callback count at one no
 * matter how many elements ride on it.
 */
@Composable
fun rememberNebArtPhase(durationMillis: Int = 11000): State<Float> {
    val transition = rememberInfiniteTransition(label = "neb_art")
    return transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "neb_art_phase"
    )
}

/** A second clock for parts that should breathe rather than travel. */
@Composable
fun rememberNebBreathPhase(durationMillis: Int = 3200): State<Float> {
    val transition = rememberInfiniteTransition(label = "neb_breath")
    return transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "neb_breath_phase"
    )
}

/** A 0..1 loop offset and wrapped, so elements on one clock never move in lockstep. */
fun wrap(value: Float): Float {
    val v = value % 1f
    return if (v < 0f) v + 1f else v
}

/** A smooth 0..1..0 pulse from a 0..1 phase. */
fun pulse(phase: Float): Float = (sin(phase * 2f * PI.toFloat()) + 1f) / 2f

fun lerp(start: Float, stop: Float, t: Float): Float = start + (stop - start) * t

/** Deterministic pseudo-random in 0..1 from an integer seed — art must not flicker across recompositions. */
fun seeded(seed: Int): Float {
    val x = sin(seed * 12.9898f) * 43758.547f
    return x - kotlin.math.floor(x)
}

// ---------------------------------------------------------------------------
// Shared marks
// ---------------------------------------------------------------------------

/** A soft radial glow. The only light source any illustration gets. */
fun DrawScope.nebGlow(
    center: Offset,
    radius: Float,
    color: Color,
    intensity: Float = 0.24f
) {
    drawCircle(
        brush = Brush.radialGradient(
            colors = listOf(color.copy(alpha = intensity), color.copy(alpha = 0f)),
            center = center,
            radius = radius
        ),
        radius = radius,
        center = center
    )
}

/** Concentric rings that fade outward — a ping, a pin, a signal. */
fun DrawScope.nebRings(
    center: Offset,
    baseRadius: Float,
    phase: Float,
    color: Color,
    count: Int = 3,
    spread: Float = 2.2f,
    strokeWidth: Float = 1.6f
) {
    for (i in 0 until count) {
        val t = wrap(phase + i / count.toFloat())
        val radius = baseRadius * lerp(1f, spread, t)
        val alpha = (1f - t) * 0.5f
        if (alpha <= 0.01f) continue
        drawCircle(
            color = color.copy(alpha = alpha),
            radius = radius,
            center = center,
            style = Stroke(width = strokeWidth)
        )
    }
}

/** Motes of light drifting upward — the journey's ambient texture. */
fun DrawScope.nebMotes(
    phase: Float,
    colors: List<Color>,
    count: Int = 14,
    maxRadius: Float = 3.4f
) {
    for (i in 0 until count) {
        val seedX = seeded(i * 7 + 3)
        val seedR = seeded(i * 11 + 5)
        val drift = wrap(phase * (0.6f + seedR * 0.7f) + seeded(i * 13 + 1))
        val x = size.width * (0.06f + seedX * 0.88f) +
            sin((drift + seedX) * 2f * PI.toFloat()) * size.width * 0.035f
        val y = size.height * (1.05f - drift * 1.12f)
        val fade = kotlin.math.min(drift * 4f, (1f - drift) * 3f).coerceIn(0f, 1f)
        drawCircle(
            color = colors[i % colors.size].copy(alpha = 0.16f + fade * 0.4f),
            radius = maxRadius * (0.35f + seedR * 0.65f),
            center = Offset(x, y)
        )
    }
}

/**
 * The Himalayan ridge that opens the journey. Three overlaid ranges, back to
 * front, each one flatter and lighter than the one in front of it.
 */
fun DrawScope.nebRidge(
    baseline: Float,
    peaks: List<Pair<Float, Float>>,
    color: Color
) {
    val path = Path().apply {
        moveTo(-size.width * 0.05f, baseline)
        peaks.forEach { (x, height) ->
            val px = size.width * x
            val py = baseline - size.height * height
            lineTo(px - size.width * 0.075f, baseline - size.height * height * 0.18f)
            lineTo(px, py)
            lineTo(px + size.width * 0.075f, baseline - size.height * height * 0.18f)
        }
        lineTo(size.width * 1.05f, baseline)
        lineTo(size.width * 1.05f, size.height * 1.05f)
        lineTo(-size.width * 0.05f, size.height * 1.05f)
        close()
    }
    drawPath(path, color)
}

/** A dashed orbit, for anything that should look like it is being tracked. */
fun DrawScope.nebOrbit(
    center: Offset,
    radius: Float,
    color: Color,
    strokeWidth: Float = 1.4f,
    dashed: Boolean = true
) {
    drawCircle(
        color = color,
        radius = radius,
        center = center,
        style = Stroke(
            width = strokeWidth,
            cap = StrokeCap.Round,
            pathEffect = if (dashed) PathEffect.dashPathEffect(floatArrayOf(5f, 9f), 0f) else null
        )
    )
}

/** A point on a circle, in degrees measured from twelve o'clock. */
fun orbitPoint(center: Offset, radius: Float, degrees: Float): Offset {
    val rad = (degrees - 90f) * PI.toFloat() / 180f
    return Offset(center.x + cos(rad) * radius, center.y + sin(rad) * radius)
}

/** A rounded-corner sheet — the base of every card, badge and slip in the art. */
fun DrawScope.nebSheet(
    topLeft: Offset,
    sheetSize: Size,
    fill: Color,
    stroke: Color? = null,
    radius: Float = 12f,
    strokeWidth: Float = 1.4f
) {
    drawRoundRect(
        color = fill,
        topLeft = topLeft,
        size = sheetSize,
        cornerRadius = androidx.compose.ui.geometry.CornerRadius(radius, radius)
    )
    if (stroke != null) {
        drawRoundRect(
            color = stroke,
            topLeft = topLeft,
            size = sheetSize,
            cornerRadius = androidx.compose.ui.geometry.CornerRadius(radius, radius),
            style = Stroke(width = strokeWidth)
        )
    }
}

/** Placeholder text lines inside a drawn card. */
fun DrawScope.nebTextLines(
    start: Offset,
    lineWidths: List<Float>,
    color: Color,
    lineHeight: Float = 7f,
    gap: Float = 8f
) {
    lineWidths.forEachIndexed { index, width ->
        drawRoundRect(
            color = color,
            topLeft = Offset(start.x, start.y + index * (lineHeight + gap)),
            size = Size(width, lineHeight),
            cornerRadius = androidx.compose.ui.geometry.CornerRadius(lineHeight / 2f, lineHeight / 2f)
        )
    }
}
