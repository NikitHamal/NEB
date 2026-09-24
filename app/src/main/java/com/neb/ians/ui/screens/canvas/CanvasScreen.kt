package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.rememberDrawerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlin.math.hypot
import kotlin.math.roundToInt

// ---------------------------------------------------------------------------
// The board.
//
// A white sheet, a grid of dots, and whatever you have made on it. The chrome
// keeps to the edges — back and the boards drawer at the top corners with the
// tools between them, the history and delete under them on the right, and
// Neby's prompt along the bottom. Nothing floats in the middle of the board
// except the work.
// ---------------------------------------------------------------------------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CanvasScreen(
    onNavigateBack: () -> Unit,
    viewModel: CanvasViewModel = hiltViewModel()
) {
    val isDark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val boards by viewModel.boards.collectAsStateWithLifecycle()
    val activeBoard by viewModel.activeBoard.collectAsStateWithLifecycle()
    val nodes by viewModel.nodes.collectAsStateWithLifecycle()
    val viewportTx by viewModel.viewportTx.collectAsStateWithLifecycle()
    val viewportTy by viewModel.viewportTy.collectAsStateWithLifecycle()
    val viewportScale by viewModel.viewportScale.collectAsStateWithLifecycle()
    val isGenerating by viewModel.isGenerating.collectAsStateWithLifecycle()
    val selectedNodeId by viewModel.selectedNodeId.collectAsStateWithLifecycle()
    val activeDetailNode by viewModel.activeDetailNode.collectAsStateWithLifecycle()
    val sidebarOpen by viewModel.sidebarOpen.collectAsStateWithLifecycle()
    val templatePickerOpen by viewModel.templatePickerOpen.collectAsStateWithLifecycle()
    val newBoardDialogOpen by viewModel.newBoardDialogOpen.collectAsStateWithLifecycle()
    val renameBoardTarget by viewModel.renameBoardTarget.collectAsStateWithLifecycle()
    val deleteBoardTarget by viewModel.deleteBoardTarget.collectAsStateWithLifecycle()
    val globalPrompt by viewModel.globalPrompt.collectAsStateWithLifecycle()
    val speedMode by viewModel.speedMode.collectAsStateWithLifecycle()
    val webSearch by viewModel.webSearch.collectAsStateWithLifecycle()
    val connectingSourceNodeId by viewModel.connectingSourceNodeId.collectAsStateWithLifecycle()
    val connectingSourceDirection by viewModel.connectingSourceDirection.collectAsStateWithLifecycle()
    val toastMessage by viewModel.toastMessage.collectAsStateWithLifecycle()
    val nodeHeights by viewModel.nodeHeights.collectAsStateWithLifecycle()
    val canUndo by viewModel.canUndo.collectAsStateWithLifecycle()
    val canRedo by viewModel.canRedo.collectAsStateWithLifecycle()

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    LaunchedEffect(sidebarOpen) {
        if (sidebarOpen) drawerState.open() else drawerState.close()
    }
    LaunchedEffect(drawerState.isOpen) {
        viewModel.setSidebarOpen(drawerState.isOpen)
    }

    val snackbarHostState = remember { SnackbarHostState() }
    LaunchedEffect(toastMessage) {
        toastMessage?.let { snackbarHostState.showSnackbar(it) }
    }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            CanvasSidebarDrawer(
                boards = boards,
                activeBoard = activeBoard,
                onSelectBoard = { viewModel.selectBoard(it) },
                onNewBoard = { viewModel.setNewBoardDialogOpen(true) },
                onOpenTemplates = { viewModel.setTemplatePickerOpen(true) },
                onRenameBoard = { viewModel.setRenameBoardTarget(it) },
                onDeleteBoard = { viewModel.setDeleteBoardTarget(it) },
                onClose = { viewModel.setSidebarOpen(false) },
                onNavigateBack = onNavigateBack
            )
        }
    ) {
        Scaffold(
            snackbarHost = { SnackbarHost(snackbarHostState) },
            topBar = {
                CanvasTopBar(
                    scale = viewportScale,
                    hasSelection = selectedNodeId != null,
                    onNavigateBack = onNavigateBack,
                    onToggleSidebar = { viewModel.setSidebarOpen(!sidebarOpen) },
                    onFitView = { viewModel.fitContent() },
                    onZoomIn = { viewModel.zoomIn() },
                    onZoomOut = { viewModel.zoomOut() },
                    onResetZoom = { viewModel.resetZoom() },
                    onAutoLayout = { viewModel.autoLayout() },
                    onDuplicateSelected = { viewModel.duplicateSelectedNode() },
                    onRenameBoard = { viewModel.setRenameBoardTarget(activeBoard) },
                    onNewBoard = { viewModel.setNewBoardDialogOpen(true) },
                    onOpenTemplates = { viewModel.setTemplatePickerOpen(true) },
                    onDeleteBoard = { activeBoard?.let { viewModel.setDeleteBoardTarget(it) } }
                )
            },
            containerColor = canvasBoardColor(isDark)
        ) { innerPadding ->
            BoxWithConstraints(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
            ) {
                val density = LocalDensity.current.density
                val containerWidth = constraints.maxWidth.toFloat()
                val containerHeight = constraints.maxHeight.toFloat()

                LaunchedEffect(containerWidth, containerHeight, density) {
                    if (containerWidth > 0 && containerHeight > 0) {
                        viewModel.setContainerDimensions(containerWidth, containerHeight, density)
                    }
                }

                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .pointerInput(Unit) {
                            detectTransformGestures { centroid, pan, zoom, _ ->
                                viewModel.updateTransform(centroid, pan, zoom)
                            }
                        }
                        .pointerInput(Unit) {
                            detectTapGestures(onTap = { viewModel.setSelectedNodeId(null) })
                        }
                ) {
                    CanvasGrid(isDark = isDark, tx = viewportTx, ty = viewportTy, scale = viewportScale)

                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .graphicsLayer {
                                translationX = viewportTx
                                translationY = viewportTy
                                scaleX = viewportScale
                                scaleY = viewportScale
                                transformOrigin = TransformOrigin(0f, 0f)
                            }
                    ) {
                        CanvasEdges(
                            nodes = nodes,
                            heights = nodeHeights,
                            selectedNodeId = selectedNodeId,
                            isDark = isDark
                        )

                        nodes.forEach { node ->
                            CanvasCardItem(
                                node = node,
                                isSelected = node.id == selectedNodeId,
                                isConnectingSource = node.id == connectingSourceNodeId,
                                connectingDirection = if (node.id == connectingSourceNodeId) connectingSourceDirection else null,
                                onDragStart = { viewModel.beginNodeDrag() },
                                onDrag = { dx, dy -> viewModel.dragNodeBy(node.id, dx, dy) },
                                onDragEnd = { viewModel.commitNodePosition(node.id) },
                                onSelect = { viewModel.onNodeClicked(node.id) },
                                onExpand = { viewModel.setActiveDetailNode(node) },
                                onDuplicate = { viewModel.duplicateNode(node.id) },
                                onColorChange = { viewModel.updateNodeColor(node.id, it) },
                                onBranch = { dir, prompt -> viewModel.createChildNode(node.id, prompt, dir) },
                                onConnect = { dir -> viewModel.startConnecting(node.id, dir) },
                                onMeasured = { viewModel.reportNodeHeight(node.id, it) },
                                modifier = Modifier.offset {
                                    IntOffset(node.x.dp.roundToPx(), node.y.dp.roundToPx())
                                }
                            )
                        }
                    }
                }

                CanvasQuickActions(
                    canUndo = canUndo,
                    canRedo = canRedo,
                    hasSelection = selectedNodeId != null,
                    onUndo = { viewModel.undo() },
                    onRedo = { viewModel.redo() },
                    onDeleteSelected = { viewModel.deleteSelectedNode() },
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(horizontal = 12.dp, vertical = 10.dp)
                )

                CanvasPromptBar(
                    prompt = globalPrompt,
                    isGenerating = isGenerating,
                    speedMode = speedMode,
                    webSearch = webSearch,
                    onPromptChange = { viewModel.setGlobalPrompt(it) },
                    onSpeedModeChange = { viewModel.setSpeedMode(it) },
                    onWebSearchChange = { viewModel.setWebSearch(it) },
                    onSubmit = { viewModel.submitGlobalPrompt() },
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .padding(start = 14.dp, end = 14.dp, bottom = 14.dp)
                )
            }
        }
    }

    if (newBoardDialogOpen) {
        NewBoardDialog(
            onDismiss = { viewModel.setNewBoardDialogOpen(false) },
            onConfirm = { viewModel.createBoard(it) }
        )
    }

    renameBoardTarget?.let { board ->
        RenameBoardDialog(
            initialTitle = board.title,
            onDismiss = { viewModel.setRenameBoardTarget(null) },
            onConfirm = { viewModel.renameBoard(it) }
        )
    }

    deleteBoardTarget?.let { board ->
        DeleteBoardDialog(
            boardTitle = board.title,
            onDismiss = { viewModel.setDeleteBoardTarget(null) },
            onConfirm = { viewModel.confirmDeleteBoard() }
        )
    }

    if (templatePickerOpen) {
        TemplatePickerModalSheet(
            onDismiss = { viewModel.setTemplatePickerOpen(false) },
            onSelectTemplate = { template -> viewModel.createBoard(template.name, template.key) }
        )
    }

    activeDetailNode?.let { node ->
        NodeDetailDialog(
            node = node,
            onDismiss = { viewModel.setActiveDetailNode(null) }
        )
    }
}

