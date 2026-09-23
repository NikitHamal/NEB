package com.neb.ians.ui.components.art

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathMeasure
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

// ---------------------------------------------------------------------------
// App-wide state art. These live outside the auth journey, so they take their
// colours from the active Material scheme rather than the journey palette, and
// they carry the same drawn language: a sheet, a ridge, an orbit, some motes.
// ---------------------------------------------------------------------------

enum class NebStateKind { Empty, Error, Offline, Success, Searching }

/**
 * A full state block: animated art, a headline, an optional line of detail and
 * an optional action. Drop-in replacement for an icon-in-a-circle empty state.
 */
@Composable
fun NebStateView(
    kind: NebStateKind,
    title: String,
    modifier: Modifier = Modifier,
    subtitle: String? = null,
    artHeight: Dp = 136.dp,
    action: (@Composable () -> Unit)? = null
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 32.dp, vertical = 28.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        NebStateArt(kind = kind, height = artHeight)
        Spacer(modifier = Modifier.height(2.dp))
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface,
            textAlign = TextAlign.Center
        )
        if (subtitle != null) {
            Text(
                text = subtitle,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
        }
        if (action != null) {
            Spacer(modifier = Modifier.height(6.dp))
            action()
        }
    }
}

/** The illustration on its own, for screens that already have their own copy. */
@Composable
fun NebStateArt(
    kind: NebStateKind,
    modifier: Modifier = Modifier,
    height: Dp = 136.dp
) {
    val scheme = MaterialTheme.colorScheme
    val accent = when (kind) {
        NebStateKind.Error -> scheme.error
        else -> scheme.onSurface
    }
    val sheet = scheme.surfaceContainerHigh
    val line = scheme.outline.copy(alpha = 0.26f)
    val faint = scheme.onSurfaceVariant.copy(alpha = 0.22f)

    val phase by rememberNebArtPhase(durationMillis = 9000)
    val breath by rememberNebBreathPhase(durationMillis = 3000)

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(height)
    ) {
        val center = Offset(size.width / 2f, size.height * 0.5f)
        when (kind) {
            NebStateKind.Empty -> drawEmpty(center, sheet, line, faint, accent, breath)
            NebStateKind.Error -> drawError(center, sheet, line, accent, breath)
            NebStateKind.Offline -> drawOffline(center, sheet, line, faint, accent, phase)
            NebStateKind.Success -> drawSuccess(center, accent, line, phase, breath)
            NebStateKind.Searching -> drawSearching(center, sheet, line, faint, accent, phase)
        }
    }
}

/** An empty shelf: two stacked sheets, the top one blank, one mote drifting. */
private fun DrawScope.drawEmpty(
    center: Offset,
    sheet: Color,
    line: Color,
    faint: Color,
    accent: Color,
    breath: Float
) {
    val w = size.minDimension * 0.58f
    val h = w * 0.66f
    val lift = (breath - 0.5f) * size.height * 0.03f

    nebSheet(
        topLeft = Offset(center.x - w / 2f + 10f, center.y - h / 2f + 14f),
        sheetSize = Size(w, h),
        fill = faint.copy(alpha = 0.14f),
        radius = 14f
    )
    nebSheet(
        topLeft = Offset(center.x - w / 2f, center.y - h / 2f + lift),
        sheetSize = Size(w, h),
        fill = sheet,
        stroke = line,
        radius = 14f
    )
    nebTextLines(
        start = Offset(center.x - w / 2f + 18f, center.y - h * 0.18f + lift),
        lineWidths = listOf(w * 0.52f, w * 0.34f),
        color = faint,
        lineHeight = 7f,
        gap = 11f
    )
    drawCircle(
        color = accent.copy(alpha = 0.5f),
        radius = 4.5f,
        center = Offset(center.x + w * 0.34f, center.y - h * 0.58f - lift * 2f)
    )
}

/** A sheet knocked off axis, with a soft ping where it went wrong. */
private fun DrawScope.drawError(
    center: Offset,
    sheet: Color,
    line: Color,
    accent: Color,
    breath: Float
) {
    val w = size.minDimension * 0.54f
    val h = w * 0.7f
    rotate(degrees = -7f, pivot = center) {
        nebSheet(
            topLeft = Offset(center.x - w / 2f, center.y - h / 2f),
            sheetSize = Size(w, h),
            fill = sheet,
            stroke = line,
            radius = 14f
        )
    }
    val badge = Offset(center.x + w * 0.42f, center.y - h * 0.44f)
    drawCircle(color = accent, radius = size.minDimension * 0.062f, center = badge)
    val stemTop = badge.copy(y = badge.y - size.minDimension * 0.026f)
    val stemBottom = badge.copy(y = badge.y + size.minDimension * 0.008f)
    drawLine(
        color = Color.White,
        start = stemTop,
        end = stemBottom,
        strokeWidth = 2.6f,
        cap = StrokeCap.Round
    )
    drawCircle(
        color = Color.White,
        radius = 1.6f,
        center = badge.copy(y = badge.y + size.minDimension * 0.026f)
    )
}

