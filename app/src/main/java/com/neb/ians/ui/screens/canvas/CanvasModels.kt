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
    fun getColors(colorKey: String, isDark: Boolean): CanvasCardColorScheme {
        return when (colorKey.lowercase()) {
            "blue" -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF111E33),
                    border = Color(0xFF20355A),
                    headerBg = Color(0xFF16253E),
                    accent = Color(0xFF6B93F7),
                    tagBg = Color(0xFF1A325C),
                    tagText = Color(0xFFA5C1FF),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFF94A3B8),
                    innerCardBg = Color(0xFF0C1627),
                    innerCardBorder = Color(0xFF1C2E4C)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFD3E2FB),
                    headerBg = Color(0xFFF2F7FF),
                    accent = Color(0xFF0052CC),
                    tagBg = Color(0xFFE3EDFF),
                    tagText = Color(0xFF003D99),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFF8FAFD),
                    innerCardBorder = Color(0xFFE2ECFA)
                )
            }
            "green" -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF0D241A),
                    border = Color(0xFF194430),
                    headerBg = Color(0xFF123123),
                    accent = Color(0xFF4ADE80),
                    tagBg = Color(0xFF16442E),
                    tagText = Color(0xFF86EFAC),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFF86A397),
                    innerCardBg = Color(0xFF091B13),
                    innerCardBorder = Color(0xFF163E2D)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFC7EBD4),
                    headerBg = Color(0xFFF0FAF4),
                    accent = Color(0xFF16A34A),
                    tagBg = Color(0xFFDCF6E7),
                    tagText = Color(0xFF14532D),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFF7FCF9),
                    innerCardBorder = Color(0xFFD6F0E0)
                )
            }
            "amber" -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF241C0E),
                    border = Color(0xFF4A3718),
                    headerBg = Color(0xFF302412),
                    accent = Color(0xFFFBBF24),
                    tagBg = Color(0xFF463513),
                    tagText = Color(0xFFFDE68A),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFFA39580),
                    innerCardBg = Color(0xFF1A1409),
                    innerCardBorder = Color(0xFF3D2E14)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFFEE685),
                    headerBg = Color(0xFFFFFDF2),
                    accent = Color(0xFFD97706),
                    tagBg = Color(0xFFFEF3C7),
                    tagText = Color(0xFF92400E),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFFFFDF5),
                    innerCardBorder = Color(0xFFFDE68A)
                )
            }
            "rose" -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF260F15),
                    border = Color(0xFF521F2B),
                    headerBg = Color(0xFF36151D),
                    accent = Color(0xFFFB7185),
                    tagBg = Color(0xFF551C29),
                    tagText = Color(0xFFFECDD3),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFFA88992),
                    innerCardBg = Color(0xFF1D0A10),
                    innerCardBorder = Color(0xFF441823)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFFFCCD5),
                    headerBg = Color(0xFFFFF5F7),
                    accent = Color(0xFFE11D48),
                    tagBg = Color(0xFFFFE4E8),
                    tagText = Color(0xFF9F1239),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFFFF7F8),
                    innerCardBorder = Color(0xFFFFD5DD)
                )
            }
            "purple" -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF1D112D),
                    border = Color(0xFF402263),
                    headerBg = Color(0xFF29163F),
                    accent = Color(0xFFC084FC),
                    tagBg = Color(0xFF3F1F64),
                    tagText = Color(0xFFE9D5FF),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFF9E8CAE),
                    innerCardBg = Color(0xFF150B21),
                    innerCardBorder = Color(0xFF341A52)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFE6D2FC),
                    headerBg = Color(0xFFFAF5FF),
                    accent = Color(0xFF9333EA),
                    tagBg = Color(0xFFF3E8FF),
                    tagText = Color(0xFF581C87),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFFCF9FF),
                    innerCardBorder = Color(0xFFECDCFD)
                )
            }
            "slate" -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF131A24),
                    border = Color(0xFF263242),
                    headerBg = Color(0xFF192230),
                    accent = Color(0xFF94A3B8),
                    tagBg = Color(0xFF253142),
                    tagText = Color(0xFFCBD5E1),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFF94A3B8),
                    innerCardBg = Color(0xFF0E131A),
                    innerCardBorder = Color(0xFF1F2836)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFE2E8F0),
                    headerBg = Color(0xFFF8FAFC),
                    accent = Color(0xFF64748B),
                    tagBg = Color(0xFFF1F5F9),
                    tagText = Color(0xFF334155),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFF8FAFC),
                    innerCardBorder = Color(0xFFE2E8F0)
                )
            }
            else -> if (isDark) {
                CanvasCardColorScheme(
                    surface = Color(0xFF121B2A),
                    border = Color(0xFF1D2B40),
                    headerBg = Color(0xFF172336),
                    accent = Color(0xFF84AAFF),
                    tagBg = Color(0xFF1C2B43),
                    tagText = Color(0xFFB8C5DA),
                    titleText = Color(0xFFF1F5F9),
                    bodyText = Color(0xFFCBD5E1),
                    secondaryText = Color(0xFF94A3B8),
                    innerCardBg = Color(0xFF0C131F),
                    innerCardBorder = Color(0xFF1A2638)
                )
            } else {
                CanvasCardColorScheme(
                    surface = Color(0xFFFFFFFF),
                    border = Color(0xFFE2E6F0),
                    headerBg = Color(0xFFF8FAFC),
                    accent = Color(0xFF0052CC),
                    tagBg = Color(0xFFEBF0FF),
                    tagText = Color(0xFF0052CC),
                    titleText = Color(0xFF0F172A),
                    bodyText = Color(0xFF334155),
                    secondaryText = Color(0xFF64748B),
                    innerCardBg = Color(0xFFF8FAFC),
                    innerCardBorder = Color(0xFFE2E6F0)
                )
            }
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
