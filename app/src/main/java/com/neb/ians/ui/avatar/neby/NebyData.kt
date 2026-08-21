package com.neb.ians.ui.avatar.neby

data class NebyExpression(
    val id: String,
    val headX: Double, val headY: Double, val headZ: Double,
    val widthLeft: Double, val widthRight: Double,
    val heightLeft: Double, val heightRight: Double,
    val spacing: Double,
    val positionXLeft: Double = 0.0, val positionXRight: Double = 0.0,
    val positionYLeft: Double, val positionYRight: Double,
    val leftAngle: Double = 0.0, val rightAngle: Double = 0.0,
    val perspective: Double = 1.0,
    val eyeMotion: String = "none", val bodyMotion: String = "none",
    val mouth: String = "none", val mouthScale: Double = 1.0,
    val mouthOffsetX: Double = 0.0, val mouthOffsetY: Double = 0.0,
    val mouthWidth: Double = 1.0, val mouthCurve: Double = 1.0,
    val effect: String = "none",
    val bodyColor: String? = null,
    val eyeStyle: String = "dot"
)

private val BASE = NebyExpression(
    id = "expression-neutral", headX = 0.0, headY = 0.0, headZ = 0.0,
    widthLeft = 20.0, widthRight = 20.0, heightLeft = 50.0, heightRight = 50.0,
    spacing = 35.0, positionYLeft = -7.0, positionYRight = -7.0
)

private val Z_NUMERIC = listOf(
    doubleArrayOf(7.3, 27.8, -16.1, 24.2, 27.6, 38.9, 40.7, 54.3, -20.5, 0.0, 0.0),
    doubleArrayOf(-35.6, 0.7, -8.5, 29.4, 27.3, 49.5, 49.8, 57.7, -42.0, 0.0, 0.0),
    doubleArrayOf(-36.2, 13.1, 15.5, 44.3, 51.3, 74.2, 76.0, 68.7, -40.7, 0.0, 0.0),
    doubleArrayOf(15.6, -16.5, -11.3, 54.0, 51.0, 49.6, 48.5, 70.9, 30.1, 0.0, 0.0),
    doubleArrayOf(3.4, 13.0, 8.9, 42.6, 44.0, 17.3, 16.0, 57.9, 4.9, 0.0, 0.0),
    doubleArrayOf(-17.7, -1.4, -8.8, 29.5, 19.2, 51.6, 41.9, 56.3, 0.0, 0.0, 90.0),
    doubleArrayOf(14.8, 14.5, 5.5, 22.9, 22.2, 32.4, 33.4, 50.9, 39.2, 0.0, 0.0),
    doubleArrayOf(25.7, 16.5, -13.5, 48.5, 48.3, 33.5, 33.0, 53.3, 41.3, 61.3, -80.0),
    doubleArrayOf(-22.8, -15.9, 6.2, 44.5, 43.9, 32.3, 24.6, 54.9, -42.0, -60.9, 69.2),
    doubleArrayOf(-11.6, 8.3, -12.7, 42.5, 22.1, 41.8, 22.2, 61.7, 12.3, 0.0, 0.0),
    doubleArrayOf(20.3, 7.0, 8.7, 30.2, 28.1, 48.8, 49.2, 56.8, 39.9, 0.0, 0.0),
    doubleArrayOf(17.5, -15.2, -8.7, 51.0, 49.2, 75.3, 73.4, 70.2, 41.6, 0.0, 0.0),
    doubleArrayOf(-10.4, 15.2, 11.8, 50.6, 51.6, 50.0, 50.7, 69.5, 16.7, 0.0, 0.0),
    doubleArrayOf(-6.0, -7.7, -9.4, 43.6, 42.8, 15.5, 18.1, 57.9, 3.5, 0.0, 0.0),
    doubleArrayOf(0.2, -3.1, 9.0, 29.6, 16.8, 51.5, 41.3, 56.4, -7.8, 0.0, 90.0),
    doubleArrayOf(-16.2, 38.4, 2.4, 23.7, 26.2, 32.7, 34.6, 53.9, -41.1, 0.0, 0.0),
    doubleArrayOf(3.5, -16.1, 15.8, 51.0, 48.5, 34.9, 33.0, 55.1, 41.9, 80.0, -62.2),
    doubleArrayOf(-17.3, 11.2, -9.1, 24.2, 44.5, 44.5, 32.2, 55.0, -36.5, 18.5, 67.9),
    doubleArrayOf(-0.7, 3.6, 12.2, 42.1, 22.2, 41.7, 22.1, 60.4, -9.1, 0.0, 0.0),
    doubleArrayOf(-25.3, -12.4, -13.3, 30.5, 26.8, 49.9, 48.8, 56.2, -35.8, 0.0, 0.0),
    doubleArrayOf(-41.1, 20.2, 18.8, 44.6, 53.0, 74.9, 77.8, 70.8, -40.6, 0.0, 0.0),
    doubleArrayOf(-14.6, -12.5, -16.1, 51.4, 50.5, 50.1, 49.4, 69.0, -20.0, 0.0, 0.0),
    doubleArrayOf(10.0, 2.7, 8.8, 42.9, 43.3, 16.4, 17.8, 57.9, 2.7, 0.0, 0.0),
    doubleArrayOf(-17.8, 10.0, -6.3, 28.8, 17.3, 51.4, 42.7, 56.6, -9.8, 0.0, 90.0),
    doubleArrayOf(-29.6, 7.5, 10.1, 21.5, 23.2, 32.0, 33.5, 51.2, -37.4, 0.0, 0.0)
)

