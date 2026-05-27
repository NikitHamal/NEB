package com.neb.ians

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.rememberTransformableState
import androidx.compose.foundation.gestures.transformable
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Article
import androidx.compose.material.icons.outlined.ChevronLeft
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.Create
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.FormatUnderlined
import androidx.compose.material.icons.outlined.OpenInFull
import androidx.compose.material.icons.outlined.Save
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
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
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import com.neb.ians.data.AppSettings
import com.neb.ians.data.LearningResource
import com.neb.ians.data.ResourceCatalog
import com.neb.ians.pdf.AnnotationType
import com.neb.ians.pdf.PdfAnnotation
import com.neb.ians.pdf.PdfAnnotationStore
import com.neb.ians.pdf.PdfCacheRepository
import com.neb.ians.pdf.PdfPageRenderer
import com.neb.ians.pdf.RenderedPdfPage
import com.neb.ians.ui.theme.NebTheme
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

class PdfViewerActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val resource = ResourceCatalog.resourceById(intent.getStringExtra(EXTRA_RESOURCE_ID).orEmpty())
            ?: ResourceCatalog.resources.first()
        setContent {
            val settings = remember { AppSettings(this) }
            NebTheme(darkTheme = settings.isDarkMode()) {
                PdfViewerScreen(resource = resource, onBack = ::finish)
            }
        }
    }

    companion object {
        const val EXTRA_RESOURCE_ID = "resource_id"
    }
}

