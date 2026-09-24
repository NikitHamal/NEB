package com.neb.ians.ui.screens.canvas

import androidx.compose.ui.geometry.Offset
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.util.UUID
import javax.inject.Inject
import kotlin.math.max
import kotlin.math.min

@HiltViewModel
class CanvasViewModel @Inject constructor(
    private val repository: CanvasRepository,
    private val aiGenerator: CanvasAiGenerator,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    val boards: StateFlow<List<CanvasBoard>> = repository.boards

    private val _activeBoard = MutableStateFlow<CanvasBoard?>(null)
    val activeBoard: StateFlow<CanvasBoard?> = _activeBoard.asStateFlow()

    private val _nodes = MutableStateFlow<List<CanvasNode>>(emptyList())
    val nodes: StateFlow<List<CanvasNode>> = _nodes.asStateFlow()

    private val _viewportTx = MutableStateFlow(0f)
    val viewportTx: StateFlow<Float> = _viewportTx.asStateFlow()

    private val _viewportTy = MutableStateFlow(0f)
    val viewportTy: StateFlow<Float> = _viewportTy.asStateFlow()

    private val _viewportScale = MutableStateFlow(1f)
    val viewportScale: StateFlow<Float> = _viewportScale.asStateFlow()

    private val _isGenerating = MutableStateFlow(false)
    val isGenerating: StateFlow<Boolean> = _isGenerating.asStateFlow()

    private val _selectedNodeId = MutableStateFlow<String?>(null)
    val selectedNodeId: StateFlow<String?> = _selectedNodeId.asStateFlow()

    private val _activeDetailNode = MutableStateFlow<CanvasNode?>(null)
    val activeDetailNode: StateFlow<CanvasNode?> = _activeDetailNode.asStateFlow()

    private val _sidebarOpen = MutableStateFlow(false)
    val sidebarOpen: StateFlow<Boolean> = _sidebarOpen.asStateFlow()

    private val _templatePickerOpen = MutableStateFlow(false)
    val templatePickerOpen: StateFlow<Boolean> = _templatePickerOpen.asStateFlow()

    private val _newBoardDialogOpen = MutableStateFlow(false)
    val newBoardDialogOpen: StateFlow<Boolean> = _newBoardDialogOpen.asStateFlow()

    private val _renameBoardTarget = MutableStateFlow<CanvasBoard?>(null)
    val renameBoardTarget: StateFlow<CanvasBoard?> = _renameBoardTarget.asStateFlow()

    private val _deleteBoardTarget = MutableStateFlow<CanvasBoard?>(null)
    val deleteBoardTarget: StateFlow<CanvasBoard?> = _deleteBoardTarget.asStateFlow()

    private val _minimapVisible = MutableStateFlow(false)
    val minimapVisible: StateFlow<Boolean> = _minimapVisible.asStateFlow()

    private val _globalPrompt = MutableStateFlow("")
    val globalPrompt: StateFlow<String> = _globalPrompt.asStateFlow()

    private val _speedMode = MutableStateFlow("fast")
    val speedMode: StateFlow<String> = _speedMode.asStateFlow()

    private val _webSearch = MutableStateFlow(false)
    val webSearch: StateFlow<Boolean> = _webSearch.asStateFlow()

    private val _connectingSourceNodeId = MutableStateFlow<String?>(null)
    val connectingSourceNodeId: StateFlow<String?> = _connectingSourceNodeId.asStateFlow()

    private val _connectingSourceDirection = MutableStateFlow<String?>(null)
    val connectingSourceDirection: StateFlow<String?> = _connectingSourceDirection.asStateFlow()

    private val _toastMessage = MutableStateFlow<String?>(null)
    val toastMessage: StateFlow<String?> = _toastMessage.asStateFlow()

    private val _nodeHeights = MutableStateFlow<Map<String, Float>>(emptyMap())
    val nodeHeights: StateFlow<Map<String, Float>> = _nodeHeights.asStateFlow()

    fun reportNodeHeight(nodeId: String, heightDp: Float) {
        if (heightDp <= 0f) return
        val known = _nodeHeights.value[nodeId]
        if (known != null && kotlin.math.abs(known - heightDp) < 1f) return
        _nodeHeights.value = _nodeHeights.value + (nodeId to heightDp)
    }

    private fun boundsFor(node: CanvasNode): CanvasBounds = boundsOf(node, _nodeHeights.value)

    private fun heightFor(nodeId: String): Float =
        _nodeHeights.value[nodeId] ?: CanvasCardFallbackHeight

    private var _containerWidth: Float = 1080f
    private var _containerHeight: Float = 1920f
    private var _containerDensity: Float = 2.75f

    fun setContainerDimensions(w: Float, h: Float, d: Float) {
        if (w > 0f && h > 0f) {
            val wasDefault = _containerWidth == 1080f && _containerHeight == 1920f
            _containerWidth = w
            _containerHeight = h
            _containerDensity = d
            if (wasDefault && _nodes.value.isNotEmpty()) {
                fitContent()
            }
        }
    }

    init {
        val initialBoardId: String? = savedStateHandle["boardId"]
        viewModelScope.launch {
            repository.boards.collect { bList ->
                if (bList.isNotEmpty()) {
                    if (!initialBoardId.isNullOrBlank()) {
                        val target = bList.find { it.id == initialBoardId }
                        if (target != null && _activeBoard.value?.id != target.id) {
                            selectBoard(target)
                        }
                    } else if (_activeBoard.value == null) {
                        selectBoard(bList.first())
                    }
                }
            }
        }
    }

    fun selectBoard(board: CanvasBoard) {
        _activeBoard.value = board
        _sidebarOpen.value = false
        viewModelScope.launch {
            val list = repository.getNodesForBoard(board.id)
            _nodes.value = list
            fitContent(list)
        }
    }

    fun setSidebarOpen(open: Boolean) {
        _sidebarOpen.value = open
    }

    fun setTemplatePickerOpen(open: Boolean) {
        _templatePickerOpen.value = open
    }

    fun setNewBoardDialogOpen(open: Boolean) {
        _newBoardDialogOpen.value = open
    }

    fun setRenameBoardTarget(board: CanvasBoard?) {
        _renameBoardTarget.value = board
    }

    fun setDeleteBoardTarget(board: CanvasBoard?) {
        _deleteBoardTarget.value = board
    }

    fun setMinimapVisible(visible: Boolean) {
        _minimapVisible.value = visible
    }

    fun setGlobalPrompt(text: String) {
        _globalPrompt.value = text
    }

    fun setSpeedMode(mode: String) {
        _speedMode.value = mode
    }

    fun setWebSearch(enabled: Boolean) {
        _webSearch.value = enabled
    }

    fun setSelectedNodeId(id: String?) {
        _selectedNodeId.value = id
    }

    fun startConnecting(nodeId: String, direction: String) {
        if (_connectingSourceNodeId.value == nodeId && _connectingSourceDirection.value == direction) {
            _connectingSourceNodeId.value = null
            _connectingSourceDirection.value = null
        } else {
            _connectingSourceNodeId.value = nodeId
            _connectingSourceDirection.value = direction
            _selectedNodeId.value = nodeId
            showToast("Tap another card to connect")
        }
    }

    fun cancelConnecting() {
        _connectingSourceNodeId.value = null
        _connectingSourceDirection.value = null
    }

    fun onNodeClicked(nodeId: String) {
        val sourceId = _connectingSourceNodeId.value
        if (sourceId != null && sourceId != nodeId) {
            toggleConnection(sourceId, nodeId)
        } else {
            _selectedNodeId.value = nodeId
            if (sourceId == nodeId) {
                cancelConnecting()
            }
        }
    }

    fun toggleConnection(sourceId: String, targetId: String) {
        val board = _activeBoard.value ?: return
        val currentNodes = _nodes.value
        val source = currentNodes.find { it.id == sourceId } ?: return
        val target = currentNodes.find { it.id == targetId } ?: return

        val isAlreadyConnected = source.connections.contains(targetId) ||
                target.connections.contains(sourceId) ||
                target.parentId == sourceId ||
                source.parentId == targetId

        val updated = if (isAlreadyConnected) {
            currentNodes.map { node ->
                when (node.id) {
                    sourceId -> node.copy(
                        connections = node.connections.filterNot { it == targetId },
                        parentId = if (node.parentId == targetId) null else node.parentId
                    )
                    targetId -> node.copy(
                        connections = node.connections.filterNot { it == sourceId },
                        parentId = if (node.parentId == sourceId) null else node.parentId
                    )
                    else -> node
                }
            }
        } else {
            currentNodes.map { node ->
                if (node.id == sourceId) {
                    node.copy(connections = (node.connections + targetId).distinct())
                } else node
            }
        }

        _nodes.value = updated
        _connectingSourceNodeId.value = null
        _connectingSourceDirection.value = null
        viewModelScope.launch {
            repository.saveNodesForBoard(board.id, updated)
        }
        showToast(if (isAlreadyConnected) "Disconnected" else "Cards connected")
    }

    fun setActiveDetailNode(node: CanvasNode?) {
        _activeDetailNode.value = node
    }

    fun showToast(msg: String) {
        _toastMessage.value = msg
        viewModelScope.launch {
            delay(2200)
            if (_toastMessage.value == msg) _toastMessage.value = null
        }
    }

    fun createBoard(title: String, templateKey: String? = null) {
        viewModelScope.launch {
            val board = repository.createBoard(title, templateKey)
            _newBoardDialogOpen.value = false
            _templatePickerOpen.value = false
            selectBoard(board)
            showToast("Canvas created: ${board.title}")
        }
    }

    fun renameBoard(newTitle: String) {
        val target = _renameBoardTarget.value ?: return
        viewModelScope.launch {
            repository.renameBoard(target.id, newTitle)
            _renameBoardTarget.value = null
            if (_activeBoard.value?.id == target.id) {
                _activeBoard.value = _activeBoard.value?.copy(title = newTitle)
            }
            showToast("Renamed to $newTitle")
        }
    }

    fun confirmDeleteBoard() {
        val target = _deleteBoardTarget.value ?: return
        viewModelScope.launch {
            repository.deleteBoard(target.id)
            _deleteBoardTarget.value = null
            val remaining = repository.boards.value
            if (remaining.isNotEmpty()) {
                selectBoard(remaining.first())
            } else {
                createBoard("My Canvas")
            }
            showToast("Canvas deleted")
        }
    }

    fun submitGlobalPrompt() {
        val prompt = _globalPrompt.value.trim()
        if (prompt.isBlank() || _isGenerating.value) return
        val currentBoard = _activeBoard.value ?: return
        _globalPrompt.value = ""

        viewModelScope.launch {
            _isGenerating.value = true
            val roots = _nodes.value.filter { it.parentId.isNullOrBlank() }
            val baseX = if (roots.isEmpty()) {
                40f
            } else {
                (roots.maxOfOrNull { it.x } ?: 0f) + CanvasCardWidth + CanvasGapX
            }
            val baseY = 40f

            val placeholder = CanvasNode(
                id = "tmp_${System.currentTimeMillis()}",
                boardId = currentBoard.id,
                parentId = null,
                prompt = prompt,
                title = prompt.take(38),
                status = "generating",
                x = baseX,
                y = baseY,
                webSearchEnabled = _webSearch.value,
                modelUsed = _speedMode.value
            )
            val withPlaceholder = _nodes.value + placeholder
            _nodes.value = withPlaceholder

            val outcome = generateNode(
                prompt = prompt,
                boardId = currentBoard.id,
                parentId = null,
                baseX = baseX,
                baseY = baseY,
                contextTitle = null
            )

            val finalized = _nodes.value.filterNot { it.id == placeholder.id } + outcome.node
            _nodes.value = finalized
            repository.saveNodesForBoard(currentBoard.id, finalized)
            _isGenerating.value = false
            fitContent(finalized)
            showToast(outcome.message)

            if (_nodes.value.size == 1 && currentBoard.title.startsWith("Untitled")) {
                val newTitle = prompt.take(28)
                repository.renameBoard(currentBoard.id, newTitle)
                _activeBoard.value = _activeBoard.value?.copy(title = newTitle)
            }
        }
    }

    fun createChildNode(parentId: String, prompt: String, direction: String = "bottom") {
        val currentBoard = _activeBoard.value ?: return
        val parent = _nodes.value.find { it.id == parentId } ?: return

        viewModelScope.launch {
            val siblings = _nodes.value.count { it.parentId == parentId }
            val (baseX, baseY) = childOrigin(boundsFor(parent), direction, siblings)

            val placeholder = CanvasNode(
                id = "tmp_${System.currentTimeMillis()}",
                boardId = currentBoard.id,
                parentId = parentId,
                prompt = prompt,
                title = prompt.take(38),
                status = "generating",
                x = baseX,
                y = baseY,
                webSearchEnabled = _webSearch.value,
                modelUsed = _speedMode.value
            )
            _nodes.value = _nodes.value + placeholder

            val outcome = generateNode(
                prompt = prompt,
                boardId = currentBoard.id,
                parentId = parentId,
                baseX = baseX,
                baseY = baseY,
                contextTitle = parent.title
            )

            val finalized = _nodes.value.filterNot { it.id == placeholder.id } + outcome.node
            _nodes.value = finalized
            repository.saveNodesForBoard(currentBoard.id, finalized)
            fitContent(finalized)
            showToast(outcome.message)
        }
    }

    private data class GenerationOutcome(val node: CanvasNode, val message: String)

    private suspend fun generateNode(
        prompt: String,
        boardId: String,
        parentId: String?,
        baseX: Float,
        baseY: Float,
        contextTitle: String?
    ): GenerationOutcome {
        return try {
            val node = aiGenerator.generate(
                prompt = prompt,
                boardId = boardId,
                parentId = parentId,
                baseX = baseX,
                baseY = baseY,
                webSearch = _webSearch.value,
                speedMode = _speedMode.value,
                context = contextTitle
            )
            GenerationOutcome(node, "Neby mapped it out")
        } catch (e: Exception) {
            val fallback = CanvasKnowledgeEngine.generateNode(
                prompt = prompt,
                boardId = boardId,
                parentId = parentId,
                baseX = baseX,
                baseY = baseY,
                webSearch = _webSearch.value,
                speedMode = _speedMode.value
            )
            val reason = (e as? CanvasAiException)?.message ?: "Neby is unreachable"
            GenerationOutcome(fallback, "$reason — showing an offline outline")
        }
    }

    fun dragNodeBy(nodeId: String, dxPx: Float, dyPx: Float) {
        val scale = _viewportScale.value.coerceAtLeast(0.05f)
        val density = _containerDensity.coerceAtLeast(0.5f)
        val dxDp = dxPx / density / scale
        val dyDp = dyPx / density / scale
        if (dxDp == 0f && dyDp == 0f) return
        val now = System.currentTimeMillis()
        _nodes.value = _nodes.value.map {
            if (it.id == nodeId) it.copy(x = it.x + dxDp, y = it.y + dyDp, updatedAt = now) else it
        }
    }

    fun moveNode(nodeId: String, newX: Float, newY: Float) {
        _nodes.value = _nodes.value.map {
            if (it.id == nodeId) it.copy(x = newX, y = newY, updatedAt = System.currentTimeMillis())
            else it
        }
    }

    fun commitNodePosition(nodeId: String) {
        val board = _activeBoard.value ?: return
        viewModelScope.launch {
            repository.saveNodesForBoard(board.id, _nodes.value)
        }
    }

    fun updateNodeColor(nodeId: String, colorKey: String) {
        val board = _activeBoard.value ?: return
        val updated = _nodes.value.map {
            if (it.id == nodeId) it.copy(color = colorKey, updatedAt = System.currentTimeMillis())
            else it
        }
        _nodes.value = updated
        viewModelScope.launch {
            repository.saveNodesForBoard(board.id, updated)
        }
    }

    fun duplicateNode(nodeId: String) {
        val board = _activeBoard.value ?: return
        val target = _nodes.value.find { it.id == nodeId } ?: return
        val dup = target.copy(
            id = "node_${System.currentTimeMillis()}_${UUID.randomUUID().toString().take(4)}",
            x = target.x + 60f,
            y = target.y + 60f,
            title = "${target.title} (Copy)"
        )
        val updated = _nodes.value + dup
        _nodes.value = updated
        viewModelScope.launch {
            repository.saveNodesForBoard(board.id, updated)
            showToast("Node duplicated")
        }
    }

    fun deleteNode(nodeId: String) {
        val board = _activeBoard.value ?: return
        val updated = _nodes.value.filterNot { it.id == nodeId }.map {
            it.copy(
                parentId = if (it.parentId == nodeId) null else it.parentId,
                connections = it.connections.filterNot { c -> c == nodeId }
            )
        }
        _nodes.value = updated
        if (_selectedNodeId.value == nodeId) _selectedNodeId.value = null
        if (_connectingSourceNodeId.value == nodeId) cancelConnecting()
        viewModelScope.launch {
            repository.saveNodesForBoard(board.id, updated)
            showToast("Card deleted")
        }
    }

    fun autoLayout() {
        val board = _activeBoard.value ?: return
        val currentNodes = _nodes.value
        if (currentNodes.isEmpty()) return

        val roots = currentNodes.filter { it.parentId.isNullOrBlank() }
        val nonRoots = currentNodes.filterNot { it.parentId.isNullOrBlank() }

        val newNodes = mutableListOf<CanvasNode>()
        var currentRootX = 40f
        val cardWidth = CanvasCardWidth
        val gapX = CanvasGapX
        val gapY = CanvasGapY

        roots.forEach { root ->
            val children = nonRoots.filter { it.parentId == root.id }
            val childrenCount = children.size
            val totalSpanWidth = if (childrenCount > 0) {
                childrenCount * cardWidth + (childrenCount - 1) * gapX
            } else {
                cardWidth
            }
            val rootCenterX = currentRootX + (totalSpanWidth - cardWidth) / 2f
            newNodes.add(root.copy(x = rootCenterX, y = 40f))

            val childY = 40f + heightFor(root.id) + gapY
            children.forEachIndexed { idx, child ->
                newNodes.add(child.copy(x = currentRootX + idx * (cardWidth + gapX), y = childY))
            }
            currentRootX += totalSpanWidth + 80f
        }

        nonRoots.filterNot { nr -> roots.any { r -> r.id == nr.parentId } }.forEachIndexed { idx, orphan ->
            newNodes.add(orphan.copy(x = currentRootX + idx * (cardWidth + gapX), y = 40f))
        }

        _nodes.value = newNodes
        viewModelScope.launch {
            repository.saveNodesForBoard(board.id, newNodes)
            fitContent(newNodes)
            showToast("Organized layout")
        }
    }

    fun fitContent(nodeList: List<CanvasNode> = _nodes.value) {
        val d = _containerDensity
        val cw = _containerWidth
        val ch = _containerHeight

        if (nodeList.isEmpty() || cw <= 0f || ch <= 0f) {
            _viewportTx.value = 40f * d
            _viewportTy.value = 40f * d
            _viewportScale.value = 0.85f
            return
        }

        var minXDp = Float.MAX_VALUE
        var minYDp = Float.MAX_VALUE
        var maxXDp = Float.MIN_VALUE
        var maxYDp = Float.MIN_VALUE

        nodeList.forEach { n ->
            minXDp = min(minXDp, n.x)
            minYDp = min(minYDp, n.y)
            maxXDp = max(maxXDp, n.x + CanvasCardWidth)
            maxYDp = max(maxYDp, n.y + heightFor(n.id))
        }

        val contentWidthPx = (maxXDp - minXDp) * d
        val contentHeightPx = (maxYDp - minYDp) * d

        val paddingPx = 36f * d
        val availableWidth = (cw - paddingPx * 2).coerceAtLeast(100f)
        val availableHeight = (ch - paddingPx * 2).coerceAtLeast(100f)

        val scaleX = availableWidth / contentWidthPx
        val scaleY = availableHeight / contentHeightPx
        val targetScale = min(scaleX, scaleY).coerceIn(0.25f, 1.15f)

        val fittedWidthPx = contentWidthPx * targetScale
        val fittedHeightPx = contentHeightPx * targetScale

        val targetTx = (cw - fittedWidthPx) / 2f - (minXDp * d) * targetScale
        val targetTy = (ch - fittedHeightPx) / 2f - (minYDp * d) * targetScale

        _viewportScale.value = targetScale
        _viewportTx.value = targetTx
        _viewportTy.value = targetTy
    }

    fun updateTransform(centroid: Offset, pan: Offset, zoomChange: Float) {
        val oldScale = _viewportScale.value
        val newScale = (oldScale * zoomChange).coerceIn(0.25f, 2.5f)
        val cx = centroid.x
        val cy = centroid.y
        val tx = _viewportTx.value
        val ty = _viewportTy.value

        val newTx = cx - (cx - tx) * (newScale / oldScale) + pan.x
        val newTy = cy - (cy - ty) * (newScale / oldScale) + pan.y

        _viewportScale.value = newScale
        _viewportTx.value = newTx
        _viewportTy.value = newTy
    }

    fun zoomIn() {
        applyZoomAt(Offset(_containerWidth / 2f, _containerHeight / 2f), 1.25f)
    }

    fun zoomOut() {
        applyZoomAt(Offset(_containerWidth / 2f, _containerHeight / 2f), 1f / 1.25f)
    }

    private fun applyZoomAt(center: Offset, factor: Float) {
        val oldScale = _viewportScale.value
        val newScale = (oldScale * factor).coerceIn(0.25f, 2.5f)
        val cx = center.x
        val cy = center.y
        val tx = _viewportTx.value
        val ty = _viewportTy.value

        val newTx = cx - (cx - tx) * (newScale / oldScale)
        val newTy = cy - (cy - ty) * (newScale / oldScale)

        _viewportScale.value = newScale
        _viewportTx.value = newTx
        _viewportTy.value = newTy
    }
}
