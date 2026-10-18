package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.Bayer
import com.neb.ians.ui.pixel.PixelCanvas
import com.neb.ians.ui.pixel.Px
import kotlin.math.abs
import kotlin.math.roundToInt
import kotlin.math.sin

/** Shorthand for opaque colours. */
internal fun c(hex: Long): Int = Px.rgb(hex)

/** The line every prop is outlined in: a deep ink, never pure black. */
internal val INK = c(0x1B2238)

/** A tiny deterministic random source (xorshift), so a seed always draws the same picture. */
internal class Dice(seed: Int) {
    private var s = if (seed == 0) 0x2545F491 else seed
    fun next(): Float { s = s xor (s shl 13); s = s xor (s ushr 17); s = s xor (s shl 5); return ((s ushr 8) and 0xFFFFFF) / 16777216f }
    fun range(a: Float, b: Float) = a + (b - a) * next()
    fun int(n: Int) = (next() * n).toInt().coerceAtMost(n - 1)
}

/** Vertical gradient through [stops], dithered between neighbours, over rows [y0, y1). */
internal fun PixelCanvas.skyGradient(stops: IntArray, y0: Int = 0, y1: Int = height) {
    for (y in y0 until y1) {
        val t = (y - y0).toFloat() / (y1 - y0 - 1).coerceAtLeast(1)
        for (x in 0 until width) set(x, y, Px.ramp(stops, t, x, y))
    }
}

/** A ridge line across the canvas: summed sines for a seeded, natural-looking skyline. */
internal fun ridge(width: Int, base: Float, amp: Float, seed: Int, jag: Float = 1f): FloatArray {
    val d = Dice(seed)
    val f1 = d.range(0.03f, 0.06f); val f2 = d.range(0.08f, 0.14f); val f3 = d.range(0.2f, 0.35f)
    val p1 = d.range(0f, 6f); val p2 = d.range(0f, 6f); val p3 = d.range(0f, 6f)
    return FloatArray(width) { x ->
        base - amp * (0.55f * sin(x * f1 + p1) + 0.3f * sin(x * f2 + p2) + 0.15f * jag * sin(x * f3 + p3))
    }
}

/** Fills everything below [line] (one y per column) to [bottom] with [fill], lit along its top edge. */
internal fun PixelCanvas.fillBelow(line: FloatArray, fill: Int, rim: Int? = null, bottom: Int = height) {
    for (x in 0 until width) {
        val top = line[x.coerceIn(0, line.size - 1)].roundToInt()
        for (y in top.coerceAtLeast(0) until bottom) set(x, y, fill)
        if (rim != null) set(x, top, rim)
    }
}

/**
 * A snowy mountain range: rock below a wavering snow line, the slopes facing away from the light
 * (upper left) a tone darker, so each peak reads as a solid with a lit and a shaded side.
 */
internal fun PixelCanvas.mountains(line: FloatArray, rock: Int, rockShade: Int, snow: Int, snowShade: Int, snowDepth: Float, seed: Int) {
    val ph = (seed % 97) * 0.37f
    for (x in 0 until width) {
        val top = line[x].roundToInt()
        val slope = line[(x + 3).coerceAtMost(width - 1)] - line[(x - 3).coerceAtLeast(0)]
        val shaded = slope > 0.6f
        val snowLine = top + snowDepth + 1.4f * sin(x * 0.9f + ph) + 1.1f * sin(x * 0.37f + ph * 2f) + (if (shaded) 1f else 0f)
        for (y in top.coerceAtLeast(0) until height) {
            val isSnow = y < snowLine
            val edge = !isSnow && y < snowLine + 2 && Bayer.threshold(x, y) < 0.5f // snow streaks into the rock
            val col = when {
                isSnow || edge -> if (shaded) snowShade else snow
                shaded -> rockShade
                else -> rock
            }
            set(x, y, col)
        }
        // a lit ridge line on the sunny slopes
        if (!shaded && top >= 0) set(x, top, snow)
    }
}

/** Seeded stars, a few brighter ones with a cross glint. */
internal fun PixelCanvas.stars(seed: Int, count: Int, maxY: Int, dim: Int, bright: Int) {
    val d = Dice(seed)
    repeat(count) { k ->
        val x = d.int(width); val y = d.int(maxY)
        if (k % 7 == 0) { set(x, y, bright); set(x - 1, y, dim); set(x + 1, y, dim); set(x, y - 1, dim); set(x, y + 1, dim) }
        else set(x, y, if (k % 3 == 0) bright else dim)
    }
}

