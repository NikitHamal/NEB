package com.neb.ians.ui.components.art

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebMotion
import kotlin.math.min

// ---------------------------------------------------------------------------
// Where you study — level, subjects, province, institution, face. The second
// half of onboarding, drawn from the same kit as the first.
// ---------------------------------------------------------------------------

/**
 * A staircase of levels with a marker standing on the chosen one. The steps above
 * stay drawn, because the point of a level is that there is somewhere further up.
 */
@Composable
fun NebAscentArt(
    stepIndex: Int,
    stepCount: Int,
    modifier: Modifier = Modifier,
    height: Dp = 150.dp
) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(2400)
    val visible = stepCount.coerceIn(1, 6)
    val marker by animateFloatAsState(
        targetValue = if (stepCount <= 1) 0f else {
            (stepIndex.toFloat() / (stepCount - 1) * (visible - 1)).coerceIn(0f, (visible - 1).toFloat())
        },
        animationSpec = tween(NebMotion.Emphasized, easing = NebMotion.Decelerate),
        label = "neb_ascent"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val stepW = w * 0.74f / visible
            val stepBase = h * 0.86f
            val rise = h * 0.11f
            val left = (w - stepW * visible) / 2f

            for (i in 0 until visible) {
                val topY = stepBase - rise * (i + 1)
                val active = kotlin.math.abs(marker - i) < 0.5f
                drawRoundRect(
                    color = if (active) palette.sapphire else palette.artFaint,
                    topLeft = Offset(left + i * stepW, topY),
                    size = Size(stepW - 3f, stepBase - topY),
                    cornerRadius = CornerRadius(5f, 5f)
                )
                if (!active) {
                    drawRoundRect(
                        color = palette.artSoft,
                        topLeft = Offset(left + i * stepW, topY),
                        size = Size(stepW - 3f, stepBase - topY),
                        cornerRadius = CornerRadius(5f, 5f),
                        style = Stroke(width = 1.1f)
                    )
                }
            }

            val mx = left + stepW * (marker + 0.5f) - 1.5f
            val my = stepBase - rise * (marker + 1) - h * 0.075f
            nebGlow(Offset(mx, my), h * 0.20f, palette.sapphire, 0.22f)
            val flagPole = h * 0.13f
            drawRoundRect(
                color = palette.artInk,
                topLeft = Offset(mx - 1.2f, my - flagPole * lerp(0.96f, 1f, breath)),
                size = Size(2.4f, flagPole),
                cornerRadius = CornerRadius(1.2f, 1.2f)
            )
            val flag = Path().apply {
                val top = my - flagPole
                moveTo(mx + 1.2f, top)
                lineTo(mx + w * 0.055f, top + h * 0.028f)
                lineTo(mx + 1.2f, top + h * 0.056f)
                close()
            }
            drawPath(flag, palette.sapphire)
            drawCircle(color = palette.artInk, radius = 3.2f, center = Offset(mx, my))
        }
    }
}

/**
 * Subjects in orbit. Each chosen subject claims a node and joins the ring; an
 * empty selection leaves the orbit hairline and waiting.
 */
