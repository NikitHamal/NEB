package com.neb.ians.ui.components

import android.content.res.Resources
import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.gestures.FlingBehavior
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.layout

/**
 * Gives the child a finite max width when an ancestor passed an infinite one (a scroller above, a wrap-content
 * parent, an intrinsic probe). A horizontal scroller measured with an infinite width throws, which is a crash
 * report we have had; this keeps it a layout that merely scrolls. Never remove it from [nebHorizontalScroll].
 */
fun Modifier.boundedWidth(): Modifier = layout { measurable, constraints ->
    val bounded = if (constraints.hasBoundedWidth) constraints
    else constraints.copy(maxWidth = maxOf(constraints.minWidth, Resources.getSystem().displayMetrics.widthPixels))
    val placeable = measurable.measure(bounded)
    layout(placeable.width, placeable.height) { placeable.place(0, 0) }
}

/** The only horizontal scroller the app uses: `horizontalScroll` behind a width guard. */
fun Modifier.nebHorizontalScroll(
    state: ScrollState,
    enabled: Boolean = true,
    flingBehavior: FlingBehavior? = null,
    reverseScrolling: Boolean = false,
): Modifier = boundedWidth().horizontalScroll(state, enabled, flingBehavior, reverseScrolling)
