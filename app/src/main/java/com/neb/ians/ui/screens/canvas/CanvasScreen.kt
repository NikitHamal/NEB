package com.neb.ians.ui.screens.canvas

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlin.math.roundToInt
import kotlin.math.hypot
import androidx.compose.ui.graphics.drawscope.DrawScope

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
    val minimapVisible by viewModel.minimapVisible.collectAsStateWithLifecycle()
    val globalPrompt by viewModel.globalPrompt.collectAsStateWithLifecycle()
    val connectingSourceNodeId by viewModel.connectingSourceNodeId.collectAsStateWithLifecycle()
    val connectingSourceDirection by viewModel.connectingSourceDirection.collectAsStateWithLifecycle()
    val toastMessage by viewModel.toastMessage.collectAsStateWithLifecycle()
    val nodeHeights by viewModel.nodeHeights.collectAsStateWithLifecycle()

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
                    activeBoard = activeBoard,
                    scale = viewportScale,
                    minimapVisible = minimapVisible,
                    onToggleDrawer = { viewModel.setSidebarOpen(!sidebarOpen) },
                    onFitView = { viewModel.fitContent() },
                    onAutoLayout = { viewModel.autoLayout() },
                    onToggleMinimap = { viewModel.setMinimapVisible(!minimapVisible) },
                    onZoomIn = { viewModel.zoomIn() },
                    onZoomOut = { viewModel.zoomOut() },
                    onRenameBoard = { viewModel.setRenameBoardTarget(activeBoard) },
                    onNavigateBack = onNavigateBack
                )
            },
            containerColor = if (isDark) Color(0xFF0A0A0B) else Color(0xFFF7F7F9)
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

                // Infinite Canvas Surface with Grid Dots and Gestures
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .pointerInput(Unit) {
                            detectTransformGestures { centroid, pan, zoom, _ ->
                                viewModel.updateTransform(centroid, pan, zoom)
                            }
                        }
                ) {
                    // Background Dot Grid
                    CanvasGrid(isDark = isDark, tx = viewportTx, ty = viewportTy, scale = viewportScale)

                    // World Container
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
                        // Edges layer: SVG-like Bezier curves
                        CanvasEdges(
                            nodes = nodes,
                            heights = nodeHeights,
                            selectedNodeId = selectedNodeId,
                            isDark = isDark
                        )

                        // Nodes layer
                        nodes.forEach { node ->
                            CanvasCardItem(
                                node = node,
                                isSelected = node.id == selectedNodeId,
                                isConnectingSource = node.id == connectingSourceNodeId,
                                connectingDirection = if (node.id == connectingSourceNodeId) connectingSourceDirection else null,
                                onDrag = { dx, dy ->
                                    viewModel.dragNodeBy(node.id, dx, dy)
                                },
                                onDragEnd = { viewModel.commitNodePosition(node.id) },
                                onSelect = { viewModel.onNodeClicked(node.id) },
                                onExpand = { viewModel.setActiveDetailNode(node) },
                                onDuplicate = { viewModel.duplicateNode(node.id) },
                                onDelete = { viewModel.deleteNode(node.id) },
                                onColorChange = { viewModel.updateNodeColor(node.id, it) },
                                onBranch = { dir, prompt ->
                                    viewModel.createChildNode(node.id, prompt, dir)
                                },
                                onConnect = { dir ->
                                    viewModel.startConnecting(node.id, dir)
                                },
                                onMeasured = { viewModel.reportNodeHeight(node.id, it) },
                                modifier = Modifier.offset {
                                    IntOffset(node.x.dp.roundToPx(), node.y.dp.roundToPx())
                                }
                            )
                        }
                    }
                }

                // Minimap radar overlay
                AnimatedVisibility(
                    visible = minimapVisible,
                    enter = fadeIn(),
                    exit = fadeOut(),
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(16.dp)
                ) {
                    CanvasMinimap(
                        nodes = nodes,
                        heights = nodeHeights,
                        viewportTx = viewportTx,
                        viewportTy = viewportTy,
                        viewportScale = viewportScale,
                        onDismiss = { viewModel.setMinimapVisible(false) },
                        onJumpTo = { _, _ -> }
                    )
                }

                // Floating Neby AI Prompt Bar at Bottom
                CanvasBottomPromptBar(
                    prompt = globalPrompt,
                    isGenerating = isGenerating,
                    isDark = isDark,
                    onPromptChange = { viewModel.setGlobalPrompt(it) },
                    onSubmit = { viewModel.submitGlobalPrompt() },
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .padding(bottom = 16.dp, start = 16.dp, end = 16.dp)
                )
            }
        }
    }

    // Dialogs
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
            onSelectTemplate = { template ->
                viewModel.createBoard(template.name, template.key)
            }
        )
    }

    activeDetailNode?.let { node ->
        NodeDetailDialog(
            node = node,
            onDismiss = { viewModel.setActiveDetailNode(null) }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun CanvasTopBar(
    activeBoard: CanvasBoard?,
    scale: Float,
    minimapVisible: Boolean,
    onToggleDrawer: () -> Unit,
    onFitView: () -> Unit,
    onAutoLayout: () -> Unit,
    onToggleMinimap: () -> Unit,
    onZoomIn: () -> Unit,
    onZoomOut: () -> Unit,
    onRenameBoard: () -> Unit,
    onNavigateBack: () -> Unit
) {
    TopAppBar(
        title = {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier
                    .clip(RoundedCornerShape(8.dp))
                    .clickable(onClick = onRenameBoard)
                    .padding(horizontal = 6.dp, vertical = 4.dp)
            ) {
                Text(
                    text = activeBoard?.title ?: "NEBians Canvas",
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    maxLines = 1
                )
                Icon(
                    imageVector = Icons.Outlined.Edit,
                    contentDescription = "Rename",
                    modifier = Modifier
                        .padding(start = 6.dp)
                        .size(15.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        },
        navigationIcon = {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                }
                IconButton(onClick = onToggleDrawer) {
                    Icon(Icons.Filled.Menu, contentDescription = "Boards")
                }
            }
        },
        actions = {
            IconButton(onClick = onFitView) {
                Icon(Icons.Outlined.FitScreen, contentDescription = "Fit View")
            }
            IconButton(onClick = onAutoLayout) {
                Icon(Icons.Outlined.AccountTree, contentDescription = "Auto Layout")
            }
            IconButton(onClick = onToggleMinimap) {
                Icon(
                    imageVector = Icons.Outlined.Map,
                    contentDescription = "Minimap",
                    tint = if (minimapVisible) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            // Zoom Controls Pill
            Surface(
                shape = RoundedCornerShape(99.dp),
                color = MaterialTheme.colorScheme.surfaceContainerHigh,
                modifier = Modifier.padding(end = 8.dp)
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(horizontal = 4.dp)
                ) {
                    IconButton(onClick = onZoomOut, modifier = Modifier.size(28.dp)) {
                        Icon(Icons.Filled.Remove, contentDescription = "Zoom Out", modifier = Modifier.size(14.dp))
                    }
                    Text(
                        text = "${(scale * 100).roundToInt()}%",
                        style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold),
                        modifier = Modifier.padding(horizontal = 4.dp)
                    )
                    IconButton(onClick = onZoomIn, modifier = Modifier.size(28.dp)) {
                        Icon(Icons.Filled.Add, contentDescription = "Zoom In", modifier = Modifier.size(14.dp))
                    }
                }
            }
        },
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = MaterialTheme.colorScheme.surface
        )
    )
}

@Composable
private fun CanvasGrid(isDark: Boolean, tx: Float, ty: Float, scale: Float) {
    val density = LocalDensity.current
    val dotColor = if (isDark) Color(0xFF26262A) else Color(0xFFDCDCE0)
    Canvas(modifier = Modifier.fillMaxSize()) {
        val stepPx = with(density) { 26.dp.toPx() } * scale
        if (stepPx < 10f) return@Canvas
        val radiusPx = with(density) { 1.6.dp.toPx() } * scale.coerceIn(0.65f, 1.35f)

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
    val idleColor = if (isDark) Color(0xFF55555C) else Color(0xFFC2C2C9)
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

private fun DrawScope.drawCardConnection(
    from: CanvasBounds,
    to: CanvasBounds,
    color: Color,
    emphasised: Boolean
) {
    val (fromSide, toSide) = routeSides(from, to)
    val start = from.anchor(fromSide)
    val end = to.anchor(toSide)

    val sx = start.x.dp.toPx()
    val sy = start.y.dp.toPx()
    val ex = end.x.dp.toPx()
    val ey = end.y.dp.toPx()

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
            width = if (emphasised) 2.4.dp.toPx() else 1.7.dp.toPx(),
            cap = StrokeCap.Round
        )
    )

    drawCircle(
        color = color,
        radius = if (emphasised) 4.dp.toPx() else 3.dp.toPx(),
        center = Offset(sx, sy)
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

@Composable
private fun CanvasBottomPromptBar(
    prompt: String,
    isGenerating: Boolean,
    isDark: Boolean,
    onPromptChange: (String) -> Unit,
    onSubmit: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier
            .widthIn(max = 680.dp)
            .fillMaxWidth()
            .shadow(
                elevation = 8.dp,
                shape = RoundedCornerShape(99.dp),
                spotColor = Color(0x1A000000)
            )
            .clip(RoundedCornerShape(99.dp)),
        color = if (isDark) Color(0xFF18181B) else Color.White,
        border = BorderStroke(
            1.dp,
            if (isDark) Color(0xFF26262A) else Color(0xFFE9E9EB)
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 22.dp, end = 6.dp, top = 6.dp, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            BasicTextField(
                value = prompt,
                onValueChange = onPromptChange,
                modifier = Modifier.weight(1f),
                singleLine = true,
                maxLines = 1,
                textStyle = MaterialTheme.typography.bodyLarge.copy(
                    fontSize = 15.sp,
                    color = if (isDark) Color(0xFFF5F5F6) else Color(0xFF0A0A0B)
                ),
                decorationBox = { innerTextField ->
                    if (prompt.isEmpty()) {
                        Text(
                            text = "What do you want to understand?",
                            style = MaterialTheme.typography.bodyLarge.copy(fontSize = 15.sp),
                            color = if (isDark) Color(0xFF9B9BA1) else Color(0xFF5C5C61),
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    innerTextField()
                }
            )

            val hasText = prompt.isNotBlank()
            IconButton(
                onClick = onSubmit,
                enabled = hasText && !isGenerating,
                modifier = Modifier
                    .size(38.dp)
                    .clip(CircleShape)
                    .background(
                        when {
                            hasText && !isGenerating -> MaterialTheme.colorScheme.primary
                            isDark -> Color(0xFF26262A)
                            else -> Color(0xFFF1F1F3)
                        }
                    )
            ) {
                if (isGenerating) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = MaterialTheme.colorScheme.primary
                    )
                } else {
                    Icon(
                        imageVector = Icons.Filled.ArrowUpward,
                        contentDescription = "Send",
                        tint = when {
                            hasText -> Color.White
                            isDark -> Color(0xFF6E6E75)
                            else -> Color(0xFF9B9BA1)
                        },
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
    }
}