private fun numExpr(idx: Int): NebyExpression {
    val a = Z_NUMERIC[idx]
    return BASE.copy(
        id = "expression-${idx.toString().padStart(2, '0')}",
        headX = a[0], headY = a[1], headZ = a[2],
        widthLeft = a[3], widthRight = a[4], heightLeft = a[5], heightRight = a[6],
        spacing = a[7], positionYLeft = a[8], positionYRight = a[8],
        leftAngle = a[9], rightAngle = a[10]
    )
}

private fun ex(id: String, block: NebyExpression.() -> NebyExpression): NebyExpression = BASE.copy(id = id).block()

val NEBY_EXPRESSIONS: List<NebyExpression> by lazy {
    val nums = Z_NUMERIC.indices.map { numExpr(it) }
    val named = listOf(
        ex("joy") { copy(headX = 5.0, headY = -5.0, headZ = -2.0, widthLeft = 30.0, widthRight = 30.0, heightLeft = 18.0, heightRight = 18.0, spacing = 38.0, positionYLeft = -2.0, positionYRight = -2.0, leftAngle = 8.0, rightAngle = -8.0, mouthScale = 1.15, eyeMotion = "sparkle", effect = "sparkles", bodyMotion = "bob") },
        ex("soft-smile") { copy(headX = 2.0, widthLeft = 24.0, widthRight = 24.0, heightLeft = 30.0, heightRight = 30.0, mouthScale = 0.9, eyeMotion = "microSaccades", bodyMotion = "breathe") },
        ex("wink") { copy(headY = -10.0, headZ = -6.0, widthLeft = 26.0, widthRight = 27.0, heightLeft = 8.0, heightRight = 34.0, spacing = 38.0, leftAngle = -8.0, rightAngle = 6.0, eyeMotion = "squintPulse", bodyMotion = "sway") },
        ex("love") { copy(headX = 4.0, widthLeft = 31.0, widthRight = 31.0, heightLeft = 28.0, heightRight = 28.0, spacing = 39.0, positionYLeft = -3.0, positionYRight = -3.0, leftAngle = 10.0, rightAngle = -10.0, mouthScale = 1.05, eyeMotion = "sparkle", effect = "hearts", bodyMotion = "float", bodyColor = "#ff6f91") },
        ex("smug") { copy(headY = 14.0, headZ = 8.0, widthLeft = 27.0, widthRight = 19.0, heightLeft = 19.0, heightRight = 16.0, positionYLeft = -4.0, positionYRight = -1.0, leftAngle = -8.0, rightAngle = 10.0, eyeMotion = "microSaccades") },
        ex("skeptical") { copy(headY = -13.0, headZ = -5.0, widthLeft = 24.0, widthRight = 20.0, heightLeft = 20.0, heightRight = 13.0, positionYLeft = -3.0, positionYRight = 1.0, leftAngle = 12.0, rightAngle = -12.0, eyeMotion = "squintPulse") },
        ex("side-eye") { copy(headY = 8.0, widthLeft = 23.0, widthRight = 23.0, heightLeft = 21.0, heightRight = 21.0, positionXLeft = 11.0, positionXRight = 11.0, positionYLeft = -3.0, positionYRight = -3.0, eyeMotion = "dart") },
        ex("focus") { copy(headX = -4.0, widthLeft = 20.0, widthRight = 20.0, heightLeft = 22.0, heightRight = 22.0, spacing = 32.0, positionYLeft = -5.0, positionYRight = -5.0, leftAngle = -5.0, rightAngle = 5.0, eyeMotion = "focusPulse", bodyMotion = "breathe") },
        ex("scan-left") { copy(headY = -10.0, widthLeft = 23.0, widthRight = 23.0, heightLeft = 29.0, heightRight = 29.0, positionXLeft = -13.0, positionXRight = -13.0, eyeMotion = "dart") },
        ex("scan-right") { copy(headY = 10.0, widthLeft = 23.0, widthRight = 23.0, heightLeft = 29.0, heightRight = 29.0, positionXLeft = 13.0, positionXRight = 13.0, eyeMotion = "dart") },
        ex("talk-a") { copy(widthLeft = 24.0, widthRight = 24.0, heightLeft = 31.0, heightRight = 31.0, mouthScale = 0.8, eyeMotion = "microSaccades") },
        ex("talk-b") { copy(headZ = 2.0, widthLeft = 23.0, widthRight = 23.0, heightLeft = 28.0, heightRight = 28.0, eyeMotion = "focusPulse", mouthScale = 0.72) },
        ex("talk-c") { copy(headZ = -2.0, widthLeft = 25.0, widthRight = 25.0, heightLeft = 27.0, heightRight = 27.0, eyeMotion = "sparkle", mouthScale = 0.78) },
        ex("gasp") { copy(headX = 7.0, widthLeft = 33.0, widthRight = 33.0, heightLeft = 47.0, heightRight = 47.0, spacing = 40.0, positionYLeft = -5.0, positionYRight = -5.0, mouthScale = 1.1, eyeMotion = "anticipate", effect = "alert", bodyMotion = "bounce") },
        ex("panic") { copy(headX = 7.0, headZ = 5.0, widthLeft = 31.0, widthRight = 31.0, heightLeft = 48.0, heightRight = 48.0, spacing = 42.0, leftAngle = -14.0, rightAngle = 14.0, eyeMotion = "shake", effect = "alert", bodyMotion = "shake") },
        ex("sad-deep") { copy(headX = -8.0, widthLeft = 22.0, widthRight = 22.0, heightLeft = 20.0, heightRight = 20.0, positionYLeft = 4.0, positionYRight = 4.0, leftAngle = -12.0, rightAngle = 12.0, eyeMotion = "squintPulse", bodyMotion = "slowDrift") },
        ex("angry-hot") { copy(headX = -5.0, widthLeft = 25.0, widthRight = 25.0, heightLeft = 15.0, heightRight = 15.0, spacing = 32.0, leftAngle = 18.0, rightAngle = -18.0, eyeMotion = "squintPulse", effect = "errorPulse", bodyMotion = "shake", bodyColor = "#ef5350") },
        ex("sleepy") { copy(headX = -6.0, widthLeft = 24.0, widthRight = 24.0, heightLeft = 8.0, heightRight = 8.0, positionYLeft = 1.0, positionYRight = 1.0, eyeMotion = "squintPulse", effect = "zzz", bodyMotion = "breathe") },
        ex("kiss") { copy(headX = 4.0, headZ = -6.0, widthLeft = 25.0, widthRight = 25.0, heightLeft = 20.0, heightRight = 20.0, leftAngle = 7.0, rightAngle = -7.0, mouthScale = 0.9, eyeMotion = "sparkle", effect = "hearts", bodyMotion = "sway") },
        ex("cat-cute") { copy(headX = 3.0, widthLeft = 30.0, widthRight = 30.0, heightLeft = 31.0, heightRight = 31.0, spacing = 38.0, mouthScale = 0.8, eyeMotion = "sparkle", bodyMotion = "bob") },
        ex("dizzy") { copy(headZ = 12.0, widthLeft = 19.0, widthRight = 29.0, heightLeft = 17.0, heightRight = 34.0, leftAngle = 35.0, rightAngle = -32.0, eyeMotion = "orbit", effect = "sparkles", bodyMotion = "sway") },
        ex("notification") { copy(headX = 6.0, widthLeft = 31.0, widthRight = 31.0, heightLeft = 40.0, heightRight = 40.0, spacing = 39.0, eyeMotion = "dart", effect = "alert", bodyMotion = "bounce") },
        ex("success") { copy(headX = 6.0, headZ = -3.0, widthLeft = 28.0, widthRight = 28.0, heightLeft = 19.0, heightRight = 19.0, eyeMotion = "sparkle", effect = "successBurst", bodyMotion = "bounce", bodyColor = "#39c98a") },
        ex("error") { copy(headX = -5.0, headZ = 4.0, widthLeft = 24.0, widthRight = 24.0, heightLeft = 14.0, heightRight = 14.0, leftAngle = 14.0, rightAngle = -14.0, eyeMotion = "shake", effect = "errorPulse", bodyMotion = "shake", bodyColor = "#ff5f6d") },
        ex("confetti") { copy(headX = 8.0, headY = -4.0, widthLeft = 32.0, widthRight = 32.0, heightLeft = 22.0, heightRight = 22.0, spacing = 40.0, mouthScale = 1.2, eyeMotion = "sparkle", effect = "confetti", bodyMotion = "bounce") },
        ex("idle-front") { copy(widthLeft = 24.0, widthRight = 24.0, heightLeft = 36.0, heightRight = 36.0, spacing = 36.0, positionYLeft = -6.0, positionYRight = -6.0, eyeMotion = "microSaccades", bodyMotion = "breathe") },
        ex("idle-glance-left") { copy(headY = -6.0, headZ = -1.5, widthLeft = 24.0, widthRight = 24.0, heightLeft = 32.0, heightRight = 32.0, spacing = 36.0, positionXLeft = -7.0, positionXRight = -7.0, positionYLeft = -6.0, positionYRight = -6.0, bodyMotion = "breathe") },
        ex("idle-glance-right") { copy(headY = 6.0, headZ = 1.5, widthLeft = 24.0, widthRight = 24.0, heightLeft = 32.0, heightRight = 32.0, spacing = 36.0, positionXLeft = 7.0, positionXRight = 7.0, positionYLeft = -6.0, positionYRight = -6.0, bodyMotion = "breathe") },
        ex("delight") { copy(headX = 5.0, headZ = -3.0, widthLeft = 31.0, widthRight = 31.0, heightLeft = 24.0, heightRight = 24.0, spacing = 40.0, leftAngle = 9.0, rightAngle = -9.0, eyeMotion = "sparkle", bodyMotion = "bounce", effect = "sparkles") },
        ex("eye-roll") { copy(headX = -2.0, widthLeft = 24.0, widthRight = 24.0, heightLeft = 25.0, heightRight = 25.0, spacing = 37.0, positionYLeft = -12.0, positionYRight = -12.0, eyeMotion = "orbit", bodyMotion = "sway") },
        ex("concern") { copy(headX = -5.0, headZ = -4.0, widthLeft = 23.0, widthRight = 23.0, heightLeft = 26.0, heightRight = 19.0, spacing = 35.0, positionYLeft = 0.0, positionYRight = 2.0, leftAngle = -11.0, rightAngle = 8.0, eyeMotion = "microSaccades", bodyMotion = "slowDrift") },
        ex("listening-focus") { copy(headX = 2.0, headY = -5.0, headZ = -2.0, widthLeft = 25.0, widthRight = 27.0, heightLeft = 34.0, heightRight = 37.0, spacing = 37.0, positionYLeft = -6.0, positionYRight = -6.0, leftAngle = -4.0, rightAngle = 3.0, eyeMotion = "microSaccades", bodyMotion = "breathe") },
        ex("puzzled") { copy(headX = -2.0, headY = 9.0, headZ = 5.0, widthLeft = 27.0, widthRight = 21.0, heightLeft = 35.0, heightRight = 20.0, spacing = 37.0, positionYLeft = -6.0, positionYRight = -1.0, leftAngle = 10.0, rightAngle = -8.0, eyeMotion = "squintPulse", bodyMotion = "sway", effect = "question") },
        ex("determined") { copy(headX = -4.0, widthLeft = 27.0, widthRight = 27.0, heightLeft = 17.0, heightRight = 17.0, spacing = 31.0, leftAngle = 15.0, rightAngle = -15.0, eyeMotion = "focusPulse", bodyMotion = "breathe") },
        ex("anticipation") { copy(headX = 4.0, widthLeft = 29.0, widthRight = 29.0, heightLeft = 41.0, heightRight = 41.0, spacing = 40.0, positionYLeft = -5.0, positionYRight = -5.0, eyeMotion = "anticipate", bodyMotion = "bob") },
        ex("cheer") { copy(headX = 8.0, headZ = -5.0, widthLeft = 32.0, widthRight = 32.0, heightLeft = 18.0, heightRight = 18.0, spacing = 41.0, leftAngle = 12.0, rightAngle = -12.0, eyeMotion = "sparkle", bodyMotion = "bounce", effect = "confetti") },
        ex("intro-neby-closed") { copy(headX = -10.0, headY = -13.0, headZ = -7.0, widthLeft = 27.0, widthRight = 27.0, heightLeft = 6.0, heightRight = 6.0, spacing = 36.0, positionYLeft = 4.0, positionYRight = 4.0, bodyMotion = "slowDrift", effect = "introGlow") },
        ex("intro-neby-peek") { copy(headX = -4.0, headY = 9.0, headZ = 4.0, widthLeft = 27.0, widthRight = 27.0, heightLeft = 19.0, heightRight = 31.0, spacing = 38.0, positionXLeft = 5.0, positionXRight = 5.0, leftAngle = -7.0, rightAngle = 6.0, eyeMotion = "anticipate", effect = "introGlow") },
        ex("intro-neby-focus") { copy(headX = 1.0, widthLeft = 29.0, widthRight = 29.0, heightLeft = 39.0, heightRight = 39.0, spacing = 40.0, positionYLeft = -7.0, positionYRight = -7.0, eyeMotion = "focusPulse", bodyMotion = "breathe", effect = "introGlow") },
        ex("intro-neby-signature") { copy(headX = 5.0, headZ = -2.0, widthLeft = 31.0, widthRight = 31.0, heightLeft = 23.0, heightRight = 23.0, spacing = 42.0, leftAngle = 8.0, rightAngle = -8.0, eyeMotion = "sparkle", bodyMotion = "float", effect = "sparkles") },
        ex("intro-pop") { copy(headX = 7.0, widthLeft = 34.0, widthRight = 34.0, heightLeft = 43.0, heightRight = 43.0, spacing = 42.0, eyeMotion = "anticipate", bodyMotion = "bounce", effect = "successBurst") },
        ex("intro-scan") { copy(headY = -7.0, widthLeft = 25.0, widthRight = 25.0, heightLeft = 31.0, heightRight = 31.0, spacing = 38.0, eyeMotion = "dart", bodyMotion = "slowDrift", effect = "introGlow") },
        ex("orbit") { copy(headX = 28.5, headY = 28.6, headZ = -13.0, widthLeft = 22.0, widthRight = 22.0, heightLeft = 46.0, heightRight = 46.0, spacing = 38.0, positionYLeft = -4.0, positionYRight = -4.0, eyeMotion = "orbit", bodyMotion = "float", effect = "orbit") },
        ex("play") { copy(headX = 12.0, headY = -8.0, headZ = -6.0, widthLeft = 22.0, widthRight = 22.0, heightLeft = 42.0, heightRight = 42.0, spacing = 36.0, eyeMotion = "none", bodyMotion = "slowDrift", effect = "playArcs") }
    )
    nums + named
}

