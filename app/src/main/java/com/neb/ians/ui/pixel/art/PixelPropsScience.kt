package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.Bayer
import com.neb.ians.ui.pixel.PixelCanvas
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Props for the sciences: physics, chemistry, mathematics, biology and general science. Each is
 * drawn standing on (x, base): x is its centre, base the ground row. Light comes from the upper
 * left, as in the rest of the pixel art.
 */
internal object PixelPropsScience {
    private val metal = c(0xE3E9F3); private val metalMid = c(0xB4C0D4); private val metalLo = c(0x7F8BA6)
    private val glass = c(0xD9F1FF); private val glassMid = c(0xAED9F4); private val glassLo = c(0x86BDE6)
    private val wood = c(0xC48E58); private val woodHi = c(0xE2B07A); private val woodLo = c(0x93613A)
    private val black = c(0x2B3044); private val white = c(0xFFFFFF)
    private val rainbow = intArrayOf(c(0xE53935), c(0xFB8C00), c(0xFDD835), c(0x43A047), c(0x1E88E5), c(0x8E24AA))

    // ---- physics -----------------------------------------------------------------------------------

    fun prism(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val top = base - 20
        // the white beam comes in from the left, the spectrum fans out to the right
        detail { for (k in -1..0) line(x - 44, base - 17 + k, x - 6, base - 11 + k, c(0xFFFDF0)) }
        prop {
            polygon(floatArrayOf(x - 12f, base.toFloat(), x.toFloat(), top.toFloat(), x + 12f, base.toFloat()), glass)
            for (yy in top..base) for (xx in x - 12..x + 12) if (get(xx, yy) == glass && (xx - x) > (yy - top) * 0.25f && Bayer.threshold(xx, yy) < 0.5f) set(xx, yy, glassMid)
            line(x - 1, top + 2, x - 9, base - 1, white)
        }
        detail {
            for ((i, col) in rainbow.withIndex()) {
                val y0 = base - 11 + i / 3
                line(x + 5, y0, x + 52, base - 18 + i * 4, col); line(x + 5, y0 + 1, x + 52, base - 17 + i * 4, col)
            }
        }
    }

    fun cradle(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val top = base - 26
        prop {
            box(x - 17, base - 3, 34, 3, wood, woodHi, woodLo)
            rect(x - 15, top, 2, 23, metalMid); rect(x + 13, top, 2, 23, metalMid)
            rect(x - 15, top, 30, 2, metal)
        }
        val balls = 5
        for (i in 0 until balls) {
            val bx0 = x - 8 + i * 4
            val swing = i == 0
            val bx = if (swing) bx0 - 9 else bx0
            val by = if (swing) base - 12 else base - 9
            detail { line(bx0, top + 2, bx, by - 2, metalLo) }
            prop { disc(bx + 0.5f, by + 0.5f, 2.6f, metalMid); set(bx - 1, by - 1, metal); set(bx, by - 1, white) }
        }
        detail { for (k in 0..2) set(x - 21 - k, base - 13 + k, c(0x9FB4D6)) }
    }

    fun telescope(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        // Saturn waits in the sky
        detail {
            disc(x + 34f, base - 38f, 4f, c(0xF2C46B)); hline(x + 31, x + 35, base - 39, c(0xF8DC9A))
            for (k in -8..8) set(x + 34 + k, base - 38 + (k * 0.25f).roundToInt(), c(0xE7D8B0))
        }
        prop {
            line(x, base - 12, x - 9, base, black); line(x, base - 12, x + 8, base, black); line(x, base - 12, x, base, black)
            line(x - 9, base, x - 8, base, black)
            // the tube, pointing up and right at the planet
            polygon(floatArrayOf(x - 13f, base - 10f, x + 15f, base - 26f, x + 18f, base - 21f, x - 10f, base - 5f), c(0x3D6FD1))
            polygon(floatArrayOf(x - 13f, base - 10f, x + 15f, base - 26f, x + 16f, base - 24f, x - 12f, base - 8f), c(0x6E98E8))
            rect(x + 14, base - 27, 5, 7, c(0x2A4F9E))
            rect(x - 16, base - 10, 4, 4, black)
        }
    }

