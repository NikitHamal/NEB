package com.neb.ians.ui.screens.canvas

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.graphics.luminance

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

    val Keys = listOf("default", "blue", "green", "amber", "rose", "purple", "slate")

    private val Tones = mapOf(
        "default" to 0f,
        "blue" to 0.18f,
        "green" to 0.34f,
        "amber" to 0.5f,
        "rose" to 0.66f,
        "purple" to 0.82f,
        "slate" to 1f
    )

    fun label(key: String): String = when (key.lowercase()) {
        "blue" -> "Concept"
        "green" -> "Formula"
        "amber" -> "Highlight"
        "rose" -> "Caution"
        "purple" -> "Synthesis"
        "slate" -> "Reference"
        else -> "Neutral"
    }

    fun tone(key: String): Float = Tones[key.lowercase()] ?: 0f

    fun accent(scheme: ColorScheme, key: String): Color =
        lerp(scheme.outline, scheme.onSurface, tone(key))

    fun colors(scheme: ColorScheme, isDark: Boolean, key: String): CanvasCardColorScheme {
        val t = tone(key)
        val accent = accent(scheme, key)
        val wash = if (isDark) 0.05f + t * 0.09f else 0.04f + t * 0.08f
        return CanvasCardColorScheme(
            surface = scheme.surfaceContainerLowest,
            border = lerp(scheme.outlineVariant, accent, 0.15f + t * 0.35f),
            headerBg = accent.copy(alpha = wash).compositeOver(scheme.surfaceContainerLow),
            accent = accent,
            tagBg = accent.copy(alpha = if (isDark) 0.22f else 0.14f)
                .compositeOver(scheme.surfaceContainerLow),
            tagText = if (isDark) lerp(accent, scheme.onSurface, 0.4f) else accent,
            titleText = scheme.onSurface,
            bodyText = scheme.onSurface.copy(alpha = 0.88f).compositeOver(scheme.surfaceContainerLowest),
            secondaryText = scheme.onSurfaceVariant,
            innerCardBg = scheme.surfaceContainerLow,
            innerCardBorder = scheme.outlineVariant
        )
    }
}

@Composable
fun canvasCardColors(key: String): CanvasCardColorScheme {
    val scheme = MaterialTheme.colorScheme
    val isDark = scheme.surface.luminance() < 0.5f
    return remember(scheme, isDark, key) { CanvasColorTokens.colors(scheme, isDark, key) }
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
