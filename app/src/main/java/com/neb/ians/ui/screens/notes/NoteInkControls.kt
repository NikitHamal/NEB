package com.neb.ians.ui.screens.notes

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.FormatAlignCenter
import androidx.compose.material.icons.outlined.FormatAlignLeft
import androidx.compose.material.icons.outlined.FormatAlignRight
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.shape.RoundedCornerShape

/** Maps the stored block alignment (0 start, 1 centre, 2 end) to a text alignment. */
fun inkAlign(a: Int): TextAlign = when (a) { 1 -> TextAlign.Center; 2 -> TextAlign.End; else -> TextAlign.Start }

/** Alignment, text colour and highlight for one text block: one tap each, nothing to type. */
@Composable
fun InkControls(block: NoteBlock, onLook: (align: Int, tint: Int, mark: Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    val dark = remember(c.surface) { c.surface.luminance() < 0.5f }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Align", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf(Icons.Outlined.FormatAlignLeft to "Left", Icons.Outlined.FormatAlignCenter to "Centre", Icons.Outlined.FormatAlignRight to "Right")
                .forEachIndexed { i, (icon, label) -> AlignChip(icon, label, block.align == i, Modifier.weight(1f)) { onLook(i, -1, -1) } }
        }
        Text("Text colour", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
        InkRow(block.tint, dark, fill = false) { onLook(-1, it, -1) }
        Text("Highlight", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
        InkRow(block.mark, dark, fill = true) { onLook(-1, -1, it) }
    }
}

@Composable
private fun AlignChip(icon: ImageVector, label: String, on: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Box(
        modifier.height(44.dp).clip(RoundedCornerShape(22.dp))
            .background(if (on) c.secondaryContainer else c.surfaceContainerLow)
            .then(if (on) Modifier else Modifier.border(1.dp, c.outlineVariant, RoundedCornerShape(22.dp)))
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center,
    ) {
        Icon(icon, label, tint = if (on) c.onSecondaryContainer else c.onSurfaceVariant, modifier = Modifier.size(22.dp))
    }
}

@Composable
private fun InkRow(current: Int, dark: Boolean, fill: Boolean, onPick: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(vertical = 2.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Box(
            Modifier.size(40.dp).clip(CircleShape).background(c.surfaceContainerHigh).clickable { onPick(0) },
            contentAlignment = Alignment.Center,
        ) { Icon(Icons.Outlined.Close, "None", tint = if (current == 0) c.primary else c.onSurfaceVariant, modifier = Modifier.size(20.dp)) }
        for (i in 1..NoteInk.count) {
            val swatch = (if (fill) NoteInk.fill(i, dark) else NoteInk.text(i, dark)) ?: Color.Transparent
            Box(
                Modifier.size(40.dp).clip(CircleShape).background(swatch)
                    .then(if (fill) Modifier.border(1.dp, c.outlineVariant, CircleShape) else Modifier)
                    .clickable { onPick(i) },
                contentAlignment = Alignment.Center,
            ) {
                if (current == i) Icon(Icons.Outlined.Check, NoteInk.names[i - 1], tint = if (fill) (NoteInk.text(i, dark) ?: c.onSurface) else Color.White, modifier = Modifier.size(20.dp))
                else if (fill) Text("A", color = NoteInk.text(i, dark) ?: c.onSurface, style = MaterialTheme.typography.labelLarge)
            }
        }
    }
}
