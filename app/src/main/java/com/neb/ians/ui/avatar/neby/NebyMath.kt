package com.neb.ians.ui.avatar.neby

import kotlin.math.*

data class Vec3(val x: Double, val y: Double, val z: Double)
data class Quat(val x: Double, val y: Double, val z: Double, val w: Double)

fun deg2rad(d: Double) = d * PI / 180.0

fun quatNormalize(q: Quat): Quat {
    val n = sqrt(q.x * q.x + q.y * q.y + q.z * q.z + q.w * q.w)
    return if (n < 1e-12) Quat(0.0, 0.0, 0.0, 1.0) else Quat(q.x / n, q.y / n, q.z / n, q.w / n)
}

fun quatMul(a: Quat, b: Quat): Quat = quatNormalize(Quat(
    a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
    a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
    a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w,
    a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z
))

private fun quatFromAxis(axis: Vec3, angle: Double): Quat {
    val h = angle / 2; val s = sin(h)
    return quatNormalize(Quat(axis.x * s, axis.y * s, axis.z * s, cos(h)))
}

fun quatRotate(q: Quat, v: Vec3): Vec3 {
    val qx = q.x; val qy = q.y; val qz = q.z; val qw = q.w
    val tx = 2.0 * (qy * v.z - qz * v.y)
    val ty = 2.0 * (qz * v.x - qx * v.z)
    val tz = 2.0 * (qx * v.y - qy * v.x)
    return Vec3(v.x + qw * tx + (qy * tz - qz * ty), v.y + qw * ty + (qz * tx - qx * tz), v.z + qw * tz + (qx * ty - qy * tx))
}

fun quatFromEuler(rx: Double, ry: Double, rz: Double): Quat {
    val qx = quatFromAxis(Vec3(1.0, 0.0, 0.0), rx)
    val qy = quatFromAxis(Vec3(0.0, 1.0, 0.0), ry)
    val qz = quatFromAxis(Vec3(0.0, 0.0, 1.0), rz)
    return quatMul(quatMul(qz, qx), qy)
}

fun vecNorm(v: Vec3): Vec3 {
    val l = sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
    return if (l < 1e-12) Vec3(0.0, 0.0, 0.0) else Vec3(v.x / l, v.y / l, v.z / l)
}

const val NEBY_CAM_DIST = 620.0

fun projectPoint(p: Vec3, perspective: Double): Vec3 {
    val denom = NEBY_CAM_DIST - p.z * perspective
    val s = if (abs(denom) < 1e-4) NEBY_CAM_DIST / 1e-4 else NEBY_CAM_DIST / denom
    return Vec3(p.x * s, p.y * s, p.z)
}

data class NebySurface(
    val type: String,
    val width: Double, val height: Double, val depth: Double,
    val roundness: Double = 0.0,
    val pattern: String? = null
)

private fun clampRoundness(v: Double) = v.coerceIn(0.0, 2.0)

private fun diamondExp(surface: NebySurface) = 1 + clampRoundness(surface.roundness) / 2

private fun cubeExp(surface: NebySurface): Double =
    if (surface.roundness <= 0) Double.POSITIVE_INFINITY
    else 2.0 / (0.04 + clampRoundness(surface.roundness) / 2 * 0.96)

private fun signedPow(v: Double, p: Double) = sign(v) * abs(v).pow(p)

private fun axisSuperellipsoid(
    theta: Double, phi: Double,
    w: Double, h: Double, d: Double,
    powPhi: Double, powTheta: Double
): Vec3 {
    val c = signedPow(cos(phi), powPhi)
    return Vec3(
        w / 2 * c * signedPow(sin(theta), powTheta),
        h / 2 * signedPow(sin(phi), powPhi),
        d / 2 * c * signedPow(cos(theta), powTheta)
    )
}

private fun lpNormalized(surface: NebySurface, theta: Double, phi: Double, exp: Double): Vec3 {
    val dx = cos(phi) * sin(theta)
    val dy = sin(phi)
    val dz = cos(phi) * cos(theta)
    val norm: Double = if (exp.isFinite()) {
        val s = abs(dx).pow(exp) + abs(dy).pow(exp) + abs(dz).pow(exp)
        val r = s.pow(1.0 / exp)
        if (r == 0.0) 1.0 else r
    } else {
        val m = max(abs(dx), max(abs(dy), abs(dz)))
        if (m == 0.0) 1.0 else m
    }
    return Vec3(surface.width / 2 * (dx / norm), surface.height / 2 * (dy / norm), surface.depth / 2 * (dz / norm))
}

fun surfacePoint(surface: NebySurface, theta: Double, phi: Double): Vec3 {
    return when (surface.type) {
        "sphere", "mickey" -> axisSuperellipsoid(theta, phi, surface.width, surface.height, surface.depth, 1.0, 1.0)
        "disc" -> axisSuperellipsoid(theta, phi, surface.width, surface.height, surface.depth, 0.9, 0.9)
        "hexagon" -> axisSuperellipsoid(theta, phi, surface.width, surface.height, surface.depth, 0.72, 0.72)
        "pebble" -> {
            val p = axisSuperellipsoid(theta, phi, surface.width, surface.height, surface.depth,
                0.82 + clampRoundness(surface.roundness) * 0.18, 0.82 + clampRoundness(surface.roundness) * 0.2)
            val l = 1 + 0.035 * cos(3 * theta) * cos(phi)
            Vec3(p.x * l, p.y, p.z * l)
        }
        "cube" -> lpNormalized(surface, theta, phi, cubeExp(surface))
        "diamond" -> lpNormalized(surface, theta, phi, diamondExp(surface))
        "gem" -> lpNormalized(surface, theta, phi, 1.2)
        "book" -> Vec3(
            surface.width / 2 * sin(theta),
            surface.height / 2 * sin(phi),
            surface.depth / 2 * cos(phi) * cos(theta) + surface.depth / 2 * abs(sin(theta)) * 0.28
        )
        else -> lpNormalized(surface, theta, phi, cubeExp(surface))
    }
}

fun surfaceNormalNumeric(surface: NebySurface, theta: Double, phi: Double): Vec3 {
    val eps = 5e-4
    val a = surfacePoint(surface, theta - eps, phi)
    val b = surfacePoint(surface, theta + eps, phi)
    val c = surfacePoint(surface, theta, max(-PI / 2, phi - eps))
    val d = surfacePoint(surface, theta, min(PI / 2, phi + eps))
    val du = Vec3(b.x - a.x, b.y - a.y, b.z - a.z)
    val dv = Vec3(d.x - c.x, d.y - c.y, d.z - c.z)
    val cx = du.y * dv.z - du.z * dv.y
    val cy = du.z * dv.x - du.x * dv.z
    val cz = du.x * dv.y - du.y * dv.x
    return vecNorm(Vec3(cx, cy, cz))
}

fun hashNoise(seed: Double): Double {
    val t = sin(seed * 127.1 + 311.7) * 43758.5453
    return (t - floor(t)) * 2 - 1
}

fun smoothStep01(t: Double): Double = t * t * (3 - 2 * t)

fun valueNoise(t: Double, salt: Int, signature: Double, period: Double): Double {
    val i = t / period
    val a = floor(i)
    val f = smoothStep01(i - a)
    val g1 = hashNoise(a * 3 + salt + signature)
    val g2 = hashNoise((a + 1) * 3 + salt + signature)
    return g1 + (g2 - g1) * f
}
