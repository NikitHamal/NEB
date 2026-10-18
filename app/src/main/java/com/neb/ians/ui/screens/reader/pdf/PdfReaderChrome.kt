package com.neb.ians.ui.screens.reader.pdf

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsIgnoringVisibility
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsIgnoringVisibility
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Bookmarks
import androidx.compose.material.icons.outlined.GridView
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlin.math.roundToInt

/** Height of each bar's content, not counting system insets. Pages pad by this much. */
val ReaderBarHeight = 60.dp

@Composable
internal fun barColor() = MaterialTheme.colorScheme.surface.copy(alpha = 0.97f)

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ReaderTopBar(
    visible: Boolean,
    title: String,
    page: Int,
    pageCount: Int,
    bookmarked: Boolean,
    onBack: () -> Unit,
    onToggleBookmark: () -> Unit,
    onOptions: () -> Unit,
    modifier: Modifier = Modifier,
    onSearch: (() -> Unit)? = null
) {
    AnimatedVisibility(
        visible = visible,
        modifier = modifier,
        enter = slideInVertically(nebSpatialSpec()) { -it } + fadeIn(nebEffectsSpec()),
        exit = slideOutVertically(nebSpatialSpec()) { -it } + fadeOut(nebEffectsSpec())
    ) {
        Column(Modifier.fillMaxWidth().background(barColor())) {
            Row(
                Modifier
                    .windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility)
                    .height(ReaderBarHeight)
                    .padding(horizontal = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack)
                Column(Modifier.weight(1f).padding(horizontal = 6.dp)) {
                    Text(
                        title.ifBlank { "Document" },
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    if (pageCount > 0) {
                        Text(
                            "Page ${page + 1} of $pageCount",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                NebIconButton(
                    if (bookmarked) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder,
                    if (bookmarked) "Remove bookmark" else "Bookmark this page",
                    onToggleBookmark,
                    tint = if (bookmarked) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant
                )
                if (onSearch != null) NebIconButton(Icons.Outlined.Search, "Search in document", onSearch)
                NebIconButton(Icons.Outlined.Tune, "Reading options", onOptions)
            }
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
        }
    }
}

@OptIn(ExperimentalLayoutApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ReaderBottomBar(
    visible: Boolean,
    page: Int,
    pageCount: Int,
    onGoToPage: () -> Unit,
    onSeek: (Int) -> Unit,
    onThumbnails: () -> Unit,
    onBookmarks: () -> Unit,
    modifier: Modifier = Modifier
) {
    AnimatedVisibility(
        visible = visible,
        modifier = modifier,
        enter = slideInVertically(nebSpatialSpec()) { it } + fadeIn(nebEffectsSpec()),
        exit = slideOutVertically(nebSpatialSpec()) { it } + fadeOut(nebEffectsSpec())
    ) {
        Column(Modifier.fillMaxWidth().background(barColor())) {
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
            Row(
                Modifier
                    .windowInsetsPadding(WindowInsets.navigationBarsIgnoringVisibility)
                    .height(ReaderBarHeight)
                    .padding(horizontal = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                var dragging by remember { mutableStateOf<Float?>(null) }
                val shown = dragging?.roundToInt() ?: page
                PageChip(label = "${shown + 1} / $pageCount", onClick = onGoToPage)
                Spacer(Modifier.width(8.dp))
                if (pageCount > 1) {
                    val ink = MaterialTheme.colorScheme.onSurface
                    Slider(
                        value = dragging ?: page.toFloat(),
                        onValueChange = { dragging = it },
                        onValueChangeFinished = {
                            dragging?.let { onSeek(it.roundToInt()) }
                            dragging = null
                        },
                        valueRange = 0f..(pageCount - 1).toFloat(),
                        colors = SliderDefaults.colors(
                            thumbColor = ink,
                            activeTrackColor = ink,
                            inactiveTrackColor = MaterialTheme.colorScheme.outlineVariant
                        ),
                        modifier = Modifier.weight(1f)
                    )
                } else {
                    Spacer(Modifier.weight(1f))
                }
                NebIconButton(Icons.Outlined.GridView, "All pages", onThumbnails)
                NebIconButton(Icons.Outlined.Bookmarks, "Bookmarks", onBookmarks)
            }
        }
    }
}

@Composable
private fun PageChip(label: String, onClick: () -> Unit) {
    Box(
        Modifier
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .nebPressable(onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 8.dp)
    ) {
        Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
    }
}

/** A hairline of reading progress, shown while the bars are hidden. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ReaderProgressLine(visible: Boolean, progress: Float, modifier: Modifier = Modifier) {
    AnimatedVisibility(visible, modifier, enter = fadeIn(nebEffectsSpec()), exit = fadeOut(nebEffectsSpec())) {
        Box(Modifier.fillMaxWidth().windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(2.dp)) {
            Box(
                Modifier
                    .fillMaxWidth(progress.coerceIn(0f, 1f))
                    .height(2.dp)
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.55f))
            )
        }
    }
}

/** A small "12 / 80" pill that shows briefly when the page changes with the bars hidden. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun FloatingPageBadge(visible: Boolean, page: Int, pageCount: Int, modifier: Modifier = Modifier) {
    AnimatedVisibility(visible, modifier, enter = fadeIn(nebEffectsSpec()), exit = fadeOut(nebEffectsSpec())) {
        Box(
            Modifier
                .windowInsetsPadding(WindowInsets.navigationBarsIgnoringVisibility)
                .padding(bottom = 18.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.inverseSurface.copy(alpha = 0.86f))
                .padding(horizontal = 14.dp, vertical = 6.dp)
        ) {
            Text(
                "${page + 1} / $pageCount",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.inverseOnSurface
            )
        }
    }
}
