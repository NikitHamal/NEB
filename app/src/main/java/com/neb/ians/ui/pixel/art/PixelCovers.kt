package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.Bayer
import com.neb.ians.ui.pixel.NebyLook
import com.neb.ians.ui.pixel.PixelCanvas
import com.neb.ians.ui.pixel.PixelNeby
import com.neb.ians.ui.pixel.Px
import kotlin.math.abs
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Profile covers in pixel art: a Nepali panorama for each role, at dawn, at dusk or at night
 * (picked by a hash of the user, so a profile keeps its cover). Covers are 192 x 64, dark enough
 * that the white type laid over them always reads; [inkFor] says which tints to use over each.
 */
object PixelCovers {
    const val WIDTH = 192
    const val HEIGHT = 64
    const val VARIANTS = 3
    val ROLES = listOf("MEMBER", "VERIFIED", "TUTOR", "INSTITUTION", "MODERATOR", "ADMIN", "BOT")

    private enum class Time { Dawn, Dusk, Night }

    private class Palette(val sky: IntArray, val rock: Int, val rockShade: Int, val snow: Int, val snowShade: Int, val hill: Int, val hillFar: Int, val glow: Int)

    private fun palette(t: Time, tint: Int): Palette {
        fun k(v: Long, amt: Float = 0.22f) = Px.mix(c(v), tint, amt)
        return when (t) {
            Time.Dawn -> Palette(intArrayOf(k(0x22346E), k(0x5A5A9A), k(0xC98AA8, 0.1f), k(0xFFC9A0, 0.05f)), k(0x5E5C8E), k(0x46457A), c(0xFFE3D0), k(0xC7AECF, 0.1f), k(0x2A2E52), k(0x3E4272), c(0xFFE6B8))
            Time.Dusk -> Palette(intArrayOf(k(0x161B44), k(0x4A2F6E), k(0xA4507A, 0.1f), k(0xF2915E, 0.05f)), k(0x3C3264), k(0x2D2650), c(0xF7C2A8), k(0xB98AA8, 0.1f), k(0x1C1838), k(0x2C2650), c(0xFFC48A))
            Time.Night -> Palette(intArrayOf(k(0x040816), k(0x0B1636), k(0x16275A), k(0x22386E)), k(0x1C2848), k(0x141E3A), c(0xA9BAE2), k(0x7486B6), k(0x0B1226), k(0x16223F), c(0xFFF2CC))
        }
    }

    private val tints = mapOf(
        "MEMBER" to c(0x3A4C6E), "VERIFIED" to c(0x2C6BE0), "TUTOR" to c(0x6A43B8), "INSTITUTION" to c(0x1F6E55),
        "MODERATOR" to c(0x2E5C8C), "ADMIN" to c(0x4A4A5A), "BOT" to c(0x13738F),
    )

    /** White type always; the accent is a light tint of the role, the deep colour the scene's darkest. */
    fun inkFor(role: String): Triple<Int, Int, Int> {
        val t = tints[role] ?: tints.getValue("MEMBER")
        return Triple(c(0xFFFFFF), Px.mix(t, c(0xFFFFFF), 0.7f), Px.mix(t, c(0x000000), 0.75f))
    }

    fun variantFor(hash: Int): Int = ((hash ushr 3) and 0x7FFFFFFF) % VARIANTS

    fun render(role: String, variant: Int, seedIn: Int = 0): PixelCanvas {
        val r = if (role in ROLES) role else "MEMBER"
        val time = Time.entries[Math.floorMod(variant, VARIANTS)]
        val p = palette(time, tints.getValue(r))
        val cv = PixelCanvas(WIDTH, HEIGHT)
        val seed = r.hashCode() + variant * 7919 + seedIn
        cv.skyGradient(p.sky, 0, HEIGHT)
        sky(cv, time, p, seed)
        when (r) {
            "VERIFIED" -> lake(cv, p, seed)
            "TUTOR" -> milkyWay(cv, p, seed)
            "INSTITUTION" -> durbar(cv, p, time, seed)
            "MODERATOR" -> swayambhu(cv, p, time, seed)
            "ADMIN" -> everest(cv, p, seed)
            "BOT" -> nebyClouds(cv, p, time, seed)
            else -> range(cv, p, seed)
        }
        return cv
    }

