package com.neb.ians.ui.screens.reader.pdf

import android.graphics.RectF
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsIgnoringVisibility
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.KeyboardArrowDown
import androidx.compose.material.icons.outlined.KeyboardArrowUp
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

/** One place a search term occurs: a page and a rectangle in page fractions. */
@Immutable
data class SearchHit(val page: Int, val rect: RectF)

/** In-document search: what was typed, how far the scan has got, and every hit so far. */
@Immutable
data class ReaderSearch(
    val open: Boolean = false,
    val query: String = "",
    val running: Boolean = false,
    val scanned: Int = 0,
    val hits: List<SearchHit> = emptyList(),
    val byPage: Map<Int, List<RectF>> = emptyMap(),
    val index: Int = -1,
    /** Bumped whenever the reader should move to the current hit. */
    val jump: Int = 0
) {
    val current: SearchHit? get() = hits.getOrNull(index)
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ReaderSearchBar(
    search: ReaderSearch,
    pageCount: Int,
    onQuery: (String) -> Unit,
    onPrev: () -> Unit,
    onNext: () -> Unit,
    onClose: () -> Unit,
    modifier: Modifier = Modifier
) {
    AnimatedVisibility(
        visible = search.open,
        modifier = modifier,
        enter = slideInVertically(nebSpatialSpec()) { -it } + fadeIn(nebEffectsSpec()),
        exit = slideOutVertically(nebSpatialSpec()) { -it } + fadeOut(nebEffectsSpec())
    ) {
        val focus = remember { FocusRequester() }
        LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
        Column(Modifier.fillMaxWidth().background(barColor())) {
            Row(
                Modifier
                    .windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility)
                    .height(ReaderBarHeight)
                    .padding(horizontal = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Close search", onClose)
                Box(Modifier.weight(1f).padding(horizontal = 6.dp), contentAlignment = Alignment.CenterStart) {
                    if (search.query.isEmpty()) {
                        Text("Search in this document", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    BasicTextField(
                        value = search.query,
                        onValueChange = onQuery,
                        singleLine = true,
                        textStyle = MaterialTheme.typography.bodyLarge.copy(color = MaterialTheme.colorScheme.onSurface),
                        cursorBrush = SolidColor(MaterialTheme.colorScheme.onSurface),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(onSearch = { onNext() }),
                        modifier = Modifier.fillMaxWidth().focusRequester(focus)
                    )
                }
                val label = when {
                    search.query.trim().length < 2 -> ""
                    search.hits.isNotEmpty() -> "${search.index + 1} / ${search.hits.size}${if (search.running) "+" else ""}"
                    search.running -> "…"
                    else -> "None"
                }
                Text(label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(horizontal = 4.dp))
                NebIconButton(Icons.Outlined.KeyboardArrowUp, "Previous match", onPrev)
                NebIconButton(Icons.Outlined.KeyboardArrowDown, "Next match", onNext)
            }
            if (search.running && pageCount > 0) {
                LinearProgressIndicator(
                    progress = { search.scanned / pageCount.toFloat() },
                    color = MaterialTheme.colorScheme.onSurface,
                    trackColor = Color.Transparent,
                    modifier = Modifier.fillMaxWidth().height(2.dp)
                )
            } else {
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
            }
        }
    }
}

private val MarkFill = Color(0x66FFC83D)
private val ActiveFill = Color(0x99FF9F1C)
private val ActiveEdge = Color(0xFFE07A00)

/** Draws search marks (rectangles in page fractions) over a page. */
fun Modifier.searchMarks(marks: List<RectF>, active: RectF?): Modifier =
    if (marks.isEmpty() && active == null) this else drawWithContent {
        drawContent()
        val pad = 1.5.dp.toPx()
        for (r in marks) {
            if (r === active) continue
            drawRoundRect(MarkFill, Offset(r.left * size.width - pad, r.top * size.height - pad), Size(r.width() * size.width + pad * 2, r.height() * size.height + pad * 2), CornerRadius(pad * 1.5f))
        }
        if (active != null) {
            val o = Offset(active.left * size.width - pad, active.top * size.height - pad)
            val s = Size(active.width() * size.width + pad * 2, active.height() * size.height + pad * 2)
            drawRoundRect(ActiveFill, o, s, CornerRadius(pad * 1.5f))
            drawRoundRect(ActiveEdge, o, s, CornerRadius(pad * 1.5f), style = Stroke(1.5.dp.toPx()))
        }
    }
