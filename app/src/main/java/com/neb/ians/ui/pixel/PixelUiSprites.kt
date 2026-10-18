package com.neb.ians.ui.pixel

import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Pixel sprites for the app's own states, 32 px objects and the 48 px Neby ([PixelNeby]): empty
 * inboxes, no results, offline, loading, the marketplace, payments, achievements. Each is drawn by
 * code (shape, shading, then a 1 px outline), so every frame is consistent and the set shares one
 * look. Played by PixelSpriteView; picked for empty states by [PixelStates].
 */
object PixelUiSprites {
    private val line = Px.rgb(0x1E2A4A)
    private val white = Px.rgb(0xFFFFFF)
    private val gold = Px.rgb(0xFFCE5C)
    private val goldHi = Px.rgb(0xFFEBA8)
    private val goldLo = Px.rgb(0xD99A2B)
    private val blue = Px.rgb(0x2F64D6)
    private val blueHi = Px.rgb(0x6E99EE)
    private val blueLo = Px.rgb(0x2450B4)
    private val sky = Px.rgb(0xDDEBFF)
    private val cloud = Px.rgb(0xF4F7FF)
    private val cloudLo = Px.rgb(0xC9D6F0)
    private val rain = Px.rgb(0x6F9BEA)
    private val steel = Px.rgb(0x8C97B3)
    private val steelHi = Px.rgb(0xB9C3DA)
    private val paper = Px.rgb(0xFFF8EA)
    private val paperLo = Px.rgb(0xEBD5B0)
    private val red = Px.rgb(0xE5484D)
    private val redHi = Px.rgb(0xFF8A8F)

    // Neby: the 48 px set
    val nebyIdle get() = PixelNeby.idle
    val nebyHop get() = PixelNeby.hop
    val nebyThink get() = PixelNeby.think
    val nebySleep get() = PixelNeby.sleep
    val nebyWink get() = PixelNeby.wink

    private fun PixelCanvas.zed(x: Int, y: Int, color: Int) {
        hline(x, x + 3, y, color); set(x + 2, y + 1, color); set(x + 1, y + 2, color); hline(x, x + 3, y + 3, color)
    }

