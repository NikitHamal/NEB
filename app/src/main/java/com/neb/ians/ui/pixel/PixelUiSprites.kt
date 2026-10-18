package com.neb.ians.ui.pixel

import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Pixel sprites for the app's own states: Neby, empty inboxes, no results, offline, loading.
 * Each is drawn by code on a small canvas (shape, shading, then a 1 px outline), so every frame
 * is consistent and the set shares one look. Played by PixelSpriteView; picked for empty states
 * by [PixelStates].
 */
object PixelUiSprites {
    private val line = Px.rgb(0x1E2A4A)
    private val white = Px.rgb(0xFFFFFF)
    private val shadow = 0x22101830

    // Neby's own colours (neby-avatar.js): a pale blue body, a deeper band, navy eyes
    private val nebyBody = Px.rgb(0xCCE2FF)
    private val nebyShade = Px.rgb(0xAFCBF6)
    private val nebyBand = Px.rgb(0x2F64D6)
    private val nebyBandHi = Px.rgb(0x5A8BEA)
    private val nebyWave = Px.rgb(0x9CC0FA)
    private val nebyEyes = Px.rgb(0x0A1C4D)

    private val gold = Px.rgb(0xFFCE5C)
    private val goldHi = Px.rgb(0xFFE9A3)
    private val goldLo = Px.rgb(0xD99A2B)
    private val blue = Px.rgb(0x2F64D6)
    private val blueHi = Px.rgb(0x6E99EE)
    private val sky = Px.rgb(0xDDEBFF)
    private val cloud = Px.rgb(0xF4F7FF)
    private val cloudLo = Px.rgb(0xC9D6F0)
    private val rain = Px.rgb(0x6F9BEA)
    private val steel = Px.rgb(0x8C97B3)
    private val steelHi = Px.rgb(0xB9C3DA)
    private val paper = Px.rgb(0xFFF8EA)
    private val paperLo = Px.rgb(0xEBD5B0)

    enum class Eyes { Open, Blink, Happy, Closed, Up }

    /** One pose of pixel Neby on a 32 x 32 canvas. */
    private fun PixelCanvas.neby(dy: Float, sx: Float = 1f, sy: Float = 1f, eyes: Eyes = Eyes.Open, look: Int = 0, phase: Float = 0f) {
        val cx = 16f
        val r = 10.5f
        val cy = 29f - r * sy + dy
        ellipse(cx, cy, r * sx, r * sy, nebyBody)
        // shade on the lower right of the dome, dithered
        for (y in 0 until height) for (x in 0 until width) {
            if (get(x, y) != nebyBody) continue
            val nx = (x + 0.5f - cx) / (r * sx); val ny = (y + 0.5f - cy) / (r * sy)
            if (nx * 0.6f + ny * 0.8f > 0.45f && Bayer.threshold(x, y) < (nx * 0.6f + ny * 0.8f - 0.45f) * 3f) set(x, y, nebyShade)
        }
        // the band, with Neby's wave on its top edge
        val bandTop = cy + r * sy * 0.32f
        for (y in 0 until height) for (x in 0 until width) {
            val c = get(x, y)
            if (c != nebyBody && c != nebyShade) continue
            val wave = bandTop + sin((x + phase) / 2.2f) * 0.9f
            if (y + 0.5f > wave + 1.4f) set(x, y, if (y + 0.5f > wave + 4f) nebyBand else nebyBandHi)
            else if (y + 0.5f > wave) set(x, y, nebyWave)
        }
        // highlight
        set((cx - r * sx * 0.55f).toInt(), (cy - r * sy * 0.55f).toInt(), white)
        set((cx - r * sx * 0.55f).toInt() + 1, (cy - r * sy * 0.55f).toInt(), white)
        set((cx - r * sx * 0.55f).toInt(), (cy - r * sy * 0.55f).toInt() + 1, white)
        // eyes
        val ex = (cx - 4f).roundToInt() + look
        val ey = (cy - 3f).roundToInt()
        for (e in intArrayOf(ex, ex + 6)) when (eyes) {
            Eyes.Open -> rect(e, ey, 2, 4, nebyEyes)
            Eyes.Up -> rect(e + 1, ey - 1, 2, 3, nebyEyes)
            Eyes.Blink -> rect(e, ey + 2, 2, 1, nebyEyes)
            Eyes.Closed -> { set(e - 1, ey + 2, nebyEyes); rect(e, ey + 3, 2, 1, nebyEyes); set(e + 2, ey + 2, nebyEyes) }
            Eyes.Happy -> { set(e - 1, ey + 2, nebyEyes); rect(e, ey + 1, 2, 1, nebyEyes); set(e + 2, ey + 2, nebyEyes) }
        }
        outline(line)
        // the shadow on the ground shrinks as Neby rises
        val lift = (-dy).coerceAtLeast(0f)
        val w = (9f - lift * 0.6f).coerceAtLeast(4f)
        for (x in (cx - w).toInt()..(cx + w).toInt()) if (get(x, 30) ushr 24 == 0) set(x, 30, shadow)
        for (x in (cx - w + 2).toInt()..(cx + w - 2).toInt()) if (get(x, 31) ushr 24 == 0) set(x, 31, shadow)
    }

