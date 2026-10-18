package com.neb.ians.ui.pixel

import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.random.Random

/**
 * The NEBians pixel sprite kit. Every sprite is built once, lazily, and shared. Hand-drawn
 * sprites are ASCII (see [PixelSprite.parse]); the book, clouds and hourglass are drawn by
 * code because their frames are geometry. Show any of them with PixelSpriteView.
 */
object PixelSprites {
    /** The shared palette for hand-drawn sprites. Warm, slightly dusty, dawn-lit. */
    val palette: Map<Char, Int> = mapOf(
        'k' to Px.rgb(0x3D2C3E), 'K' to Px.rgb(0x6B5470), 'w' to Px.rgb(0xFFFFFF),
        'p' to Px.rgb(0xFFF8EA), 'P' to Px.rgb(0xEEDCBD), 'q' to Px.rgb(0xD8BC92),
        'y' to Px.rgb(0xFFC94A), 'Y' to Px.rgb(0xFFEFA6), 'o' to Px.rgb(0xF2A541),
        'r' to Px.rgb(0xD9404A), 'R' to Px.rgb(0xFF7C86), 'b' to Px.rgb(0x4C7BD9),
        'B' to Px.rgb(0xA9C8FF), 'g' to Px.rgb(0xA7ADBA), 'G' to Px.rgb(0x6E7584),
        'n' to Px.rgb(0x8A5A3B), 'N' to Px.rgb(0x5A3A26), 'm' to Px.rgb(0x6F5C7E)
    )

    /** A small bird, three wing positions. Loop it and move it. */
    val bird: PixelSprite by lazy {
        PixelSprite.parse(
            palette, 110,
            """
            m.....m
            .m...m.
            ..m.m..
            ...m...
            """,
            """
            .......
            mmm.mmm
            ...m...
            .......
            """,
            """
            .......
            ...m...
            .mm.mm.
            m.....m
            """
        )
    }

    /** A twinkle: dot, cross, star, cross, dot, rest. */
    val sparkle: PixelSprite by lazy {
        PixelSprite.parse(
            palette, 110,
            """
            .....
            .....
            ..Y..
            """,
            """
            .....
            ..Y..
            .YwY.
            ..Y..
            """,
            """
            ..Y..
            ..w..
            YwwwY
            ..w..
            ..Y..
            """,
            """
            .....
            ..Y..
            .YwY.
            ..Y..
            """,
            """
            .....
            .....
            ..Y..
            """,
            """
            .....
            """
        )
    }

    /** A paper plane, bobbing a pixel. For "sent", "shared", "posted". */
    val paperPlane: PixelSprite by lazy {
        PixelSprite.parse(
            palette, 260,
            """
            ............kkk
            .........kkkwwk
            ......kkkwwwwk.
            ...kkkwwwwwwk..
            .kkwwwwwwwwk...
            kkBBBBwwwwk....
            ...kkBBBwk.....
            .....kkBk......
            .......k.......
            """,
            """
            ...............
            ............kkk
            .........kkkwwk
            ......kkkwwwwk.
            ...kkkwwwwwwk..
            .kkwwwwwwwwk...
            kkBBBBwwwwk....
            ...kkBBBwk.....
            .....kkBk......
            .......k.......
            """
        )
    }

    /** A heart that pops once: small, full, burst, settle. For likes. */
    val heartPop: PixelSprite by lazy {
        PixelSprite.parse(
            palette, 90,
            """
            ...........
            ...........
            ...kk.kk...
            ..kRRkRrk..
            ..kRRRRrk..
            ...kRRrk...
            ....krk....
            .....k.....
            """,
            """
            ...........
            .kkk...kkk.
            kRRRk.kRRrk
            kRwRRkRRRrk
            kRRRRRRRRrk
            .kRRRRRRrk.
            ..kRRRRrk..
            ...kRRrk...
            ....krk....
            .....k.....
            """,
            """
            Y.........Y
            .kkk...kkk.
            kRRRk.kRRrk
            kRwRRkRRRrk
            kRRRRRRRRrk
            .kRRRRRRrk.
            ..kRRRRrk..
            ...kRRrk...
            Y...krk...Y
            .....k.....
            """,
            """
            ...........
            .kkk...kkk.
            kRRRk.kRRrk
            kRwRRkRRRrk
            kRRRRRRRRrk
            .kRRRRRRrk.
            ..kRRRRrk..
            ...kRRrk...
            ....krk....
            .....k.....
            """,
            loop = false
        )
    }

    /** A star with a glint that runs across it. For points, badges, the leaderboard. */
    val star: PixelSprite by lazy {
        PixelSprite.parse(
            palette, 180,
            """
            ....k....
            ...kYk...
            kkkkYykkk
            kYYYYyyyk
            .kYYyyyk.
            ..kYyyk..
            .kYyykyk.
            kyyk.kyyk
            kkk...kkk
            """,
            """
            ....k....
            ...kwk...
            kkkkwykkk
            kYYwYyyyk
            .kwYyyyk.
            ..kYyyk..
            .kYyykyk.
            kyyk.kyyk
            kkk...kkk
            """,
            """
            ....k....
            ...kYk...
            kkkkYykkk
            kYYYYwyyk
            .kYYywyk.
            ..kYwyk..
            .kYwykyk.
            kyyk.kyyk
            kkk...kkk
            """
        )
    }

