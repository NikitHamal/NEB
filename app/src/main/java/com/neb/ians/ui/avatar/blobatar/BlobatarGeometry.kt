package com.neb.ians.ui.avatar.blobatar

import android.graphics.Path
import kotlin.math.*

fun superellipsePath(cx: Double, cy: Double, rx: Double, ry: Double, n: Double = 4.0, rot: Double = 0.0): Path {
    val k = min(1.0, (8 * 2.0.pow(-1.0 / n) - 4) / 3.0)
    val a = rx; val b = ry
    val ak = a * k; val bk = b * k
    val pts = arrayOf(
        doubleArrayOf(a, 0.0), doubleArrayOf(a, bk), doubleArrayOf(ak, b), doubleArrayOf(0.0, b),
        doubleArrayOf(-ak, b), doubleArrayOf(-a, bk), doubleArrayOf(-a, 0.0),
        doubleArrayOf(-a, -bk), doubleArrayOf(-ak, -b), doubleArrayOf(0.0, -b),
        doubleArrayOf(ak, -b), doubleArrayOf(a, -bk), doubleArrayOf(a, 0.0)
    )
    val t = rot * PI / 180.0
    val cosR = cos(t); val sinR = sin(t)
    fun at(i: Int): Pair<Float, Float> {
        val x = pts[i][0]; val y = pts[i][1]
        return Pair((cx + x * cosR - y * sinR).toFloat(), (cy + x * sinR + y * cosR).toFloat())
    }
    val p = Path()
    val s0 = at(0); p.moveTo(s0.first, s0.second)
    var i = 1
    while (i < 13) {
        val c1 = at(i); val c2 = at(i + 1); val e = at(i + 2)
        p.cubicTo(c1.first, c1.second, c2.first, c2.second, e.first, e.second)
        i += 3
    }
    p.close()
    return p
}

fun blobPathDef(cx: Double, cy: Double, rx: Double, ry: Double, radii: List<Double>, rot: Double = 0.0): Path {
    val n = radii.size
    val t0 = rot * PI / 180.0
    val pts = Array(n) { i ->
        val m = radii[i]
        val a = t0 + 2 * PI * i / n
        doubleArrayOf(cx + rx * m * cos(a), cy + ry * m * sin(a))
    }
    fun at(i: Int): DoubleArray = pts[(i % n + n) % n]
    val p = Path()
    p.moveTo(at(0)[0].toFloat(), at(0)[1].toFloat())
    for (idx in 0 until n) {
        val x0 = at(idx - 1)[0]; val y0 = at(idx - 1)[1]
        val x1 = at(idx)[0]; val y1 = at(idx)[1]
        val x2 = at(idx + 1)[0]; val y2 = at(idx + 1)[1]
        val x3 = at(idx + 2)[0]; val y3 = at(idx + 2)[1]
        p.cubicTo(
            (x1 + (x2 - x0) / 6).toFloat(), (y1 + (y2 - y0) / 6).toFloat(),
            (x2 - (x3 - x1) / 6).toFloat(), (y2 - (y3 - y1) / 6).toFloat(),
            x2.toFloat(), y2.toFloat()
        )
    }
    p.close()
    return p
}

fun polygonPath(cx: Double, cy: Double, rx: Double, ry: Double, sides: Int, roundFrac: Double = 0.3, rot: Double = 0.0): Path {
    val k = when { roundFrac <= 0 -> 0.0; roundFrac >= 1 -> 0.5; else -> roundFrac / 2 }
    val t0 = rot * PI / 180.0 - PI / 2
    val v = Array(sides) { i ->
        val a = t0 + 2 * PI * i / sides
        doubleArrayOf(cx + rx * cos(a), cy + ry * sin(a))
    }
    fun at(i: Int): DoubleArray = v[(i % sides + sides) % sides]
    fun cut(i: Int, j: Int): Pair<Float, Float> {
        val x0 = at(i)[0]; val y0 = at(i)[1]
        val x1 = at(j)[0]; val y1 = at(j)[1]
        return Pair((x0 + (x1 - x0) * k).toFloat(), (y0 + (y1 - y0) * k).toFloat())
    }
    val p = Path()
    val start = cut(0, sides - 1); p.moveTo(start.first, start.second)
    for (i in 0 until sides) {
        val x = at(i)[0].toFloat(); val y = at(i)[1].toFloat()
        val c = cut(i, (i + 1) % sides)
        p.quadTo(x, y, c.first, c.second)
        if (k < 0.5) {
            val e2 = cut(i + 1, i)
            p.lineTo(e2.first, e2.second)
        }
    }
    p.close()
    return p
}

fun boxPath(cx: Double, cy: Double, rx: Double, ry: Double): Path {
    val p = Path()
    p.moveTo((cx - rx).toFloat(), (cy - ry).toFloat())
    p.lineTo((cx + rx).toFloat(), (cy - ry).toFloat())
    p.lineTo((cx + rx).toFloat(), (cy + ry).toFloat())
    p.lineTo((cx - rx).toFloat(), (cy + ry).toFloat())
    p.close()
    return p
}

fun taperPath(cx: Double, cy: Double, rx: Double, ry: Double, tip: Double): Path {
    val t = max(1.05, tip)
    val tx = rx * sqrt(1 - 1 / (t * t))
    val ty = cy - ry / t
    val apex = cy - t * ry
    val px = tx * 0.14
    val py = ty + 0.86 * (apex - ty)
    val p = Path()
    p.moveTo((cx - tx).toFloat(), ty.toFloat())
    p.lineTo((cx - px).toFloat(), py.toFloat())
    p.quadTo(cx.toFloat(), apex.toFloat(), (cx + px).toFloat(), py.toFloat())
    p.lineTo((cx + tx).toFloat(), ty.toFloat())
    p.close()
    return p
}
