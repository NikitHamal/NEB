package com.neb.ians.ui.sim.gl

import android.opengl.Matrix
import kotlin.math.cos
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sin
import kotlin.math.sqrt

/** Surface look: sRGB base colour, roughness, metalness, an optional glow and transparency. */
class GlMaterial(
    color: Int,
    var roughness: Float = 0.5f,
    var metalness: Float = 0f,
    var emissive: Float = 0f,
    var alpha: Float = 1f,
    var unlit: Boolean = false
) {
    val rgb = FloatArray(3)
    init { setColor(color) }
    fun setColor(c: Int) {
        rgb[0] = toLinear(((c shr 16) and 0xFF) / 255f)
        rgb[1] = toLinear(((c shr 8) and 0xFF) / 255f)
        rgb[2] = toLinear((c and 0xFF) / 255f)
    }
    private fun toLinear(v: Float) = if (v <= 0.04045f) v / 12.92f else Math.pow(((v + 0.055f) / 1.055f).toDouble(), 2.4).toFloat()
}

/**
 * A node in the scene: an optional mesh and material, a transform (position, Euler rotation in
 * radians applied Y then X then Z, scale) and children. World matrices are recomputed each frame;
 * scenes here have a few hundred nodes at most.
 */
class GlNode(var mesh: GlMesh? = null, var material: GlMaterial? = null) {
    val position = floatArrayOf(0f, 0f, 0f)
    val rotation = floatArrayOf(0f, 0f, 0f)
    val scale = floatArrayOf(1f, 1f, 1f)
    var visible = true
    /** A soft contact shadow of this radius on the ground under the node (0 = none). */
    var blobShadow = 0f
    val children = ArrayList<GlNode>()
    internal val world = FloatArray(16)
    var pickRadius = 0f
    var tag: Any? = null

    fun add(child: GlNode): GlNode { children.add(child); return child }
    fun at(x: Float, y: Float, z: Float): GlNode { position[0] = x; position[1] = y; position[2] = z; return this }
    fun scaled(x: Float, y: Float = x, z: Float = x): GlNode { scale[0] = x; scale[1] = y; scale[2] = z; return this }
    fun rotated(x: Float, y: Float, z: Float): GlNode { rotation[0] = x; rotation[1] = y; rotation[2] = z; return this }

    internal fun update(parent: FloatArray?) {
        val local = TMP
        Matrix.setIdentityM(local, 0)
        Matrix.translateM(local, 0, position[0], position[1], position[2])
        if (rotation[1] != 0f) Matrix.rotateM(local, 0, Math.toDegrees(rotation[1].toDouble()).toFloat(), 0f, 1f, 0f)
        if (rotation[0] != 0f) Matrix.rotateM(local, 0, Math.toDegrees(rotation[0].toDouble()).toFloat(), 1f, 0f, 0f)
        if (rotation[2] != 0f) Matrix.rotateM(local, 0, Math.toDegrees(rotation[2].toDouble()).toFloat(), 0f, 0f, 1f)
        Matrix.scaleM(local, 0, scale[0], scale[1], scale[2])
        if (parent == null) System.arraycopy(local, 0, world, 0, 16) else Matrix.multiplyMM(world, 0, parent, 0, local, 0)
        for (c in children) c.update(world)
    }

    /** This node's world-space origin. */
    fun worldPosition(out: FloatArray = FloatArray(3)): FloatArray { out[0] = world[12]; out[1] = world[13]; out[2] = world[14]; return out }

    companion object { private val TMP = FloatArray(16) }
}

/** The scene root, the studio backdrop and ground, and the orbit camera. */
class GlScene {
    val root = GlNode()
    val camera = OrbitCamera()
    var skyTop = 0xDCE6F2
    var skyBottom = 0xF6F7FA
    var groundY = 0f
    var groundColor = 0xE9ECF1
    var showGround = true
    var exposure = 1.05f
    /** Direction toward the key light (normalised in the renderer). */
    val keyDir = floatArrayOf(0.45f, 0.8f, 0.4f)
    var keyIntensity = 2.6f

    fun add(node: GlNode): GlNode = root.add(node)
}

/** An orbiting camera with gentle inertia: theta around y, phi from the pole, a radius. */
class OrbitCamera {
    var theta = 0.6f; var phi = 1.15f; var radius = 6f
    val target = floatArrayOf(0f, 1f, 0f)
    var fov = 40f
    var minRadius = 1f; var maxRadius = 40f
    var minPhi = 0.15f; var maxPhi = 1.52f
    private var vTheta = 0f; private var vPhi = 0f
    val view = FloatArray(16); val proj = FloatArray(16); val viewProj = FloatArray(16); private val inv = FloatArray(16)
    val eye = FloatArray(3)

