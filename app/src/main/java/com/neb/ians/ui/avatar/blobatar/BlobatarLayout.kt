package com.neb.ians.ui.avatar.blobatar

import android.graphics.Path
import kotlin.math.*

data class MutableBody(
    var cx: Double, var cy: Double, var rx: Double, var ry: Double,
    var n: Double, var rot: Double,
    var radii: MutableList<Double> = mutableListOf(),
    var sides: Int = 6,
    var round: Double = 0.3
)

data class Petal(var cx: Double, var cy: Double, var r: Double)

data class EyeDef(var cx: Double, var cy: Double, var rx: Double, var ry: Double, var n: Double, var rot: Double)

data class BlobLayout(
    val shape: String,
    val draw: ((MutableBody) -> Path)?,
    val body: MutableBody,
    val face: MutableBody,
    val petals: List<Petal>,
    val extra: List<Path>,
    val eyes: List<EyeDef>
)

private fun shrunk(k: Double): (MutableBody) -> MutableBody = { b ->
    MutableBody(b.cx, b.cy, b.rx * k, b.ry * k, b.n, b.rot, b.radii.toMutableList(), b.sides, b.round)
}

private val faceShrunk095: (MutableBody) -> MutableBody = { b ->
    val k = (b.radii.minOrNull() ?: 1.0) * 0.95
    shrunk(k)(b)
}
private val faceShrunk084: (MutableBody) -> MutableBody = shrunk(0.84)
private val faceShrunk094: (MutableBody) -> MutableBody = shrunk(0.94)

data class ShapeDef(
    val name: String,
    val core: Double,
    val body: ((Traits, MutableBody) -> Unit)? = null,
    val face: ((MutableBody) -> MutableBody)? = null,
    val decorate: ((Traits, MutableBody, MutableList<Petal>, MutableList<Path>) -> Unit)? = null,
    val path: ((MutableBody) -> Path)? = null
)

private val SHAPE_ROUND = ShapeDef("round", 1.0)

private val SHAPE_ORGANIC = ShapeDef("organic", 0.98,
    path = { b -> blobPathDef(b.cx, b.cy, b.rx, b.ry, b.radii, b.rot) },
    face = faceShrunk095
)

private val SHAPE_BOXY = ShapeDef("boxy", 0.86,
    body = { t, b ->
        b.n = t.num("body.n", 3.4, 6.0)
        b.rot = t.num("body.rot", -20.0, 20.0)
    }
)

private val SHAPE_CAPSULE = ShapeDef("capsule", 1.02,
    body = { t, b -> b.ry = b.ry * t.num("capsule.squat", 0.55, 0.68) },
    face = faceShrunk094,
    decorate = { _, b, petals, _ ->
        petals.add(Petal(b.cx - (b.rx - b.ry), b.cy, b.ry))
        petals.add(Petal(b.cx + (b.rx - b.ry), b.cy, b.ry))
    },
    path = { b -> boxPath(b.cx, b.cy, b.rx - b.ry, b.ry) }
)

private val SHAPE_NUB = ShapeDef("nub", 0.88,
    decorate = { t, b, petals, _ ->
        val n = t.int("nub.n", 1, 2)
        for (i in 0 until n) {
            petals.add(Petal(
                b.cx + cos(t.num("nub.a$i", 0.0, 2 * PI)) * b.rx * 0.88,
                b.cy + sin(t.num("nub.a$i", 0.0, 2 * PI)) * b.rx * 0.88,
                b.rx * t.num("nub.r$i", 0.24, 0.4)
            ))
        }
    }
)

private val SHAPE_CLOUD = ShapeDef("cloud", 0.78,
    path = { b -> blobPathDef(b.cx, b.cy, b.rx, b.ry, b.radii, b.rot) },
    face = faceShrunk095,
    decorate = { t, b, petals, _ ->
        val count = t.int("cloud.n", 4, 6)
        for (i in 0 until count) {
            val a = PI + PI * (i + 0.5) / count
            petals.add(Petal(
                b.cx + cos(a) * b.rx * 0.8,
                b.cy + sin(a) * b.rx * 0.5,
                b.rx * t.num("cloud.r$i", 0.44, 0.62)
            ))
        }
    }
)

private val SHAPE_DROPLET = ShapeDef("droplet", 0.78,
    body = { t, b ->
        b.cy += 0.22 * b.ry
        b.n = 2.0
        b.radii.clear()
    },
    face = { b -> MutableBody(b.cx, b.cy + b.ry * 0.05, b.rx * 0.88, b.ry * 0.88, b.n, b.rot, b.radii, b.sides, b.round) },
    decorate = { t, b, _, extra ->
        extra.add(taperPath(b.cx, b.cy, b.rx, b.ry, t.num("droplet.tip", 1.4, 1.65)))
    }
)

