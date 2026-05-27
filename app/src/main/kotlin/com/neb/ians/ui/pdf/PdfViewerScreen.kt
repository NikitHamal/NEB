package com.neb.ians.ui.pdf

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.FormatColorFill
import androidx.compose.material.icons.outlined.FormatUnderlined
import androidx.compose.material.icons.outlined.NoteAdd
import androidx.compose.material.icons.outlined.PanTool
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.db.AnnotationEntity
import java.io.File

enum class AnnotationTool { PAN, HIGHLIGHT, UNDERLINE, NOTE }

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfViewerScreen(
    resourceId: String,
    localPath: String,
    title: String,
    onBack: () -> Unit,
    vm: PdfViewerViewModel = hiltViewModel(),
) {
    val annotations by vm.annotations.collectAsStateWithLifecycle()
    var tool by remember { mutableStateOf(AnnotationTool.PAN) }
    var pendingNote by remember { mutableStateOf<PendingNote?>(null) }

    LaunchedEffect(resourceId) { vm.load(resourceId) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(title, maxLines = 1) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),
            )
        },
        bottomBar = {
            AnnotationToolbar(selected = tool, onSelect = { tool = it })
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            PdfPagesList(
                localPath = localPath,
                annotations = annotations,
                tool = tool,
                onAddRectAnnotation = { page, rect, kind ->
                    vm.addRectAnnotation(resourceId, page, rect, kind)
                },
                onAddNote = { page, point ->
                    pendingNote = PendingNote(page, point)
                },
            )
        }
    }

    pendingNote?.let { p ->
        var noteText by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { pendingNote = null },
            confirmButton = {
                TextButton(onClick = {
                    if (noteText.isNotBlank()) vm.addNote(resourceId, p.page, p.point, noteText)
                    pendingNote = null
                }) { Text("Save") }
            },
            dismissButton = { TextButton(onClick = { pendingNote = null }) { Text("Cancel") } },
            title = { Text("Sticky note") },
            text = {
                OutlinedTextField(
                    value = noteText,
                    onValueChange = { noteText = it },
                    placeholder = { Text("Write your note") },
                )
            }
        )
    }
}

private data class PendingNote(val page: Int, val point: Offset)

@Composable
private fun AnnotationToolbar(selected: AnnotationTool, onSelect: (AnnotationTool) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surface)
            .padding(horizontal = 12.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceAround,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        ToolChip("Pan", Icons.Outlined.PanTool, selected == AnnotationTool.PAN) { onSelect(AnnotationTool.PAN) }
        ToolChip("Highlight", Icons.Outlined.FormatColorFill, selected == AnnotationTool.HIGHLIGHT) { onSelect(AnnotationTool.HIGHLIGHT) }
        ToolChip("Underline", Icons.Outlined.FormatUnderlined, selected == AnnotationTool.UNDERLINE) { onSelect(AnnotationTool.UNDERLINE) }
        ToolChip("Note", Icons.Outlined.NoteAdd, selected == AnnotationTool.NOTE) { onSelect(AnnotationTool.NOTE) }
    }
}

@Composable
private fun ToolChip(label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, selected: Boolean, onClick: () -> Unit) {
    FilterChip(
        selected = selected,
        onClick = onClick,
        label = { Text(label, fontSize = 12.sp) },
        leadingIcon = { Icon(icon, contentDescription = null) },
        shape = MaterialTheme.shapes.medium,
    )
}

@Composable
private fun PdfPagesList(
    localPath: String,
    annotations: List<AnnotationEntity>,
    tool: AnnotationTool,
    onAddRectAnnotation: (page: Int, rect: Rect, kind: String) -> Unit,
    onAddNote: (page: Int, point: Offset) -> Unit,
) {
    val file = remember(localPath) { File(localPath) }
    val rendererState = remember(localPath) { PdfRendererState.open(file) }

    DisposableEffect(rendererState) {
        onDispose { rendererState?.close() }
    }

    if (rendererState == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("Could not open document.", style = MaterialTheme.typography.bodyMedium)
        }
        return
    }

    val pageCount = rendererState.pageCount
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 12.dp, horizontal = 12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        itemsIndexed((0 until pageCount).toList(), key = { _, i -> i }) { _, pageIndex ->
            PdfPage(
                rendererState = rendererState,
                pageIndex = pageIndex,
                annotations = annotations.filter { it.page == pageIndex },
                tool = tool,
                onAddRectAnnotation = { rect, kind -> onAddRectAnnotation(pageIndex, rect, kind) },
                onAddNote = { point -> onAddNote(pageIndex, point) },
            )
        }
    }
}