    // ---- chemistry ---------------------------------------------------------------------------------

    fun flask(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val liquid = c(0x2FD38F); val liquidLo = c(0x1FA872)
        prop {
            rect(x - 3, base - 30, 7, 9, glass)
            rect(x - 4, base - 31, 9, 2, glassMid)
            polygon(floatArrayOf(x - 3f, base - 21f, x + 4f, base - 21f, x + 13f, base.toFloat(), x - 12f, base.toFloat()), glass)
            // liquid
            for (yy in base - 10..base - 1) for (xx in x - 12..x + 13) if (get(xx, yy) == glass) set(xx, yy, if (yy == base - 10) c(0x9CF2C9) else if (xx > x + 4 && Bayer.threshold(xx, yy) < 0.6f) liquidLo else liquid)
            line(x - 2, base - 29, x - 2, base - 22, white); line(x - 4, base - 19, x - 9, base - 5, white)
        }
        detail {
            set(x - 3, base - 14, white); set(x + 2, base - 17, c(0xC9F7E2)); set(x, base - 24, c(0xC9F7E2)); set(x + 1, base - 36, c(0xC9F7E2))
            disc(x + 3f, base - 40f, 1.4f, c(0xE6FBF2)); disc(x - 2f, base - 45f, 1.8f, c(0xE6FBF2))
        }
    }

    fun tubes(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val cols = intArrayOf(c(0xFF6F91), c(0x3FA7FF), c(0xFFC93C), c(0x9B5DE5))
        prop {
            for (i in 0 until 4) {
                val tx = x - 13 + i * 8
                val h = 20 + (i % 2) * 3
                rect(tx, base - h, 5, h - 2, glass); rect(tx + 1, base - 2, 3, 1, glass)
                for (yy in base - h + 8 + i..base - 2) for (xx in tx..tx + 4) if (get(xx, yy) == glass) set(xx, yy, cols[i])
                line(tx + 1, base - h + 1, tx + 1, base - h + 6, white)
            }
            box(x - 17, base - 9, 35, 3, wood, woodHi, woodLo)
            rect(x - 17, base - 6, 3, 6, woodLo); rect(x + 15, base - 6, 3, 6, woodLo)
        }
    }

    fun molecule(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val cy = base - 18
        val atoms = listOf(Triple(x - 13, cy + 6, 3.4f), Triple(x + 12, cy + 7, 3.4f), Triple(x + 2, cy - 12, 3.4f), Triple(x - 6, cy - 6, 2.8f))
        detail { for ((ax, ay, _) in atoms) { line(x, cy, ax, ay, c(0x9AA6BD)); line(x + 1, cy, ax + 1, ay, c(0x9AA6BD)) } }
        prop {
            disc(x + 0.5f, cy + 0.5f, 5.6f, c(0xE5484D))
            for ((i, a) in atoms.withIndex()) disc(a.first + 0.5f, a.second + 0.5f, a.third, if (i == 3) c(0x3FA7FF) else c(0xF4F6FA))
        }
        detail {
            set(x - 2, cy - 2, c(0xFF9A9D)); set(x - 1, cy - 3, white)
            for ((ax, ay, _) in atoms) set(ax - 1, ay - 1, white)
        }
    }

    // ---- mathematics -------------------------------------------------------------------------------

