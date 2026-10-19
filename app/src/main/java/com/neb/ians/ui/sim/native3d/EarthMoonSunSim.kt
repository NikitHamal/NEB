package com.neb.ians.ui.sim.native3d

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.neb.ians.ui.sim.SimChips
import com.neb.ians.ui.sim.SimPanel
import com.neb.ians.ui.sim.SimReadouts
import com.neb.ians.ui.sim.SimSlider
import com.neb.ians.ui.sim.SimToggle
import com.neb.ians.ui.sim.gl.GlMaterial
import com.neb.ians.ui.sim.gl.GlMesh
import com.neb.ians.ui.sim.gl.GlNode
import com.neb.ians.ui.sim.gl.GlScene
import com.neb.ians.ui.sim.gl.GlSim
import com.neb.ians.ui.sim.gl.GlStage
import kotlin.math.PI
import kotlin.math.acos
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.random.Random

/**
 * Earth, Moon and Sun, natively. Distances and sizes are squeezed to fit, but the motions are
 * true to ratio: a 365.25-day year, a 27.32-day sidereal month, a 23.44° axis that keeps its
 * direction in space (hence seasons), and a Moon orbit tilted 5.1°. Sunlight comes from the Sun,
 * so the Moon's phase and the Earth's day side are what the geometry makes them.
 */
class EarthMoonSunGlSim : GlSim() {
    @Volatile var daysPerSecond = 8f
    @Volatile var showAxis = true
    @Volatile var showOrbits = true
    @Volatile var view = 0
    val day = mutableFloatStateOf(80f)
    val phase = mutableStateOf("—")
    val lit = mutableFloatStateOf(0f)
    val season = mutableStateOf("—")

    private var t = 80.0
    private lateinit var earth: GlNode; private lateinit var earthSpin: GlNode; private lateinit var moon: GlNode
    private lateinit var axis: GlNode; private lateinit var earthOrbit: GlNode; private lateinit var moonOrbit: GlNode
    private val R = 7f; private val r = 1.4f
    private var pub = 0f; private var shownView = -1

    override fun build(scene: GlScene) {
        scene.showGround = false; scene.skyTop = 0x0B1226; scene.skyBottom = 0x02040A; scene.exposure = 1.1f; scene.keyIntensity = 3.2f
        scene.camera.home(0.5f, 1.05f, 18f, 0f, 0f, 0f); scene.camera.minRadius = 2f; scene.camera.maxRadius = 40f; scene.camera.minPhi = 0.05f; scene.camera.maxPhi = 3.0f
        val rnd = Random(7)
        val star = GlMesh.sphere(1f, 6, 4)
        repeat(180) {
            val u = rnd.nextFloat() * 2 - 1; val a = rnd.nextFloat() * 2 * PI.toFloat(); val s = sqrt(1 - u * u)
            val m = GlMaterial(if (rnd.nextFloat() < 0.2f) 0xFFE8C2 else 0xDCE6FF, unlit = true, emissive = rnd.nextFloat() * 0.8f)
            scene.add(GlNode(star, m).at(s * cos(a) * 60, u * 60, s * sin(a) * 60).scaled(0.06f + rnd.nextFloat() * 0.1f))
        }
        scene.add(GlNode(GlMesh.sphere(1.2f, 48, 24), GlMaterial(0xFFC94A, unlit = true, emissive = 0.8f)))
        scene.add(GlNode(GlMesh.sphere(1.55f, 32, 16), GlMaterial(0xFFB020, unlit = true, alpha = 0.18f)))
        scene.add(GlNode(GlMesh.sphere(2.1f, 32, 16), GlMaterial(0xFF8A00, unlit = true, alpha = 0.07f)))
        earthOrbit = scene.add(GlNode(GlMesh.torus(R, 0.012f, 160, 4), GlMaterial(0x6B7FA6, unlit = true, alpha = 0.5f)).rotated((PI / 2).toFloat(), 0f, 0f))
        earth = scene.add(GlNode())
        val tilt = GlNode().rotated(0f, 0f, Math.toRadians(23.44).toFloat()); earth.add(tilt)
        earthSpin = tilt.add(GlNode(GlMesh.sphere(0.45f, 48, 24), GlMaterial(0x1E5BD8, roughness = 0.45f)))
        val land = GlMaterial(0x3E9B4F, roughness = 0.8f); val ice = GlMaterial(0xF4F8FF, roughness = 0.6f)
        val blob = GlMesh.sphere(1f, 16, 10)
        val lands = listOf(Triple(20f, 30f, 0.2f), Triple(-10f, 100f, 0.17f), Triple(40f, 200f, 0.22f), Triple(-25f, 260f, 0.14f), Triple(10f, 320f, 0.16f), Triple(55f, 120f, 0.15f))
        lands.forEach { (lat, lon, s) ->
            val la = Math.toRadians(lat.toDouble()); val lo = Math.toRadians(lon.toDouble())
            val nx = (cos(la) * sin(lo)).toFloat(); val ny = sin(la).toFloat(); val nz = (cos(la) * cos(lo)).toFloat()
            earthSpin.add(GlNode(blob, land).at(nx * 0.43f, ny * 0.43f, nz * 0.43f).rotated(acos(ny), atan2(nx, nz), 0f).scaled(s, 0.035f, s * 0.8f))
        }
        earthSpin.add(GlNode(blob, ice).at(0f, 0.43f, 0f).scaled(0.18f, 0.04f, 0.18f)); earthSpin.add(GlNode(blob, ice).at(0f, -0.43f, 0f).scaled(0.2f, 0.04f, 0.2f))
        axis = tilt.add(GlNode(GlMesh.cylinder(0.008f, 0.008f, 1.5f, 8, false), GlMaterial(0xFFFFFF, unlit = true, alpha = 0.8f)))
        val moonPlane = earth.add(GlNode().rotated(Math.toRadians(5.1).toFloat(), 0f, 0f))
        moonOrbit = moonPlane.add(GlNode(GlMesh.torus(r, 0.008f, 96, 4), GlMaterial(0x8C97B3, unlit = true, alpha = 0.45f)).rotated((PI / 2).toFloat(), 0f, 0f))
        moon = moonPlane.add(GlNode(GlMesh.sphere(0.13f, 32, 16), GlMaterial(0xB9BCC4, roughness = 0.85f)))
    }