    /** A bell, swaying and dozing: nothing new to ring for. */
    val sleepyBell: PixelSprite by lazy {
        PixelSprite.build(32, 32, 12, 120) { f ->
            val a = sin(2 * PI * f / 12).toFloat() * 0.16f
            val px = 15.5f; val py = 4f
            fun rot(x: Float, y: Float) = floatArrayOf(px + x * cos(a) - y * sin(a), py + x * sin(a) + y * cos(a))
            val body = listOf(-2f to 1.5f, 2f to 1.5f, 6f to 5.5f, 7.5f to 13f, 10f to 17.5f, -10f to 17.5f, -7.5f to 13f, -6f to 5.5f)
            val clap = rot(-a * 16f, 20f)
            disc(clap[0], clap[1], 2.2f, goldLo)
            val pts = FloatArray(body.size * 2)
            body.forEachIndexed { i, (x, y) -> val p = rot(x, y); pts[i * 2] = p[0]; pts[i * 2 + 1] = p[1] }
            polygon(pts, gold)
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == gold) {
                val local = (x + 0.5f - px) * cos(a) + (y + 0.5f - py) * sin(a)
                val down = -(x + 0.5f - px) * sin(a) + (y + 0.5f - py) * cos(a)
                when {
                    down > 15.5f -> set(x, y, goldLo)
                    local > 3.5f -> set(x, y, goldLo)
                    local < -4f && Bayer.threshold(x, y) < 0.55f -> set(x, y, goldHi)
                }
            }
            val knob = rot(0f, -0.5f)
            disc(knob[0], knob[1], 1.8f, goldLo)
            outline(line)
            val t = (f % 12) / 12f
            zed(22 + (t * 4).toInt(), (12 - t * 11).toInt(), if (t < 0.75f) steel else steelHi)
        }
    }

    /** A magnifier sweeping for something that is not there, a glint crossing the glass. */
    val magnifier: PixelSprite by lazy {
        PixelSprite.build(32, 32, 10, 130) { f ->
            val sway = sin(2 * PI * f / 10).toFloat() * 2f
            val cx = 13f + sway; val cy = 13f
            for (i in 0..8) rect((cx + 5.5f + i).roundToInt(), (cy + 5.5f + i).roundToInt(), 3, 3, if (i > 3) Px.rgb(0x3A4A6E) else line)
            disc(cx, cy, 8.5f, steel)
            disc(cx, cy, 6.4f, sky)
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == steel && (x + 0.5f - cx) + (y + 0.5f - cy) < -4f) set(x, y, steelHi)
            val g = ((f % 10) / 10f) * 16f - 8f
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == sky) {
                val d = (x + 0.5f - cx) - (y + 0.5f - cy) - g
                if (abs(d) < 1.1f) set(x, y, white)
            }
            rect((cx - 3).roundToInt(), (cy - 4).roundToInt(), 2, 1, white)
            outline(line)
            if (f % 10 >= 3) {
                val qx = 24; val qy = 1
                hline(qx + 1, qx + 3, qy, blue); set(qx, qy + 1, blue); set(qx + 4, qy + 1, blue); set(qx + 4, qy + 2, blue)
                set(qx + 3, qy + 3, blue); set(qx + 2, qy + 4, blue); set(qx + 2, qy + 6, blue)
            }
        }
    }

    /** A small rain cloud: something did not load. */
    val rainCloud: PixelSprite by lazy {
        PixelSprite.build(32, 32, 8, 95) { f ->
            val bob = if (f % 8 < 4) 0f else -1f
            disc(10f, 14f + bob, 6f, cloud); disc(16.5f, 11f + bob, 8f, cloud); disc(23.5f, 15f + bob, 5.5f, cloud)
            rect(5, (16 + bob).toInt(), 23, 4, cloud)
            for (y in 0 until height) for (x in 0 until width) if (get(x, y) == cloud) {
                if (y >= 18 + bob) set(x, y, cloudLo) else if (y >= 16 + bob && Bayer.threshold(x, y) < 0.5f) set(x, y, cloudLo)
            }
            outline(line)
            for ((k, x) in intArrayOf(10, 16, 22).withIndex()) {
                val t = ((f + k * 3) % 8) / 8f
                val y = 23 + (t * 8).toInt()
                rect(x, y, 1, 2, rain)
            }
        }
    }

    /** A bookmark ribbon waving: a place kept for later. */
    val ribbon: PixelSprite by lazy {
        PixelSprite.build(32, 32, 10, 110) { f ->
            for (y in 3..27) {
                val wave = (sin((y / 4f) - f * 2 * PI.toFloat() / 10) * 1.6f * (y - 3) / 24f).roundToInt()
                val notch = if (y > 21) (y - 21) else 0
                val left = 10 + wave; val right = 21 + wave
                if (notch == 0) hline(left, right, y, blue)
                else { hline(left, left + 5 - notch, y, blue); hline(right - 5 + notch, right, y, blue) }
                if (notch == 0) { hline(left, left + 1, y, blueHi); set(right, y, blueLo) }
            }
            outline(line)
            if (f % 10 in 2..5) { set(25, 5, gold); set(24, 6, goldHi); set(26, 6, goldHi); set(25, 7, gold); set(25, 4, goldHi) }
        }
    }

    /** An arrow dropping into a tray, the tray taking it. For downloads. */
    val downloadTray: PixelSprite by lazy {
        PixelSprite.build(32, 32, 10, 90) { f ->
            val bump = if (f == 7) 1 else 0
            rect(4, 17 + bump, 4, 11, steel); rect(24, 17 + bump, 4, 11, steel); rect(4, 24 + bump, 24, 4, steel)
            hline(5, 26, 25 + bump, steelHi); rect(5, 17 + bump, 1, 8, steelHi)
            if (f < 7) {
                val y = f * 3 - 2
                rect(14, y, 4, 8, blue); rect(14, y, 1, 8, blueHi)
                for (i in 0..4) hline(15 - i - 1, 16 + i + 1, y + 8 + (4 - i), blue)
            }
            outline(line)
            if (f >= 8) for (i in 0..6) set(12 + i, (if (i < 2) 19 + i else 21 - (i - 2)), blue)
        }
    }

    /** A chat bubble with someone typing. For quiet forums and threads. */
    val typing: PixelSprite by lazy {
        PixelSprite.build(32, 26, 6, 140) { f ->
            roundRect(2, 3, 28, 16, 4, white)
            hline(4, 27, 17, sky)
            rect(8, 19, 2, 2, white); set(7, 21, white); set(6, 22, white)
            outline(line)
            for (i in 0 until 3) {
                val up = if ((f % 6) / 2 == i) 1 else 0
                rect(9 + i * 6, 10 - up, 3, 3, blue)
            }
        }
    }

    /** A small book with a page turning over and over. A loader for documents. */
    val bookLoader: PixelSprite by lazy {
        PixelSprite.build(48, 32, 14, 70) { f ->
            polygon(floatArrayOf(1f, 24f, 24f, 27f, 47f, 24f, 47f, 27.5f, 24f, 31f, 1f, 27.5f), blue)
            line(2, 25, 22, 28, blueHi); line(26, 28, 46, 25, blueHi)
            polygon(floatArrayOf(3f, 13f, 13f, 10.5f, 24f, 14.5f, 24f, 25.5f, 3f, 23f), paper)
            polygon(floatArrayOf(45f, 13f, 35f, 10.5f, 24f, 14.5f, 24f, 25.5f, 45f, 23f), paper)
            for (k in 0..2) { line(6, 16 + k * 2, 20, 18 + k * 2, paperLo); line(28, 18 + k * 2, 42, 16 + k * 2, paperLo) }
            line(24, 14, 24, 25, paperLo)
            val t = (f % 14) / 14f
            val th = PI * t
            val tipX = 24f + 21f * cos(th).toFloat()
            val tipY = 13.5f - 10f * sin(th).toFloat()
            polygon(floatArrayOf(24f, 14.5f, tipX, tipY, tipX, tipY + 10f, 24f, 25.5f), if (t < 0.5f) white else paperLo)
            outline(line)
        }
    }

    /** A padlock that jiggles now and then, a glint running down it. For locked or private content. */
    val padlock: PixelSprite by lazy {
        PixelSprite.build(32, 32, 12, 100) { f ->
            val jig = when (f) { 3 -> -1; 4 -> 1; 5 -> -1; else -> 0 }
            for (a in 0..36) {
                val t = PI * a / 36
                val x = 16f + jig + cos(t).toFloat() * 6.5f; val y = 13f - sin(t).toFloat() * 7f
                disc(x, y, 1.7f, steel)
            }
            rect(9 + jig, 13, 2, 3, steel); rect(21 + jig, 13, 2, 3, steel)
            roundRect(6 + jig, 15, 20, 14, 2, gold)
            hline(7 + jig, 24 + jig, 15, goldHi); rect(23 + jig, 16, 2, 12, goldLo)
            disc(16f + jig, 20.5f, 2.2f, line); rect(15 + jig, 21, 2, 4, line)
            val g = f % 12
            if (g in 7..10) for (y in 16..27) if (get(8 + jig + (g - 7) * 4 + (y - 16) / 3, y) == gold) set(8 + jig + (g - 7) * 4 + (y - 16) / 3, y, goldHi)
            outline(line)
        }
    }

    /** A folded newspaper, its corner lifting in a breeze. For news and blog. */
    val newspaper: PixelSprite by lazy {
        PixelSprite.build(32, 32, 8, 130) { f ->
            roundRect(4, 5, 24, 22, 1, paper)
            rect(7, 8, 18, 3, line)
            for (k in 0..3) { hline(7, 15, 13 + k * 2, paperLo); hline(18, 25, 13 + k * 2, paperLo) }
            rect(7, 22, 8, 3, sky)
            val lift = intArrayOf(0, 1, 2, 3, 3, 2, 1, 0)[f]
            if (lift > 0) polygon(floatArrayOf(27.5f - lift * 2, 26.5f, 27.5f, 26.5f - lift * 2, 27.5f - lift * 2 - 0.5f, 26.5f - lift * 2 - 0.5f), paperLo)
            outline(line)
        }
    }

    /** A coin turning in the light. For payments and earnings. */
    val coin: PixelSprite by lazy {
        PixelSprite.build(32, 32, 10, 85) { f ->
            val w = abs(cos(PI * f / 10)).toFloat()
            val rx = (10f * w).coerceAtLeast(1.4f)
            ellipse(16f, 16f, rx + 1.2f, 11.2f, goldLo)
            ellipse(16f, 16f, rx, 10f, gold)
            if (rx > 4f) {
                ellipse(16f, 16f, rx * 0.62f, 6.2f, goldHi)
                ellipse(16f, 16f, rx * 0.46f, 4.6f, gold)
                rect(15, 12, 2, 8, goldLo)
            }
            outline(line)
            if (f == 0 || f == 9) { set(25, 5, white); set(24, 6, goldHi); set(26, 6, goldHi); set(25, 7, white) }
        }
    }

    /** A push pin bobbing into the board. For pinned items. */
    val pushPin: PixelSprite by lazy {
        PixelSprite.build(32, 32, 8, 120) { f ->
            val dy = intArrayOf(0, -1, -2, -3, -3, -2, -1, 0)[f]
            ellipse(16f, 29f, (7f + dy).coerceAtLeast(4f), 1.4f, 0x26101830)
            rect(15, 17 + dy, 2, 9, steel)
            disc(16f, 11f + dy, 6.5f, red)
            roundRect(10, 15 + dy, 12, 3, 1, red)
            disc(14f, 9f + dy, 2f, redHi)
            outline(line)
        }
    }

    /** A little shop, its awning lifting in the wind. For the marketplace. */
    val storefront: PixelSprite by lazy {
        PixelSprite.build(32, 32, 8, 130) { f ->
            rect(5, 13, 22, 16, paper)
            rect(8, 18, 7, 11, blueLo); rect(9, 19, 5, 10, blue); set(13, 24, gold)
            rect(17, 17, 8, 7, sky); hline(17, 24, 20, white); set(18, 18, white)
            for (s in 0 until 6) {
                val x = 3 + s * 4
                val drop = if ((s + f) % 4 == 0) 1 else 0
                rect(x, 7, 4, 6 + drop, if (s % 2 == 0) blue else white)
            }
            hline(3, 26, 6, blueLo)
            outline(line)
        }
    }

    /** A trophy, a shine running across it and a star above. For leaderboards and achievements. */
    val trophy: PixelSprite by lazy {
        PixelSprite.build(32, 32, 12, 110) { f ->
            for (k in 0..6) set(7 - k / 3, 9 + k, goldLo).also { set(24 + k / 3, 9 + k, goldLo) }
            polygon(floatArrayOf(9f, 6f, 23f, 6f, 22f, 15f, 18f, 19f, 14f, 19f, 10f, 15f), gold)
            rect(14, 19, 4, 4, goldLo)
            roundRect(10, 23, 12, 4, 1, gold)
            hline(10, 21, 26, goldLo)
            val s = (f % 12) - 1
            if (s in 0..9) for (y in 6..18) { val x = 10 + s + (y - 6) / 3; if (get(x, y) == gold) set(x, y, goldHi) }
            outline(line)
            if (f % 12 in 4..8) { set(16, 1, gold); hline(15, 17, 2, goldHi); set(16, 3, gold) }
        }
    }

    val all: List<Pair<String, PixelSprite>> by lazy {
        listOf(
            "nebyIdle" to nebyIdle, "nebyHop" to nebyHop, "nebyThink" to nebyThink, "nebySleep" to nebySleep, "nebyWink" to nebyWink,
            "sleepyBell" to sleepyBell, "magnifier" to magnifier, "rainCloud" to rainCloud, "ribbon" to ribbon,
            "downloadTray" to downloadTray, "typing" to typing, "bookLoader" to bookLoader,
            "padlock" to padlock, "newspaper" to newspaper, "coin" to coin, "pushPin" to pushPin,
            "storefront" to storefront, "trophy" to trophy,
        )
    }
}