/** The board is paper: white in the day, ink at night. */
fun canvasBoardColor(isDark: Boolean): Color =
    if (isDark) Color(0xFF0A0A0B) else Color.White

@Composable
private fun CanvasGrid(isDark: Boolean, tx: Float, ty: Float, scale: Float) {
    val density = LocalDensity.current
    val dotColor = if (isDark) Color(0xFF232327) else Color(0xFFE0E0E6)
    Canvas(modifier = Modifier.fillMaxSize()) {
        val stepPx = with(density) { 26.dp.toPx() } * scale
        if (stepPx < 10f) return@Canvas
        val radiusPx = with(density) { 1.5.dp.toPx() } * scale.coerceIn(0.65f, 1.35f)

        val startX = (tx % stepPx + stepPx) % stepPx
        val startY = (ty % stepPx + stepPx) % stepPx

        var x = startX
        while (x < size.width) {
            var y = startY
            while (y < size.height) {
                drawCircle(color = dotColor, radius = radiusPx, center = Offset(x, y))
                y += stepPx
            }
            x += stepPx
        }
    }
}

@Composable
private fun CanvasEdges(
    nodes: List<CanvasNode>,
    heights: Map<String, Float>,
    selectedNodeId: String?,
    isDark: Boolean
) {
    val idleColor = if (isDark) Color(0xFF4A4A52) else Color(0xFFBFBFC8)
    val activeColor = if (isDark) Color(0xFFE8E8EC) else Color(0xFF2B2B30)

    Canvas(modifier = Modifier.fillMaxSize()) {
        val byId = nodes.associateBy { it.id }
        val seen = HashSet<String>()
        val links = ArrayList<Pair<CanvasNode, CanvasNode>>()

        fun link(from: CanvasNode, to: CanvasNode) {
            val key = if (from.id < to.id) "${from.id}|${to.id}" else "${to.id}|${from.id}"
            if (seen.add(key)) links.add(from to to)
        }

        nodes.forEach { node ->
            node.parentId?.let { parentId ->
                byId[parentId]?.let { parent -> link(parent, node) }
            }
            node.connections.forEach { targetId ->
                byId[targetId]?.let { target -> link(node, target) }
            }
        }

        links.forEach { (from, to) ->
            val active = selectedNodeId == from.id || selectedNodeId == to.id
            drawCardConnection(
                from = boundsOf(from, heights),
                to = boundsOf(to, heights),
                color = if (active) activeColor else idleColor,
                emphasised = active
            )
        }
    }
}

