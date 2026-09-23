package com.neb.ians.ui.components.art

import androidx.compose.animation.core.animateFloatAsState
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlin.math.min

// ---------------------------------------------------------------------------
// Who you are — the illustrations for the four steps that establish identity.
// Each one takes the step's own value, so the art answers the question with the
// user instead of decorating the screen beside them.
// ---------------------------------------------------------------------------

/**
 * Four paths leaving one trailhead. The selected role's path is drawn in accent
 * and its summit lights up; the others stay neutral hairlines, still visible,
 * still open.
 */
@Composable
fun NebPathsArt(
    selectedIndex: Int,
    modifier: Modifier = Modifier,
    pathCount: Int = 4,
    height: Dp = 150.dp
) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(2800)
    val selected by animateFloatAsState(
        targetValue = selectedIndex.coerceAtLeast(0).toFloat(),
        animationSpec = nebSpatialSpec(),
        label = "neb_paths_selected"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val origin = Offset(w * 0.5f, h * 0.94f)

            for (i in 0 until pathCount) {
                val t = if (pathCount == 1) 0.5f else i / (pathCount - 1).toFloat()
                val end = Offset(w * lerp(0.13f, 0.87f, t), h * lerp(0.44f, 0.16f, kotlin.math.abs(0.5f - t) * 2f))
                val active = kotlin.math.abs(selected - i) < 0.5f
                val strength = (1f - kotlin.math.abs(selected - i)).coerceIn(0f, 1f)
                val color = palette.accent

                val path = Path().apply {
                    moveTo(origin.x, origin.y)
                    cubicTo(
                        origin.x + (end.x - origin.x) * 0.15f, origin.y - h * 0.32f,
                        origin.x + (end.x - origin.x) * 0.72f, end.y + h * 0.26f,
                        end.x, end.y
                    )
                }
                drawPath(
                    path = path,
                    color = if (active) color else palette.artSoft,
                    style = Stroke(width = lerp(1.3f, 3.2f, strength), cap = StrokeCap.Round)
                )
                if (strength > 0.5f) {
                }
                drawCircle(
                    color = if (active) color else palette.artMid,
                    radius = lerp(3.2f, 6.4f, strength) * lerp(0.94f, 1.06f, breath),
                    center = end
                )
            }

            drawCircle(color = palette.page, radius = 9f, center = origin)
            drawCircle(
                color = palette.accent,
                radius = 7f,
                center = origin,
                style = Stroke(width = 2.4f)
            )
        }
    }
}

/**
 * A name taking shape on a card: an initial badge, a written line that grows with
 * the text, and a caret that keeps blinking until the line is full.
 */
@Composable
fun NebNameplateArt(
    initial: Char?,
    progress: Float,
    modifier: Modifier = Modifier,
    height: Dp = 140.dp
) {
    val palette = LocalNebAuthPalette.current
    val caret by rememberNebBreathPhase(900)
    val grown by animateFloatAsState(
        targetValue = progress.coerceIn(0f, 1f),
        animationSpec = nebSpatialSpec(),
        label = "neb_nameplate"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val cardW = min(w * 0.72f, h * 2.1f)
            val cardH = cardW * 0.44f
            val left = (w - cardW) / 2f
            val top = (h - cardH) / 2f

            nebSheet(
                topLeft = Offset(left, top),
                sheetSize = Size(cardW, cardH),
                fill = palette.card,
                stroke = palette.hairlineStrong,
                radius = 14f
            )

            val badgeR = cardH * 0.24f
            val badgeCenter = Offset(left + cardH * 0.36f, top + cardH * 0.42f)
            drawCircle(color = palette.accentSoft, radius = badgeR, center = badgeCenter)
            drawCircle(
                color = palette.accent.copy(alpha = 0.55f),
                radius = badgeR,
                center = badgeCenter,
                style = Stroke(width = 1.4f)
            )
            if (initial != null) {
                drawRoundRect(
                    color = palette.accent,
                    topLeft = Offset(badgeCenter.x - badgeR * 0.30f, badgeCenter.y - badgeR * 0.40f),
                    size = Size(badgeR * 0.60f, badgeR * 0.80f),
                    cornerRadius = CornerRadius(badgeR * 0.18f, badgeR * 0.18f)
                )
            }

            val lineLeft = badgeCenter.x + badgeR + cardW * 0.06f
            val lineMax = left + cardW - cardW * 0.10f - lineLeft
            val lineY = top + cardH * 0.40f
            drawRoundRect(
                color = palette.field,
                topLeft = Offset(lineLeft, lineY - 4f),
                size = Size(lineMax, 8f),
                cornerRadius = CornerRadius(4f, 4f)
            )
            if (grown > 0.01f) {
                drawRoundRect(
                    color = palette.ink.copy(alpha = 0.78f),
                    topLeft = Offset(lineLeft, lineY - 4f),
                    size = Size(lineMax * grown, 8f),
                    cornerRadius = CornerRadius(4f, 4f)
                )
            }
            if (grown < 0.995f) {
                drawRoundRect(
                    color = palette.accent.copy(alpha = lerp(0.15f, 1f, caret)),
                    topLeft = Offset(lineLeft + lineMax * grown + 3f, lineY - 9f),
                    size = Size(2.4f, 18f),
                    cornerRadius = CornerRadius(1.2f, 1.2f)
                )
            }
            nebTextLines(
                start = Offset(lineLeft, top + cardH * 0.64f),
                lineWidths = listOf(lineMax * 0.52f),
                color = palette.hairline,
                lineHeight = 6f
            )
        }
    }
}

