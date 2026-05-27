package com.neb.ians.ui.reader

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.outlined.FormatUnderlined
import androidx.compose.material.icons.outlined.Highlight
import androidx.compose.material.icons.outlined.StickyNote2
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Delete
import androidx.compose.material.icons.rounded.MenuBook
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.AssistChip
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilledIconToggleButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.local.AnnotationEntity
import com.neb.ians.data.local.AnnotationKind
import com.neb.ians.ui.common.EmptyState

@Composable
fun PdfReaderScreen(
    resourceId: Long,
    onBack: () -> Unit,
    vm: PdfReaderViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsState()
    val annotations by vm.annotationsFlow.collectAsState()
    val resource = state.resource

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        resource?.title ?: "Reader",
                        style = MaterialTheme.typography.titleMedium,
                        maxLines = 1,
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                ),
            )
        },
        bottomBar = { AnnotationToolbar(state.tool, vm::setTool) },
    ) { inner ->
        if (!state.ready) {
            Box(Modifier.fillMaxSize().padding(inner), contentAlignment = Alignment.Center) {
                if (resource == null) {
                    EmptyState(
                        title = "Resource not found",
                        body = "It may have been removed.",
                        icon = Icons.Rounded.MenuBook,
                    )
                } else {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator()
                        Spacer(Modifier.height(12.dp))
                        Text("Preparing for offline reading…", style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
            return@Scaffold
        }

        val listState = rememberLazyListState()
        var noteDialogFor by remember { mutableStateOf<AnnotationEntity?>(null) }

        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize().padding(inner),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            items((0 until state.pageCount).toList(), key = { it }) { pageIdx ->
                PdfPage(
                    pageIndex = pageIdx,
                    totalPages = state.pageCount,
                    annotations = annotations.filter { it.page == pageIdx },
                    tool = state.tool,
                    onRender = { w -> vm.renderPage(pageIdx, w) },
                    onAddAnnotation = { x, y, w, h, note -> vm.addAnnotation(pageIdx, x, y, w, h, note) },
                    onTapAnnotation = { ann ->
                        if (ann.kind == AnnotationKind.StickyNote) noteDialogFor = ann
                    },
                    onLongPressAnnotation = { ann -> vm.removeAnnotation(ann.id) },
                )
            }
        }

        noteDialogFor?.let { ann ->
            var draft by remember(ann.id) { mutableStateOf(ann.note.orEmpty()) }
            AlertDialog(
                onDismissRequest = { noteDialogFor = null },
                confirmButton = {
                    TextButton(onClick = {
                        vm.updateNote(ann, draft)
                        noteDialogFor = null
                    }) { Text("Save") }
                },
                dismissButton = {
                    TextButton(onClick = {
                        vm.removeAnnotation(ann.id); noteDialogFor = null
                    }) {
                        Icon(Icons.Rounded.Delete, contentDescription = null)
                        Spacer(Modifier.width(6.dp))
                        Text("Delete")
                    }
                },
                title = { Text("Note") },
                text = {
                    OutlinedTextField(
                        value = draft,
                        onValueChange = { draft = it },
                        modifier = Modifier.fillMaxWidth().height(120.dp),
                        placeholder = { Text("Write a sticky note for this spot…") },
                    )
                },
            )
        }
    }
}

@Composable
private fun PdfPage(
    pageIndex: Int,
    totalPages: Int,
    annotations: List<AnnotationEntity>,
    tool: ToolMode,
    onRender: suspend (widthPx: Int) -> android.graphics.Bitmap?,
    onAddAnnotation: (xPct: Float, yPct: Float, wPct: Float, hPct: Float, note: String?) -> Unit,
    onTapAnnotation: (AnnotationEntity) -> Unit,
    onLongPressAnnotation: (AnnotationEntity) -> Unit,
) {
    val density = LocalDensity.current
    val targetWidthPx = with(density) { 1000.dp.roundToPx().coerceAtMost(1600) }
    val bitmap by produceState<android.graphics.Bitmap?>(null, pageIndex) {
        value = onRender(targetWidthPx)
    }

    Surface(
        shape = RoundedCornerShape(14.dp),
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 0.dp,
        modifier = Modifier.fillMaxWidth(),
    ) {
        Box(
            Modifier.fillMaxWidth()
                .aspectRatio(0.707f)
                .clip(RoundedCornerShape(14.dp))
                .background(Color.White)
                .pointerInput(tool, pageIndex) {
                    detectTapGestures(
                        onTap = { offset ->
                            if (tool == ToolMode.None) return@detectTapGestures
                            val x = (offset.x / size.width).coerceIn(0f, 1f)
                            val y = (offset.y / size.height).coerceIn(0f, 1f)
                            when (tool) {
                                ToolMode.StickyNote ->
                                    onAddAnnotation(x - 0.02f, y - 0.02f, 0.04f, 0.04f, "")
                                ToolMode.Highlight ->
                                    onAddAnnotation(x - 0.1f, y - 0.01f, 0.2f, 0.025f, null)
                                ToolMode.Underline ->
                                    onAddAnnotation(x - 0.1f, y - 0.001f, 0.2f, 0.005f, null)
                                ToolMode.None -> Unit
                            }
                        },
                    )
                },
        ) {
            bitmap?.let { bmp ->
                Image(
                    bitmap = bmp.asImageBitmap(),
                    contentDescription = "Page ${pageIndex + 1}",
                    modifier = Modifier.fillMaxSize(),
                )
            } ?: Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }

            // Annotation overlays — % coordinates so they stay locked to the page.
            annotations.forEach { ann ->
                AnnotationOverlay(
                    ann = ann,
                    onTap = { onTapAnnotation(ann) },
                    onLongPress = { onLongPressAnnotation(ann) },
                )
            }

            // Page chip
            Surface(
                color = Color.Black.copy(alpha = 0.55f),
                shape = RoundedCornerShape(8.dp),
                modifier = Modifier.padding(8.dp).align(Alignment.BottomEnd),
            ) {
                Text(
                    "${pageIndex + 1} / $totalPages",
                    color = Color.White,
                    style = MaterialTheme.typography.labelSmall,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                )
            }
        }
    }
}