val EXPR_BY_ID: Map<String, NebyExpression> by lazy { NEBY_EXPRESSIONS.associateBy { it.id } }

data class AnimStep(val expressionId: String, val holdMs: Int, val transitionMs: Int, val transition: String)
data class NebyAnimation(
    val id: String, val playbackMode: String,
    val steps: List<AnimStep>,
    val blinkEnabled: Boolean, val blinkInitialMs: Int, val blinkMinMs: Int, val blinkMaxMs: Int, val blinkDurMs: Int
)

private fun q(vararg ids: String) = ids.toList()

private val GT: Map<String, List<String>> = mapOf(
    "intro-neby" to q("intro-neby-closed", "intro-neby-peek", "intro-neby-focus", "intro-neby-signature", "idle-front"),
    "intro-cinematic" to q("sleepy", "anticipation", "focus", "delight", "idle-front"),
    "intro-pop" to q("sleepy", "intro-pop", "cheer", "soft-smile"),
    "intro-scan" to q("scan-left", "scan-right", "intro-scan", "determined", "idle-front"),
    "sleeping" to q("sleepy", "sleepy", "sleepy"),
    "waking" to q("sleepy", "anticipation", "idle-front"),
    "idle" to q("idle-front", "idle-glance-left", "idle-front", "idle-glance-right"),
    "listening" to q("idle-front", "listening-focus", "idle-front"),
    "thinking" to q("skeptical", "eye-roll", "side-eye", "focus"),
    "searching" to q("scan-left", "focus", "scan-right"),
    "working" to q("focus", "scan-left", "determined", "scan-right"),
    "speaking" to q("talk-a", "talk-b", "talk-c", "soft-smile"),
    "presenting" to q("focus", "soft-smile", "anticipation", "soft-smile"),
    "scanning" to q("scan-left", "intro-scan", "scan-right"),
    "excited" to q("anticipation", "delight", "cheer", "joy"),
    "surprised" to q("anticipation", "gasp", "delight"),
    "suspicious" to q("skeptical", "side-eye", "determined"),
    "angry" to q("determined", "angry-hot", "skeptical"),
    "drowsy" to q("sleepy", "concern", "sleepy"),
    "happy" to q("soft-smile", "delight", "joy"),
    "curious" to q("anticipation", "side-eye", "focus"),
    "confused" to q("skeptical", "puzzled", "eye-roll"),
    "bored" to q("sleepy", "side-eye", "eye-roll"),
    "proud" to q("smug", "soft-smile", "determined"),
    "shy" to q("soft-smile", "kiss", "concern"),
    "sad" to q("concern", "sad-deep", "concern"),
    "laughing" to q("joy", "delight", "joy"),
    "scared" to q("anticipation", "panic", "gasp"),
    "playful" to q("wink", "cat-cute", "side-eye", "joy"),
    "celebrate" to q("cheer", "confetti", "success", "joy"),
    "greeting" to q("anticipation", "wink", "soft-smile", "delight"),
    "agree" to q("soft-smile", "success", "idle-front"),
    "disagree" to q("skeptical", "error", "side-eye"),
    "wink" to q("idle-front", "wink", "soft-smile"),
    "love" to q("anticipation", "love", "soft-smile"),
    "success" to q("anticipation", "success", "confetti", "soft-smile"),
    "error" to q("focus", "error", "concern"),
    "notification" to q("idle-front", "notification", "focus"),
    "dizzy" to q("dizzy", "eye-roll", "dizzy"),
    "dance" to q("cheer", "wink", "love", "joy"),
    "kiss" to q("anticipation", "kiss", "love", "soft-smile"),
    "orbit" to q("orbit"),
    "play" to q("play")
)