/** A disc with a dithered halo: suns and moons. */
internal fun PixelCanvas.glowDisc(cx: Float, cy: Float, r: Float, body: Int, halo: Int, haloR: Float) {
    for (y in (cy - haloR).toInt()..(cy + haloR).toInt()) for (x in (cx - haloR).toInt()..(cx + haloR).toInt()) {
        val dd = kotlin.math.hypot(x + 0.5f - cx, y + 0.5f - cy)
        if (dd in r..haloR && Bayer.threshold(x, y) < (1f - (dd - r) / (haloR - r)) * 0.6f) set(x, y, halo)
    }
    disc(cx, cy, r, body)
}

/** A crescent moon: a disc with a second disc of the sky taken out of it. */
internal fun PixelCanvas.crescent(cx: Float, cy: Float, r: Float, body: Int, sky: (Int, Int) -> Int) {
    disc(cx, cy, r, body)
    for (y in (cy - r).toInt() - 1..(cy + r).toInt() + 1) for (x in (cx - r).toInt() - 1..(cx + r).toInt() + 1) {
        if (kotlin.math.hypot(x + 0.5f - (cx + r * 0.45f), y + 0.5f - (cy - r * 0.25f)) <= r * 0.85f) set(x, y, sky(x, y))
    }
}

/** A puffy cumulus: overlapping discs, a lit top and a flat, shaded base. Drawn on its own layer, so clouds overlap cleanly. */
internal fun PixelCanvas.cloud(cx: Float, base: Float, w: Float, body: Int, light: Int, shade: Int, seed: Int) {
    val d = Dice(seed)
    val l = PixelCanvas(width, height)
    val n = (w / 6f).toInt().coerceAtLeast(2)
    val puffs = List(n) { i ->
        val x = cx - w / 2 + (i + 0.5f) * w / n + d.range(-1.5f, 1.5f)
        val r = (w / n) * d.range(0.75f, 1.1f) * (if (i == n / 2) 1.35f else 1f)
        Triple(x, base - r * 0.7f, r)
    }
    for ((x, y, r) in puffs) l.disc(x, y, r, body)
    for ((x, y, r) in puffs) for (yy in (y - r).toInt()..(y - r * 0.2f).toInt()) for (xx in (x - r).toInt()..(x + r).toInt()) {
        if (kotlin.math.hypot(xx + 0.5f - x + r * 0.25f, yy + 0.5f - y + r * 0.3f) < r * 0.7f && l.get(xx, yy) == body) l.set(xx, yy, light)
    }
    val b = base.toInt()
    for (xx in 0 until width) {
        for (yy in b - 2..b) if (l.get(xx, yy) == body && (yy == b || Bayer.threshold(xx, yy) < 0.5f)) l.set(xx, yy, shade)
        for (yy in b + 1 until height) if (yy >= 0) l.pixels[yy * width + xx] = 0
    }
    for (i in pixels.indices) if ((l.pixels[i] ushr 24) != 0) pixels[i] = l.pixels[i]
}

/**
 * Props are drawn on their own layer, outlined there, then laid over the scene, so an outline is
 * always one clean pixel whatever the backdrop behind it.
 */
internal fun PixelCanvas.prop(outline: Int = INK, draw: PixelCanvas.() -> Unit) {
    val layer = PixelCanvas(width, height)
    layer.draw()
    layer.outline(outline)
    for (i in pixels.indices) if ((layer.pixels[i] ushr 24) != 0) pixels[i] = layer.pixels[i]
}

/** Draws on top of everything without an outline: glints, sparks, fine lines. */
internal fun PixelCanvas.detail(draw: PixelCanvas.() -> Unit) = draw()

/** A soft contact shadow under a prop: the ground darkened toward [shade], dithered at the edges. */
internal fun PixelCanvas.contactShadow(cx: Int, y: Int, halfW: Int, shade: Int) {
    for (x in cx - halfW..cx + halfW) {
        val t = abs(x - cx).toFloat() / halfW
        if (Bayer.threshold(x, y) < 1f - t * 0.8f) set(x, y, Px.mix(get(x, y), shade, 0.7f))
        if (t < 0.6f && Bayer.threshold(x, y + 1) < 0.5f - t) set(x, y + 1, Px.mix(get(x, y + 1), shade, 0.5f))
    }
}

/** Shades a rectangle top-lit: a light top row, the face, a dark bottom row. */
internal fun PixelCanvas.box(x: Int, y: Int, w: Int, h: Int, face: Int, light: Int, dark: Int) {
    rect(x, y, w, h, face); hline(x, x + w - 1, y, light); hline(x, x + w - 1, y + h - 1, dark)
}

/** Picks between two colours across a span with ordered dithering. */
internal fun dith(a: Int, b: Int, t: Float, x: Int, y: Int): Int = if (t > Bayer.threshold(x, y)) b else a
