package com.neb.ians.ui.screens.pdfviewer

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.FormatColorFill
import androidx.compose.material.icons.filled.FormatUnderlined
import androidx.compose.material.icons.filled.StickyNote2
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.BottomAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconToggleButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neb.ians.data.local.entity.AnnotationEntity
import com.neb.ians.data.local.entity.ResourceEntity

enum class AnnotationMode { NONE, HIGHLIGHT, UNDERLINE, STICKY_NOTE }

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfViewerScreen(
    resourceId: Long,
    onBack: () -> Unit,
    viewModel: PdfViewerViewModel = viewModel(),
) {
    val resource by viewModel.resource.collectAsState()
    val annotations by viewModel.annotations.collectAsState()
    val isBookmarked by viewModel.isBookmarked.collectAsState()
    var annotationMode by rememberSaveable { mutableStateOf(AnnotationMode.NONE) }
    var showStickyDialog by rememberSaveable { mutableStateOf(false) }
    var stickyNoteX by remember { mutableFloatStateOf(0f) }
    var stickyNoteY by remember { mutableFloatStateOf(0f) }
    var stickyNotePage by remember { mutableIntStateOf(0) }

    LaunchedEffect(resourceId) {
        viewModel.loadResource(resourceId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            resource?.title ?: "PDF Viewer",
                            style = MaterialTheme.typography.titleMedium,
                        )
                        if (resource != null) {
                            Text(
                                "${resource?.subject} • ${resource?.grade}",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { viewModel.toggleBookmark() }) {
                        Icon(
                            if (isBookmarked) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
                            contentDescription = "Bookmark",
                            tint = if (isBookmarked) MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                },
            )
        },
        bottomBar = {
            BottomAppBar(
                actions = {
                    IconToggleButton(
                        checked = annotationMode == AnnotationMode.HIGHLIGHT,
                        onCheckedChange = {
                            annotationMode = if (it) AnnotationMode.HIGHLIGHT else AnnotationMode.NONE
                        },
                    ) {
                        Icon(
                            Icons.Filled.FormatColorFill,
                            contentDescription = "Highlight",
                            tint = if (annotationMode == AnnotationMode.HIGHLIGHT)
                                MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    IconToggleButton(
                        checked = annotationMode == AnnotationMode.UNDERLINE,
                        onCheckedChange = {
                            annotationMode = if (it) AnnotationMode.UNDERLINE else AnnotationMode.NONE
                        },
                    ) {
                        Icon(
                            Icons.Filled.FormatUnderlined,
                            contentDescription = "Underline",
                            tint = if (annotationMode == AnnotationMode.UNDERLINE)
                                MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    IconToggleButton(
                        checked = annotationMode == AnnotationMode.STICKY_NOTE,
                        onCheckedChange = {
                            annotationMode = if (it) AnnotationMode.STICKY_NOTE else AnnotationMode.NONE
                        },
                    ) {
                        Icon(
                            Icons.Filled.StickyNote2,
                            contentDescription = "Sticky Note",
                            tint = if (annotationMode == AnnotationMode.STICKY_NOTE)
                                MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    if (annotationMode != AnnotationMode.NONE) {
                        Spacer(Modifier.width(8.dp))
                        IconButton(onClick = { annotationMode = AnnotationMode.NONE }) {
                            Icon(Icons.Filled.Close, "Cancel annotation")
                        }
                    }
                },
            )
        },
    ) { innerPadding ->
        if (resource != null) {
            PdfContent(
                resource = resource!!,
                annotations = annotations,
                annotationMode = annotationMode,
                onAddAnnotation = { page, startX, startY, endX, endY ->
                    when (annotationMode) {
                        AnnotationMode.HIGHLIGHT -> {
                            viewModel.addAnnotation(
                                page = page,
                                type = "highlight",
                                startX = startX, startY = startY,
                                endX = endX, endY = endY,
                            )
                        }
                        AnnotationMode.UNDERLINE -> {
                            viewModel.addAnnotation(
                                page = page,
                                type = "underline",
                                startX = startX, startY = startY,
                                endX = endX, endY = endY,
                            )
                        }
                        AnnotationMode.STICKY_NOTE -> {
                            stickyNoteX = startX
                            stickyNoteY = startY
                            stickyNotePage = page
                            showStickyDialog = true
                        }
                        AnnotationMode.NONE -> {}
                    }
                },
                onDeleteAnnotation = { viewModel.deleteAnnotation(it) },
                modifier = Modifier.padding(innerPadding),
            )
        } else {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    "Loading...",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }

        if (showStickyDialog) {
            StickyNoteDialog(
                onDismiss = { showStickyDialog = false },
                onConfirm = { text ->
                    viewModel.addAnnotation(
                        page = stickyNotePage,
                        type = "sticky",
                        content = text,
                        startX = stickyNoteX,
                        startY = stickyNoteY,
                        endX = stickyNoteX,
                        endY = stickyNoteY,
                    )
                    showStickyDialog = false
                },
            )
        }
    }
}

@Composable
private fun PdfContent(
    resource: ResourceEntity,
    annotations: List<AnnotationEntity>,
    annotationMode: AnnotationMode,
    onAddAnnotation: (page: Int, startX: Float, startY: Float, endX: Float, endY: Float) -> Unit,
    onDeleteAnnotation: (AnnotationEntity) -> Unit,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val samplePageCount = 5

    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(8.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        itemsIndexed((0 until samplePageCount).toList()) { index, page ->
            PdfPage(
                pageIndex = page,
                resourceTitle = resource.title,
                annotations = annotations.filter { it.page == page },
                annotationMode = annotationMode,
                onAddAnnotation = { startX, startY, endX, endY ->
                    onAddAnnotation(page, startX, startY, endX, endY)
                },
                onDeleteAnnotation = onDeleteAnnotation,
            )
        }
    }
}

@Composable
private fun PdfPage(
    pageIndex: Int,
    resourceTitle: String,
    annotations: List<AnnotationEntity>,
    annotationMode: AnnotationMode,
    onAddAnnotation: (startX: Float, startY: Float, endX: Float, endY: Float) -> Unit,
    onDeleteAnnotation: (AnnotationEntity) -> Unit,
) {
    var dragStart by remember { mutableStateOf(Offset.Zero) }
    var dragEnd by remember { mutableStateOf(Offset.Zero) }
    var isDragging by remember { mutableStateOf(false) }
    val highlightColor = Color(0x40FFEB3B)
    val underlineColor = Color(0xFFFF5722)
    val stickyColor = Color(0xFFFFF176)

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(500.dp)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .then(
                if (annotationMode != AnnotationMode.NONE) {
                    Modifier
                        .pointerInput(annotationMode) {
                            if (annotationMode == AnnotationMode.STICKY_NOTE) {
                                detectTapGestures { offset ->
                                    onAddAnnotation(
                                        offset.x / size.width,
                                        offset.y / size.height,
                                        offset.x / size.width,
                                        offset.y / size.height,
                                    )
                                }
                            } else {
                                detectDragGestures(
                                    onDragStart = { offset ->
                                        dragStart = offset
                                        dragEnd = offset
                                        isDragging = true
                                    },
                                    onDrag = { change, _ ->
                                        dragEnd = change.position
                                    },
                                    onDragEnd = {
                                        isDragging = false
                                        onAddAnnotation(
                                            dragStart.x / size.width,
                                            dragStart.y / size.height,
                                            dragEnd.x / size.width,
                                            dragEnd.y / size.height,
                                        )
                                    },
                                )
                            }
                        }
                } else Modifier
            ),
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawRect(
                color = Color.White,
                topLeft = Offset.Zero,
                size = size,
            )

            val textColor = Color(0xFF333333)
            val lineSpacing = 24.dp.toPx()
            val marginX = 32.dp.toPx()
            var y = 48.dp.toPx()

            drawContext.canvas.nativeCanvas.apply {
                val titlePaint = android.graphics.Paint().apply {
                    color = 0xFF1B6EF3.toInt()
                    textSize = 18.dp.toPx()
                    isAntiAlias = true
                    typeface = android.graphics.Typeface.create("sans-serif-medium", android.graphics.Typeface.BOLD)
                }
                drawText(resourceTitle, marginX, y, titlePaint)
                y += lineSpacing * 1.5f

                val bodyPaint = android.graphics.Paint().apply {
                    color = 0xFF333333.toInt()
                    textSize = 13.dp.toPx()
                    isAntiAlias = true
                }

                val pageLabel = "Page ${pageIndex + 1}"
                val pagePaint = android.graphics.Paint().apply {
                    color = 0xFF999999.toInt()
                    textSize = 11.dp.toPx()
                    isAntiAlias = true
                }
                drawText(pageLabel, size.width - marginX - pagePaint.measureText(pageLabel), size.height - 20.dp.toPx(), pagePaint)

                val sampleLines = listOf(
                    "This is a sample PDF page for the NEBians educational app.",
                    "In a real implementation, actual PDF content would be rendered",
                    "using Android's PdfRenderer API for high-fidelity display.",
                    "",
                    "The annotation tools allow you to:",
                    "  • Highlight important sections by dragging across text",
                    "  • Underline key concepts for quick reference",
                    "  • Add sticky notes with your own thoughts",
                    "",
                    "All annotations are saved locally and will persist",
                    "even when you close the app or go offline.",
                    "",
                    "NEB (National Examinations Board) curriculum resources",
                    "are organized by subject, grade, and type for easy access.",
                    "",
                    "Subjects include: Physics, Chemistry, Mathematics,",
                    "Biology, English, Nepali, Computer Science, Economics,",
                    "Account, and Social Studies.",
                    "",
                    "This viewer supports Grade 11 and Grade 12 materials.",
                )

                for (line in sampleLines) {
                    drawText(line, marginX, y, bodyPaint)
                    y += lineSpacing
                }
            }

            annotations.forEach { annotation ->
                val aStartX = annotation.startX * size.width
                val aStartY = annotation.startY * size.height
                val aEndX = annotation.endX * size.width
                val aEndY = annotation.endY * size.height

                when (annotation.type) {
                    "highlight" -> {
                        drawRect(
                            color = highlightColor,
                            topLeft = Offset(
                                minOf(aStartX, aEndX),
                                minOf(aStartY, aEndY),
                            ),
                            size = Size(
                                kotlin.math.abs(aEndX - aStartX),
                                kotlin.math.abs(aEndY - aStartY),
                            ),
                        )
                    }
                    "underline" -> {
                        drawLine(
                            color = underlineColor,
                            start = Offset(minOf(aStartX, aEndX), maxOf(aStartY, aEndY)),
                            end = Offset(maxOf(aStartX, aEndX), maxOf(aStartY, aEndY)),
                            strokeWidth = 3.dp.toPx(),
                        )
                    }
                    "sticky" -> {
                        drawRect(
                            color = stickyColor,
                            topLeft = Offset(aStartX, aStartY),
                            size = Size(120.dp.toPx(), 80.dp.toPx()),
                        )
                        drawRect(
                            color = Color(0xFFE6C700),
                            topLeft = Offset(aStartX, aStartY),
                            size = Size(120.dp.toPx(), 80.dp.toPx()),
                            style = Stroke(width = 1.dp.toPx()),
                        )
                        drawContext.canvas.nativeCanvas.apply {
                            val notePaint = android.graphics.Paint().apply {
                                color = 0xFF333333.toInt()
                                textSize = 10.dp.toPx()
                                isAntiAlias = true
                            }
                            val noteText = annotation.content
                            val maxWidth = 110.dp.toPx()
                            val words = noteText.split(" ")
                            var line = ""
                            var noteY = aStartY + 16.dp.toPx()
                            for (word in words) {
                                val test = if (line.isEmpty()) word else "$line $word"
                                if (notePaint.measureText(test) <= maxWidth) {
                                    line = test
                                } else {
                                    drawText(line, aStartX + 5.dp.toPx(), noteY, notePaint)
                                    noteY += 14.dp.toPx()
                                    line = word
                                }
                            }
                            if (line.isNotEmpty()) {
                                drawText(line, aStartX + 5.dp.toPx(), noteY, notePaint)
                            }
                        }
                    }
                }
            }

            if (isDragging && annotationMode != AnnotationMode.NONE && annotationMode != AnnotationMode.STICKY_NOTE) {
                val previewColor = when (annotationMode) {
                    AnnotationMode.HIGHLIGHT -> highlightColor
                    AnnotationMode.UNDERLINE -> underlineColor
                    else -> Color.Transparent
                }
                if (annotationMode == AnnotationMode.HIGHLIGHT) {
                    drawRect(
                        color = previewColor,
                        topLeft = Offset(
                            minOf(dragStart.x, dragEnd.x),
                            minOf(dragStart.y, dragEnd.y),
                        ),
                        size = Size(
                            kotlin.math.abs(dragEnd.x - dragStart.x),
                            kotlin.math.abs(dragEnd.y - dragStart.y),
                        ),
                    )
                } else {
                    drawLine(
                        color = previewColor,
                        start = Offset(minOf(dragStart.x, dragEnd.x), maxOf(dragStart.y, dragEnd.y)),
                        end = Offset(maxOf(dragStart.x, dragEnd.x), maxOf(dragStart.y, dragEnd.y)),
                        strokeWidth = 3.dp.toPx(),
                    )
                }
            }
        }

        if (annotationMode != AnnotationMode.NONE) {
            Text(
                when (annotationMode) {
                    AnnotationMode.HIGHLIGHT -> "Drag to highlight"
                    AnnotationMode.UNDERLINE -> "Drag to underline"
                    AnnotationMode.STICKY_NOTE -> "Tap to add note"
                    else -> ""
                },
                modifier = Modifier
                    .align(Alignment.TopCenter)
                    .padding(8.dp)
                    .background(
                        MaterialTheme.colorScheme.primaryContainer,
                        MaterialTheme.shapes.small,
                    )
                    .padding(horizontal = 12.dp, vertical = 4.dp),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
            )
        }
    }
}

@Composable
private fun StickyNoteDialog(
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit,
) {
    var text by rememberSaveable { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add Note") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                placeholder = { Text("Your note...") },
                modifier = Modifier.fillMaxWidth(),
                maxLines = 4,
            )
        },
        confirmButton = {
            TextButton(
                onClick = { onConfirm(text) },
                enabled = text.isNotBlank(),
            ) {
                Text("Add")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        },
    )
}
