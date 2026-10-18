package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.Bayer
import com.neb.ians.ui.pixel.PixelCanvas
import com.neb.ians.ui.pixel.Px
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * The four places a resource banner can be set, each by day and by night (the web and the app
 * show the night version in dark mode). A backdrop leaves a ground line at [Stage.groundY] for
 * the subject's prop to stand on, and says what colour a contact shadow should be there.
 */
internal class Stage(val groundY: Int, val shadow: Int)

internal enum class Backdrop { Himalaya, Desk, Terraces, Clouds }

internal object PixelBackdrops {

    fun draw(c: PixelCanvas, b: Backdrop, night: Boolean, seed: Int): Stage = when (b) {
        Backdrop.Himalaya -> himalaya(c, night, seed)
        Backdrop.Desk -> desk(c, night, seed)
        Backdrop.Terraces -> terraces(c, night, seed)
        Backdrop.Clouds -> clouds(c, night, seed)
    }

    private fun sky(night: Boolean) = if (night) intArrayOf(c(0x0A1230), c(0x14204A), c(0x223466), c(0x34487E))
        else intArrayOf(c(0x6FA8EE), c(0x8DBDF3), c(0xB3D4F8), c(0xDCEBFC))

    /** Snow peaks in two ranges, green hills, a meadow in front. */
    private fun himalaya(cv: PixelCanvas, night: Boolean, seed: Int): Stage = with(cv) {
        skyGradient(sky(night), 0, 40)
        if (night) {
            stars(seed, 46, 30, c(0x6C7FB5), c(0xE8EEFF))
            crescent(width * 0.16f, 10f, 4.5f, c(0xFFF4D6)) { x, y -> get(x + 12, y) }
        } else {
            glowDisc(width * 0.15f, 11f, 4f, c(0xFFF6D8), c(0xFFFDF2), 9f)
            cloud(width * 0.42f, 15f, 22f, c(0xFFFFFF), c(0xFFFFFF), c(0xD8E6FA), seed + 3)
        }
        // the far range, pale with distance; then the near range, sharper, with its fishtail peak
        val far = ridge(width, 24f, 8f, seed + 11, jag = 0.5f)
        mountains(far, if (night) c(0x34477A) else c(0xA9BEE2), if (night) c(0x2A3B68) else c(0x95ACD6),
            if (night) c(0xB8C6E8) else c(0xF6FAFF), if (night) c(0x8FA2CF) else c(0xD5E2F6), 4f, seed + 12)
        val near = ridge(width, 34f, 9f, seed + 21, jag = 0.7f)
        val peak = (width * 0.62f).toInt()
        for (x in 0 until width) near[x] -= (12f - kotlin.math.abs(x - peak) * 0.5f).coerceAtLeast(0f)
        mountains(near, if (night) c(0x26365E) else c(0x7E95C2), if (night) c(0x1D2B4D) else c(0x6A80AE),
            if (night) c(0xA9B9DF) else c(0xFFFFFF), if (night) c(0x7E92C2) else c(0xC9D8F0), 5f, seed + 22)
        // rolling hills and the meadow
        val hills = ridge(width, 44f, 3f, seed + 31)
        fillBelow(hills, if (night) c(0x1B3A3A) else c(0x5E9E5C), if (night) c(0x2A5050) else c(0x7DBB6E))
        val meadow = FloatArray(width) { 52f + sin(it * 0.05f + seed) * 1.2f }
        fillBelow(meadow, if (night) c(0x22443A) else c(0x82C16E), if (night) c(0x35604E) else c(0xA6D98A))
        for (x in 0 until width) for (y in 54 until height) if (Bayer.threshold(x * 3, y) < 0.12f) set(x, y, if (night) c(0x2E5446) else c(0x6FB05E))
        Stage(53, if (night) c(0x15302A) else c(0x5C9A4C))
    }