/** The state a handle can be in, which is also the state its ring is drawn in. */
enum class NebHandleState { Idle, Checking, Available, Taken }

/**
 * An @ drawn as an arc inside a ring. The ring is the verdict: hairline while
 * idle, accent sweeping while the server is asked, then success or danger.
 */
@Composable
fun NebHandleArt(
    state: NebHandleState,
    modifier: Modifier = Modifier,
    height: Dp = 140.dp
) {
    val palette = LocalNebAuthPalette.current
    val spin by rememberNebArtPhase(1400)
    val breath by rememberNebBreathPhase(2400)
    val target: Color = when (state) {
        NebHandleState.Idle -> palette.hairlineStrong
        NebHandleState.Checking -> palette.accent
        NebHandleState.Available -> palette.success
        NebHandleState.Taken -> palette.danger
    }

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val center = Offset(size.width / 2f, size.height / 2f)
            val r = min(size.width, size.height) * 0.26f


            if (state == NebHandleState.Checking) {
                drawArc(
                    color = target,
                    startAngle = spin * 360f,
                    sweepAngle = 96f,
                    useCenter = false,
                    topLeft = Offset(center.x - r, center.y - r),
                    size = Size(r * 2f, r * 2f),
                    style = Stroke(width = r * 0.13f, cap = StrokeCap.Round)
                )
                nebOrbit(center, r, palette.hairline, strokeWidth = r * 0.13f, dashed = false)
            } else {
                drawCircle(
                    color = target.copy(alpha = if (state == NebHandleState.Idle) 0.6f else 1f),
                    radius = r * lerp(0.99f, 1.02f, breath),
                    center = center,
                    style = Stroke(width = r * 0.13f)
                )
            }

            val inner = r * 0.42f
            drawCircle(
                color = palette.ink.copy(alpha = 0.82f),
                radius = inner,
                center = center,
                style = Stroke(width = r * 0.11f)
            )
            val tail = Path().apply {
                moveTo(center.x + inner, center.y - inner * 0.55f)
                lineTo(center.x + inner, center.y + inner * 0.45f)
                cubicTo(
                    center.x + inner, center.y + inner * 1.25f,
                    center.x + inner * 1.9f, center.y + inner * 1.15f,
                    center.x + inner * 2.0f, center.y + inner * 0.55f
                )
            }
            drawPath(
                path = tail,
                color = palette.ink.copy(alpha = 0.82f),
                style = Stroke(width = r * 0.11f, cap = StrokeCap.Round)
            )

        }
    }
}

/**
 * A calendar leaf with one day lit. The ring of dots around it is a year turning,
 * which is the only honest way to draw a birthday.
 */
