package com.neb.ians.ui.screens.reader.pdf

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.AnimationState
import androidx.compose.animation.core.animateDecay
import androidx.compose.animation.core.exponentialDecay
import androidx.compose.animation.core.FiniteAnimationSpec
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.calculateCentroid
import androidx.compose.foundation.gestures.calculatePan
import androidx.compose.foundation.gestures.calculateZoom
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.PointerEventPass
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.pointer.positionChange
import androidx.compose.ui.input.pointer.util.VelocityTracker
import androidx.compose.ui.unit.IntSize
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch
import kotlin.math.abs

/**
 * Zoom for the reader. The content is scaled from its top-left corner and translated, so the
 * visible window is always inside the scaled content. In the scrolling layout vertical
 * movement goes to the list (see [zoomGestures]); in the paged layout it moves the page.
 */
@Stable
class ReaderZoomState(private val spec: FiniteAnimationSpec<Float>) {
    var scale by mutableFloatStateOf(1f)
        private set
    var offsetX by mutableFloatStateOf(0f)
        private set
    var offsetY by mutableFloatStateOf(0f)
        private set

    /** The zoom the pages are rendered for. Changes only when a gesture ends, never mid-pinch. */
    var renderScale by mutableFloatStateOf(1f)
        private set

    var size: IntSize = IntSize.Zero

    val isZoomed: Boolean get() = scale > 1.01f

    /**
     * Zooms about [centroid]. With [scrollBy] (scrolling layout) the vertical anchoring is done by
     * scrolling the list rather than translating it, so the page under the fingers stays put.
     */
    fun transform(centroid: Offset, zoom: Float, pan: Offset, scrollBy: ((Float) -> Unit)?) {
        val next = (scale * zoom).coerceIn(MIN, MAX)
        val factor = next / scale
        offsetX = centroid.x - (centroid.x - offsetX) * factor + pan.x
        if (scrollBy == null) {
            offsetY = centroid.y - (centroid.y - offsetY) * factor + pan.y
        } else {
            offsetY = 0f
            scrollBy((centroid.y * (factor - 1f) - pan.y) / next)
        }
        scale = next
        clamp()
    }

    /** Moves by [delta]; returns the vertical part that could not be used. */
    fun pan(delta: Offset, moveY: Boolean): Float {
        offsetX += delta.x
        if (!moveY) {
            clamp()
            return delta.y
        }
        val before = offsetY
        offsetY += delta.y
        clamp()
        return delta.y - (offsetY - before)
    }

    fun settle() {
        if (scale < 1.02f) reset() else renderScale = RENDER_STEPS.lastOrNull { it <= scale + 0.25f } ?: 1f
    }

    fun reset() {
        scale = 1f
        offsetX = 0f
        offsetY = 0f
        renderScale = 1f
    }

    suspend fun animateTo(target: Float, focus: Offset, scrollBy: ((Float) -> Unit)?) {
        val anim = Animatable(scale)
        anim.animateTo(target, spec) {
            transform(focus, value / scale, Offset.Zero, scrollBy)
        }
        settle()
    }

    private fun clamp() {
        val maxX = (scale - 1f) * size.width
        val maxY = (scale - 1f) * size.height
        offsetX = offsetX.coerceIn(-maxX, 0f)
        offsetY = offsetY.coerceIn(-maxY, 0f)
    }

    companion object {
        const val MIN = 1f
        const val MAX = 4f
        const val DOUBLE_TAP = 2.5f
        private val RENDER_STEPS = listOf(1f, 1.5f, 2f, 2.5f, 3f, 3.5f)
    }
}

@Composable
fun rememberReaderZoomState(): ReaderZoomState {
    val spec = nebSpatialSpec<Float>()
    return remember { ReaderZoomState(spec) }
}

/** Applies the zoom to the content it modifies. */
fun Modifier.zoomed(state: ReaderZoomState): Modifier = graphicsLayer {
    transformOrigin = TransformOrigin(0f, 0f)
    scaleX = state.scale
    scaleY = state.scale
    translationX = state.offsetX
    translationY = state.offsetY
}

/**
 * Pinch, pan and double-tap. Gestures are read in the Initial pass so a pinch never reaches the
 * list below; single-finger drags at 1x are left alone so normal scrolling and paging keep
 * their own physics. [scrollBy] receives vertical movement while zoomed (scrolling layout) and
 * is null in the paged layout, where the page itself moves.
 */
fun Modifier.zoomGestures(
    state: ReaderZoomState,
    scope: CoroutineScope,
    onTap: () -> Unit,
    scrollBy: ((Float) -> Unit)?,
    flingBy: (suspend (Float) -> Unit)?
): Modifier = this
    .pointerInput(state, scrollBy) {
        val lockY = scrollBy == null
        awaitEachGesture {
            awaitFirstDown(requireUnconsumed = false, pass = PointerEventPass.Initial)
            val tracker = VelocityTracker()
            var panned = false
            do {
                val event = awaitPointerEvent(PointerEventPass.Initial)
                val pressed = event.changes.count { it.pressed }
                if (pressed >= 2) {
                    state.transform(event.calculateCentroid(), event.calculateZoom(), event.calculatePan(), scrollBy)
                    event.changes.forEach { it.consume() }
                    panned = false
                } else if (state.isZoomed) {
                    val change = event.changes.firstOrNull { it.pressed } ?: break
                    val delta = change.positionChange()
                    if (delta != Offset.Zero) {
                        val leftover = state.pan(delta, moveY = lockY)
                        if (!lockY) scrollBy?.invoke(-leftover / state.scale)
                        tracker.addPosition(change.uptimeMillis, change.position)
                        panned = true
                        change.consume()
                    }
                }
            } while (event.changes.any { it.pressed })
            state.settle()
            if (panned && !lockY && flingBy != null) {
                val velocity = tracker.calculateVelocity().y
                if (abs(velocity) > 300f) scope.launch { flingBy(-velocity / state.scale) }
            }
        }
    }
    .pointerInput(state) {
        detectTapGestures(
            onTap = { onTap() },
            onDoubleTap = { focus ->
                scope.launch {
                    val target = if (state.isZoomed) 1f else ReaderZoomState.DOUBLE_TAP
                    state.animateTo(target, focus, scrollBy)
                }
            }
        )
    }

/** A decaying fling for a list driven by [scrollBy], used while zoomed in. */
suspend fun decayFling(velocity: Float, scrollBy: (Float) -> Float) {
    var last = 0f
    AnimationState(initialValue = 0f, initialVelocity = velocity).animateDecay(exponentialDecay()) {
        val delta = value - last
        last = value
        if (abs(delta) > 0.5f && abs(scrollBy(delta)) < 0.5f) cancelAnimation()
    }
}
