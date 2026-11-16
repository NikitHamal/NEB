package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.unit.Dp

/**
 * A scrolling Pathways page that keeps the status bar readable. At the top the page (a tinted hero, say) runs under
 * the bar as designed; as it scrolls, a flat strip of the page colour fades in over the bar so text and buttons never
 * slide up under the clock and icons. The strip is part of the page, so it travels with it during a transition.
 */
@Composable
internal fun PwScrollPage(bottom: Dp, content: @Composable ColumnScope.() -> Unit) {
    val state = rememberScrollState()
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(state).padding(bottom = bottom), content = content)
        Box(
            Modifier.align(Alignment.TopStart).fillMaxWidth().windowInsetsTopHeight(WindowInsets.statusBars)
                .graphicsLayer { alpha = (state.value / (size.height * 0.6f).coerceAtLeast(1f)).coerceIn(0f, 1f) }
                .background(MaterialTheme.colorScheme.surface),
        )
    }
}

/** The same strip for a lazy list: clear while the first row is at the top, solid once the list has moved. */
@Composable
internal fun BoxScope.PwLazyScrim(state: androidx.compose.foundation.lazy.LazyListState) {
    Box(
        Modifier.align(Alignment.TopStart).fillMaxWidth().windowInsetsTopHeight(WindowInsets.statusBars)
            .graphicsLayer {
                alpha = if (state.firstVisibleItemIndex > 0) 1f else (state.firstVisibleItemScrollOffset / (size.height * 0.6f).coerceAtLeast(1f)).coerceIn(0f, 1f)
            }
            .background(MaterialTheme.colorScheme.surface),
    )
}
