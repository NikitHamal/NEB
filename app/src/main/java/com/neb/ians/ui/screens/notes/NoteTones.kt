package com.neb.ians.ui.screens.notes

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance

/** A tonal note colour: fill and its label, always a role pair. */
@Immutable
data class NoteTone(val container: Color, val content: Color, val hairline: Boolean)

/** A ready-made look: colour, cover and icon in one tap. */
@Immutable
data class NoteTheme(val label: String, val tone: Int, val cover: Int, val icon: String)

object NoteTones {
    val labels = listOf(
        "Paper", "Blue", "Slate", "Teal", "Rose", "Sky", "Stone",
        "Sand", "Mint", "Lemon", "Peach", "Ocean", "Sage", "Linen", "Periwinkle", "Graphite", "Midnight", "Forest",
    )
    val count: Int get() = labels.size

    val themes = listOf(
        NoteTheme("Study", 1, 1, "school"),
        NoteTheme("Journal", 7, 12, "book"),
        NoteTheme("Garden", 8, 19, "eco"),
        NoteTheme("Sunrise", 10, 14, "sun"),
        NoteTheme("Ocean", 11, 2, "world"),
        NoteTheme("Calm", 14, 4, "mind"),
        NoteTheme("Focus", 15, 22, "bolt"),
        NoteTheme("Night", 16, 9, "star"),
        NoteTheme("Forest", 17, 24, "park"),
    )

    private class Pair2(val lc: Long, val lt: Long, val dc: Long, val dt: Long)

    private val fixed = listOf(
        Pair2(0xFFF5EBDD, 0xFF4A3B22, 0xFF3A3126, 0xFFEBDDC5), // 7 Sand
        Pair2(0xFFDDF3E4, 0xFF0F3D26, 0xFF17382A, 0xFFBFEBD0), // 8 Mint
        Pair2(0xFFFBF1C4, 0xFF4A4000, 0xFF3B3512, 0xFFF3E8A3), // 9 Lemon
        Pair2(0xFFFFE3D3, 0xFF5A2B10, 0xFF442618, 0xFFFFD0B5), // 10 Peach
        Pair2(0xFFBFE6F7, 0xFF063B57, 0xFF0C3550, 0xFFB4E2FA), // 11 Ocean
        Pair2(0xFFE1EBD9, 0xFF2B3A1E, 0xFF27301F, 0xFFD3E3C6), // 12 Sage
        Pair2(0xFFEFEAE4, 0xFF3B342D, 0xFF2E2B28, 0xFFE5DED5), // 13 Linen
        Pair2(0xFFDDE3FF, 0xFF1D2A6B, 0xFF232B55, 0xFFC9D2FF), // 14 Periwinkle
        Pair2(0xFF2B2E36, 0xFFE6E8EE, 0xFF1A1C22, 0xFFE6E8EE), // 15 Graphite
        Pair2(0xFF0F1A33, 0xFFDCE6FF, 0xFF0A1226, 0xFFDCE6FF), // 16 Midnight
        Pair2(0xFF163B2A, 0xFFD5F0E0, 0xFF0F2A1E, 0xFFD5F0E0), // 17 Forest
    )

    internal fun fixedTone(index: Int, dark: Boolean): NoteTone? {
        val p = fixed.getOrNull(index - 7) ?: return null
        return if (dark) NoteTone(Color(p.dc), Color(p.dt), false) else NoteTone(Color(p.lc), Color(p.lt), false)
    }
}

@Composable
fun noteTone(index: Int): NoteTone {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.luminance() < 0.5f
    return when (index) {
        1 -> NoteTone(c.primaryContainer, c.onPrimaryContainer, false)
        2 -> NoteTone(c.secondaryContainer, c.onSecondaryContainer, false)
        3 -> NoteTone(c.tertiaryContainer, c.onTertiaryContainer, false)
        4 -> NoteTone(c.errorContainer, c.onErrorContainer, false)
        5 -> NoteTone(c.surfaceContainerHigh, c.onSurface, false)
        6 -> NoteTone(c.surfaceVariant, c.onSurfaceVariant, false)
        in 7..17 -> NoteTones.fixedTone(index, dark) ?: NoteTone(c.surfaceContainerLowest, c.onSurface, true)
        else -> NoteTone(c.surfaceContainerLowest, c.onSurface, true)
    }
}
