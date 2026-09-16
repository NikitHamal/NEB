package com.neb.ians.ui.screens.canvas

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.CanvasBoard
import com.neb.ians.data.api.CanvasNode
import com.neb.ians.data.api.CanvasNodeMeta
import com.neb.ians.data.api.CanvasSnapshot
import com.neb.ians.data.api.CanvasSuggestion
import com.neb.ians.data.repository.CanvasRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import javax.inject.Inject

data class CanvasBoardUiState(
    val board: CanvasBoard? = null,
    val nodes: List<CanvasNode> = emptyList(),
    val drawObjects: List<JsonObject> = emptyList(),
    val snapshots: List<CanvasSnapshot> = emptyList(),
    val suggestions: List<CanvasSuggestion> = emptyList(),
    val shareUrl: String = "",
    val isLoading: Boolean = true,
    val isGenerating: Boolean = false,
    val isSavingObjects: Boolean = false,
    val error: String? = null,
    val snackbarMessage: String? = null,
    val readOnly: Boolean = false
)

@HiltViewModel
class CanvasBoardViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repository: CanvasRepository
) : ViewModel() {

    private val boardId: String = savedStateHandle.get<String>("boardId").orEmpty()
    private val sharedToken: String? = savedStateHandle.get<String>("token")?.takeIf { it.isNotBlank() }

    private val _uiState = MutableStateFlow(CanvasBoardUiState())
    val uiState: StateFlow<CanvasBoardUiState> = _uiState.asStateFlow()

    private var objectsSaveJob: Job? = null

    init { load() }

    fun load() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val token = sharedToken
            if (token != null) {
                repository.getSharedDetail(token).onSuccess { (board, _, nodes) ->
                    _uiState.update {
                        it.copy(board = board, nodes = nodes, isLoading = false, readOnly = true)
                    }
                }.onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
                return@launch
            }
            repository.getBoard(boardId).onSuccess { (board, nodes) ->
                _uiState.update { it.copy(board = board, nodes = nodes, isLoading = false) }
                launch { loadObjects() }
                launch { loadSnapshots() }
            }.onFailure { e ->
                _uiState.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }

    private suspend fun loadObjects() {
        repository.getObjects(boardId).onSuccess { objects ->
            _uiState.update { it.copy(drawObjects = objects) }
        }
    }

    fun refreshSnapshots() {
        viewModelScope.launch { loadSnapshots() }
    }

    private suspend fun loadSnapshots() {
        repository.getSnapshots(boardId).onSuccess { snapshots ->
            _uiState.update { it.copy(snapshots = snapshots) }
        }
    }

    fun sendGoal(goal: String, onNewNodes: (List<CanvasNode>) -> Unit = {}) {
        if (goal.isBlank() || _uiState.value.readOnly) return
        viewModelScope.launch {
            _uiState.update { it.copy(isGenerating = true) }
            repository.explore(boardId, goal).onSuccess { (_, nodes, questions) ->
                _uiState.update { it.copy(isGenerating = false, nodes = it.nodes + nodes) }
                onNewNodes(nodes)
                if (questions.isNotEmpty()) {
                    _uiState.update { it.copy(snackbarMessage = questions.first()) }
                }
            }.onFailure { e ->
                _uiState.update { it.copy(isGenerating = false, snackbarMessage = e.message) }
            }
        }
    }

    fun createAiNode(prompt: String, parentId: String? = null, x: Double? = null, y: Double? = null) {
        if (prompt.isBlank() || _uiState.value.readOnly) return
        viewModelScope.launch {
            _uiState.update { it.copy(isGenerating = true) }
            repository.createNode(boardId, prompt, parentId, x, y).onSuccess { node ->
                _uiState.update { it.copy(isGenerating = false, nodes = it.nodes + node) }
            }.onFailure { e ->
                _uiState.update { it.copy(isGenerating = false, snackbarMessage = e.message) }
            }
        }
    }

    fun createNote(title: String, body: String, kind: String, x: Double, y: Double, parentId: String? = null) {
        viewModelScope.launch {
            repository.createNote(boardId, title, body, kind, x, y, parentId).onSuccess { node ->
                _uiState.update { it.copy(nodes = it.nodes + node) }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun moveNodeLocal(nodeId: String, x: Double, y: Double) {
        _uiState.update { s ->
            s.copy(nodes = s.nodes.map { if (it.id == nodeId) it.copy(x = x, y = y) else it })
        }
    }

    fun moveNodeCommit(nodeId: String, x: Double, y: Double) {
        if (_uiState.value.readOnly) return
        viewModelScope.launch {
            repository.moveNode(nodeId, x, y).onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun deleteNode(nodeId: String) {
        viewModelScope.launch {
            repository.deleteNode(nodeId).onSuccess {
                _uiState.update { s -> s.copy(nodes = s.nodes.filterNot { it.id == nodeId }) }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun retryNode(nodeId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isGenerating = true) }
            repository.retryNode(nodeId).onSuccess { node ->
                _uiState.update { s ->
                    s.copy(isGenerating = false, nodes = s.nodes.map { if (it.id == nodeId) node else it })
                }
            }.onFailure { e ->
                _uiState.update { it.copy(isGenerating = false, snackbarMessage = e.message) }
            }
        }
    }

    fun followupNode(nodeId: String, prompt: String, x: Double? = null, y: Double? = null) {
        if (prompt.isBlank()) return
        viewModelScope.launch {
            _uiState.update { it.copy(isGenerating = true) }
            repository.followupNode(nodeId, prompt, x, y).onSuccess { node ->
                _uiState.update { it.copy(isGenerating = false, nodes = it.nodes + node) }
            }.onFailure { e ->
                _uiState.update { it.copy(isGenerating = false, snackbarMessage = e.message) }
            }
        }
    }

    fun updateNode(nodeId: String, title: String?, body: String?, kind: String?, meta: CanvasNodeMeta?) {
        viewModelScope.launch {
            repository.updateNode(nodeId, title, body, kind, meta).onSuccess { node ->
                _uiState.update { s ->
                    s.copy(nodes = s.nodes.map { if (it.id == nodeId) node else it })
                }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun setDrawObjects(objects: List<JsonObject>) {
        _uiState.update { it.copy(drawObjects = objects) }
        if (_uiState.value.readOnly) return
        objectsSaveJob?.cancel()
        objectsSaveJob = viewModelScope.launch {
            delay(800)
            _uiState.update { it.copy(isSavingObjects = true) }
            repository.saveObjects(boardId, _uiState.value.drawObjects).onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
            _uiState.update { it.copy(isSavingObjects = false) }
        }
    }

    fun deleteDrawObject(objectId: String) {
        setDrawObjects(_uiState.value.drawObjects.filterNot { (it["id"] as? kotlinx.serialization.json.JsonPrimitive)?.content == objectId })
    }

    fun loadSuggestions() {
        viewModelScope.launch {
            repository.getSuggestions(boardId).onSuccess { suggestions ->
                _uiState.update { it.copy(suggestions = suggestions) }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun createSnapshot(label: String) {
        viewModelScope.launch {
            repository.createSnapshot(boardId, label).onSuccess { snapshot ->
                _uiState.update { s -> s.copy(snapshots = listOf(snapshot) + s.snapshots) }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun restoreSnapshot(snapshotId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            repository.restoreSnapshot(boardId, snapshotId).onSuccess { nodes ->
                _uiState.update { it.copy(isLoading = false, nodes = nodes) }
                launch { loadObjects() }
            }.onFailure { e ->
                _uiState.update { it.copy(isLoading = false, snackbarMessage = e.message) }
            }
        }
    }

    fun shareBoard(revoke: Boolean = false) {
        viewModelScope.launch {
            repository.shareBoard(boardId, revoke).onSuccess { (enabled, url) ->
                _uiState.update { it.copy(shareUrl = if (enabled) url else "") }
                if (!enabled) _uiState.update { it.copy(snackbarMessage = "Share link revoked") }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun exportBoard(format: String, onResult: (String) -> Unit) {
        viewModelScope.launch {
            repository.exportBoard(boardId, format).onSuccess { text ->
                onResult(text)
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun importBoard(canvasJson: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            repository.importBoard(boardId, canvasJson).onSuccess { nodes ->
                _uiState.update { it.copy(isLoading = false, nodes = nodes) }
            }.onFailure { e ->
                _uiState.update { it.copy(isLoading = false, snackbarMessage = e.message) }
            }
        }
    }

    fun buildWidget(kind: String, topic: String, x: Double, y: Double) {
        viewModelScope.launch {
            _uiState.update { it.copy(isGenerating = true) }
            repository.getWidgetContent(boardId, kind, topic).onSuccess { content ->
                val widget = kotlinx.serialization.json.buildJsonObject {
                    put("id", kotlinx.serialization.json.JsonPrimitive("o_" + System.currentTimeMillis()))
                    put("type", kotlinx.serialization.json.JsonPrimitive("widget"))
                    put("kind", kotlinx.serialization.json.JsonPrimitive(kind))
                    put("x", kotlinx.serialization.json.JsonPrimitive(x))
                    put("y", kotlinx.serialization.json.JsonPrimitive(y))
                    put("w", kotlinx.serialization.json.JsonPrimitive(280.0))
                    put("h", kotlinx.serialization.json.JsonPrimitive(200.0))
                    put("topic", kotlinx.serialization.json.JsonPrimitive(topic))
                    put("state", content)
                }
                setDrawObjects(_uiState.value.drawObjects + widget)
                _uiState.update { it.copy(isGenerating = false) }
            }.onFailure { e ->
                _uiState.update { it.copy(isGenerating = false, snackbarMessage = e.message) }
            }
        }
    }

    fun cloneShared(onCloned: (String) -> Unit) {
        val token = sharedToken ?: return
        viewModelScope.launch {
            repository.cloneShared(token).onSuccess { board ->
                onCloned(board.id)
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message) }
            }
        }
    }

    fun consumeSnackbar() {
        _uiState.update { it.copy(snackbarMessage = null) }
    }
}