@Composable
private fun PdfPage(
    rendererState: PdfRendererState,
    pageIndex: Int,
    annotations: List<AnnotationEntity>,
    tool: AnnotationTool,
    onAddRectAnnotation: (Rect, String) -> Unit,
    onAddNote: (Offset) -> Unit,
) {
    val bitmap = remember(pageIndex) { rendererState.renderPage(pageIndex) }
    val imageBitmap = remember(bitmap) { bitmap.asImageBitmap() }
    val ratio = remember(pageIndex) { bitmap.width.toFloat() / bitmap.height.toFloat() }
    var draftRect by remember { mutableStateOf<Rect?>(null) }

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(ratio)
            .background(Color.White)
    ) {
        val widthPx = constraints.maxWidth.toFloat()
        val heightPx = constraints.maxHeight.toFloat()

        Image(
            bitmap = imageBitmap,
            contentDescription = null,
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.FillBounds,
        )

        Canvas(modifier = Modifier.fillMaxSize()) {
            val size = Size(widthPx, heightPx)
            annotations.forEach { ann ->
                val r = ann.toRect(size) ?: return@forEach
                when (ann.kind) {
                    "HIGHLIGHT" -> drawRect(
                        Color(ann.color).copy(alpha = 0.35f),
                        topLeft = Offset(r.left, r.top),
                        size = androidx.compose.ui.geometry.Size(r.width, r.height),
                    )
                    "UNDERLINE" -> drawLine(
                        color = Color(ann.color),
                        start = Offset(r.left, r.bottom),
                        end = Offset(r.right, r.bottom),
                        strokeWidth = 4f,
                    )
                    "NOTE" -> {
                        val center = Offset(r.left, r.top)
                        drawCircle(Color(ann.color), radius = 14f, center = center)
                        drawCircle(Color.White, radius = 14f, center = center, style = Stroke(width = 2f))
                    }
                }
            }
            draftRect?.let { dr ->
                drawRect(
                    Color(0xFFFFEB3B).copy(alpha = 0.3f),
                    topLeft = Offset(dr.left, dr.top),
                    size = androidx.compose.ui.geometry.Size(dr.width, dr.height),
                )
            }
        }

        Box(
            modifier = Modifier
                .fillMaxSize()
                .pointerInput(tool, pageIndex) {
                    when (tool) {
                        AnnotationTool.NOTE -> {
                            awaitPointerEventScope {
                                while (true) {
                                    val ev = awaitPointerEvent()
                                    val p = ev.changes.firstOrNull() ?: continue
                                    if (p.pressed) {
                                        onAddNote(Offset(p.position.x / widthPx, p.position.y / heightPx))
                                        p.consume()
                                    }
                                }
                            }
                        }
                        AnnotationTool.HIGHLIGHT, AnnotationTool.UNDERLINE -> {
                            awaitPointerEventScope {
                                while (true) {
                                    val down = awaitPointerEvent()
                                    val pc = down.changes.firstOrNull() ?: continue
                                    if (!pc.pressed) continue
                                    pc.consume()
                                    val start = pc.position
                                    var current = start
                                    drag@ while (true) {
                                        val move = awaitPointerEvent()
                                        val mc = move.changes.firstOrNull() ?: break@drag
                                        current = mc.position
                                        draftRect = Rect(
                                            minOf(start.x, current.x),
                                            minOf(start.y, current.y),
                                            maxOf(start.x, current.x),
                                            maxOf(start.y, current.y),
                                        )
                                        mc.consume()
                                        if (!mc.pressed) break@drag
                                    }
                                    draftRect?.let { r ->
                                        if (r.width > 6f && r.height > 4f) {
                                            val normalized = Rect(
                                                r.left / widthPx, r.top / heightPx,
                                                r.right / widthPx, r.bottom / heightPx,
                                            )
                                            val kind = if (tool == AnnotationTool.HIGHLIGHT) "HIGHLIGHT" else "UNDERLINE"
                                            onAddRectAnnotation(normalized, kind)
                                        }
                                    }
                                    draftRect = null
                                }
                            }
                        }
                        AnnotationTool.PAN -> { /* parent LazyColumn handles scroll */ }
                    }
                }
        )
    }
}
