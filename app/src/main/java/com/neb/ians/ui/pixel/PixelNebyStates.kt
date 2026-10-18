package com.neb.ians.ui.pixel

import com.neb.ians.ui.pixel.PixelNeby.Eyes
import com.neb.ians.ui.pixel.PixelNeby.Mouth
import com.neb.ians.ui.pixel.PixelNeby.Pose
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
    Listen(140), Celebrate(85), Cool(120), Kiss(110), LookAround(130),
    // festivals
    Tika(120), Kite(130), Swing(90), Diyo(110), Deusi(95), Splash(90), Fireworks(100), Namaste(120);

    val sprite: PixelSprite get() = PixelNebyStates.sprite(this)
    fun sprite(look: NebyLook): PixelSprite = PixelNebyStates.sprite(this, look)
    /** The web and server name: LookAround -> look-around. */
    val key: String get() = name.replace(Regex("(?<!^)([A-Z])"), "-$1").lowercase()

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
            "tika", "blessing" -> Tika
            "kite", "changa" -> Kite
            "swing", "ping" -> Swing
            "diyo", "deepawali", "diwali", "lamp" -> Diyo
            "deusi", "bhailo", "dance" -> Deusi
            "splash", "gulal" -> Splash
            "fireworks" -> Fireworks
            "namaste", "bow" -> Namaste
            else -> Idle
        }

        /** The reactions a tap plays on an interactive Neby, in turn. */
        val reactions = listOf(Hop, Wink, Love, Laugh, Surprised, Cool, Kiss, Celebrate)
    }
}

object PixelNebyStates {
    private val cache = HashMap<Pair<NebyState, NebyLook>, PixelSprite>()
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

    fun sprite(s: NebyState, look: NebyLook = NebyLook.Classic): PixelSprite =
        synchronized(cache) { cache.getOrPut(s to look) { build(s, look) } }

    private fun frames(n: Int, s: NebyState, draw: PixelCanvas.(Int) -> Unit) =
        PixelSprite.build(PixelNeby.SIZE, PixelNeby.SIZE, n, s.frameMs, s.loop, draw)

    private fun bob(f: Int, n: Int, amp: Float = 1.5f) = -(sin(2 * PI * f / n).toFloat() * 0.5f + 0.5f) * amp