    // ---- sky -------------------------------------------------------------------------------------

    private fun sky(cv: PixelCanvas, t: Time, p: Palette, seed: Int) = with(cv) {
        when (t) {
            Time.Night -> {
                stars(seed, 90, 44, c(0x5A6A9A), c(0xF2F5FF))
                crescent(30f, 12f, 5f, c(0xFFF4D6)) { x, y -> get(x + 14, y) }
            }
            Time.Dawn -> {
                stars(seed, 18, 14, c(0x6A6EA8), c(0xD8DCF5))
                glowDisc(150f, 40f, 5f, c(0xFFE9C2), p.glow, 16f)
            }
            Time.Dusk -> {
                stars(seed, 24, 16, c(0x6A5E9A), c(0xE8DCF5))
                glowDisc(40f, 42f, 6f, c(0xFFC48A), p.glow, 18f)
            }
        }
    }

    // ---- scenes ----------------------------------------------------------------------------------

    private fun bigRange(cv: PixelCanvas, p: Palette, seed: Int, base: Float, amp: Float, peakAt: Int, peakH: Float) {
        val line = ridge(cv.width, base, amp, seed, 0.6f)
        for (x in 0 until cv.width) line[x] -= (peakH - abs(x - peakAt) * 0.42f).coerceAtLeast(0f)
        cv.mountains(line, p.rock, p.rockShade, p.snow, p.snowShade, 5f, seed)
    }

    /** MEMBER: the range end to end, prayer flags strung across the foreground ridge. */
    private fun range(cv: PixelCanvas, p: Palette, seed: Int) = with(cv) {
        val far = ridge(width, 30f, 6f, seed + 1, 0.5f)
        mountains(far, p.hillFar, Px.mix(p.hillFar, c(0x000000), 0.15f), p.snowShade, Px.mix(p.snowShade, p.hillFar, 0.4f), 3f, seed + 1)
        bigRange(cv, p, seed + 2, 40f, 7f, 120, 16f)
        val hill = FloatArray(width) { x -> 54f + sin(x * 0.03f + seed) * 3f - (if (x < 60) (60 - x) * 0.12f else 0f) }
        fillBelow(hill, p.hill)
        flags(cv, 6, hill[6].roundToInt() - 14, 150, hill[150].roundToInt() - 10, seed)
        rect(5, hill[5].roundToInt() - 15, 1, 15, c(0x5A4A3A)); rect(150, hill[150].roundToInt() - 11, 1, 11, c(0x5A4A3A))
    }

    private fun flags(cv: PixelCanvas, x0: Int, y0: Int, x1: Int, y1: Int, seed: Int) = with(cv) {
        val cols = intArrayOf(c(0x2F64D6), c(0xF5F5F5), c(0xE53935), c(0x2E9E4F), c(0xFDD835))
        val n = (x1 - x0) / 4
        for (k in 0..n) {
            val t = k.toFloat() / n
            val x = (x0 + (x1 - x0) * t).roundToInt()
            val y = (y0 + (y1 - y0) * t + sin(t * Math.PI.toFloat()) * 8f).roundToInt()
            set(x, y, c(0x8A7E70)); set(x + 1, y, c(0x8A7E70)); set(x + 2, y, c(0x8A7E70))
            if (k % 1 == 0) rect(x, y + 1, 3, 3, Px.mix(cols[k % cols.size], c(0x101830), 0.25f))
        }
    }