    /** A study desk by a window with the mountains outside; a lamp on at night. */
    private fun desk(cv: PixelCanvas, night: Boolean, seed: Int): Stage = with(cv) {
        val wall = if (night) c(0x262B42) else c(0xF1E6D6)
        val wallLo = if (night) c(0x20243A) else c(0xE6D7C2)
        for (y in 0 until 50) for (x in 0 until width) set(x, y, if (Bayer.threshold(x, y) < 0.18f) wallLo else wall)
        // the window
        val wx = 8; val wy = 6; val ww = 40; val wh = 32
        val glass = PixelCanvas(ww, wh)
        glass.skyGradient(sky(night))
        if (night) glass.stars(seed, 14, 16, c(0x6C7FB5), c(0xE8EEFF))
        else glass.cloud(ww * 0.6f, 9f, 14f, c(0xFFFFFF), c(0xFFFFFF), c(0xD8E6FA), seed)
        glass.mountains(ridge(ww, 20f, 5f, seed + 5, 2f), if (night) c(0x26365E) else c(0x8FA5CF), if (night) c(0x1D2B4D) else c(0x7A92C0),
            if (night) c(0xA9B9DF) else c(0xFFFFFF), if (night) c(0x7E92C2) else c(0xD0DDF2), 4f, seed + 6)
        glass.fillBelow(ridge(ww, 27f, 2f, seed + 7), if (night) c(0x1B3A3A) else c(0x6DAA62))
        for (y in 0 until wh) for (x in 0 until ww) set(wx + x, wy + y, glass.get(x, y))
        val frame = if (night) c(0x5B4632) else c(0xFFFFFF); val frameLo = if (night) c(0x3E3022) else c(0xD9CCBA)
        rect(wx - 2, wy - 2, ww + 4, 2, frame); rect(wx - 2, wy + wh, ww + 4, 2, frame)
        rect(wx - 2, wy, 2, wh, frame); rect(wx + ww, wy, 2, wh, frame); rect(wx + ww / 2 - 1, wy, 2, wh, frame)
        hline(wx - 3, wx + ww + 2, wy + wh + 2, frameLo)
        // a shelf with books, right of the window
        val sy = 11
        hline(64, 120, sy, if (night) c(0x6B5238) else c(0xB98A5A)); hline(64, 120, sy + 1, if (night) c(0x4A3826) else c(0x8F6640))
        val bookCols = intArrayOf(c(0xD9534F), c(0x3D7DD8), c(0xF0AD4E), c(0x5CB85C), c(0x8E6CC4), c(0x2BA3A3))
        val d = Dice(seed)
        var x = 68
        while (x < 116) {
            val bw = 3 + d.int(2); val bh = 6 + d.int(3)
            val col = if (night) Px.mix(bookCols[d.int(bookCols.size)], c(0x1A1E30), 0.45f) else bookCols[d.int(bookCols.size)]
            rect(x, sy - bh, bw, bh, col); hline(x, x + bw - 1, sy - bh + 2, Px.mix(col, c(0xFFFFFF), 0.4f))
            x += bw + (if (d.next() < 0.2f) 3 else 0)
        }
        // the desk
        val top = 50
        hline(0, width - 1, top - 1, if (night) c(0x8A6A48) else c(0xE2B07A))
        rect(0, top, width, 3, if (night) c(0x6E5238) else c(0xC48E58))
        for (y in top + 3 until height) for (xx in 0 until width) set(xx, y, if (Bayer.threshold(xx, y) < 0.3f) (if (night) c(0x4C3825) else c(0x9A6A3E)) else (if (night) c(0x5A4330) else c(0xAC7848)))
        if (night) {
            // the lamp's pool of light
            for (y in 24 until height) for (xx in 92 until width) {
                val dd = kotlin.math.hypot(xx - 112f, (y - 44f) * 1.4f)
                if (dd < 26f && Bayer.threshold(xx, y) < (1f - dd / 26f) * 0.5f) set(xx, y, Px.mix(get(xx, y), c(0xFFD98A), 0.35f))
            }
            prop {
                rect(110, 36, 3, 13, c(0x3A3F55)); rect(106, 48, 11, 2, c(0x3A3F55))
                polygon(floatArrayOf(104f, 36f, 108f, 28f, 117f, 28f, 121f, 36f), c(0x2E7D6B))
            }
            for (xx in 105..120) set(xx, 36, c(0xFFE8A8))
        }
        Stage(50, if (night) c(0x3E2E1E) else c(0x8C5E34))
    }

