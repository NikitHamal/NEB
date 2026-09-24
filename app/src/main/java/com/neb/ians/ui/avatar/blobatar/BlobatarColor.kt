package com.neb.ians.ui.avatar.blobatar

import kotlin.math.*

private fun cbrt(v: Double): Double = if (v >= 0) v.pow(1.0 / 3.0) else -((-v).pow(1.0 / 3.0))

private fun toLinear(l: Double, c: Double, h: Double): DoubleArray {
    val r = h * PI / 180.0
    val a = c * cos(r)
    val b = c * sin(r)
    val lp = l + 0.3963377774 * a + 0.2158037573 * b
    val mp = l - 0.1055613458 * a - 0.0638541728 * b
    val sp = l - 0.0894841775 * a - 1.291485548 * b
    val L = lp * lp * lp
    val M = mp * mp * mp
    val S = sp * sp * sp
    return doubleArrayOf(
        4.0767416621 * L - 3.3077115913 * M + 0.2309699292 * S,
        -1.2684380046 * L + 2.6097574011 * M - 0.3413193965 * S,
        -0.0041960863 * L - 0.7034186147 * M + 1.707614701 * S
    )
}

private fun inGamut(rgb: DoubleArray): Boolean = rgb.all { it >= -1e-4 && it <= 1 + 1e-4 }

private fun resolveOklch(l: Double, c: Double, h: Double): DoubleArray {
    var rgb = toLinear(l, c, h)
    if (!inGamut(rgb)) {
        var lo = 0.0
        var hi = c
        repeat(12) {
            val mid = (lo + hi) / 2
            rgb = toLinear(l, mid, h)
            if (inGamut(rgb)) lo = mid else hi = mid
        }
        rgb = toLinear(l, lo, h)
    }
    return DoubleArray(3) { i -> rgb[i].coerceIn(0.0, 1.0) }
}

private fun luminance(l: Double, c: Double, h: Double): Double {
    val rgb = resolveOklch(l, c, h)
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
}

fun contrast(a: Triple<Double, Double, Double>, b: Triple<Double, Double, Double>): Double {
    val x = luminance(a.first, a.second, a.third)
    val y = luminance(b.first, b.second, b.third)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)
}

fun ensureContrast(
    fg: Triple<Double, Double, Double>,
    bg: Triple<Double, Double, Double>,
    minimum: Double
): Triple<Double, Double, Double> {
    if (contrast(fg, bg) >= minimum) return fg
    val lean = if (fg.first >= bg.first) 1 else -1
    for (direction in listOf(lean, -lean)) {
        val probe = doubleArrayOf(fg.first, fg.second, fg.third)
        repeat(60) {
            probe[0] = (probe[0] + direction * 0.02).coerceIn(0.0, 1.0)
            if (contrast(Triple(probe[0], probe[1], probe[2]), bg) >= minimum) {
                return Triple(probe[0], probe[1], probe[2])
            }
            if (probe[0] == 0.0 || probe[0] == 1.0) return@repeat
        }
        if (probe[0] == 0.0 || probe[0] == 1.0) continue
    }
    val black = Triple(0.0, 0.0, fg.third)
    val white = Triple(1.0, 0.0, fg.third)
    return if (contrast(black, bg) >= contrast(white, bg)) black else white
}

fun oklchToHex(l: Double, c: Double, h: Double): String {
    val rgb = resolveOklch(l, c, h)
    val sb = StringBuilder("#")
    for (v in rgb) {
        val s = if (v <= 0.0031308) 12.92 * v else 1.055 * v.pow(1.0 / 2.4) - 0.055
        sb.append(String.format("%02x", (s * 255 + 0.5).toInt().coerceIn(0, 255)))
    }
    return sb.toString()
}

fun hexToOklch(hex: String): Triple<Double, Double, Double> {
    val n = hex.trim().removePrefix("#").toInt(16)
    val chans = DoubleArray(3)
    for (i in 0..2) {
        val shift = (2 - i) * 8
        val v = ((n shr shift) and 255) / 255.0
        chans[i] = if (v <= 0.04045) v / 12.92 else ((v + 0.055) / 1.055).pow(2.4)
    }
    val r = chans[0]; val g = chans[1]; val b = chans[2]
    val l = cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    val m = cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    val s = cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    val A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s
    val B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s
    return Triple(
        0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
        hypot(A, B),
        atan2(B, A) * 180.0 / PI
    )
}

