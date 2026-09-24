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

// ---------------------------------------------------------------------------
// The themes a card can wear.
//
// The app is mono, which means restraint, not absence. A card is a white sheet
// on a white board and the colour is a single thread through it — the rule at
// the top of the header, the tag, the wire that leaves it. Seven answers,
// each one a real hue held at the same weight as the ink around it, so a board
// of seven themes still reads as one drawing.
// ---------------------------------------------------------------------------

@Immutable
private data class CanvasTone(
    val label: String,
    val light: Color,
    val dark: Color
)

object CanvasColorTokens {

    val Keys = listOf("default", "blue", "green", "amber", "rose", "purple", "slate")

    private val Tones = mapOf(
        "default" to CanvasTone("Neutral", Color(0xFF34343A), Color(0xFFD4D4DA)),
        "blue" to CanvasTone("Concept", Color(0xFF2551C9), Color(0xFF92B4FF)),
        "green" to CanvasTone("Formula", Color(0xFF0B6A4E), Color(0xFF52D2A4)),
        "amber" to CanvasTone("Highlight", Color(0xFF8F5507), Color(0xFFE5A84C)),
        "rose" to CanvasTone("Caution", Color(0xFFA8271F), Color(0xFFFF9186)),
        "purple" to CanvasTone("Synthesis", Color(0xFF5A3CC4), Color(0xFFBBA6FF)),
        "slate" to CanvasTone("Reference", Color(0xFF3B5464), Color(0xFF9FB6C4))
    )

    private fun tone(key: String): CanvasTone = Tones[key.lowercase()] ?: Tones.getValue("default")

    fun label(key: String): String = tone(key).label

    fun accent(isDark: Boolean, key: String): Color = tone(key).let { if (isDark) it.dark else it.light }

    fun colors(scheme: ColorScheme, isDark: Boolean, key: String): CanvasCardColorScheme {
        val accent = accent(isDark, key)
        val surface = if (isDark) scheme.surfaceContainerLow else Color.White
        val neutral = key.equals("default", ignoreCase = true)
        return CanvasCardColorScheme(
            surface = surface,
            border = lerp(scheme.outlineVariant, accent, if (neutral) 0.12f else 0.3f),
            headerBg = accent.copy(alpha = if (isDark) 0.14f else 0.07f).compositeOver(surface),
            accent = accent,
            tagBg = accent.copy(alpha = if (isDark) 0.2f else 0.12f).compositeOver(surface),
            tagText = if (isDark) accent else lerp(accent, scheme.onSurface, 0.1f),
            titleText = scheme.onSurface,
            bodyText = scheme.onSurface.copy(alpha = 0.86f).compositeOver(surface),
            secondaryText = scheme.onSurfaceVariant,
            innerCardBg = accent.copy(alpha = if (isDark) 0.07f else 0.04f).compositeOver(surface),
            innerCardBorder = lerp(scheme.outlineVariant, accent, 0.18f)
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
