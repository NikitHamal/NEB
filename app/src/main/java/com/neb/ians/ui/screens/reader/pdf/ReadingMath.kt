package com.neb.ians.ui.screens.reader.pdf

import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathFillType
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.withTransform

/** A [VShape] ready to draw: its path built once. */
private class RdShape(val path: Path, val shape: VShape)

private fun buildPath(s: VShape): Path {
    val p = Path()
    p.fillType = if (s.evenOdd) PathFillType.EvenOdd else PathFillType.NonZero
    val m = s.cmds
    var i = 0
    while (i < m.size) {
        when (m[i].toInt()) {
            V_MOVE -> { p.moveTo(m[i + 1], m[i + 2]); i += 3 }
            V_LINE -> { p.lineTo(m[i + 1], m[i + 2]); i += 3 }
            V_CUBIC -> { p.cubicTo(m[i + 1], m[i + 2], m[i + 3], m[i + 4], m[i + 5], m[i + 6]); i += 7 }
            else -> { p.close(); i += 1 }
        }
    }
    return p
}

/**
 * Turns a picture of black ink on white paper (a crop of the page: a formula that could not be drawn from its outlines)
 * into the theme's ink with the white made transparent, so it has no white box on a tonal card, a table row or Night.
 */
internal fun inkMask(ink: Color): androidx.compose.ui.graphics.ColorFilter = androidx.compose.ui.graphics.ColorFilter.colorMatrix(
    androidx.compose.ui.graphics.ColorMatrix(
        floatArrayOf(
            0f, 0f, 0f, 0f, ink.red * 255f,
            0f, 0f, 0f, 0f, ink.green * 255f,
            0f, 0f, 0f, 0f, ink.blue * 255f,
            -0.299f, -0.587f, -0.114f, 0f, 255f
        )
    )
)

/**
 * The colour a printed colour takes in the reading theme: black and near black become the theme's ink (so maths
 * is light on Night), white knock-outs are not drawn, anything else keeps its own colour.
 */
internal fun rdInk(rgb: Int, ink: Color, diagram: Boolean = false): Color? {
    val l = rgbLuma(rgb)
    val neutral = !diagram || (maxOf((rgb shr 16) and 0xFF, (rgb shr 8) and 0xFF, rgb and 0xFF) - minOf((rgb shr 16) and 0xFF, (rgb shr 8) and 0xFF, rgb and 0xFF)) < 24
    return when {
        l < 0.38f && neutral -> ink
        l > 0.93f -> null
        else -> Color(0xFF000000.toInt() or rgb)
    }
}

/**
 * Typeset maths drawn from its outlines, scaled so the art's width fills the modifier's width. [shiftPts] moves the
 * drawing down (in points of the page) inside its slot, for slots taller than the formula.
 */
@Composable
internal fun RdVector(art: VectorArt, ink: Color, modifier: Modifier, shiftPts: Float = 0f) {
    val shapes = remember(art) { art.shapes.map { RdShape(buildPath(it), it) } }
    Canvas(modifier) {
        val k = if (art.width > 0f) size.width / art.width else 1f
        withTransform({
            translate(0f, shiftPts * k)
            scale(k, k, Offset.Zero)
        }) {
            for (s in shapes) {
                val v = s.shape
                if (v.fill) rdInk(v.fillRgb, ink, art.diagram)?.let { drawPath(s.path, it.copy(alpha = it.alpha * v.fillA)) }
                if (v.stroke) rdInk(v.strokeRgb, ink, art.diagram)?.let { drawPath(s.path, it.copy(alpha = it.alpha * v.strokeA), style = Stroke(width = v.width)) }
            }
        }
    }
}
