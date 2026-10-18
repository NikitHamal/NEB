package com.neb.ians.ui.pixel

import kotlin.math.PI
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.floor
import kotlin.math.pow
import kotlin.math.roundToInt
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.random.Random

/**
 * The auth hero, in pixels: an open book floating in a dawn sky. Rendered into a
 * [WIDTH] x [HEIGHT] buffer and scaled up crisp by the view.
 *
 * Layers, back to front: a dithered sky that slowly warms and cools; a sun glow behind the
 * book with turning rays; high clouds drifting slowly, mid clouds a little faster; birds now
 * and then; the book, bobbing, turning a page every few seconds; sparkles around it; motes
 * rising; a bank of near clouds; and a fade to [ground] at the bottom.
 *
 * Everything is a function of time, so any frame can be rendered on its own (and tested).
 */
class PixelSkyScene(private val ground: Int = Px.rgb(0xFFFFFF)) {
    val canvas = PixelCanvas(WIDTH, HEIGHT)

    private val skyStops = intArrayOf(
        Px.rgb(0x86A9D6), Px.rgb(0x9DB8DF), Px.rgb(0xB7C6E6), Px.rgb(0xD4CBE3),
        Px.rgb(0xEACAD2), Px.rgb(0xF6D0C2), Px.rgb(0xFCDCC4), Px.rgb(0xFDE8D6)
    )
    private val warmStops = intArrayOf(
        Px.rgb(0x8EAAD4), Px.rgb(0xA9BADF), Px.rgb(0xC6C5E2), Px.rgb(0xE3C8DA),
        Px.rgb(0xF4C9C6), Px.rgb(0xFBD0B8), Px.rgb(0xFEDDBE), Px.rgb(0xFFEBD3)
    )
    private val glow = Px.rgb(0xFFF3D2)
    private val glowHot = Px.rgb(0xFFFBEF)

    private class Drifter(val sprite: PixelSprite, var x: Float, val y: Int, val speed: Float)

    private val rnd = Random(7)
    private val high = List(4) { i ->
        Drifter(
            PixelSprites.cloud(11 + i, 44 + rnd.nextInt(24), 18 + rnd.nextInt(6), Px.rgb(0xF4F0F6), Px.rgb(0xDCDDED), Px.rgb(0xC4CAE3)),
            rnd.nextFloat() * WIDTH * 1.4f - 20f, 26 + i * 24 + rnd.nextInt(8), 1.6f + rnd.nextFloat() * 1f
        )
    }
    private val mid = List(4) { i ->
        Drifter(
            PixelSprites.cloud(31 + i, 54 + rnd.nextInt(28), 22 + rnd.nextInt(7), Px.rgb(0xFFF6F0), Px.rgb(0xF8DCD6), Px.rgb(0xEDBFC0)),
            rnd.nextFloat() * WIDTH * 1.4f - 30f, 128 + i * 15 + rnd.nextInt(8), 3f + rnd.nextFloat() * 1.4f
        )
    }
    private val near = List(6) { i ->
        Drifter(
            PixelSprites.cloud(57 + i, 76 + rnd.nextInt(40), 32 + rnd.nextInt(10), Px.rgb(0xFFFDFB), Px.rgb(0xFCE6E0), Px.rgb(0xF2CFCB)),
            i * 50f - 26f + rnd.nextInt(12), 286 + (i % 3) * 12 + rnd.nextInt(6), 5f + rnd.nextFloat() * 1.8f
        )
    }

    private class Mote(val x: Float, val phase: Float, val speed: Float, val warm: Boolean)
    private val motes = List(28) { Mote(BOOK_X - 60f + rnd.nextFloat() * 120f, rnd.nextFloat(), 5f + rnd.nextFloat() * 6f, rnd.nextBoolean()) }

    private val sparkles = List(7) {
        val a = rnd.nextFloat() * 2f * PI.toFloat()
        val d = 34f + rnd.nextFloat() * 34f
        Triple((BOOK_X + cos(a) * d * 1.4f).toInt(), (BOOK_Y - 10 + sin(a) * d * 0.8f).toInt(), rnd.nextInt(4000))
    }

    fun render(timeMs: Long) {
        val t = timeMs / 1000f
        val c = canvas
        val warmth = (sin(t * 2f * PI.toFloat() / 9f) * 0.5f + 0.5f) * 0.6f
        sky(c, warmth)
        rays(c, t)
        drift(c, high, t)
        birds(c, t)
        drift(c, mid, t)
        book(c, t, timeMs)
        sparkles(c, timeMs)
        motes(c, t)
        drift(c, near, t)
        groundFade(c)
    }

