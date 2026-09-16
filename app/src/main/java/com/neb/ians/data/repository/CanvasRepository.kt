package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.CanvasBatchMoveNode
import com.neb.ians.data.api.CanvasBatchMoveRequest
import com.neb.ians.data.api.CanvasBoard
import com.neb.ians.data.api.CanvasBoardCreateRequest
import com.neb.ians.data.api.CanvasBoardTitleRequest
import com.neb.ians.data.api.CanvasDigDeeperRequest
import com.neb.ians.data.api.CanvasExploreRequest
import com.neb.ians.data.api.CanvasFollowupRequest
import com.neb.ians.data.api.CanvasImportRequest
import com.neb.ians.data.api.CanvasNode
import com.neb.ians.data.api.CanvasNodeCreateRequest
import com.neb.ians.data.api.CanvasNodeMeta
import com.neb.ians.data.api.CanvasNodeMoveRequest
import com.neb.ians.data.api.CanvasNodeUpdateRequest
import com.neb.ians.data.api.CanvasNoteCreateRequest
import com.neb.ians.data.api.CanvasObjectsSaveRequest
import com.neb.ians.data.api.CanvasShareRequest
import com.neb.ians.data.api.CanvasSnapshot
import com.neb.ians.data.api.CanvasSnapshotCreateRequest
import com.neb.ians.data.api.CanvasSuggestion
import com.neb.ians.data.api.CanvasTemplate
import com.neb.ians.data.api.CanvasTemplateCreateRequest
import com.neb.ians.data.api.CanvasWidgetRequest
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import retrofit2.HttpException
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CanvasRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    private val json = Json { ignoreUnknownKeys = true }

    private suspend fun token(): String? = authRepository.getBearerToken()

    private fun mapError(e: Exception): String {
        if (e is HttpException && e.code() == 402) {
            return "Out of Neby credits — top up to keep generating"
        }
        return ApiErrorMapper.mapException(e)
    }

    private fun <T> fail(e: Exception): Result<T> = Result.failure(IllegalStateException(mapError(e)))

    suspend fun getBoards(): Result<List<CanvasBoard>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        Result.success(apiService.getCanvasBoards(t).boards)
    } catch (e: Exception) { fail(e) }

    suspend fun createBoard(title: String): Result<CanvasBoard> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.createCanvasBoard(t, CanvasBoardCreateRequest(title.ifBlank { "Untitled canvas" }))
        res.board?.takeIf { it.id.isNotBlank() }?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not create board"))
    } catch (e: Exception) { fail(e) }

    suspend fun getBoard(boardId: String): Result<Pair<CanvasBoard, List<CanvasNode>>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.getCanvasBoard(t, boardId)
        val board = res.board?.takeIf { it.id.isNotBlank() }
            ?: return Result.failure(IllegalStateException(res.error ?: "Board not found"))
        Result.success(board to res.nodes)
    } catch (e: Exception) { fail(e) }

    suspend fun renameBoard(boardId: String, title: String): Result<CanvasBoard> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.updateCanvasBoard(t, boardId, CanvasBoardTitleRequest(title))
        res.board?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not rename board"))
    } catch (e: Exception) { fail(e) }

    suspend fun deleteBoard(boardId: String): Result<Unit> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.deleteCanvasBoard(t, boardId)
        if (res.ok) Result.success(Unit) else Result.failure(IllegalStateException(res.error ?: "Could not delete board"))
    } catch (e: Exception) { fail(e) }

    suspend fun shareBoard(boardId: String, revoke: Boolean = false): Result<Pair<Boolean, String>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.shareCanvasBoard(t, boardId, CanvasShareRequest(revoke))
        if (res.error != null && !res.enabled) Result.failure(IllegalStateException(res.error))
        else Result.success(res.enabled to res.url)
    } catch (e: Exception) { fail(e) }

    suspend fun createNode(
        boardId: String,
        prompt: String,
        parentId: String? = null,
        x: Double? = null,
        y: Double? = null
    ): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.createCanvasNode(t, boardId, CanvasNodeCreateRequest(prompt, parentId, x, y))
        res.node?.takeIf { it.id.isNotBlank() }?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Generation failed"))
    } catch (e: Exception) { fail(e) }

    suspend fun createNote(
        boardId: String,
        title: String,
        body: String,
        kind: String = "note",
        x: Double? = null,
        y: Double? = null,
        parentId: String? = null,
        meta: CanvasNodeMeta? = null
    ): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.createCanvasNote(t, boardId, CanvasNoteCreateRequest(title, body, kind, x, y, parentId, meta))
        res.node?.takeIf { it.id.isNotBlank() }?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not create note"))
    } catch (e: Exception) { fail(e) }

    suspend fun moveNode(nodeId: String, x: Double, y: Double): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.moveCanvasNode(t, nodeId, CanvasNodeMoveRequest(x, y))
        res.node?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not move card"))
    } catch (e: Exception) { fail(e) }

    suspend fun deleteNode(nodeId: String): Result<Unit> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.deleteCanvasNode(t, nodeId)
        if (res.ok) Result.success(Unit) else Result.failure(IllegalStateException(res.error ?: "Could not delete card"))
    } catch (e: Exception) { fail(e) }

    suspend fun retryNode(nodeId: String): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.retryCanvasNode(t, nodeId)
        res.node?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Retry failed"))
    } catch (e: Exception) { fail(e) }

    suspend fun followupNode(nodeId: String, prompt: String, x: Double? = null, y: Double? = null): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.followupCanvasNode(t, nodeId, CanvasFollowupRequest(prompt, x, y))
        res.node?.takeIf { it.id.isNotBlank() }?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Follow-up failed"))
    } catch (e: Exception) { fail(e) }

    suspend fun digDeeper(nodeId: String, selectedText: String, prompt: String = ""): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.digDeeperCanvasNode(t, nodeId, CanvasDigDeeperRequest(selectedText, prompt))
        res.node?.takeIf { it.id.isNotBlank() }?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Dig deeper failed"))
    } catch (e: Exception) { fail(e) }

    suspend fun updateNode(
        nodeId: String,
        title: String? = null,
        body: String? = null,
        kind: String? = null,
        meta: CanvasNodeMeta? = null
    ): Result<CanvasNode> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.updateCanvasNode(t, nodeId, CanvasNodeUpdateRequest(title, body, kind, meta))
        res.node?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not save card"))
    } catch (e: Exception) { fail(e) }

    suspend fun batchMove(boardId: String, nodes: List<Pair<String, Pair<Double, Double>>>): Result<Unit> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.batchMoveCanvasNodes(
            t, boardId,
            CanvasBatchMoveRequest("freeform", nodes.map { CanvasBatchMoveNode(it.first, it.second.first, it.second.second) })
        )
        if (res.ok) Result.success(Unit) else Result.failure(IllegalStateException(res.error ?: "Could not rearrange"))
    } catch (e: Exception) { fail(e) }

    suspend fun getSnapshots(boardId: String): Result<List<CanvasSnapshot>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        Result.success(apiService.getCanvasSnapshots(t, boardId).snapshots)
    } catch (e: Exception) { fail(e) }

    suspend fun createSnapshot(boardId: String, label: String): Result<CanvasSnapshot> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.createCanvasSnapshot(t, boardId, CanvasSnapshotCreateRequest(label))
        res.snapshot?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not save checkpoint"))
    } catch (e: Exception) { fail(e) }

    suspend fun restoreSnapshot(boardId: String, snapshotId: String): Result<List<CanvasNode>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.restoreCanvasSnapshot(t, boardId, snapshotId)
        if (res.ok) Result.success(res.nodes)
        else Result.failure(IllegalStateException(res.error ?: "Could not restore checkpoint"))
    } catch (e: Exception) { fail(e) }

    suspend fun exportBoard(boardId: String, format: String): Result<String> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        Result.success(apiService.exportCanvasBoard(t, boardId, format).string())
    } catch (e: Exception) { fail(e) }

    suspend fun importBoard(boardId: String, canvasJson: String): Result<List<CanvasNode>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val element = json.parseToJsonElement(canvasJson)
        val canvas = (element as? JsonObject)?.get("canvas") as? JsonObject ?: element as? JsonObject
            ?: return Result.failure(IllegalStateException("Invalid canvas file"))
        val res = apiService.importCanvasBoard(t, boardId, CanvasImportRequest(canvas))
        if (res.ok) Result.success(res.nodes)
        else Result.failure(IllegalStateException(res.error ?: "Import failed"))
    } catch (e: Exception) { fail(e) }

    suspend fun getTemplates(): Result<List<CanvasTemplate>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        Result.success(apiService.getCanvasTemplates(t).templates)
    } catch (e: Exception) { fail(e) }

    suspend fun createFromTemplate(template: String, title: String): Result<Pair<CanvasBoard, List<CanvasNode>>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.createCanvasFromTemplate(t, CanvasTemplateCreateRequest(template, title.ifBlank { "Untitled canvas" }))
        val board = res.board?.takeIf { it.id.isNotBlank() }
            ?: return Result.failure(IllegalStateException(res.error ?: "Could not create from template"))
        Result.success(board to res.nodes)
    } catch (e: Exception) { fail(e) }

    suspend fun explore(boardId: String, goal: String, anchorId: String? = null): Result<Triple<String, List<CanvasNode>, List<String>>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.exploreCanvasBoard(t, boardId, CanvasExploreRequest(goal, anchorId))
        if (res.error != null && res.nodes.isEmpty()) Result.failure(IllegalStateException(res.error))
        else Result.success(Triple(res.summary, res.nodes, res.nextQuestions))
    } catch (e: Exception) { fail(e) }

    suspend fun getSuggestions(boardId: String, goal: String = ""): Result<List<CanvasSuggestion>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.getCanvasSuggestions(t, boardId, CanvasExploreRequest(goal))
        if (res.error != null && res.suggestions.isEmpty()) Result.failure(IllegalStateException(res.error))
        else Result.success(res.suggestions)
    } catch (e: Exception) { fail(e) }

    suspend fun getWidgetContent(boardId: String, kind: String, topic: String): Result<JsonObject> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.getCanvasWidgetContent(t, boardId, CanvasWidgetRequest(kind, topic))
        res.content?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not build widget"))
    } catch (e: Exception) { fail(e) }

    suspend fun getObjects(boardId: String): Result<List<JsonObject>> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val raw = apiService.getCanvasObjects(t, boardId).string().trim()
        if (raw.isEmpty()) return Result.success(emptyList())
        val element = json.parseToJsonElement(raw)
        val arr: JsonArray = when {
            element is JsonObject && element["objects"] is JsonArray -> element["objects"]!!.jsonArray
            element is JsonArray -> element
            else -> return Result.success(emptyList())
        }
        Result.success(arr.mapNotNull { it as? JsonObject })
    } catch (e: Exception) { fail(e) }

    suspend fun saveObjects(boardId: String, objects: List<JsonObject>): Result<Unit> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.saveCanvasObjects(t, boardId, CanvasObjectsSaveRequest(objects))
        if (res.ok) Result.success(Unit) else Result.failure(IllegalStateException(res.error ?: "Could not save drawings"))
    } catch (e: Exception) { fail(e) }

    suspend fun getSharedDetail(tokenValue: String): Result<Triple<CanvasBoard, String, List<CanvasNode>>> = try {
        val res = apiService.getSharedCanvasDetail(token(), tokenValue)
        val board = res.board?.takeIf { it.id.isNotBlank() }
            ?: return Result.failure(IllegalStateException(res.error ?: "Shared canvas not found"))
        Result.success(Triple(board, res.owner, res.nodes))
    } catch (e: Exception) { fail(e) }

    suspend fun cloneShared(tokenValue: String): Result<CanvasBoard> = try {
        val t = token() ?: return Result.failure(IllegalStateException("Not authenticated"))
        val res = apiService.cloneSharedCanvas(t, tokenValue)
        res.board?.takeIf { it.id.isNotBlank() }?.let { Result.success(it) }
            ?: Result.failure(IllegalStateException(res.error ?: "Could not clone canvas"))
    } catch (e: Exception) { fail(e) }
}
