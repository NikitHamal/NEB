package com.neb.ians.ui.avatar.neby

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import kotlin.math.*

data class NebyFrameOut(
    val headPath: Path,
    val leftEyePath: Path, val rightEyePath: Path,
    val leftVisible: Boolean, val rightVisible: Boolean,
    val decals: List<Pair<Path, Int>>,
    val bodyOffsetX: Double, val bodyOffsetY: Double,
    val effectDraw: ((Canvas, Double) -> Unit)?
)

private const val HULL_GRID_ROWS = 17
private const val HULL_GRID_COLS = 49
private const val EYE_MAP_SCALE = 120.0
private const val DECAL_COLS = 96

class NebyRenderer(private val surface: NebySurface = NebySurface("cube", 240.0, 240.0, 215.0, 2.0, "book")) {

    private val perspectiveDefault = 1.0

    private val hullPoints: Array<Vec3> = Array(HULL_GRID_ROWS * HULL_GRID_COLS) { idx ->
        val r = idx / HULL_GRID_COLS
        val c = idx % HULL_GRID_COLS
        val phi = -PI / 2 + r / (HULL_GRID_ROWS - 1.0) * PI
        val theta = -PI + c / (HULL_GRID_COLS - 1.0) * 2 * PI
        surfacePoint(surface, theta, phi)
    }

    private val projX = DoubleArray(hullPoints.size)
    private val projY = DoubleArray(hullPoints.size)

    private val decalVLevels: List<Double> = buildList {
        add(0.4)
        val sub1 = 12
        for (i in 1..sub1) add(0.4 + (PI / 2 - 0.001 - 0.4) * i / sub1)
        add(0.45)
        add(0.5)
        add(0.33)
        add(0.365)
    }

    private val decalNodeRot = Array(decalVLevels.size) { Array<Vec3?>(DECAL_COLS + 1) { null } }
    private val decalNodeNormZ = Array(decalVLevels.size) { DoubleArray(DECAL_COLS + 1) }
    private val decalNodeProjX = Array(decalVLevels.size) { DoubleArray(DECAL_COLS + 1) }
    private val decalNodeProjY = Array(decalVLevels.size) { DoubleArray(DECAL_COLS + 1) }

    private val pathHead = Path()
    private val pathLeftEye = Path()
    private val pathRightEye = Path()
    private val pathDecalMain = Path()
    private val pathDecalMid = Path()
    private val pathDecalLight = Path()

    fun render(
        pose: NebyPose,
        blinkAmount: Double,
        timeSec: Double,
        eyeOffset: Pair<Double, Double> = 0.0 to 0.0
    ): NebyFrameOut {
        val orient = pose.orientation
        val persp = pose.expression.perspective

        buildHeadPath(orient, persp)
        val leftVis = buildEyePath(pathLeftEye, pose, blinkAmount, eyeOffset, -1, orient, persp)
        val rightVis = buildEyePath(pathRightEye, pose, blinkAmount, eyeOffset, 1, orient, persp)
        val decals = if (surface.pattern == "book") buildDecals(orient, persp) else emptyList()

        val off = bodyOffset(pose.expression, timeSec)
        return NebyFrameOut(
            headPath = pathHead,
            leftEyePath = pathLeftEye, rightEyePath = pathRightEye,
            leftVisible = leftVis, rightVisible = rightVis,
            decals = decals,
            bodyOffsetX = off.first, bodyOffsetY = off.second,
            effectDraw = effectFor(pose.expression.effect)
        )
    }

    private fun buildHeadPath(orient: Quat, persp: Double) {
        var n = 0
        for (p in hullPoints) {
            val rp = quatRotate(orient, p)
            val pr = projectPoint(rp, persp)
            projX[n] = pr.x; projY[n] = pr.y; n++
        }
        val hull = convexHullCoords(projX, projY, n)
        writeCatmullClosed(pathHead, resampleLoop(hull, 7.0))
    }

