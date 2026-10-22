package com.neb.ians.ui.pixel

import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Pixel Neby, the NEBians mascot, at 48 x 48. This file draws one pose: the body (lit from the
 * upper left in three tones, the deep-blue band with its wave and rising bubbles, a rim of light,
 * a highlight), the face (13 eye styles, 8 mouths, cheeks), squash, stretch and tilt, and the
 * ground shadow. The animated states built from poses live in [PixelNebyStates].
 */
object PixelNeby {
    const val SIZE = 48

    internal val line = Px.rgb(0x1E2A4A)
    internal val white = Px.rgb(0xFFFFFF)
    private val shadow = 0x26101830
    private val light = Px.rgb(0xE8F2FF)
    internal val body = Px.rgb(0xCCE2FF)
    private val shade = Px.rgb(0xAFCBF6)
    private val deep = Px.rgb(0x93B5EC)
    private val rim = Px.rgb(0xDDEAFF)
    internal val wave = Px.rgb(0xA9C9FB)
    internal val bandHi = Px.rgb(0x5A8BEA)
    internal val band = Px.rgb(0x2F64D6)
    internal val bandLo = Px.rgb(0x2450B4)
    internal val eyes = Px.rgb(0x0A1C4D)
    internal val blush = Px.rgb(0xF5A9C3)
    internal val pink = Px.rgb(0xFF6F91)
    internal val pinkHi = Px.rgb(0xFFB3C6)
    private val tongue = Px.rgb(0xF0708A)

    enum class Eyes { Open, Half, Blink, Happy, Closed, Up, Wink, Big, Heart, Spiral, Sad, Down, Shades, Star }
    enum class Mouth { None, Smile, Open, O, Flat, Frown, Tongue, Kiss }

    /** One pose. dy moves Neby up (negative) or down; sx/sy squash and stretch; tilt in radians. */
    data class Pose(
        val dy: Float = 0f,
        val sx: Float = 1f,
        val sy: Float = 1f,
        val tilt: Float = 0f,
        val eyes: Eyes = Eyes.Open,
        val mouth: Mouth = Mouth.None,
        val lookX: Int = 0,
        val lookY: Int = 0,
        val blush: Boolean = false,
        val phase: Float = 0f,
        /** What Neby is wearing: festival dress, a hat, headphones... see [NebyLook]. */
        val look: NebyLook = NebyLook.Classic,
        /** Sideways shift, for swings and dances. */
        val dx: Float = 0f,
        /** A Dashain tika on the forehead and jamara behind the ear, whatever the look. */
        val tika: Boolean = false,
        val jamara: Boolean = false,
        /** How much Holi colour has landed on Neby, 0..1. */
        val paint: Float = 0f,
        /** The frame controls tika and jamara itself (the blessing being given): the look adds none of its own. */
        val own: Boolean = false,
    )

    /** Body measurements for one pose, for anything drawn on or around Neby. */
    class Geo(val cx: Float, val cy: Float, val rx: Float, val ry: Float, val ey: Int, val lx: Int, val rx2: Int, val pose: Pose) {
        val top: Float get() = cy - ry
        val bandTop: Float get() = cy + ry * 0.3f
        /** Half the body's width at row [y]. */
        fun halfWidth(y: Float): Float { val t = (y - cy) / ry; return if (t * t >= 1f) 0f else rx * kotlin.math.sqrt(1f - t * t) }
    }

    /** Where the face sits for a pose, so props can be placed relative to it. */
    fun faceY(p: Pose): Float = 44f - 15.5f * p.sy + p.dy - 5f

    /** Draws [p] into this canvas (48 x 48), shadow included. */
    fun PixelCanvas.drawNeby(p: Pose) {
        if (p.tilt == 0f) {
            figure(this, p)
        } else {
            val layer = PixelCanvas(SIZE, SIZE)
            figure(layer, p.copy())
            // rotate about the base so Neby rocks on the ground rather than spinning in air
            val px = 24f + p.dx; val py = 44f + p.dy
            val c = cos(-p.tilt); val s = sin(-p.tilt)
            for (y in 0 until height) for (x in 0 until width) {
                val dx = x + 0.5f - px; val dyy = y + 0.5f - py
                val sxp = (px + dx * c - dyy * s).toInt(); val syp = (py + dx * s + dyy * c).toInt()
                val v = layer.get(sxp, syp)
                if ((v ushr 24) != 0) set(x, y, v)
            }
        }
        val lift = (-p.dy).coerceAtLeast(0f)
        val w = (13f * p.sx - lift * 0.7f).coerceAtLeast(5f)
        val sc = 24f + p.dx
        for (x in (sc - w).toInt()..(sc + w).toInt()) if ((get(x, 46) ushr 24) == 0) set(x, 46, shadow)
        for (x in (sc - w + 3).toInt()..(sc + w - 3).toInt()) if ((get(x, 47) ushr 24) == 0) set(x, 47, shadow)
    }

