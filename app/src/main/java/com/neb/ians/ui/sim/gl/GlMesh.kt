package com.neb.ians.ui.sim.gl

import android.opengl.GLES30
import java.nio.ByteBuffer
import java.nio.ByteOrder
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

/**
 * A triangle mesh: interleaved position + normal, 32-bit indices. Built on any thread,
 * uploaded to the GPU lazily on the GL thread the first time it is drawn.
 */
class GlMesh(private val data: FloatArray, private val indices: IntArray) {
    private var vao = 0
    private var vbo = 0
    private var ibo = 0
    val count: Int get() = indices.size

    fun bind() {
        if (vao == 0) upload()
        GLES30.glBindVertexArray(vao)
    }

    private fun upload() {
        val ids = IntArray(1)
        GLES30.glGenVertexArrays(1, ids, 0); vao = ids[0]
        GLES30.glBindVertexArray(vao)
        val bufs = IntArray(2)
        GLES30.glGenBuffers(2, bufs, 0); vbo = bufs[0]; ibo = bufs[1]
        val fb = ByteBuffer.allocateDirect(data.size * 4).order(ByteOrder.nativeOrder()).asFloatBuffer().put(data)
        fb.position(0)
        GLES30.glBindBuffer(GLES30.GL_ARRAY_BUFFER, vbo)
        GLES30.glBufferData(GLES30.GL_ARRAY_BUFFER, data.size * 4, fb, GLES30.GL_STATIC_DRAW)
        val ib = ByteBuffer.allocateDirect(indices.size * 4).order(ByteOrder.nativeOrder()).asIntBuffer().put(indices)
        ib.position(0)
        GLES30.glBindBuffer(GLES30.GL_ELEMENT_ARRAY_BUFFER, ibo)
        GLES30.glBufferData(GLES30.GL_ELEMENT_ARRAY_BUFFER, indices.size * 4, ib, GLES30.GL_STATIC_DRAW)
        GLES30.glEnableVertexAttribArray(0)
        GLES30.glVertexAttribPointer(0, 3, GLES30.GL_FLOAT, false, 24, 0)
        GLES30.glEnableVertexAttribArray(1)
        GLES30.glVertexAttribPointer(1, 3, GLES30.GL_FLOAT, false, 24, 12)
        GLES30.glBindVertexArray(0)
    }

    /** Frees the GPU buffers; the mesh re-uploads if drawn again (after a context loss). */
    fun release() {
        if (vao != 0) {
            GLES30.glDeleteVertexArrays(1, intArrayOf(vao), 0)
            GLES30.glDeleteBuffers(2, intArrayOf(vbo, ibo), 0)
        }
        vao = 0; vbo = 0; ibo = 0
    }

    /** Forgets GPU handles without deleting them (the context that owned them is gone). */
    fun invalidate() { vao = 0; vbo = 0; ibo = 0 }

