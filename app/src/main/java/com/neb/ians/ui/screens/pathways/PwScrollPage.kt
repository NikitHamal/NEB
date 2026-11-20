package com.neb.ians.ui.screens.pathways

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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * A scrolling Pathways page. When [topBar] is provided, the top bar stays sticky at the top of the screen
 * and receives the scroll progress (0f..1f) so a 1dp outlineVariant hairline fades in when content scrolls under it.
 * When [topBar] is null (detail pages with a tonal hero), a status-bar scrim and optional sticky hero bar are used.
 */
@Composable
internal fun PwScrollPage(
    bottom: Dp,
    topBar: (@Composable (scrolled: () -> Float) -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit,
) {
    val state = rememberScrollState()
    if (topBar != null) {
        Column(Modifier.fillMaxSize()) {
            topBar { (state.value / 24f).coerceIn(0f, 1f) }
            Column(Modifier.weight(1f).fillMaxWidth().verticalScroll(state).padding(bottom = bottom), content = content)
        }
        return
    }
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(state).padding(bottom = bottom), content = content)
        Box(
            Modifier.align(Alignment.TopStart).fillMaxWidth().windowInsetsTopHeight(WindowInsets.statusBars)
                .graphicsLayer { alpha = (state.value / (size.height * 0.6f).coerceAtLeast(1f)).coerceIn(0f, 1f) }
                .background(MaterialTheme.colorScheme.surface),
        )
    }
}

/**
 * Detail page with a tonal [PwHero] header at the top and a sticky compact top bar that fades in
 * as the hero scrolls off-screen, keeping Back, Title and Save reachable at all times (like ProfileTopBar).
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
    content: @Composable ColumnScope.() -> Unit,
) {
    val state = rememberScrollState()
    val c = MaterialTheme.colorScheme
    val progress: () -> Float = { ((state.value - 80f) / 90f).coerceIn(0f, 1f) }
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(state).padding(bottom = bottom)) {
            PwHero(tone, title, sub, badge)
            content()
        }
        Box(Modifier.align(Alignment.TopCenter).fillMaxWidth()) {
            Box(Modifier.matchParentSize().graphicsLayer { alpha = progress() }.background(c.surface))
            Box(
                Modifier.align(Alignment.BottomCenter).fillMaxWidth().height(1.dp)
                    .graphicsLayer { alpha = progress() }.background(c.outlineVariant)
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
