package com.neb.ians.ui.components.art

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebMotion
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.sin

// ---------------------------------------------------------------------------
// The three set pieces of the journey: the horizon the user arrives at, the
// code in flight, and the moment it all lands.
// ---------------------------------------------------------------------------

/**
 * Sunrise over the range. Nepal's own horizon, drawn in the palette's landscape
 * accents, with motes of light rising off the valley floor.
 */
@Composable
fun NebHorizonArt(
    modifier: Modifier = Modifier,
    height: Dp = 200.dp
) {
    val palette = LocalNebAuthPalette.current
    val phase by rememberNebArtPhase(14000)
    val breath by rememberNebBreathPhase(4200)

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxWidth().height(height)) {
            val w = size.width
            val h = size.height
            val sunCenter = Offset(w * 0.5f, h * 0.60f)
            val sunRadius = min(w, h) * 0.20f * lerp(0.97f, 1.04f, breath)

            nebGlow(sunCenter, sunRadius * 3.2f, palette.marigold, 0.20f)
            drawCircle(
                brush = Brush.verticalGradient(
                    colors = listOf(palette.marigold, palette.rhododendron),
                    startY = sunCenter.y - sunRadius,
                    endY = sunCenter.y + sunRadius
                ),
                radius = sunRadius,
                center = sunCenter
            )

            for (i in 0 until 5) {
                val t = wrap(phase * 0.5f + i * 0.2f)
                val radius = sunRadius * lerp(1.15f, 2.6f, t)
                drawCircle(
                    color = palette.marigold.copy(alpha = (1f - t) * 0.22f),
                    radius = radius,
                    center = sunCenter,
                    style = Stroke(width = 1.2f)
                )
            }

            nebRidge(
                baseline = h * 0.78f,
                peaks = listOf(0.14f to 0.30f, 0.38f to 0.44f, 0.66f to 0.34f, 0.90f to 0.26f),
                color = palette.dusk.copy(alpha = if (palette.isDark) 0.34f else 0.16f)
            )
            nebRidge(
                baseline = h * 0.86f,
                peaks = listOf(0.06f to 0.22f, 0.30f to 0.34f, 0.55f to 0.26f, 0.80f to 0.32f),
                color = palette.sapphire.copy(alpha = if (palette.isDark) 0.40f else 0.22f)
            )
            nebRidge(
                baseline = h * 0.94f,
                peaks = listOf(0.20f to 0.16f, 0.48f to 0.22f, 0.76f to 0.18f),
                color = palette.everest.copy(alpha = if (palette.isDark) 0.46f else 0.28f)
            )

            nebMotes(
                phase = phase,
                colors = listOf(palette.marigold, palette.everest, palette.sapphire, palette.rhododendron),
                count = 16
            )
        }
    }
}

/**
 * A six-digit code in flight. The slip rises out of the envelope and its cells
 * fill as the user types, so the illustration is the progress indicator.
 */
@Composable
fun NebCodeInFlightArt(
    filledCount: Int,
    modifier: Modifier = Modifier,
    total: Int = 6,
    height: Dp = 160.dp
) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(2600)
    val phase by rememberNebArtPhase(9000)
    val fill by animateFloatAsState(
        targetValue = (filledCount.toFloat() / total).coerceIn(0f, 1f),
        animationSpec = tween(NebMotion.Standard, easing = NebMotion.Decelerate),
        label = "neb_code_fill"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxWidth().height(height)) {
            val w = size.width
            val h = size.height
            val envW = min(w * 0.46f, h * 1.25f)
            val envH = envW * 0.66f
            val envLeft = (w - envW) / 2f
            val envTop = h * 0.44f

            nebGlow(Offset(w / 2f, h * 0.46f), envW * 1.5f, palette.sapphire, 0.16f)

            val lift = lerp(0f, 1f, breath) * 6f
            val slipW = envW * 0.78f
            val slipH = envH * 0.72f
            val slipLeft = envLeft + (envW - slipW) / 2f
            val slipTop = envTop - slipH * 0.62f - lift

            nebSheet(
                topLeft = Offset(slipLeft, slipTop),
                sheetSize = Size(slipW, slipH),
                fill = palette.card,
                stroke = palette.hairlineStrong,
                radius = 10f
            )

            val cellCount = total
            val cellGap = slipW * 0.035f
            val cellW = (slipW * 0.82f - cellGap * (cellCount - 1)) / cellCount
            val cellH = slipH * 0.44f
            val cellsLeft = slipLeft + slipW * 0.09f
            val cellsTop = slipTop + (slipH - cellH) / 2f
            for (i in 0 until cellCount) {
                val isFilled = i < (fill * cellCount)
                val x = cellsLeft + i * (cellW + cellGap)
                drawRoundRect(
                    color = if (isFilled) palette.sapphire else palette.field,
                    topLeft = Offset(x, cellsTop),
                    size = Size(cellW, cellH),
                    cornerRadius = CornerRadius(4f, 4f)
                )
                if (!isFilled) {
                    drawRoundRect(
                        color = palette.hairline,
                        topLeft = Offset(x, cellsTop),
                        size = Size(cellW, cellH),
                        cornerRadius = CornerRadius(4f, 4f),
                        style = Stroke(width = 1.2f)
                    )
                }
            }

            nebSheet(
                topLeft = Offset(envLeft, envTop),
                sheetSize = Size(envW, envH),
                fill = palette.field,
                stroke = palette.hairlineStrong,
                radius = 12f
            )
            val flap = Path().apply {
                moveTo(envLeft, envTop + envH * 0.06f)
                lineTo(envLeft + envW / 2f, envTop + envH * 0.52f)
                lineTo(envLeft + envW, envTop + envH * 0.06f)
            }
            drawPath(flap, palette.hairlineStrong, style = Stroke(width = 1.6f, cap = StrokeCap.Round))

            nebRings(
                center = Offset(w / 2f, envTop + envH * 0.55f),
                baseRadius = envW * 0.6f,
                phase = phase,
                color = palette.sapphire,
                count = 3,
                spread = 1.9f
            )
        }
    }
}

