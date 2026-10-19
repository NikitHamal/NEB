package com.neb.ians.ui.pixel

import com.neb.ians.ui.pixel.PixelNeby.Geo
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Neby's wardrobe. A look is drawn in three passes around the body: [NebyLooks.back] before it
 * (jamara, a helmet's glass, a headphone band), [NebyLooks.front] on top of the face but before
 * the outline (hats, garlands, tika), and [NebyLooks.detail] after the outline for single-pixel
 * work that a 1 px outline would smother (rice grains, tassels, glints). Everything is placed from
 * the pose's [Geo], so a hat squashes, stretches, tilts and hops with Neby.
 *
 * [key] is the name the server and the web use. [theme] ties a look to a site theme, so Neby
 * dresses for the festival that is on unless an admin picks a look.
 */
enum class NebyLook(val key: String, val label: String, val festival: Boolean = false, val hat: Boolean = false, val theme: String? = null) {
    Classic("classic", "Classic"),
    Dashain("dashain", "Dashain", festival = true, hat = true, theme = "dashain"),
    Tihar("tihar", "Tihar", festival = true, theme = "tihar"),
    Holi("holi", "Holi", festival = true, theme = "holi"),
    Teej("teej", "Teej", festival = true),
    Losar("losar", "Losar", festival = true, hat = true),
    NewYear("new-year", "Nepali New Year", festival = true, hat = true, theme = "new-year"),
    Christmas("christmas", "Christmas", festival = true, hat = true),
    Monsoon("monsoon", "Monsoon", hat = true, theme = "monsoon"),
    Winter("winter", "Winter", hat = true, theme = "winter"),
    Topi("topi", "Dhaka topi", hat = true),
    Graduate("graduate", "Graduate", hat = true, theme = "exams"),
    Astronaut("astronaut", "Astronaut", hat = true),
    Wizard("wizard", "Wizard", hat = true),
    Headphones("headphones", "Headphones", hat = true),
    Scientist("scientist", "Scientist"),
    Ninja("ninja", "Ninja"),
    Night("night", "Night cap", hat = true),
    Crown("crown", "Champion", hat = true);

    companion object {
        fun fromKey(key: String?): NebyLook = entries.firstOrNull { it.key == key } ?: Classic

        /** The look a site theme dresses Neby in; everyday and unknown themes keep the classic look. */
        fun forTheme(theme: String?): NebyLook = entries.firstOrNull { it.theme != null && it.theme == theme } ?: Classic
    }
}

/** What Neby wears app-wide, set from the server's site theme (an admin's pick or the festival's dress). */
object NebyDress {
    @Volatile var current: NebyLook = NebyLook.Classic
}

object NebyLooks {
    private fun c(hex: Long) = Px.rgb(hex)

    // tika and jamara
    private val tikaRed = c(0xD7263D); private val tikaLo = c(0xA51C30); private val rice = c(0xFFF6DE)
    private val jamara = c(0xE3DC5C); private val jamaraLo = c(0xB9C23A); private val jamaraHi = c(0xF7F3B0)
    // flowers and lights
    private val marigold = c(0xFF9F1C); private val marigoldHi = c(0xFFD23F); private val makhamali = c(0xB0306A)
    private val gold = c(0xF2C230); private val goldLo = c(0xC98E16); private val goldHi = c(0xFFE58A)
    private val white = c(0xFFFFFF); private val ink = c(0x1E2A4A)
    private val crimson = c(0xDC143C); private val crimsonLo = c(0xA30E2C); private val nepalBlue = c(0x003893)
    private val gulal = intArrayOf(c(0xFF4FA3), c(0x2DCB73), c(0xFFD23F), c(0x9B5DE5), c(0xFF8C42), c(0x3FA7FF))
    private val rainbow = intArrayOf(c(0xE53935), c(0xFB8C00), c(0xFDD835), c(0x43A047), c(0x1E88E5), c(0x3949AB), c(0x8E24AA))

    /** Band palette (band, highlight, low, wave): blue for Neby, red for Teej. */
    fun band(look: NebyLook): IntArray = when (look) {
        NebyLook.Teej -> intArrayOf(c(0xC8203A), c(0xE8475E), c(0x9C1830), c(0xF4A0AE))
        else -> intArrayOf(PixelNeby.band, PixelNeby.bandHi, PixelNeby.bandLo, PixelNeby.wave)
    }

    // ---- pass 1: behind the body ------------------------------------------------------------------

    fun back(cv: PixelCanvas, g: Geo) = with(cv) {
        val p = g.pose
        if (p.jamara || p.look == NebyLook.Dashain) jamaraClump(this, g)
        when (p.look) {
            NebyLook.Astronaut -> {
                // the glass of the helmet shows as a pale rim around the head, the collar below
                ellipse(g.cx, g.cy - 0.5f, g.rx + 3f, g.ry + 3f, c(0xE6F0FF))
                ellipse(g.cx, g.cy + g.ry - 1f, g.rx * 0.8f, 3f, c(0xB4BECE))
            }
            NebyLook.Headphones -> {
                // the band arcs over the head, two pixels thick
                for (a in 0..40) {
                    val t = PI * a / 40.0
                    val x = g.cx - (g.rx + 1.5f) * kotlin.math.cos(t).toFloat()
                    val y = g.cy - 3f - (g.ry + 1.5f) * sin(t).toFloat()
                    rect(x.roundToInt(), y.roundToInt(), 2, 2, c(0x2A2F45))
                }
            }
            else -> Unit
        }
    }

    private fun jamaraClump(cv: PixelCanvas, g: Geo) = with(cv) {
        // a tuft of barley shoots fanning out from behind the ear, each blade two pixels wide
        val bx = g.cx + g.rx * 0.5f; val by = g.top + 6f
        val sway = sin(g.pose.phase * 0.7f) * 0.8f
        for (k in 0 until 6) {
            val o = k - 2.5f
            val tx = (bx + o * 2.2f + sway * (0.5f + k * 0.15f)).roundToInt()
            val ty = (by - 10f - (k % 3) * 1.5f + kotlin.math.abs(o) * 0.8f).roundToInt()
            line((bx + o * 0.6f).roundToInt(), by.roundToInt(), tx, ty, jamara)
            line((bx + o * 0.6f).roundToInt() + 1, by.roundToInt(), tx + 1, ty, if (k % 2 == 0) jamara else jamaraLo)
        }
    }

    // ---- pass 2: on the body, outlined with it ------------------------------------------------------

    fun front(cv: PixelCanvas, g: Geo) = with(cv) {
        val p = g.pose
        val t = g.top
        val cx = g.cx; val cxi = cx.roundToInt()
        if (p.tika || p.look == NebyLook.Dashain) tika(this, g)
        if (p.paint > 0f || p.look == NebyLook.Holi) splashes(this, g, if (p.look == NebyLook.Holi) 1f else p.paint)
        when (p.look) {
            NebyLook.Tihar -> {
                garland(this, g)
                // Bhai Tika: seven colours side by side down the forehead
                val y0 = (g.cy - 13f).roundToInt()
                for (i in 0 until 7) for (k in 0 until 4) if (!(k == 0 && (i == 0 || i == 6))) set(cxi - 3 + i, y0 + k, rainbow[i])
            }
            NebyLook.Teej -> {
                // green pote with a gold tilhari, a red bindi, a hibiscus in the hair
                beads(this, g, intArrayOf(c(0x2E9E4F), c(0x7ED957)), 2)
                val by = (g.bandTop + 4f).roundToInt()
                rect(cxi - 1, by, 3, 4, gold); set(cxi, by + 1, goldHi)
                rect(cxi, (g.cy - 11f).roundToInt(), 2, 2, tikaRed)
                flower(this, cx - g.rx * 0.6f, t + 3f, c(0xE53950), c(0xFFD23F))
            }
            NebyLook.Losar -> {
                // a fur-brimmed hat: red crown, gold brocade, cream fur
                ellipse(cx, t + 0.5f, 9f, 5f, c(0xB3202E))
                hline(cxi - 8, cxi + 8, (t + 1.5f).roundToInt(), gold)
                for (x in cxi - 7..cxi + 7 step 3) set(x, (t - 1f).roundToInt(), gold)
                disc(cx, t - 4.5f, 1.6f, gold)
                fur(this, cx, t + 3f, 14f, 3f)
            }
            NebyLook.NewYear -> {
                // a party hat in the flag's crimson and blue, leaning a little
                cone(this, cx + 1f, t + 3f, 7f, cx + 4f, t - 8f, crimson, nepalBlue)
                disc(cx + 4f, t - 8.5f, 1.8f, gold)
                flower(this, cx - g.rx * 0.62f, t + 4f, crimson, c(0xFFE0E6)) // lali gurans
            }
            NebyLook.Christmas -> {
                // a floppy Santa hat whose point falls to the right
                polygon(floatArrayOf(cx - 12f, t + 4f, cx - 4f, t - 8f, cx + 6f, t - 9f, cx + 14f, t - 3f, cx + 12f, t + 4f), c(0xD62839))
                polygon(floatArrayOf(cx + 4f, t - 8f, cx + 11f, t - 7f, cx + 15f, t - 1f, cx + 10f, t - 4f), c(0xA71D2C))
                fur(this, cx, t + 4f, 14f, 2.5f)
                disc(cx + 15f, t, 2.6f, white)
            }
            NebyLook.Monsoon -> {
                // a yellow rain hat with a wide brim
                ellipse(cx, t - 1f, 9f, 6f, c(0xFFC531))
                ellipse(cx, t + 3f, 16f, 3f, c(0xF0A800))
                hline(cxi - 8, cxi + 8, (t + 1f).roundToInt(), c(0xD89200))
            }
            NebyLook.Winter -> {
                // a knitted beanie with a pompom, and a striped scarf
                val y1 = (t + 7f).roundToInt()
                for (y in (t - 1f).roundToInt()..y1) {
                    val hw = g.halfWidth(y.toFloat()).coerceAtLeast(if (y < t + 1f) 6f else 0f) + 1f
                    for (x in (cx - hw).roundToInt()..(cx + hw).roundToInt()) set(x, y, if (y >= y1 - 2) c(0xF2828C) else if ((x + 100) % 3 == 0) c(0xC23A48) else c(0xE04E5A))
                }
                disc(cx, t - 3f, 3f, c(0xFFF1F2))
                scarf(this, g)
            }
            NebyLook.Topi -> topi(this, g)
            NebyLook.Graduate -> {
                rect(cxi - 7, (t - 1f).roundToInt(), 15, 4, c(0x262B3D))
                polygon(floatArrayOf(cx - 15f, t - 2f, cx, t - 7f, cx + 15f, t - 2f, cx, t + 2f), c(0x1A1F2E))
            }
            NebyLook.Wizard -> {
                ellipse(cx, t + 3f, 15f, 2.6f, c(0x4A32A0))
                polygon(floatArrayOf(cx - 8f, t + 2f, cx - 3f, t - 7f, cx - 7f, t - 10.5f, cx + 1f, t - 8f, cx + 8f, t + 2f), c(0x5B3FB5))
                hline(cxi - 7, cxi + 7, (t + 1f).roundToInt(), gold)
            }
            NebyLook.Headphones -> {
                for (s in intArrayOf(-1, 1)) {
                    val x = if (s < 0) (cx - g.rx - 2f).roundToInt() else (cx + g.rx - 3f).roundToInt()
                    roundRect(x, (g.cy - 9f).roundToInt(), 5, 10, 2, c(0xFF5A5F))
                    rect(x + 1, (g.cy - 7f).roundToInt(), 1, 5, c(0xFF9A9D))
                }
            }
            NebyLook.Scientist -> {
                val gy = (t + 6f).roundToInt()
                for (y in gy..gy + 1) { val hw = g.halfWidth(y.toFloat()); hline((cx - hw).roundToInt(), (cx + hw).roundToInt(), y, c(0x3B4256)) }
                for (s in intArrayOf(-1, 1)) { disc(cx + s * 5.5f, gy + 1f, 3.6f, c(0x6B7A90)); disc(cx + s * 5.5f, gy + 1f, 2.4f, c(0xA8E6FF)) }
            }
            NebyLook.Ninja -> {
                val y0 = (g.cy - 13f).roundToInt()
                for (y in y0..y0 + 2) { val hw = g.halfWidth(y.toFloat()) + 0.5f; hline((cx - hw).roundToInt(), (cx + hw).roundToInt(), y, c(0xD7263D)) }
                // the knot's tails stream out behind
                val w = sin(p.phase * 1.3f) * 1.5f
                val kx = (cx + g.rx).roundToInt()
                polygon(floatArrayOf(kx - 1f, y0 + 0f, kx + 7f, y0 - 2f + w, kx + 8f, y0 + 0f + w, kx - 1f, y0 + 2f), c(0xD7263D))
                polygon(floatArrayOf(kx - 1f, y0 + 1f, kx + 6f, y0 + 4f - w, kx + 6f, y0 + 6f - w, kx - 1f, y0 + 3f), c(0xB71C32))
            }
            NebyLook.Night -> {
                polygon(floatArrayOf(cx - 13f, t + 5f, cx - 6f, t - 6f, cx + 4f, t - 8f, cx + 12f, t - 4f, cx + 17f, t + 6f, cx + 13f, t + 5f), c(0x3D5AFE))
                fur(this, cx, t + 4.5f, 13.5f, 2f)
                disc(cx + 17f, t + 7f, 2.6f, c(0xFFF1F2))
            }
            NebyLook.Crown -> {
                val y = (t - 1f).roundToInt()
                rect(cxi - 8, y, 17, 4, gold)
                for (k in 0..2) polygon(floatArrayOf(cx - 8f + k * 6f, y.toFloat(), cx - 5.5f + k * 6f + 0.5f, y - 5f, cx - 2f + k * 6f + 0.5f, y.toFloat()), gold)
                hline(cxi - 8, cxi + 8, y + 3, goldLo)
            }
            NebyLook.Dashain -> Unit // tika and jamara, drawn above
            else -> Unit
        }
    }

    // ---- pass 3: fine detail, after the outline -----------------------------------------------------

    fun detail(cv: PixelCanvas, g: Geo) = with(cv) {
        val p = g.pose
        val t = g.top
        val cx = g.cx; val cxi = cx.roundToInt()
        if (p.tika || p.look == NebyLook.Dashain) {
            val ty = (g.cy - 12f).roundToInt()
            set(cxi - 1, ty, rice); set(cxi + 1, ty + 2, rice); set(cxi, ty + 3, rice)
        }
        if (p.jamara || p.look == NebyLook.Dashain) {
            // sunlit tips on the blades
            val bx = g.cx + g.rx * 0.5f; val by = g.top + 6f
            val sway = sin(p.phase * 0.7f) * 0.8f
            for (k in intArrayOf(1, 3, 5)) {
                val o = k - 2.5f
                set((bx + o * 2.2f + sway * (0.5f + k * 0.15f)).roundToInt(), (by - 10f - (k % 3) * 1.5f + kotlin.math.abs(o) * 0.8f).roundToInt(), jamaraHi)
            }
        }
        when (p.look) {
            NebyLook.Astronaut -> {
                // glints on the glass and a blinking antenna
                set((cx - g.rx - 1f).roundToInt(), (g.cy - 6f).roundToInt(), white); set((cx - g.rx).roundToInt(), (g.cy - 9f).roundToInt(), white)
                set((cx - g.rx + 2f).roundToInt(), (t - 1f).roundToInt(), white)
                val ay = (t - 3f).roundToInt()
                line(cxi + 6, ay + 1, cxi + 8, ay - 4, c(0x8C97B3))
                rect(cxi + 8, ay - 6, 2, 2, if ((p.phase.toInt() / 3) % 2 == 0) c(0xFF5A5F) else c(0xFFB3B5))
            }
            NebyLook.Graduate -> {
                val tx = cxi + 9
                line(cxi, (t - 4f).roundToInt(), tx, (t - 2f).roundToInt(), gold)
                for (k in 0..5) set(tx + if (k > 3) (sin(p.phase) * 1f).roundToInt() else 0, (t - 2f).roundToInt() + k, if (k == 5) goldHi else gold)
            }
            NebyLook.Wizard -> {
                set(cxi - 2, (t - 4f).roundToInt(), goldHi); set(cxi + 3, (t - 1f).roundToInt(), goldHi); set(cxi - 4, (t - 8f).roundToInt(), gold)
                val tw = (p.phase.toInt() % 4) == 0
                if (tw) { set(cxi - 7, (t - 10f).roundToInt(), goldHi) }
            }
            NebyLook.Headphones -> {
                // a note drifts up now and then
                val k = (p.phase * 0.6f) % 6f
                if (k < 4f) note(this, (cx + g.rx + 3f).roundToInt(), (g.cy - 12f - k * 2f).roundToInt(), c(0xFF5A5F))
            }
            NebyLook.Crown -> {
                val y = (t - 1f).roundToInt()
                set(cxi - 5, y + 1, c(0xE53950)); set(cxi, y + 1, c(0x3FA7FF)); set(cxi + 5, y + 1, c(0x2DCB73))
                set(cxi - 7, y, goldHi); set(cxi - 2, y - 4, goldHi)
            }
            NebyLook.Monsoon -> {
                // rain runs off the brim
                for (k in 0 until 2) {
                    val dy = ((p.phase * 1.4f + k * 3f) % 6f).roundToInt()
                    set((cx - 15f + k * 29f).roundToInt(), (t + 5f).roundToInt() + dy, c(0x7FB2FF))
                }
            }
            NebyLook.Topi -> {
                // a tiny flag pin on the topi
                val py = (t - 2f).roundToInt()
                set(cxi - 5, py, crimson); set(cxi - 5, py + 1, crimson); set(cxi - 4, py + 1, crimson); set(cxi - 6, py + 1, nepalBlue)
            }
            NebyLook.Losar, NebyLook.Christmas, NebyLook.Night -> {
                // glints on fur and pompoms
                set(cxi - 9, (t + 3f).roundToInt(), white)
            }
            NebyLook.Tihar -> {
                set(cxi - 3, (g.cy - 13f).roundToInt(), white)
            }
            else -> Unit
        }
    }

    // ---- shared pieces ------------------------------------------------------------------------------

    private fun tika(cv: PixelCanvas, g: Geo) = with(cv) {
        // a generous rato tika: red rice pressed on the forehead
        val cx = g.cx.roundToInt(); val y = (g.cy - 13f).roundToInt()
        roundRect(cx - 2, y, 5, 6, 1, tikaRed); hline(cx - 1, cx + 1, y + 5, tikaLo); set(cx + 2, y + 4, tikaLo)
    }

    private fun garland(cv: PixelCanvas, g: Geo) = beads(cv, g, intArrayOf(marigold, marigoldHi, marigold, makhamali), 3)

    /** Flowers or beads hanging in a shallow U across the top of the band. */
    private fun beads(cv: PixelCanvas, g: Geo, colors: IntArray, step: Int) = with(cv) {
        val span = g.rx * 0.82f
        var i = 0
        var x = -span
        while (x <= span) {
            val y = g.bandTop + 0.5f + 3.2f * (1f - (x / span) * (x / span))
            val col = colors[i % colors.size]
            if (step >= 3) {
                disc(g.cx + x, y, 1.7f, col)
                set((g.cx + x).roundToInt(), y.roundToInt() + 1, if (col == makhamali) c(0x7E1F4B) else c(0xD9790F))
            } else {
                set((g.cx + x).roundToInt(), y.roundToInt(), col)
            }
            x += step.toFloat(); i++
        }
    }

    private fun splashes(cv: PixelCanvas, g: Geo, amount: Float) = with(cv) {
        // where gulal lands, relative to the face, never on the eyes
        val spots = floatArrayOf(-10f, -5f, 2.4f, 9f, -9f, 2f, 7f, 4f, 1.9f, -6f, 9f, 2.1f, 1f, -13f, 1.6f, -12f, 5f, 1.5f, 11f, -1f, 1.6f)
        val n = (spots.size / 3 * amount).roundToInt()
        for (k in 0 until n) {
            val x = g.cx + spots[k * 3]; val y = g.cy + spots[k * 3 + 1]; val r = spots[k * 3 + 2]
            val col = gulal[k % gulal.size]
            for (yy in (y - r - 1).toInt()..(y + r + 1).toInt()) for (xx in (x - r - 1).toInt()..(x + r + 1).toInt()) {
                val d = kotlin.math.hypot(xx + 0.5f - x, yy + 0.5f - y)
                // a soft, powdery edge: solid inside, dithered at the rim, only on the body
                if (cv.get(xx, yy) ushr 24 == 0) continue
                if (d <= r || (d <= r + 1.2f && Bayer.threshold(xx, yy) < 0.45f)) set(xx, yy, col)
            }
        }
    }

    private fun fur(cv: PixelCanvas, cx: Float, y: Float, rx: Float, ry: Float) = with(cv) {
        ellipse(cx, y, rx, ry, c(0xF6EEE2))
        for (x in (cx - rx).toInt()..(cx + rx).toInt()) if (Bayer.threshold(x, y.toInt() + 1) < 0.35f) set(x, (y + ry - 0.5f).roundToInt(), c(0xD9CBB3))
    }

    private fun flower(cv: PixelCanvas, x: Float, y: Float, petal: Int, centre: Int) = with(cv) {
        for (a in 0 until 5) {
            val t = a * 2 * PI.toFloat() / 5f
            disc(x + kotlin.math.cos(t) * 2f, y + sin(t) * 2f, 1.3f, petal)
        }
        set(x.roundToInt(), y.roundToInt(), centre)
    }

    private fun cone(cv: PixelCanvas, bx: Float, by: Float, hw: Float, tx: Float, ty: Float, a: Int, b: Int) = with(cv) {
        polygon(floatArrayOf(bx - hw, by, tx, ty, bx + hw, by), a)
        // stripes, following the cone up
        for (k in 1..3) {
            val f = k / 4f
            val y = (by + (ty - by) * f).roundToInt()
            val half = hw * (1f - f)
            val mx = bx + (tx - bx) * f
            hline((mx - half).roundToInt(), (mx + half).roundToInt(), y, b)
        }
        ellipse(bx, by, hw + 0.5f, 1.2f, b)
    }

    private fun scarf(cv: PixelCanvas, g: Geo) = with(cv) {
        val y0 = (g.bandTop - 1f).roundToInt()
        for (y in y0..y0 + 3) {
            val hw = g.halfWidth(y.toFloat()) + 1f
            for (x in (g.cx - hw).roundToInt()..(g.cx + hw).roundToInt()) set(x, y, if (((x + 100) / 3) % 2 == 0) c(0x2E7D32) else c(0xF5F5F5))
        }
        val tx = (g.cx + 5f).roundToInt()
        for (y in y0 + 3..y0 + 9) for (x in tx..tx + 3) set(x, y, if (((y + 100) / 2) % 2 == 0) c(0x2E7D32) else c(0xF5F5F5))
    }

    /** The Dhaka topi: brimless, taller on the left, cream cloth woven with rows of small red and black diamonds. */
    private fun topi(cv: PixelCanvas, g: Geo) = with(cv) {
        val t = g.top
        val left = (g.cx - 9f).roundToInt(); val right = (g.cx + 9f).roundToInt()
        val base = (t + 5f).roundToInt()
        for (x in left..right) {
            val f = (x - left).toFloat() / (right - left)
            var top = (t - 5f + f * 3f).roundToInt()
            if (x == left || x == right) top += 1 // soft corners
            for (y in top..base) {
                val row = y - (t - 5f).roundToInt()
                val band = Math.floorMod(row, 4)
                val d = Math.floorMod(x + (row / 4) * 2, 4)
                val col = when {
                    y == base -> c(0x6A1B1B)
                    band == 1 && d == 1 -> c(0xC62828)
                    band == 2 && (d == 0 || d == 2) -> c(0xC62828)
                    band == 2 && d == 1 -> c(0x2B2530)
                    band == 3 && d == 1 -> c(0xC62828)
                    band == 0 && d == 3 -> c(0xE58E26)
                    else -> c(0xF4E8D0)
                }
                set(x, y, col)
            }
        }
    }

    private fun note(cv: PixelCanvas, x: Int, y: Int, col: Int) = with(cv) {
        rect(x, y + 3, 2, 2, col); line(x + 1, y, x + 1, y + 3, col); set(x + 2, y, col); set(x + 3, y + 1, col)
    }

    /** Distance from the body's centre line, used by states placing props. */
    internal fun clearOfBody(g: Geo, x: Float): Boolean = abs(x - g.cx) > g.rx + 1f
}
