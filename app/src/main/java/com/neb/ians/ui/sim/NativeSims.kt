package com.neb.ians.ui.sim

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.neb.ians.ui.sim.native2d.NativeConcaveMirror
import com.neb.ians.ui.sim.native2d.NativeProjectileMotion
import com.neb.ians.ui.sim.native2d.NativeWavesLab
import com.neb.ians.ui.sim.native3d.NativeEarthMoonSun
import com.neb.ians.ui.sim.native3d.NativeMoleculeGallery
import com.neb.ians.ui.sim.native3d.NativePendulumLab

/**
 * Lessons whose simulation runs natively (Compose Canvas for 2D, the app's own OpenGL ES 3
 * renderer for 3D) instead of in a WebView. Everything else keeps the web lesson.
 */
object NativeSims {
    private val byLesson = mapOf(
        "virtual-physics-lab/pendulum-lab" to "physics/pendulum-lab",
        "virtual-physics-lab/projectile-motion" to "physics/projectile-motion",
        "virtual-physics-lab/waves-and-sound" to "physics/waves-lab",
        "virtual-chemistry-lab/molecule-gallery" to "chemistry/molecule-viewer",
        "solar-system-journey/earth-moon-and-sun" to "space/earth-moon-sun",
        "neb-science-10-lab/concave-mirror" to "nebclass10/concave-mirror"
    )

    fun simFor(courseSlug: String, lessonSlug: String): String? = byLesson["$courseSlug/$lessonSlug"]

    @Composable
    fun Render(sim: String, modifier: Modifier = Modifier) {
        when (sim) {
            "physics/pendulum-lab" -> NativePendulumLab(modifier)
            "physics/projectile-motion" -> NativeProjectileMotion(modifier)
            "physics/waves-lab" -> NativeWavesLab(modifier)
            "chemistry/molecule-viewer" -> NativeMoleculeGallery(modifier)
            "space/earth-moon-sun" -> NativeEarthMoonSun(modifier)
            "nebclass10/concave-mirror" -> NativeConcaveMirror(modifier)
        }
    }
}
