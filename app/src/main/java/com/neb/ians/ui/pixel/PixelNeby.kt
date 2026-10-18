package com.neb.ians.ui.pixel

import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Pixel Neby at 48 x 48: the app's mascot drawn from its own colours (neby-avatar.js). Three-tone
 * shading lit from the upper left, the deep-blue band with its wave and a few drifting bubbles,
 * eyes with a glint, cheeks that blush when happy, and a ground shadow that shrinks as it rises.
 */
object PixelNeby {
    private val line = Px.rgb(0x1E2A4A)
    private val white = Px.rgb(0xFFFFFF)
    private val shadow = 0x26101830
    private val light = Px.rgb(0xE8F2FF)
    private val body = Px.rgb(0xCCE2FF)
    private val shade = Px.rgb(0xAFCBF6)
    private val deep = Px.rgb(0x93B5EC)
    private val wave = Px.rgb(0xA9C9FB)
    private val bandHi = Px.rgb(0x5A8BEA)
    private val band = Px.rgb(0x2F64D6)
    private val bandLo = Px.rgb(0x2450B4)
    private val eyes = Px.rgb(0x0A1C4D)
    private val blush = Px.rgb(0xF5A9C3)

    enum class Eyes { Open, Blink, Happy, Closed, Up, Wink }

    const val SIZE = 48

    fun PixelCanvas.pose(dy: Float, sx: Float = 1f, sy: Float = 1f, eyesAre: Eyes = Eyes.Open, look: Int = 0, phase: Float = 0f) {
        val cx = 24f
        val r = 15.5f
        val ground = 44f
        val cy = ground - r * sy + dy
        val rx = r * sx; val ry = r * sy
        ellipse(cx, cy, rx, ry, body)
        val bandTop = cy + ry * 0.3f
        for (y in 0 until height) for (x in 0 until width) {
            if (get(x, y) != body) continue
            val nx = (x + 0.5f - cx) / rx; val ny = (y + 0.5f - cy) / ry
            val wy = bandTop + sin((x + phase) / 3f) * 1.1f
            if (y + 0.5f > wy) {
                // the band: a lit top edge, the deep blue, darker toward the lower right
                val depth = y + 0.5f - wy
                val c = when {
                    depth < 1.2f -> wave
                    depth < 3.6f -> bandHi
                    nx * 0.6f + ny * 0.8f > 0.72f && Bayer.threshold(x, y) < 0.6f -> bandLo
                    else -> band
                }
                set(x, y, c)
                continue
            }
            val lit = -nx * 0.55f - ny * 0.75f
            val c = when {
                lit > 0.62f -> light
                lit > 0.48f -> if (Bayer.threshold(x, y) < (lit - 0.48f) / 0.14f) light else body
                lit < -0.55f -> deep
                lit < -0.38f -> if (Bayer.threshold(x, y) < (-lit - 0.38f) / 0.17f) deep else shade
                lit < -0.12f -> shade
                lit < 0.02f -> if (Bayer.threshold(x, y) < (-lit + 0.02f) / 0.14f) shade else body
                else -> body
            }
            set(x, y, c)
        }
        // bubbles rising inside the band
        for (k in 0 until 2) {
            val t = ((phase * 0.15f + k * 0.5f) % 1f)
            val bx = (cx - 6 + k * 9).roundToInt()
            val by = (cy + ry * 0.85f - t * ry * 0.4f).roundToInt()
            if (get(bx, by) == band || get(bx, by) == bandLo) set(bx, by, bandHi)
        }
        // the highlight
        val hx = (cx - rx * 0.5f).roundToInt(); val hy = (cy - ry * 0.55f).roundToInt()
        rect(hx, hy, 3, 2, white); set(hx, hy + 2, white)
        // eyes
        val ey = (cy - 5f).roundToInt()
        val lx = (cx - 6.5f).roundToInt() + look
        val rx2 = (cx + 3.5f).roundToInt() + look
        for ((i, ex) in intArrayOf(lx, rx2).withIndex()) {
            val state = if (eyesAre == Eyes.Wink && i == 1) Eyes.Happy else if (eyesAre == Eyes.Wink) Eyes.Open else eyesAre
            when (state) {
                Eyes.Open -> { rect(ex, ey, 3, 5, eyes); set(ex, ey, white) }
                Eyes.Up -> { rect(ex + 1, ey - 1, 3, 4, eyes); set(ex + 1, ey - 1, white) }
                Eyes.Blink -> rect(ex, ey + 3, 3, 1, eyes)
                Eyes.Closed -> { set(ex - 1, ey + 2, eyes); rect(ex, ey + 3, 3, 1, eyes); set(ex + 3, ey + 2, eyes) }
                Eyes.Happy -> { set(ex - 1, ey + 3, eyes); set(ex, ey + 2, eyes); set(ex + 1, ey + 1, eyes); set(ex + 2, ey + 2, eyes); set(ex + 3, ey + 3, eyes) }
                Eyes.Wink -> Unit
            }
        }
        if (eyesAre == Eyes.Happy || eyesAre == Eyes.Wink) {
            hline(lx - 2, lx, ey + 6, blush); hline(rx2 + 2, rx2 + 4, ey + 6, blush)
        }
        outline(line)
        val lift = (-dy).coerceAtLeast(0f)
        val w = (13f - lift * 0.7f).coerceAtLeast(5f)
        for (x in (cx - w).toInt()..(cx + w).toInt()) if (get(x, 46) ushr 24 == 0) set(x, 46, shadow)
        for (x in (cx - w + 3).toInt()..(cx + w - 3).toInt()) if (get(x, 47) ushr 24 == 0) set(x, 47, shadow)
    }

