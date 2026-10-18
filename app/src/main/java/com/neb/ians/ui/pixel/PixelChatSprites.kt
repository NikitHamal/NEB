package com.neb.ians.ui.pixel

import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Hand-drawn pixel loaders for the Neby chat: what Neby is doing while you wait. Each is drawn
 * frame by frame in code with the same palette and 1 px outline as the rest of the pixel set,
 * timed so the loops are seamless.
 *
 * - [thinking]: three orbs riding a wave, squashing as they touch down, a spark trailing.
 * - [writing]: a pencil writing a line of script across a strip of paper, then wiping it.
 * - [reading]: a page being scanned, its lines turning blue as the beam passes.
 * - [sparkle]: a four-point star burst, played once when an answer lands.
 */
object PixelChatSprites {
    private val line = Px.rgb(0x1E2A4A)
    private val white = Px.rgb(0xFFFFFF)
    private val blue = Px.rgb(0x2F64D6)
    private val blueHi = Px.rgb(0x6E99EE)
    private val blueLo = Px.rgb(0x2450B4)
    private val sky = Px.rgb(0xDDEBFF)
    private val gold = Px.rgb(0xFFCE5C)
    private val goldHi = Px.rgb(0xFFEBA8)
    private val paper = Px.rgb(0xFFF8EA)
    private val paperLo = Px.rgb(0xEBD5B0)
    private val wood = Px.rgb(0xE5A24A)
    private val woodLo = Px.rgb(0xB8742A)
    private val pink = Px.rgb(0xF08FA8)
    private val graphite = Px.rgb(0x3A4560)

    val thinking: PixelSprite by lazy {
        val n = 18
        PixelSprite.build(30, 14, n, 55) { f ->
            val t = f / n.toFloat()
            for (i in 0 until 3) {
                val phase = (t - i * 0.16f) * 2f * PI.toFloat()
                val s = sin(phase)
                val cx = 6f + i * 9f
                val cy = 7.5f - s * 3.2f
                val squash = if (s < -0.7f) 1 else 0
                val ry = 2.6f - squash * 0.7f
                val rx = 2.6f + squash * 0.6f
                ellipse(cx, cy, rx, ry, if (i == 1) blue else blueHi)
                set(cx.roundToInt() - 1, (cy - ry + 1).roundToInt(), white)
                if (s > 0.8f) set(cx.roundToInt() + 2, (cy - 3.6f).roundToInt(), gold)
            }
            outline(line)
        }
    }

    val writing: PixelSprite by lazy {
        val n = 24
        PixelSprite.build(36, 22, n, 70) { f ->
            roundRect(1, 13, 34, 8, 2, paper)
            hline(3, 32, 19, paperLo)
            outline(line)
            val write = (f / (n * 0.75f)).coerceAtMost(1f)
            val wipe = ((f - n * 0.75f) / (n * 0.25f)).coerceIn(0f, 1f)
            val endX = 4 + (28 * write).roundToInt()
            var tipX = 4f; var tipY = 16f
            for (x in 4..endX) {
                val y = 16f + sin(x * 0.9f) * 1.4f + (if (x % 7 == 3) -1f else 0f)
                val gone = wipe > 0f && x < 4 + 28 * wipe
                if (!gone) set(x, y.roundToInt(), graphite)
                tipX = x.toFloat(); tipY = y
            }
            if (wipe > 0f) {
                val wx = 4 + (28 * wipe).roundToInt()
                rect(wx - 1, 14, 3, 5, pink)
            }
            val bob = if (f % 2 == 0) 0 else 1
            val px = if (wipe > 0f) 4f + 28f * wipe else tipX
            val py = if (wipe > 0f) 12f else tipY - 1f + bob
            for (k in 0..8) {
                val x = (px + k * 0.9f).roundToInt(); val y = (py - k * 1.15f).roundToInt()
                val c = when { k < 2 -> graphite; k < 3 -> paperLo; k < 7 -> wood; else -> pink }
                set(x, y, c); set(x + 1, y, if (k in 3..6) woodLo else c)
            }
            if (write < 1f && f % 3 == 0) set(px.roundToInt() - 1, py.roundToInt() - 2, gold)
        }
    }

    val reading: PixelSprite by lazy {
        val n = 20
        PixelSprite.build(26, 30, n, 75) { f ->
            roundRect(3, 2, 20, 26, 2, paper)
            polygon(floatArrayOf(17f, 2f, 23f, 8f, 17f, 8f), paperLo)
            outline(line)
            val beam = 4 + ((f / n.toFloat()) * 23f).roundToInt()
            for (r in 0 until 8) {
                val y = 7 + r * 2 + (if (r > 3) 1 else 0)
                val w = if (r % 3 == 2) 9 else 14
                hline(6, 5 + w, y, if (y < beam) blue else paperLo)
            }
            if (beam in 3..27) {
                hline(4, 21, beam, blueHi)
                for (x in 4..21) if ((x + f) % 3 == 0) set(x, beam - 1, sky)
            }
        }
    }

    val sparkle: PixelSprite by lazy {
        val n = 10
        PixelSprite.build(17, 17, n, 55, loop = false) { f ->
            val t = f / (n - 1f)
            val r = (2 + 6 * sin(t * PI)).roundToInt()
            val c = if (t < 0.6f) gold else goldHi
            for (k in 0..r) {
                val a = if (k == r) goldHi else c
                set(8 + k, 8, a); set(8 - k, 8, a); set(8, 8 + k, a); set(8, 8 - k, a)
            }
            if (t > 0.3f) {
                val d = (r * 0.55f).roundToInt()
                for (s in listOf(-1, 1)) for (u in listOf(-1, 1)) set(8 + s * d, 8 + u * d, white)
            }
            set(8, 8, white)
            if (abs(t - 0.5f) < 0.3f) outline(line)
        }
    }

    /** A blinking block caret for the end of streaming text (two frames). */
    val caret: PixelSprite by lazy {
        PixelSprite.build(4, 12, 2, 420) { f ->
            if (f == 0) rect(0, 1, 3, 10, blue)
            else for (y in 1..10) set(1, y, blueLo)
            if (f == 0) set(0, 1, blueHi)
        }
    }

}
