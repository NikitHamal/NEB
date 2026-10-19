package com.neb.ians.ui.screens.reader.pdf

import android.graphics.Bitmap
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.ViewAgenda
import androidx.compose.material.icons.outlined.ViewCarousel
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebSegment
import com.neb.ians.ui.components.NebSegmentedChoice
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.nebPressable

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReaderOptionsSheet(
    theme: ReadingTheme,
    layout: ReadingLayout,
    keepScreenOn: Boolean,
    onTheme: (ReadingTheme) -> Unit,
    onLayout: (ReadingLayout) -> Unit,
    onKeepScreenOn: (Boolean) -> Unit,
    onDismiss: () -> Unit
) {
    NebModalSheet(onDismiss = onDismiss, title = "Reading options") {
        Column(Modifier.padding(horizontal = 22.dp), verticalArrangement = Arrangement.spacedBy(20.dp)) {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                OptionLabel("Page colour")
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    ThemeTile("Paper", Color.White, Color(0xFF1B1B1B), theme == ReadingTheme.Paper, Modifier.weight(1f)) { onTheme(ReadingTheme.Paper) }
                    ThemeTile("Sepia", Color(0xFFF4ECD8), Color(0xFF3B2F23), theme == ReadingTheme.Sepia, Modifier.weight(1f)) { onTheme(ReadingTheme.Sepia) }
                    ThemeTile("Night", Color(0xFF141414), Color(0xFFDADADA), theme == ReadingTheme.Night, Modifier.weight(1f)) { onTheme(ReadingTheme.Night) }
                }
            }
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                OptionLabel("Layout")
                NebSegmentedChoice(
                    segments = listOf(
                        NebSegment(ReadingLayout.Scroll.name, "Scroll", Icons.Outlined.ViewAgenda),
                        NebSegment(ReadingLayout.Pages.name, "Page by page", Icons.Outlined.ViewCarousel)
                    ),
                    selected = layout.name,
                    onSelect = { onLayout(ReadingLayout.valueOf(it)) },
                    minHeight = 48.dp
                )
            }
            NebToggleRow(
                title = "Keep screen on",
                subtitle = "The screen stays awake while this document is open",
                checked = keepScreenOn,
                onCheckedChange = onKeepScreenOn
            )
        }
    }
}