private fun timingFor(anim: String, idx: Int): Pair<Int, Int> {
    val introSet = setOf("intro-neby", "intro-cinematic", "intro-pop", "intro-scan")
    val excitedSet = setOf("excited", "surprised", "laughing", "scared", "playful", "celebrate", "greeting", "agree", "disagree", "wink", "love", "success", "error", "notification", "dizzy", "dance")
    val thinkingSet = setOf("listening", "thinking", "searching", "working", "scanning", "presenting")
    val sleepySet = setOf("sleeping", "drowsy", "bored", "sad")
    return when {
        anim == "idle" -> listOf(2100 to 260, 420 to 180, 1250 to 240, 420 to 180).getOrElse(idx) { 900 to 220 }
        anim == "intro-neby" -> listOf(480 to 260, 430 to 240, 620 to 300, 780 to 340, 520 to 280).getOrElse(idx) { 520 to 260 }
        introSet.contains(anim) -> when (idx) { 0 -> 360; 1 -> 420; 2 -> 520; 3 -> 620; else -> 460 } to if (idx == 0) 220 else 250
        excitedSet.contains(anim) -> (if (idx == 0) 260 else 380) to if (idx == 0) 140 else 170
        thinkingSet.contains(anim) -> 560 to 220
        anim == "sleeping" -> 1350 to 420
        sleepySet.contains(anim) -> 620 to 250
        else -> 440 to 180
    }
}

