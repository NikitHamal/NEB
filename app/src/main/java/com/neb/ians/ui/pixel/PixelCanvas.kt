package com.neb.ians.ui.pixel

import kotlin.math.abs
import kotlin.math.roundToInt

/**
 * A tiny ARGB framebuffer and the handful of primitives pixel art needs: plot, spans, lines,
 * polygons, ordered dithering and sprite blits. Pure Kotlin (no Android types) so scenes can be
 * rendered and checked in a plain JVM unit test.
 */
class PixelCanvas(val width: Int, val height: Int) {
    val pixels = IntArray(width * height)

    fun fill(color: Int) = pixels.fill(color)

    fun set(x: Int, y: Int, color: Int) {
        if (x in 0 until width && y in 0 until height && (color ushr 24) != 0) pixels[y * width + x] = color
    }

    fun get(x: Int, y: Int): Int = if (x in 0 until width && y in 0 until height) pixels[y * width + x] else 0

    fun hline(x0: Int, x1: Int, y: Int, color: Int) {
        if (y !in 0 until height) return
        val a = maxOf(0, minOf(x0, x1)); val b = minOf(width - 1, maxOf(x0, x1))
        for (x in a..b) pixels[y * width + x] = color
    }

    fun rect(x: Int, y: Int, w: Int, h: Int, color: Int) {
        for (yy in y until y + h) hline(x, x + w - 1, yy, color)
    }

    fun line(x0: Int, y0: Int, x1: Int, y1: Int, color: Int) {
        var x = x0; var y = y0
        val dx = abs(x1 - x0); val dy = -abs(y1 - y0)
        val sx = if (x0 < x1) 1 else -1; val sy = if (y0 < y1) 1 else -1
        var err = dx + dy
        while (true) {
            set(x, y, color)
            if (x == x1 && y == y1) return
            val e2 = 2 * err
            if (e2 >= dy) { err += dy; x += sx }
            if (e2 <= dx) { err += dx; y += sy }
        }
    }

    /** Even-odd scanline fill of a polygon given as x0,y0,x1,y1,... in pixel units. */
    fun polygon(points: FloatArray, color: Int) {
        val n = points.size / 2
        var minY = Float.MAX_VALUE; var maxY = -Float.MAX_VALUE
        for (i in 0 until n) { minY = minOf(minY, points[i * 2 + 1]); maxY = maxOf(maxY, points[i * 2 + 1]) }
        val xs = FloatArray(n)
        for (y in maxOf(0, minY.toInt())..minOf(height - 1, maxY.toInt())) {
            val sy = y + 0.5f
            var count = 0
            for (i in 0 until n) {
                val ax = points[i * 2]; val ay = points[i * 2 + 1]
                val bx = points[((i + 1) % n) * 2]; val by = points[((i + 1) % n) * 2 + 1]
                if ((ay <= sy && by > sy) || (by <= sy && ay > sy)) {
                    xs[count++] = ax + (sy - ay) / (by - ay) * (bx - ax)
                }
            }
            xs.sort(0, count)
            var k = 0
            while (k + 1 < count) {
                hline(xs[k].roundToInt(), (xs[k + 1] - 0.5f).roundToInt(), y, color)
                k += 2
            }
        }
    }

    /** A filled disc centred on (cx, cy); half-pixel centres give even-width discs. */
    fun disc(cx: Float, cy: Float, r: Float, color: Int) {
        val r2 = r * r
        for (y in (cy - r).toInt() - 1..(cy + r).toInt() + 1) for (x in (cx - r).toInt() - 1..(cx + r).toInt() + 1) {
            val dx = x + 0.5f - cx; val dy = y + 0.5f - cy
            if (dx * dx + dy * dy <= r2) set(x, y, color)
        }
    }

    /** An ellipse, for shadows and lenses. */
    fun ellipse(cx: Float, cy: Float, rx: Float, ry: Float, color: Int) {
        for (y in (cy - ry).toInt() - 1..(cy + ry).toInt() + 1) for (x in (cx - rx).toInt() - 1..(cx + rx).toInt() + 1) {
            val dx = (x + 0.5f - cx) / rx; val dy = (y + 0.5f - cy) / ry
            if (dx * dx + dy * dy <= 1f) set(x, y, color)
        }
    }