    private fun eyeOutlinePoints(w: Double, h: Double): Array<Vec3> {
        val hw = w / 2; val hh = h / 2
        val rad = min(hw, hh)
        val out = ArrayList<Vec3>(160)
        fun edge(x0: Double, y0: Double, x1: Double, y1: Double) {
            val steps = max(2, ceil(hypot(x1 - x0, y1 - y0) / 1.5).toInt())
            for (i in 0 until steps) {
                val t = i.toDouble() / steps
                out.add(Vec3(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0.0))
            }
        }
        fun arc(cx: Double, cy: Double, startAngle: Double) {
            for (i in 0 until 14) {
                val a = startAngle + i / 14.0 * (PI / 2)
                out.add(Vec3(cx + cos(a) * rad, cy + sin(a) * rad, 0.0))
            }
        }
        edge(-hw + rad, -hh, hw - rad, -hh)
        arc(hw - rad, -hh + rad, -PI / 2)
        edge(hw, -hh + rad, hw, hh - rad)
        arc(hw - rad, hh - rad, 0.0)
        edge(hw - rad, hh, -hw + rad, hh)
        arc(-hw + rad, hh - rad, PI / 2)
        edge(-hw, hh - rad, -hw, -(hh - rad))
        arc(-hw + rad, -(hh - rad), PI)
        return out.toTypedArray()
    }

    private fun buildEyePath(
        path: Path, pose: NebyPose, blink: Double, eyeOffset: Pair<Double, Double>,
        sign: Int, orient: Quat, persp: Double
    ): Boolean {
        val e = pose.expression
        val w = if (sign < 0) e.widthLeft else e.widthRight
        val hRaw = if (sign < 0) e.heightLeft else e.heightRight
        val h = 5 + (hRaw - 5) * blink.coerceIn(0.0, 1.0)
        val posX = (if (sign < 0) e.positionXLeft else e.positionXRight) + eyeOffset.first
        val posY = (if (sign < 0) e.positionYLeft else e.positionYRight) + eyeOffset.second
        val ang = deg2rad(if (sign < 0) e.leftAngle else e.rightAngle)
        val cx = sign * e.spacing / 2 + posX
        val cy = posY
        val cosA = cos(ang); val sinA = sin(ang)

        val outline = eyeOutlinePoints(max(w, 6.0), max(h, 5.0))
        path.rewind()
        var visSum = 0.0
        var first = true
        for ((idx, pt) in outline.withIndex()) {
            val rx = pt.x * cosA - pt.y * sinA
            val ry = pt.x * sinA + pt.y * cosA
            val wx = cx + rx
            val wy = cy + ry
            val theta = EYE_MAP_SCALE * cos(wy / EYE_MAP_SCALE) * sin(wx / EYE_MAP_SCALE)
            val phi = EYE_MAP_SCALE * sin(wy / EYE_MAP_SCALE)
            val sp = surfacePoint(surface, theta, phi)
            val rp = quatRotate(orient, sp)
            val pr = projectPoint(rp, persp)
            if (first) { path.moveTo(pr.x.toFloat(), pr.y.toFloat()); first = false }
            else path.lineTo(pr.x.toFloat(), pr.y.toFloat())
            if (idx % 6 == 0) {
                val nrm = surfaceNormalNumeric(surface, theta, phi)
                val rn = quatRotate(orient, nrm)
                visSum += rn.z
            }
        }
        path.close()
        return visSum > 0
    }

    private fun visibility(rotatedPoint: Vec3, rotatedNormal: Vec3, persp: Double): Double {
        val camZ = NEBY_CAM_DIST / persp
        val lx = -rotatedPoint.x; val ly = -rotatedPoint.y; val lz = camZ - rotatedPoint.z
        val len = sqrt(lx * lx + ly * ly + lz * lz).coerceAtLeast(1e-9)
        return (rotatedNormal.x * lx + rotatedNormal.y * ly + rotatedNormal.z * lz) / len - 1e-5
    }