private data class BlinkCfg(val initial: Int, val min: Int, val max: Int, val dur: Int)
private val BLINK_CFG: Map<String, BlinkCfg> = mapOf(
    "natural" to BlinkCfg(2600, 3400, 6200, 280),
    "calm" to BlinkCfg(4800, 6500, 9500, 420),
    "attentive" to BlinkCfg(3200, 4800, 7200, 240),
    "active" to BlinkCfg(2100, 2800, 5000, 260),
    "reactive" to BlinkCfg(1200, 1800, 3600, 220)
)
private fun blinkForAnim(anim: String): BlinkCfg {
    val intros = setOf("intro-neby", "intro-cinematic", "intro-pop", "intro-scan")
    val sleepy2 = setOf("sleeping", "drowsy", "bored", "sad")
    val thinking2 = setOf("listening", "thinking", "working", "searching", "scanning")
    val excited2 = setOf("speaking", "excited", "surprised", "laughing", "scared", "celebrate", "greeting", "agree", "disagree", "wink", "love", "success", "error", "notification", "dizzy", "dance")
    return when {
        anim == "idle" -> BLINK_CFG["natural"]!!
        intros.contains(anim) -> BLINK_CFG["attentive"]!!
        sleepy2.contains(anim) -> BLINK_CFG["calm"]!!
        thinking2.contains(anim) -> BLINK_CFG["attentive"]!!
        excited2.contains(anim) -> BLINK_CFG["reactive"]!!
        else -> BLINK_CFG["active"]!!
    }
}

val NEBY_ANIMATIONS: Map<String, NebyAnimation> by lazy {
    GT.mapValues { (anim, ids) ->
        val mode = if (anim.startsWith("intro-")) "once" else "loop"
        val bc = blinkForAnim(anim)
        val steps = ids.mapIndexed { idx, exprId ->
            val (hold, trans) = timingFor(anim, idx)
            val transition = if (anim.startsWith("intro-")) "spring"
            else if (setOf("excited", "surprised", "laughing", "scared", "playful", "celebrate", "greeting", "agree", "disagree", "wink", "love", "success", "error", "notification", "dizzy", "dance").contains(anim)) "snappy" else "smooth"
            val resolvedId = EXPR_BY_ID[exprId]?.id ?: EXPR_BY_ID.values.first().id
            AnimStep(resolvedId, hold, trans, transition)
        }
        NebyAnimation(anim, mode, steps, anim != "sleeping", bc.initial, bc.min, bc.max, bc.dur)
    }
}