    fun home(theta: Float, phi: Float, radius: Float, tx: Float, ty: Float, tz: Float) {
        this.theta = theta; this.phi = phi; this.radius = radius; target[0] = tx; target[1] = ty; target[2] = tz; vTheta = 0f; vPhi = 0f
    }
    fun drag(dx: Float, dy: Float) { vTheta = -dx * 0.009f; vPhi = -dy * 0.007f; theta += vTheta; phi = (phi + vPhi).coerceIn(minPhi, maxPhi) }
    fun release() {}
    fun zoom(f: Float) { radius = (radius / f).coerceIn(minRadius, maxRadius) }

    fun update(dt: Float, aspect: Float, dragging: Boolean) {
        if (!dragging) {
            val k = Math.pow(0.02, dt.toDouble()).toFloat()
            vTheta *= k; vPhi *= k
            theta += vTheta; phi = (phi + vPhi).coerceIn(minPhi, maxPhi)
        }
        eye[0] = target[0] + radius * sin(phi) * sin(theta)
        eye[1] = target[1] + radius * cos(phi)
        eye[2] = target[2] + radius * sin(phi) * cos(theta)
        Matrix.setLookAtM(view, 0, eye[0], eye[1], eye[2], target[0], target[1], target[2], 0f, 1f, 0f)
        Matrix.perspectiveM(proj, 0, fov, max(0.1f, aspect), max(0.02f, radius * 0.02f), radius * 20f + 50f)
        Matrix.multiplyMM(viewProj, 0, proj, 0, view, 0)
    }

    /** A world-space ray through the normalised device point (x, y in -1..1). */
    fun ray(ndcX: Float, ndcY: Float, origin: FloatArray, dir: FloatArray) {
        Matrix.invertM(inv, 0, viewProj, 0)
        val near = floatArrayOf(ndcX, ndcY, -1f, 1f); val far = floatArrayOf(ndcX, ndcY, 1f, 1f)
        val a = FloatArray(4); val b = FloatArray(4)
        Matrix.multiplyMV(a, 0, inv, 0, near, 0); Matrix.multiplyMV(b, 0, inv, 0, far, 0)
        for (i in 0..2) { a[i] /= a[3]; b[i] /= b[3] }
        origin[0] = a[0]; origin[1] = a[1]; origin[2] = a[2]
        var dx = b[0] - a[0]; var dy = b[1] - a[1]; var dz = b[2] - a[2]
        val l = sqrt(dx * dx + dy * dy + dz * dz); dx /= l; dy /= l; dz /= l
        dir[0] = dx; dir[1] = dy; dir[2] = dz
    }

    /** Projects a world point to normalised device coordinates; returns false when behind. */
    fun project(p: FloatArray, out: FloatArray): Boolean {
        val v = floatArrayOf(p[0], p[1], p[2], 1f); val r = FloatArray(4)
        Matrix.multiplyMV(r, 0, viewProj, 0, v, 0)
        if (r[3] <= 0f) return false
        out[0] = r[0] / r[3]; out[1] = r[1] / r[3]
        return true
    }
}

/** Distance along a ray to a sphere, or -1. */
fun raySphere(o: FloatArray, d: FloatArray, c: FloatArray, r: Float): Float {
    val ox = o[0] - c[0]; val oy = o[1] - c[1]; val oz = o[2] - c[2]
    val b = ox * d[0] + oy * d[1] + oz * d[2]
    val cc = ox * ox + oy * oy + oz * oz - r * r
    val h = b * b - cc
    if (h < 0f) return -1f
    val t = -b - sqrt(h)
    return if (t > 0f) t else -1f
}

/** Where a ray meets the plane through point p with normal n, or null. */
fun rayPlane(o: FloatArray, d: FloatArray, p: FloatArray, n: FloatArray, out: FloatArray): Boolean {
    val den = d[0] * n[0] + d[1] * n[1] + d[2] * n[2]
    if (kotlin.math.abs(den) < 1e-6f) return false
    val t = ((p[0] - o[0]) * n[0] + (p[1] - o[1]) * n[1] + (p[2] - o[2]) * n[2]) / den
    if (t < 0f) return false
    out[0] = o[0] + d[0] * t; out[1] = o[1] + d[1] * t; out[2] = o[2] + d[2] * t
    return true
}

internal fun clampf(v: Float, a: Float, b: Float) = min(b, max(a, v))
