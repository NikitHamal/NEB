package com.neb.ians.ui.screens.pdf

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledIconToggleButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neb.ians.R
import com.neb.ians.data.model.AnnotationType
import com.neb.ians.di.AppModule
import com.neb.ians.ui.screens.pdf.PdfViewerViewModel.AnnotationMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfViewerScreen(
    pdfUri: String,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val vm: PdfViewerViewModel = viewModel {
        PdfViewerViewModel(
            pdfUri = pdfUri,
            cacheManager = AppModule.providePdfCacheManager(context),
            annotationRepository = AppModule.provideAnnotationRepository(context)
        )
    }

    var showNoteDialog by remember { mutableStateOf(false) }
    var noteText by remember { mutableStateOf("") }
    var tapOffset by remember { mutableStateOf<Offset?>(null) }
    var canvasSize by remember { mutableStateOf(androidx.compose.ui.unit.IntSize.Zero) }

    LaunchedEffect(vm.currentPage) {
        // page changed
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("PDF Viewer") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        },
        bottomBar = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(8.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = { vm.prevPage() }, enabled = vm.currentPage > 0) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Previous")
                    }
                    Text(
                        text = "${vm.currentPage + 1} / ${vm.pageCount.coerceAtLeast(1)}",
                        style = MaterialTheme.typography.labelLarge
                    )
                    IconButton(
                        onClick = { vm.nextPage() },
                        enabled = vm.currentPage < vm.pageCount - 1
                    ) {
                        Icon(Icons.Default.ArrowForward, contentDescription = "Next")
                    }
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    AnnotationToggleButton(
                        selected = vm.annotationMode is AnnotationMode.Highlight,
                        onClick = {
                            vm.annotationMode =
                                if (vm.annotationMode is AnnotationMode.Highlight) null else AnnotationMode.Highlight
                        },
                        label = stringResource(R.string.highlight)
                    )
                    AnnotationToggleButton(
                        selected = vm.annotationMode is AnnotationMode.Underline,
                        onClick = {
                            vm.annotationMode =
                                if (vm.annotationMode is AnnotationMode.Underline) null else AnnotationMode.Underline
                        },
                        label = stringResource(R.string.underline)
                    )
                    AnnotationToggleButton(
                        selected = vm.annotationMode is AnnotationMode.StickyNote,
                        onClick = {
                            vm.annotationMode =
                                if (vm.annotationMode is AnnotationMode.StickyNote) null else AnnotationMode.StickyNote
                        },
                        label = stringResource(R.string.sticky_note)
                    )
                    IconButton(onClick = { vm.persistAnnotations() }) {
                        Icon(Icons.Default.Save, contentDescription = stringResource(R.string.save))
                    }
                }
            }
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(MaterialTheme.colorScheme.background)
        ) {
            if (vm.isLoading) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            } else if (vm.error != null) {
                Text(
                    text = vm.error ?: "Error",
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.align(Alignment.Center)
                )
            } else {
                val bmp = vm.bitmap
                if (bmp != null) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .onSizeChanged { canvasSize = it }
                            .pointerInput(vm.annotationMode) {
                                detectTapGestures { offset ->
                                    val mode = vm.annotationMode ?: return@detectTapGestures
                                    if (canvasSize == androidx.compose.ui.unit.IntSize.Zero) return@detectTapGestures
                                    val nx = offset.x / canvasSize.width
                                    val ny = offset.y / canvasSize.height
                                    if (mode is AnnotationMode.StickyNote) {
                                        tapOffset = Offset(nx, ny)
                                        showNoteDialog = true
                                    } else {
                                        val w = if (mode is AnnotationMode.Highlight) 0.2f else 0.25f
                                        val h = if (mode is AnnotationMode.Highlight) 0.03f else 0.01f
                                        vm.addAnnotation(
                                            x = (nx - w / 2).coerceIn(0f, 1f - w),
                                            y = (ny - h / 2).coerceIn(0f, 1f - h),
                                            width = w,
                                            height = h
                                        )
                                    }
                                }
                            }
                    ) {
                        Image(
                            bitmap = bmp.asImageBitmap(),
                            contentDescription = "PDF Page",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.FillBounds
                        )
                        AnnotationOverlay(
                            annotations = vm.annotations.filter { it.pageIndex == vm.currentPage },
                            containerSize = canvasSize
                        )
                    }
                }
            }
        }
    }

    if (showNoteDialog) {
        AlertDialog(
            onDismissRequest = { showNoteDialog = false },
            title = { Text(stringResource(R.string.add_note)) },
            text = {
                TextField(
                    value = noteText,
                    onValueChange = { noteText = it },
                    placeholder = { Text(stringResource(R.string.add_note)) }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    tapOffset?.let { off ->
                        vm.addAnnotation(
                            x = off.x.coerceIn(0f, 0.95f),
                            y = off.y.coerceIn(0f, 0.95f),
                            width = 0.05f,
                            height = 0.05f,
                            note = noteText
                        )
                    }
                    showNoteDialog = false
                    noteText = ""
                    tapOffset = null
                }) {
                    Text(stringResource(R.string.save))
                }
            },
            dismissButton = {
                TextButton(onClick = { showNoteDialog = false }) {
                    Text(stringResource(R.string.cancel))
                }
            }
        )
    }
}

@Composable
private fun AnnotationToggleButton(
    selected: Boolean,
    onClick: () -> Unit,
    label: String
) {
    FilledIconToggleButton(
        checked = selected,
        onCheckedChange = { onClick() }
    ) {
        Text(text = label, style = MaterialTheme.typography.labelSmall)
    }
}

@Composable
fun AnnotationOverlay(
    annotations: List<com.neb.ians.data.model.PdfAnnotation>,
    containerSize: androidx.compose.ui.unit.IntSize
) {
    if (containerSize == androidx.compose.ui.unit.IntSize.Zero) return
    val measurer = rememberTextMeasurer()
    Canvas(modifier = Modifier.fillMaxSize()) {
        annotations.forEach { ann ->
            val x = ann.x * containerSize.width
            val y = ann.y * containerSize.height
            val w = ann.width * containerSize.width
            val h = ann.height * containerSize.height
            when (ann.type) {
                AnnotationType.HIGHLIGHT -> {
                    drawRect(
                        color = Color(ann.color).copy(alpha = 0.4f),
                        topLeft = Offset(x, y),
                        size = Size(w, h)
                    )
                }
                AnnotationType.UNDERLINE -> {
                    drawLine(
                        color = Color(ann.color),
                        start = Offset(x, y + h / 2),
                        end = Offset(x + w, y + h / 2),
                        strokeWidth = 4.dp.toPx()
                    )
                }
                AnnotationType.STICKY_NOTE -> {
                    drawRect(
                        color = Color(ann.color).copy(alpha = 0.9f),
                        topLeft = Offset(x, y),
                        size = Size(w.coerceAtLeast(40f), h.coerceAtLeast(40f))
                    )
                    ann.noteText?.let { text ->
                        drawText(
                            textMeasurer = measurer,
                            text = text,
                            topLeft = Offset(x + 4f, y + 14f),
                            style = androidx.compose.ui.text.TextStyle(
                                color = Color.Black,
                                fontSize = 12.sp
                            )
                        )
                    }
                }
            }
        }
    }
}