    private fun sky(c: PixelCanvas, warmth: Float) {
        val px = c.pixels
        for (y in 0 until HEIGHT) {
            val ty = y / (HEIGHT * 0.86f)
            for (x in 0 until WIDTH) {
                val cool = Px.ramp(skyStops, ty, x, y)
                px[y * WIDTH + x] = if (warmth > Bayer.threshold(x + 2, y + 1) * 1.0f) Px.ramp(warmStops, ty, x, y) else cool
            }
        }
    }

    private fun rays(c: PixelCanvas, t: Float) {
        val turn = t * 0.06f
        val r0 = 150f
        for (y in maxOf(0, BOOK_Y - 150) until minOf(HEIGHT, BOOK_Y + 110)) {
            for (x in 0 until WIDTH) {
                val dx = (x - BOOK_X).toFloat(); val dy = (y - BOOK_Y + 2).toFloat() * 1.15f
                val d = sqrt(dx * dx + dy * dy)
                if (d > r0) continue
                val fall = 1f - d / r0
                val ang = atan2(dy, dx)
                val ray = cos(ang * 9f + turn).pow(2f).let { it * it } * fall.pow(1.4f) * 0.7f
                val core = fall.pow(2.6f)
                val amount = (core * 1.1f + ray).coerceAtMost(1f)
                // below a floor the dither turns into lone specks, which read as noise, not light
                if (amount > 0.1f) c.dither(x, y, glow, amount)
                if (core > 0.42f) c.dither(x, y, glowHot, (core - 0.42f) * 2.2f)
            }
        }
    }

    private fun drift(c: PixelCanvas, list: List<Drifter>, t: Float) {
        val span = WIDTH + 120f
        for (d in list) {
            val x = floor(((d.x + t * d.speed) % span + span) % span - 70f).toInt()
            c.blit(d.sprite, 0, x, d.y - d.sprite.height)
        }
    }

    private fun birds(c: PixelCanvas, t: Float) {
        val period = 14f
        val k = (t % period) / period
        if (k > 0.62f) return
        val bx = (-14f + k / 0.62f * (WIDTH + 28f)).toInt()
        val by = 92 + (sin(t * 1.3f) * 3f).roundToInt()
        val frameMs = (t * 1000).toLong()
        c.blit(PixelSprites.bird, PixelSprites.bird.frameAt(frameMs), bx, by)
        c.blit(PixelSprites.bird, PixelSprites.bird.frameAt(frameMs + 160), bx - 11, by + 6)
        c.blit(PixelSprites.bird, PixelSprites.bird.frameAt(frameMs + 70), bx - 20, by - 3)
    }

    private fun book(c: PixelCanvas, t: Float, timeMs: Long) {
        val sprite = PixelSprites.book
        val bob = (sin(t * 2f * PI.toFloat() / 3.4f) * 2.2f).roundToInt()
        // idle (breathing pages) most of the time; a page turns every 4.2 s
        val cycle = timeMs % 4200L
        val flipStart = 4200L - PixelSprites.BOOK_FLIP * sprite.frameMs
        val frame = if (cycle >= flipStart) {
            PixelSprites.BOOK_IDLE + ((cycle - flipStart) / sprite.frameMs).toInt().coerceAtMost(PixelSprites.BOOK_FLIP - 1)
        } else {
            ((timeMs / 420L) % PixelSprites.BOOK_IDLE).toInt()
        }
        c.blit(sprite, frame, BOOK_X - PixelSprites.BOOK_W / 2, BOOK_Y - 42 + bob)
    }

    private fun sparkles(c: PixelCanvas, timeMs: Long) {
        val s = PixelSprites.sparkle
        for ((x, y, offset) in sparkles) {
            val local = (timeMs + offset) % 2600L
            if (local < s.durationMs) c.blit(s, s.frameAt(local), x - 2, y - 2)
        }
    }

    private fun motes(c: PixelCanvas, t: Float) {
        val warm = Px.rgb(0xFFE6A6); val pale = Px.rgb(0xFFFFFF)
        for (m in motes) {
            val life = ((t * m.speed / 60f) + m.phase) % 1f
            val y = (BOOK_Y + 40 - life * 170f).toInt()
            val x = (m.x + sin((t + m.phase * 10f) * 1.7f) * 3f).toInt()
            val fade = sin(life * PI.toFloat())
            c.dither(x, y, if (m.warm) warm else pale, fade * 1.3f)
        }
    }

    private fun groundFade(c: PixelCanvas) {
        val start = HEIGHT - 78
        for (y in start until HEIGHT) {
            val k = ((y - start) / 70f).coerceIn(0f, 1f)
            for (x in 0 until WIDTH) c.dither(x, y, ground, k * 1.08f)
        }
    }

    companion object {
        const val WIDTH = 216
        const val HEIGHT = 384
        const val BOOK_X = 108
        const val BOOK_Y = 200
    }
}