@Composable
private fun OptionLabel(text: String) {
    Text(text, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
}

@Composable
private fun ThemeTile(label: String, paper: Color, ink: Color, selected: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val shape = RoundedCornerShape(16.dp)
    Column(
        modifier
            .clip(shape)
            .border(
                width = if (selected) 2.dp else 1.dp,
                color = if (selected) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.outlineVariant,
                shape = shape
            )
            .background(paper)
            .nebPressable(onClick = onClick)
            .padding(vertical = 14.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text("Aa", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold, color = ink)
        Text(label, style = MaterialTheme.typography.labelMedium, color = ink.copy(alpha = 0.75f))
    }
}

@Composable
private fun Thumbnail(index: Int, aspect: Float, look: ReaderLook, load: suspend (Int) -> Bitmap?, modifier: Modifier) {
    val bitmap by produceState<Bitmap?>(null, index) { value = load(index) }
    val image = remember(bitmap) { bitmap?.asImageBitmap() }
    Box(modifier.aspectRatio(1f / aspect.coerceAtLeast(0.1f)).background(look.paper)) {
        if (image != null) {
            Image(image, null, Modifier.fillMaxSize(), contentScale = ContentScale.FillBounds, colorFilter = look.filter)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ThumbnailsSheet(
    aspects: List<Float>,
    current: Int,
    bookmarks: Set<Int>,
    look: ReaderLook,
    load: suspend (Int) -> Bitmap?,
    onPick: (Int) -> Unit,
    onDismiss: () -> Unit
) {
    NebModalSheet(onDismiss = onDismiss, title = "All pages", subtitle = "${aspects.size} pages") {
        val gridState = rememberLazyGridState(initialFirstVisibleItemIndex = (current - 3).coerceAtLeast(0))
        LazyVerticalGrid(
            columns = GridCells.Adaptive(96.dp),
            state = gridState,
            modifier = Modifier.fillMaxWidth().heightIn(max = 560.dp),
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            items(count = aspects.size, key = { it }) { index ->
                val selected = index == current
                Column(
                    Modifier.nebPressable(onClick = { onPick(index) }),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box {
                        Thumbnail(
                            index, aspects[index], look, load,
                            Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(6.dp))
                                .border(
                                    if (selected) 2.dp else 1.dp,
                                    if (selected) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.outlineVariant,
                                    RoundedCornerShape(6.dp)
                                )
                        )
                        if (index in bookmarks) BookmarkFlag(Modifier.align(Alignment.TopEnd).padding(end = 8.dp))
                    }
                    Spacer(Modifier.height(6.dp))
                    Text(
                        "${index + 1}",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal,
                        color = if (selected) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun BookmarkFlag(modifier: Modifier = Modifier, width: Dp = 10.dp) {
    Box(
        modifier
            .size(width = width, height = width * 1.5f)
            .clip(RoundedCornerShape(bottomStart = 3.dp, bottomEnd = 3.dp))
            .background(MaterialTheme.colorScheme.onSurface)
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BookmarksSheet(
    bookmarks: Set<Int>,
    aspects: List<Float>,
    look: ReaderLook,
    load: suspend (Int) -> Bitmap?,
    onPick: (Int) -> Unit,
    onRemove: (Int) -> Unit,
    onDismiss: () -> Unit
) {
    val pages = remember(bookmarks) { bookmarks.filter { it in aspects.indices }.sorted() }
    NebModalSheet(onDismiss = onDismiss, title = "Bookmarks") {
        if (pages.isEmpty()) {
            NebEmptyState(
                icon = Icons.Outlined.BookmarkBorder,
                title = "No bookmarks yet",
                subtitle = "Tap the bookmark at the top to keep a page here.",
                modifier = Modifier.fillMaxWidth().padding(vertical = 24.dp)
            )
        } else {
            LazyColumn(Modifier.fillMaxWidth().heightIn(max = 520.dp)) {
                items(pages, key = { it }) { page ->
                    Row(
                        Modifier
                            .fillMaxWidth()
                            .nebPressable(onClick = { onPick(page) })
                            .padding(horizontal = 22.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Thumbnail(
                            page, aspects[page], look, load,
                            Modifier
                                .width(44.dp)
                                .clip(RoundedCornerShape(4.dp))
                                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(4.dp))
                        )
                        Text(
                            "Page ${page + 1}",
                            style = MaterialTheme.typography.titleSmall,
                            modifier = Modifier.weight(1f).padding(horizontal = 16.dp)
                        )
                        NebIconButton(Icons.Outlined.Close, "Remove bookmark", { onRemove(page) })
                    }
                }
            }
        }
    }
}

@Composable
fun GoToPageDialog(pageCount: Int, current: Int, onGo: (Int) -> Unit, onDismiss: () -> Unit) {
    var text by remember { mutableStateOf("") }
    val target = text.toIntOrNull()
    val valid = target != null && target in 1..pageCount
    NebDialog(
        onDismissRequest = onDismiss,
        title = "Go to page",
        supportingText = "You are on page ${current + 1} of $pageCount.",
        confirm = NebDialogAction("Go", onClick = { if (valid) onGo(target!! - 1) }, enabled = valid),
        dismiss = NebDialogAction("Cancel", onClick = onDismiss)
    ) {
        NebDialogTextField(
            value = text,
            onValueChange = { value -> text = value.filter(Char::isDigit).take(5) },
            placeholder = "1 to $pageCount",
            isError = text.isNotEmpty() && !valid,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
        )
    }
}