private val SHAPE_HEXAGON = ShapeDef("hexagon", 1.05,
    path = { b -> polygonPath(b.cx, b.cy, b.rx, b.ry, b.sides, b.round, b.rot) },
    face = faceShrunk084,
    body = { t, b ->
        b.sides = 6
        b.rot = t.num("body.rot", -12.0, 12.0)
        b.round = t.num("poly.round", 0.24, 0.5)
    }
)

private val SHAPE_SUN = ShapeDef("sun", 0.7,
    decorate = { t, b, petals, _ ->
        val count = t.int("sun.n", 6, 9)
        val dist = b.rx * t.num("sun.dist", 1.0, 1.08)
        val pr = b.rx * t.num("sun.r", 0.2, 0.26)
        val off = t.num("sun.rot", 0.0, 2 * PI)
        for (i in 0 until count) {
            val a = off + 2 * PI * i / count
            petals.add(Petal(b.cx + cos(a) * dist, b.cy + sin(a) * dist, pr))
        }
    }
)

private val SHAPE_TRIANGLE = ShapeDef("triangle", 1.15,
    path = { b -> polygonPath(b.cx, b.cy, b.rx, b.ry, b.sides, b.round, b.rot) },
    body = { t, b ->
        b.sides = 3
        b.rot = t.num("body.rot", -5.0, 5.0)
        b.round = t.num("poly.round", 0.24, 0.5)
    },
    face = { b -> MutableBody(b.cx, b.cy + b.ry * 0.1, b.rx * 0.54, b.ry * 0.36, b.n, b.rot, b.radii, b.sides, b.round) }
)

private val BANDS: List<Pair<ShapeDef, Double>> = listOf(
    SHAPE_ROUND to 0.22, SHAPE_ORGANIC to 0.48, SHAPE_BOXY to 0.6, SHAPE_CAPSULE to 0.7,
    SHAPE_NUB to 0.79, SHAPE_CLOUD to 0.86, SHAPE_DROPLET to 0.915, SHAPE_HEXAGON to 0.95,
    SHAPE_SUN to 0.98, SHAPE_TRIANGLE to 1.0
)

fun pickShape(v: Double): ShapeDef {
    for ((shape, up) in BANDS) if (v < up) return shape
    return BANDS.last().first
}

fun faceFit(t: Traits, b: MutableBody, face: MutableBody): List<EyeDef> {
    val rx = b.rx
    val er0 = t.num("eye.rx", 0.075, 0.105) * rx
    val ratio = t.num("eye.ratio", 1.9, 3.2)
    val scale = t.num("eye.scale", 0.78, 1.24)
    val stretch = t.num("eye.stretch", 0.85, 1.18)
    val clearance = t.num("eye.gap", 0.1, 0.24) * rx
    val wide = er0 * max(1.0, scale)
    val tall = er0 * ratio * max(1.0, scale * stretch)
    val gap0 = wide + rx * 0.03 + clearance
    val gx = t.jitter("gaze.x", 0.09) * face.rx
    val gy = t.num("gaze.y", -0.2, 0.08) * face.ry
    val dy = t.jitter("eye.dy", 0.04) * face.ry
    val reach = hypot(wide, tall)
    val need = hypot((abs(gx) + gap0 + reach) / face.rx, (abs(gy) + abs(dy) + reach) / face.ry)
    val fit = if (need > 0.9) 0.9 / need else 1.0
    val er = er0 * fit
    val eyeRy = er * ratio
    val gap = gap0 * fit
    val room = max(0.0, min(1.0, clearance / tall))
    val bound = min(12.0, asin(room) * 180.0 / PI)
    val lean = t.num("eye.lean", -1.0, 1.0) * bound
    val lean2 = max(-12.0, min(12.0, lean + t.jitter("eye.lean2", 3.5)))
    val cx = face.cx + gx * fit
    val cy = face.cy + gy * fit
    val n = t.num("eye.n", 3.5, 6.0)
    return listOf(
        EyeDef(cx - gap, cy, er, eyeRy, n, lean),
        EyeDef(cx + gap, cy + dy * fit, er * scale, eyeRy * scale * stretch, n, lean2)
    )
}

fun blobLayout(t: Traits): BlobLayout {
    val shape = pickShape(t("shape"))
    val r = t.num("body.r", 31.0, 38.0) * shape.core
    val body = MutableBody(
        cx = 50 + t.jitter("body.x", 1.5),
        cy = 50 + t.jitter("body.y", 1.5),
        rx = r, ry = r * t.num("body.ratio", 0.92, 1.08),
        n = t.num("body.n", 1.9, 2.5), rot = 0.0,
        radii = MutableList(t.int("body.pts", 6, 8)) { i -> 1 + t.jitter("body.r$i", 0.16) }
    )
    shape.body?.invoke(t, body)
    val face = shape.face?.invoke(body) ?: body.copy()
    val petals = mutableListOf<Petal>()
    val extra = mutableListOf<Path>()
    shape.decorate?.invoke(t, body, petals, extra)
    val eyes = faceFit(t, body, face)
    return BlobLayout(shape.name, shape.path, body, face, petals, extra, eyes)
}