/**
 * The landing. A ring closes, a tick draws itself, and the five accents scatter
 * outward once — used for a verified code and a finished profile alike.
 */
@Composable
fun NebArrivalArt(
    modifier: Modifier = Modifier,
    height: Dp = 180.dp
) {
    val palette = LocalNebAuthPalette.current
    val phase by rememberNebArtPhase(6000)
    val breath by rememberNebBreathPhase(2200)
    val reveal by animateFloatAsState(
        targetValue = 1f,
        animationSpec = tween(NebMotion.Slow, easing = NebMotion.Decelerate),
        label = "neb_arrival"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxWidth().height(height)) {
            val center = Offset(size.width / 2f, size.height * 0.5f)
            val r = min(size.width, size.height) * 0.22f

            nebGlow(center, r * 3.4f, palette.everest, 0.18f)

            val accents = palette.accents
            for (i in 0 until 14) {
                val angle = i * (360f / 14f) + phase * 40f
                val seed = seeded(i * 5 + 2)
                val distance = r * lerp(1.6f, 2.9f, seed) * reveal
                val p = orbitPoint(center, distance, angle)
                val dotR = lerp(1.6f, 4.2f, seeded(i * 9 + 4))
                drawCircle(
                    color = accents[i % accents.size].copy(alpha = 0.22f + seed * 0.45f),
                    radius = dotR * lerp(0.9f, 1.15f, breath),
                    center = p
                )
            }

            nebOrbit(center, r * 1.55f, palette.hairlineStrong, strokeWidth = 1.2f)

            drawCircle(color = palette.successSoft, radius = r * 1.18f, center = center)
            drawArc(
                color = palette.success,
                startAngle = -90f,
                sweepAngle = 360f * reveal,
                useCenter = false,
                topLeft = Offset(center.x - r, center.y - r),
                size = Size(r * 2f, r * 2f),
                style = Stroke(width = r * 0.14f, cap = StrokeCap.Round)
            )

            val tick = Path().apply {
                moveTo(center.x - r * 0.42f, center.y + r * 0.03f)
                lineTo(center.x - r * 0.08f, center.y + r * 0.36f)
                lineTo(center.x + r * 0.46f, center.y - r * 0.32f)
            }
            drawPath(
                path = tick,
                color = palette.success,
                style = Stroke(width = r * 0.16f, cap = StrokeCap.Round)
            )
        }
    }
}

/**
 * The compact mark that sits above a sign-in form: an open book whose pages lift,
 * with the community orbiting it. Small enough to share a screen with two fields.
 */
@Composable
fun NebOpenBookMark(
    modifier: Modifier = Modifier,
    markSize: Dp = 84.dp
) {
    val palette = LocalNebAuthPalette.current
    val phase by rememberNebArtPhase(10000)
    val breath by rememberNebBreathPhase(3000)

    Box(modifier = modifier.height(markSize)) {
        Canvas(modifier = Modifier.height(markSize).fillMaxWidth()) {
            val w = this.size.width
            val h = this.size.height
            val center = Offset(w / 2f, h * 0.54f)
            val s = min(w, h)

            nebGlow(center, s * 0.62f, palette.sapphire, 0.18f)

            for (i in 0 until 3) {
                val angle = phase * 360f + i * 120f
                val p = orbitPoint(center, s * 0.44f, angle)
                drawCircle(
                    color = palette.accents[(i + 1) % palette.accents.size].copy(alpha = 0.7f),
                    radius = s * 0.035f,
                    center = p
                )
            }
            nebOrbit(center, s * 0.44f, palette.hairline, strokeWidth = 1f)

            val lift = lerp(0f, s * 0.035f, breath)
            val pageW = s * 0.28f
            val pageH = s * 0.22f
            listOf(-1f, 1f).forEach { side ->
                val path = Path().apply {
                    moveTo(center.x, center.y - lift)
                    cubicTo(
                        center.x + side * pageW * 0.35f, center.y - pageH * 0.55f - lift,
                        center.x + side * pageW * 0.75f, center.y - pageH * 0.62f - lift,
                        center.x + side * pageW, center.y - pageH * 0.34f - lift
                    )
                    lineTo(center.x + side * pageW, center.y + pageH * 0.42f)
                    cubicTo(
                        center.x + side * pageW * 0.7f, center.y + pageH * 0.2f,
                        center.x + side * pageW * 0.3f, center.y + pageH * 0.16f,
                        center.x, center.y + pageH * 0.3f
                    )
                    close()
                }
                drawPath(path, palette.sapphire.copy(alpha = if (side < 0f) 0.9f else 0.65f))
            }
        }
    }
}

/** A single accent spark, used to punctuate a headline. */
@Composable
fun NebSparkMark(modifier: Modifier = Modifier, markSize: Dp = 18.dp) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(1800)
    Canvas(modifier = modifier.height(markSize)) {
        val c = Offset(this.size.width / 2f, this.size.height / 2f)
        val r = min(this.size.width, this.size.height) / 2f * lerp(0.82f, 1f, breath)
        rotate(degrees = lerp(0f, 18f, breath), pivot = c) {
            val path = Path()
            for (i in 0 until 8) {
                val angle = i * 45f * PI.toFloat() / 180f
                val radius = if (i % 2 == 0) r else r * 0.34f
                val x = c.x + cos(angle) * radius
                val y = c.y + sin(angle) * radius
                if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
            }
            path.close()
            drawPath(path, palette.marigold)
        }
    }
}