    /** Sand running through an hourglass. A loader with some patience in it. */
    val hourglass: PixelSprite by lazy {
        val wood = Px.rgb(0x5A3A26); val woodHi = Px.rgb(0x8A5A3B)
        val glass = Px.rgb(0x6E7584); val tint = Px.rgb(0xE6F0FF)
        val sand = Px.rgb(0xF2C46D); val sandDk = Px.rgb(0xD9A441)
        PixelSprite.build(11, 15, 12, 150) { f ->
            val p = f / 11f
            rect(0, 0, 11, 2, wood); hline(1, 9, 0, woodHi)
            rect(0, 13, 11, 2, wood); hline(1, 9, 14, woodHi)
            // bulbs: half-width per row, narrowing to the neck at row 7
            val half = intArrayOf(0, 0, 4, 4, 3, 2, 1, 0, 1, 2, 3, 4, 4)
            for (y in 2..12) {
                val h = half[y]
                hline(5 - h, 5 + h, y, tint)
                set(5 - h - 1, y, glass); set(5 + h + 1, y, glass)
            }
            // top sand sinks, bottom sand piles up
            val topRows = ((1f - p) * 4f).roundToInt()
            for (r in 0 until topRows) { val y = 6 - r; hline(5 - half[y], 5 + half[y], y, sand) }
            val bottomRows = (p * 4f).roundToInt()
            for (r in 0 until bottomRows) {
                val y = 12 - r
                hline(5 - half[y], 5 + half[y], y, if (r == bottomRows - 1) sand else sandDk)
            }
            if (f in 1..10) for (y in 7..(12 - bottomRows)) if ((y + f) % 2 == 0) set(5, y, sand)
        }
    }

    /**
     * The open book, its pages fanned up like the photo on the old auth screen. Three idle
     * frames (the top pages lift and settle), then a page turning from right to left.
     * Spine at x = 48; the cover rests at y = 44.
     */
    val book: PixelSprite by lazy {
        PixelSprite.build(BOOK_W, BOOK_H, BOOK_IDLE + BOOK_FLIP, 80, loop = false) { f -> drawBook(this, f) }
    }
    const val BOOK_W = 96
    const val BOOK_H = 52
    const val BOOK_IDLE = 3
    const val BOOK_FLIP = 10

    private val bookPaper = Px.rgb(0xFFF9EE)
    private val bookPaper2 = Px.rgb(0xF7EAD2)
    private val bookShade = Px.rgb(0xEBD5B0)
    private val bookEdge = Px.rgb(0xC9A273)
    private val bookCover = Px.rgb(0x4A3125)
    private val bookCoverHi = Px.rgb(0x7B5343)
    private val bookGold = Px.rgb(0xFFDE8A)
    private val bookGlow = Px.rgb(0xFFF1C9)

    /** Points along a page curve from the spine to its tip: a quadratic arch. */
    private fun pageCurve(side: Int, layer: Int, lift: Float): FloatArray {
        val sx = 48f; val sy = 42f - layer * 0.7f
        val tx = 48f + side * (45f - layer * 1.6f)
        val ty = 39f - layer * 3.1f - lift
        val cx = 48f + side * (11f + layer * 0.8f)
        val cy = 25f - layer * 3.4f - lift * 0.6f
        val out = FloatArray(26)
        for (i in 0..12) {
            val u = i / 12f
            out[i * 2] = quad(sx, cx, tx, u); out[i * 2 + 1] = quad(sy, cy, ty, u)
        }
        return out
    }

