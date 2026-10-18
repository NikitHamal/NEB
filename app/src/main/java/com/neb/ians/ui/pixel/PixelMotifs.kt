package com.neb.ians.ui.pixel

import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * The festival marks as 16 x 16 pixel sprites, tinted with the live theme's colour: a kite for
 * Dashain, a diyo for Tihar, gulal for Holi, a gurans for New Year, a raindrop for monsoon, a
 * snowflake for winter, a pencil for exams. Same names as the web's motifs (site_themes.APP).
 * Built once per (motif, colour) and cached.
 */
object PixelMotifs {
    private val line = Px.rgb(0x1E2A4A)
    private val gold = Px.rgb(0xFFCE5C)
    private val goldLo = Px.rgb(0xD99A2B)
    private val flame = Px.rgb(0xFFB020)
    private val flameHi = Px.rgb(0xFFF1A6)
    private val teal = Px.rgb(0x18A999)
    private val white = Px.rgb(0xFFFFFF)
    private val cache = HashMap<String, PixelSprite>()

    fun sprite(motif: String, color: Int): PixelSprite? = synchronized(cache) {
        cache.getOrPut("$motif:$color") { build(motif, color) ?: return null }
    }

    private fun build(motif: String, c: Int): PixelSprite? {
        val hi = Px.mix(c, white, 0.45f)
        val lo = Px.mix(c, line, 0.35f)
        return when (motif) {
            "kite" -> PixelSprite.build(16, 16, 8, 140) { f ->
                val a = sin(2 * PI * f / 8).toFloat() * 0.18f
                val pts = floatArrayOf(0f, -6f, 4.5f, -1f, 0f, 4f, -4.5f, -1f)
                val rot = FloatArray(8)
                for (i in 0 until 4) {
                    val x = pts[i * 2]; val y = pts[i * 2 + 1]
                    rot[i * 2] = 8f + x * cos(a) - y * sin(a); rot[i * 2 + 1] = 7f + x * sin(a) + y * cos(a)
                }
                polygon(rot, c)
                polygon(floatArrayOf(rot[0], rot[1], rot[2], rot[3], 8f, 6.5f), hi)
                outline(line)
                for (i in 0..4) set((8 + sin(i * 1.2f + f * 0.8f) * 1.2f).roundToInt(), 12 + i, lo)
            }
            "diyo" -> PixelSprite.build(16, 16, 6, 110) { f ->
                val h = intArrayOf(4, 5, 4, 3, 4, 5)[f]
                for (y in 0 until h) { val w = if (y == 0) 0 else 1; hline(8 - w, 8 + w - (if (y == h - 1) 1 else 0), 8 - y, if (y < 2) flame else flameHi) }
                set(8, 9, flame)
                roundRect(2, 10, 12, 4, 2, c)
                hline(4, 11, 10, hi)
                outline(line)
            }
            "gulal" -> PixelSprite.build(16, 16, 8, 150) { f ->
                val k = sin(2 * PI * f / 8).toFloat()
                disc(6f, 7f, 3.6f + k * 0.5f, c)
                disc(10.5f, 6f, 2.8f - k * 0.4f, teal)
                disc(9f, 11f, 2.8f + k * 0.3f, gold)
                outline(line)
                if (f % 4 == 1) { set(13, 2, hi); set(2, 12, gold) }
            }
            "gurans" -> PixelSprite.build(16, 16, 10, 160) { f ->
                val turn = f * (2 * PI.toFloat() / 5f) / 10f
                for (i in 0 until 5) {
                    val a = turn + i * 2 * PI.toFloat() / 5f
                    disc(8f + cos(a) * 3.4f, 8f + sin(a) * 3.4f, 2.7f, if (i % 2 == 0) c else hi)
                }
                disc(8f, 8f, 1.8f, gold)
                outline(line)
                set(8, 8, goldLo)
            }
            "drop" -> PixelSprite.build(16, 16, 8, 110) { f ->
                if (f < 5) {
                    val y = 1f + f * 2f
                    disc(8f, y + 3f, 2.6f, c)
                    polygon(floatArrayOf(8f, y - 1f, 10f, y + 3f, 6f, y + 3f), c)
                    set(7, (y + 2).toInt(), hi)
                    outline(line)
                } else {
                    val s = f - 4
                    hline(8 - s * 2, 8 + s * 2, 14, c)
                    set(8 - s * 2 - 1, 13, hi); set(8 + s * 2 + 1, 13, hi)
                }
            }
            "snow" -> PixelSprite.build(16, 16, 8, 170) { f ->
                for (k in 0 until 3) {
                    val a = k * PI.toFloat() / 3f
                    for (r in -6..6) set((8 + cos(a) * r).roundToInt(), (8 + sin(a) * r).roundToInt(), if (r % 2 == 0) c else hi)
                }
                disc(8f, 8f, 1.5f, white)
                val tip = f % 6
                val a = tip * PI.toFloat() / 3f
                set((8 + cos(a) * 6).roundToInt(), (8 + sin(a) * 6).roundToInt(), white)
            }
            "pencil" -> PixelSprite.build(16, 16, 8, 120) { f ->
                // the line it has written so far
                for (x in 1..(1 + f)) set(x, 14 - ((x + 1) % 3 == 0).compareTo(false), lo)
                val px = 2 + f
                polygon(floatArrayOf(px.toFloat(), 13f, px + 2f, 11f, px + 9f, 4f, px + 7f, 2f, px.toFloat() - 0f, 9f), c)
                polygon(floatArrayOf(px + 9f, 4f, px + 11f, 2f, px + 9f, 0f, px + 7f, 2f), gold)
                set(px, 13, line)
                outline(line)
            }
            else -> null
        }
    }
}
