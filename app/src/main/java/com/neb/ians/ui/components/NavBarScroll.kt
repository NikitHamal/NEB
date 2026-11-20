package com.neb.ians.ui.components

import androidx.compose.animation.core.animate
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Job
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Stable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.nestedscroll.NestedScrollConnection
import androidx.compose.ui.input.nestedscroll.NestedScrollSource
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Velocity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

/**
 * Hide on scroll down, return on scroll up, for the floating bottom bar. One connection sits above the whole
 * screen, so Home, Library and Notes (any vertical scroller below it) drive the same bar. The bar follows the
 * finger, then a spring settles it fully shown or fully hidden. Only the layer transform changes while it
 * moves, so nothing recomposes or re-measures per frame.
 */
@Stable
class NavBarScroll internal constructor(private val scope: CoroutineScope, internal val travelPx: Float) {
    private var offset by mutableFloatStateOf(0f)
    private var job: Job? = null

    /** 0 = shown, 1 = hidden. Read it only in a draw or layer block. */
    val hidden: Float get() = if (travelPx <= 0f) 0f else (offset / travelPx).coerceIn(0f, 1f)

    private fun animateTo(target: Float) {
        val clamped = target.coerceIn(0f, travelPx)
        if (kotlin.math.abs(offset - clamped) < 0.5f) {
            job?.cancel()
            job = null
            if (offset != clamped) offset = clamped
            return
        }
        job?.cancel()
        job = scope.launch { animate(offset, clamped, 0f, spring(dampingRatio = 0.8f, stiffness = Spring.StiffnessMediumLow)) { v, _ -> offset = v } }
    }

    private fun set(v: Float) {
        val clamped = v.coerceIn(0f, travelPx)
        if (job != null) {
            job?.cancel()
            job = null
        }
        if (offset != clamped) offset = clamped
    }

    fun show() = animateTo(0f)
    private fun settle() = animateTo(if (offset > travelPx * 0.4f) travelPx else 0f)

    val connection = object : NestedScrollConnection {
        override fun onPreScroll(available: androidx.compose.ui.geometry.Offset, source: NestedScrollSource): androidx.compose.ui.geometry.Offset {
            val dy = available.y
            if (dy != 0f && kotlin.math.abs(dy) > kotlin.math.abs(available.x)) {
                if ((dy < 0f && offset < travelPx) || (dy > 0f && offset > 0f)) {
                    set(offset - dy)
                }
            }
            return androidx.compose.ui.geometry.Offset.Zero
        }

        override suspend fun onPostFling(consumed: Velocity, available: Velocity): Velocity {
            if (offset > 0f && offset < travelPx) settle()
            return Velocity.Zero
        }

        override fun onPostScroll(
            consumed: androidx.compose.ui.geometry.Offset,
            available: androidx.compose.ui.geometry.Offset,
            source: NestedScrollSource
        ): androidx.compose.ui.geometry.Offset {
            // list already at its top edge and still pulled down: bring the bar back
            if (available.y > 0f && offset > 0f) set(offset - available.y)
            return androidx.compose.ui.geometry.Offset.Zero
        }
    }
}

@Composable
fun rememberNavBarScroll(travelDp: Float = 120f): NavBarScroll {
    val scope = rememberCoroutineScope()
    val px = with(LocalDensity.current) { travelDp.dp.toPx() }
    return remember(scope, px) { NavBarScroll(scope, px) }
}

/** The bar slides down and fades as [state] hides it; [pinned] keeps it in place (open menu). */
fun Modifier.navBarScrollTransform(state: NavBarScroll, pinned: Boolean = false): Modifier =
    graphicsLayer {
        val h = if (pinned) 0f else state.hidden
        translationY = h * state.travelPx
        alpha = (1f - h).coerceIn(0f, 1f)
    }

fun Modifier.navBarScrollSource(state: NavBarScroll): Modifier = nestedScroll(state.connection)
