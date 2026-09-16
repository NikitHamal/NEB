package com.neb.ians.ui.screens.canvas

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.CropSquare
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.Highlight
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.NoteAdd
import androidx.compose.material.icons.filled.PanTool
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.TextFields
import androidx.compose.material.icons.filled.TouchApp
import androidx.compose.material.icons.filled.Widgets
import androidx.compose.material.icons.outlined.Circle
import androidx.compose.material.icons.outlined.DeleteSweep
import androidx.compose.material.icons.outlined.StickyNote2
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.CanvasNode
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.luminanceIsDark
import kotlin.math.abs
import kotlin.math.roundToInt

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CanvasBoardScreen(
    onNavigateBack: () -> Unit,
    onOpenBoard: (String) -> Unit,
    viewModel: CanvasBoardViewModel = hiltViewModel(),
    listViewModel: CanvasListViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val listState by listViewModel.uiState.collectAsStateWithLifecycle()
    val density = LocalDensity.current
    val d = density.density
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }

    var scale by remember { mutableFloatStateOf(1f) }
    var viewX by remember { mutableFloatStateOf(0f) }
    var viewY by remember { mutableFloatStateOf(0f) }
    var viewportWpx by remember { mutableFloatStateOf(0f) }
    var viewportHpx by remember { mutableFloatStateOf(0f) }
    val cardHeights = remember { mutableStateMapOf<String, Float>() }

    var tool by remember { mutableStateOf(CanvasTool.SELECT) }
    var drawColor by remember { mutableStateOf(CANVAS_DRAW_COLORS[0]) }
    var drawWidth by remember { mutableFloatStateOf(4f) }

    var inspectorNodeId by remember { mutableStateOf<String?>(null) }
    var showNoteComposer by remember { mutableStateOf(false) }
    var noteAt by remember { mutableStateOf(Offset(420f, 120f)) }
    var showHistory by remember { mutableStateOf(false) }
    var showShare by remember { mutableStateOf(false) }
    var showTemplates by remember { mutableStateOf(false) }
    var showPalette by remember { mutableStateOf(false) }
    var showWidgetPicker by remember { mutableStateOf(false) }
    var showMoreMenu by remember { mutableStateOf(false) }
    var annotate by remember { mutableStateOf<Pair<CanvasTool, Offset>?>(null) }
    var promptDraft by remember { mutableStateOf("") }
    var fittedOnce by remember { mutableStateOf(false) }

    val nodes = uiState.nodes
    val nodeById = remember(nodes) { nodes.associateBy { it.id } }
    val inspectorNode = inspectorNodeId?.let { nodeById[it] }
    val (widgetObjs, drawObjs) = remember(uiState.drawObjects) {
        uiState.drawObjects.partition { it.drawType() == "widget" }
    }

    LaunchedEffect(uiState.snackbarMessage) {
        uiState.snackbarMessage?.let {
            snackbarHostState.showSnackbar(it)
            viewModel.consumeSnackbar()
        }
    }

    val importLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        if (uri == null) return@rememberLauncherForActivityResult
        try {
            context.contentResolver.openInputStream(uri)?.use { stream ->
                viewModel.importBoard(stream.bufferedReader().readText())
            }
        } catch (_: Exception) {
        }
    }

    fun shareText(text: String, mime: String, title: String) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            putExtra(Intent.EXTRA_TEXT, text)
            type = mime
        }
        context.startActivity(Intent.createChooser(intent, title))
    }

    fun centerOn(wx: Float, wy: Float, targetScale: Float = scale) {
        if (viewportWpx <= 0f) return
        scale = targetScale.coerceIn(0.08f, 8f)
        viewX = viewportWpx / 2f - wx * d * scale
        viewY = viewportHpx / 2f - wy * d * scale
    }

    fun fitAll() {
        if (viewportWpx <= 0f) return
        if (nodes.isEmpty()) {
            scale = 1f
            viewX = viewportWpx / 2f - 420f * d
            viewY = viewportHpx / 3f
            return
        }
        var l = Float.MAX_VALUE; var t = Float.MAX_VALUE
        var r = -Float.MAX_VALUE; var b = -Float.MAX_VALUE
        nodes.forEach { n ->
            val h = cardHeights[n.id] ?: 220f
            l = minOf(l, n.x.toFloat()); t = minOf(t, n.y.toFloat())
            r = maxOf(r, n.x.toFloat() + 340f); b = maxOf(b, n.y.toFloat() + h)
        }
        val cw = (r - l + 160f) * d
        val ch = (b - t + 160f) * d
        val s = minOf(viewportWpx / cw, viewportHpx / ch, 1f).coerceIn(0.08f, 8f)
        scale = s
        viewX = viewportWpx / 2f - (l + r) / 2f * d * s
        viewY = viewportHpx / 2f - (t + b) / 2f * d * s
    }

    fun screenToWorld(px: Offset): Offset =
        Offset((px.x - viewX) / scale / d, (px.y - viewY) / scale / d)

    fun worldToScreenLocal(wx: Float, wy: Float): Offset =
        Offset(wx * d * scale + viewX, wy * d * scale + viewY)

    fun viewportCenterWorld(): Offset =
        screenToWorld(Offset(viewportWpx / 2f, viewportHpx / 2f))

    val anchorColor = MaterialTheme.colorScheme.primary

    fun anchorCenters(node: CanvasNode): List<Offset> {
        val h = cardHeights[node.id] ?: 220f
        val x = node.x.toFloat()
        val y = node.y.toFloat()
        return listOf(
            worldToScreenLocal(x + 170f, y),
            worldToScreenLocal(x + 170f, y + h),
            worldToScreenLocal(x, y + h / 2f),
            worldToScreenLocal(x + 340f, y + h / 2f)
        )
    }

    fun findAnchorHit(tap: Offset): String? {
        val slop = 28f * d
        nodes.forEach { node ->
            anchorCenters(node).forEach { c ->
                if ((tap - c).getDistance() <= slop) return node.id
            }
        }
        return null
    }

    LaunchedEffect(viewportWpx, nodes.isNotEmpty()) {
        if (nodes.isNotEmpty() && !fittedOnce && viewportWpx > 0f) {
            fittedOnce = true
            fitAll()
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            NebTopBar(
                showBrand = false,
                title = uiState.board?.title?.ifBlank { "Canvas" } ?: "Canvas",
                onBack = onNavigateBack,
                actions = {
                    if (uiState.readOnly) {
                        TextButton(onClick = { viewModel.cloneShared(onOpenBoard) }) {
                            Text("Clone")
                        }
                    }
                }
            )
        },
        containerColor = if (MaterialTheme.colorScheme.surface.luminanceIsDark()) Color(0xFF0B1320) else Color(0xFFF5F7FB)
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            if (!uiState.readOnly) {
                Surface(color = MaterialTheme.colorScheme.surface) {
                    Column {
                        CanvasToolbar(
                            tool = tool,
                            onTool = { tool = it },
                            onNote = {
                                val c = viewportCenterWorld()
                                noteAt = c
                                showNoteComposer = true
                            },
                            onWidgets = { showWidgetPicker = true },
                            onHistory = {
                                viewModel.refreshSnapshots()
                                showHistory = true
                            },
                            onShare = { showShare = true },
                            onPalette = { showPalette = true },
                            onMore = { showMoreMenu = true }
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                    }
                }
            }
            BoxWithConstraints(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {
            LaunchedEffect(maxWidth, maxHeight) {
                viewportWpx = with(density) { maxWidth.toPx() }
                viewportHpx = with(density) { maxHeight.toPx() }
            }

            val dotColor = if (MaterialTheme.colorScheme.surface.luminanceIsDark()) Color(0xFF3B4C68) else Color(0xFFD0D7E5)
            val wireColor = if (MaterialTheme.colorScheme.surface.luminanceIsDark()) Color(0xFF3B4C68) else Color(0xFFA8B8D8)

            Canvas(
                modifier = Modifier.fillMaxSize(),
                onDraw = {
                    val step = 28f * d * scale
                    if (step > 8f) {
                        var ox = viewX % step
                        if (ox > 0) ox -= step
                        var oy = viewY % step
                        if (oy > 0) oy -= step
                        var x = ox
                        while (x < size.width) {
                            var y = oy
                            while (y < size.height) {
                                drawCircle(dotColor, radius = 1.4f * d, center = Offset(x, y))
                                y += step
                            }
                            x += step
                        }
                    }
                }
            )

            Canvas(
                modifier = Modifier
                    .fillMaxSize()
                    .pointerInput(nodeById, scale, viewX, viewY) {
                        detectTapGestures(onTap = { tap ->
                            val hit = findAnchorHit(tap)
                            if (hit != null) inspectorNodeId = hit
                        })
                    },
                onDraw = {
                    nodeById.values.forEach { node ->
                        val parentId = node.parentId
                        val parent = parentId?.let { nodeById[it] } ?: return@forEach
                        val p0 = worldToScreenLocal(parent.x.toFloat() + 170f, parent.y.toFloat() + (cardHeights[parent.id] ?: 220f))
                        val p3 = worldToScreenLocal(node.x.toFloat() + 170f, node.y.toFloat())
                        val dx = p3.x - p0.x
                        val dy = p3.y - p0.y
                        val path = Path()
                        if (abs(dy) >= 0.7f * abs(dx)) {
                            path.moveTo(p0.x, p0.y)
                            path.cubicTo(p0.x, p0.y + dy / 2f, p3.x, p3.y - dy / 2f, p3.x, p3.y)
                        } else {
                            path.moveTo(p0.x, p0.y)
                            path.cubicTo(p0.x + dx / 2f, p0.y, p3.x - dx / 2f, p3.y, p3.x, p3.y)
                        }
                        drawPath(path, wireColor, style = Stroke(width = 2f * d, cap = StrokeCap.Round))
                        val ah = 9f * d
                        drawLine(wireColor, Offset(p3.x - ah, p3.y - ah), p3, strokeWidth = 2f * d, cap = StrokeCap.Round)
                        drawLine(wireColor, Offset(p3.x + ah, p3.y - ah), p3, strokeWidth = 2f * d, cap = StrokeCap.Round)
                    }
                    nodes.forEach { node ->
                        anchorCenters(node).forEach { c ->
                            drawCircle(Color.White, radius = 8f * d, center = c)
                            drawCircle(anchorColor, radius = 6f * d, center = c)
                        }
                    }
                }
            )

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .pointerInput(tool) {
                        detectTransformGestures { centroid, pan, zoom, _ ->
                            if (tool == CanvasTool.SELECT || tool == CanvasTool.PAN) {
                                val newScale = (scale * zoom).coerceIn(0.08f, 8f)
                                val factor = newScale / scale
                                viewX = centroid.x - (centroid.x - viewX) * factor + pan.x
                                viewY = centroid.y - (centroid.y - viewY) * factor + pan.y
                                scale = newScale
                            }
                        }
                    }
                    .pointerInput(tool) {
                        detectTapGestures(onDoubleTap = { offset ->
                            if ((tool == CanvasTool.SELECT || tool == CanvasTool.PAN) && !uiState.readOnly) {
                                noteAt = screenToWorld(offset)
                                showNoteComposer = true
                            }
                        })
                    }
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .graphicsLayer(
                            scaleX = scale,
                            scaleY = scale,
                            translationX = viewX,
                            translationY = viewY
                        )
                ) {
                    nodes.forEach { node ->
                        key(node.id) {
                            Box(
                                modifier = Modifier.offset {
                                    IntOffset((node.x * d).roundToInt(), (node.y * d).roundToInt())
                                }
                            ) {
                                CanvasCard(
                                    node = node,
                                    onDrag = { dxPx, dyPx ->
                                        viewModel.moveNodeLocal(node.id, node.x + dxPx / d, node.y + dyPx / d)
                                    },
                                    onDragEnd = { viewModel.moveNodeCommit(node.id, node.x, node.y) },
                                    onOpenInspector = { inspectorNodeId = node.id },
                                    onFocus = { centerOn(node.x.toFloat() + 170f, node.y.toFloat() + 110f) },
                                    onDelete = { viewModel.deleteNode(node.id) },
                                    onRetry = { viewModel.retryNode(node.id) },
                                    onFollowup = { prompt -> viewModel.followupNode(node.id, prompt) },
                                    onReportHeight = { h ->
                                        if (cardHeights[node.id] != h) cardHeights[node.id] = h
                                    }
                                )
                            }
                        }
                    }
                    widgetObjs.forEach { obj ->
                        key(obj.str("id")) {
                            Box(
                                modifier = Modifier.offset {
                                    IntOffset((obj.num("x").toFloat() * d).roundToInt(), (obj.num("y").toFloat() * d).roundToInt())
                                }
                            ) {
                                CanvasWidgetCard(
                                    obj = obj,
                                    onDelete = {
                                        viewModel.deleteDrawObject(obj.str("id"))
                                    }
                                )
                            }
                        }
                    }
                }

                CanvasDrawOverlay(
                    tool = tool,
                    objects = drawObjs,
                    colorHex = drawColor,
                    width = drawWidth,
                    scale = scale,
                    viewX = viewX,
                    viewY = viewY,
                    density = density,
                    onCommit = { obj -> viewModel.setDrawObjects(uiState.drawObjects + obj) },
                    onEraseAt = { world ->
                        val hit = uiState.drawObjects.lastOrNull { o ->
                            drawObjectBounds(o)?.inflate(10f)?.contains(world) == true
                        }
                        if (hit != null) {
                            viewModel.deleteDrawObject(hit.str("id"))
                        }
                    },
                    onTapAnnotate = { t, world -> annotate = t to world },
                    modifier = Modifier.fillMaxSize()
                )
            }

            Column(
                modifier = Modifier
                    .align(Alignment.CenterEnd)
                    .padding(end = 12.dp, bottom = 96.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                ZoomFab(icon = Icons.Filled.Add, desc = "Zoom in") {
                    val s = (scale * 1.25f).coerceIn(0.08f, 8f)
                    val f = s / scale
                    viewX = viewportWpx / 2f - (viewportWpx / 2f - viewX) * f
                    viewY = viewportHpx / 2f - (viewportHpx / 2f - viewY) * f
                    scale = s
                }
                ZoomFab(icon = Icons.Filled.Remove, desc = "Zoom out") {
                    val s = (scale / 1.25f).coerceIn(0.08f, 8f)
                    val f = s / scale
                    viewX = viewportWpx / 2f - (viewportWpx / 2f - viewX) * f
                    viewY = viewportHpx / 2f - (viewportHpx / 2f - viewY) * f
                    scale = s
                }
                ZoomFab(icon = Icons.Filled.Fullscreen, desc = "Fit") { fitAll() }
            }

            if (showMoreMenu) {
                Box(modifier = Modifier.align(Alignment.TopEnd)) {
                    DropdownMenu(expanded = true, onDismissRequest = { showMoreMenu = false }) {
                        DropdownMenuItem(text = { Text("Templates") }, onClick = {
                            showMoreMenu = false
                            showTemplates = true
                        })
                        DropdownMenuItem(text = { Text("Save checkpoint") }, onClick = {
                            showMoreMenu = false
                            viewModel.createSnapshot("Quick checkpoint")
                        })
                        DropdownMenuItem(text = { Text("Export JSON") }, onClick = {
                            showMoreMenu = false
                            uiState.board?.let { b ->
                                viewModel.exportBoard("json") { text -> shareText(text, "application/json", b.title) }
                            }
                        })
                        DropdownMenuItem(text = { Text("Export Markdown") }, onClick = {
                            showMoreMenu = false
                            uiState.board?.let { b ->
                                viewModel.exportBoard("md") { text -> shareText(text, "text/markdown", b.title) }
                            }
                        })
                        DropdownMenuItem(text = { Text("Import") }, onClick = {
                            showMoreMenu = false
                            importLauncher.launch("application/json")
                        })
                        DropdownMenuItem(text = { Text("Share") }, onClick = {
                            showMoreMenu = false
                            showShare = true
                        })
                    }
                }
            }

            when {
                uiState.isLoading && nodes.isEmpty() -> {
                    Box(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.surface.copy(alpha = 0.7f)), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                uiState.error != null && nodes.isEmpty() -> {
                    Box(Modifier.fillMaxSize().padding(16.dp), contentAlignment = Alignment.Center) {
                        ErrorCard(message = uiState.error ?: "Something went wrong", onRetry = { viewModel.load() })
                    }
                }
                nodes.isEmpty() && drawObjs.isEmpty() && widgetObjs.isEmpty() && !uiState.isLoading -> {
                    Box(Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text(
                            if (uiState.readOnly) "This shared canvas is empty." else "Start with a question below — Neby will map it out.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
            } // BoxWithConstraints viewport

            if (!uiState.readOnly) {
                CanvasBottomBar(
                    draft = promptDraft,
                    onDraft = { promptDraft = it },
                    generating = uiState.isGenerating,
                    onSend = {
                        val goal = promptDraft.trim()
                        if (goal.isNotBlank()) {
                            promptDraft = ""
                            viewModel.sendGoal(goal) { newNodes ->
                                newNodes.firstOrNull()?.let { n ->
                                    centerOn(n.x.toFloat() + 170f, n.y.toFloat() + 110f)
                                }
                            }
                        }
                    }
                )
            }
        } // outer Column
    }

    inspectorNode?.let { node ->
        NodeInspectorSheet(
            node = node,
            onDismiss = { inspectorNodeId = null },
            onSave = { title, body, kind, meta ->
                viewModel.updateNode(node.id, title, body, kind, meta)
                inspectorNodeId = null
            },
            onDelete = {
                viewModel.deleteNode(node.id)
                inspectorNodeId = null
            },
            onRetry = {
                viewModel.retryNode(node.id)
                inspectorNodeId = null
            },
            onFocus = {
                centerOn(node.x.toFloat() + 170f, node.y.toFloat() + 110f)
                inspectorNodeId = null
            }
        )
    }

    if (showNoteComposer) {
        NoteComposerSheet(
            onDismiss = { showNoteComposer = false },
            onSave = { title, body, kind ->
                viewModel.createNote(title, body, kind, noteAt.x.toDouble(), noteAt.y.toDouble())
                showNoteComposer = false
            }
        )
    }

    if (showHistory) {
        HistorySheet(
            snapshots = uiState.snapshots,
            onCreate = { viewModel.createSnapshot(it.ifBlank { "Checkpoint" }) },
            onRestore = {
                viewModel.restoreSnapshot(it)
                showHistory = false
            },
            onDismiss = { showHistory = false }
        )
    }

    if (showShare) {
        ShareSheet(
            shareUrl = uiState.shareUrl,
            onEnable = { viewModel.shareBoard(false) },
            onRevoke = { viewModel.shareBoard(true) },
            onCopy = { url ->
                val cm = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                cm.setPrimaryClip(ClipData.newPlainText("Canvas link", url))
            },
            onDismiss = { showShare = false }
        )
    }

    if (showTemplates) {
        TemplatesSheet(
            templates = listState.templates,
            onPick = { template ->
                showTemplates = false
                listViewModel.createFromTemplate(template.key, template.name, onOpenBoard)
            },
            onDismiss = { showTemplates = false }
        )
    }

    if (showPalette) {
        CommandPaletteSheet(
            nodes = nodes,
            onPick = { node ->
                showPalette = false
                centerOn(node.x.toFloat() + 170f, node.y.toFloat() + 110f)
            },
            onDismiss = { showPalette = false }
        )
    }

    if (showWidgetPicker) {
        WidgetPickerDialog(
            onDismiss = { showWidgetPicker = false },
            onPick = { kind, topic ->
                showWidgetPicker = false
                val c = viewportCenterWorld()
                viewModel.buildWidget(kind, topic, c.x.toDouble(), c.y.toDouble())
            }
        )
    }

    annotate?.let { (t, world) ->
        AnnotateDialog(
            isSticky = t == CanvasTool.STICKY,
            onDismiss = { annotate = null },
            onConfirm = { text ->
                viewModel.setDrawObjects(
                    uiState.drawObjects + buildTextObject(t, world.x, world.y, text, drawColor, "#FFF9C4")
                )
                annotate = null
            }
        )
    }
}

@Composable
private fun CanvasToolbar(
    tool: CanvasTool,
    onTool: (CanvasTool) -> Unit,
    onNote: () -> Unit,
    onWidgets: () -> Unit,
    onHistory: () -> Unit,
    onShare: () -> Unit,
    onPalette: () -> Unit,
    onMore: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 6.dp)
            .horizontalScroll(rememberScrollState()),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        ToolButton(icon = Icons.Filled.TouchApp, desc = "Select", selected = tool == CanvasTool.SELECT, onClick = { onTool(CanvasTool.SELECT) })
        ToolButton(icon = Icons.Filled.PanTool, desc = "Pan", selected = tool == CanvasTool.PAN, onClick = { onTool(CanvasTool.PAN) })
        ToolbarDivider()
        ToolButton(icon = Icons.Filled.Edit, desc = "Pen", selected = tool == CanvasTool.PEN, onClick = { onTool(CanvasTool.PEN) })
        ToolButton(icon = Icons.Filled.Highlight, desc = "Highlighter", selected = tool == CanvasTool.HIGHLIGHTER, onClick = { onTool(CanvasTool.HIGHLIGHTER) })
        ToolButton(icon = Icons.Filled.CropSquare, desc = "Rectangle", selected = tool == CanvasTool.RECT, onClick = { onTool(CanvasTool.RECT) })
        ToolButton(icon = Icons.Outlined.Circle, desc = "Ellipse", selected = tool == CanvasTool.ELLIPSE, onClick = { onTool(CanvasTool.ELLIPSE) })
        ToolButton(icon = Icons.Filled.Remove, desc = "Line", selected = tool == CanvasTool.LINE, onClick = { onTool(CanvasTool.LINE) })
        ToolButton(icon = Icons.AutoMirrored.Filled.ArrowForward, desc = "Arrow", selected = tool == CanvasTool.ARROW, onClick = { onTool(CanvasTool.ARROW) })
        ToolButton(icon = Icons.Filled.TextFields, desc = "Text", selected = tool == CanvasTool.TEXT, onClick = { onTool(CanvasTool.TEXT) })
        ToolButton(icon = Icons.Outlined.StickyNote2, desc = "Sticky", selected = tool == CanvasTool.STICKY, onClick = { onTool(CanvasTool.STICKY) })
        ToolButton(icon = Icons.Outlined.DeleteSweep, desc = "Eraser", selected = tool == CanvasTool.ERASER, onClick = { onTool(CanvasTool.ERASER) })
        ToolbarDivider()
        ToolButton(icon = Icons.Filled.NoteAdd, desc = "Note", selected = false, onClick = onNote)
        ToolButton(icon = Icons.Filled.Widgets, desc = "Widgets", selected = false, onClick = onWidgets)
        ToolButton(icon = Icons.Filled.History, desc = "History", selected = false, onClick = onHistory)
        ToolButton(icon = Icons.Filled.Share, desc = "Share", selected = false, onClick = onShare)
        ToolButton(icon = Icons.Filled.Search, desc = "Find card", selected = false, onClick = onPalette)
        ToolButton(icon = Icons.Filled.MoreVert, desc = "More", selected = false, onClick = onMore)
    }
}

@Composable
private fun ToolbarDivider() {
    Box(
        modifier = Modifier
            .padding(horizontal = 4.dp)
            .width(1.dp)
            .height(24.dp)
            .background(MaterialTheme.colorScheme.outlineVariant)
    )
}

@Composable
private fun ToolButton(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    desc: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    val contentColor =
        if (selected) MaterialTheme.colorScheme.primary
        else MaterialTheme.colorScheme.onSurfaceVariant
    Box(
        modifier = Modifier
            .size(40.dp)
            .clip(CircleShape)
            .background(if (selected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = desc,
            tint = contentColor,
            modifier = Modifier.size(22.dp)
        )
    }
}

@Composable
private fun CanvasBottomBar(
    draft: String,
    onDraft: (String) -> Unit,
    generating: Boolean,
    onSend: () -> Unit
) {
    Column {
        if (generating) {
            LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
        }
        Surface(
            shape = RoundedCornerShape(28.dp),
            color = MaterialTheme.colorScheme.surfaceContainerLowest,
            shadowElevation = 8.dp,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp)
                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(28.dp))
        ) {
            OutlinedTextField(
                value = draft,
                onValueChange = onDraft,
                placeholder = { Text("What do you want to understand?") },
                singleLine = true,
                textStyle = MaterialTheme.typography.bodyMedium,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = RoundedCornerShape(28.dp),
                colors = androidx.compose.material3.TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent
                ),
                trailingIcon = {
                    Box(
                        modifier = Modifier
                            .size(32.dp)
                            .clip(CircleShape)
                            .background(
                                if (draft.isBlank() || generating) MaterialTheme.colorScheme.surfaceContainerHigh
                                else MaterialTheme.colorScheme.primary
                            )
                            .clickable(enabled = !generating && draft.isNotBlank(), onClick = onSend),
                        contentAlignment = Alignment.Center
                    ) {
                        if (generating) {
                            CircularProgressIndicator(
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(16.dp),
                                strokeWidth = 2.dp
                            )
                        } else {
                            Icon(
                                imageVector = Icons.Filled.ArrowUpward,
                                contentDescription = "Send",
                                tint = if (draft.isBlank()) MaterialTheme.colorScheme.onSurfaceVariant
                                else MaterialTheme.colorScheme.onPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                }
            )
        }
    }
}

@Composable
private fun ZoomFab(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    desc: String,
    onClick: () -> Unit
) {
    Surface(
        shape = CircleShape,
        color = MaterialTheme.colorScheme.surfaceContainerHigh,
        shadowElevation = 4.dp,
        modifier = Modifier.size(40.dp)
    ) {
        IconButton(onClick = onClick) {
            Icon(icon, contentDescription = desc, modifier = Modifier.size(20.dp))
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun WidgetPickerDialog(
    onDismiss: () -> Unit,
    onPick: (kind: String, topic: String) -> Unit
) {
    var kind by remember { mutableStateOf("quiz") }
    var topic by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add widget") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    CANVAS_WIDGET_KINDS.forEach { k ->
                        Text(
                            k,
                            style = MaterialTheme.typography.labelLarge,
                            color = if (kind == k) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (kind == k) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceContainerHigh)
                                .clickable { kind = k }
                                .padding(horizontal = 12.dp, vertical = 8.dp)
                        )
                    }
                }
                OutlinedTextField(value = topic, onValueChange = { topic = it }, label = { Text("Topic") }, singleLine = true, modifier = Modifier.fillMaxWidth())
            }
        },
        confirmButton = {
            TextButton(enabled = topic.isNotBlank(), onClick = { onPick(kind, topic.trim()) }) { Text("Place") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel") } }
    )
}
