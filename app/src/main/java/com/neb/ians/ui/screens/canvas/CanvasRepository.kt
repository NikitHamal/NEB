package com.neb.ians.ui.screens.canvas

import android.content.Context
import android.content.SharedPreferences
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CanvasRepository @Inject constructor(
    @ApplicationContext private val context: Context,
    private val authRepository: AuthRepository
) {
    private val prefs: SharedPreferences = context.getSharedPreferences("nebians_canvas_prefs", Context.MODE_PRIVATE)

    private val _boards = MutableStateFlow<List<CanvasBoard>>(emptyList())
    val boards: StateFlow<List<CanvasBoard>> = _boards.asStateFlow()

    init {
        loadBoardsFromDisk()
    }

    private fun loadBoardsFromDisk() {
        val rawBoards = prefs.getString("canvas_boards_meta", null)
        if (rawBoards.isNullOrBlank()) {
            _boards.value = emptyList()
        } else {
            try {
                val jsonArray = JSONArray(rawBoards)
                val list = mutableListOf<CanvasBoard>()
                for (i in 0 until jsonArray.length()) {
                    val obj = jsonArray.getJSONObject(i)
                    list.add(
                        CanvasBoard(
                            id = obj.getString("id"),
                            title = obj.getString("title"),
                            nodeCount = obj.optInt("nodeCount", 0),
                            updatedAt = obj.optLong("updatedAt", System.currentTimeMillis()),
                            isLocal = obj.optBoolean("isLocal", true)
                        )
                    )
                }
                _boards.value = list
            } catch (e: Exception) {
                e.printStackTrace()
                _boards.value = emptyList()
            }
        }
    }

    private fun saveBoardsToDisk(list: List<CanvasBoard>) {
        val jsonArray = JSONArray()
        list.forEach { b ->
            val obj = JSONObject()
            obj.put("id", b.id)
            obj.put("title", b.title)
            obj.put("nodeCount", b.nodeCount)
            obj.put("updatedAt", b.updatedAt)
            obj.put("isLocal", b.isLocal)
            jsonArray.put(obj)
        }
        prefs.edit().putString("canvas_boards_meta", jsonArray.toString()).apply()
    }

    suspend fun createBoard(title: String, templateKey: String? = null): CanvasBoard = withContext(Dispatchers.IO) {
        val id = "board_${System.currentTimeMillis()}_${UUID.randomUUID().toString().take(5)}"
        val cleanTitle = title.trim().ifBlank { "Untitled Canvas" }
        val newBoard = CanvasBoard(
            id = id,
            title = cleanTitle,
            nodeCount = 0,
            updatedAt = System.currentTimeMillis()
        )
        val updated = listOf(newBoard) + _boards.value
        _boards.value = updated
        saveBoardsToDisk(updated)

        if (templateKey != null) {
            val template = CanvasTemplates.getTemplates().find { it.key == templateKey }
            if (template != null) {
                val nodesWithBoardId = template.initialNodes.map { node ->
                    node.copy(
                        id = if (node.id.startsWith("node_")) "node_${UUID.randomUUID().toString().take(6)}" else "${node.id}_${UUID.randomUUID().toString().take(4)}",
                        boardId = id
                    )
                }
                saveNodesForBoard(id, nodesWithBoardId)
                updateBoardNodeCount(id, nodesWithBoardId.size)
            }
        }
        newBoard
    }

    suspend fun renameBoard(boardId: String, newTitle: String) = withContext(Dispatchers.IO) {
        val updated = _boards.value.map {
            if (it.id == boardId) it.copy(title = newTitle.trim().ifBlank { "Untitled Canvas" }, updatedAt = System.currentTimeMillis())
            else it
        }
        _boards.value = updated
        saveBoardsToDisk(updated)
    }

    suspend fun deleteBoard(boardId: String) = withContext(Dispatchers.IO) {
        val updated = _boards.value.filterNot { it.id == boardId }
        _boards.value = updated
        saveBoardsToDisk(updated)
        prefs.edit().remove("canvas_nodes_$boardId").apply()
    }

    suspend fun duplicateBoard(boardId: String): CanvasBoard = withContext(Dispatchers.IO) {
        val original = _boards.value.find { it.id == boardId }
        val newTitle = if (original != null) "${original.title} (Copy)" else "Untitled Canvas (Copy)"
        val newBoard = createBoard(newTitle)
        val originalNodes = getNodesForBoard(boardId)
        val clonedNodes = originalNodes.map { node ->
            node.copy(
                id = "node_${UUID.randomUUID().toString().take(8)}",
                boardId = newBoard.id
            )
        }
        saveNodesForBoard(newBoard.id, clonedNodes)
        updateBoardNodeCount(newBoard.id, clonedNodes.size)
        newBoard
    }

    suspend fun getNodesForBoard(boardId: String): List<CanvasNode> = withContext(Dispatchers.IO) {
        val raw = prefs.getString("canvas_nodes_$boardId", null)
        if (raw.isNullOrBlank()) {
            if (boardId == "board_welcome") {
                saveInitialWelcomeNodes("board_welcome")
                return@withContext getNodesForBoard("board_welcome")
            }
            return@withContext emptyList()
        }
        try {
            CanvasJsonSerializer.deserializeNodes(raw)
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    suspend fun saveNodesForBoard(boardId: String, nodes: List<CanvasNode>) = withContext(Dispatchers.IO) {
        val json = CanvasJsonSerializer.serializeNodes(nodes)
        prefs.edit().putString("canvas_nodes_$boardId", json).apply()
        updateBoardNodeCount(boardId, nodes.size)
    }

    private fun updateBoardNodeCount(boardId: String, count: Int) {
        val updated = _boards.value.map {
            if (it.id == boardId) it.copy(nodeCount = count, updatedAt = System.currentTimeMillis())
            else it
        }
        _boards.value = updated
        saveBoardsToDisk(updated)
    }

    private fun saveInitialWelcomeNodes(boardId: String) {
        val template = CanvasTemplates.getTemplates().find { it.key == "concept-master" } ?: return
        val nodes = template.initialNodes.map { it.copy(boardId = boardId) }
        val json = CanvasJsonSerializer.serializeNodes(nodes)
        prefs.edit().putString("canvas_nodes_$boardId", json).apply()
    }
}
