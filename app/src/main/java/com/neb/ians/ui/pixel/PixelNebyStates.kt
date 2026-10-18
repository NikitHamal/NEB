package com.neb.ians.ui.pixel

import com.neb.ians.ui.pixel.PixelNeby.Eyes
import com.neb.ians.ui.pixel.PixelNeby.Mouth
import com.neb.ians.ui.pixel.PixelNeby.Pose
import com.neb.ians.ui.pixel.PixelNeby.drawNeby
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Everything pixel Neby can do. Each state is a short choreography of poses plus props (hearts,
 * a tear, Zs, sparkles, a book...), built once and cached. Loops unless noted. The same states are
 * exported for the web (PixelSkySceneTest -> static/web/img/neby) so both apps share one Neby.
 */
enum class NebyState(val frameMs: Int, val loop: Boolean = true) {
    Idle(115), Still(1000), Blink(110), Hop(72), Think(160), Sleep(140), Wink(110), Talk(95), Love(110),
    Surprised(80), Sad(130), Laugh(80), Dizzy(100), Wave(110), Success(80), Oops(100), Read(140),
    Listen(140), Celebrate(85), Cool(120), Kiss(110), LookAround(130);

    val sprite: PixelSprite get() = PixelNebyStates.sprite(this)

    companion object {
        /** The 3D avatar's animation names, mapped so existing callers keep their meaning. */
        fun fromName(name: String?): NebyState = when (name?.lowercase()?.replace('_', '-')) {
            null, "", "idle", "idle-front", "default" -> Idle
            "still", "static", "none" -> Still
            "happy", "joy", "delight", "cheer", "jump", "hop" -> Hop
            "thinking", "think", "focus", "listening-focus", "scan", "puzzled", "typing", "loading" -> Think
            "sleep", "sleepy" -> Sleep
            "wink" -> Wink
            "talk", "talk-a", "talk-b", "talk-c", "speaking", "responding" -> Talk
            "love", "heart" -> Love
            "gasp", "surprised", "notification", "wow" -> Surprised
            "sad", "sad-deep", "concern" -> Sad
            "laugh", "lol", "smug" -> Laugh
            "dizzy", "confused", "error" -> Dizzy
            "wave", "hello", "hi", "greet", "intro-pop" -> Wave
            "success", "done", "check" -> Success
            "oops", "panic", "sorry" -> Oops
            "read", "reading", "study" -> Read
            "listen", "listening" -> Listen
            "celebrate", "confetti", "party" -> Celebrate
            "cool", "sunglasses" -> Cool
            "kiss" -> Kiss
            "look", "look-around", "idle-glance-left", "idle-glance-right", "side-eye" -> LookAround
            else -> Idle
        }

        /** The reactions a tap plays on an interactive Neby, in turn. */
        val reactions = listOf(Hop, Wink, Love, Laugh, Surprised, Cool, Kiss, Celebrate)
    }
}

object PixelNebyStates {
    private val cache = HashMap<NebyState, PixelSprite>()
    private val gold = Px.rgb(0xFFCE5C)
    private val goldHi = Px.rgb(0xFFEBA8)
    private val steel = Px.rgb(0x8C97B3)
    private val steelHi = Px.rgb(0xB9C3DA)
    private val tear = Px.rgb(0x7FB2FF)
    private val green = Px.rgb(0x2FB36B)
    private val confetti = intArrayOf(Px.rgb(0xFF6F91), Px.rgb(0xFFCE5C), Px.rgb(0x2FB36B), Px.rgb(0x5A8BEA), Px.rgb(0x9C6BFF))
    private val paper = Px.rgb(0xFFF8EA)
    private val paperLo = Px.rgb(0xEBD5B0)
    private val bookBlue = Px.rgb(0x2F64D6)

    fun sprite(s: NebyState): PixelSprite = synchronized(cache) { cache.getOrPut(s) { build(s) } }

    private fun frames(n: Int, s: NebyState, draw: PixelCanvas.(Int) -> Unit) =
        PixelSprite.build(PixelNeby.SIZE, PixelNeby.SIZE, n, s.frameMs, s.loop, draw)

