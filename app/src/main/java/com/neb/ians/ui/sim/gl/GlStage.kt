package com.neb.ians.ui.sim.gl

import android.app.ActivityManager
import android.content.Context
import android.opengl.GLSurfaceView
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import javax.microedition.khronos.egl.EGL10
import javax.microedition.khronos.egl.EGLConfig
import javax.microedition.khronos.egl.EGLDisplay

/** Whether this phone should get the light path: no MSAA, 30 fps cap. */
fun isLowEndDevice(context: Context): Boolean {
    val am = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
    return am.isLowRamDevice || am.memoryClass <= 192 || Runtime.getRuntime().availableProcessors() <= 4
}

/** Picks an RGB888 + 16-bit depth config, with 4x MSAA when the device can afford it. */
private class MsaaChooser(private val msaa: Boolean) : GLSurfaceView.EGLConfigChooser {
    override fun chooseConfig(egl: EGL10, display: EGLDisplay): EGLConfig {
        fun pick(samples: Int): EGLConfig? {
            val attrs = intArrayOf(
                EGL10.EGL_RED_SIZE, 8, EGL10.EGL_GREEN_SIZE, 8, EGL10.EGL_BLUE_SIZE, 8, EGL10.EGL_DEPTH_SIZE, 16,
                EGL10.EGL_RENDERABLE_TYPE, 0x40,
                EGL10.EGL_SAMPLE_BUFFERS, if (samples > 0) 1 else 0, EGL10.EGL_SAMPLES, samples, EGL10.EGL_NONE
            )
            val n = IntArray(1)
            if (!egl.eglChooseConfig(display, attrs, null, 0, n) || n[0] <= 0) return null
            val out = arrayOfNulls<EGLConfig>(n[0])
            egl.eglChooseConfig(display, attrs, out, n[0], n)
            return out.firstOrNull()
        }
        return (if (msaa) pick(4) else null) ?: pick(0)
            ?: throw IllegalStateException("No OpenGL ES 3 config")
    }
}

/**
 * A GLSurfaceView for a [GlSim]: one finger orbits (unless the sim takes the press to drag
 * something), two fingers pinch to zoom. Touch hit-tests run against the last frame's camera,
 * under the same lock the renderer draws with.
 */
class NebGlView(context: Context, sim: GlSim) : GLSurfaceView(context) {
    private val low = isLowEndDevice(context)
    val renderer: GlRenderer
    private val scene = GlScene()
    private val simRef = sim
    private var lastX = 0f; private var lastY = 0f
    private var mode = 0
    private val o = FloatArray(3); private val d = FloatArray(3)
    private val pinch = ScaleGestureDetector(context, object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
        override fun onScale(det: ScaleGestureDetector): Boolean { synchronized(scene) { scene.camera.zoom(det.scaleFactor) }; return true }
    })

    init {
        setEGLContextClientVersion(3)
        setEGLConfigChooser(MsaaChooser(!low))
        preserveEGLContextOnPause = true
        renderer = GlRenderer(sim, scene, low)
        setRenderer(renderer)
        renderMode = RENDERMODE_CONTINUOUSLY
    }

    private fun ray(x: Float, y: Float) {
        scene.camera.ray(x / width * 2f - 1f, 1f - y / height * 2f, o, d)
    }

    override fun onTouchEvent(e: MotionEvent): Boolean {
        pinch.onTouchEvent(e)
        when (e.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                parent?.requestDisallowInterceptTouchEvent(true)
                lastX = e.x; lastY = e.y
                synchronized(scene) { ray(e.x, e.y); mode = if (simRef.pointerDown(o, d)) 2 else 1 }
                renderer.dragging = mode == 1
            }
            MotionEvent.ACTION_POINTER_DOWN -> { if (mode == 2) synchronized(scene) { simRef.pointerUp() }; mode = 3 }
            MotionEvent.ACTION_MOVE -> {
                if (mode == 1 && e.pointerCount == 1) synchronized(scene) { scene.camera.drag(e.x - lastX, e.y - lastY) }
                else if (mode == 2) synchronized(scene) { ray(e.x, e.y); simRef.pointerMove(o, d) }
                lastX = e.x; lastY = e.y
            }
            MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                if (mode == 2) synchronized(scene) { simRef.pointerUp() }
                mode = 0; renderer.dragging = false
                parent?.requestDisallowInterceptTouchEvent(false)
            }
        }
        return true
    }
}

/** A native 3D stage in Compose. Pauses with the screen's lifecycle; the sim keeps its state. */
@Composable
fun GlStage(sim: GlSim, modifier: Modifier = Modifier) {
    val owner = LocalLifecycleOwner.current
    val holder = remember { arrayOfNulls<NebGlView>(1) }
    DisposableEffect(owner) {
        val obs = LifecycleEventObserver { _, ev ->
            when (ev) {
                Lifecycle.Event.ON_PAUSE -> holder[0]?.onPause()
                Lifecycle.Event.ON_RESUME -> holder[0]?.onResume()
                else -> Unit
            }
        }
        owner.lifecycle.addObserver(obs)
        onDispose { owner.lifecycle.removeObserver(obs) }
    }
    AndroidView(
        factory = { ctx -> NebGlView(ctx, sim).also { holder[0] = it } },
        modifier = modifier,
        onRelease = { it.onPause() }
    )
}
