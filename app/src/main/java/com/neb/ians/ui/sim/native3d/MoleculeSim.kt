package com.neb.ians.ui.sim.native3d

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import com.neb.ians.ui.sim.SimChips
import com.neb.ians.ui.sim.SimPanel
import com.neb.ians.ui.sim.SimReadouts
import com.neb.ians.ui.sim.SimToggle
import com.neb.ians.ui.sim.gl.GlMaterial
import com.neb.ians.ui.sim.gl.GlMesh
import com.neb.ians.ui.sim.gl.GlNode
import com.neb.ians.ui.sim.gl.GlScene
import com.neb.ians.ui.sim.gl.GlSim
import com.neb.ians.ui.sim.gl.GlStage
import com.neb.ians.ui.sim.gl.raySphere
import kotlin.math.PI
import kotlin.math.acos
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

internal class Atom(val el: String, val x: Float, val y: Float, val z: Float)
internal class Molecule(val name: String, val atoms: List<Atom>, val bonds: List<Triple<Int, Int, Int>>, val shape: String, val ionic: Boolean = false)

private val STYLE = mapOf(
    "H" to (0xF1F5F9 to 0.33f), "C" to (0x374151 to 0.50f), "N" to (0x3B82F6 to 0.48f),
    "O" to (0xEF4444 to 0.47f), "Na" to (0x8B5CF6 to 0.45f), "Cl" to (0x22C55E to 0.56f)
)
val ELEMENT_INFO = mapOf(
    "H" to "Hydrogen: the lightest element. One proton, one electron; in molecules it always forms exactly one bond.",
    "C" to "Carbon: the backbone of life. Four strong bonds, and chains of itself without end.",
    "N" to "Nitrogen: 78% of the air as N₂. In ammonia it forms three bonds and keeps a lone pair.",
    "O" to "Oxygen: forms two bonds; its strong pull on electrons makes water polar.",
    "Na" to "Sodium: gives away one electron to become Na⁺, locked in the salt lattice with Cl⁻.",
    "Cl" to "Chlorine: takes one electron to become Cl⁻, pairing with sodium to make table salt."
)

private val TET = listOf(floatArrayOf(1f, 1f, 1f), floatArrayOf(1f, -1f, -1f), floatArrayOf(-1f, 1f, -1f), floatArrayOf(-1f, -1f, 1f)).map { v -> val l = sqrt(3f); floatArrayOf(v[0] / l, v[1] / l, v[2] / l) }