@Composable
private fun AnnotationOverlay(
    ann: AnnotationEntity,
    onTap: () -> Unit,
    onLongPress: () -> Unit,
) {
    val color = Color(ann.color.toInt())
    androidx.compose.foundation.layout.BoxWithConstraints(
        Modifier
            .fillMaxSize()
            .pointerInput(ann.id) {
                detectTapGestures(
                    onTap = { onTap() },
                    onLongPress = { onLongPress() },
                )
            }
    ) {
        val parentW = maxWidth
        val parentH = maxHeight
        val x = parentW * ann.xPct.coerceAtLeast(0f)
        val y = parentH * ann.yPct.coerceAtLeast(0f)
        val w = parentW * ann.widthPct.coerceAtLeast(0f)
        val h = parentH * ann.heightPct.coerceAtLeast(0f)
        when (ann.kind) {
            AnnotationKind.Highlight -> Box(
                Modifier
                    .padding(start = x, top = y)
                    .width(w)
                    .height(h)
                    .background(color.copy(alpha = 0.4f), RoundedCornerShape(2.dp)),
            )
            AnnotationKind.Underline -> Box(
                Modifier
                    .padding(start = x, top = y)
                    .width(w)
                    .height(h.coerceAtLeast(2.dp))
                    .background(color, RoundedCornerShape(1.dp)),
            )
            AnnotationKind.StickyNote -> Surface(
                color = color,
                shape = RoundedCornerShape(50),
                modifier = Modifier
                    .padding(start = x, top = y)
                    .width(20.dp)
                    .height(20.dp),
            ) {}
        }
    }
}

@Composable
private fun AnnotationToolbar(tool: ToolMode, onChange: (ToolMode) -> Unit) {
    Surface(
        tonalElevation = 0.dp,
        color = MaterialTheme.colorScheme.surface,
    ) {
        Column {
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                ToolToggle(
                    selected = tool == ToolMode.Highlight,
                    onClick = { onChange(ToolMode.Highlight) },
                    icon = Icons.Outlined.Highlight,
                    label = "Highlight",
                )
                ToolToggle(
                    selected = tool == ToolMode.Underline,
                    onClick = { onChange(ToolMode.Underline) },
                    icon = Icons.Outlined.FormatUnderlined,
                    label = "Underline",
                )
                ToolToggle(
                    selected = tool == ToolMode.StickyNote,
                    onClick = { onChange(ToolMode.StickyNote) },
                    icon = Icons.Outlined.StickyNote2,
                    label = "Note",
                )
                Spacer(Modifier.weight(1f))
                if (tool != ToolMode.None) {
                    AssistChip(
                        onClick = { onChange(ToolMode.None) },
                        label = { Text("Done") },
                        leadingIcon = { Icon(Icons.Rounded.Close, contentDescription = null) },
                    )
                }
            }
        }
    }
}

@Composable
private fun ToolToggle(
    selected: Boolean,
    onClick: () -> Unit,
    icon: ImageVector,
    label: String,
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        FilledIconToggleButton(
            checked = selected,
            onCheckedChange = { onClick() },
            colors = IconButtonDefaults.filledIconToggleButtonColors(),
        ) { Icon(icon, contentDescription = label) }
        Text(label, style = MaterialTheme.typography.labelSmall)
    }
}
