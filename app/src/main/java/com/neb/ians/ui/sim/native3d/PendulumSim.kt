package com.neb.ians.ui.sim.native3d

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.neb.ians.ui.sim.SimButton
import com.neb.ians.ui.sim.SimChips
import com.neb.ians.ui.sim.SimPanel
import com.neb.ians.ui.sim.SimReadouts
import com.neb.ians.ui.sim.SimSection
import com.neb.ians.ui.sim.SimSlider
import com.neb.ians.ui.sim.gl.GlMaterial
import com.neb.ians.ui.sim.gl.GlMesh
import com.neb.ians.ui.sim.gl.GlNode
import com.neb.ians.ui.sim.gl.GlScene
import com.neb.ians.ui.sim.gl.GlSim
import com.neb.ians.ui.sim.gl.GlStage
import com.neb.ians.ui.sim.gl.rayPlane
import com.neb.ians.ui.sim.gl.raySphere
import kotlin.math.PI
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

/**
 * The pendulum lab, natively: a brass bob on a thread from a retort stand, integrating the full
 * equation θ'' = -(g/L) sin θ - bθ' with RK4. Drag the bob to set the angle and let go; the
 * measured period (timed between upward crossings of the vertical) is compared with 2π√(L/g).
 */
class PendulumGlSim : GlSim() {
    @Volatile var length = 1.0f
    @Volatile var gravity = 9.81f
    @Volatile var damping = 0.02f
    @Volatile var startAngle = 15f
    val period = mutableFloatStateOf(0f)
    val swings = mutableIntStateOf(0)
    val angleNow = mutableFloatStateOf(0f)

    private var th = 0.26; private var w = 0.0
    private var held = false
    private var t = 0.0; private var lastCross = -1.0
    private var publish = 0f
    private val pivotY = 2.15f
    private lateinit var thread: GlNode; private lateinit var bob: GlNode; private lateinit var arc: GlNode
    private val bobPos = FloatArray(3)
    private val hit = FloatArray(3)

    fun reset() { synchronized(this) { th = Math.toRadians(startAngle.toDouble()); w = 0.0; swings.intValue = 0; lastCross = -1.0; period.floatValue = 0f } }

    override fun build(scene: GlScene) {
        scene.camera.home(0.35f, 1.28f, 4.2f, 0f, 1.25f, 0f)
        scene.camera.minRadius = 1.6f; scene.camera.maxRadius = 9f
        val dark = GlMaterial(0x2B3138, roughness = 0.55f)
        val steel = GlMaterial(0xC9D0D8, roughness = 0.28f, metalness = 1f)
        val brass = GlMaterial(0xD4A94A, roughness = 0.22f, metalness = 1f)
        val thr = GlMaterial(0xF5F5F4, roughness = 0.8f)
        scene.add(GlNode(GlMesh.box(1.1f, 0.06f, 0.7f), dark).at(-0.35f, 0.03f, 0f)).blobShadow = 0.7f
        scene.add(GlNode(GlMesh.cylinder(0.022f, 0.022f, 2.2f), steel).at(-0.75f, 1.13f, 0f))
        scene.add(GlNode(GlMesh.box(0.07f, 0.07f, 0.07f), dark).at(-0.75f, pivotY, 0f))
        scene.add(GlNode(GlMesh.cylinder(0.012f, 0.012f, 0.78f), steel).at(-0.37f, pivotY, 0f).rotated(0f, 0f, (PI / 2).toFloat()))
        scene.add(GlNode(GlMesh.cylinder(0.03f, 0.03f, 0.06f), GlMaterial(0xB98B5A, roughness = 0.9f)).at(0f, pivotY, 0f))
        thread = scene.add(GlNode(GlMesh.cylinder(0.0035f, 0.0035f, 1f, 6, false), thr))
        bob = scene.add(GlNode(GlMesh.sphere(0.06f, 36, 20), brass)); bob.blobShadow = 0.12f
        arc = scene.add(GlNode(GlMesh.torus(0.35f, 0.004f, 48, 6, (PI / 3).toFloat()), GlMaterial(0x1E2A4A, roughness = 0.5f, alpha = 0.55f)))
        arc.rotated(0f, 0f, (-PI / 2 - PI / 6).toFloat()).at(0f, pivotY, 0f)
        reset()
    }

    private fun deriv(a: Double, v: Double, L: Double, g: Double, b: Double) = -(g / L) * sin(a) - b * v