private fun molecules(): List<Molecule> {
    val water = run {
        val a = (104.5 / 2 * PI / 180)
        Molecule("Water H₂O", listOf(Atom("O", 0f, 0.25f, 0f), Atom("H", (sin(a) * 0.96).toFloat(), (0.25 - cos(a) * 0.96).toFloat(), 0f), Atom("H", (-sin(a) * 0.96).toFloat(), (0.25 - cos(a) * 0.96).toFloat(), 0f)),
            listOf(Triple(0, 1, 1), Triple(0, 2, 1)), "Bent, 104.5°")
    }
    val co2 = Molecule("Carbon dioxide CO₂", listOf(Atom("C", 0f, 0f, 0f), Atom("O", 1.16f, 0f, 0f), Atom("O", -1.16f, 0f, 0f)), listOf(Triple(0, 1, 2), Triple(0, 2, 2)), "Linear, 180°")
    val ch4 = Molecule("Methane CH₄", listOf(Atom("C", 0f, 0f, 0f)) + TET.map { Atom("H", it[0] * 1.09f, it[1] * 1.09f, it[2] * 1.09f) }, (1..4).map { Triple(0, it, 1) }, "Tetrahedral, 109.5°")
    val nh3 = Molecule("Ammonia NH₃", listOf(Atom("N", 0f, 0.22f, 0f)) + (0 until 3).map { i -> val a = i / 3.0 * 2 * PI; Atom("H", (cos(a) * 0.94).toFloat(), 0.22f - 0.38f, (sin(a) * 0.94).toFloat()) }, (1..3).map { Triple(0, it, 1) }, "Pyramidal, 107°")
    val o2 = Molecule("Oxygen O₂", listOf(Atom("O", 0.6f, 0f, 0f), Atom("O", -0.6f, 0f, 0f)), listOf(Triple(0, 1, 2)), "Linear, a double bond")
    val ethanol = Molecule("Ethanol C₂H₅OH", listOf(
        Atom("C", -1.23f, -0.25f, 0.05f), Atom("C", 0.07f, 0.51f, 0f), Atom("O", 1.16f, -0.36f, -0.05f), Atom("H", 1.97f, 0.12f, 0.1f),
        Atom("H", -2.1f, 0.4f, 0.1f), Atom("H", -1.3f, -0.9f, 0.9f), Atom("H", -1.33f, -0.87f, -0.86f), Atom("H", 0.13f, 1.15f, 0.89f), Atom("H", 0.1f, 1.18f, -0.85f)
    ), listOf(Triple(0, 1, 1), Triple(1, 2, 1), Triple(2, 3, 1), Triple(0, 4, 1), Triple(0, 5, 1), Triple(0, 6, 1), Triple(1, 7, 1), Triple(1, 8, 1)), "Tetrahedral carbons, an –OH group")
    val benzene = run {
        val atoms = ArrayList<Atom>(); val bonds = ArrayList<Triple<Int, Int, Int>>()
        for (i in 0 until 6) { val a = i / 6.0 * 2 * PI; atoms.add(Atom("C", (cos(a) * 1.39).toFloat(), 0f, (sin(a) * 1.39).toFloat())) }
        for (i in 0 until 6) { val a = i / 6.0 * 2 * PI; atoms.add(Atom("H", (cos(a) * 2.47).toFloat(), 0f, (sin(a) * 2.47).toFloat())); bonds.add(Triple(i, (i + 1) % 6, if (i % 2 == 0) 2 else 1)); bonds.add(Triple(i, i + 6, 1)) }
        Molecule("Benzene C₆H₆", atoms, bonds, "Flat hexagon, 120°")
    }
    val nacl = run {
        val atoms = ArrayList<Atom>(); val bonds = ArrayList<Triple<Int, Int, Int>>(); val sp = 1.55f
        fun idx(i: Int, j: Int, k: Int) = i * 9 + j * 3 + k
        for (i in 0 until 3) for (j in 0 until 3) for (k in 0 until 3) {
            atoms.add(Atom(if ((i + j + k) % 2 == 0) "Na" else "Cl", (i - 1) * sp, (j - 1) * sp, (k - 1) * sp))
            if (i > 0) bonds.add(Triple(idx(i - 1, j, k), idx(i, j, k), 1)); if (j > 0) bonds.add(Triple(idx(i, j - 1, k), idx(i, j, k), 1)); if (k > 0) bonds.add(Triple(idx(i, j, k - 1), idx(i, j, k), 1))
        }
        Molecule("Salt NaCl lattice", atoms, bonds, "Cubic lattice of ions", ionic = true)
    }
    return listOf(water, co2, ch4, nh3, o2, ethanol, benzene, nacl)
}

/** Points a unit +y cylinder from a to b (rotation X then Y). */
internal fun GlNode.span(ax: Float, ay: Float, az: Float, bx: Float, by: Float, bz: Float): GlNode {
    val dx = bx - ax; val dy = by - ay; val dz = bz - az; val l = sqrt(dx * dx + dy * dy + dz * dz).coerceAtLeast(1e-5f)
    at((ax + bx) / 2, (ay + by) / 2, (az + bz) / 2)
    rotated(acos((dy / l).coerceIn(-1f, 1f)), atan2(dx, dz), 0f)
    scaled(1f, l, 1f)
    return this
}

/**
 * The molecule gallery, natively: glossy ball-and-stick models (bonds coloured half and half
 * by the atoms they join, double bonds as two sticks), spinning slowly; tap an atom to learn it.
 */
class MoleculeGlSim : GlSim() {
    private val all = molecules()
    @Volatile var index = 0
    @Volatile var spin = true
    val tapped = mutableStateOf<String?>(null)
    private var shown = -1
    private val holder = GlNode()
    private var angle = 0f
    private val sphereMesh = GlMesh.sphere(1f, 40, 22)
    private val stick = GlMesh.cylinder(1f, 1f, 1f, 18, false)
    private val mats = HashMap<String, GlMaterial>()
    private val centers = ArrayList<Pair<FloatArray, Pair<String, Float>>>()

    val names: List<String> get() = all.map { it.name }
    internal fun info(i: Int) = all[i]