    /** VERIFIED: Phewa: Machhapuchhre mirrored in still water, two doonga boats. */
    private fun lake(cv: PixelCanvas, p: Palette, seed: Int) = with(cv) {
        val water = 44
        val sky = PixelCanvas(width, water)
        for (y in 0 until water) for (x in 0 until width) sky.set(x, y, get(x, y))
        val line = ridge(width, 30f, 5f, seed, 0.5f)
        for (x in 0 until width) line[x] -= (16f - abs(x - 96) * 0.5f).coerceAtLeast(0f) + (if (abs(x - 100) < 3) 3f - abs(x - 100) else 0f)
        sky.mountains(line, p.rock, p.rockShade, p.snow, p.snowShade, 5f, seed)
        sky.fillBelow(FloatArray(width) { x -> 40f + sin(x * 0.07f + seed) * 2f }, p.hill, bottom = water)
        for (y in 0 until water) for (x in 0 until width) set(x, y, sky.get(x, y))
        // the reflection, darker, broken by ripples
        for (y in water until height) {
            val sy = water - 1 - (y - water) * 2
            for (x in 0 until width) {
                val ripple = if ((y + x / 9) % 5 == 0) 1 else 0
                val src = sky.get((x + ripple).coerceIn(0, width - 1), sy.coerceIn(0, water - 1))
                set(x, y, if (Bayer.threshold(x, y) < 0.18f) Px.mix(src, c(0xFFFFFF), 0.15f) else Px.mix(src, c(0x061026), 0.35f))
            }
        }
        hline(0, width - 1, water, Px.mix(p.glow, p.sky[3], 0.5f))
        for ((bx, by) in listOf(54 to 52, 70 to 57)) prop(c(0x0A0F1E)) {
            polygon(floatArrayOf(bx - 8f, by.toFloat(), bx + 8f, by.toFloat(), bx + 6f, by + 2f, bx - 6f, by + 2f), c(0x8A3B2E))
            hline(bx - 6, bx + 6, by, c(0xC0563E))
        }
        set(56, 49, c(0xE0D8C8)); rect(56, 50, 1, 2, c(0x3A3040))
    }

    /** TUTOR: the Milky Way arching over dark hills, a shooting star. */
    private fun milkyWay(cv: PixelCanvas, p: Palette, seed: Int) = with(cv) {
        val d = Dice(seed)
        for (y in 0 until 50) for (x in 0 until width) {
            val band = abs((y - 8) - (x - 40) * 0.28f)
            if (band < 9f) {
                val a = (1f - band / 9f)
                if (Bayer.threshold(x * 2 + y, y) < a * 0.35f) set(x, y, Px.mix(get(x, y), c(0xC9B6F5), 0.35f))
                if (d.next() < a * 0.08f) set(x, y, c(0xF4EEFF))
            }
        }
        line(150, 8, 168, 3, c(0xFFFFFF)); line(144, 10, 150, 8, c(0x9C8CD0))
        fillBelow(ridge(width, 48f, 5f, seed + 3, 0.6f), p.hillFar)
        fillBelow(ridge(width, 56f, 4f, seed + 4, 0.8f), p.hill)
    }

    /** INSTITUTION: Kathmandu Durbar Square: tiered temple roofs and old houses, windows lit. */
    private fun durbar(cv: PixelCanvas, p: Palette, t: Time, seed: Int) = with(cv) {
        bigRange(cv, p, seed, 36f, 5f, 40, 8f)
        val sil = Px.mix(p.hill, c(0x000000), 0.2f)
        val lit = c(0xFFC66B)
        fillBelow(FloatArray(width) { 56f }, sil)
        val d = Dice(seed)
        // houses along the square
        var x = 0
        while (x < width) {
            val w = 8 + d.int(8); val h = 8 + d.int(8)
            rect(x, 56 - h, w, h, sil)
            polygon(floatArrayOf(x - 1f, 56f - h, x + w / 2f, 52f - h, x + w + 1f, 56f - h), sil)
            for (wy in 0 until h / 4) for (wx in 0 until w / 4) if (d.next() < (if (t == Time.Night) 0.45f else 0.25f)) set(x + 2 + wx * 4, 58 - h + wy * 4, lit)
            x += w + d.int(3)
        }
        // three temples of different heights
        for ((tx, tiers) in listOf(40 to 3, 98 to 5, 150 to 2)) {
            var y = 56; var hw = 11 + tiers
            rect(tx - hw, y - 4, hw * 2, 4, sil)
            y -= 4
            for (k in 0 until tiers) {
                rect(tx - hw + 4, y - 4, (hw - 4) * 2, 4, sil)
                polygon(floatArrayOf(tx - hw - 1f, y - 4f, tx - hw + 4f, y - 8f, tx + hw - 4f, y - 8f, tx + hw + 1f, y - 4f), sil)
                set(tx, y - 2, lit)
                y -= 8; hw -= 2
            }
            rect(tx, y - 4, 1, 4, c(0xE0B44A)); set(tx, y - 5, c(0xFFE08A))
        }
    }