/** A ridge with a broken signal arc above it — the shape of no connection. */
private fun DrawScope.drawOffline(
    center: Offset,
    sheet: Color,
    line: Color,
    faint: Color,
    accent: Color,
    phase: Float
) {
    val baseline = size.height * 0.84f
    nebRidge(baseline, listOf(0.22f to 0.30f, 0.55f to 0.44f, 0.84f to 0.26f), faint.copy(alpha = 0.18f))
    nebRidge(baseline, listOf(0.36f to 0.22f, 0.70f to 0.32f), faint.copy(alpha = 0.28f))

    val mast = Offset(size.width * 0.5f, baseline)
    drawLine(
        color = line,
        start = mast,
        end = mast.copy(y = size.height * 0.30f),
        strokeWidth = 2.2f,
        cap = StrokeCap.Round
    )
    val top = mast.copy(y = size.height * 0.30f)
    val blink = if (pulse(phase * 2f) > 0.45f) 0.85f else 0.2f
    drawCircle(color = accent.copy(alpha = blink), radius = 4.2f, center = top)
    for (i in 1..2) {
        val r = size.minDimension * (0.10f + i * 0.075f)
        nebOrbit(top, r, line.copy(alpha = 0.55f - i * 0.12f), strokeWidth = 1.8f, dashed = true)
    }
    drawLine(
        color = accent.copy(alpha = 0.75f),
        start = Offset(top.x - size.minDimension * 0.17f, top.y - size.minDimension * 0.12f),
        end = Offset(top.x + size.minDimension * 0.17f, top.y + size.minDimension * 0.16f),
        strokeWidth = 2.6f,
        cap = StrokeCap.Round
    )
    nebSheet(
        topLeft = Offset(center.x - size.minDimension * 0.05f, baseline - 4f),
        sheetSize = Size(size.minDimension * 0.1f, 8f),
        fill = sheet,
        radius = 4f
    )
}

/** A ring that closes, then a tick that draws itself inside it. */
private fun DrawScope.drawSuccess(
    center: Offset,
    accent: Color,
    line: Color,
    phase: Float,
    breath: Float
) {
    val radius = size.minDimension * 0.24f
    nebOrbit(center, radius * 1.42f, line.copy(alpha = 0.4f), strokeWidth = 1.4f)
    drawCircle(color = accent.copy(alpha = 0.14f), radius = radius, center = center)
    drawCircle(
        color = accent,
        radius = radius,
        center = center,
        style = Stroke(width = 2.4f)
    )

    val tick = Path().apply {
        moveTo(center.x - radius * 0.42f, center.y + radius * 0.04f)
        lineTo(center.x - radius * 0.08f, center.y + radius * 0.36f)
        lineTo(center.x + radius * 0.46f, center.y - radius * 0.34f)
    }
    val measure = PathMeasure().apply { setPath(tick, false) }
    val drawn = Path()
    val progress = (0.35f + breath * 0.65f).coerceIn(0f, 1f)
    measure.getSegment(0f, measure.length * progress, drawn, true)
    drawPath(
        path = drawn,
        color = accent,
        style = Stroke(width = 3.4f, cap = StrokeCap.Round)
    )
}

/** A lens sweeping a field of cards — for "looking" rather than "nothing here". */
private fun DrawScope.drawSearching(
    center: Offset,
    sheet: Color,
    line: Color,
    faint: Color,
    accent: Color,
    phase: Float
) {
    val cardW = size.minDimension * 0.2f
    val cardH = cardW * 0.74f
    for (row in 0 until 2) {
        for (col in 0 until 3) {
            val x = center.x + (col - 1) * (cardW + 12f) - cardW / 2f
            val y = center.y + (row - 0.5f) * (cardH + 12f) - cardH / 2f
            nebSheet(
                topLeft = Offset(x, y),
                sheetSize = Size(cardW, cardH),
                fill = sheet,
                stroke = line,
                radius = 8f
            )
            nebTextLines(
                start = Offset(x + 8f, y + cardH * 0.34f),
                lineWidths = listOf(cardW * 0.6f, cardW * 0.4f),
                color = faint,
                lineHeight = 4f,
                gap = 6f
            )
        }
    }

    val sweep = orbitPoint(center, size.minDimension * 0.22f, 142f)
    val lens = size.minDimension * 0.11f
    drawCircle(color = accent.copy(alpha = 0.12f), radius = lens, center = sweep)
    drawCircle(color = accent, radius = lens, center = sweep, style = Stroke(width = 2.4f))
    drawLine(
        color = accent,
        start = Offset(sweep.x + lens * 0.7f, sweep.y + lens * 0.7f),
        end = Offset(sweep.x + lens * 1.55f, sweep.y + lens * 1.55f),
        strokeWidth = 3f,
        cap = StrokeCap.Round
    )
}

/**
 * A breathing halo for an icon that already carries the meaning — used behind the
 * glyph in [com.neb.ians.ui.components.NebEmptyState] so every existing empty
 * state gains motion without changing its call site.
 */
@Composable
fun NebIconHalo(
    modifier: Modifier = Modifier,
    diameter: Dp = 78.dp,
    color: Color = MaterialTheme.colorScheme.primary
) {
    val phase by rememberNebArtPhase(durationMillis = 5200)
    val breath by rememberNebBreathPhase(durationMillis = 3400)
    val fill = MaterialTheme.colorScheme.surfaceContainerHigh
    Canvas(modifier = modifier.size(diameter)) {
        val center = Offset(size.width / 2f, size.height / 2f)
        val base = size.minDimension * 0.34f
        drawCircle(color = fill, radius = base * (0.98f + breath * 0.04f), center = center)
    }
}

/** A compact inline spark for row-level loading or "new" affordances. */
@Composable
fun NebStatePulse(
    modifier: Modifier = Modifier,
    dotSize: Dp = 26.dp,
    color: Color = MaterialTheme.colorScheme.primary
) {
    val phase by rememberNebArtPhase(durationMillis = 1800)
    Canvas(modifier = modifier.size(dotSize)) {
        val center = Offset(size.width / 2f, size.height / 2f)
        nebRings(center, size.minDimension * 0.18f, phase, color, count = 3, spread = 2.4f, strokeWidth = 1.4f)
        drawCircle(color = color, radius = size.minDimension * 0.16f, center = center)
    }
}