    private fun buildDecals(orient: Quat, persp: Double): List<Pair<Path, Int>> {
        for (vi in decalVLevels.indices) {
            val v = decalVLevels[vi]
            for (ui in 0..DECAL_COLS) {
                val u = -PI + ui / DECAL_COLS.toDouble() * 2 * PI
                val p = surfacePoint(surface, u, v)
                val nrm = surfaceNormalNumeric(surface, u, v)
                val rp = quatRotate(orient, p)
                val rn = quatRotate(orient, nrm)
                decalNodeRot[vi][ui] = rp
                decalNodeNormZ[vi][ui] = visibility(rp, rn, persp)
                val pr = projectPoint(rp, persp)
                decalNodeProjX[vi][ui] = pr.x
                decalNodeProjY[vi][ui] = pr.y
            }
        }

        fun fillRegion(path: Path, vStart: Double, vEnd: Double, subDivs: Int) {
            path.rewind()
            var vi0 = -1; var vi1 = -1
            for (vi in decalVLevels.indices) {
                if (abs(decalVLevels[vi] - vStart) < 1e-9) vi0 = vi
                if (abs(decalVLevels[vi] - vEnd) < 1e-9) vi1 = vi
            }
            if (vi0 < 0 || vi1 < 0 || vi1 <= vi0) return
            val span = vi1 - vi0
            for (ui in 0 until DECAL_COLS) {
                for (s in 0 until subDivs) {
                    val rowA = vi0 + span * s / subDivs
                    val rowB = vi0 + span * (s + 1) / subDivs
                    val c0x = decalNodeProjX[rowA][ui]; val c0y = decalNodeProjY[rowA][ui]
                    val c1x = decalNodeProjX[rowB][ui]; val c1y = decalNodeProjY[rowB][ui]
                    val c2x = decalNodeProjX[rowB][ui + 1]; val c2y = decalNodeProjY[rowB][ui + 1]
                    val c3x = decalNodeProjX[rowA][ui + 1]; val c3y = decalNodeProjY[rowA][ui + 1]
                    val v0 = decalNodeNormZ[rowA][ui]; val v1 = decalNodeNormZ[rowB][ui]
                    val v2 = decalNodeNormZ[rowB][ui + 1]; val v3 = decalNodeNormZ[rowA][ui + 1]
                    if (v0 >= 0 && v1 >= 0 && v2 >= 0 && v3 >= 0) {
                        path.moveTo(c0x.toFloat(), c0y.toFloat())
                        path.lineTo(c1x.toFloat(), c1y.toFloat())
                        path.lineTo(c2x.toFloat(), c2y.toFloat())
                        path.lineTo(c3x.toFloat(), c3y.toFloat())
                        path.close()
                    } else if (v0 > -0.25 && v1 > -0.25 && v2 > -0.25 && v3 > -0.25) {
                        val xs = doubleArrayOf(c0x, c1x, c2x, c3x)
                        val ys = doubleArrayOf(c0y, c1y, c2y, c3y)
                        val vs = doubleArrayOf(v0, v1, v2, v3)
                        appendClippedPoly(path, xs, ys, vs)
                    }
                }
            }
        }

        fillRegion(pathDecalMain, 0.4, PI / 2 - 0.001, 12)
        fillRegion(pathDecalMid, 0.4, 0.5, 2)
        fillRegion(pathDecalLight, 0.33, 0.4, 2)

        return listOf(
            pathDecalMain to Color.parseColor("#1d4ed8"),
            pathDecalMid to Color.parseColor("#3b82f6"),
            pathDecalLight to Color.parseColor("#93c5fd")
        )
    }

    private fun appendClippedPoly(path: Path, xs: DoubleArray, ys: DoubleArray, vs: DoubleArray) {
        val n = 4
        var started = false
        for (i in 0 until n) {
            val j = (i + 1) % n
            val curIn = vs[i] >= 0
            val nextIn = vs[j] >= 0
            if (curIn) {
                if (!started) { path.moveTo(xs[i].toFloat(), ys[i].toFloat()); started = true }
                else path.lineTo(xs[i].toFloat(), ys[i].toFloat())
            }
            if (curIn != nextIn) {
                val t = vs[i] / (vs[i] - vs[j])
                val ix = xs[i] + (xs[j] - xs[i]) * t
                val iy = ys[i] + (ys[j] - ys[i]) * t
                if (!started) { path.moveTo(ix.toFloat(), iy.toFloat()); started = true }
                else path.lineTo(ix.toFloat(), iy.toFloat())
            }
        }
        if (started) path.close()
    }