    override fun step(dt: Float, scene: GlScene) {
        t += dt * daysPerSecond
        val yearA = 2 * PI * (t / 365.25)
        val ex = (cos(yearA) * R).toFloat(); val ez = (-sin(yearA) * R).toFloat()
        earth.at(ex, 0f, ez)
        earthSpin.rotation[1] = (2 * PI * (t % 1.0)).toFloat()
        val moonA = 2 * PI * (t / 27.32)
        moon.at((cos(moonA) * r).toFloat(), 0f, (-sin(moonA) * r).toFloat())
        axis.visible = showAxis; earthOrbit.visible = showOrbits; moonOrbit.visible = showOrbits
        val l = sqrt(ex * ex + ez * ez); scene.keyDir[0] = -ex / l; scene.keyDir[1] = 0.05f; scene.keyDir[2] = -ez / l
        if (view != shownView || view == 1) {
            when (view) {
                1 -> { scene.camera.target[0] = ex; scene.camera.target[1] = 0f; scene.camera.target[2] = ez; if (shownView != 1) { scene.camera.radius = 4.5f; scene.camera.phi = 1.2f } }
                2 -> scene.camera.home((PI / 2).toFloat(), 1.53f, 19f, 0f, 0f, 0f)
                else -> if (shownView != view) scene.camera.home(0.5f, 1.05f, 18f, 0f, 0f, 0f)
            }
            shownView = view
        }
        pub += dt
        if (pub > 0.12f) {
            pub = 0f
            day.floatValue = (t % 365.25).toFloat()
            // phase from the Sun-Earth-Moon angle: the Moon's elongation from the Sun as seen from Earth
            val synodic = ((t / 29.53) % 1.0)
            val illum = ((1 - cos(2 * PI * synodic)) / 2).toFloat()
            lit.floatValue = illum
            phase.value = when ((synodic * 8 + 0.5).toInt() % 8) { 0 -> "New moon"; 1 -> "Waxing crescent"; 2 -> "First quarter"; 3 -> "Waxing gibbous"; 4 -> "Full moon"; 5 -> "Waning gibbous"; 6 -> "Last quarter"; else -> "Waning crescent" }
            val d = (t % 365.25)
            season.value = when { d < 79 || d >= 355 -> "Winter (north)"; d < 172 -> "Spring (north)"; d < 265 -> "Summer (north)"; else -> "Autumn (north)" }
        }
    }
}

@Composable
fun NativeEarthMoonSun(modifier: Modifier = Modifier) {
    val sim = remember { EarthMoonSunGlSim() }
    var speed by remember { mutableFloatStateOf(8f) }
    var axis by remember { mutableStateOf(true) }
    var orbits by remember { mutableStateOf(true) }
    var view by remember { mutableStateOf(0) }
    Column(modifier) {
        GlStage(sim, Modifier.fillMaxWidth().aspectRatio(1f))
        SimPanel {
            SimReadouts(listOf(
                "Day of the year" to "%.0f".format(sim.day.floatValue),
                "Season" to sim.season.value,
                "Moon" to sim.phase.value,
                "Moon lit" to "%.0f %%".format(sim.lit.floatValue * 100)
            ))
            SimChips(listOf(0 to "View from space", 1 to "Follow Earth", 2 to "Side-on"), view) { view = it; sim.view = it }
            SimSlider("Time speed", speed, 0f..60f, { "%.0f days/s".format(it) }, { speed = it; sim.daysPerSecond = it })
            SimToggle("Show Earth's axis", axis) { axis = it; sim.showAxis = it }
            SimToggle("Show orbit lines", orbits) { orbits = it; sim.showOrbits = it }
        }
    }
}