@Composable
fun NebCalendarArt(
    dayOfMonth: Int?,
    modifier: Modifier = Modifier,
    height: Dp = 150.dp
) {
    val palette = LocalNebAuthPalette.current
    val chosen by animateFloatAsState(
        targetValue = if (dayOfMonth != null) 1f else 0f,
        animationSpec = nebSpatialSpec(),
        label = "neb_calendar"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val center = Offset(w / 2f, h / 2f)
            val sheetW = min(w * 0.42f, h * 0.86f)
            val sheetH = sheetW * 1.06f
            val left = center.x - sheetW / 2f
            val top = center.y - sheetH / 2f

            nebOrbit(center, min(w, h) * 0.45f, palette.hairline, strokeWidth = 1f)

            nebSheet(
                topLeft = Offset(left, top),
                sheetSize = Size(sheetW, sheetH),
                fill = palette.card,
                stroke = palette.hairlineStrong,
                radius = 12f
            )
            drawRoundRect(
                color = palette.accent,
                topLeft = Offset(left, top),
                size = Size(sheetW, sheetH * 0.20f),
                cornerRadius = CornerRadius(12f, 12f)
            )
            drawRect(
                color = palette.accent,
                topLeft = Offset(left, top + sheetH * 0.12f),
                size = Size(sheetW, sheetH * 0.08f)
            )
            listOf(0.3f, 0.7f).forEach { fx ->
                drawRoundRect(
                    color = palette.field,
                    topLeft = Offset(left + sheetW * fx - 2f, top - sheetH * 0.07f),
                    size = Size(4.5f, sheetH * 0.12f),
                    cornerRadius = CornerRadius(2.25f, 2.25f)
                )
            }

            val cols = 4
            val rows = 3
            val cellW = sheetW * 0.17f
            val cellH = sheetH * 0.15f
            val gridLeft = left + (sheetW - (cols * cellW + (cols - 1) * sheetW * 0.045f)) / 2f
            val gridTop = top + sheetH * 0.30f
            val litIndex = ((dayOfMonth ?: 1) - 1).mod(cols * rows)
            for (row in 0 until rows) {
                for (col in 0 until cols) {
                    val index = row * cols + col
                    val x = gridLeft + col * (cellW + sheetW * 0.045f)
                    val y = gridTop + row * (cellH + sheetH * 0.045f)
                    val lit = index == litIndex
                    drawRoundRect(
                        color = if (lit) palette.accent.copy(alpha = chosen) else palette.field,
                        topLeft = Offset(x, y),
                        size = Size(cellW, cellH),
                        cornerRadius = CornerRadius(4f, 4f)
                    )
                    if (lit && chosen > 0.4f) {
                        drawCircle(
                            color = palette.onAccent,
                            radius = cellH * 0.18f,
                            center = Offset(x + cellW / 2f, y + cellH / 2f)
                        )
                    }
                }
            }
        }
    }
}

/**
 * Three pebbles, one lifted. The gender step needs a mark that carries no figure
 * and no symbol — only the fact that one of several has been chosen, so the
 * chosen one is the single accent object and the rest stay stone.
 */
@Composable
fun NebFacetsArt(
    selectedIndex: Int,
    modifier: Modifier = Modifier,
    count: Int = 3,
    height: Dp = 130.dp
) {
    val palette = LocalNebAuthPalette.current
    val breath by rememberNebBreathPhase(3000)
    val selected by animateFloatAsState(
        targetValue = selectedIndex.coerceAtLeast(0).toFloat(),
        animationSpec = nebSpatialSpec(),
        label = "neb_facets"
    )

    Box(modifier = modifier.fillMaxWidth().height(height)) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height
            val baseR = min(w / (count * 2.6f), h * 0.26f)
            for (i in 0 until count) {
                val t = if (count == 1) 0.5f else i / (count - 1).toFloat()
                val strength = (1f - kotlin.math.abs(selected - i)).coerceIn(0f, 1f)
                val cx = w * lerp(0.26f, 0.74f, t)
                val cy = h * 0.58f - h * 0.10f * strength * lerp(0.9f, 1.1f, breath)
                val color = palette.accent

                drawRoundRect(
                    color = palette.artSoft,
                    topLeft = Offset(cx - baseR * 0.7f, h * 0.80f),
                    size = Size(baseR * 1.4f, 4f),
                    cornerRadius = CornerRadius(2f, 2f)
                )
                drawCircle(
                    color = if (strength > 0.5f) color else palette.artFaint,
                    radius = baseR * lerp(0.78f, 1f, strength),
                    center = Offset(cx, cy)
                )
                if (strength <= 0.5f) {
                    drawCircle(
                        color = palette.artMid,
                        radius = baseR * 0.78f,
                        center = Offset(cx, cy),
                        style = Stroke(width = 1.3f)
                    )
                }
            }
        }
    }
}
