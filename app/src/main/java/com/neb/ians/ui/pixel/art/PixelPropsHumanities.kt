package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.Bayer
import com.neb.ians.ui.pixel.PixelCanvas
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Props for languages, computing, commerce, social studies, health, exams and the general set.
 * Same contract as [PixelPropsScience]: centred on x, standing on base, lit from the upper left.
 */
internal object PixelPropsHumanities {
    private val paper = c(0xFFFDF6); private val paperLo = c(0xE6DDCB); private val lineCol = c(0xB9C3D6)
    private val wood = c(0xC48E58); private val woodHi = c(0xE2B07A); private val woodLo = c(0x93613A)
    private val gold = c(0xF5C243); private val goldHi = c(0xFFE58A); private val goldLo = c(0xC98E16)
    private val white = c(0xFFFFFF); private val black = c(0x2B3044)

    // ---- languages ---------------------------------------------------------------------------------

    fun openBook(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            polygon(floatArrayOf(x - 22f, base - 2f, x - 21f, base - 16f, x.toFloat(), base - 13f, x + 21f, base - 16f, x + 22f, base - 2f, x.toFloat(), base.toFloat()), c(0x2F64D6))
            polygon(floatArrayOf(x - 20f, base - 4f, x - 19f, base - 17f, x - 1f, base - 14f, x - 1f, base - 1f), paper)
            polygon(floatArrayOf(x + 1f, base - 1f, x + 1f, base - 14f, x + 19f, base - 17f, x + 20f, base - 4f), paper)
            line(x, base - 14, x, base - 1, paperLo)
        }
        detail {
            for (k in 0 until 5) { line(x - 17, base - 14 + k * 2, x - 4, base - 12 + k * 2, lineCol); line(x + 4, base - 12 + k * 2, x + 17 - (k % 2) * 4, base - 14 + k * 2, lineCol) }
        }
        // a quill in an inkwell beside it
        prop {
            rect(x + 24, base - 6, 7, 6, c(0x2B3044)); rect(x + 25, base - 7, 5, 1, c(0x4A5068))
            polygon(floatArrayOf(x + 27f, base - 7f, x + 33f, base - 26f, x + 36f, base - 25f, x + 29f, base - 9f), c(0xF5F1E6))
        }
        detail { line(x + 28, base - 8, x + 34, base - 25, c(0xC9C0AE)) }
    }

    fun bookStack(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val books = listOf(Triple(c(0xD9534F), 24, 0), Triple(c(0x3D7DD8), 22, 2), Triple(c(0xF0AD4E), 25, -1), Triple(c(0x5CB85C), 20, 1))
        prop {
            var y = base
            for ((col, w, off) in books) {
                rect(x - w / 2 + off, y - 5, w, 5, col)
                rect(x - w / 2 + off + 1, y - 4, w - 3, 3, paper)
                hline(x - w / 2 + off, x + w / 2 + off - 1, y - 5, com.neb.ians.ui.pixel.Px.mix(col, white, 0.35f))
                y -= 5
            }
            // an apple on top
            disc(x + 2f, y - 3.5f, 3.6f, c(0xE53935))
            set(x + 2, y - 8, c(0x6D4C41)); set(x + 3, y - 8, c(0x43A047)); set(x + 4, y - 9, c(0x43A047))
        }
        detail { set(x + 1, base - 24, white) }
    }

    /** Wooden letter blocks: an English A, a Devanagari क, and a B. */
    fun letterBlocks(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val glyphA = arrayOf(".111.", "1...1", "11111", "1...1", "1...1")
        val glyphB = arrayOf("1111.", "1...1", "1111.", "1...1", "1111.")
        val glyphKa = arrayOf("11111", "..1..", "1111.", "1.1.1", ".11..", "..1..")
        val blocks = listOf(Triple(x - 14, base, glyphA to c(0xE53935)), Triple(x + 1, base, glyphKa to c(0x2F64D6)), Triple(x - 6, base - 13, glyphB to c(0x2E9E4F)))
        for ((bx, by, g) in blocks) {
            prop { box(bx - 6, by - 13, 13, 13, c(0xF2D3A2), c(0xFBE7C6), c(0xD9B07A)); rect(bx - 4, by - 11, 9, 9, c(0xFFF4E0)) }
            detail {
                val rows = g.first
                for (r in rows.indices) for (k in 0 until 5) if (rows[r][k] == '1') set(bx - 2 + k, by - 10 + r + (if (rows.size == 5) 1 else 0), g.second)
            }
        }
    }

    // ---- computing ---------------------------------------------------------------------------------

    fun laptop(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            rect(x - 16, base - 25, 32, 21, c(0x3B4158))
            rect(x - 14, base - 23, 28, 17, c(0x14192B))
            polygon(floatArrayOf(x - 20f, base - 4f, x + 20f, base - 4f, x + 22f, base.toFloat(), x - 22f, base.toFloat()), c(0xC9D1E0))
            hline(x - 4, x + 4, base - 2, c(0x9AA4B8))
        }
        detail {
            val cols = intArrayOf(c(0xFF79C6), c(0x8BE9FD), c(0x50FA7B), c(0xF1FA8C), c(0xBD93F9))
            val lens = intArrayOf(10, 16, 8, 19, 12, 6)
            for (k in lens.indices) {
                val ind = if (k in 1..3) 3 else 0
                hline(x - 12 + ind, x - 12 + ind + 2, base - 21 + k * 2, cols[k % cols.size])
                hline(x - 12 + ind + 4, x - 12 + ind + lens[k], base - 21 + k * 2, c(0xC8D0E8))
            }
            set(x - 12 + 13, base - 9, c(0xFFFFFF))
        }
    }

    fun robot(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val body = c(0xD7DEEA); val bodyLo = c(0xA9B4C8); val accent = c(0xFF6F61)
        prop {
            rect(x - 8, base - 3, 6, 3, bodyLo); rect(x + 3, base - 3, 6, 3, bodyLo)
            rect(x - 6, base - 6, 3, 3, c(0x7F8BA6)); rect(x + 4, base - 6, 3, 3, c(0x7F8BA6))
            box(x - 9, base - 18, 19, 12, body, white, bodyLo)
            rect(x - 3, base - 15, 7, 5, c(0x3B4158))
            box(x - 7, base - 30, 15, 11, body, white, bodyLo)
            rect(x - 5, base - 27, 11, 5, c(0x14192B))
            rect(x, base - 33, 1, 3, c(0x7F8BA6))
            // arms: one waving
            rect(x - 13, base - 17, 4, 3, bodyLo); rect(x - 14, base - 17, 2, 8, bodyLo)
            rect(x + 10, base - 17, 4, 3, bodyLo); rect(x + 13, base - 24, 2, 9, bodyLo)
        }
        detail {
            rect(x - 4, base - 26, 3, 2, c(0x5CF2FF)); rect(x + 2, base - 26, 3, 2, c(0x5CF2FF))
            set(x, base - 34, accent); set(x - 1, base - 13, accent); set(x + 1, base - 13, c(0x50FA7B)); set(x + 3, base - 13, c(0xF1FA8C))
        }
    }

    fun terminal(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            rect(x - 15, base - 30, 30, 24, c(0xE6E0D2)); rect(x - 15, base - 30, 30, 2, c(0xF6F1E6))
            rect(x - 12, base - 27, 24, 17, c(0x0F2A1D))
            rect(x - 6, base - 6, 12, 2, c(0xC9C1AE)); rect(x - 18, base - 4, 36, 4, c(0xD9D2C2))
        }
        detail {
            val green = c(0x4BF08B); val dim = c(0x2BA35D)
            hline(x - 10, x - 9, base - 24, green); hline(x - 7, x + 4, base - 24, dim)
            hline(x - 10, x - 9, base - 20, green); hline(x - 7, x + 7, base - 20, dim)
            hline(x - 10, x - 9, base - 16, green); rect(x - 7, base - 17, 2, 3, green)
            for (k in 0 until 9) set(x - 16 + k * 4, base - 3, c(0xB4AC98))
        }
    }

    // ---- commerce ----------------------------------------------------------------------------------

    fun growth(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val bars = intArrayOf(8, 13, 11, 19, 25)
        val cols = intArrayOf(c(0x7FB2FF), c(0x5A8BEA), c(0x7FB2FF), c(0x2F9E6B), c(0x2FB36B))
        prop {
            for ((i, h) in bars.withIndex()) box(x - 20 + i * 7, base - h, 5, h, cols[i], c(0xFFFFFF), cols[i])
            // a stack of coins at the side
            for (k in 0 until 4) { ellipse(x + 20f, base - 2f - k * 2.5f, 4.5f, 1.8f, gold); hline(x + 16, x + 24, (base - 1f - k * 2.5f).roundToInt(), goldLo) }
        }
        detail {
            // the trend arrow
            line(x - 19, base - 13, x - 5, base - 18, c(0xE53935)); line(x - 5, base - 18, x + 1, base - 15, c(0xE53935)); line(x + 1, base - 15, x + 12, base - 30, c(0xE53935))
            set(x + 12, base - 30, c(0xE53935)); set(x + 10, base - 30, c(0xE53935)); set(x + 12, base - 28, c(0xE53935)); set(x + 11, base - 30, c(0xE53935)); set(x + 12, base - 29, c(0xE53935))
            set(x + 18, base - 11, goldHi)
        }
    }

    fun calculator(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            // a ledger first, then the calculator on it
            polygon(floatArrayOf(x - 22f, base.toFloat(), x - 18f, base - 6f, x + 16f, base - 6f, x + 20f, base.toFloat()), paper)
            box(x - 8, base - 26, 18, 24, c(0x3B4158), c(0x5A6178), c(0x262B3D))
            rect(x - 6, base - 24, 14, 5, c(0xB9E8C9))
        }
        detail {
            for (r in 0 until 4) for (k in 0 until 4) rect(x - 6 + k * 4, base - 17 + r * 4, 2, 2, if (k == 3) c(0xFF9F43) else c(0xD7DEEA))
            hline(x - 4, x + 6, base - 21, c(0x2E5E44)); set(x + 6, base - 23, c(0x2E5E44))
            for (k in 0 until 3) hline(x - 18 + k, x - 10, base - 4 + 0 * k, lineCol)
        }
    }

    fun piggy(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val pink = c(0xFF9EB8); val pinkLo = c(0xE57A98); val pinkHi = c(0xFFC7D6)
        prop {
            rect(x - 8, base - 4, 3, 4, pinkLo); rect(x + 5, base - 4, 3, 4, pinkLo)
            ellipse(x + 0.5f, base - 11f, 13f, 9f, pink)
            for (yy in base - 20..base - 2) for (xx in x - 13..x + 14) if (get(xx, yy) == pink && yy > base - 8 && Bayer.threshold(xx, yy) < 0.6f) set(xx, yy, pinkLo)
            ellipse(x + 13.5f, base - 11f, 3f, 3.2f, pinkHi)
            polygon(floatArrayOf(x + 5f, base - 18f, x + 8f, base - 24f, x + 10f, base - 17f), pinkLo)
        }
        detail {
            set(x + 13, base - 12, pinkLo); set(x + 14, base - 10, pinkLo)
            set(x + 7, base - 14, black)
            hline(x - 3, x + 2, base - 19, c(0x9C3B5A))
            line(x - 14, base - 12, x - 16, base - 15, pinkLo)
            // a coin on its way in
            ellipse(x - 0.5f, base - 27f, 3f, 3f, gold); set(x - 1, base - 28, goldHi)
        }
    }

    // ---- social studies ----------------------------------------------------------------------------

    /** A five-tiered pagoda in the style of Bhaktapur's Nyatapola. */
    fun pagoda(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val brick = c(0xB5523A); val brickLo = c(0x8C3B29); val roof = c(0x4A3B33); val roofHi = c(0x7A6253)
        prop {
            for (k in 0 until 3) rect(x - 15 + k * 2, base - 2 - k * 2, 31 - k * 4, 2, c(0xC9B79C))
            var y = base - 6
            var hw = 9
            for (t in 0 until 5) {
                rect(x - hw + 3, y - 4, hw * 2 - 5, 4, if (t == 0) brick else brickLo)
                polygon(floatArrayOf(x - hw - 3f, y - 4f, x - hw + 1f, y - 8f, x + hw - 0f, y - 8f, x + hw + 4f, y - 4f), roof)
                hline(x - hw + 1, x + hw, y - 8, roofHi)
                y -= 8; hw -= 1
            }
            rect(x, y - 4, 1, 4, gold)
            disc(x + 0.5f, y - 5f, 1.5f, gold)
        }
        detail { for (t in 0 until 5) set(x - 11 + t, base - 10 - t * 8, gold); for (t in 0 until 5) set(x + 12 - t, base - 10 - t * 8, gold) }
    }

    /** Boudhanath: the white dome, the gilded harmika with the Buddha's eyes, prayer flags. */
    fun stupa(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val flags = intArrayOf(c(0x2F64D6), c(0xFFFFFF), c(0xE53935), c(0x2E9E4F), c(0xFDD835))
        detail {
            for (side in intArrayOf(-1, 1)) {
                for (k in 0 until 14) {
                    val fx = x + side * (3 + k * 2); val fy = base - 30 + (k * k * 0.12f).roundToInt()
                    rect(fx, fy, 2, 2, flags[k % flags.size]); set(fx, fy - 1, c(0xB8B0A0))
                }
            }
        }
        prop {
            for (k in 0 until 3) rect(x - 20 + k * 2, base - 3 - k * 2, 41 - k * 4, 2, c(0xF4F1EA))
            ellipse(x + 0.5f, base - 8f, 13f, 8f, c(0xFAFAF7))
            for (yy in base - 16..base - 7) for (xx in x - 13..x + 14) if (get(xx, yy) == c(0xFAFAF7) && xx > x + 4 && Bayer.threshold(xx, yy) < 0.45f) set(xx, yy, c(0xDCD8CE))
            rect(x - 4, base - 21, 9, 6, gold)
            polygon(floatArrayOf(x - 3f, base - 21f, x + 0.5f, base - 34f, x + 4f, base - 21f), gold)
            for (k in 0 until 5) hline(x - 3 + k / 2, x + 3 - k / 2, base - 23 - k * 2, goldLo)
            disc(x + 0.5f, base - 35f, 1.3f, goldHi)
        }
        detail {
            // the eyes, and the nose shaped like the number one in Nepali
            hline(x - 3, x - 1, base - 19, black); hline(x + 1, x + 3, base - 19, black)
            set(x - 2, base - 18, c(0x2F64D6)); set(x + 2, base - 18, c(0x2F64D6))
            set(x, base - 17, c(0x2F64D6))
        }
    }

    fun map(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val panels = intArrayOf(c(0xFFF7E3), c(0xF3E7CA), c(0xFFF7E3))
        prop {
            for (i in 0 until 3) {
                val px = x - 21 + i * 14
                val skew = if (i % 2 == 0) 0f else 2f
                polygon(floatArrayOf(px.toFloat(), base - 22f + skew, px + 14f, base - 22f + 2f - skew, px + 14f, base.toFloat() - skew + 2f - 2f, px.toFloat(), base.toFloat() - skew), panels[i])
            }
        }
        detail {
            // land, a river, a dashed route and a pin
            for ((cx, cy, r) in listOf(Triple(x - 13f, base - 13f, 5f), Triple(x + 6f, base - 8f, 4f), Triple(x + 10f, base - 16f, 3f))) {
                for (yy in (cy - r).toInt()..(cy + r).toInt()) for (xx in (cx - r - 1).toInt()..(cx + r + 1).toInt())
                    if (kotlin.math.hypot(xx - cx, (yy - cy) * 1.3f) < r && get(xx, yy) in panels) set(xx, yy, c(0x9ED67A))
            }
            for (xx in x - 20 until x + 21) { val yy = (base - 4 - sin(xx * 0.3f) * 1.5f).roundToInt(); if (get(xx, yy) in panels || get(xx, yy) == c(0x9ED67A)) set(xx, yy, c(0x5AA9F0)) }
            for (k in 0 until 7) set(x - 14 + k * 4, base - 13 + (k % 3) - k / 2, c(0xE53935))
            disc(x + 10.5f, base - 25f, 2.4f, c(0xE53935)); line(x + 10, base - 23, x + 10, base - 18, c(0x6B7280)); set(x + 10, base - 26, c(0xFF9A9D))
        }
    }

    // ---- health ------------------------------------------------------------------------------------

    fun football(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val cx = x + 0.5f; val cy = base - 10f
        prop {
            disc(cx, cy, 10f, white)
            for (yy in base - 20..base) for (xx in x - 10..x + 11) if (get(xx, yy) == white && kotlin.math.hypot(xx + 0.5f - cx + 3f, yy + 0.5f - cy + 3f) > 11f && Bayer.threshold(xx, yy) < 0.6f) set(xx, yy, c(0xD5DCE8))
        }
        detail {
            // the pentagons
            for ((px, py, r) in listOf(Triple(0f, 0f, 3f), Triple(-7f, -3f, 2f), Triple(6f, -5f, 2f), Triple(-3f, 7f, 2f), Triple(7f, 5f, 2f))) disc(cx + px, cy + py, r, black)
            for (k in 0 until 3) hline(x - 26 + k * 2, x - 16, base - 14 + k * 4, c(0xE9EEF6))
        }
    }

    fun heart(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val red = c(0xE53950); val redLo = c(0xB71C3C)
        prop {
            disc(x - 5f, base - 19f, 7f, red); disc(x + 6f, base - 19f, 7f, red)
            polygon(floatArrayOf(x - 12f, base - 17f, x + 13f, base - 17f, x + 0.5f, base - 2f), red)
            for (yy in base - 26..base) for (xx in x - 12..x + 13) if (get(xx, yy) == red && xx > x + 3 && yy > base - 18 && Bayer.threshold(xx, yy) < 0.6f) set(xx, yy, redLo)
        }
        detail {
            rect(x - 8, base - 23, 3, 2, c(0xFF9AA8)); set(x - 9, base - 21, c(0xFF9AA8))
            // a pulse line across
            val pts = listOf(-30 to 0, -12 to 0, -9 to -6, -6 to 6, -3 to -10, 0 to 4, 3 to 0, 30 to 0)
            for (i in 0 until pts.size - 1) line(x + pts[i].first, base - 14 + pts[i].second, x + pts[i + 1].first, base - 14 + pts[i + 1].second, c(0xFFFFFF))
        }
    }

    fun fitness(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            rect(x - 18, base - 4, 22, 2, c(0x8692AB))
            for (dx in intArrayOf(-19, -16, 1, 4)) rect(x + dx, base - 9, 3, 10, c(0x3B4158))
            disc(x + 14f, base - 8f, 7.5f, c(0x7CC24A))
            rect(x + 14, base - 18, 1, 3, c(0x6D4C41))
            polygon(floatArrayOf(x + 15f, base - 17f, x + 20f, base - 20f, x + 19f, base - 16f), c(0x43A047))
        }
        detail { set(x + 11, base - 11, c(0xD8F5B8)); set(x + 10, base - 10, c(0xB8E68A)); set(x - 18, base - 8, c(0x6B7390)); set(x + 1, base - 8, c(0x6B7390)) }
    }

    // ---- exams -------------------------------------------------------------------------------------

    fun stopwatch(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val cy = base - 13
        prop {
            rect(x - 1, cy - 16, 3, 3, c(0x8692AB)); rect(x - 3, cy - 17, 7, 2, c(0xB4C0D4))
            disc(x + 0.5f, cy + 0.5f, 12.5f, c(0xE53935))
            disc(x + 0.5f, cy + 0.5f, 10f, white)
        }
        detail {
            for (k in 0 until 12) { val a = k * Math.PI.toFloat() / 6f; set((x + 0.5f + kotlin.math.cos(a) * 8.5f).roundToInt(), (cy + 0.5f + sin(a) * 8.5f).roundToInt(), c(0x9AA4B8)) }
            line(x, cy, x, cy - 7, black); line(x, cy, x + 5, cy + 2, c(0xE53935))
            set(x - 6, cy - 6, c(0xFFFFFF)); for (k in 0 until 3) line(x - 22 + k, cy - 6 + k * 5, x - 16, cy - 6 + k * 5, c(0xE9EEF6))
        }
    }

    fun answerSheet(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            polygon(floatArrayOf(x - 16f, base - 1f, x - 12f, base - 30f, x + 12f, base - 28f, x + 10f, base + 1f), paper)
        }
        detail {
            for (k in 0 until 7) line(x - 11, base - 24 + k * 3, x + 6, base - 23 + k * 3, lineCol)
            // a red A+ in a circle
            val gx = x + 3; val gy = base - 22
            for (a in 0 until 20) { val t = a * Math.PI.toFloat() / 10f; set((gx + kotlin.math.cos(t) * 6f).roundToInt(), (gy + sin(t) * 5f).roundToInt(), c(0xE53935)) }
            val glyph = arrayOf(".1...", "1.1.1", "111.1", "1.1..")
            for (r in glyph.indices) for (k in 0 until 5) if (glyph[r][k] == '1') set(gx - 3 + k, gy - 2 + r, c(0xE53935))
            set(gx + 1, gy - 1, c(0xE53935)); set(gx + 3, gy - 1, c(0xE53935))
        }
        prop {
            // the pencil
            polygon(floatArrayOf(x + 14f, base - 4f, x + 28f, base - 26f, x + 31f, base - 24f, x + 17f, base - 2f), c(0xFFC93C))
            polygon(floatArrayOf(x + 14f, base - 4f, x + 17f, base - 2f, x + 13f, base.toFloat()), c(0xF2D3A2))
            polygon(floatArrayOf(x + 28f, base - 26f, x + 31f, base - 24f, x + 32f, base - 27f, x + 30f, base - 28f), c(0xFF8FA3))
        }
    }

    fun trophy(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            box(x - 8, base - 4, 17, 4, c(0x6D4C41), c(0x8D6E63), c(0x4E342E))
            rect(x - 2, base - 10, 5, 6, gold)
            polygon(floatArrayOf(x - 10f, base - 28f, x + 11f, base - 28f, x + 8f, base - 16f, x + 0.5f, base - 11f, x - 7f, base - 16f), gold)
            for (yy in base - 28..base - 11) for (xx in x..x + 11) if (get(xx, yy) == gold && Bayer.threshold(xx, yy) < 0.55f) set(xx, yy, goldLo)
            for (s in intArrayOf(-1, 1)) { val hx = if (s < 0) x - 14 else x + 11; rect(hx, base - 26, 4, 2, gold); rect(hx + (if (s < 0) 0 else 2), base - 26, 2, 7, gold); rect(hx, base - 21, 4, 2, gold) }
        }
        detail {
            line(x - 6, base - 26, x - 4, base - 17, goldHi)
            // a star on the cup
            set(x + 1, base - 24, white); hline(x - 1, x + 3, base - 23, c(0xFFF6C8)); set(x + 1, base - 22, c(0xFFF6C8)); set(x, base - 21, c(0xFFF6C8)); set(x + 2, base - 21, c(0xFFF6C8))
            for ((sx, sy) in listOf(-16 to -32, 17 to -30, -19 to -14)) { set(x + sx, base + sy, goldHi); set(x + sx - 1, base + sy, gold); set(x + sx + 1, base + sy, gold) }
        }
    }

    // ---- general -----------------------------------------------------------------------------------

    fun deskLamp(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            box(x - 20, base - 4, 18, 4, c(0x3D7DD8), c(0x7FB2FF), c(0x2A5BB0))
            box(x - 18, base - 8, 15, 4, c(0xF0AD4E), c(0xFFD08A), c(0xC98A2A))
            box(x + 2, base - 3, 14, 3, c(0x3B4158), c(0x5A6178), c(0x262B3D))
            line(x + 9, base - 3, x + 4, base - 18, c(0x3B4158)); line(x + 10, base - 3, x + 5, base - 18, c(0x3B4158))
            line(x + 4, base - 18, x + 14, base - 26, c(0x3B4158)); line(x + 5, base - 18, x + 15, base - 26, c(0x3B4158))
            polygon(floatArrayOf(x + 10f, base - 28f, x + 20f, base - 30f, x + 22f, base - 21f, x + 16f, base - 20f), c(0x2E9E8A))
        }
        detail {
            for (yy in base - 20..base - 5) for (xx in x + 4..x + 26) {
                val t = (yy - (base - 20)) / 15f
                if (xx > x + 14 - t * 8 && xx < x + 21 + t * 6 && Bayer.threshold(xx, yy) < 0.18f && (get(xx, yy) ushr 24) != 0) set(xx, yy, c(0xFFF2B8))
            }
            hline(x + 16, x + 21, base - 21, c(0xFFF2B8))
        }
    }

    fun backpack(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val blue = c(0x3F7DE8); val blueLo = c(0x2A5BB0); val blueHi = c(0x7FB2FF)
        prop {
            rect(x - 5, base - 31, 11, 3, blueLo)
            roundRect(x - 11, base - 28, 23, 28, 4, blue)
            for (yy in base - 28..base) for (xx in x + 5..x + 12) if (get(xx, yy) == blue && Bayer.threshold(xx, yy) < 0.6f) set(xx, yy, blueLo)
            roundRect(x - 8, base - 13, 17, 11, 3, c(0xFFC93C))
            hline(x - 7, x + 7, base - 13, c(0xFFE08A))
        }
        detail {
            hline(x - 8, x + 8, base - 9, c(0xC98E16)); set(x, base - 8, c(0x8692AB))
            line(x - 9, base - 26, x - 9, base - 15, blueHi)
            set(x - 3, base - 30, c(0x1A3C80)); set(x + 3, base - 30, c(0x1A3C80))
        }
    }

    fun paperPlane(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        val py = base - 22
        detail {
            // a looping dashed trail behind it
            for (k in 0 until 26) {
                val t = k / 26f * 6.2f
                val tx = (x - 46 + k * 1.6f + sin(t) * 4f).roundToInt(); val ty = (py + 8 + kotlin.math.cos(t) * 6f).roundToInt()
                if (k % 2 == 0) set(tx, ty, c(0x9FB4D6))
            }
        }
        prop {
            polygon(floatArrayOf(x - 14f, py + 8f, x + 16f, py - 6f, x - 2f, py + 12f), white)
            polygon(floatArrayOf(x - 2f, py + 12f, x + 16f, py - 6f, x + 1f, py + 7f), c(0xD3DDF0))
            polygon(floatArrayOf(x - 2f, py + 12f, x + 1f, py + 7f, x.toFloat(), py + 14f), c(0xAFBEDB))
        }
    }

}