    val idle: PixelSprite by lazy {
        val dys = floatArrayOf(0f, 0f, -0.5f, -1f, -1.5f, -1.5f, -1f, -0.5f, 0f, 0f, -0.5f, -1f, -1.5f, -1.5f, -1f, -0.5f)
        PixelSprite.build(SIZE, SIZE, dys.size, 115) { f ->
            pose(dys[f], eyesAre = if (f == 14) Eyes.Blink else Eyes.Open, look = if (f in 5..9) 1 else 0, phase = f.toFloat())
        }
    }

    val hop: PixelSprite by lazy {
        val poses = listOf(
            Triple(0f, 1f, 1f), Triple(0f, 1.12f, 0.86f), Triple(-3f, 0.92f, 1.1f), Triple(-7f, 0.96f, 1.04f),
            Triple(-9f, 1f, 1f), Triple(-7.5f, 1f, 1f), Triple(-3f, 0.96f, 1.04f), Triple(0f, 1.14f, 0.85f),
            Triple(0f, 1.05f, 0.95f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f),
        )
        PixelSprite.build(SIZE, SIZE, poses.size, 72) { f ->
            val (dy, sx, sy) = poses[f]
            pose(dy, sx, sy, eyesAre = if (f in 2..8) Eyes.Happy else Eyes.Open, phase = f * 1.5f)
        }
    }

    val think: PixelSprite by lazy {
        PixelSprite.build(SIZE, SIZE, 8, 160) { f ->
            pose(if (f % 4 < 2) 0f else -0.5f, eyesAre = if (f == 6) Eyes.Blink else Eyes.Up, phase = f * 1.2f)
            val n = f % 4
            for (i in 0 until 3) rect(31 + i * 5, 4 - if (i < n) 1 else 0, 3, 3, if (i < n) band else wave)
        }
    }

    val sleep: PixelSprite by lazy {
        PixelSprite.build(SIZE, SIZE, 12, 140) { f ->
            pose(if (f % 6 < 3) 0f else 0.5f, sx = 1.02f, sy = 0.98f, eyesAre = Eyes.Closed, phase = f * 0.5f)
            for (k in 0 until 2) {
                val t = ((f + k * 6) % 12) / 12f
                val x = 33 + (t * 6).toInt() + k * 2
                val y = (15 - t * 13).toInt()
                val c = if (t < 0.8f) Px.rgb(0x8C97B3) else Px.rgb(0xB9C3DA)
                hline(x, x + 3, y, c); set(x + 2, y + 1, c); set(x + 1, y + 2, c); hline(x, x + 3, y + 3, c)
            }
        }
    }

    val wink: PixelSprite by lazy {
        PixelSprite.build(SIZE, SIZE, 10, 110) { f ->
            val dy = floatArrayOf(0f, -1f, -2f, -2f, -2f, -2f, -1f, 0f, 0f, 0f)[f]
            pose(dy, eyesAre = if (f in 2..6) Eyes.Wink else Eyes.Open, phase = f.toFloat())
        }
    }
}