    /** Neby idling: a breath, a glance, a blink. */
    val nebyIdle: PixelSprite by lazy {
        val dys = floatArrayOf(0f, 0f, -0.5f, -1f, -1f, -0.5f, 0f, 0f, -0.5f, -1f, -1f, -0.5f, 0f, 0f, 0f, 0f)
        PixelSprite.build(32, 32, dys.size, 120) { f ->
            val eyes = if (f == 13) Eyes.Blink else Eyes.Open
            val look = when (f) { in 5..8 -> 1; else -> 0 }
            neby(dys[f], eyes = eyes, look = look, phase = f * 0.6f)
        }
    }

    /** Neby hops for joy: squash, stretch, up, land. For success and "all done". */
    val nebyHop: PixelSprite by lazy {
        val poses = listOf(
            Triple(0f, 1f, 1f), Triple(0f, 1.12f, 0.86f), Triple(-2f, 0.92f, 1.1f), Triple(-5f, 0.96f, 1.04f),
            Triple(-6f, 1f, 1f), Triple(-5f, 1f, 1f), Triple(-2f, 0.96f, 1.04f), Triple(0f, 1.14f, 0.85f),
            Triple(0f, 1.04f, 0.96f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f),
        )
        PixelSprite.build(32, 32, poses.size, 75) { f ->
            val (dy, sx, sy) = poses[f]
            neby(dy, sx, sy, eyes = if (f in 2..7) Eyes.Happy else Eyes.Open, phase = f.toFloat())
        }
    }

    /** Neby thinking: eyes up, three dots filling in above. For loading and "working on it". */
    val nebyThink: PixelSprite by lazy {
        PixelSprite.build(32, 32, 8, 160) { f ->
            neby(if (f % 4 < 2) 0f else -0.5f, eyes = if (f == 6) Eyes.Blink else Eyes.Up, phase = f * 0.8f)
            val n = (f % 4)
            for (i in 0 until 3) {
                val x = 21 + i * 3
                val y = 3 - if (i < n) 1 else 0
                rect(x, y, 2, 2, if (i < n) blue else steelHi)
            }
        }
    }

    /** Neby asleep, small Zs drifting up. For quiet, empty places. */
    val nebySleep: PixelSprite by lazy {
        PixelSprite.build(32, 32, 12, 140) { f ->
            neby(if (f % 6 < 3) 0f else 0.5f, sx = 1.02f, sy = 0.98f, eyes = Eyes.Closed, phase = f * 0.3f)
            for (k in 0 until 2) {
                val t = ((f + k * 6) % 12) / 12f
                zed(this, 22 + (t * 4).toInt() + k, (10 - t * 9).toInt(), if (t < 0.8f) steel else steelHi)
            }
        }
    }

    /** A 3 x 3 "z". */
    private fun zed(c: PixelCanvas, x: Int, y: Int, color: Int) = with(c) {
        hline(x, x + 2, y, color); set(x + 1, y + 1, color); hline(x, x + 2, y + 2, color)
    }

