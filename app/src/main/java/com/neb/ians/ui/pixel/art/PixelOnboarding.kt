package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.Bayer
import com.neb.ians.ui.pixel.NebyState
import com.neb.ians.ui.pixel.PixelCanvas
import com.neb.ians.ui.pixel.Px
import kotlin.math.roundToInt

/**
 * The pictures for sign-up and onboarding, in pixel art. Each step is a small scene that answers
 * the form: arrows on a signpost light up as a path is chosen, a name card fills as a name is
 * typed, a calendar turns to the birthday and a cake appears, Neby climbs the stairs to the class
 * chosen. The scene is a still picture; Neby, standing in it, is a live sprite drawn on top
 * ([Scene.neby] says where and doing what), so the picture only re-renders when the answer
 * changes.
 */
object PixelOnboarding {
    const val WIDTH = 128
    const val HEIGHT = 64

    enum class Kind { Welcome, Paths, Name, Handle, Birthday, Facets, Level, Subjects, Province, School, Photo, Arrival, Code }
    enum class Handle { Idle, Checking, Available, Taken }

    /** Where Neby stands (art pixels: centre x and the ground row) and what Neby is doing. */
    class NebyMark(val x: Int, val ground: Int, val state: NebyState)

    class Scene(val canvas: PixelCanvas, val neby: NebyMark)

    private val accent = c(0xFF8A3D); private val accentHi = c(0xFFC08A)
    private val green = c(0x2FB36B); private val red = c(0xE5484D); private val amber = c(0xF5B53F)
    private val wood = c(0xB7814E); private val woodHi = c(0xD9A26A); private val woodLo = c(0x8A5A32)
    private val paper = c(0xFFFDF6); private val paperLo = c(0xE6DDCB); private val ink = c(0x2B3044)