@Composable
fun NebOrbitsArt(
    selectedCount: Int,
    modifier: Modifier = Modifier,
    nodeCount: Int = 8,
    height: Dp = 150.dp
) {
    val palette = LocalNebAuthPalette.current
    val phase by rememberNebArtPhase(18000)
    val breath by rememberNebBreathPhase(2600)
    val filled by animateFloatAsState(
        targetValue = selectedCount.coerceIn(0, nodeCount).toFloat(),
        animationSpec = tween(NebMotion.Emphasized, easing = NebMotion.Decelerate),
        label = "neb_orbits"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val center = Offset(size.width / 2f, size.height / 2f)
            val r = min(size.width, size.height) * 0.36f

            nebGlow(center, r * 1.7f, palette.sapphire, 0.14f)
            nebOrbit(center, r, palette.artSoft, strokeWidth = 1.2f)
            if (filled > 0.01f) {
                drawArc(
                    color = palette.sapphire.copy(alpha = 0.55f),
                    startAngle = -90f + phase * 360f,
                    sweepAngle = 360f * (filled / nodeCount),
                    useCenter = false,
                    topLeft = Offset(center.x - r, center.y - r),
                    size = Size(r * 2f, r * 2f),
                    style = Stroke(width = 2.4f, cap = StrokeCap.Round)
                )
            }

            for (i in 0 until nodeCount) {
                val angle = i * (360f / nodeCount) + phase * 360f
                val p = orbitPoint(center, r, angle)
                val active = i < filled
                val color = palette.sapphire
                if (active) {
                    drawCircle(color = color.copy(alpha = 0.22f), radius = 9f, center = p)
                    drawCircle(color = color, radius = 4.6f * lerp(0.94f, 1.06f, breath), center = p)
                } else {
                    drawCircle(color = palette.page, radius = 4.2f, center = p)
                    drawCircle(
                        color = palette.artMid,
                        radius = 4.2f,
                        center = p,
                        style = Stroke(width = 1.2f)
                    )
                }
            }

            drawCircle(color = palette.sapphireSoft, radius = r * 0.34f, center = center)
            drawCircle(
                color = palette.sapphire,
                radius = r * 0.34f,
                center = center,
                style = Stroke(width = 1.6f)
            )
            val book = Path().apply {
                val bw = r * 0.19f
                val bh = r * 0.14f
                moveTo(center.x - bw, center.y - bh * 0.5f)
                lineTo(center.x, center.y - bh)
                lineTo(center.x + bw, center.y - bh * 0.5f)
                lineTo(center.x + bw, center.y + bh)
                lineTo(center.x, center.y + bh * 0.55f)
                lineTo(center.x - bw, center.y + bh)
                close()
            }
            drawPath(book, palette.sapphire)
        }
    }
}

/**
 * A pin dropping into a province. The seven blocks stand for Nepal's seven
 * provinces without pretending to be a map, and the chosen one rises to meet it.
 */
@Composable
fun NebProvinceArt(
    provinceIndex: Int,
    modifier: Modifier = Modifier,
    provinceCount: Int = 7,
    height: Dp = 150.dp
) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(2600)
    val selected by animateFloatAsState(
        targetValue = provinceIndex.coerceAtLeast(0).toFloat(),
        animationSpec = tween(NebMotion.Emphasized, easing = NebMotion.Decelerate),
        label = "neb_province"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val barW = w * 0.80f / provinceCount
            val left = (w - barW * provinceCount) / 2f
            val baseline = h * 0.82f

            for (i in 0 until provinceCount) {
                val strength = (1f - kotlin.math.abs(selected - i)).coerceIn(0f, 1f)
                val tallness = 0.22f + seeded(i * 3 + 1) * 0.16f
                val barH = h * tallness * lerp(1f, 1.22f, strength)
                val x = left + i * barW
                drawRoundRect(
                    color = if (strength > 0.5f) palette.sapphire else palette.artFaint,
                    topLeft = Offset(x + 2f, baseline - barH),
                    size = Size(barW - 4f, barH),
                    cornerRadius = CornerRadius(6f, 6f)
                )
                if (strength <= 0.5f) {
                    drawRoundRect(
                        color = palette.artSoft,
                        topLeft = Offset(x + 2f, baseline - barH),
                        size = Size(barW - 4f, barH),
                        cornerRadius = CornerRadius(6f, 6f),
                        style = Stroke(width = 1.1f)
                    )
                }
            }

            val px = left + barW * (selected + 0.5f)
            val selectedH = h * (0.22f + seeded(selected.toInt() * 3 + 1) * 0.16f) * 1.22f
            val pinTip = baseline - selectedH - h * 0.03f
            val pinR = h * 0.062f
            val pinCenter = Offset(px, pinTip - pinR * 1.5f - lerp(0f, h * 0.012f, breath))
            val pin = Path().apply {
                moveTo(px, pinTip)
                cubicTo(
                    px - pinR * 1.05f, pinCenter.y + pinR * 0.7f,
                    px - pinR * 1.1f, pinCenter.y - pinR * 0.6f,
                    px, pinCenter.y - pinR
                )
                cubicTo(
                    px + pinR * 1.1f, pinCenter.y - pinR * 0.6f,
                    px + pinR * 1.05f, pinCenter.y + pinR * 0.7f,
                    px, pinTip
                )
                close()
            }
            drawPath(pin, palette.sapphire)
            drawCircle(color = palette.page, radius = pinR * 0.38f, center = pinCenter)

            drawRoundRect(
                color = palette.artSoft,
                topLeft = Offset(left, baseline),
                size = Size(barW * provinceCount, 2.2f),
                cornerRadius = CornerRadius(1.1f, 1.1f)
            )
        }
    }
}

