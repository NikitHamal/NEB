package com.neb.ians.ui.screens.reader.pdf

import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

/*
 * Typeset maths in the NEBians print is vector outlines, one filled path per glyph. Reading mode keeps those outlines
 * and draws them itself (sharp at every size, in the theme's ink, no white boxes, no bitmaps to wait for) instead of
 * cropping a render of the page. Pure Kotlin like the rest of the structure reader.
 */

internal const val V_MOVE = 0
internal const val V_LINE = 1
internal const val V_CUBIC = 2
internal const val V_CLOSE = 3

/**
 * One painted path in points, origin at the top left of its [VectorArt]. [cmds] is a flat list: an opcode
 * ([V_MOVE] x y, [V_LINE] x y, [V_CUBIC] x1 y1 x2 y2 x3 y3, [V_CLOSE]) followed by its operands.
 */
class VShape(
    val cmds: FloatArray, val fill: Boolean, val stroke: Boolean,
    val fillRgb: Int, val strokeRgb: Int, val width: Float, val evenOdd: Boolean
)

/** A formula or drawing as outlines: [width] by [height] points. A [diagram] keeps its own colours (only neutral darks follow the ink). */
class VectorArt(val width: Float, val height: Float, val shapes: List<VShape>, val diagram: Boolean = false)

/** 0 (black) to 1 (white) for a packed 0xRRGGBB colour. */
internal fun rgbLuma(rgb: Int): Float {
    val r = (rgb shr 16) and 0xFF; val g = (rgb shr 8) and 0xFF; val b = rgb and 0xFF
    return (0.299f * r + 0.587f * g + 0.114f * b) / 255f
}

internal object PdfVector {
    /**
     * The outlines inside the box, or null when the box cannot be drawn faithfully from them: text sits in it (the
     * crop of the page keeps that), an image sits in it, or a path inside was too big to keep.
     */
    fun of(c: PageContent, l: Float, t: Float, r: Float, b: Float, diagram: Boolean = false): VectorArt? {
        for (run in c.runs) {
            if (run.hidden) continue
            val top = run.base - run.size * 0.8f
            val bottom = run.base + run.size * 0.2f
            val ox = min(run.x1, r) - max(run.x0, l)
            val oy = min(bottom, b) - max(top, t)
            if (ox > 0.6f && oy > 0.3f * (bottom - top)) return null
        }
        val slack = 1.5f
        val shapes = ArrayList<VShape>()
        for (g in c.gfx) {
            if (g.x1 < l - slack || g.x0 > r + slack || g.y1 < t - slack || g.y0 > b + slack) continue
            if (g.kind == G_IMAGE) return null
            val inside = g.x0 >= l - slack && g.x1 <= r + slack && g.y0 >= t - slack && g.y1 <= b + slack
            if (!inside) continue
            val cmds = g.cmds ?: return null
            if (g.fill && !g.stroke && rgbLuma(g.fillRgb) > 0.93f) continue
            val out = FloatArray(cmds.size)
            var i = 0
            while (i < cmds.size) {
                val op = cmds[i].toInt()
                out[i] = cmds[i]
                val n = when (op) { V_MOVE, V_LINE -> 1; V_CUBIC -> 3; else -> 0 }
                for (k in 0 until n) { out[i + 1 + 2 * k] = cmds[i + 1 + 2 * k] - l; out[i + 2 + 2 * k] = cmds[i + 2 + 2 * k] - t }
                i += 1 + 2 * n
            }
            shapes.add(VShape(out, g.fill, g.stroke, g.fillRgb, g.strokeRgb, max(g.lineWidth, 0.3f), g.evenOdd))
        }
        if (shapes.isEmpty() || shapes.size > 2500) return null
        return VectorArt(r - l, b - t, shapes, diagram)
    }

    /** Distance from [center] to the farther edge of a [height] tall box: half the height of a box centred on [center]. */
    fun half(center: Float, height: Float): Float = max(abs(center), abs(height - center))
}