    private fun build(s: NebyState, look: NebyLook): PixelSprite {
        fun PixelCanvas.neby(p: Pose) { with(PixelNeby) { drawNeby(p.copy(look = look)) } }
        return when (s) {
        NebyState.Idle -> {
            val dys = floatArrayOf(0f, 0f, -0.5f, -1f, -1.5f, -1.5f, -1f, -0.5f, 0f, 0f, -0.5f, -1f, -1.5f, -1.5f, -1f, -0.5f)
            frames(dys.size, s) { f -> neby(Pose(dys[f], eyes = if (f == 14) Eyes.Blink else Eyes.Open, lookX = if (f in 5..9) 1 else 0, phase = f.toFloat())) }
        }
        NebyState.Still -> frames(1, s) { neby(Pose()) }
        NebyState.Blink -> frames(6, s) { f -> neby(Pose(eyes = if (f == 3) Eyes.Blink else Eyes.Open, phase = f.toFloat())) }
        NebyState.Hop -> {
            val poses = listOf(
                Triple(0f, 1f, 1f), Triple(0f, 1.12f, 0.86f), Triple(-3f, 0.92f, 1.1f), Triple(-7f, 0.96f, 1.04f),
                Triple(-9f, 1f, 1f), Triple(-7.5f, 1f, 1f), Triple(-3f, 0.96f, 1.04f), Triple(0f, 1.14f, 0.85f),
                Triple(0f, 1.05f, 0.95f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f), Triple(0f, 1f, 1f),
            )
            frames(poses.size, s) { f ->
                val (dy, sx, sy) = poses[f]
                neby(Pose(dy, sx, sy, eyes = if (f in 2..8) Eyes.Happy else Eyes.Open, mouth = if (f in 2..8) Mouth.Open else Mouth.None, phase = f * 1.5f))
            }
        }
        NebyState.Think -> frames(8, s) { f ->
            neby(Pose(if (f % 4 < 2) 0f else -0.5f, tilt = 0.06f, eyes = if (f == 6) Eyes.Blink else Eyes.Up, mouth = Mouth.Flat, phase = f * 1.2f))
            val n = f % 4
            for (i in 0 until 3) rect(31 + i * 5, 4 - if (i < n) 1 else 0, 3, 3, if (i < n) PixelNeby.band else PixelNeby.bandHi)
        }
        NebyState.Sleep -> frames(12, s) { f ->
            neby(Pose(if (f % 6 < 3) 0f else 0.5f, sx = 1.02f, sy = 0.98f, eyes = Eyes.Closed, mouth = if (f % 6 < 3) Mouth.None else Mouth.O, phase = f * 0.5f))
            for (k in 0 until 2) {
                val t = ((f + k * 6) % 12) / 12f
                zed(this, 33 + (t * 6).toInt() + k * 2, (15 - t * 13).toInt(), if (t < 0.8f) steel else steelHi)
            }
        }
        NebyState.Wink -> frames(10, s) { f ->
            val dy = floatArrayOf(0f, -1f, -2f, -2f, -2f, -2f, -1f, 0f, 0f, 0f)[f]
            neby(Pose(dy, eyes = if (f in 2..6) Eyes.Wink else Eyes.Open, mouth = if (f in 2..6) Mouth.Tongue else Mouth.None, phase = f.toFloat()))
            if (f in 3..5) sparkle(this, 39, 10, f - 3)
        }
        NebyState.Talk -> frames(8, s) { f ->
            val m = arrayOf(Mouth.Open, Mouth.Smile, Mouth.O, Mouth.Flat, Mouth.Open, Mouth.Smile, Mouth.O, Mouth.Smile)[f]
            neby(Pose(if (f % 2 == 0) -0.5f else 0f, eyes = if (f == 5) Eyes.Blink else Eyes.Open, mouth = m, phase = f * 1.4f))
        }
        NebyState.Love -> frames(12, s) { f ->
            neby(Pose(bob(f, 12), sx = 1f + 0.03f * sin(f * 0.5f), eyes = Eyes.Heart, mouth = Mouth.Smile, phase = f.toFloat()))
            for (k in 0 until 2) {
                val t = ((f + k * 6) % 12) / 12f
                heart(this, (8 + k * 30 + sin(t * 6f) * 2).roundToInt(), (16 - t * 14).roundToInt(), t < 0.75f)
            }
        }
        NebyState.Surprised -> frames(10, s) { f ->
            val dy = floatArrayOf(0f, -4f, -6f, -5f, -3f, -1f, 0f, 0f, 0f, 0f)[f]
            val sy = if (f == 1) 1.1f else if (f == 6) 0.92f else 1f
            neby(Pose(dy, 2f - sy, sy, eyes = Eyes.Big, mouth = Mouth.O, phase = f.toFloat()))
            if (f in 1..8) exclaim(this, 38, 3 + (if (f < 3) 2 - f else 0))
        }
        NebyState.Sad -> frames(12, s) { f ->
            neby(Pose(1f, 1.03f, 0.95f, eyes = Eyes.Sad, mouth = Mouth.Frown, lookY = 1, phase = f * 0.4f))
            // a tear wells under the left eye and rolls down the cheek
            val t = (f % 12) / 12f
            val ty = (31 + t * 9).roundToInt()
            if (t < 0.9f) { set(18, ty, tear); hline(17, 19, ty + 1, tear); set(18, ty + 2, tear); set(17, ty + 1, PixelNeby.white) }
        }
        NebyState.Laugh -> frames(10, s) { f ->
            val shake = if (f % 2 == 0) -1 else 1
            neby(Pose(if (f % 4 < 2) -1f else 0f, 1f + 0.04f * (f % 2), 1f - 0.04f * (f % 2), tilt = 0.07f * shake, eyes = Eyes.Happy, mouth = Mouth.Open, phase = f * 2f))
            if (f % 4 < 2) { tinyText(this, "ha", 33, 4, PixelNeby.band) }
        }
        NebyState.Dizzy -> frames(12, s) { f ->
            neby(Pose(0f, tilt = sin(f * PI.toFloat() / 6f) * 0.14f, eyes = Eyes.Spiral, mouth = Mouth.Flat, phase = f.toFloat()))
            for (k in 0 until 3) {
                val a = f * 2 * PI.toFloat() / 12f + k * 2.1f
                star(this, (24 + cos(a) * 14).roundToInt(), (7 + sin(a) * 3).roundToInt())
            }
        }
        NebyState.Wave -> frames(10, s) { f ->
            val tilt = sin(f * 2 * PI.toFloat() / 10f) * 0.12f
            neby(Pose(bob(f, 10, 1f), tilt = tilt, eyes = Eyes.Happy, mouth = Mouth.Smile, phase = f.toFloat()))
            // a little hand, waving from the side
            val hx = 40 + (sin(f * 2 * PI.toFloat() / 5f) * 2).roundToInt()
            disc(hx + 0.5f, 22.5f, 3.6f, PixelNeby.line); disc(hx + 0.5f, 22.5f, 2.6f, Px.rgb(0xCCE2FF)); set(hx - 1, 21, PixelNeby.white)
            bubble(this, "hi", 31, 1, f >= 2)
        }
        NebyState.Success -> frames(12, s) { f ->
            val dy = floatArrayOf(0f, 1f, -4f, -7f, -6f, -3f, 0f, 1f, 0f, 0f, 0f, 0f)[f]
            neby(Pose(dy, if (f == 1 || f == 7) 1.1f else 1f, if (f == 1 || f == 7) 0.9f else 1f, eyes = Eyes.Happy, mouth = Mouth.Smile, phase = f.toFloat()))
            if (f >= 3) check(this, 37, 2, ((f - 3) / 4f).coerceAtMost(1f))
        }
        NebyState.Oops -> frames(10, s) { f ->
            neby(Pose(0f, tilt = if (f in 2..5) (if (f % 2 == 0) 0.05f else -0.05f) else 0f, eyes = Eyes.Big, mouth = Mouth.Flat, lookX = if (f > 5) -1 else 0, phase = f.toFloat()))
            val t = (f % 10) / 10f
            sweat(this, 36, (17 + t * 5).roundToInt())
        }
        NebyState.Read -> frames(14, s) { f ->
            neby(Pose(bob(f, 14, 0.8f), eyes = if (f == 11) Eyes.Blink else Eyes.Down, mouth = Mouth.Smile, phase = f * 0.6f))
            book(this, 24, 34, (f % 14) / 14f)
        }
        NebyState.Listen -> frames(8, s) { f ->
            neby(Pose(0f, tilt = -0.12f, eyes = Eyes.Open, lookX = 2, mouth = Mouth.None, phase = f.toFloat()))
            val n = f % 4
            for (k in 0..n.coerceAtMost(2)) arc(this, 40 + k * 2, 20, 2 + k * 2)
        }
        NebyState.Celebrate -> frames(14, s) { f ->
            val dy = floatArrayOf(0f, 1f, -5f, -9f, -10f, -8f, -4f, 0f, 1f, 0f, -2f, -3f, -2f, 0f)[f]
            neby(Pose(dy, if (f == 1 || f == 8) 1.12f else 1f, if (f == 1 || f == 8) 0.88f else 1f, eyes = Eyes.Star, mouth = Mouth.Open, phase = f * 1.5f))
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
            neby(Pose(if (f > 5) bob(f, 4, 0.6f) else 0f, eyes = if (slide < 1f) Eyes.Open else Eyes.Shades, mouth = if (slide < 1f) Mouth.None else Mouth.Smile, phase = f.toFloat()))
            if (slide < 1f) {
                val y = (4 + slide * 15).roundToInt()
                rect(15, y, 7, 4, PixelNeby.eyes); rect(25, y, 7, 4, PixelNeby.eyes); hline(21, 25, y + 1, PixelNeby.eyes)
            }
            if (f in 6..8) sparkle(this, 36, 14, f - 6)
        }
        NebyState.Kiss -> frames(12, s) { f ->
            neby(Pose(bob(f, 12, 1f), tilt = 0.06f, eyes = Eyes.Closed, mouth = Mouth.Kiss, blush = true, phase = f.toFloat()))
            val t = (f % 12) / 12f
            if (f >= 3) heart(this, (31 + t * 8).roundToInt(), (20 - t * 16).roundToInt(), true)
        }
        NebyState.LookAround -> frames(12, s) { f ->
            val gaze = intArrayOf(0, -1, -2, -2, -2, -1, 0, 1, 2, 2, 2, 1)[f]
            neby(Pose(0f, eyes = if (f == 6) Eyes.Blink else Eyes.Open, lookX = gaze, phase = f.toFloat()))
        }

        // ---- festivals ----------------------------------------------------------------------------

        // Dashain: Neby bows, an elder's hand comes down with the tika, jamara is tucked behind the ear
        NebyState.Tika -> frames(18, s) { f ->
            val bow = f in 2..10
            val given = f >= 8
            neby(Pose(if (bow) 1f else if (f in 12..14) -2f else 0f, if (bow) 1.03f else 1f, if (bow) 0.95f else 1f,
                eyes = when { bow -> Eyes.Closed; given -> Eyes.Happy; else -> Eyes.Open }, mouth = if (given) Mouth.Smile else Mouth.None,
                blush = given, tika = given, jamara = f >= 10, phase = f.toFloat()))
            // the hand: down from the top left, a pause on the forehead, then away
            val k = when { f < 3 -> -1f; f <= 7 -> (f - 3) / 4f; f <= 10 -> 1f - (f - 7) / 4f * 0.2f; f <= 13 -> 0.8f - (f - 10) / 3f; else -> -1f }
            if (k >= 0f) hand(this, (k * 15).roundToInt(), (-10 + k * 19).roundToInt())
            if (f in 13..16) sparkle(this, 39, 9, (f - 13).coerceAtMost(2))
        }
        // Dashain: flying a changa from the rooftop, the string running up to the kite
        NebyState.Kite -> frames(16, s) { f ->
            val a = f * 2 * PI.toFloat() / 16f
            neby(Pose(bob(f, 16, 0.6f), tilt = 0.05f, eyes = Eyes.Up, lookX = 1, mouth = Mouth.Smile, phase = f.toFloat()))
            val kx = 42 + (sin(a) * 1.5f).roundToInt(); val ky = 5 + (sin(a * 2f) * 1.5f).roundToInt()
            behind(this) { line(38, 32, kx, ky + 4, steelHi) }
            kite(this, kx, ky, a)
        }
        // Dashain: the bamboo ping, swinging high
        NebyState.Swing -> frames(16, s) { f ->
            val a = sin(f * 2 * PI.toFloat() / 16f) * 0.2f
            val dx = 60f * sin(a); val lift = -(60f - 60f * cos(a)) * 0.6f
            val high = kotlin.math.abs(a) > 0.15f
            neby(Pose(lift, dx = dx, tilt = -a * 0.6f, eyes = if (high) Eyes.Happy else Eyes.Open, mouth = if (high) Mouth.Open else Mouth.Smile, phase = f.toFloat()))
            val sx = 24 + dx.roundToInt(); val sy = (45f + lift).roundToInt()
            behind(this) { line(14, 0, sx - 11, sy, bamboo); line(34, 0, sx + 11, sy, bamboo) }
            rect(sx - 13, sy, 27, 2, plank); hline(sx - 13, sx + 13, sy + 2, plankLo)
        }
        // Tihar: a diyo in front of Neby, its flame dancing, the glow on Neby's face
        NebyState.Diyo -> frames(12, s) { f ->
            neby(Pose(0f, eyes = if (f == 9) Eyes.Blink else Eyes.Happy, lookY = 1, mouth = Mouth.Smile, blush = true, phase = f * 0.6f))
            diyo(this, 24, 41, f)
        }
        // Tihar: deusi-bhailo, a hopping dance from side to side with music in the air
        NebyState.Deusi -> frames(12, s) { f ->
            val side = if (f < 6) -1f else 1f
            val k = f % 6
            val dy = floatArrayOf(0f, -3f, -5f, -3f, 0f, 0f)[k]
            val sq = if (k == 4) 0.9f else 1f
            neby(Pose(dy, 2f - sq, sq, dx = side * 3f, tilt = side * 0.1f, eyes = Eyes.Happy, mouth = if (k in 1..3) Mouth.Open else Mouth.Smile, phase = f * 1.5f))
            for (n in 0 until 2) {
                val t = ((f + n * 6) % 12) / 12f
                note(this, (6 + n * 32 + sin(t * 6f) * 2).roundToInt(), (18 - t * 16).roundToInt(), if (n == 0) PixelNeby.band else PixelNeby.pink)
            }
        }
        // Holi: a puff of gulal, a surprised Neby, then a colourful, laughing one
        NebyState.Splash -> frames(16, s) { f ->
            val paint = ((f - 4) / 5f).coerceIn(0f, 1f)
            val shake = if (f in 5..7) (if (f % 2 == 0) 0.06f else -0.06f) else 0f
            neby(Pose(if (f in 9..11) -2f else 0f, tilt = shake, eyes = when { f < 4 -> Eyes.Open; f < 8 -> Eyes.Big; else -> Eyes.Happy },
                mouth = when { f < 4 -> Mouth.None; f < 8 -> Mouth.O; else -> Mouth.Open }, paint = paint, phase = f.toFloat()))
            // the cloud of powder, flying in from the left and settling
            if (f in 2..12) for (k in 0 until 26) {
                val t = (f - 2) / 10f
                val ang = k * 2.4f
                val r = 4f + t * 16f + (k % 5)
                val x = (12 + t * 10 + cos(ang) * r).roundToInt(); val y = (24 + sin(ang) * r * 0.7f).roundToInt()
                if (Bayer.threshold(x, y) > t * 0.9f && (get(x, y) ushr 24) == 0) set(x, y, gulal[k % gulal.size])
            }
        }
        // New Year, Tihar: bursts of light overhead, reflected in Neby's eyes
        NebyState.Fireworks -> frames(16, s) { f ->
            neby(Pose(bob(f, 16, 0.6f), eyes = if (f % 8 in 2..5) Eyes.Star else Eyes.Up, mouth = Mouth.O, phase = f.toFloat()))
            burst(this, 10, 9, f, gold, goldHi)
            burst(this, 38, 6, (f + 8) % 16, PixelNeby.pink, PixelNeby.pinkHi)
        }
        // Namaste: palms together, a small bow, eyes closed, then a smile
        NebyState.Namaste -> frames(12, s) { f ->
            val bow = f in 3..8
            neby(Pose(if (bow) 1.5f else 0f, 1f, if (bow) 0.95f else 1f, eyes = if (bow) Eyes.Closed else Eyes.Happy, mouth = Mouth.Smile, phase = f.toFloat()))
            palms(this, 24, if (bow) 35 else 34)
        }
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

    private val bamboo = Px.rgb(0x8A6A3A)
    private val plank = Px.rgb(0x9C6B3C)
    private val plankLo = Px.rgb(0x6E4824)
    private val skin = Px.rgb(0xE2A878)
    private val skinLo = Px.rgb(0xC0825A)
    private val clay = Px.rgb(0xC0602A)
    private val clayLo = Px.rgb(0x8E4420)
    private val flame = Px.rgb(0xFFD23F)
    private val flameHi = Px.rgb(0xFFF6C8)
    private val flameLo = Px.rgb(0xFF8C1A)
    private val glow = Px.rgb(0xFFE9A8)
    private val gulal = intArrayOf(Px.rgb(0xFF4FA3), Px.rgb(0x2DCB73), Px.rgb(0xFFD23F), Px.rgb(0x9B5DE5), Px.rgb(0xFF8C42), Px.rgb(0x3FA7FF))

    /** An elder's arm and hand reaching in from the top left, ring finger dipped in red. (x, y) is the hand. */
    private fun hand(c: PixelCanvas, x: Int, y: Int) = with(c) {
        // the sleeve, from off-canvas to the wrist
        for (w in -2..2) line(x - 12 + w, y - 14, x + 1 + w, y + 1, Px.rgb(0x8E2430))
        for (w in -1..1) line(x - 12 + w, y - 15, x + w, y, Px.rgb(0xB0303F))
        // the hand, fingers pointing down and right
        polygon(floatArrayOf(x - 1f, y + 1f, x + 5f, y - 1f, x + 10f, y + 6f, x + 7f, y + 10f, x + 2f, y + 8f), PixelNeby.line)
        polygon(floatArrayOf(x + 0f, y + 1.5f, x + 5f, y + 0f, x + 9f, y + 6f, x + 6.5f, y + 9f, x + 2.5f, y + 7f), skin)
        line(x + 3, y + 6, x + 6, y + 8, skinLo)
        set(x + 8, y + 8, Px.rgb(0xD7263D)); set(x + 7, y + 9, Px.rgb(0xD7263D))
    }

    /** Draws [block] only where nothing has been drawn yet, so ropes and strings pass behind Neby. */
    private fun behind(c: PixelCanvas, block: PixelCanvas.() -> Unit) {
        val layer = PixelCanvas(c.width, c.height)
        layer.block()
        for (i in c.pixels.indices) if ((c.pixels[i] ushr 24) == 0 && (layer.pixels[i] ushr 24) != 0) c.pixels[i] = layer.pixels[i]
    }

    /** A Nepali changa: a diamond in four colours with a tail. */
    private fun kite(c: PixelCanvas, x: Int, y: Int, a: Float) = with(c) {
        val cols = intArrayOf(Px.rgb(0xE53935), Px.rgb(0xFDD835), Px.rgb(0x1E88E5), Px.rgb(0x43A047))
        for (dy in -4..4) for (dx in -4..4) {
            if (kotlin.math.abs(dx) + kotlin.math.abs(dy) > 4) continue
            val q = (if (dx < 0) 0 else 1) + (if (dy < 0) 0 else 2)
            set(x + dx, y + dy, if (kotlin.math.abs(dx) + kotlin.math.abs(dy) == 4) PixelNeby.line else cols[q])
        }
        for (k in 1..5) set(x + (sin(a + k * 0.9f) * 1.5f).roundToInt(), y + 4 + k, if (k % 2 == 0) cols[0] else cols[1])
    }

    private fun diyo(c: PixelCanvas, x: Int, y: Int, f: Int) = with(c) {
        // glow first, so the lamp and Neby's band sit inside it
        for (yy in y - 10..y + 2) for (xx in x - 9..x + 9) {
            val d = kotlin.math.hypot((xx - x).toFloat(), (yy - y + 4).toFloat())
            if (d < 9f && (get(xx, yy) ushr 24) == 0 && Bayer.threshold(xx, yy) < (1f - d / 9f) * 0.55f) set(xx, yy, glow)
        }
        ellipse(x + 0.5f, y + 2.5f, 6.5f, 3f, PixelNeby.line)
        ellipse(x + 0.5f, y + 2f, 5.5f, 2.2f, clay)
        hline(x - 3, x + 4, y + 3, clayLo)
        hline(x - 4, x + 5, y + 1, clayLo)
        val h = intArrayOf(5, 6, 5, 4, 6, 5, 6, 4, 5, 6, 5, 5)[f % 12]
        val sway = intArrayOf(0, 0, 1, 0, -1, 0, 0, 1, 0, 0, -1, 0)[f % 12]
        for (k in 0 until h) {
            val w = if (k < 2) 1 else 0
            val col = if (k < 2) flameLo else if (k < h - 1) flame else flameHi
            hline(x - w + (if (k > h / 2) sway else 0), x + w + (if (k > h / 2) sway else 0), y - k, col)
        }
        set(x, y - 1, flameHi)
    }

    private fun note(c: PixelCanvas, x: Int, y: Int, col: Int) = with(c) {
        rect(x, y + 3, 2, 2, col); line(x + 1, y, x + 1, y + 3, col); set(x + 2, y, col); set(x + 3, y + 1, col)
    }

    /** A firework: a rising spark, then two rings of light that spread and fade. */
    private fun burst(c: PixelCanvas, x: Int, y: Int, f: Int, col: Int, hi: Int) = with(c) {
        if (f < 4) { set(x, y + 10 - f * 3, hi); set(x, y + 11 - f * 3, col); set(x, y + 12 - f * 3, goldHi); return@with }
        val t = (f - 4) / 11f
        if (t > 1f) return@with
        if (f == 4) { rect(x - 1, y - 1, 3, 3, hi); return@with }
        val r = 2f + t * 9f
        for (k in 0 until 16) {
            val a = k * PI.toFloat() / 8f
            val px = (x + cos(a) * r).roundToInt(); val py = (y + sin(a) * r).roundToInt()
            if (Bayer.threshold(px, py) > t * t) { set(px, py, if (k % 2 == 0) hi else col); if (t < 0.4f) set(px, py + 1, col) }
            if (k % 2 == 0 && t < 0.7f) set((x + cos(a) * r * 0.55f).roundToInt(), (y + sin(a) * r * 0.55f).roundToInt(), goldHi)
        }
    }

    /** Two small hands, palms together, fingertips up. */
    private fun palms(c: PixelCanvas, x: Int, y: Int) = with(c) {
        polygon(floatArrayOf(x - 4.5f, y + 9f, x - 4f, y + 3f, x - 0.5f, y - 2f, x + 1.5f, y - 2f, x + 5f, y + 3f, x + 5.5f, y + 9f), PixelNeby.line)
        polygon(floatArrayOf(x - 3.5f, y + 8f, x - 3f, y + 3.5f, x - 0.2f, y - 0.8f, x + 1.2f, y - 0.8f, x + 4f, y + 3.5f, x + 4.5f, y + 8f), Px.rgb(0xF4F9FF))
        line(x, y, x, y + 7, Px.rgb(0x93B5EC))
        hline(x - 3, x + 3, y + 7, Px.rgb(0xCCE2FF))
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