    /** Rice terraces stepping down the hill, a village house, paddy water holding the sky. */
    private fun terraces(cv: PixelCanvas, night: Boolean, seed: Int): Stage = with(cv) {
        skyGradient(sky(night), 0, 34)
        if (night) { stars(seed, 34, 22, c(0x6C7FB5), c(0xE8EEFF)); glowDisc(width * 0.84f, 9f, 3.5f, c(0xFFF4D6), c(0x46598C), 7f) }
        else glowDisc(width * 0.84f, 9f, 4f, c(0xFFF2C4), c(0xFFFBEA), 9f)
        val far = ridge(width, 24f, 5f, seed + 3, 1.5f)
        fillBelow(far, if (night) c(0x23345C) else c(0x98B4DE))
        val greens = if (night) intArrayOf(c(0x1D3B34), c(0x234740), c(0x1A3530)) else intArrayOf(c(0x7CBF5A), c(0x93CF68), c(0x6AAE50))
        val lips = if (night) c(0x35605A) else c(0xB8E58C)
        val water = if (night) c(0x2B3D6A) else c(0xBFD9F6)
        var y = 30
        var k = 0
        while (y < height) {
            // each terrace follows the hill's contour: highest over the shoulder at the left, falling away to the right
            val curve = FloatArray(width) { x -> val dx = (x - 30f) / 70f; y + dx * dx * 9f + sin(x * 0.11f + k * 1.7f) * 1.2f - 2f }
            val col = greens[k % greens.size]
            for (x in 0 until width) {
                val t = curve[x].roundToInt()
                for (yy in t.coerceAtLeast(0) until height) set(x, yy, if (k % 2 == 1 && yy in t + 2..t + 3 && Bayer.threshold(x, yy) < 0.75f) water else col)
                set(x, t, lips); set(x, t + 1, Px.mix(col, c(0x000000), 0.12f))
            }
            y += 5 + k % 2; k++
        }
        // a village house on the upper terrace, ochre walls and a slate roof
        val hx = 18; val hy = 34
        prop {
            rect(hx, hy - 7, 12, 7, if (night) c(0x8A5A3A) else c(0xD9824A)); rect(hx, hy - 3, 12, 3, if (night) c(0xC9B9A0) else c(0xF3E7D2))
            polygon(floatArrayOf(hx - 2f, hy - 7f, hx + 6f, hy - 12f, hx + 14f, hy - 7f), if (night) c(0x3A3F55) else c(0x5A6178))
        }
        set(hx + 3, hy - 5, if (night) c(0xFFD36B) else c(0x3A2A20)); set(hx + 8, hy - 5, if (night) c(0xFFD36B) else c(0x3A2A20))
        if (night) { val d = Dice(seed); repeat(10) { set(d.int(width), 38 + d.int(24), c(0xFFF3A0)) } } // fireflies
        Stage(56, if (night) c(0x12261F) else c(0x5A9A46))
    }

    /** Above the clouds: a sea of cumulus in sunlight, or in moonlight with the stars out. */
    private fun clouds(cv: PixelCanvas, night: Boolean, seed: Int): Stage = with(cv) {
        skyGradient(if (night) intArrayOf(c(0x0B1230), c(0x1A2452), c(0x2E3A70), c(0x4A4F86)) else intArrayOf(c(0x4F94E8), c(0x76B0F0), c(0xA6CEF6), c(0xE6F1FD)))
        if (night) {
            stars(seed, 60, 40, c(0x6C7FB5), c(0xE8EEFF))
            crescent(width * 0.82f, 12f, 5f, c(0xFFF4D6)) { x, y -> get(x - 14, y) }
        } else {
            glowDisc(width * 0.82f, 12f, 5f, c(0xFFF4C8), c(0xFFFBEA), 12f)
        }
        val body = if (night) c(0x6C77B0) else c(0xFFFFFF); val light = if (night) c(0x9AA4D8) else c(0xFFFFFF); val shade = if (night) c(0x4A5390) else c(0xCFE0F7)
        val d = Dice(seed)
        cloud(width * 0.25f, 26f, 20f, Px.mix(body, c(0xB9D3F5), if (night) 0f else 0.3f), light, shade, seed + 1)
        cloud(width * 0.6f, 22f, 14f, Px.mix(body, c(0xB9D3F5), if (night) 0f else 0.3f), light, shade, seed + 2)
        var x = -8f
        var i = 0
        while (x < width + 10) {
            val w = d.range(18f, 30f)
            cloud(x + w / 2, 58f + d.range(-2f, 2f), w, body, light, shade, seed + 10 + i)
            x += w * 0.7f; i++
        }
        for (xx in 0 until width) for (y in 57 until height) set(xx, y, if (Bayer.threshold(xx, y) < 0.3f) shade else body)
        Stage(52, shade)
    }
}