    private fun drawBook(c: PixelCanvas, f: Int) = with(c) {
        // cover: a shallow V under the pages
        polygon(floatArrayOf(1f, 41f, 48f, 45f, 95f, 41f, 95f, 44f, 48f, 48.5f, 1f, 44f), bookCover)
        line(2, 42, 47, 46, bookCoverHi); line(49, 46, 94, 42, bookCoverHi)
        for (side in intArrayOf(-1, 1)) {
            var below = floatArrayOf(48f, 44f, 48f + side * 46f, 42f)
            for (layer in 0..5) {
                val flutter = if (f < BOOK_IDLE && layer >= 4) ((f + layer + (side + 1) / 2) % 3).toFloat() * 0.7f else 0f
                val curve = pageCurve(side, layer, flutter)
                // fill between this page and the one below it
                val poly = ArrayList<Float>()
                for (v in curve) poly += v
                for (i in below.size / 2 - 1 downTo 0) { poly += below[i * 2]; poly += below[i * 2 + 1] }
                polygon(poly.toFloatArray(), if (layer % 2 == 0) bookPaper else bookPaper2)
                // the page's top edge
                for (i in 0 until 12) {
                    line(curve[i * 2].roundToInt(), curve[i * 2 + 1].roundToInt(),
                        curve[i * 2 + 2].roundToInt(), curve[i * 2 + 3].roundToInt(),
                        if (layer == 5) bookShade else bookEdge)
                }
                below = curve
            }
            // light pooling on the top pages near the spine
            for (i in 1..4) set(48 + side * i, 22 - i / 2, bookGlow)
        }
        line(48, 22, 48, 44, bookShade)
        set(48, 21, bookGold); set(47, 22, bookGold); set(49, 22, bookGold)
        if (f >= BOOK_IDLE) {
            val t = (f - BOOK_IDLE + 1) / (BOOK_FLIP + 1f)
            val theta = PI * t
            val tipX = 48f + 44f * cos(theta).toFloat()
            val tipY = 21f - 19f * sin(theta).toFloat()
            val ctrlX = 48f + 12f * cos(theta).toFloat()
            val ctrlY = 6f - 4f * sin(theta).toFloat()
            val top = FloatArray(26); val bottom = FloatArray(26)
            for (i in 0..12) {
                val u = i / 12f
                top[i * 2] = quad(48f, ctrlX, tipX, u); top[i * 2 + 1] = quad(21f, ctrlY, tipY, u)
                // the sheet has depth: seen from slightly above, it shows as a band
                bottom[i * 2] = quad(48f, ctrlX, tipX, u); bottom[i * 2 + 1] = quad(27f, ctrlY + 7f, tipY + 7f, u)
            }
            val poly = ArrayList<Float>()
            for (v in top) poly += v
            for (i in 12 downTo 0) { poly += bottom[i * 2]; poly += bottom[i * 2 + 1] }
            polygon(poly.toFloatArray(), if (t > 0.5f) bookPaper2 else bookPaper)
            for (i in 0 until 12) {
                line(top[i * 2].roundToInt(), top[i * 2 + 1].roundToInt(), top[i * 2 + 2].roundToInt(), top[i * 2 + 3].roundToInt(), bookEdge)
                line(bottom[i * 2].roundToInt(), bottom[i * 2 + 1].roundToInt(), bottom[i * 2 + 2].roundToInt(), bottom[i * 2 + 3].roundToInt(), bookShade)
            }
            line(tipX.roundToInt(), tipY.roundToInt(), tipX.roundToInt(), (tipY + 7f).roundToInt(), bookEdge)
        }
    }

    private fun quad(a: Float, b: Float, c: Float, t: Float) = (1 - t) * (1 - t) * a + 2 * (1 - t) * t * b + t * t * c

    /**
     * A cloud: a union of discs on a flat base, lit from above. [light], [mid] and [shade] are
     * the three tones top to bottom; transitions between them are dithered.
     */
    fun cloud(seed: Int, width: Int, height: Int, light: Int, mid: Int, shade: Int): PixelSprite {
        val rnd = Random(seed)
        val base = height - 1.5f
        val n = 5 + rnd.nextInt(3)
        // puffs: bigger in the middle, centred low so the base stays flat and the top is bumpy
        val discs = List(n) { i ->
            val t = (i + 0.5f) / n
            val alt = if (i % 2 == 0) 0.07f else -0.06f
            val r = height * (0.2f + 0.3f * sin(t * PI).toFloat() + alt + rnd.nextFloat() * 0.07f).coerceAtMost(0.6f)
            Triple(width * (0.1f + 0.8f * t) + rnd.nextFloat() * 3f - 1.5f, base - r * 0.6f, r)
        }
        val rim = Px.mix(light, Px.rgb(0xFFFFFF), 0.6f)
        return PixelSprite.build(width, height, 1, 1000) {
            for (y in 0 until height) for (x in 0 until width) {
                if (y > base) continue
                var best = -1f; var lit = 0f
                for ((cx, cy, r) in discs) {
                    val dx = x + 0.5f - cx; val dy = y + 0.5f - cy
                    val d2 = dx * dx + dy * dy
                    if (d2 <= r * r) {
                        // light from the upper left: how far toward that side of this puff we are
                        val k = 1f - sqrt(d2) / r
                        val face = ((-dx * 0.45f - dy) / r).coerceIn(-1f, 1f)
                        if (k > best) { best = k; lit = face }
                    }
                }
                if (best < 0f) continue
                val height01 = (y / base)
                val tone = lit * 0.9f - (height01 - 0.55f) * 1.3f
                val c = when {
                    best < 0.08f && lit > 0.35f -> rim
                    tone > 0.42f -> light
                    tone > 0.30f -> if (Bayer.threshold(x, y) < (tone - 0.30f) / 0.12f) light else mid
                    tone > -0.05f -> mid
                    tone > -0.2f -> if (Bayer.threshold(x, y) < (tone + 0.2f) / 0.15f) mid else shade
                    else -> shade
                }
                set(x, y, c)
            }
        }
    }
}
