package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonObject

@Serializable
data class CanvasBoard(
    val id: String = "",
    val title: String = "",
    val createdAt: Long = 0,
    val updatedAt: Long = 0,
    val nodeCount: Int = 0,
    val settings: JsonObject? = null
)

@Serializable
data class CanvasBoardsResponse(val boards: List<CanvasBoard> = emptyList())

@Serializable
data class CanvasBoardCreateRequest(val title: String = "Untitled canvas")

@Serializable
data class CanvasBoardResponse(val board: CanvasBoard? = null, val error: String? = null)

@Serializable
data class CanvasBoardDetailResponse(
    val board: CanvasBoard? = null,
    val nodes: List<CanvasNode> = emptyList(),
    val error: String? = null
)

@Serializable
data class CanvasBoardTitleRequest(val title: String)

@Serializable
data class CanvasShareRequest(val revoke: Boolean = false)

@Serializable
data class CanvasShareResponse(
    val enabled: Boolean = false,
    val url: String = "",
    val error: String? = null
)

@Serializable
data class CanvasNode(
    val id: String = "",
    val boardId: String = "",
    val parentId: String? = null,
    val prompt: String = "",
    val title: String = "",
    val content: JsonObject? = null,
    val status: String = "done",
    val x: Double = 0.0,
    val y: Double = 0.0,
    val webSearchEnabled: Boolean = false,
    val modelUsed: String = "",
    val kind: String = "note",
    val meta: JsonObject? = null,
    val error: String? = null,
    val createdAt: Long = 0,
    val updatedAt: Long = 0
)

@Serializable
data class CanvasNodeResponse(val node: CanvasNode? = null, val error: String? = null)

@Serializable
data class CanvasNodeCreateRequest(
    val prompt: String,
    @SerialName("parent_id") val parentId: String? = null,
    val x: Double? = null,
    val y: Double? = null,
    @SerialName("web_search_enabled") val webSearchEnabled: Boolean = false,
    @SerialName("speed_mode") val speedMode: String = "fast"
)

@Serializable
data class CanvasNoteCreateRequest(
    val title: String = "",
    val body: String = "",
    val kind: String = "note",
    val x: Double? = null,
    val y: Double? = null,
    val parentId: String? = null,
    val meta: CanvasNodeMeta? = null
)

@Serializable
data class CanvasNodeMeta(
    val color: String = "default",
    val tags: List<String> = emptyList(),
    val pinned: Boolean = false
)

@Serializable
data class CanvasNodeUpdateRequest(
    val title: String? = null,
    val body: String? = null,
    val kind: String? = null,
    val meta: CanvasNodeMeta? = null
)

@Serializable
data class CanvasNodeMoveRequest(val x: Double, val y: Double)

@Serializable
data class CanvasFollowupRequest(
    val prompt: String,
    val x: Double? = null,
    val y: Double? = null,
    @SerialName("web_search_enabled") val webSearchEnabled: Boolean = false,
    @SerialName("speed_mode") val speedMode: String = "fast"
)

@Serializable
data class CanvasDigDeeperRequest(
    @SerialName("selected_text") val selectedText: String,
    val prompt: String = "",
    val x: Double? = null,
    val y: Double? = null
)

@Serializable
data class CanvasBatchMoveRequest(
    val layout: String = "freeform",
    val nodes: List<CanvasBatchMoveNode> = emptyList()
)

@Serializable
data class CanvasBatchMoveNode(val id: String, val x: Double, val y: Double)

@Serializable
data class CanvasOkResponse(val ok: Boolean = false, val error: String? = null)

@Serializable
data class CanvasSnapshot(
    val id: String = "",
    val label: String = "",
    val createdAt: Long = 0,
    val nodeCount: Int = 0
)

@Serializable
data class CanvasSnapshotsResponse(val snapshots: List<CanvasSnapshot> = emptyList())

@Serializable
data class CanvasSnapshotCreateRequest(val label: String = "")

@Serializable
data class CanvasSnapshotResponse(val snapshot: CanvasSnapshot? = null, val error: String? = null)

@Serializable
data class CanvasSnapshotRestoreResponse(
    val ok: Boolean = false,
    val board: CanvasBoard? = null,
    val nodes: List<CanvasNode> = emptyList(),
    val error: String? = null
)

@Serializable
data class CanvasTemplate(
    val key: String = "",
    val name: String = "",
    val icon: String = "",
    val description: String = ""
)

@Serializable
data class CanvasTemplatesResponse(val templates: List<CanvasTemplate> = emptyList())

@Serializable
data class CanvasTemplateCreateRequest(val template: String, val title: String = "")

@Serializable
data class CanvasTemplateCreateResponse(
    val board: CanvasBoard? = null,
    val nodes: List<CanvasNode> = emptyList(),
    val error: String? = null
)

@Serializable
data class CanvasExploreRequest(val goal: String = "", val anchorId: String? = null)

@Serializable
data class CanvasExploreResponse(
    val summary: String = "",
    val nodes: List<CanvasNode> = emptyList(),
    val nextQuestions: List<String> = emptyList(),
    val provider: String = "",
    val error: String? = null
)

@Serializable
data class CanvasSuggestion(
    val title: String = "",
    val prompt: String = "",
    val why: String = ""
)

@Serializable
data class CanvasSuggestionsResponse(
    val suggestions: List<CanvasSuggestion> = emptyList(),
    val provider: String = "",
    val error: String? = null
)

@Serializable
data class CanvasWidgetRequest(val kind: String, val topic: String)

@Serializable
data class CanvasWidgetResponse(
    val content: JsonObject? = null,
    val provider: String = "",
    val error: String? = null
)

@Serializable
data class CanvasObjectsSaveRequest(val objects: List<JsonObject> = emptyList())

@Serializable
data class CanvasImportRequest(val canvas: JsonObject)

@Serializable
data class CanvasImportResponse(
    val ok: Boolean = false,
    val board: CanvasBoard? = null,
    val nodes: List<CanvasNode> = emptyList(),
    val error: String? = null
)

@Serializable
data class CanvasSharedDetailResponse(
    val board: CanvasBoard? = null,
    val owner: String = "",
    val readonly: Boolean = true,
    val nodes: List<CanvasNode> = emptyList(),
    val error: String? = null
)

@Serializable
data class CanvasCloneResponse(
    val board: CanvasBoard? = null,
    val url: String = "",
    val error: String? = null
)
