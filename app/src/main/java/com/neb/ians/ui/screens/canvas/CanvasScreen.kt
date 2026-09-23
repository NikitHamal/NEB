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
            containerColor = if (isDark) Color(0xFF090D16) else Color(0xFFF8FAFC)
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
                        CanvasEdges(nodes = nodes, isDark = isDark)

                        // Nodes layer
                        nodes.forEach { node ->
                            CanvasCardItem(
                                node = node,
                                isSelected = node.id == selectedNodeId,
                                isConnectingSource = node.id == connectingSourceNodeId,
                                connectingDirection = if (node.id == connectingSourceNodeId) connectingSourceDirection else null,
                                onDrag = { dx, dy ->
                                    val dxDp = (dx / density) / viewportScale
                                    val dyDp = (dy / density) / viewportScale
                                    viewModel.moveNode(node.id, node.x + dxDp, node.y + dyDp)
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
    val dotColor = if (isDark) Color(0xFF334155) else Color(0xFFB8C2D1)
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
private fun CanvasEdges(nodes: List<CanvasNode>, isDark: Boolean) {
    val edgeColor = if (isDark) Color(0xFF64748B) else Color(0xFF94A3B8)
    val dotColor = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B)

    Canvas(modifier = Modifier.fillMaxSize()) {
        val drawnPairs = mutableSetOf<String>()

        nodes.forEach { nodeA ->
            // Check parentId
            nodeA.parentId?.let { pId ->
                val parent = nodes.find { it.id == pId }
                if (parent != null) {
                    val pairKey = if (parent.id < nodeA.id) "${parent.id}_${nodeA.id}" else "${nodeA.id}_${parent.id}"
                    if (pairKey !in drawnPairs) {
                        drawnPairs.add(pairKey)
                        drawCardConnection(parent, nodeA, edgeColor, dotColor)
                    }
                }
            }
            // Check explicit connections list
            nodeA.connections.forEach { targetId ->
                val target = nodes.find { it.id == targetId }
                if (target != null) {
                    val pairKey = if (nodeA.id < target.id) "${nodeA.id}_${target.id}" else "${target.id}_${nodeA.id}"
                    if (pairKey !in drawnPairs) {
                        drawnPairs.add(pairKey)
                        drawCardConnection(nodeA, target, edgeColor, dotColor)
                    }
                }
            }
        }
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawCardConnection(
    fromNode: CanvasNode,
    toNode: CanvasNode,
    edgeColor: Color,
    dotColor: Color
) {
    val cardWidth = 340f
    val centerAX = fromNode.x + cardWidth * 0.5f
    val centerAY = fromNode.y + 180f
    val centerBX = toNode.x + cardWidth * 0.5f
    val centerBY = toNode.y + 180f

    val dx = centerBX - centerAX
    val dy = centerBY - centerAY

    val startX: Float
    val startY: Float
    val endX: Float
    val endY: Float

    val path = Path()

    if (kotlin.math.abs(dx) >= kotlin.math.abs(dy)) {
        // Horizontal connection (matching reference Image 2)
        if (dx >= 0) {
            startX = (fromNode.x + cardWidth).dp.toPx()
            startY = (fromNode.y + 140f).dp.toPx()
            endX = toNode.x.dp.toPx()
            endY = (toNode.y + 140f).dp.toPx()
        } else {
            startX = fromNode.x.dp.toPx()
            startY = (fromNode.y + 140f).dp.toPx()
            endX = (toNode.x + cardWidth).dp.toPx()
            endY = (toNode.y + 140f).dp.toPx()
        }
        val cdx = (endX - startX) * 0.5f
        path.moveTo(startX, startY)
        path.cubicTo(
            startX + cdx, startY,
            endX - cdx, endY,
            endX, endY
        )
    } else {
        // Vertical connection
        if (dy >= 0) {
            startX = (fromNode.x + cardWidth * 0.5f).dp.toPx()
            startY = (fromNode.y + 360f).dp.toPx()
            endX = (toNode.x + cardWidth * 0.5f).dp.toPx()
            endY = toNode.y.dp.toPx()
        } else {
            startX = (fromNode.x + cardWidth * 0.5f).dp.toPx()
            startY = fromNode.y.dp.toPx()
            endX = (toNode.x + cardWidth * 0.5f).dp.toPx()
            endY = (toNode.y + 360f).dp.toPx()
        }
        val cdy = (endY - startY) * 0.5f
        path.moveTo(startX, startY)
        path.cubicTo(
            startX, startY + cdy,
            endX, endY - cdy,
            endX, endY
        )
    }

    drawPath(
        path = path,
        color = edgeColor,
        style = Stroke(width = 2.2f, cap = StrokeCap.Round)
    )

    // Subtle connection endpoint dots
    drawCircle(color = dotColor, radius = 3.5f, center = Offset(startX, startY))
    drawCircle(color = dotColor, radius = 3.5f, center = Offset(endX, endY))
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
        color = if (isDark) Color(0xFF1E293B) else Color.White,
        border = BorderStroke(
            1.dp,
            if (isDark) Color(0xFF334155) else Color(0xFFE2E8F0)
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
                    color = if (isDark) Color(0xFFF1F5F9) else Color(0xFF0F172A)
                ),
                decorationBox = { innerTextField ->
                    if (prompt.isEmpty()) {
                        Text(
                            text = "What do you want to understand?",
                            style = MaterialTheme.typography.bodyLarge.copy(fontSize = 15.sp),
                            color = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B),
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
                            isDark -> Color(0xFF334155)
                            else -> Color(0xFFEEF2F6)
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
                            isDark -> Color(0xFF64748B)
                            else -> Color(0xFF94A3B8)
                        },
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
    }
}