    companion object {
        /** A surface of revolution about +y from (radius, y) points, normals from the profile. */
        fun lathe(profile: List<Pair<Float, Float>>, segments: Int = 32): GlMesh {
            val n = profile.size
            val verts = FloatArray((segments + 1) * n * 6)
            var k = 0
            for (s in 0..segments) {
                val a = 2.0 * PI * s / segments
                val ca = cos(a).toFloat(); val sa = sin(a).toFloat()
                for (i in 0 until n) {
                    val (r, y) = profile[i]
                    val (r0, y0) = profile[maxOf(0, i - 1)]
                    val (r1, y1) = profile[minOf(n - 1, i + 1)]
                    var dr = r1 - r0; var dy = y1 - y0
                    val len = sqrt(dr * dr + dy * dy).coerceAtLeast(1e-6f); dr /= len; dy /= len
                    val nx = dy; val ny = -dr
                    verts[k++] = r * ca; verts[k++] = y; verts[k++] = r * sa
                    verts[k++] = nx * ca; verts[k++] = ny; verts[k++] = nx * sa
                }
            }
            val idx = IntArray(segments * (n - 1) * 6)
            k = 0
            for (s in 0 until segments) for (i in 0 until n - 1) {
                val a = s * n + i; val b = (s + 1) * n + i
                idx[k++] = a; idx[k++] = a + 1; idx[k++] = b
                idx[k++] = b; idx[k++] = a + 1; idx[k++] = b + 1
            }
            return GlMesh(verts, idx)
        }

        fun sphere(r: Float, segments: Int = 32, rings: Int = 18): GlMesh {
            val profile = (0..rings).map { i ->
                val t = PI * i / rings
                (sin(t).toFloat() * r).coerceAtLeast(1e-4f) to (-cos(t).toFloat() * r)
            }
            val m = lathe(profile, segments)
            return m.withRadialNormals()
        }

        fun cylinder(rTop: Float, rBottom: Float, h: Float, segments: Int = 28, capped: Boolean = true): GlMesh {
            val side = lathe(listOf(rBottom to -h / 2, rTop to h / 2), segments)
            if (!capped) return side
            return merge(side, disc(rTop, segments, h / 2, up = true), disc(rBottom, segments, -h / 2, up = false))
        }

        fun disc(r: Float, segments: Int = 32, y: Float = 0f, up: Boolean = true): GlMesh {
            val v = FloatArray((segments + 2) * 6); var k = 0
            val ny = if (up) 1f else -1f
            v[k++] = 0f; v[k++] = y; v[k++] = 0f; v[k++] = 0f; v[k++] = ny; v[k++] = 0f
            for (s in 0..segments) {
                val a = 2.0 * PI * s / segments
                v[k++] = (cos(a) * r).toFloat(); v[k++] = y; v[k++] = (sin(a) * r).toFloat(); v[k++] = 0f; v[k++] = ny; v[k++] = 0f
            }
            val idx = IntArray(segments * 3); k = 0
            for (s in 0 until segments) { idx[k++] = 0; if (up) { idx[k++] = s + 2; idx[k++] = s + 1 } else { idx[k++] = s + 1; idx[k++] = s + 2 } }
            return GlMesh(v, idx)
        }

        fun box(w: Float, h: Float, d: Float): GlMesh {
            val x = w / 2; val y = h / 2; val z = d / 2
            val faces = arrayOf(
                floatArrayOf(0f, 0f, 1f, -x, -y, z, x, -y, z, x, y, z, -x, y, z),
                floatArrayOf(0f, 0f, -1f, x, -y, -z, -x, -y, -z, -x, y, -z, x, y, -z),
                floatArrayOf(1f, 0f, 0f, x, -y, z, x, -y, -z, x, y, -z, x, y, z),
                floatArrayOf(-1f, 0f, 0f, -x, -y, -z, -x, -y, z, -x, y, z, -x, y, -z),
                floatArrayOf(0f, 1f, 0f, -x, y, z, x, y, z, x, y, -z, -x, y, -z),
                floatArrayOf(0f, -1f, 0f, -x, -y, -z, x, -y, -z, x, -y, z, -x, -y, z)
            )
            val v = FloatArray(24 * 6); val idx = IntArray(36); var k = 0; var q = 0
            faces.forEachIndexed { f, a ->
                for (i in 0 until 4) { v[k++] = a[3 + i * 3]; v[k++] = a[4 + i * 3]; v[k++] = a[5 + i * 3]; v[k++] = a[0]; v[k++] = a[1]; v[k++] = a[2] }
                val b = f * 4
                idx[q++] = b; idx[q++] = b + 1; idx[q++] = b + 2; idx[q++] = b; idx[q++] = b + 2; idx[q++] = b + 3
            }
            return GlMesh(v, idx)
        }

        fun torus(radius: Float, tube: Float, segments: Int = 40, sides: Int = 12, arc: Float = (2 * PI).toFloat()): GlMesh {
            val v = FloatArray((segments + 1) * (sides + 1) * 6); var k = 0
            for (s in 0..segments) {
                val u = arc * s / segments
                for (t in 0..sides) {
                    val w = 2.0 * PI * t / sides
                    val cx = cos(u) * radius; val cy = sin(u) * radius
                    val nx = cos(w) * cos(u); val ny = cos(w) * sin(u); val nz = sin(w)
                    v[k++] = (cx + nx * tube).toFloat(); v[k++] = (cy + ny * tube).toFloat(); v[k++] = (nz * tube).toFloat()
                    v[k++] = nx.toFloat(); v[k++] = ny.toFloat(); v[k++] = nz.toFloat()
                }
            }
            val idx = IntArray(segments * sides * 6); k = 0
            for (s in 0 until segments) for (t in 0 until sides) {
                val a = s * (sides + 1) + t; val b = (s + 1) * (sides + 1) + t
                idx[k++] = a; idx[k++] = b; idx[k++] = a + 1; idx[k++] = b; idx[k++] = b + 1; idx[k++] = a + 1
            }
            return GlMesh(v, idx)
        }

        /** A flat square on the XZ plane facing +y. */
        fun plane(size: Float): GlMesh = box(size, 0.0001f, size)

        fun merge(vararg parts: GlMesh): GlMesh {
            val data = FloatArray(parts.sumOf { it.data.size }); val idx = IntArray(parts.sumOf { it.indices.size })
            var dv = 0; var di = 0; var base = 0
            for (p in parts) {
                System.arraycopy(p.data, 0, data, dv, p.data.size)
                for (i in p.indices) idx[di++] = i + base
                dv += p.data.size; base += p.data.size / 6
            }
            return GlMesh(data, idx)
        }
    }

    private fun withRadialNormals(): GlMesh {
        for (i in data.indices step 6) {
            val x = data[i]; val y = data[i + 1]; val z = data[i + 2]
            val l = sqrt(x * x + y * y + z * z).coerceAtLeast(1e-6f)
            data[i + 3] = x / l; data[i + 4] = y / l; data[i + 5] = z / l
        }
        return this
    }
}
