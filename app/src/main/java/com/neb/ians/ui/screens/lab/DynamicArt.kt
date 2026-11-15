package com.neb.ians.ui.screens.lab

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate

/** Colours and corner ease toward the next look, so changing a look reads as one smooth repaint. */
@Composable
internal fun animateLook(target: Look): Look {
    val t = tween<Color>(durationMillis = 300)
    val bg by animateColorAsState(target.bg, t, label = "bg")
    val ink by animateColorAsState(target.ink, t, label = "ink")
    val accent by animateColorAsState(target.accent, t, label = "accent")
    val soft by animateColorAsState(target.soft, t, label = "soft")
    val corner by animateFloatAsState(target.corner.toFloat(), tween(300), label = "corner")
    return target.copy(bg = bg, ink = ink, accent = accent, soft = soft, corner = corner.toInt())
}

/** Flat cover art. Everything is a stroke or a fill in the accent at low alpha. */
internal fun DrawScope.drawPattern(look: Look) {
    val col = look.accent.copy(alpha = 0.22f)
    val w = size.width
    val h = size.height
    when (look.pattern) {
        Pattern.None -> Unit
        Pattern.Dots -> {
            var y = 14f
            while (y < h) { var x = 14f; while (x < w) { drawCircle(col, 3.2f, Offset(x, y)); x += 26f }; y += 26f }
        }
        Pattern.Lines -> {
            var y = 12f
            while (y < h) { drawLine(col, Offset(0f, y), Offset(w, y), 2f); y += 16f }
        }
        Pattern.Grid -> {
            var x = 0f
            while (x < w) { drawLine(col, Offset(x, 0f), Offset(x, h), 1.5f); x += 28f }
            var y = 0f
            while (y < h) { drawLine(col, Offset(0f, y), Offset(w, y), 1.5f); y += 28f }
        }
        Pattern.Waves -> {
            var row = 0
            while (row * 24f < h + 24f) {
                val p = Path()
                p.moveTo(0f, row * 24f)
                var x = 0f
                while (x < w) { p.relativeQuadraticTo(15f, -12f, 30f, 0f); p.relativeQuadraticTo(15f, 12f, 30f, 0f); x += 60f }
                drawPath(p, col, style = Stroke(2.5f))
                row++
            }
        }
        Pattern.Rings -> for (i in 1..6) drawCircle(col, i * 26f, Offset(w * 0.86f, h * 0.2f), style = Stroke(2.5f))
        Pattern.Blobs -> {
            drawCircle(col, h * 0.62f, Offset(w * 0.84f, h * 0.18f))
            drawCircle(col, h * 0.34f, Offset(w * 0.1f, h * 0.9f))
            drawRoundRect(col, Offset(w * 0.42f, h * 0.55f), Size(h * 0.5f, h * 0.5f), CornerRadius(h * 0.2f))
        }
        Pattern.Stripes -> {
            val gap = 30f
            var x = -h
            while (x < w) { drawLine(col, Offset(x, h), Offset(x + h, 0f), 9f); x += gap }
        }
        Pattern.Confetti -> {
            var i = 0
            var y = 18f
            while (y < h) {
                var x = if (i % 2 == 0) 20f else 46f
                while (x < w) {
                    rotate((x * 0.7f + y * 1.3f) % 180f, Offset(x, y)) {
                        drawRoundRect(col, Offset(x - 7f, y - 2.5f), Size(14f, 5f), CornerRadius(2.5f))
                    }
                    x += 52f
                }
                y += 26f; i++
            }
        }
    }
}

/** A section break in the look's own divider style. */
internal fun DrawScope.drawDivider(look: Look) {
    val col = look.accent.copy(alpha = 0.5f)
    val w = size.width
    val cy = size.height / 2f
    when (look.divider) {
        Divider.Line -> drawLine(col, Offset(0f, cy), Offset(w, cy), 2f, StrokeCap.Round)
        Divider.Dots -> {
            val n = 3
            val gap = 18f
            val start = w / 2f - gap
            for (k in 0 until n) drawCircle(col, 3.5f, Offset(start + k * gap, cy))
        }
        Divider.Wave -> {
            val p = Path()
            p.moveTo(w / 2f - 120f, cy)
            repeat(4) { p.relativeQuadraticTo(15f, -9f, 30f, 0f); p.relativeQuadraticTo(15f, 9f, 30f, 0f) }
            drawPath(p, col, style = Stroke(2.5f, cap = StrokeCap.Round))
        }
    }
}