    private fun figure(c: PixelCanvas, p: Pose) = with(c) {
        val cx = 24f + p.dx
        val r = 15.5f
        val rx = r * p.sx; val ry = r * p.sy
        val cy = 44f - ry + p.dy
        val ey = (cy - 5f).roundToInt() + p.lookY
        val lx = (cx - 6.5f).roundToInt() + p.lookX
        val rx2 = (cx + 3.5f).roundToInt() + p.lookX
        val g = Geo(cx, cy, rx, ry, ey, lx, rx2, p)
        val pal = NebyLooks.band(p.look)
        val band = pal[0]; val bandHi = pal[1]; val bandLo = pal[2]; val wave = pal[3]
        NebyLooks.back(this, g)
        ellipse(cx, cy, rx, ry, body)
        val bandTop = cy + ry * 0.3f
        for (y in 0 until height) for (x in 0 until width) {
            if (get(x, y) != body) continue
            val nx = (x + 0.5f - cx) / rx; val ny = (y + 0.5f - cy) / ry
            val wy = bandTop + sin((x + p.phase) / 3f) * 1.1f
            if (y + 0.5f > wy) {
                val depth = y + 0.5f - wy
                val col = when {
                    depth < 1.2f -> wave
                    depth < 3.6f -> bandHi
                    nx * 0.6f + ny * 0.8f > 0.72f && Bayer.threshold(x, y) < 0.6f -> bandLo
                    else -> band
                }
                set(x, y, col)
                continue
            }
            val lit = -nx * 0.55f - ny * 0.75f
            val edge = nx * nx + ny * ny
            val col = when {
                lit > 0.62f -> light
                lit > 0.48f -> if (Bayer.threshold(x, y) < (lit - 0.48f) / 0.14f) light else body
                edge > 0.82f && nx < -0.2f && ny > -0.2f -> rim // light bouncing up the shadow side
                lit < -0.55f -> deep
                lit < -0.38f -> if (Bayer.threshold(x, y) < (-lit - 0.38f) / 0.17f) deep else shade
                lit < -0.12f -> shade
                lit < 0.02f -> if (Bayer.threshold(x, y) < (-lit + 0.02f) / 0.14f) shade else body
                else -> body
            }
            set(x, y, col)
        }
        for (k in 0 until 2) {
            val t = ((p.phase * 0.15f + k * 0.5f) % 1f)
            val bx = (cx - 6 + k * 9).roundToInt()
            val by = (cy + ry * 0.85f - t * ry * 0.4f).roundToInt()
            if (get(bx, by) == band || get(bx, by) == bandLo) set(bx, by, bandHi)
        }
        val hx = (cx - rx * 0.5f).roundToInt(); val hy = (cy - ry * 0.55f).roundToInt()
        rect(hx, hy, 3, 2, white); set(hx, hy + 2, white)

        eyesAt(this, p.eyes, lx, rx2, ey)
        if (p.blush || p.eyes == Eyes.Happy || p.eyes == Eyes.Wink || p.eyes == Eyes.Heart) {
            hline(lx - 2, lx, ey + 6, blush); hline(rx2 + 2, rx2 + 4, ey + 6, blush)
        }
        mouthAt(this, p.mouth, (cx + p.lookX).roundToInt(), ey + 7)
        NebyLooks.front(this, g)
        outline(line)
        NebyLooks.detail(this, g)
    }