private fun CanvasSide.outwardX(): Float = when (this) {
    CanvasSide.Left -> -1f
    CanvasSide.Right -> 1f
    else -> 0f
}

private fun CanvasSide.outwardY(): Float = when (this) {
    CanvasSide.Top -> -1f
    CanvasSide.Bottom -> 1f
    else -> 0f
}

/**
 * A wire between two cards.
 *
 * Both ends are pushed a hair inside the card they belong to. The cards are
 * drawn over this layer, so the wire disappears under the border instead of
 * stopping short of it — which is the difference between a connection and two
 * things near each other.
 */
private fun DrawScope.drawCardConnection(
    from: CanvasBounds,
    to: CanvasBounds,
    color: Color,
    emphasised: Boolean
) {
    val (fromSide, toSide) = routeSides(from, to)
    val start = from.anchor(fromSide)
    val end = to.anchor(toSide)
    val bite = 3.dp.toPx()

    val sx = start.x.dp.toPx() - fromSide.outwardX() * bite
    val sy = start.y.dp.toPx() - fromSide.outwardY() * bite
    val ex = end.x.dp.toPx() - toSide.outwardX() * bite
    val ey = end.y.dp.toPx() - toSide.outwardY() * bite

    val span = hypot(ex - sx, ey - sy)
    val curve = (span * 0.42f).coerceIn(44.dp.toPx(), 190.dp.toPx())

    val path = Path().apply {
        moveTo(sx, sy)
        cubicTo(
            sx + fromSide.outwardX() * curve,
            sy + fromSide.outwardY() * curve,
            ex + toSide.outwardX() * curve,
            ey + toSide.outwardY() * curve,
            ex,
            ey
        )
    }

    drawPath(
        path = path,
        color = color,
        style = Stroke(
            width = if (emphasised) 2.2.dp.toPx() else 1.6.dp.toPx(),
            cap = StrokeCap.Round
        )
    )

    val headLength = 9.dp.toPx()
    val headWidth = 5.dp.toPx()
    val nx = toSide.outwardX()
    val ny = toSide.outwardY()
    val baseX = ex + nx * headLength
    val baseY = ey + ny * headLength
    val head = Path().apply {
        moveTo(ex, ey)
        lineTo(baseX - ny * headWidth, baseY + nx * headWidth)
        lineTo(baseX + ny * headWidth, baseY - nx * headWidth)
        close()
    }
    drawPath(path = head, color = color)
}

internal fun zoomLabel(scale: Float): String = "${(scale * 100).roundToInt()}%"
