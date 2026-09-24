package com.neb.ians.ui.screens.canvas

import androidx.compose.runtime.Immutable

@Immutable
data class CanvasBoard(
    val id: String,
    val title: String,
    val nodeCount: Int = 0,
    val updatedAt: Long = System.currentTimeMillis(),
    val isLocal: Boolean = true
)

@Immutable
data class CanvasNode(
    val id: String,
    val boardId: String,
    val parentId: String? = null,
    val connections: List<String> = emptyList(),
    val prompt: String = "",
    val title: String = "",
    val content: CanvasNodeContent = CanvasNodeContent(),
    val status: String = "done", // "idle", "generating", "done", "failed"
    val x: Float = 0f,
    val y: Float = 0f,
    val width: Float = 460f,
    val kind: String = "topic", // goal, topic, question, practice, summary, source, comparison, warning, decision, task, note
    val color: String = "default", // default, blue, green, amber, rose, purple, slate
    val webSearchEnabled: Boolean = false,
    val modelUsed: String = "fast", // fast, deep
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)

@Immutable
data class CanvasNodeContent(
    val title: String = "",
    val summary: String = "",
    val sections: List<CanvasSection> = emptyList()
)

@Immutable
data class CanvasSection(
    val type: String, // "text", "diagram", "comparison", "cards", "bullets", "flowchart", "timeline"
    val title: String? = null,
    val content: String? = null,
    val nodes: List<DiagramNodeItem>? = null,
    val edges: List<DiagramEdgeItem>? = null,
    val headers: List<String>? = null,
    val rows: List<List<String>>? = null,
    val cardItems: List<CardRefItem>? = null,
    val bulletItems: List<String>? = null,
    val flowSteps: List<FlowStepItem>? = null,
    val timelineItems: List<TimelineItem>? = null
)

@Immutable
data class DiagramNodeItem(
    val id: String,
    val label: String,
    val desc: String = ""
)

@Immutable
data class DiagramEdgeItem(
    val from: String,
    val to: String
)

@Immutable
data class CardRefItem(
    val title: String,
    val subtitle: String = "",
    val bullets: List<String> = emptyList(),
    val desc: String = ""
)

@Immutable
data class FlowStepItem(
    val title: String,
    val desc: String = "",
    val status: String? = null
)

@Immutable
data class TimelineItem(
    val number: Int,
    val title: String,
    val subtitle: String = ""
)

@Immutable
data class CanvasTemplate(
    val key: String,
    val name: String,
    val subtitle: String,
    val description: String,
    val iconName: String,
    val initialNodes: List<CanvasNode>
)