private enum class ViewerTool(val label: String) {
    Pan("Pan"),
    Highlight("Highlight"),
    Underline("Underline"),
    StickyNote("Note")
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun PdfViewerScreen(resource: LearningResource, onBack: () -> Unit) {
    val context = LocalContext.current
    val annotationStore = remember { PdfAnnotationStore(context) }
    val scope = rememberCoroutineScope()
    var pdfFile by remember { mutableStateOf<File?>(null) }
    var renderedPage by remember { mutableStateOf<RenderedPdfPage?>(null) }
    var annotations by remember { mutableStateOf<List<PdfAnnotation>>(emptyList()) }
    var pageIndex by rememberSaveable { mutableStateOf(0) }
    var pageCount by rememberSaveable { mutableStateOf(resource.pages) }
    var tool by rememberSaveable { mutableStateOf(ViewerTool.Pan.name) }
    var scale by remember { mutableFloatStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }
    val selectedTool = ViewerTool.valueOf(tool)

    LaunchedEffect(resource.id) {
        pdfFile = PdfCacheRepository.ensurePdf(context, resource)
        annotations = withContext(Dispatchers.IO) { annotationStore.load(resource.id) }
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                ),
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                title = {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(resource.title, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(
                            text = "${resource.subject.label} • ${resource.grade.label}",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                },
                actions = {
                    IconButton(
                        onClick = {
                            scope.launch {
                                annotations = withContext(Dispatchers.IO) {
                                    annotationStore.clearPage(resource.id, pageIndex)
                                }
                            }
                        }
                    ) {
                        Icon(Icons.Outlined.Delete, contentDescription = "Clear page annotations")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(MaterialTheme.colorScheme.background),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                ViewerToolbar(
                    selectedTool = selectedTool,
                    onToolSelected = { next ->
                        tool = next.name
                        if (next != ViewerTool.Pan) {
                            scale = 1f
                            offset = Offset.Zero
                        }
                    }
                )
            }
            item {
                PdfPageSurface(
                    resource = resource,
                    file = pdfFile,
                    pageIndex = pageIndex,
                    renderedPage = renderedPage,
                    annotations = annotations,
                    selectedTool = selectedTool,
                    scale = scale,
                    offset = offset,
                    onTransform = { zoomChange, panChange ->
                        scale = (scale * zoomChange).coerceIn(1f, 4f)
                        offset = if (scale == 1f) Offset.Zero else offset + panChange
                    },
                    onRendered = { rendered ->
                        renderedPage = rendered
                        pageCount = rendered.pageCount
                    },
                    onAnnotation = { type, startX, startY, endX, endY, note ->
                        scope.launch {
                            annotations = withContext(Dispatchers.IO) {
                                annotationStore.add(
                                    resourceId = resource.id,
                                    pageIndex = pageIndex,
                                    type = type,
                                    startX = startX,
                                    startY = startY,
                                    endX = endX,
                                    endY = endY,
                                    note = note
                                )
                            }
                        }
                    }
                )
            }
            item {
                PageControls(
                    pageIndex = pageIndex,
                    pageCount = pageCount,
                    onPrevious = {
                        pageIndex = (pageIndex - 1).coerceAtLeast(0)
                        scale = 1f
                        offset = Offset.Zero
                    },
                    onNext = {
                        pageIndex = (pageIndex + 1).coerceAtMost(pageCount - 1)
                        scale = 1f
                        offset = Offset.Zero
                    }
                )
            }
            val pageNotes = annotations.filter { it.pageIndex == pageIndex && it.type == AnnotationType.StickyNote }
            if (pageNotes.isNotEmpty()) {
                item {
                    Text("Sticky notes", style = MaterialTheme.typography.titleMedium)
                }
                items(pageNotes, key = { it.id }) { note ->
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
                        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
                    ) {
                        Text(
                            text = note.note,
                            modifier = Modifier.padding(14.dp),
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                }
            }
            item {
                AssistChip(
                    onClick = { },
                    label = { Text("Saved locally for offline access") },
                    leadingIcon = { Icon(Icons.Outlined.Save, contentDescription = null) }
                )
            }
        }
    }
}

@Composable
private fun ViewerToolbar(
    selectedTool: ViewerTool,
    onToolSelected: (ViewerTool) -> Unit
) {
    LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        items(ViewerTool.entries) { item ->
            FilterChip(
                selected = selectedTool == item,
                onClick = { onToolSelected(item) },
                label = { Text(item.label) },
                leadingIcon = { Icon(toolIcon(item), contentDescription = null) }
            )
        }
    }
}

@Composable
private fun PdfPageSurface(
    resource: LearningResource,
    file: File?,
    pageIndex: Int,
    renderedPage: RenderedPdfPage?,
    annotations: List<PdfAnnotation>,
    selectedTool: ViewerTool,
    scale: Float,
    offset: Offset,
    onTransform: (Float, Offset) -> Unit,
    onRendered: (RenderedPdfPage) -> Unit,
    onAnnotation: (AnnotationType, Float, Float, Float, Float, String) -> Unit
) {
    val density = LocalDensity.current
    BoxWithConstraints(
        modifier = Modifier.fillMaxWidth()
    ) {
        val targetWidth = with(density) { maxWidth.roundToPx() }.coerceAtLeast(1080)
        LaunchedEffect(file, pageIndex, targetWidth) {
            if (file != null) {
                onRendered(PdfPageRenderer.render(file, pageIndex, targetWidth))
            }
        }

        val bitmap = renderedPage?.takeIf { it.pageIndex == pageIndex }?.bitmap
        if (file == null || bitmap == null) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(420.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainer),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            var viewportSize by remember { mutableStateOf(IntSize.Zero) }
            var dragStart by remember { mutableStateOf<Offset?>(null) }
            var dragCurrent by remember { mutableStateOf<Offset?>(null) }
            var pendingNote by remember { mutableStateOf<Offset?>(null) }
            var noteText by rememberSaveable { mutableStateOf("") }
            val transformState = rememberTransformableState { zoomChange, panChange, _ ->
                onTransform(zoomChange, panChange)
            }
            val ratio = bitmap.width.toFloat() / bitmap.height.toFloat()
            val gestureModifier = when (selectedTool) {
                ViewerTool.Pan -> Modifier.transformable(transformState)
                ViewerTool.Highlight,
                ViewerTool.Underline -> Modifier.pointerInput(selectedTool, viewportSize, pageIndex) {
                    detectDragGestures(
                        onDragStart = { start ->
                            dragStart = start
                            dragCurrent = start
                        },
                        onDrag = { change, _ ->
                            dragCurrent = change.position
                        },
                        onDragEnd = {
                            val start = dragStart
                            val end = dragCurrent
                            if (start != null && end != null && viewportSize.width > 0 && viewportSize.height > 0) {
                                if (abs(start.x - end.x) > 10f || abs(start.y - end.y) > 10f) {
                                    val type = if (selectedTool == ViewerTool.Highlight) {
                                        AnnotationType.Highlight
                                    } else {
                                        AnnotationType.Underline
                                    }
                                    onAnnotation(
                                        type,
                                        start.x / viewportSize.width,
                                        start.y / viewportSize.height,
                                        end.x / viewportSize.width,
                                        end.y / viewportSize.height,
                                        ""
                                    )
                                }
                            }
                            dragStart = null
                            dragCurrent = null
                        },
                        onDragCancel = {
                            dragStart = null
                            dragCurrent = null
                        }
                    )
                }
                ViewerTool.StickyNote -> Modifier.pointerInput(viewportSize, pageIndex) {
                    detectTapGestures { tap ->
                        if (viewportSize.width > 0 && viewportSize.height > 0) {
                            pendingNote = Offset(
                                x = (tap.x / viewportSize.width).coerceIn(0f, 1f),
                                y = (tap.y / viewportSize.height).coerceIn(0f, 1f)
                            )
                            noteText = ""
                        }
                    }
                }
            }

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(ratio)
                    .clip(RoundedCornerShape(8.dp))
                        .background(Color.White)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .onSizeChanged { viewportSize = it }
                        .graphicsLayer(
                            scaleX = scale,
                            scaleY = scale,
                            translationX = offset.x,
                            translationY = offset.y
                        )
                        .then(gestureModifier)
                ) {
                    Image(
                        bitmap = bitmap.asImageBitmap(),
                        contentDescription = "${resource.title} page ${pageIndex + 1}",
                        contentScale = ContentScale.FillBounds,
                        modifier = Modifier.fillMaxSize()
                    )
                    AnnotationCanvas(
                        annotations = annotations.filter { it.pageIndex == pageIndex },
                        dragStart = dragStart,
                        dragCurrent = dragCurrent,
                        previewType = selectedTool
                    )
                }
            }

            if (pendingNote != null) {
                AlertDialog(
                    onDismissRequest = { pendingNote = null },
                    title = { Text("Sticky note") },
                    text = {
                        OutlinedTextField(
                            value = noteText,
                            onValueChange = { noteText = it },
                            label = { Text("Note") },
                            minLines = 3
                        )
                    },
                    confirmButton = {
                        TextButton(
                            enabled = noteText.isNotBlank(),
                            onClick = {
                                val point = pendingNote ?: return@TextButton
                                onAnnotation(
                                    AnnotationType.StickyNote,
                                    point.x,
                                    point.y,
                                    (point.x + 0.035f).coerceAtMost(1f),
                                    (point.y + 0.035f).coerceAtMost(1f),
                                    noteText
                                )
                                pendingNote = null
                                noteText = ""
                            }
                        ) {
                            Text("Save")
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { pendingNote = null }) {
                            Text("Cancel")
                        }
                    }
                )
            }
        }
    }
}

