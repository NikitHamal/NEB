package com.neb.ians.ui.screens.notes

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color

/** A tonal note colour: fill and its label, always a role pair from the theme. */
@Immutable
data class NoteTone(val container: Color, val content: Color, val hairline: Boolean)

object NoteTones {
    val labels = listOf("Paper", "Blue", "Slate", "Teal", "Rose", "Sky", "Stone")
    val count: Int get() = labels.size
}

@Composable
fun noteTone(index: Int): NoteTone {
    val c = MaterialTheme.colorScheme
    return when (index) {
        1 -> NoteTone(c.primaryContainer, c.onPrimaryContainer, false)
        2 -> NoteTone(c.secondaryContainer, c.onSecondaryContainer, false)
        3 -> NoteTone(c.tertiaryContainer, c.onTertiaryContainer, false)
        4 -> NoteTone(c.errorContainer, c.onErrorContainer, false)
        5 -> NoteTone(c.surfaceContainerHigh, c.onSurface, false)
        6 -> NoteTone(c.surfaceVariant, c.onSurfaceVariant, false)
        else -> NoteTone(c.surfaceContainerLowest, c.onSurface, true)
    }
}