    companion object {
        fun bodyOffset(expr: NebyExpression, t: Double): Pair<Double, Double> {
            val sig = expr.headX * 0.71 + expr.headY * 1.13 + expr.headZ * 1.37
            return when (expr.bodyMotion) {
                "slowDrift" -> Pair(valueNoise(t, 3, sig, 2.9) * 1.45, valueNoise(t, 4, sig, 3.7) * 1.1)
                "breathe" -> Pair(0.0, sin(t * 1.7) * 1.15)
                "bob" -> Pair(0.0, sin(t * 3.2) * 2.2)
                "bounce" -> Pair(sin(t * 2.4) * 0.9, -abs(sin(t * 3.6)) * 4.2)
                "sway" -> Pair(sin(t * 1.8) * 2.1, cos(t * 1.4) * 0.55)
                "float" -> Pair(valueNoise(t, 5, sig, 4.2) * 2.2, valueNoise(t, 6, sig, 5.1) * 2.5)
                "shake" -> Pair((sin(t * 31) + sin(t * 53) * 0.45) * 1.35, (sin(t * 37) + sin(t * 61) * 0.4) * 1.1)
                else -> Pair(0.0, 0.0)
            }
        }

        fun effectFor(effect: String): ((Canvas, Double) -> Unit)? = when (effect) {
            "hearts" -> { c, t -> drawHearts(c, t) }
            "sparkles", "sparkle", "introGlow" -> { c, t -> drawSparkles(c, t) }
            "confetti" -> { c, t -> drawConfetti(c, t) }
            "alert" -> { c, t -> drawAlert(c, t) }
            "successBurst" -> { c, t -> drawSuccessBurst(c, t) }
            "errorPulse" -> { c, t -> drawErrorPulse(c, t) }
            "zzz" -> { c, t -> drawTextFloat(c, t, "Z") }
            "question" -> { c, t -> drawTextFloat(c, t, "?") }
            else -> null
        }

        private val EFFECT_COLORS = intArrayOf(
            Color.parseColor("#ff4d8d"), Color.parseColor("#ffd166"), Color.parseColor("#38d9a9"),
            Color.parseColor("#5b8cff"), Color.parseColor("#a970ff"), Color.parseColor("#ff7a45")
        )

        fun drawHearts(canvas: Canvas, timeSec: Double) {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
            for (i in 0 until 7) {
                val r = (timeSec / (1.9 + i % 3 * 0.35) + i * 0.17) % 1.0
                val x = -88 + i * 29 + sin(r * 2 * PI + i) * 8
                val y = 112 - r * 238
                paint.color = if (i % 2 == 0) Color.parseColor("#ff4d8d") else Color.parseColor("#ff7aa8")
                paint.alpha = (sin(min(1.0, r) * PI) * 0.9 * 255).toInt().coerceIn(0, 255)
                canvas.drawPath(heartPath(x, y, 10.0 + i % 3 * 2), paint)
            }
        }

        fun heartPath(cx: Double, cy: Double, s: Double): Path {
            val p = Path()
            p.moveTo(cx.toFloat(), (cy + s * 0.35).toFloat())
            p.cubicTo((cx - s * 0.65).toFloat(), (cy - s * 0.45).toFloat(), (cx - s * 0.35).toFloat(), (cy - s * 1.0).toFloat(), cx.toFloat(), (cy - s * 0.35).toFloat())
            p.cubicTo((cx + s * 0.35).toFloat(), (cy - s * 1.0).toFloat(), (cx + s * 0.65).toFloat(), (cy - s * 0.45).toFloat(), cx.toFloat(), (cy + s * 0.35).toFloat())
            p.close()
            return p
        }

        fun drawSparkles(canvas: Canvas, timeSec: Double) {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
            val pts = arrayOf(doubleArrayOf(-104.0, -78.0, 10.0), doubleArrayOf(108.0, -55.0, 8.0), doubleArrayOf(-118.0, 45.0, 7.0), doubleArrayOf(112.0, 64.0, 11.0), doubleArrayOf(78.0, -112.0, 6.0))
            for ((idx, pt) in pts.withIndex()) {
                val a = 0.72 + (sin(timeSec * (4 + idx * 0.33) + idx) + 1) * 0.22
                paint.color = EFFECT_COLORS[(idx + 1) % EFFECT_COLORS.size]
                paint.alpha = ((0.45 + a * 0.45) * 255).toInt().coerceIn(0, 255)
                canvas.drawPath(starPath(pt[0], pt[1], pt[2] * a), paint)
            }
        }

        fun starPath(cx: Double, cy: Double, r: Double): Path {
            val p = Path()
            for (i in 0 until 8) {
                val ang = -PI / 2 + i / 8.0 * 2 * PI
                val rad = if (i % 2 == 0) r else r * 0.38
                val x = cx + cos(ang) * rad
                val y = cy + sin(ang) * rad
                if (i == 0) p.moveTo(x.toFloat(), y.toFloat()) else p.lineTo(x.toFloat(), y.toFloat())
            }
            p.close()
            return p
        }

        fun drawConfetti(canvas: Canvas, timeSec: Double) {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL; alpha = 240 }
            for (i in 0 until 22) {
                val x = -138 + hash01(i + 1) * 276
                val y = ((-170 + (95 + hash01(i + 31) * 85) * timeSec + hash01(i + 71) * 260 + 180) % 350) - 180
                val wob = sin(timeSec * (2.2 + hash01(i + 91) * 2.4) + i) * 10
                paint.color = EFFECT_COLORS[i % EFFECT_COLORS.size]
                canvas.save()
                canvas.rotate(((timeSec * (180 + hash01(i + 111) * 420) + i * 37) % 360).toFloat(), (x + wob).toFloat(), y.toFloat())
                canvas.drawRect((x + wob - 3).toFloat(), (y - 2).toFloat(), (x + wob + 3).toFloat(), (y + 2).toFloat(), paint)
                canvas.restore()
            }
        }