@Composable
private fun AnnotationCanvas(
    annotations: List<PdfAnnotation>,
    dragStart: Offset?,
    dragCurrent: Offset?,
    previewType: ViewerTool
) {
    Canvas(modifier = Modifier.fillMaxSize()) {
        annotations.forEach { annotation ->
            val left = min(annotation.startX, annotation.endX) * size.width
            val right = max(annotation.startX, annotation.endX) * size.width
            val top = min(annotation.startY, annotation.endY) * size.height
            val bottom = max(annotation.startY, annotation.endY) * size.height
            when (annotation.type) {
                AnnotationType.Highlight -> {
                    drawRoundRect(
                        color = Color(0xFFFFD54F).copy(alpha = 0.42f),
                        topLeft = Offset(left, top),
                        size = Size((right - left).coerceAtLeast(18f), (bottom - top).coerceAtLeast(18f)),
                        cornerRadius = CornerRadius(6.dp.toPx(), 6.dp.toPx())
                    )
                }
                AnnotationType.Underline -> {
                    drawLine(
                        color = Color(0xFF2F6FD6),
                        start = Offset(left, bottom),
                        end = Offset(right, bottom),
                        strokeWidth = 4.dp.toPx(),
                        cap = StrokeCap.Round
                    )
                }
                AnnotationType.StickyNote -> {
                    val point = Offset(annotation.startX * size.width, annotation.startY * size.height)
                    drawCircle(
                        color = Color(0xFFF2B84B),
                        radius = 13.dp.toPx(),
                        center = point
                    )
                    drawRoundRect(
                        color = Color.White.copy(alpha = 0.92f),
                        topLeft = Offset(point.x - 4.dp.toPx(), point.y - 7.dp.toPx()),
                        size = Size(8.dp.toPx(), 14.dp.toPx()),
                        cornerRadius = CornerRadius(2.dp.toPx(), 2.dp.toPx())
                    )
                }
            }
        }

        if (dragStart != null && dragCurrent != null) {
            val left = min(dragStart.x, dragCurrent.x)
            val right = max(dragStart.x, dragCurrent.x)
            val top = min(dragStart.y, dragCurrent.y)
            val bottom = max(dragStart.y, dragCurrent.y)
            if (previewType == ViewerTool.Highlight) {
                drawRoundRect(
                    color = Color(0xFFFFD54F).copy(alpha = 0.26f),
                    topLeft = Offset(left, top),
                    size = Size((right - left).coerceAtLeast(18f), (bottom - top).coerceAtLeast(18f)),
                    cornerRadius = CornerRadius(6.dp.toPx(), 6.dp.toPx())
                )
            }
            if (previewType == ViewerTool.Underline) {
                drawLine(
                    color = Color(0xFF2F6FD6).copy(alpha = 0.75f),
                    start = Offset(left, bottom),
                    end = Offset(right, bottom),
                    strokeWidth = 4.dp.toPx(),
                    cap = StrokeCap.Round
                )
            }
        }
    }
}

@Composable
private fun PageControls(
    pageIndex: Int,
    pageCount: Int,
    onPrevious: () -> Unit,
    onNext: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        IconButton(enabled = pageIndex > 0, onClick = onPrevious) {
            Icon(Icons.Outlined.ChevronLeft, contentDescription = "Previous page")
        }
        Spacer(Modifier.width(10.dp))
        Text(
            text = "Page ${pageIndex + 1} of $pageCount",
            style = MaterialTheme.typography.titleSmall
        )
        Spacer(Modifier.width(10.dp))
        IconButton(enabled = pageIndex < pageCount - 1, onClick = onNext) {
            Icon(Icons.Outlined.ChevronRight, contentDescription = "Next page")
        }
    }
}

private fun toolIcon(tool: ViewerTool): ImageVector = when (tool) {
    ViewerTool.Pan -> Icons.Outlined.OpenInFull
    ViewerTool.Highlight -> Icons.Outlined.Create
    ViewerTool.Underline -> Icons.Outlined.FormatUnderlined
    ViewerTool.StickyNote -> Icons.Outlined.Article
}
