@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.M3xArt
import com.neb.ians.ui.components.M3xCoverTile
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.nebPressable

/** The profile cover chooser: the v7 covers of the M3X art library (23 compositions, 8 colours each). */
@Composable
fun CoverPickerSheet(
    currentId: String?,
    onPick: (String) -> Unit,
    onDefault: () -> Unit,
    onDismiss: () -> Unit
) {
    val context = LocalContext.current
    val covers = remember { M3xArt.covers(context) }
    val scheme = MaterialTheme.colorScheme
    NebModalSheet(
        onDismiss = onDismiss,
        title = "Choose a cover",
        fullBleed = true // bleed: the grid pads itself
    ) {
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxWidth().weight(1f, fill = false),
            contentPadding = PaddingValues(horizontal = 22.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            item(span = { androidx.compose.foundation.lazy.grid.GridItemSpan(2) }, key = "default") {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(22.dp))
                        .border(BorderStroke(1.5.dp, scheme.outlineVariant), RoundedCornerShape(22.dp))
                        .clickable(onClick = onDefault)
                        .padding(horizontal = 18.dp, vertical = 14.dp),
                    contentAlignment = Alignment.CenterStart
                ) {
                    Text("Default cover", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = scheme.primary)
                }
            }
            items(covers, key = { it.id }) { cover ->
                val selected = cover.id == currentId
                val shape = RoundedCornerShape(18.dp)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(3f)
                        .nebPressable(scale = 0.97f, onClick = { onPick(cover.id) })
                        .clip(shape)
                        .border(
                            BorderStroke(if (selected) 2.5.dp else 1.5.dp, if (selected) scheme.primary else scheme.outlineVariant),
                            shape
                        )
                ) {
                    M3xCoverTile(cover.id, Modifier.fillMaxSize())
                    if (selected) {
                        Box(
                            modifier = Modifier.align(Alignment.TopEnd).padding(8.dp).size(24.dp)
                                .background(scheme.primary, RoundedCornerShape(12.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Filled.Check, contentDescription = "Selected", tint = scheme.onPrimary, modifier = Modifier.size(16.dp))
                        }
                    }
                }
            }
        }
    }
}