    private fun mat(el: String) = mats.getOrPut(el) { GlMaterial(STYLE[el]?.first ?: 0xCCCCCC, roughness = 0.18f) }

    override fun build(scene: GlScene) {
        scene.camera.home(0.4f, 1.2f, 7f, 0f, 0f, 0f); scene.camera.minRadius = 3f; scene.camera.maxRadius = 16f
        scene.groundY = -2.6f; scene.skyTop = 0x2A3346; scene.skyBottom = 0x0E121B; scene.groundColor = 0x1B2130; scene.exposure = 1.15f
        scene.add(holder)
    }

    private fun rebuild() {
        holder.children.clear(); centers.clear()
        val m = all[index]
        val s = 1.5f
        m.atoms.forEach { a ->
            val r = (STYLE[a.el]?.second ?: 0.45f) * (if (m.ionic) 0.95f else 0.82f)
            holder.add(GlNode(sphereMesh, mat(a.el)).at(a.x * s, a.y * s, a.z * s).scaled(r)).tag = a.el
        }
        m.bonds.forEach { (i, j, order) ->
            val a = m.atoms[i]; val b = m.atoms[j]
            val ax = a.x * s; val ay = a.y * s; val az = a.z * s; val bx = b.x * s; val by = b.y * s; val bz = b.z * s
            val mx = (ax + bx) / 2; val my = (ay + by) / 2; val mz = (az + bz) / 2
            val r = if (m.ionic) 0.05f else if (order > 1) 0.075f else 0.11f
            var ox = 0f; var oy = 0f; var oz = 0f
            if (order > 1) { val dx = bx - ax; val dz = bz - az; val l = sqrt(dx * dx + dz * dz).coerceAtLeast(1e-4f); ox = -dz / l * 0.13f; oz = dx / l * 0.13f; if (l < 1e-3f) oy = 0.13f }
            val offs = if (order > 1) listOf(1f, -1f) else listOf(0f)
            offs.forEach { k ->
                holder.add(GlNode(stick, mat(a.el)).span(ax + ox * k, ay + oy * k, az + oz * k, mx + ox * k, my + oy * k, mz + oz * k).also { it.scale[0] = r; it.scale[2] = r })
                holder.add(GlNode(stick, mat(b.el)).span(mx + ox * k, my + oy * k, mz + oz * k, bx + ox * k, by + oy * k, bz + oz * k).also { it.scale[0] = r; it.scale[2] = r })
            }
        }
        shown = index
    }

    override fun step(dt: Float, scene: GlScene) {
        if (shown != index) rebuild()
        if (spin) angle += dt * 0.35f
        holder.rotation[1] = angle
    }

    override fun pointerDown(origin: FloatArray, dir: FloatArray): Boolean {
        var best = Float.MAX_VALUE; var el: String? = null
        val c = FloatArray(3)
        holder.children.forEach { n -> if (n.tag is String) { n.worldPosition(c); val t = raySphere(origin, dir, c, n.scale[0] * 1.15f); if (t in 0f..best) { best = t; el = n.tag as String } } }
        if (el != null) tapped.value = el
        return false
    }
}

@Composable
fun NativeMoleculeGallery(modifier: Modifier = Modifier) {
    val sim = remember { MoleculeGlSim() }
    var i by remember { mutableStateOf(0) }
    var spin by remember { mutableStateOf(true) }
    val m = sim.info(i)
    Column(modifier) {
        GlStage(sim, Modifier.fillMaxWidth().aspectRatio(1f))
        SimPanel {
            SimChips(sim.names.mapIndexed { k, n -> k to n }, i) { i = it; sim.index = it; sim.tapped.value = null }
            SimReadouts(listOf("Atoms" to "${m.atoms.size}", "Bonds" to "${m.bonds.size}", "Shape" to m.shape, "Type" to if (m.ionic) "Ionic" else "Covalent"))
            SimToggle("Spin", spin) { spin = it; sim.spin = it }
            val el = sim.tapped.value
            Text(if (el == null) "Tap an atom to find out what it is." else ELEMENT_INFO[el] ?: el,
                style = MaterialTheme.typography.bodyMedium, fontWeight = if (el == null) FontWeight.Normal else FontWeight.Medium,
                color = if (el == null) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface)
        }
    }
}