    fun geometry(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            // a protractor, then a set square standing against it
            for (yy in base - 13..base) for (xx in x - 20..x + 4) {
                val d = kotlin.math.hypot(xx + 0.5f - (x - 8), yy + 0.5f - base)
                if (d <= 12.5f) set(xx, yy, if (d > 10.5f) c(0xFFD54F) else c(0xFFF3C4))
            }
            polygon(floatArrayOf(x + 2f, base.toFloat(), x + 2f, base - 26f, x + 20f, base.toFloat()), c(0x7FB2FF))
            polygon(floatArrayOf(x + 5f, base - 3f, x + 5f, base - 17f, x + 14f, base - 3f), c(0xE7F0FF))
        }
        detail {
            for (k in 0..8) { val a = PI.toFloat() * k / 8f; set((x - 8 + cos(a) * 11f).roundToInt(), (base - sin(a) * 11f).roundToInt(), c(0xC79A12)) }
            set(x - 8, base - 1, c(0xC79A12))
            for (k in 0..4) set(x + 3, base - 4 - k * 5, c(0x2F64D6))
        }
    }

    fun abacus(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val cols = intArrayOf(c(0xE53935), c(0xFB8C00), c(0xFDD835), c(0x43A047), c(0x1E88E5))
        prop {
            rect(x - 18, base - 26, 36, 3, wood); rect(x - 18, base - 3, 36, 3, wood)
            rect(x - 18, base - 26, 3, 26, woodLo); rect(x + 15, base - 26, 3, 26, woodLo)
            hline(x - 18, x + 17, base - 26, woodHi)
        }
        detail { for (r in 0 until 5) hline(x - 15, x + 14, base - 21 + r * 4, c(0x8C7A66)) }
        for (r in 0 until 5) {
            val n = 2 + (r * 3) % 5
            val shift = (r * 5) % 9
            for (k in 0 until n) prop(c(0x00000000)) {
                val bx = x - 14 + shift + k * 3
                rect(bx, base - 22 + r * 4, 3, 3, cols[r]); set(bx, base - 22 + r * 4, c(0xFFFFFF))
            }
        }
    }

    fun solids(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            // cube, isometric: top, left and right faces in three tones
            val cx = x - 12; val s = 8
            polygon(floatArrayOf(cx - s.toFloat(), base - 15f, cx.toFloat(), base - 19f, cx + s.toFloat(), base - 15f, cx.toFloat(), base - 11f), c(0xB3D1FF))
            polygon(floatArrayOf(cx - s.toFloat(), base - 15f, cx.toFloat(), base - 11f, cx.toFloat(), base.toFloat(), cx - s.toFloat(), base - 4f), c(0x6F9EF0))
            polygon(floatArrayOf(cx.toFloat(), base - 11f, cx + s.toFloat(), base - 15f, cx + s.toFloat(), base - 4f, cx.toFloat(), base.toFloat()), c(0x3F6FD0))
            // cone
            polygon(floatArrayOf(x + 1f, base.toFloat(), x + 7f, base - 22f, x + 13f, base.toFloat()), c(0xFFB74D))
            polygon(floatArrayOf(x + 7f, base - 22f, x + 13f, base.toFloat(), x + 9f, base.toFloat()), c(0xF08A24))
            ellipse(x + 7f, base - 0.5f, 6f, 1.6f, c(0xE07A18))
            // sphere
            disc(x + 21f, base - 6f, 6f, c(0xFF7AA2))
            for (yy in base - 12..base) for (xx in x + 15..x + 27) {
                val d = kotlin.math.hypot(xx + 0.5f - (x + 21) + 2f, yy + 0.5f - (base - 6) + 2f)
                if (get(xx, yy) == c(0xFF7AA2) && d > 6.5f && Bayer.threshold(xx, yy) < 0.7f) set(xx, yy, c(0xD94F7C))
            }
        }
        detail { set(x + 18, base - 9, c(0xFFFFFF)); set(x + 19, base - 9, c(0xFFC4D6)); set(x - 12, base - 18, c(0xFFFFFF)) }
    }

    // ---- biology -----------------------------------------------------------------------------------

    fun microscope(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            box(x - 12, base - 4, 22, 4, black, c(0x4A5068), c(0x1C2030))
            // the arm curves up from the base and holds the tube
            polygon(floatArrayOf(x + 2f, base - 4f, x + 7f, base - 4f, x + 8f, base - 18f, x + 4f, base - 24f, x + 1f, base - 20f, x + 4f, base - 16f), c(0x3B4158))
            rect(x - 9, base - 12, 14, 2, black)
            polygon(floatArrayOf(x - 7f, base - 15f, x - 2f, base - 31f, x + 3f, base - 29f, x - 2f, base - 13f), metal)
            polygon(floatArrayOf(x - 2f, base - 31f, x + 3f, base - 29f, x + 2f, base - 26f, x - 3f, base - 28f), metalMid)
            rect(x - 4, base - 35, 5, 4, black)
            disc(x + 7.5f, base - 13.5f, 2f, metalMid)
        }
        detail { line(x - 6, base - 16, x - 2, base - 28, white); set(x - 3, base - 11, c(0x8DF0C2)) }
    }

    fun sprout(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val leaf = c(0x4CAF50); val leafHi = c(0x8BD86A); val leafLo = c(0x2E7D32)
        prop {
            polygon(floatArrayOf(x - 8f, base - 10f, x + 9f, base - 10f, x + 6f, base.toFloat(), x - 5f, base.toFloat()), c(0xD2723C))
            rect(x - 9, base - 12, 19, 3, c(0xE58A52))
            line(x, base - 12, x, base - 30, leafLo); line(x + 1, base - 12, x + 1, base - 30, leafLo)
            for ((dy, side) in listOf(16 to -1, 21 to 1, 26 to -1)) {
                val ly = base - dy
                ellipse(x + side * 6f + 0.5f, ly.toFloat(), 6f, 2.6f, leaf)
                hline(x + side * 2, x + side * 9, ly - 1, leafHi)
            }
            disc(x + 0.5f, base - 32f, 3f, c(0xFF7AA2)); set(x, base - 33, c(0xFFD54F))
        }
        // a butterfly comes to visit
        detail {
            val bx = x + 17; val by = base - 30
            rect(bx - 3, by - 2, 3, 3, c(0xFFA726)); rect(bx + 1, by - 2, 3, 3, c(0xFFA726))
            rect(bx - 2, by + 1, 2, 2, c(0xFB8C00)); rect(bx + 1, by + 1, 2, 2, c(0xFB8C00))
            line(bx, by - 2, bx, by + 2, c(0x3A2A20)); set(bx - 1, by - 4, c(0x3A2A20)); set(bx + 1, by - 4, c(0x3A2A20))
        }
    }

    fun helix(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val top = base - 36
        for (y in top..base - 4) {
            val t = (y - top) * 0.32f
            val a = (x + sin(t) * 9f).roundToInt(); val b = (x - sin(t) * 9f).roundToInt()
            val front = cos(t) > 0
            if ((y - top) % 4 == 0) detail { hline(minOf(a, b) + 1, maxOf(a, b) - 1, y, c(0xC8D3EA)) }
            prop(c(0x00000000)) {
                rect(if (front) b else a, y, 2, 1, if (front) c(0xFF6F91) else c(0x3F7DE8))
                rect(if (front) a else b, y, 2, 1, if (front) c(0x3F7DE8) else c(0xFF6F91))
            }
        }
    }

    // ---- general science ---------------------------------------------------------------------------

    fun globe(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val cy = base - 19
        prop {
            box(x - 8, base - 3, 17, 3, wood, woodHi, woodLo)
            rect(x, base - 7, 2, 5, c(0xC9A43B))
            disc(x + 0.5f, cy + 0.5f, 11f, c(0x3E8EDE))
            // continents
            val land = c(0x5CBF5A)
            for ((lx, ly, r) in listOf(Triple(-4f, -4f, 4.2f), Triple(3f, 3f, 3.6f), Triple(-2f, 6f, 2.4f), Triple(6f, -6f, 2f))) disc(x + lx, cy + ly, r, land)
            for (yy in cy - 11..cy + 11) for (xx in x - 11..x + 12) {
                val d = kotlin.math.hypot(xx + 0.5f - x - 0.5f, yy + 0.5f - cy - 0.5f)
                if (d > 11.5f) { if (get(xx, yy) == land) set(xx, yy, c(0x3E8EDE)) }
                else if (xx > x + 3 && yy > cy - 2 && Bayer.threshold(xx, yy) < (d / 11f) * 0.8f && (get(xx, yy) == c(0x3E8EDE) || get(xx, yy) == land))
                    set(xx, yy, if (get(xx, yy) == land) c(0x3E8F48) else c(0x2C6DB8))
            }
        }
        detail {
            // the brass meridian ring, a C around the right of the globe
            for (k in -20..20) { val a = k / 20f * 1.9f; set((x + 0.5f + cos(a) * 13.5f).roundToInt(), (cy + 0.5f + sin(a) * 13.5f).roundToInt(), c(0xD8B44A)) }
            set(x - 5, cy - 7, c(0xFFFFFF)); set(x - 4, cy - 8, c(0xBFE3FF))
        }
    }

    fun volcano(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            polygon(floatArrayOf(x - 22f, base.toFloat(), x - 5f, base - 22f, x + 5f, base - 22f, x + 22f, base.toFloat()), c(0x8D5A3B))
            polygon(floatArrayOf(x + 1f, base - 22f, x + 5f, base - 22f, x + 22f, base.toFloat(), x + 9f, base.toFloat()), c(0x6E4329))
            // lava down one flank
            polygon(floatArrayOf(x - 5f, base - 22f, x + 2f, base - 22f, x - 3f, base - 12f, x - 8f, base - 5f, x - 7f, base - 13f), c(0xFF7A1A))
            hline(x - 4, x + 4, base - 22, c(0xFFC93C))
        }
        detail {
            for ((k, col) in listOf(c(0xFFC93C), c(0xFF7A1A), c(0xE53935)).withIndex()) { set(x - 2 + k * 3, base - 27 - k * 2, col); set(x + 4 - k * 4, base - 30 - k, col) }
            disc(x - 1f, base - 36f, 3.5f, c(0xD7DCE6)); disc(x + 4f, base - 40f, 4.5f, c(0xE6EAF1)); disc(x + 10f, base - 44f, 3.5f, c(0xF0F3F8))
        }
    }

    fun rocket(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val lift = 8
        detail {
            // smoke at the pad, flame under the nozzle
            for ((dx, r) in listOf(-12 to 4.5f, -5 to 5.5f, 5 to 5f, 12 to 4f)) disc(x + dx.toFloat(), base - 3f, r, c(0xE9EDF4))
            for ((dx, r) in listOf(-9 to 2.5f, 8 to 2.5f)) disc(x + dx.toFloat(), base - 6f, r, c(0xFFFFFF))
            polygon(floatArrayOf(x - 3f, base - lift - 4f, x + 4f, base - lift - 4f, x + 0.5f, base - 4f), c(0xFFC93C))
            polygon(floatArrayOf(x - 1.5f, base - lift - 4f, x + 2.5f, base - lift - 4f, x + 0.5f, base - lift + 1f), c(0xFFF6C8))
        }
        prop {
            val b = base - lift - 4
            rect(x - 4, b - 22, 9, 22, c(0xF5F7FB))
            polygon(floatArrayOf(x - 4f, b - 22f, x + 0.5f, b - 32f, x + 5f, b - 22f), c(0xE53935))
            polygon(floatArrayOf(x - 4f, b - 6f, x - 9f, b.toFloat(), x - 4f, b.toFloat()), c(0xE53935))
            polygon(floatArrayOf(x + 5f, b - 6f, x + 10f, b.toFloat(), x + 5f, b.toFloat()), c(0xE53935))
            rect(x + 3, b - 21, 2, 21, c(0xD3DAE6))
            disc(x + 0.5f, b - 14.5f, 2.4f, c(0x3FA7FF))
        }
        detail { set(x - 1, base - lift - 20, c(0xFFFFFF)) }
    }
}
