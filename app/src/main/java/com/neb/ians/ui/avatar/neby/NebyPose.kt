package com.neb.ians.ui.avatar.neby

import kotlin.math.*

data class NebyPose(val expression: NebyExpression, val orientation: Quat)

fun poseFromExpression(expr: NebyExpression): NebyPose =
    NebyPose(expr, quatFromEuler(deg2rad(expr.headX), deg2rad(expr.headY), deg2rad(expr.headZ)))

fun nearestAngle(target: Double, current: Double): Double {
    var r = target
    while (r - current > 180) r -= 360
    while (r - current < -180) r += 360
    return r
}

fun lerpExpression(from: NebyExpression, to: NebyExpression, t: Double): NebyExpression {
    fun l(a: Double, b: Double) = a + (b - a) * t
    fun la(a: Double, b: Double) = a + (nearestAngle(b, a) - a) * t
    return from.copy(
        headX = la(from.headX, to.headX),
        headY = la(from.headY, to.headY),
        headZ = la(from.headZ, to.headZ),
        widthLeft = l(from.widthLeft, to.widthLeft),
        widthRight = l(from.widthRight, to.widthRight),
        heightLeft = l(from.heightLeft, to.heightLeft),
        heightRight = l(from.heightRight, to.heightRight),
        spacing = l(from.spacing, to.spacing),
        positionXLeft = l(from.positionXLeft, to.positionXLeft),
        positionXRight = l(from.positionXRight, to.positionXRight),
        positionYLeft = l(from.positionYLeft, to.positionYLeft),
        positionYRight = l(from.positionYRight, to.positionYRight),
        leftAngle = la(from.leftAngle, to.leftAngle),
        rightAngle = la(from.rightAngle, to.rightAngle),
        perspective = l(from.perspective, to.perspective)
    )
}

private const val EYE_SIG = 17.29

