@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians

import android.graphics.Bitmap
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.automirrored.outlined.StickyNote2
import androidx.compose.material.icons.outlined.BorderColor
import androidx.compose.material.icons.outlined.DeleteSweep
import androidx.compose.material.icons.outlined.FormatUnderlined
import androidx.compose.material.icons.outlined.ZoomIn
import androidx.compose.material.icons.outlined.ZoomOut
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import java.io.File
import java.util.UUID
import kotlin.math.max
import kotlin.math.min
import kotlin.math.roundToInt

@Composable
fun PdfViewerScreen(resource: LearningResource, onBack: () -> Unit) {
    val container = LocalNebiansContainer.current
    val scope = rememberCoroutineScope()
    val annotationsFlow = remember(resource.id) { container.annotations.observe(resource.id) }
    val annotations by annotationsFlow.collectAsState()
    var pdfFile by remember(resource.id) { mutableStateOf<File?>(null) }
    var error by remember(resource.id) { mutableStateOf<String?>(null) }
    var tool by remember { mutableStateOf(AnnotationTool.Navigate) }
    var zoom by remember { mutableStateOf(1f) }

    LaunchedEffect(resource.id) {
        error = null
        runCatching { container.cache.getOrCreatePdf(resource) }
            .onSuccess { pdfFile = it }
            .onFailure { error = it.message ?: "Unable to open PDF" }
    }

    val renderer = remember(pdfFile?.absolutePath) {
        pdfFile?.let { PdfBitmapRenderer(it) }
    }
    DisposableEffect(renderer) {
        onDispose { renderer?.close() }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(resource.title, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(
                            "${resource.subject.label} - ${resource.grade.label}",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (annotations.isNotEmpty()) {
                        IconButton(onClick = { scope.launch { container.annotations.clear(resource.id) } }) {
                            Icon(Icons.Outlined.DeleteSweep, contentDescription = "Clear annotations")
                        }
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            PdfToolsRow(
                selectedTool = tool,
                onToolSelected = { tool = it },
                zoom = zoom,
                onZoomChange = { zoom = it.coerceIn(0.8f, 2.4f) }
            )

            when {
                error != null -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(error.orEmpty(), color = MaterialTheme.colorScheme.error)
                }
                renderer == null -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
                else -> BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                    val density = LocalDensity.current
                    val baseWidth = maxWidth
                    val targetWidthPx = with(density) { (baseWidth.toPx() * zoom).roundToInt() }
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(12.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(renderer.pageCount) { pageIndex ->
                            val pageAnnotations = annotations.filter { it.pageIndex == pageIndex }
                            PdfPageView(
                                renderer = renderer,
                                resource = resource,
                                pageIndex = pageIndex,
                                pageWidth = baseWidth * zoom,
                                targetWidthPx = targetWidthPx,
                                tool = tool,
                                annotations = pageAnnotations,
                                onAddAnnotation = { annotation ->
                                    scope.launch { container.annotations.add(annotation) }
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun PdfToolsRow(
    selectedTool: AnnotationTool,
    onToolSelected: (AnnotationTool) -> Unit,
    zoom: Float,
    onZoomChange: (Float) -> Unit
) {
    Surface(
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 0.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(AnnotationTool.entries.toList()) { item ->
                    FilterChip(
                        selected = selectedTool == item,
                        onClick = { onToolSelected(item) },
                        leadingIcon = {
                            Icon(toolIcon(item), contentDescription = null, modifier = Modifier.size(18.dp))
                        },
                        label = { Text(item.label) }
                    )
                }
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { onZoomChange(zoom - 0.1f) }) {
                    Icon(Icons.Outlined.ZoomOut, contentDescription = "Zoom out")
                }
                Text(
                    "${(zoom * 100).roundToInt()}%",
                    modifier = Modifier.width(64.dp),
                    style = MaterialTheme.typography.labelLarge
                )
                IconButton(onClick = { onZoomChange(zoom + 0.1f) }) {
                    Icon(Icons.Outlined.ZoomIn, contentDescription = "Zoom in")
                }
            }
        }
    }
}

@Composable
private fun PdfPageView(
    renderer: PdfBitmapRenderer,
    resource: LearningResource,
    pageIndex: Int,
    pageWidth: Dp,
    targetWidthPx: Int,
    tool: AnnotationTool,
    annotations: List<PdfAnnotation>,
    onAddAnnotation: (PdfAnnotation) -> Unit
) {
    var bitmap by remember(renderer, pageIndex, targetWidthPx) { mutableStateOf<Bitmap?>(null) }
    var draftRect by remember { mutableStateOf<Rect?>(null) }
    var pendingSticky by remember { mutableStateOf<Offset?>(null) }
    var stickyText by remember { mutableStateOf("") }

    LaunchedEffect(renderer, pageIndex, targetWidthPx) {
        bitmap = renderer.renderPage(pageIndex, targetWidthPx)
    }

    val pageBitmap = bitmap
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        if (pageBitmap == null) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(420.dp),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            val scrollState = rememberScrollState()
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(scrollState),
                contentAlignment = Alignment.Center
            ) {
                Surface(
                    modifier = Modifier
                        .width(pageWidth)
                        .aspectRatio(pageBitmap.width / pageBitmap.height.toFloat()),
                    shape = RoundedCornerShape(2.dp),
                    color = Color.White,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                    shadowElevation = 0.dp
                ) {
                    Box(modifier = Modifier.fillMaxSize()) {
                        Image(
                            bitmap = pageBitmap.asImageBitmap(),
                            contentDescription = "PDF page ${pageIndex + 1}",
                            modifier = Modifier.matchParentSize(),
                            contentScale = ContentScale.FillBounds
                        )
                        Canvas(
                            modifier = Modifier
                                .matchParentSize()
                                .annotationPointerInput(
                                    tool = tool,
                                    pageIndex = pageIndex,
                                    pdfId = resource.id,
                                    onDraftChanged = { draftRect = it },
                                    onStickyTap = { pendingSticky = it },
                                    onAddAnnotation = onAddAnnotation
                                )
                        ) {
                            annotations.forEach { annotation ->
                                drawAnnotation(annotation)
                            }
                            draftRect?.let { rect ->
                                drawRoundRect(
                                    color = Color(0xFFFFC107).copy(alpha = 0.22f),
                                    topLeft = Offset(rect.left, rect.top),
                                    size = Size(rect.width, rect.height),
                                    cornerRadius = CornerRadius(6f, 6f)
                                )
                            }
                        }
                    }
                }
            }
        }

        val notes = annotations.filter { it.kind == AnnotationKind.StickyNote && it.note.isNotBlank() }
        if (notes.isNotEmpty()) {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                notes.forEach { note ->
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        shape = MaterialTheme.shapes.medium,
                        color = MaterialTheme.colorScheme.tertiaryContainer,
                        tonalElevation = 0.dp
                    ) {
                        Text(
                            note.note,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onTertiaryContainer
                        )
                    }
                }
            }
        }
    }

    if (pendingSticky != null) {
        AlertDialog(
            onDismissRequest = {
                pendingSticky = null
                stickyText = ""
            },
            title = { Text("Sticky Note") },
            text = {
                OutlinedTextField(
                    value = stickyText,
                    onValueChange = { stickyText = it },
                    label = { Text("Note") },
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                Button(
                    enabled = stickyText.isNotBlank(),
                    onClick = {
                        val point = pendingSticky ?: return@Button
                        onAddAnnotation(
                            PdfAnnotation(
                                id = UUID.randomUUID().toString(),
                                pdfId = resource.id,
                                pageIndex = pageIndex,
                                kind = AnnotationKind.StickyNote,
                                x = point.x,
                                y = point.y,
                                width = 0.18f,
                                height = 0.07f,
                                note = stickyText.trim(),
                                color = 0xFF476179.toInt(),
                                createdAt = System.currentTimeMillis()
                            )
                        )
                        pendingSticky = null
                        stickyText = ""
                    }
                ) {
                    Text("Save")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        pendingSticky = null
                        stickyText = ""
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }
}

private fun Modifier.annotationPointerInput(
    tool: AnnotationTool,
    pageIndex: Int,
    pdfId: String,
    onDraftChanged: (Rect?) -> Unit,
    onStickyTap: (Offset) -> Unit,
    onAddAnnotation: (PdfAnnotation) -> Unit
): Modifier {
    return when (tool) {
        AnnotationTool.Highlight,
        AnnotationTool.Underline -> this.pointerInput(tool, pageIndex, pdfId) {
            var start: Offset? = null
            var latest: Offset? = null
            detectDragGestures(
                onDragStart = { offset ->
                    start = offset
                    latest = offset
                    onDraftChanged(Rect(offset, offset))
                },
                onDragCancel = {
                    start = null
                    latest = null
                    onDraftChanged(null)
                },
                onDragEnd = {
                    val origin = start
                    val end = latest
                    start = null
                    latest = null
                    val draft = if (origin != null && end != null) rectFromOffsets(origin, end) else null
                    onDraftChanged(null)
                    if (draft != null) {
                        val pageWidth = size.width.toFloat()
                        val pageHeight = size.height.toFloat()
                        if (draft.width > 10f && draft.height > 6f && pageWidth > 0f && pageHeight > 0f) {
                            val kind = if (tool == AnnotationTool.Highlight) {
                                AnnotationKind.Highlight
                            } else {
                                AnnotationKind.Underline
                            }
                            onAddAnnotation(
                                PdfAnnotation(
                                    id = UUID.randomUUID().toString(),
                                    pdfId = pdfId,
                                    pageIndex = pageIndex,
                                    kind = kind,
                                    x = (draft.left / pageWidth).coerceIn(0f, 1f),
                                    y = (draft.top / pageHeight).coerceIn(0f, 1f),
                                    width = (draft.width / pageWidth).coerceIn(0f, 1f),
                                    height = (draft.height / pageHeight).coerceIn(0f, 1f),
                                    note = "",
                                    color = if (kind == AnnotationKind.Highlight) 0xFFFFC107.toInt() else 0xFF0E5D4E.toInt(),
                                    createdAt = System.currentTimeMillis()
                                )
                            )
                        }
                    }
                },
                onDrag = { change, _ ->
                    val origin = start
                    if (origin != null) {
                        latest = change.position
                        onDraftChanged(rectFromOffsets(origin, change.position))
                    }
                    change.consume()
                }
            )
        }

        AnnotationTool.StickyNote -> this.pointerInput(tool, pageIndex, pdfId) {
            detectTapGestures { offset ->
                val pageWidth = size.width.toFloat().coerceAtLeast(1f)
                val pageHeight = size.height.toFloat().coerceAtLeast(1f)
                onStickyTap(
                    Offset(
                        (offset.x / pageWidth).coerceIn(0f, 1f),
                        (offset.y / pageHeight).coerceIn(0f, 1f)
                    )
                )
            }
        }

        AnnotationTool.Navigate -> this
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawAnnotation(annotation: PdfAnnotation) {
    val left = annotation.x * size.width
    val top = annotation.y * size.height
    val width = annotation.width * size.width
    val height = annotation.height * size.height
    when (annotation.kind) {
        AnnotationKind.Highlight -> drawRoundRect(
            color = Color(annotation.color).copy(alpha = 0.28f),
            topLeft = Offset(left, top),
            size = Size(width, height),
            cornerRadius = CornerRadius(6f, 6f)
        )

        AnnotationKind.Underline -> drawLine(
            color = Color(annotation.color),
            start = Offset(left, top + height),
            end = Offset(left + width, top + height),
            strokeWidth = max(3f, size.width * 0.004f)
        )

        AnnotationKind.StickyNote -> {
            drawRoundRect(
                color = Color(annotation.color).copy(alpha = 0.92f),
                topLeft = Offset(left, top),
                size = Size(max(width, 46f), max(height, 28f)),
                cornerRadius = CornerRadius(10f, 10f)
            )
            drawCircle(
                color = Color.White.copy(alpha = 0.92f),
                radius = 5f,
                center = Offset(left + 14f, top + 14f)
            )
        }
    }
}

private fun rectFromOffsets(start: Offset, end: Offset): Rect {
    return Rect(
        left = min(start.x, end.x),
        top = min(start.y, end.y),
        right = max(start.x, end.x),
        bottom = max(start.y, end.y)
    )
}

private fun toolIcon(tool: AnnotationTool): ImageVector = when (tool) {
    AnnotationTool.Navigate -> Icons.AutoMirrored.Outlined.MenuBook
    AnnotationTool.Highlight -> Icons.Outlined.BorderColor
    AnnotationTool.Underline -> Icons.Outlined.FormatUnderlined
    AnnotationTool.StickyNote -> Icons.AutoMirrored.Outlined.StickyNote2
}