    private fun bob(f: Int, n: Int, amp: Float = 1.5f) = -(sin(2 * PI * f / n).toFloat() * 0.5f + 0.5f) * amp

    private fun build(s: NebyState): PixelSprite = when (s) {
        NebyState.Idle -> {
            val dys = floatArrayOf(0f, 0f, -0.5f, -1f, -1.5f, -1.5f, -1f, -0.5f, 0f, 0f, -0.5f, -1f, -1.5f, -1.5f, -1f, -0.5f)
            frames(dys.size, s) { f -> drawNeby(Pose(dys[f], eyes = if (f == 14) Eyes.Blink else Eyes.Open, lookX = if (f in 5..9) 1 else 0, phase = f.toFloat())) }
        }
        NebyState.Still -> frames(1, s) { drawNeby(Pose()) }
        NebyState.Blink -> frames(6, s) { f -> drawNeby(Pose(eyes = if (f == 3) Eyes.Blink else Eyes.Open, phase = f.toFloat())) }
        NebyState.Hop -> {
            val poses = listOf(
                Triple(0f, 1f, 1f), Triple(0f, 1.12f, 0.86f), Triple(-3f, 0.92f, 1.1f), Triple(-7f, 0.96f, 1.04f),
                Triple(-9f, 1f, 1f), Triple(-7.5f, 1f, 1f), Triple(-3f, 0.96f, 1.04f), Triple(0f, 1.14f, 0.85f),
                Triple(0f, 1.05f, 0.95f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f),
            )
            frames(poses.size, s) { f ->
                val (dy, sx, sy) = poses[f]
                drawNeby(Pose(dy, sx, sy, eyes = if (f in 2..8) Eyes.Happy else Eyes.Open, mouth = if (f in 2..8) Mouth.Open else Mouth.None, phase = f * 1.5f))
            }
        }
        NebyState.Think -> frames(8, s) { f ->
            drawNeby(Pose(if (f % 4 < 2) 0f else -0.5f, tilt = 0.06f, eyes = if (f == 6) Eyes.Blink else Eyes.Up, mouth = Mouth.Flat, phase = f * 1.2f))
            val n = f % 4
            for (i in 0 until 3) rect(31 + i * 5, 4 - if (i < n) 1 else 0, 3, 3, if (i < n) PixelNeby.band else PixelNeby.bandHi)
        }
        NebyState.Sleep -> frames(12, s) { f ->
            drawNeby(Pose(if (f % 6 < 3) 0f else 0.5f, sx = 1.02f, sy = 0.98f, eyes = Eyes.Closed, mouth = if (f % 6 < 3) Mouth.None else Mouth.O, phase = f * 0.5f))
            for (k in 0 until 2) {
                val t = ((f + k * 6) % 12) / 12f
                zed(this, 33 + (t * 6).toInt() + k * 2, (15 - t * 13).toInt(), if (t < 0.8f) steel else steelHi)
            }
        }
        NebyState.Wink -> frames(10, s) { f ->
            val dy = floatArrayOf(0f, -1f, -2f, -2f, -2f, -2f, -1f, 0f, 0f, 0f)[f]
            drawNeby(Pose(dy, eyes = if (f in 2..6) Eyes.Wink else Eyes.Open, mouth = if (f in 2..6) Mouth.Tongue else Mouth.None, phase = f.toFloat()))
            if (f in 3..5) sparkle(this, 39, 10, f - 3)
        }
        NebyState.Talk -> frames(8, s) { f ->
            val m = arrayOf(Mouth.Open, Mouth.Smile, Mouth.O, Mouth.Flat, Mouth.Open, Mouth.Smile, Mouth.O, Mouth.Smile)[f]
            drawNeby(Pose(if (f % 2 == 0) -0.5f else 0f, eyes = if (f == 5) Eyes.Blink else Eyes.Open, mouth = m, phase = f * 1.4f))
        }
        NebyState.Love -> frames(12, s) { f ->
            drawNeby(Pose(bob(f, 12), sx = 1f + 0.03f * sin(f * 0.5f), eyes = Eyes.Heart, mouth = Mouth.Smile, phase = f.toFloat()))
            for (k in 0 until 2) {
                val t = ((f + k * 6) % 12) / 12f
                heart(this, (8 + k * 30 + sin(t * 6f) * 2).roundToInt(), (16 - t * 14).roundToInt(), t < 0.75f)
            }
        }
        NebyState.Surprised -> frames(10, s) { f ->
            val dy = floatArrayOf(0f, -4f, -6f, -5f, -3f, -1f, 0f, 0f, 0f, 0f)[f]
            val sy = if (f == 1) 1.1f else if (f == 6) 0.92f else 1f
            drawNeby(Pose(dy, 2f - sy, sy, eyes = Eyes.Big, mouth = Mouth.O, phase = f.toFloat()))
            if (f in 1..8) exclaim(this, 38, 3 + (if (f < 3) 2 - f else 0))
        }
        NebyState.Sad -> frames(12, s) { f ->
            drawNeby(Pose(1f, 1.03f, 0.95f, eyes = Eyes.Sad, mouth = Mouth.Frown, lookY = 1, phase = f * 0.4f))
            // a tear wells under the left eye and rolls down the cheek
            val t = (f % 12) / 12f
            val ty = (31 + t * 9).roundToInt()
            if (t < 0.9f) { set(18, ty, tear); hline(17, 19, ty + 1, tear); set(18, ty + 2, tear); set(17, ty + 1, PixelNeby.white) }
        }
        NebyState.Laugh -> frames(10, s) { f ->
            val shake = if (f % 2 == 0) -1 else 1
            drawNeby(Pose(if (f % 4 < 2) -1f else 0f, 1f + 0.04f * (f % 2), 1f - 0.04f * (f % 2), tilt = 0.07f * shake, eyes = Eyes.Happy, mouth = Mouth.Open, phase = f * 2f))
            if (f % 4 < 2) { tinyText(this, "ha", 33, 4, PixelNeby.band) }
        }
        NebyState.Dizzy -> frames(12, s) { f ->
            drawNeby(Pose(0f, tilt = sin(f * PI.toFloat() / 6f) * 0.14f, eyes = Eyes.Spiral, mouth = Mouth.Flat, phase = f.toFloat()))
            for (k in 0 until 3) {
                val a = f * 2 * PI.toFloat() / 12f + k * 2.1f
                star(this, (24 + cos(a) * 14).roundToInt(), (7 + sin(a) * 3).roundToInt())
            }
        }
        NebyState.Wave -> frames(10, s) { f ->
            val tilt = sin(f * 2 * PI.toFloat() / 10f) * 0.12f
            drawNeby(Pose(bob(f, 10, 1f), tilt = tilt, eyes = Eyes.Happy, mouth = Mouth.Smile, phase = f.toFloat()))
            // a little hand, waving from the side
            val hx = 40 + (sin(f * 2 * PI.toFloat() / 5f) * 2).roundToInt()
            disc(hx + 0.5f, 22.5f, 3.6f, PixelNeby.line); disc(hx + 0.5f, 22.5f, 2.6f, Px.rgb(0xCCE2FF)); set(hx - 1, 21, PixelNeby.white)
            bubble(this, "hi", 31, 1, f >= 2)
        }
        NebyState.Success -> frames(12, s) { f ->
            val dy = floatArrayOf(0f, 1f, -4f, -7f, -6f, -3f, 0f, 1f, 0f, 0f, 0f, 0f)[f]
            drawNeby(Pose(dy, if (f == 1 || f == 7) 1.1f else 1f, if (f == 1 || f == 7) 0.9f else 1f, eyes = Eyes.Happy, mouth = Mouth.Smile, phase = f.toFloat()))
            if (f >= 3) check(this, 37, 2, ((f - 3) / 4f).coerceAtMost(1f))
        }
        NebyState.Oops -> frames(10, s) { f ->
            drawNeby(Pose(0f, tilt = if (f in 2..5) (if (f % 2 == 0) 0.05f else -0.05f) else 0f, eyes = Eyes.Big, mouth = Mouth.Flat, lookX = if (f > 5) -1 else 0, phase = f.toFloat()))
            val t = (f % 10) / 10f
            sweat(this, 36, (17 + t * 5).roundToInt())
        }
        NebyState.Read -> frames(14, s) { f ->
            drawNeby(Pose(bob(f, 14, 0.8f), eyes = if (f == 11) Eyes.Blink else Eyes.Down, mouth = Mouth.Smile, phase = f * 0.6f))
            book(this, 24, 34, (f % 14) / 14f)
        }
        NebyState.Listen -> frames(8, s) { f ->
            drawNeby(Pose(0f, tilt = -0.12f, eyes = Eyes.Open, lookX = 2, mouth = Mouth.None, phase = f.toFloat()))
            val n = f % 4
            for (k in 0..n.coerceAtMost(2)) arc(this, 40 + k * 2, 20, 2 + k * 2)
        }
        NebyState.Celebrate -> frames(14, s) { f ->
            val dy = floatArrayOf(0f, 1f, -5f, -9f, -10f, -8f, -4f, 0f, 1f, 0f, -2f, -3f, -2f, 0f)[f]
            drawNeby(Pose(dy, if (f == 1 || f == 8) 1.12f else 1f, if (f == 1 || f == 8) 0.88f else 1f, eyes = Eyes.Star, mouth = Mouth.Open, phase = f * 1.5f))
            for (k in 0 until 10) {
                val t = ((f + k * 1.4f) % 14) / 14f
                val x = (k * 47 % 44 + 2 + sin(t * 8f + k) * 2).roundToInt()
                val y = (t * 40).roundToInt()
                // confetti falls behind Neby, never across the face
                for (yy in y until y + 1 + (k % 2)) for (xx in x until x + 2) if ((get(xx, yy) ushr 24) == 0) set(xx, yy, confetti[k % confetti.size])
            }
        }
        NebyState.Cool -> frames(10, s) { f ->
            val slide = (f.coerceAtMost(4)) / 4f
            drawNeby(Pose(if (f > 5) bob(f, 4, 0.6f) else 0f, eyes = if (slide < 1f) Eyes.Open else Eyes.Shades, mouth = if (slide < 1f) Mouth.None else Mouth.Smile, phase = f.toFloat()))
            if (slide < 1f) {
                val y = (4 + slide * 15).roundToInt()
                rect(15, y, 7, 4, PixelNeby.eyes); rect(25, y, 7, 4, PixelNeby.eyes); hline(21, 25, y + 1, PixelNeby.eyes)
            }
            if (f in 6..8) sparkle(this, 36, 14, f - 6)
        }
        NebyState.Kiss -> frames(12, s) { f ->
            drawNeby(Pose(bob(f, 12, 1f), tilt = 0.06f, eyes = Eyes.Closed, mouth = Mouth.Kiss, blush = true, phase = f.toFloat()))
            val t = (f % 12) / 12f
            if (f >= 3) heart(this, (31 + t * 8).roundToInt(), (20 - t * 16).roundToInt(), true)
        }
        NebyState.LookAround -> frames(12, s) { f ->
            val look = intArrayOf(0, -1, -2, -2, -2, -1, 0, 1, 2, 2, 2, 1)[f]
            drawNeby(Pose(0f, eyes = if (f == 6) Eyes.Blink else Eyes.Open, lookX = look, phase = f.toFloat()))
        }
    }

