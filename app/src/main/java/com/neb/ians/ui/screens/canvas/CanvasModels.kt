package com.neb.ians.ui.screens.canvas

import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color

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

object CanvasColorTokens {

    private val AccentOrderDark = listOf(
        "default" to Color(0xFFE7E7E9),
        "blue" to Color(0xFFC9C9CD),
        "green" to Color(0xFFA1A1A8),
        "amber" to Color(0xFFD5D5D9),
        "rose" to Color(0xFFB4B4BA),
        "purple" to Color(0xFF8E8E96),
        "slate" to Color(0xFF7C7C83)
    ).toMap()

    private val AccentOrderLight = listOf(
        "default" to Color(0xFF101012),
        "blue" to Color(0xFF26262A),
        "green" to Color(0xFF47474B),
        "amber" to Color(0xFF313136),
        "rose" to Color(0xFF5C5C61),
        "purple" to Color(0xFF6E6E75),
        "slate" to Color(0xFF7C7C83)
    ).toMap()

    fun getColors(colorKey: String, isDark: Boolean): CanvasCardColorScheme {
        val key = colorKey.lowercase()
        return if (isDark) {
            val accent = AccentOrderDark[key] ?: AccentOrderDark.getValue("default")
            CanvasCardColorScheme(
                surface = Color(0xFF131315),
                border = Color(0xFF26262A),
                headerBg = Color(0xFF18181B),
                accent = accent,
                tagBg = Color(0xFF26262A),
                tagText = Color(0xFFC9C9CD),
                titleText = Color(0xFFF5F5F6),
                bodyText = Color(0xFFC9C9CD),
                secondaryText = Color(0xFFA1A1A8),
                innerCardBg = Color(0xFF0C0C0D),
                innerCardBorder = Color(0xFF26262A)
            )
        } else {
            val accent = AccentOrderLight[key] ?: AccentOrderLight.getValue("default")
            CanvasCardColorScheme(
                surface = Color(0xFFFFFFFF),
                border = Color(0xFFE9E9EB),
                headerBg = Color(0xFFF7F7F9),
                accent = accent,
                tagBg = Color(0xFFF1F1F3),
                tagText = Color(0xFF313136),
                titleText = Color(0xFF0A0A0B),
                bodyText = Color(0xFF313136),
                secondaryText = Color(0xFF5C5C61),
                innerCardBg = Color(0xFFFAFAFB),
                innerCardBorder = Color(0xFFE9E9EB)
            )
        }
    }
}

@Immutable
data class CanvasCardColorScheme(
    val surface: Color,
    val border: Color,
    val headerBg: Color,
    val accent: Color,
    val tagBg: Color,
    val tagText: Color,
    val titleText: Color,
    val bodyText: Color,
    val secondaryText: Color,
    val innerCardBg: Color,
    val innerCardBorder: Color
)