        private fun hash01(i: Int): Double {
            val t = sin(i * 12.9898 + 78.233) * 43758.5453
            return t - floor(t)
        }

        fun drawAlert(canvas: Canvas, timeSec: Double) {
            val e = (timeSec % 0.9) / 0.9
            val ring = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                style = Paint.Style.STROKE; strokeWidth = 4f
                color = Color.parseColor("#ffd166"); alpha = (0.55 * (1 - e) * 255).toInt().coerceIn(0, 255)
            }
            canvas.drawCircle(0f, 0f, (112 + e * 30).toFloat(), ring)
            val tri = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                style = Paint.Style.FILL; color = Color.parseColor("#ffd166")
                alpha = (0.55 + sin(timeSec * 8.5) * 0.35).let { (it * 255).toInt().coerceIn(0, 255) }
            }
            val p = Path().apply { moveTo(0f, -140f); lineTo(-8f, -122f); lineTo(8f, -122f); close() }
            canvas.drawPath(p, tri)
        }

        fun drawSuccessBurst(canvas: Canvas, timeSec: Double) {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.STROKE; strokeWidth = 4f; strokeCap = Paint.Cap.ROUND }
            for (i in 0 until 12) {
                val ang = i / 12.0 * 2 * PI
                val a = 0.45 + (sin(timeSec * 6.4 - i * 0.2) + 1) * 0.25
                paint.color = EFFECT_COLORS[i % EFFECT_COLORS.size]
                paint.alpha = (a * 255).toInt().coerceIn(0, 255)
                canvas.drawLine(cos(ang).toFloat() * 112, sin(ang).toFloat() * 112, cos(ang).toFloat() * 137, sin(ang).toFloat() * 137, paint)
            }
        }

        fun drawErrorPulse(canvas: Canvas, timeSec: Double) {
            val e = (timeSec % 0.56) / 0.56
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                style = Paint.Style.STROKE; strokeWidth = 4f; color = Color.parseColor("#ff5f6d")
                alpha = (0.72 * sin(e * PI) * 255).toInt().coerceIn(0, 255)
            }
            canvas.drawCircle(0f, 0f, (116 + e * 22).toFloat(), paint)
        }

        fun drawTextFloat(canvas: Canvas, timeSec: Double, glyph: String) {
            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                color = Color.parseColor("#64748b"); typeface = android.graphics.Typeface.DEFAULT_BOLD
                textAlign = Paint.Align.CENTER
            }
            for (i in 0..2) {
                paint.alpha = (0.45 + sin(timeSec * (2.2 + i * 0.2) + i) * 0.25).let { (it * 255).toInt().coerceIn(0, 255) }
                paint.textSize = (18 + i * 5).toFloat()
                canvas.drawText(glyph, 76f + i * 20, -78f - i * 22, paint)
            }
        }
    }
}