fun mixOklch(
    a: Triple<Double, Double, Double>,
    b: Triple<Double, Double, Double>,
    t: Double
): Triple<Double, Double, Double> {
    val ax = a.second * cos(a.third * PI / 180)
    val ay = a.second * sin(a.third * PI / 180)
    val bx = b.second * cos(b.third * PI / 180)
    val by = b.second * sin(b.third * PI / 180)
    val x = ax + (bx - ax) * t
    val y = ay + (by - ay) * t
    return Triple(
        a.first + (b.first - a.first) * t,
        hypot(x, y),
        atan2(y, x) * 180.0 / PI
    )
}

fun mixHex(a: String, b: String, t: Double): String {
    val ca = hexToOklch(a)
    val cb = hexToOklch(b)
    val m = mixOklch(ca, cb, t)
    return oklchToHex(m.first, m.second, m.third)
}

private val TONES = listOf(
    0.14 to (0.82 to 0.0),
    0.30 to (0.73 to 0.0),
    0.50 to (0.64 to 0.0),
    0.70 to (0.55 to 0.0),
    0.87 to (0.46 to 0.0),
    1.0 to (0.36 to 0.0)
)

private fun toneAt(v: Double): Pair<Double, Double> {
    for ((edge, tone) in TONES) if (v < edge) return tone
    return TONES[0].second
}

const val SURFACE_FLOOR = 1.5
val DARK_SURFACE = Triple(0.145, 0.0, 0.0)

fun ramp(hue: Double, enforce: Boolean = true, tone: Double = 0.0): Map<String, Triple<Double, Double, Double>> {
    val t = toneAt(tone)
    val spread = hue / 360.0
    val headL = (t.first + (spread - 0.5) * 0.13).coerceIn(0.16, 0.88)
    val bgL = (0.955 - spread * 0.055).coerceIn(0.9, 0.97)
    var head = ensureContrast(Triple(headL, t.second, hue), DARK_SURFACE, SURFACE_FLOOR)
    val r = mutableMapOf(
        "bg" to Triple(bgL, 0.0, hue),
        "head" to head,
        "eye" to (if (head.first >= 0.5) Triple(0.17, 0.0, hue) else Triple(0.97, 0.0, hue))
    )
    if (enforce) {
        for ((fg, bg, minimum) in listOf(Triple("head", "bg", 1.25), Triple("eye", "head", 4.5))) {
            r[fg] = ensureContrast(r[fg]!!, r[bg]!!, minimum)
        }
    }
    return r
}

fun palette(hue: Double, enforce: Boolean = true, tone: Double = 0.0): Map<String, String> =
    ramp(hue, enforce, tone).mapValues { (_, v) -> oklchToHex(v.first, v.second, v.third) }

private const val TINT_FLOOR = 4.55
data class TintDef(val h: Double, val l: Double, val pull: Double, val c: Double)
private val HOT = TintDef(27.0, 0.58, 0.6, 0.0)
private val ROSE = TintDef(358.0, 0.72, 0.55, 0.0)
private val BLUSH = TintDef(12.0, 0.84, 0.4, 0.0)
private val BILE = TintDef(142.0, 0.66, 0.6, 0.0)
val TINT_HOT = HOT; val TINT_ROSE = ROSE; val TINT_BLUSH = BLUSH; val TINT_BILE = BILE

fun tinted(head: String, eye: String, t: TintDef): Pair<String, String> {
    val base = hexToOklch(head)
    val baseEye = hexToOklch(eye)
    var hotHead = Triple(
        base.first + (t.l - base.first) * t.pull,
        min(base.second, t.c),
        t.h
    )
    hotHead = ensureContrast(hotHead, DARK_SURFACE, SURFACE_FLOOR)
    var hotEye = ensureContrast(baseEye, hotHead, TINT_FLOOR)
    val direction = if (hotEye.first >= hotHead.first) 1 else -1
    val headHex = oklchToHex(hotHead.first, hotHead.second, hotHead.third)
    repeat(40) {
        val eyeHex = oklchToHex(hotEye.first, hotEye.second, hotEye.third)
        var worst = Double.MAX_VALUE
        for (i in 0..10) {
            val tt = i / 10.0
            worst = min(
                worst,
                contrast(hexToOklch(mixHex(eye, eyeHex, tt)), hexToOklch(mixHex(head, headHex, tt)))
            )
        }
        if (worst >= TINT_FLOOR) return headHex to eyeHex
        val newL = (hotEye.first + direction * 0.02).coerceIn(0.0, 1.0)
        if (newL == hotEye.first) return headHex to eyeHex
        hotEye = Triple(newL, hotEye.second, hotEye.third)
    }
    return headHex to oklchToHex(hotEye.first, hotEye.second, hotEye.third)
}

fun tintWith(pal: Map<String, String>, tint: TintDef): Map<String, String> {
    val (hHead, hEye) = tinted(pal["head"]!!, pal["eye"]!!, tint)
    return pal.toMutableMap().also { it["head"] = hHead; it["eye"] = hEye }
}