    override fun step(dt: Float, scene: GlScene) {
        val L = length.toDouble(); val g = gravity.toDouble(); val b = damping.toDouble()
        if (!held) {
            val n = maxOf(1, (dt / 0.002f).toInt()); val h = dt.toDouble() / n
            for (i in 0 until n) {
                val k1t = w; val k1w = deriv(th, w, L, g, b)
                val k2t = w + 0.5 * h * k1w; val k2w = deriv(th + 0.5 * h * k1t, w + 0.5 * h * k1w, L, g, b)
                val k3t = w + 0.5 * h * k2w; val k3w = deriv(th + 0.5 * h * k2t, w + 0.5 * h * k2w, L, g, b)
                val k4t = w + h * k3w; val k4w = deriv(th + h * k3t, w + h * k3w, L, g, b)
                val prev = th
                th += h / 6 * (k1t + 2 * k2t + 2 * k3t + k4t); w += h / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
                t += h
                if (prev < 0 && th >= 0 && w > 0) {
                    val tc = t - h * th / (th - prev)
                    if (lastCross >= 0) { period.floatValue = (tc - lastCross).toFloat(); swings.intValue = swings.intValue + 1 }
                    lastCross = tc
                }
            }
        }
        val Lf = length
        bobPos[0] = (sin(th) * Lf).toFloat(); bobPos[1] = pivotY - (cos(th) * Lf).toFloat(); bobPos[2] = 0f
        bob.at(bobPos[0], bobPos[1], bobPos[2])
        thread.at(bobPos[0] / 2, (pivotY + bobPos[1]) / 2, 0f).rotated(0f, 0f, th.toFloat()).scaled(1f, Lf - 0.06f, 1f)
        arc.scaled(Lf / 0.35f * 0.5f, Lf / 0.35f * 0.5f, 1f)
        publish += dt
        if (publish > 0.1f) { publish = 0f; angleNow.floatValue = Math.toDegrees(th).toFloat() }
    }

    override fun pointerDown(origin: FloatArray, dir: FloatArray): Boolean {
        if (raySphere(origin, dir, bobPos, 0.16f) < 0f) return false
        held = true; w = 0.0; return true
    }
    override fun pointerMove(origin: FloatArray, dir: FloatArray) {
        if (!rayPlane(origin, dir, floatArrayOf(0f, 0f, 0f), floatArrayOf(0f, 0f, 1f), hit)) return
        th = atan2((hit[0]).toDouble(), (pivotY - hit[1]).toDouble()).coerceIn(-1.4, 1.4)
    }
    override fun pointerUp() { held = false; w = 0.0; lastCross = -1.0; swings.intValue = 0 }
}

@Composable
fun NativePendulumLab(modifier: Modifier = Modifier) {
    val sim = remember { PendulumGlSim() }
    var L by remember { mutableFloatStateOf(1.0f) }
    var g by remember { mutableFloatStateOf(9.81f) }
    var preset by remember { mutableStateOf("Earth") }
    var amp by remember { mutableFloatStateOf(15f) }
    var damp by remember { mutableFloatStateOf(0.02f) }
    val theory = 2 * PI * sqrt(L / g)
    Column(modifier) {
        GlStage(sim, Modifier.fillMaxWidth().aspectRatio(4f / 3.4f))
        SimPanel {
            SimReadouts(listOf(
                "Measured period" to if (sim.period.floatValue > 0f) "%.3f s".format(sim.period.floatValue) else "—",
                "Theory 2π√(L/g)" to "%.3f s".format(theory),
                "Completed swings" to "${sim.swings.intValue}",
                "Angle now" to "%.1f°".format(sim.angleNow.floatValue)
            ))
            SimSection("Pendulum")
            SimSlider("Length L", L, 0.2f..2.0f, { "%.2f m".format(it) }, { L = it; sim.length = it })
            SimChips(listOf("Earth" to "Earth 9.81", "Moon" to "Moon 1.62", "Jupiter" to "Jupiter 24.8"), preset) { p ->
                preset = p; g = when (p) { "Moon" -> 1.62f; "Jupiter" -> 24.8f; else -> 9.81f }; sim.gravity = g
            }
            SimSlider("Initial angle", amp, 2f..80f, { "%.0f°".format(it) }, { amp = it; sim.startAngle = it })
            SimSlider("Air damping", damp, 0f..0.5f, { "%.2f /s".format(it) }, { damp = it; sim.damping = it })
            Row { SimButton("Reset swing") { sim.reset() } }
            if (amp > 20f) androidx.compose.material3.Text(
                "At ${amp.toInt()}° the period is about ${"%.1f".format((amp * PI / 180).let { it * it / 16 } * 100)} % longer than 2π√(L/g): the formula assumes sin θ ≈ θ.",
                style = androidx.compose.material3.MaterialTheme.typography.bodySmall,
                color = androidx.compose.material3.MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