/**
 * A school under prayer flags: a pagoda roofline over a body of windows, lit when
 * an institution has been named. The flags are cut from the art ramp rather than
 * coloured, and they are the only thing that moves.
 */
@Composable
fun NebCampusArt(
    named: Boolean,
    modifier: Modifier = Modifier,
    height: Dp = 160.dp
) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(3000)
    val lit by animateFloatAsState(
        targetValue = if (named) 1f else 0f,
        animationSpec = tween(NebMotion.Slow, easing = NebMotion.Decelerate),
        label = "neb_campus"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val bodyW = min(w * 0.46f, h * 1.0f)
            val bodyH = h * 0.38f
            val left = (w - bodyW) / 2f
            val bodyTop = h * 0.50f

            for (tier in 0 until 2) {
                val spread = bodyW * (1.22f - tier * 0.26f)
                val y = bodyTop - bodyH * (0.10f + tier * 0.22f)
                val roof = Path().apply {
                    moveTo(w / 2f - spread / 2f, y)
                    cubicTo(
                        w / 2f - spread * 0.28f, y - bodyH * 0.20f,
                        w / 2f + spread * 0.28f, y - bodyH * 0.20f,
                        w / 2f + spread / 2f, y
                    )
                    lineTo(w / 2f + spread * 0.34f, y + bodyH * 0.06f)
                    lineTo(w / 2f - spread * 0.34f, y + bodyH * 0.06f)
                    close()
                }
                drawPath(roof, if (tier == 0) palette.artLine else palette.artMid)
            }

            nebSheet(
                topLeft = Offset(left, bodyTop),
                sheetSize = Size(bodyW, bodyH),
                fill = palette.card,
                stroke = palette.hairlineStrong,
                radius = 8f
            )
            val winCols = 3
            val winRows = 2
            val winW = bodyW * 0.18f
            val winH = bodyH * 0.22f
            val gridLeft = left + (bodyW - (winCols * winW + (winCols - 1) * bodyW * 0.08f)) / 2f
            for (row in 0 until winRows) {
                for (col in 0 until winCols) {
                    val index = row * winCols + col
                    val alpha = if (index < lit * winCols * winRows) 1f else 0.25f
                    drawRoundRect(
                        color = palette.sapphire.copy(alpha = alpha * lerp(0.82f, 1f, breath)),
                        topLeft = Offset(
                            gridLeft + col * (winW + bodyW * 0.08f),
                            bodyTop + bodyH * 0.16f + row * (winH + bodyH * 0.16f)
                        ),
                        size = Size(winW, winH),
                        cornerRadius = CornerRadius(3f, 3f)
                    )
                }
            }
            drawRoundRect(
                color = palette.sapphire,
                topLeft = Offset(w / 2f - bodyW * 0.09f, bodyTop + bodyH * 0.62f),
                size = Size(bodyW * 0.18f, bodyH * 0.38f),
                cornerRadius = CornerRadius(4f, 4f)
            )

            val flagY = h * 0.16f
            val tones = palette.artTones
            for (i in 0 until 7) {
                val t = i / 6f
                val x = w * lerp(0.10f, 0.90f, t)
                val sag = kotlin.math.sin(t * kotlin.math.PI.toFloat()) * h * 0.06f
                val sway = kotlin.math.sin((t + breath) * 3f) * h * 0.012f
                drawRoundRect(
                    color = tones[1 + i % 3],
                    topLeft = Offset(x - 4f, flagY + sag + sway),
                    size = Size(8f, h * 0.055f),
                    cornerRadius = CornerRadius(1.5f, 1.5f)
                )
            }
            val line = Path().apply {
                moveTo(w * 0.06f, flagY)
                cubicTo(w * 0.35f, flagY + h * 0.09f, w * 0.65f, flagY + h * 0.09f, w * 0.94f, flagY)
            }
            drawPath(line, palette.artMid, style = Stroke(width = 1.2f))

            drawRoundRect(
                color = palette.artSoft,
                topLeft = Offset(w * 0.14f, bodyTop + bodyH),
                size = Size(w * 0.72f, 2.4f),
                cornerRadius = CornerRadius(1.2f, 1.2f)
            )
        }
    }
}