    /** MODERATOR: Swayambhu on its hill above the valley, the city's lights below. */
    private fun swayambhu(cv: PixelCanvas, p: Palette, t: Time, seed: Int) = with(cv) {
        bigRange(cv, p, seed, 38f, 5f, 150, 10f)
        val hill = FloatArray(width) { x -> val dx = (x - 70) / 46f; 30f + dx * dx * 26f }
        fillBelow(hill, p.hill)
        for (x in 0 until width) for (y in hill[x].roundToInt() until height) if (Bayer.threshold(x * 3, y * 2) < 0.15f) set(x, y, Px.mix(p.hill, c(0x2E5A3A), 0.4f))
        prop(c(0x0A0F1E)) {
            ellipse(70.5f, 30f, 9f, 5f, c(0xF4F1EA))
            rect(67, 21, 8, 5, c(0xE0B44A))
            polygon(floatArrayOf(67.5f, 21f, 71f, 11f, 74.5f, 21f), c(0xE0B44A))
        }
        hline(68, 69, 23, c(0x1E2A4A)); hline(72, 73, 23, c(0x1E2A4A)); set(71, 24, c(0x2F64D6))
        flags(cv, 71, 12, 104, 36, seed); flags(cv, 38, 36, 70, 12, seed + 1)
        val d = Dice(seed)
        repeat(if (t == Time.Night) 70 else 40) { val x = d.int(width); val y = 56 + d.int(8); if (abs(x - 70) > 28) set(x, y, if (d.next() < 0.5f) c(0xFFC66B) else c(0xFFE9B0)) }
    }

    /** ADMIN: Everest alone against the stars, a plume of snow off the summit. */
    private fun everest(cv: PixelCanvas, p: Palette, seed: Int) = with(cv) {
        val line = FloatArray(width) { x -> val dx = abs(x - 120f); (10f + dx * 0.75f + sin(x * 0.4f) * 1.2f).coerceAtMost(46f + sin(x * 0.05f) * 3f) }
        mountains(line, p.rock, p.rockShade, p.snow, p.snowShade, 9f, seed)
        for (k in 0 until 26) { val x = 121 + k; val y = 10 + (k * 0.3f).roundToInt(); if (Bayer.threshold(x, y) < 1f - k / 26f) { set(x, y, p.snow); if (k < 14) set(x, y - 1, Px.mix(p.snow, p.sky[1], 0.5f)) } }
        bigRange(cv, p, seed + 5, 50f, 5f, 40, 6f)
        fillBelow(ridge(width, 58f, 2f, seed + 6), p.hill)
    }

    /** BOT: Neby on a sea of clouds under the stars. */
    private fun nebyClouds(cv: PixelCanvas, p: Palette, t: Time, seed: Int) = with(cv) {
        val body = Px.mix(p.sky[3], c(0xFFFFFF), 0.35f); val light = Px.mix(body, c(0xFFFFFF), 0.4f); val shade = Px.mix(body, p.sky[1], 0.45f)
        cloud(60f, 30f, 26f, Px.mix(body, p.sky[2], 0.4f), body, shade, seed + 1)
        var x = -6f; var i = 0
        val d = Dice(seed)
        while (x < width + 12) { val w = d.range(20f, 32f); cloud(x + w / 2, 56f + d.range(-2f, 2f), w, body, light, shade, seed + 9 + i); x += w * 0.7f; i++ }
        for (xx in 0 until width) for (y in 55 until height) set(xx, y, if (Bayer.threshold(xx, y) < 0.3f) shade else body)
        // Neby sits on the clouds, right of centre, looking at the stars
        val n = PixelCanvas(PixelNeby.SIZE, PixelNeby.SIZE)
        with(PixelNeby) { n.drawNeby(PixelNeby.Pose(eyes = if (t == Time.Night) PixelNeby.Eyes.Up else PixelNeby.Eyes.Happy, mouth = PixelNeby.Mouth.Smile, look = NebyLook.Classic)) }
        for (yy in 0 until 46) for (xx in 0 until PixelNeby.SIZE) { val v = n.get(xx, yy); if ((v ushr 24) == 0xFF) set(140 + xx - 24, 14 + yy, v) }
    }
}