    /** A bell, swaying and dozing: nothing new to ring for. */
    val sleepyBell: PixelSprite by lazy {
        PixelSprite.build(24, 24, 12, 120) { f ->
            val a = sin(2 * PI * f / 12).toFloat() * 0.16f
            val pivot = floatArrayOf(11.5f, 3f)
            fun rot(x: Float, y: Float): FloatArray {
                val c = cos(a); val s = sin(a)
                return floatArrayOf(pivot[0] + x * c - y * s, pivot[1] + x * s + y * c)
            }
            val body = listOf(-1.5f to 1f, 1.5f to 1f, 4.5f to 4f, 5.5f to 10f, 7.5f to 13f, -7.5f to 13f, -5.5f to 10f, -4.5f to 4f)
            val clap = rot(-a * 12f, 15f)
            disc(clap[0], clap[1], 1.6f, goldLo)
            val pts = FloatArray(body.size * 2)
            body.forEachIndexed { i, (x, y) -> val p = rot(x, y); pts[i * 2] = p[0]; pts[i * 2 + 1] = p[1] }
            polygon(pts, gold)
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == gold) {
                val local = (x + 0.5f - pivot[0]) * cos(a) + (y + 0.5f - pivot[1]) * sin(a)
                if (local > 2.5f) set(x, y, goldLo) else if (local < -3f && Bayer.threshold(x, y) < 0.5f) set(x, y, goldHi)
            }
            val knob = rot(0f, -0.5f)
            disc(knob[0], knob[1], 1.3f, goldLo)
            outline(line)
            val t = (f % 12) / 12f
            zed(this, 17 + (t * 3).toInt(), (9 - t * 8).toInt(), if (t < 0.75f) steel else steelHi)
        }
    }

    /** A magnifier sweeping for something that is not there, a glint crossing the glass. */
    val magnifier: PixelSprite by lazy {
        PixelSprite.build(24, 24, 10, 130) { f ->
            val sway = sin(2 * PI * f / 10).toFloat() * 1.6f
            val cx = 10f + sway; val cy = 10f
            // handle
            for (i in 0..6) { rect((cx + 4 + i).roundToInt(), (cy + 4 + i).roundToInt(), 2, 2, line) }
            disc(cx, cy, 6.5f, line)
            disc(cx, cy, 4.6f, sky)
            // a glint sweeping across the lens
            val g = ((f % 10) / 10f) * 12f - 6f
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == sky) {
                val d = (x + 0.5f - cx) - (y + 0.5f - cy) - g
                if (abs(d) < 1f) set(x, y, white)
            }
            set((cx - 2).roundToInt(), (cy - 3).roundToInt(), white)
            outline(line)
            // a question mark that comes and goes
            if (f % 10 >= 3) {
                val qx = 18; val qy = 1
                hline(qx, qx + 2, qy, blue); set(qx + 3, qy + 1, blue); set(qx + 2, qy + 2, blue); set(qx + 1, qy + 3, blue); set(qx + 1, qy + 5, blue)
            }
        }
    }

    /** A small rain cloud: something did not load. */
    val rainCloud: PixelSprite by lazy {
        PixelSprite.build(24, 24, 8, 95) { f ->
            val bob = if (f % 8 < 4) 0f else -0.5f
            disc(7.5f, 11f + bob, 4.5f, cloud); disc(12.5f, 8.5f + bob, 6f, cloud); disc(17.5f, 11.5f + bob, 4f, cloud)
            rect(4, (12 + bob).toInt(), 17, 3, cloud)
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == cloud && y >= 13 + bob) set(x, y, cloudLo)
            outline(line)
            for ((k, x) in intArrayOf(7, 12, 17).withIndex()) {
                val t = ((f + k * 3) % 8) / 8f
                val y = 17 + (t * 6).toInt()
                set(x, y, rain); set(x, y + 1, rain)
            }
        }
    }

    /** A bookmark ribbon waving: a place kept for later. */
    val ribbon: PixelSprite by lazy {
        PixelSprite.build(24, 24, 10, 110) { f ->
            for (y in 2..20) {
                val wave = (sin((y / 3.2f) - f * 2 * PI.toFloat() / 10) * 1.2f * (y - 2) / 18f).roundToInt()
                val notch = if (y > 16) (y - 16) else 0
                val left = 7 + wave; val right = 16 + wave
                if (notch == 0) hline(left, right, y, blue)
                else { hline(left, left + 4 - notch, y, blue); hline(right - 4 + notch, right, y, blue) }
            }
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == blue) {
                val left = (0 until width).first { get(it, y) == blue }
                if (x - left < 2) set(x, y, blueHi)
            }
            outline(line)
            if (f % 10 in 2..4) { set(19, 4, gold); set(18, 5, goldHi); set(20, 5, goldHi); set(19, 6, gold) }
        }
    }

    /** An arrow dropping into a tray, the tray taking it. For downloads. */
    val downloadTray: PixelSprite by lazy {
        PixelSprite.build(24, 24, 10, 90) { f ->
            // an open tray: two walls and a floor, the arrow drops in from above
            val bump = if (f == 7) 1 else 0
            rect(3, 12 + bump, 3, 9, steel); rect(18, 12 + bump, 3, 9, steel); rect(3, 18 + bump, 18, 3, steel)
            hline(4, 19, 19 + bump, steelHi)
            if (f < 7) {
                val y = (f * 2) - 1
                rect(11, y, 2, 6, blue)
                for (i in 0..3) hline(11 - i, 12 + i, y + 6 + (3 - i), blue)
            }
            outline(line)
            if (f >= 8) { set(9, 14, blue); set(10, 15, blue); set(11, 16, blue); set(12, 15, blue); set(13, 14, blue); set(14, 13, blue); set(15, 12, blue) }
        }
    }

    /** A chat bubble with someone typing. For quiet forums and threads. */
    val typing: PixelSprite by lazy {
        PixelSprite.build(24, 20, 6, 140) { f ->
            roundRect(2, 3, 20, 12, 3, white)
            set(6, 15, white); set(6, 16, white); set(5, 17, white)
            outline(line)
            for (i in 0 until 3) {
                val up = if ((f % 6) / 2 == i) 1 else 0
                rect(7 + i * 4, 8 - up, 2, 2, blue)
            }
        }
    }

    /** A small book with a page turning over and over. A loader for documents. */
    val bookLoader: PixelSprite by lazy {
        PixelSprite.build(32, 22, 12, 80) { f ->
            // cover and the two page blocks
            polygon(floatArrayOf(1f, 16f, 16f, 18f, 31f, 16f, 31f, 18.5f, 16f, 21f, 1f, 18.5f), blue)
            polygon(floatArrayOf(2f, 9f, 9f, 7.5f, 16f, 10f, 16f, 17f, 2f, 15.5f), paper)
            polygon(floatArrayOf(30f, 9f, 23f, 7.5f, 16f, 10f, 16f, 17f, 30f, 15.5f), paper)
            line(4, 14, 14, 15, paperLo); line(18, 15, 28, 14, paperLo)
            // the turning page, front then back
            val t = (f % 12) / 12f
            val th = PI * t
            val tipX = 16f + 14f * cos(th).toFloat()
            val tipY = 9f - 7f * sin(th).toFloat()
            polygon(floatArrayOf(16f, 10f, tipX, tipY, tipX, tipY + 6.5f, 16f, 17f), if (t < 0.5f) white else paperLo)
            outline(line)
        }
    }

    val all: List<Pair<String, PixelSprite>> by lazy {
        listOf(
            "nebyIdle" to nebyIdle, "nebyHop" to nebyHop, "nebyThink" to nebyThink, "nebySleep" to nebySleep,
            "sleepyBell" to sleepyBell, "magnifier" to magnifier, "rainCloud" to rainCloud, "ribbon" to ribbon,
            "downloadTray" to downloadTray, "typing" to typing, "bookLoader" to bookLoader,
        )
    }
}