    private fun eyesAt(c: PixelCanvas, e: Eyes, lx: Int, rx: Int, ey: Int) = with(c) {
        for ((i, ex) in intArrayOf(lx, rx).withIndex()) when (e) {
            Eyes.Open -> { rect(ex, ey, 3, 5, eyes); set(ex, ey, white) }
            Eyes.Up -> { rect(ex + 1, ey - 1, 3, 4, eyes); set(ex + 1, ey - 1, white) }
            Eyes.Down -> { rect(ex, ey + 2, 3, 3, eyes); set(ex, ey + 2, white) }
            // the lid halfway down: the eye's lower half, no glint
            Eyes.Half -> rect(ex, ey + 2, 3, 3, eyes)
            Eyes.Blink -> rect(ex, ey + 3, 3, 1, eyes)
            Eyes.Closed -> { set(ex - 1, ey + 2, eyes); rect(ex, ey + 3, 3, 1, eyes); set(ex + 3, ey + 2, eyes) }
            Eyes.Happy -> { set(ex - 1, ey + 3, eyes); set(ex, ey + 2, eyes); set(ex + 1, ey + 1, eyes); set(ex + 2, ey + 2, eyes); set(ex + 3, ey + 3, eyes) }
            Eyes.Wink -> if (i == 1) { set(ex - 1, ey + 3, eyes); set(ex, ey + 2, eyes); set(ex + 1, ey + 1, eyes); set(ex + 2, ey + 2, eyes); set(ex + 3, ey + 3, eyes) } else { rect(ex, ey, 3, 5, eyes); set(ex, ey, white) }
            Eyes.Big -> { rect(ex - 1, ey - 1, 5, 6, eyes); rect(ex - 1, ey - 1, 2, 2, white); set(ex + 2, ey + 3, white) }
            Eyes.Heart -> { set(ex - 1, ey + 1, pink); set(ex, ey, pink); set(ex + 2, ey, pink); set(ex + 3, ey + 1, pink); hline(ex - 1, ex + 3, ey + 1, pink); hline(ex - 1, ex + 3, ey + 2, pink); hline(ex, ex + 2, ey + 3, pink); set(ex + 1, ey + 4, pink); set(ex, ey + 1, pinkHi) }
            Eyes.Spiral -> { rect(ex - 1, ey, 5, 5, eyes); set(ex + 1, ey + 2, white); set(ex, ey + 1, white); set(ex + 2, ey + 1, white); set(ex + 2, ey + 3, white); set(ex, ey + 3, white) }
            Eyes.Sad -> { rect(ex, ey + 1, 3, 4, eyes); set(ex, ey + 1, white); if (i == 0) set(ex + 2, ey + 1, body) else set(ex, ey + 1, body); hline(ex - 1, ex + 3, ey - 2 + (if (i == 0) 1 else 0), eyes) }
            Eyes.Star -> { set(ex + 1, ey, Px.rgb(0xFFCE5C)); hline(ex - 1, ex + 3, ey + 2, Px.rgb(0xFFCE5C)); rect(ex, ey + 1, 3, 3, Px.rgb(0xFFCE5C)); set(ex - 1, ey + 4, Px.rgb(0xFFCE5C)); set(ex + 3, ey + 4, Px.rgb(0xFFCE5C)); set(ex + 1, ey + 2, white) }
            Eyes.Shades -> Unit
        }
        if (e == Eyes.Shades) {
            rect(lx - 2, ey, 7, 4, eyes); rect(rx - 1, ey, 7, 4, eyes); hline(lx + 4, rx - 1, ey + 1, eyes)
            set(lx - 1, ey + 1, white); set(rx, ey + 1, white); set(lx, ey + 1, Px.rgb(0x5A8BEA)); set(rx + 1, ey + 1, Px.rgb(0x5A8BEA))
        }
    }

    private fun mouthAt(c: PixelCanvas, m: Mouth, x: Int, y: Int) = with(c) {
        when (m) {
            Mouth.None -> Unit
            Mouth.Smile -> { set(x - 2, y, eyes); hline(x - 1, x + 1, y + 1, eyes); set(x + 2, y, eyes) }
            Mouth.Open -> { rect(x - 2, y, 4, 3, eyes); hline(x - 1, x, y + 2, tongue) }
            Mouth.O -> { rect(x - 1, y, 2, 3, eyes); set(x - 2, y + 1, eyes); set(x + 1, y + 1, eyes) }
            Mouth.Flat -> hline(x - 1, x + 1, y + 1, eyes)
            Mouth.Frown -> { hline(x - 1, x + 1, y, eyes); set(x - 2, y + 1, eyes); set(x + 2, y + 1, eyes) }
            Mouth.Tongue -> { set(x - 2, y, eyes); hline(x - 1, x + 1, y + 1, eyes); set(x + 2, y, eyes); rect(x, y + 2, 2, 2, tongue) }
            Mouth.Kiss -> { set(x, y, eyes); set(x + 1, y + 1, eyes); set(x, y + 2, eyes) }
        }
    }
}