fun applyAmbient(expr: NebyExpression, timeSec: Double, strength: Double = 1.0): Pair<NebyExpression, Pair<Double, Double>> {
    var e = expr
    val sig = expr.headX * 0.71 + expr.headY * 1.13 + expr.headZ * 1.37
    val tm = timeSec * 1000.0
    when (expr.bodyMotion) {
        "slowDrift" -> e = e.copy(
            headX = e.headX + valueNoise(tm, 0, sig, 2600.0) * 0.8 * strength,
            headY = e.headY + valueNoise(tm, 1, sig, 3300.0) * 1.15 * strength,
            headZ = e.headZ + valueNoise(tm, 2, sig, 4100.0) * 0.45 * strength
        )
        "breathe" -> e = e.copy(headX = e.headX + sin(timeSec * 1.7) * 0.45 * strength)
        "bob" -> e = e.copy(headX = e.headX + sin(timeSec * 3.2) * 1.4 * strength)
        "bounce" -> e = e.copy(headZ = e.headZ + sin(timeSec * 3.6) * 2.2 * strength)
        "sway" -> e = e.copy(
            headZ = e.headZ + sin(timeSec * 1.8) * 3.4 * strength,
            headY = e.headY + sin(timeSec * 0.9) * 1.2 * strength
        )
        "float" -> e = e.copy(
            headX = e.headX + valueNoise(tm, 7, sig, 4200.0) * 1.25 * strength,
            headY = e.headY + valueNoise(tm, 8, sig, 5100.0) * 1.8 * strength,
            headZ = e.headZ + valueNoise(tm, 9, sig, 4700.0) * 0.9 * strength
        )
        "shake" -> e = e.copy(
            headX = e.headX + (sin(timeSec * 31) + sin(timeSec * 53) * 0.45) * 1.15 * strength,
            headY = e.headY + (sin(timeSec * 37) + sin(timeSec * 61) * 0.4) * 1.35 * strength,
            headZ = e.headZ + sin(timeSec * 43) * 0.7 * strength
        )
    }

    var wMod = 1.0; var hMod = 1.0
    when (expr.eyeMotion) {
        "focusPulse" -> { val s = sin(timeSec * 4.8); wMod = 1 + s * 0.025; hMod = 1 - s * 0.055 }
        "squintPulse" -> { val s = (sin(timeSec * 2.6) + 1) * 0.5; wMod = 1 + s * 0.04; hMod = 0.82 + s * 0.18 }
        "sparkle" -> {
            val s = (sin(timeSec * 5.4) + 1) * 0.5
            wMod = 0.98 + s * 0.08; hMod = 0.96 + s * 0.12
            e = e.copy(
                leftAngle = e.leftAngle + sin(timeSec * 3.1) * 1.6 * strength,
                rightAngle = e.rightAngle - sin(timeSec * 3.1) * 1.6 * strength
            )
        }
        "anticipate" -> { val s = (1 - cos(timeSec * 3.2)) * 0.5; wMod = 1 + s * 0.1; hMod = 1 + s * 0.16 }
        "orbit" -> e = e.copy(
            leftAngle = e.leftAngle + sin(timeSec * 2.15) * 3 * strength,
            rightAngle = e.rightAngle - sin(timeSec * 2.15) * 3 * strength
        )
    }
    if (wMod != 1.0 || hMod != 1.0) {
        e = e.copy(
            widthLeft = max(5.0, e.widthLeft * (1 + (wMod - 1) * strength)),
            widthRight = max(5.0, e.widthRight * (1 + (wMod - 1) * strength)),
            heightLeft = max(5.0, e.heightLeft * (1 + (hMod - 1) * strength)),
            heightRight = max(5.0, e.heightRight * (1 + (hMod - 1) * strength))
        )
    }

    val off = when (expr.eyeMotion) {
        "microSaccades" -> Pair(saccadeNoise(tm, 0, EYE_SIG) * 1.5 * strength, saccadeNoise(tm, 1, EYE_SIG) * 0.9 * strength)
        "wander" -> Pair(valueNoise(tm, 9, EYE_SIG, 2100.0) * 3.2 * strength, valueNoise(tm, 10, EYE_SIG, 2700.0) * 1.8 * strength)
        "lookAround" -> Pair(sin(timeSec * 1.8) * 4.2 * strength, sin(timeSec * 0.9 + 0.7) * 1.4 * strength)
        "focusPulse" -> Pair(sin(timeSec * 5.2) * 0.35 * strength, cos(timeSec * 4.8) * 0.25 * strength)
        "shake" -> Pair((sin(timeSec * 47) + sin(timeSec * 71) * 0.45) * 1.2 * strength, (sin(timeSec * 59) + sin(timeSec * 83) * 0.4) * 0.8 * strength)
        "dart" -> Pair(tanh(sin(timeSec * 3.8) * 4.2) * 5.6 * strength, sin(timeSec * 1.9 + 0.8) * 1.15 * strength)
        "orbit" -> Pair(sin(timeSec * 2.15) * 5.1 * strength, -cos(timeSec * 2.15) * 3.2 * strength)
        "squintPulse" -> Pair(sin(timeSec * 2.1) * 0.45 * strength, cos(timeSec * 1.7) * 0.3 * strength)
        "sparkle" -> Pair((sin(timeSec * 4.7) + sin(timeSec * 11.3) * 0.3) * 0.75 * strength, (cos(timeSec * 5.1) + sin(timeSec * 9.4) * 0.25) * 0.5 * strength)
        "anticipate" -> Pair(sin(timeSec * 1.6) * 0.55 * strength, -((1 - cos(timeSec * 3.2)) * 0.5) * 1.1 * strength)
        else -> Pair(0.0, 0.0)
    }
    return e to off
}

private fun saccadeNoise(tMs: Double, salt: Int, sig: Double): Double {
    if (tMs <= 0) return 0.0
    val period = 1100.0
    val i = floor(tMs / period).toInt()
    val a = (tMs - i * period) / 140.0
    val s = smoothStep01(min(a, 1.0))
    val g1 = if (i == 0) 0.0 else hashNoise((i - 1) * 2 + salt + sig)
    val g2 = hashNoise(i * 2 + salt + sig)
    return g1 + (g2 - g1) * s
}