    // ---- props ---------------------------------------------------------------------------------

    private fun zed(c: PixelCanvas, x: Int, y: Int, color: Int) = with(c) {
        hline(x, x + 3, y, color); set(x + 2, y + 1, color); set(x + 1, y + 2, color); hline(x, x + 3, y + 3, color)
    }

    private fun heart(c: PixelCanvas, x: Int, y: Int, full: Boolean) = with(c) {
        val col = if (full) PixelNeby.pink else PixelNeby.pinkHi
        set(x, y, col); set(x + 1, y, col); set(x + 3, y, col); set(x + 4, y, col)
        hline(x, x + 4, y + 1, col); hline(x + 1, x + 3, y + 2, col); set(x + 2, y + 3, col)
        set(x + 1, y, PixelNeby.pinkHi)
    }

    private fun sparkle(c: PixelCanvas, x: Int, y: Int, step: Int) = with(c) {
        set(x, y, gold)
        if (step >= 1) { set(x - 1, y, goldHi); set(x + 1, y, goldHi); set(x, y - 1, goldHi); set(x, y + 1, goldHi) }
        if (step >= 2) { set(x - 2, y, gold); set(x + 2, y, gold); set(x, y - 2, gold); set(x, y + 2, gold) }
    }

    private fun star(c: PixelCanvas, x: Int, y: Int) = with(c) {
        set(x, y - 1, gold); hline(x - 1, x + 1, y, gold); set(x, y + 1, gold); set(x, y, goldHi)
    }

