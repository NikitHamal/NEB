package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInParent
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * A scrolling Pathways page. When [topBar] is provided, the top bar (and optional [stickyHeader]
 * such as a segmented section bar or filter strip) stays sticky at the top of the screen
 * and receives the scroll progress (0f..1f) so a 1dp outlineVariant hairline fades in when content scrolls under it.
 */
@Composable
internal fun PwScrollPage(
    bottom: Dp,
    state: ScrollState = rememberScrollState(),
    topBar: (@Composable (scrolled: () -> Float) -> Unit)? = null,
    stickyHeader: (@Composable () -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit,
) {
    val c = MaterialTheme.colorScheme
    if (topBar != null) {
        val scrolled: () -> Float = { (state.value / 24f).coerceIn(0f, 1f) }
        Column(Modifier.fillMaxSize()) {
            topBar { if (stickyHeader != null) 0f else scrolled() }
            if (stickyHeader != null) {
                Column(Modifier.fillMaxWidth().background(c.surface)) {
                    stickyHeader()
                    Box(
                        Modifier.fillMaxWidth().height(1.dp)
                            .graphicsLayer { alpha = scrolled() }
                            .background(c.outlineVariant)
                    )
                }
            }
            Column(Modifier.weight(1f).fillMaxWidth().verticalScroll(state).padding(bottom = bottom), content = content)
        }
        return
    }
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(state).padding(bottom = bottom), content = content)
        Box(
            Modifier.align(Alignment.TopStart).fillMaxWidth().windowInsetsTopHeight(WindowInsets.statusBars)
                .graphicsLayer { alpha = (state.value / (size.height * 0.6f).coerceAtLeast(1f)).coerceIn(0f, 1f) }
                .background(c.surface),
        )
    }
}

/**
 * Detail page with a tonal [PwHero] header at the top, a sticky compact top bar that fades in
 * as the hero scrolls off-screen, and an optional [stickyTabs] bar that scrolls naturally with the
 * overview header until it reaches the bottom of the sticky top bar, where it pins cleanly (Google M3 standard).
 */
@Composable
internal fun PwHeroScrollPage(
    tone: PwTone,
    title: String,
    sub: String,
    saved: Boolean?,
    onSave: () -> Unit,
    onBack: () -> Unit,
    bottom: Dp,
    badge: @Composable () -> Unit,
    tabKey: Any? = null,
    aboveTabs: (@Composable ColumnScope.() -> Unit)? = null,
    stickyTabs: (@Composable () -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit,
) {
    val state = rememberScrollState()
    val c = MaterialTheme.colorScheme
    var topBarHeightPx by remember { mutableIntStateOf(0) }
    var tabsOffsetY by remember { mutableIntStateOf(0) }
    val progress: () -> Float = { ((state.value - 80f) / 90f).coerceIn(0f, 1f) }
    val isTabsPinned by remember {
        androidx.compose.runtime.derivedStateOf {
            stickyTabs != null && topBarHeightPx > 0 && tabsOffsetY > 0 && state.value >= (tabsOffsetY - topBarHeightPx)
        }
    }
    androidx.compose.runtime.LaunchedEffect(tabKey) {
        if (tabKey != null && topBarHeightPx > 0 && tabsOffsetY > 0) {
            val pinY = (tabsOffsetY - topBarHeightPx).coerceAtLeast(0)
            if (state.value > pinY) state.scrollTo(pinY)
        }
    }
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(state).padding(bottom = bottom)) {
            PwHero(tone, title, sub, badge)
            aboveTabs?.invoke(this)
            if (stickyTabs != null) {
                Box(
                    Modifier.fillMaxWidth()
                        .onGloballyPositioned { tabsOffsetY = it.positionInParent().y.toInt() }
                        .graphicsLayer { alpha = if (isTabsPinned) 0f else 1f }
                ) {
                    stickyTabs()
                }
            }
            content()
        }
        Column(Modifier.align(Alignment.TopCenter).fillMaxWidth()) {
            Box(
                Modifier.fillMaxWidth()
                    .onGloballyPositioned { topBarHeightPx = it.size.height }
            ) {
                Box(Modifier.matchParentSize().graphicsLayer { alpha = progress() }.background(c.surface))
                Box(
                    Modifier.align(Alignment.BottomCenter).fillMaxWidth().height(1.dp)
                        .graphicsLayer { alpha = if (isTabsPinned) 0f else progress() }
                        .background(c.outlineVariant)
                )
                Row(
                    Modifier.fillMaxWidth().statusBarsPadding().padding(16.dp, 10.dp, 16.dp, 10.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    PwIconButton(
                        Icons.AutoMirrored.Outlined.ArrowBack,
                        "Back",
                        onBack,
                        container = c.surface.copy(alpha = 0.86f),
                        tint = c.onSurface,
                    )
                    Text(
                        title,
                        Modifier.weight(1f).graphicsLayer {
                            val p = progress()
                            alpha = p
                            translationY = (1f - p) * 8.dp.toPx()
                        },
                        fontSize = 18.sp,
                        fontWeight = FontWeight.SemiBold,
                        letterSpacing = (-0.3).sp,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                    if (saved != null) {
                        PwIconButton(
                            if (saved) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder,
                            "Save",
                            onSave,
                            if (saved) c.onSurface else c.surface.copy(alpha = 0.86f),
                            if (saved) c.surface else c.onSurface,
                        )
                    }
                }
            }
            if (stickyTabs != null && isTabsPinned) {
                Box(Modifier.fillMaxWidth().background(c.surface)) {
                    stickyTabs()
                }
            }
        }
    }
}