    /** A rectangle with its corners cut by [r] pixels (pixel-art rounding). */
    fun roundRect(x: Int, y: Int, w: Int, h: Int, r: Int, color: Int) {
        for (yy in 0 until h) {
            val d = minOf(yy, h - 1 - yy)
            val cut = if (d < r) r - d else 0
            hline(x + cut, x + w - 1 - cut, y + yy, color)
        }
    }

    /** Replaces every pixel of [from] with [to]: palette swaps for states (on/off, lit/dim). */
    fun swap(from: Int, to: Int) {
        for (i in pixels.indices) if (pixels[i] == from) pixels[i] = to
    }

    /**
     * Outlines whatever has been drawn: every transparent pixel touching an opaque one becomes
     * [color]. Draw the shape, then call this, and the sprite gets the clean 1 px line pixel art
     * is read by.
     */
    fun outline(color: Int) {
        val src = pixels.copyOf()
        for (y in 0 until height) for (x in 0 until width) {
            if ((src[y * width + x] ushr 24) != 0) continue
            var touch = false
            if (x > 0 && (src[y * width + x - 1] ushr 24) != 0) touch = true
            if (x < width - 1 && (src[y * width + x + 1] ushr 24) != 0) touch = true
            if (y > 0 && (src[(y - 1) * width + x] ushr 24) != 0) touch = true
            if (y < height - 1 && (src[(y + 1) * width + x] ushr 24) != 0) touch = true
            if (touch) pixels[y * width + x] = color
        }
    }

    /** Plots [color] where an ordered-dither threshold says [amount] (0..1) of the pixels should be. */
    fun dither(x: Int, y: Int, color: Int, amount: Float) {
        if (amount > Bayer.threshold(x, y)) set(x, y, color)
    }

    fun blit(sprite: PixelSprite, frame: Int, x: Int, y: Int, flipX: Boolean = false) {
        val data = sprite.frames[Math.floorMod(frame, sprite.frames.size)]
        for (sy in 0 until sprite.height) {
            val ty = y + sy
            if (ty !in 0 until height) continue
            for (sx in 0 until sprite.width) {
                val c = data[sy * sprite.width + if (flipX) sprite.width - 1 - sx else sx]
                if ((c ushr 24) != 0) {
                    val tx = x + sx
                    if (tx in 0 until width) pixels[ty * width + tx] = c
                }
            }
        }
    }

    /** Like [blit], but only a dithered fraction [amount] of the sprite's pixels land. */
    fun blitDithered(sprite: PixelSprite, frame: Int, x: Int, y: Int, amount: Float) {
        val data = sprite.frames[Math.floorMod(frame, sprite.frames.size)]
        for (sy in 0 until sprite.height) for (sx in 0 until sprite.width) {
            val c = data[sy * sprite.width + sx]
            if ((c ushr 24) != 0) dither(x + sx, y + sy, c, amount)
        }
    }
}

/** 4x4 ordered dither: the classic, stable pattern that reads as "pixel art" rather than noise. */
object Bayer {
    private val m = intArrayOf(0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5)
    fun threshold(x: Int, y: Int): Float = (m[(y and 3) * 4 + (x and 3)] + 0.5f) / 16f
}

/** Colour helpers on packed ARGB ints. */
object Px {
    fun rgb(hex: Long): Int = (0xFF000000 or hex).toInt()

    fun mix(a: Int, b: Int, t: Float): Int {
        val k = t.coerceIn(0f, 1f)
        fun ch(shift: Int) = (((a shr shift) and 0xFF) + (((b shr shift) and 0xFF) - ((a shr shift) and 0xFF)) * k).roundToInt()
        return (0xFF shl 24) or (ch(16) shl 16) or (ch(8) shl 8) or ch(0)
    }

    /** Posterised gradient: picks between the two nearest [stops] with ordered dithering. */
    fun ramp(stops: IntArray, t: Float, x: Int, y: Int): Int {
        val f = t.coerceIn(0f, 0.9999f) * (stops.size - 1)
        val i = f.toInt()
        return if (f - i > Bayer.threshold(x, y)) stops[i + 1] else stops[i]
    }
}