    private fun exclaim(c: PixelCanvas, x: Int, y: Int) = with(c) {
        rect(x, y, 2, 5, PixelNeby.band); rect(x, y + 6, 2, 2, PixelNeby.band)
    }

    private fun check(c: PixelCanvas, x: Int, y: Int, p: Float) = with(c) {
        disc(x + 4.5f, y + 4.5f, 5f, green)
        val pts = listOf(2 to 4, 3 to 5, 4 to 6, 5 to 5, 6 to 4, 7 to 3)
        val n = (pts.size * p).roundToInt()
        for (i in 0 until n) { val (dx, dy) = pts[i]; set(x + dx, y + dy, PixelNeby.white) }
    }

    private fun sweat(c: PixelCanvas, x: Int, y: Int) = with(c) {
        set(x, y - 1, PixelNeby.line); set(x - 1, y, PixelNeby.line); set(x + 1, y, PixelNeby.line)
        hline(x - 2, x + 2, y + 1, PixelNeby.line); hline(x - 2, x + 2, y + 2, PixelNeby.line); hline(x - 1, x + 1, y + 3, PixelNeby.line)
        set(x, y, tear); hline(x - 1, x + 1, y + 1, tear); hline(x - 1, x + 1, y + 2, tear); set(x, y + 3, tear); set(x - 1, y + 1, PixelNeby.white)
    }