    /**
     * [a] and [b] carry the step's answer: a selected index and a count, a progress in
     * thousandths, a day of the month. [flag] is a yes/no (a school named, a photo chosen).
     */
    fun render(kind: Kind, a: Int = -1, b: Int = 0, flag: Boolean = false, handle: Handle = Handle.Idle): Scene {
        val cv = PixelCanvas(WIDTH, HEIGHT)
        val seed = kind.ordinal * 7 + 3
        return when (kind) {
            Kind.Welcome -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Himalaya, false, seed)
                PixelPropsHumanities.paperPlane(cv, 98, st.groundY - 4)
                Scene(cv, NebyMark(54, st.groundY, NebyState.Wave))
            }
            Kind.Paths -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Terraces, false, seed)
                cv.contactShadow(84, st.groundY, 10, st.shadow)
                signpost(cv, 84, st.groundY - 1, b.coerceIn(1, 5), a)
                Scene(cv, NebyMark(46, st.groundY, if (a >= 0) NebyState.Hop else NebyState.LookAround))
            }
            Kind.Name -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Desk, false, seed)
                nameCard(cv, 88, st.groundY - 1, a / 1000f)
                Scene(cv, NebyMark(46, st.groundY, if (a > 0) NebyState.Talk else NebyState.Wave))
            }
            Kind.Handle -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Clouds, false, seed)
                atSign(cv, 88, st.groundY - 1, handle)
                val mood = when (handle) { Handle.Idle -> NebyState.Idle; Handle.Checking -> NebyState.Think; Handle.Available -> NebyState.Success; Handle.Taken -> NebyState.Oops }
                Scene(cv, NebyMark(44, st.groundY, mood))
            }
            Kind.Birthday -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Desk, false, seed)
                calendar(cv, 76, 6, if (a in 1..31) a else null)
                if (a in 1..31) cake(cv, 100, st.groundY - 1)
                Scene(cv, NebyMark(42, st.groundY, if (a in 1..31) NebyState.Celebrate else NebyState.Think))
            }
            Kind.Facets -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Clouds, false, seed)
                gems(cv, 86, st.groundY - 6, b.coerceIn(1, 5), a)
                Scene(cv, NebyMark(40, st.groundY, if (a >= 0) NebyState.Love else NebyState.LookAround))
            }
            Kind.Level -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Himalaya, false, seed)
                val n = b.coerceIn(2, 12)
                val pos = stairs(cv, st.groundY, n, a.coerceIn(0, n - 1))
                Scene(cv, NebyMark(pos.first, pos.second, NebyState.Hop))
            }
            Kind.Subjects -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Desk, false, seed)
                bookPile(cv, 90, st.groundY - 1, a.coerceIn(0, 8))
                Scene(cv, NebyMark(44, st.groundY, if (a > 0) NebyState.Read else NebyState.Idle))
            }
            Kind.Province -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Clouds, false, seed)
                nepal(cv, 58, 16, if (a in 0..6) 6 - a else -1)
                Scene(cv, NebyMark(22, st.groundY, if (a >= 0) NebyState.Wave else NebyState.LookAround))
            }
            Kind.School -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Terraces, false, seed)
                school(cv, 88, st.groundY - 1, flag)
                Scene(cv, NebyMark(42, st.groundY, if (flag) NebyState.Success else NebyState.Idle))
            }
            Kind.Photo -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Desk, false, seed)
                camera(cv, 90, st.groundY - 1, flag)
                Scene(cv, NebyMark(44, st.groundY, NebyState.Cool))
            }
            Kind.Arrival -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Himalaya, true, seed)
                for ((x, y, col) in listOf(Triple(30, 14, c(0xFFCE5C)), Triple(96, 10, c(0xFF6F91)), Triple(70, 20, c(0x7FD6FF)))) burstStill(cv, x, y, col)
                flags(cv, st.groundY)
                Scene(cv, NebyMark(64, st.groundY, NebyState.Celebrate))
            }
            Kind.Code -> {
                val st = PixelBackdrops.draw(cv, Backdrop.Clouds, false, seed)
                envelope(cv, 90, 30)
                codeDots(cv, 64, 6, a.coerceAtLeast(0), b.coerceIn(1, 8))
                Scene(cv, NebyMark(40, st.groundY, if (a >= b && b > 0) NebyState.Success else if (a > 0) NebyState.Listen else NebyState.Idle))
            }
        }
    }

    // ---- props -------------------------------------------------------------------------------------

    private fun signpost(cv: PixelCanvas, x: Int, base: Int, count: Int, selected: Int) = with(cv) {
        prop { box(x - 1, base - 36, 3, 36, wood, woodHi, woodLo) }
        for (i in 0 until count) {
            val y = base - 34 + i * 7
            val right = i % 2 == 0
            val on = i == selected
            prop {
                val col = if (on) accent else wood
                if (right) polygon(floatArrayOf(x + 1f, y.toFloat(), x + 16f, y.toFloat(), x + 19f, y + 2.5f, x + 16f, y + 5f, x + 1f, y + 5f), col)
                else polygon(floatArrayOf(x + 1f, y.toFloat(), x - 15f, y.toFloat(), x - 18f, y + 2.5f, x - 15f, y + 5f, x + 1f, y + 5f), col)
            }
            detail {
                val sx = if (right) x + 4 else x - 13
                hline(sx, sx + 8, y + 2, if (on) accentHi else woodHi)
                if (on) { set(if (right) x + 21 else x - 20, y + 2, c(0xFFE6B8)); set(if (right) x + 22 else x - 21, y + 1, c(0xFFE6B8)) }
            }
        }
    }

    private fun nameCard(cv: PixelCanvas, x: Int, base: Int, progress: Float) = with(cv) {
        prop {
            polygon(floatArrayOf(x - 18f, base.toFloat(), x - 15f, base - 18f, x + 15f, base - 18f, x + 18f, base.toFloat()), paper)
            hline(x - 17, x + 17, base - 1, paperLo)
        }
        detail {
            val w = (progress.coerceIn(0f, 1f) * 24).roundToInt()
            for (k in 0..1) if (w > 0) hline(x - 12, x - 12 + w, base - 12 + k, ink)
            hline(x - 12, x + 12, base - 8, paperLo)
            hline(x - 12, x - 12 + (w * 0.6f).roundToInt(), base - 5, c(0x9AA4B8))
            // the caret, just after the last letter
            if (w < 24) for (k in 0..3) set(x - 11 + w, base - 14 + k, accent)
        }
    }

    private fun atSign(cv: PixelCanvas, x: Int, base: Int, state: Handle) = with(cv) {
        val col = when (state) { Handle.Idle -> c(0x7FA7E8); Handle.Checking -> amber; Handle.Available -> green; Handle.Taken -> red }
        prop {
            box(x - 1, base - 18, 3, 18, wood, woodHi, woodLo)
            disc(x + 0.5f, base - 30f, 13f, c(0xFFFFFF))
        }
        detail {
            // a ring in the verdict's colour, and the @ inside it
            for (k in 0 until 64) { val t = k / 64f * 6.283f; set((x + 0.5f + kotlin.math.cos(t) * 11.5f).roundToInt(), (base - 30f + kotlin.math.sin(t) * 11.5f).roundToInt(), col) }
            val g = arrayOf(".1111.", "1....1", "1.11.1", "1.1.11", "1..11.", "1.....", ".1111.")
            for (r in g.indices) for (k in 0 until 6) if (g[r][k] == '1') rect(x - 6 + k * 2, base - 37 + r * 2, 2, 2, ink)
            if (state == Handle.Available) { set(x + 9, base - 42, green); set(x + 10, base - 43, green) }
        }
    }

    private val digits = arrayOf(
        arrayOf("111", "1.1", "1.1", "1.1", "111"), arrayOf(".1.", "11.", ".1.", ".1.", "111"), arrayOf("111", "..1", "111", "1..", "111"),
        arrayOf("111", "..1", "111", "..1", "111"), arrayOf("1.1", "1.1", "111", "..1", "..1"), arrayOf("111", "1..", "111", "..1", "111"),
        arrayOf("111", "1..", "111", "1.1", "111"), arrayOf("111", "..1", ".1.", ".1.", ".1."), arrayOf("111", "1.1", "111", "1.1", "111"),
        arrayOf("111", "1.1", "111", "..1", "111"),
    )
    private val question = arrayOf("111", "..1", ".11", "...", ".1.")

    private fun glyph(cv: PixelCanvas, g: Array<String>, x: Int, y: Int, scale: Int, col: Int) {
        for (r in g.indices) for (k in g[r].indices) if (g[r][k] == '1') cv.rect(x + k * scale, y + r * scale, scale, scale, col)
    }

    private fun calendar(cv: PixelCanvas, x: Int, y: Int, day: Int?) = with(cv) {
        prop {
            rect(x - 13, y, 26, 26, paper)
            rect(x - 13, y, 26, 7, red)
        }
        detail {
            for (k in 0 until 3) { set(x - 8 + k * 8, y - 1, c(0x8692AB)); set(x - 8 + k * 8, y, c(0x8692AB)) }
            hline(x - 13, x + 12, y + 25, paperLo)
            if (day == null) glyph(this, question, x - 3, y + 10, 2, c(0x9AA4B8))
            else {
                val s = day.toString()
                val w = s.length * 8 - 2
                s.forEachIndexed { i, ch -> glyph(this, digits[ch - '0'], x - w / 2 + i * 8, y + 10, 2, ink) }
            }
        }
    }

    private fun cake(cv: PixelCanvas, x: Int, base: Int) = with(cv) {
        prop {
            box(x - 9, base - 7, 19, 7, c(0xF7B6C8), c(0xFFD6E2), c(0xE58AA6))
            box(x - 6, base - 12, 13, 5, c(0xFFF4E6), c(0xFFFFFF), c(0xEAD8C0))
            rect(x, base - 17, 2, 5, c(0x7FB2FF))
        }
        detail {
            set(x, base - 19, c(0xFFC93C)); set(x + 1, base - 19, c(0xFFC93C)); set(x, base - 20, c(0xFFF6C8))
            for (k in 0 until 4) set(x - 7 + k * 5, base - 5, c(0xFFFFFF))
        }
    }

    private fun gems(cv: PixelCanvas, x: Int, base: Int, count: Int, selected: Int) = with(cv) {
        val cols = intArrayOf(c(0x9B5DE5), c(0x2EC4B6), c(0xF5B53F), c(0xFF6F91), c(0x3FA7FF))
        for (i in 0 until count) {
            val gx = x - (count - 1) * 9 + i * 18
            val on = i == selected
            val s = if (on) 9f else 6f
            val gy = base - (if (on) 22 else 14)
            if (on) for (yy in gy - 14..gy + 14) for (xx in gx - 14..gx + 14) {
                val d = kotlin.math.hypot((xx - gx).toFloat(), (yy - gy).toFloat())
                if (d in s..14f && Bayer.threshold(xx, yy) < (1f - d / 14f) * 0.7f) set(xx, yy, Px.mix(get(xx, yy), cols[i % cols.size], 0.35f))
            }
            prop {
                polygon(floatArrayOf(gx - s, gy.toFloat(), gx - s * 0.5f, gy - s * 0.6f, gx + s * 0.5f, gy - s * 0.6f, gx + s, gy.toFloat(), gx.toFloat(), gy + s), cols[i % cols.size])
                hline((gx - s * 0.5f).roundToInt(), (gx + s * 0.5f).roundToInt(), (gy - s * 0.6f).roundToInt() + 1, Px.mix(cols[i % cols.size], c(0xFFFFFF), 0.5f))
            }
            detail { set(gx - 2, gy - 2, c(0xFFFFFF)) }
        }
    }

    /** Stairs rising to a summit flag; returns where step [at] is (centre x, top row) for Neby. */
    private fun stairs(cv: PixelCanvas, ground: Int, count: Int, at: Int): Pair<Int, Int> = with(cv) {
        val x0 = 18; val x1 = 122
        val sw = (x1 - x0) / count
        val rise = (30f / count).coerceAtLeast(2f)
        var mark = x0 + sw / 2 to ground
        prop {
            for (i in 0 until count) {
                val top = (ground - (i + 1) * rise).roundToInt()
                box(x0 + i * sw, top, sw, ground - top, c(0xD8CBB4), c(0xF2E8D6), c(0xB9A88C))
            }
        }
        for (i in 0 until count) {
            val top = (ground - (i + 1) * rise).roundToInt()
            if (i == at) { mark = x0 + i * sw + sw / 2 to top; detail { hline(x0 + i * sw + 1, x0 + (i + 1) * sw - 2, top, accent) } }
        }
        val fx = x1 - sw / 2; val fy = (ground - count * rise).roundToInt()
        detail {
            rect(fx, fy - 12, 1, 12, c(0x5A4A3A))
            polygon(floatArrayOf(fx + 1f, fy - 12f, fx + 8f, fy - 9f, fx + 1f, fy - 6f), red)
        }
        mark
    }

    private fun bookPile(cv: PixelCanvas, x: Int, base: Int, n: Int) = with(cv) {
        val cols = intArrayOf(c(0xD9534F), c(0x3D7DD8), c(0xF0AD4E), c(0x5CB85C), c(0x8E6CC4), c(0x2BA3A3), c(0xE07A5F), c(0x4A6FA5))
        if (n == 0) { prop { rect(x - 12, base - 2, 24, 2, paperLo) }; return@with }
        prop {
            var y = base
            for (i in 0 until n) {
                val w = 22 + (i * 5) % 7; val off = ((i * 3) % 5) - 2
                rect(x - w / 2 + off, y - 4, w, 4, cols[i % cols.size]); rect(x - w / 2 + off + 1, y - 3, w - 3, 2, paper)
                y -= 4
            }
        }
    }

    /** Nepal, west to east, in seven slices; [slice] (0 = far west) is filled in. */
    private fun nepal(cv: PixelCanvas, x: Int, y: Int, slice: Int) = with(cv) {
        val pts = floatArrayOf(0f, 9f, 9f, 3f, 20f, 6f, 31f, 9f, 43f, 13f, 56f, 15f, 66f, 17f, 70f, 21f, 67f, 27f, 52f, 26f, 37f, 24f, 22f, 21f, 9f, 19f, 2f, 15f)
        val p = FloatArray(pts.size) { if (it % 2 == 0) x - 35 + pts[it] else y + pts[it] }
        val land = c(0xE8F1E2); val on = accent
        val layer = PixelCanvas(width, height)
        layer.polygon(p, land)
        for (yy in 0 until height) for (xx in 0 until width) if (layer.get(xx, yy) == land) {
            val s = ((xx - (x - 35)) / 10).coerceIn(0, 6)
            layer.set(xx, yy, if (s == slice) on else if (s % 2 == 0) land else c(0xD6E6CC))
        }
        layer.outline(c(0x3B4A3A))
        for (i in pixels.indices) if ((layer.pixels[i] ushr 24) != 0) pixels[i] = layer.pixels[i]
        // a pin on the chosen province
        if (slice >= 0) detail {
            val px = x - 35 + slice * 10 + 5
            disc(px + 0.5f, y + 4f, 2.6f, red); set(px, y + 3, c(0xFFB3B5)); line(px, y + 6, px, y + 11, ink)
        }
    }

    private fun nepalFlag(cv: PixelCanvas, x: Int, y: Int) = with(cv) {
        polygon(floatArrayOf(x.toFloat(), y.toFloat(), x + 8f, y + 5f, x + 3f, y + 5f, x + 8f, y + 10f, x.toFloat(), y + 10f), c(0x003893))
        polygon(floatArrayOf(x + 1f, y + 1.5f, x + 6f, y + 4.5f, x + 1f, y + 4.5f), c(0xDC143C))
        polygon(floatArrayOf(x + 1f, y + 5.5f, x + 6f, y + 9.2f, x + 1f, y + 9.2f), c(0xDC143C))
        set(x + 2, y + 3, c(0xFFFFFF)); set(x + 2, y + 7, c(0xFFFFFF))
    }

    private fun school(cv: PixelCanvas, x: Int, base: Int, named: Boolean) = with(cv) {
        prop {
            box(x - 18, base - 14, 30, 14, c(0xF4F1EA), c(0xFFFFFF), c(0xD9D2C2))
            polygon(floatArrayOf(x - 21f, base - 14f, x - 3f, base - 22f, x + 15f, base - 14f), c(0xB5523A))
            rect(x - 6, base - 8, 6, 8, c(0x2F64D6))
        }
        detail {
            for (k in 0 until 2) { rect(x - 15 + k * 21, base - 11, 4, 4, c(0x7FB2FF)); set(x - 15 + k * 21, base - 11, c(0xFFFFFF)) }
            hline(x - 18, x + 11, base - 14, c(0x2F64D6))
            rect(x + 20, base - 30, 1, 30, c(0x8692AB))
            nepalFlag(this, x + 21, if (named) base - 30 else base - 12)
        }
    }

    private fun camera(cv: PixelCanvas, x: Int, base: Int, taken: Boolean) = with(cv) {
        prop {
            line(x, base - 12, x - 8, base, ink); line(x, base - 12, x + 8, base, ink); line(x, base - 12, x, base, ink)
            box(x - 11, base - 25, 22, 13, c(0x3B4158), c(0x5A6178), c(0x262B3D))
            rect(x - 6, base - 28, 7, 3, c(0x3B4158))
            disc(x + 0.5f, base - 18.5f, 5.5f, c(0x14192B))
            disc(x + 0.5f, base - 18.5f, 3.5f, c(0x3F6FD0))
        }
        detail {
            set(x - 1, base - 20, c(0xFFFFFF)); rect(x + 7, base - 24, 2, 2, c(0xFFC93C))
            if (taken) for (k in 1..3) { set(x - 10 - k * 2, base - 32 - k, c(0xFFF2B8)); set(x + 12 + k * 2, base - 32 - k, c(0xFFF2B8)); set(x + 1, base - 32 - k * 2, c(0xFFF2B8)) }
        }
    }

    private fun burstStill(cv: PixelCanvas, x: Int, y: Int, col: Int) = with(cv) {
        for (k in 0 until 12) {
            val a = k * Math.PI.toFloat() / 6f
            for (r in 4..8 step 2) set((x + kotlin.math.cos(a) * r).roundToInt(), (y + kotlin.math.sin(a) * r).roundToInt(), if (r == 8) Px.mix(col, c(0xFFFFFF), 0.4f) else col)
        }
        set(x, y, c(0xFFFFFF))
    }

    private fun flags(cv: PixelCanvas, ground: Int) = with(cv) {
        val cols = intArrayOf(c(0x2F64D6), c(0xF5F5F5), c(0xE53935), c(0x2E9E4F), c(0xFDD835))
        for (k in 0..30) {
            val t = k / 30f
            val x = (6 + t * 116).roundToInt(); val y = (ground - 22 + kotlin.math.sin(t * Math.PI.toFloat()) * 8f).roundToInt()
            set(x, y, c(0x8A7E70)); if (k % 1 == 0) rect(x, y + 1, 3, 3, cols[k % cols.size])
        }
    }

    private fun envelope(cv: PixelCanvas, x: Int, y: Int) = with(cv) {
        detail { for (k in 0 until 4) hline(x - 30 + k * 3, x - 18, y + 2 + k * 3, c(0xFFFFFF)) }
        prop {
            rect(x - 13, y - 8, 26, 17, paper)
            polygon(floatArrayOf(x - 13f, y - 8f, x + 13f, y - 8f, x.toFloat(), y + 2f), paperLo)
        }
        detail { rect(x + 6, y + 2, 4, 4, red); set(x + 7, y + 3, c(0xFFB3B5)) }
    }

    private fun codeDots(cv: PixelCanvas, x: Int, y: Int, filled: Int, total: Int) = with(cv) {
        val w = total * 8 - 2
        for (i in 0 until total) prop { roundRect(x - w / 2 + i * 8, y, 6, 8, 1, if (i < filled) accent else c(0xFFFFFF)) }
        detail { for (i in 0 until minOf(filled, total)) set(x - w / 2 + i * 8 + 1, y + 1, accentHi) }
    }
}