/**
 * The frame a face goes in. An aperture of neutral blades around an empty ring
 * while there is no photo; once there is one, the blades retract and the ring
 * closes in sapphire.
 */
@Composable
fun NebApertureArt(
    hasPhoto: Boolean,
    modifier: Modifier = Modifier,
    height: Dp = 150.dp
) {
    val palette = LocalNebAuthPalette.current
    val phase by rememberNebArtPhase(20000)
    val breath by rememberNebBreathPhase(2800)
    val closed by animateFloatAsState(
        targetValue = if (hasPhoto) 1f else 0f,
        animationSpec = tween(NebMotion.Slow, easing = NebMotion.Decelerate),
        label = "neb_aperture"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val center = Offset(size.width / 2f, size.height / 2f)
            val r = min(size.width, size.height) * 0.30f

            nebGlow(center, r * 2.3f, palette.sapphire, if (hasPhoto) 0.18f else 0.10f)

            val tones = palette.artTones
            for (i in 0 until 6) {
                val angle = i * 60f + phase * 360f
                val dist = r * lerp(1.62f, 1.18f, closed)
                val p = orbitPoint(center, dist, angle)
                val blade = Path().apply {
                    moveTo(p.x, p.y)
                    val a = orbitPoint(center, dist * 0.82f, angle - 14f)
                    val b = orbitPoint(center, dist * 0.82f, angle + 14f)
                    lineTo(a.x, a.y)
                    lineTo(b.x, b.y)
                    close()
                }
                drawPath(blade, tones[1 + i % 3].copy(alpha = lerp(0.9f, 0.25f, closed)))
            }

            drawCircle(
                color = if (hasPhoto) palette.sapphire else palette.artMid,
                radius = r * lerp(1f, 1.03f, breath),
                center = center,
                style = Stroke(width = r * 0.10f)
            )
            drawCircle(color = palette.artFaint, radius = r * 0.86f, center = center)

            val headR = r * 0.26f
            val headCenter = Offset(center.x, center.y - r * 0.20f)
            val figureColor = if (hasPhoto) palette.sapphire else palette.artMid
            drawCircle(color = figureColor.copy(alpha = 0.85f), radius = headR, center = headCenter)
            val shoulders = Path().apply {
                moveTo(center.x - r * 0.46f, center.y + r * 0.58f)
                cubicTo(
                    center.x - r * 0.42f, center.y + r * 0.08f,
                    center.x + r * 0.42f, center.y + r * 0.08f,
                    center.x + r * 0.46f, center.y + r * 0.58f
                )
                close()
            }
            drawPath(shoulders, figureColor.copy(alpha = 0.85f))
        }
    }
}