internal fun convexHullCoords(xs: DoubleArray, ys: DoubleArray, n: Int): FloatArray {
    if (n < 3) return FloatArray(0)
    val idx = Array(n) { it }
    idx.sortWith(compareBy({ xs[it] }, { ys[it] }))
    val cross = { o: Int, a: Int, b: Int -> (xs[a] - xs[o]) * (ys[b] - ys[o]) - (ys[a] - ys[o]) * (xs[b] - xs[o]) }
    val lower = IntArray(n); var lk = 0
    for (i in 0 until n) {
        while (lk >= 2 && cross(lower[lk - 2], lower[lk - 1], idx[i]) <= 0) lk--
        lower[lk++] = idx[i]
    }
    val upper = IntArray(n); var uk = 0
    for (i in n - 1 downTo 0) {
        while (uk >= 2 && cross(upper[uk - 2], upper[uk - 1], idx[i]) <= 0) uk--
        upper[uk++] = idx[i]
    }
    val count = lk + uk - 2
    if (count < 3) return FloatArray(0)
    val out = FloatArray(count * 2)
    var w = 0
    for (i in 0 until lk - 1) { out[w++] = xs[lower[i]].toFloat(); out[w++] = ys[lower[i]].toFloat() }
    for (i in 0 until uk - 1) { out[w++] = xs[upper[i]].toFloat(); out[w++] = ys[upper[i]].toFloat() }
    return out
}

internal fun resampleLoop(hull: FloatArray, step: Double): FloatArray {
    val m = hull.size / 2
    if (m < 3) return FloatArray(0)
    val out = ArrayList<Float>(hull.size * 2)
    for (i in 0 until m) {
        val j = (i + 1) % m
        val ax = hull[i * 2]; val ay = hull[i * 2 + 1]
        val bx = hull[j * 2]; val by = hull[j * 2 + 1]
        val dx = bx - ax; val dy = by - ay
        val dist = sqrt(dx * dx + dy * dy)
        val steps = max(1, ceil(dist / step).toInt())
        for (s in 0 until steps) {
            val t = s.toDouble() / steps
            out.add((ax + dx * t).toFloat()); out.add((ay + dy * t).toFloat())
        }
    }
    val arr = FloatArray(out.size)
    out.forEachIndexed { i, v -> arr[i] = v }
    return arr
}

internal fun writeCatmullClosed(path: Path, pts: FloatArray) {
    val n = pts.size / 2
    path.rewind()
    if (n < 3) return
    fun px(i: Int) = pts[((i % n) + n) % n * 2].toDouble()
    fun py(i: Int) = pts[((i % n) + n) % n * 2 + 1].toDouble()
    path.moveTo(px(0).toFloat(), py(0).toFloat())
    for (i in 0 until n) {
        val x0 = px(i - 1); val y0 = py(i - 1)
        val x1 = px(i); val y1 = py(i)
        val x2 = px(i + 1); val y2 = py(i + 1)
        val x3 = px(i + 2); val y3 = py(i + 2)
        path.cubicTo(
            (x1 + (x2 - x0) / 6).toFloat(), (y1 + (y2 - y0) / 6).toFloat(),
            (x2 - (x3 - x1) / 6).toFloat(), (y2 - (y3 - y1) / 6).toFloat(),
            x2.toFloat(), y2.toFloat()
        )
    }
    path.close()
}