    private fun arc(c: PixelCanvas, x: Int, y: Int, r: Int) = with(c) {
        for (k in -r..r) set(x + (r - kotlin.math.abs(k)) / 2, y + k, steel)
    }

    private fun book(c: PixelCanvas, cx: Int, y: Int, t: Float) = with(c) {
        rect(cx - 9, y, 18, 7, bookBlue)
        rect(cx - 8, y - 1, 8, 6, paper); rect(cx + 1, y - 1, 8, 6, paper)
        hline(cx - 7, cx - 2, y + 1, paperLo); hline(cx + 2, cx + 7, y + 1, paperLo); hline(cx - 7, cx - 3, y + 3, paperLo); hline(cx + 2, cx + 6, y + 3, paperLo)
        set(cx, y - 1, paperLo)
        // a page turning over
        val px = (cx + 7 - t * 14).roundToInt()
        val lift = (sin(t * PI.toFloat()) * 4).roundToInt()
        line(cx, y - 1, px, y - 1 - lift, paperLo)
        line(cx, y, px, y - lift + 2, paper)
    }

    /** A tiny speech bubble with 2-3 letters drawn in a 3x5 pixel font. */
    private fun bubble(c: PixelCanvas, text: String, x: Int, y: Int, show: Boolean) = with(c) {
        if (!show) return@with
        val w = text.length * 4 + 3
        roundRect(x, y, w, 9, 2, PixelNeby.white)
        set(x + 2, y + 9, PixelNeby.white); set(x + 1, y + 10, PixelNeby.white)
        tinyText(this, text, x + 2, y + 2, PixelNeby.band)
    }

    private val FONT = mapOf(
        'h' to arrayOf("1..", "1..", "111", "1.1", "1.1"),
        'i' to arrayOf(".1.", "...", ".1.", ".1.", ".1."),
        'a' to arrayOf("...", "11.", "..1", "111", "111"),
    )

    private fun tinyText(c: PixelCanvas, text: String, x: Int, y: Int, color: Int) = with(c) {
        text.forEachIndexed { i, ch ->
            val g = FONT[ch] ?: return@forEachIndexed
            for (row in g.indices) for (col in 0 until 3) if (g[row][col] == '1') set(x + i * 4 + col, y + row, color)
        }
    }
}
