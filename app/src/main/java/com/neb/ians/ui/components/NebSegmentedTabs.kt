@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ButtonGroup
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.ToggleButton
import androidx.compose.material3.ToggleButtonDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

data class NebTab(
    val label: String,
    val icon: ImageVector? = null,
    val count: Int = 0
)

@Composable
fun NebSegmentedTabs(
    tabs: List<NebTab>,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier,
    minHeight: Dp = 42.dp,
    compact: Boolean = false
) {
    if (tabs.isEmpty()) return
    val interactions = remember(tabs.size) { List(tabs.size) { MutableInteractionSource() } }
    val colors = ToggleButtonDefaults.toggleButtonColors(
        containerColor = Color.Transparent,
        contentColor = MaterialTheme.colorScheme.onSurfaceVariant,
        checkedContainerColor = MaterialTheme.colorScheme.onSurface,
        checkedContentColor = MaterialTheme.colorScheme.surface
    )

    ButtonGroup(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(3.dp),
        horizontalArrangement = Arrangement.spacedBy(0.dp)
    ) {
        tabs.forEachIndexed { index, tab ->
            ToggleButton(
                checked = selectedIndex == index,
                onCheckedChange = { onSelect(index) },
                modifier = Modifier
                    .weight(1f)
                    .heightIn(min = minHeight)
                    .animateWidth(interactions[index]),
                shapes = ToggleButtonDefaults.shapes(),
                colors = colors,
                interactionSource = interactions[index],
                contentPadding = PaddingValues(
                    horizontal = if (compact) 6.dp else 8.dp,
                    vertical = 8.dp
                )
            ) {
                if (tab.icon != null) {
                    Icon(
                        imageVector = tab.icon,
                        contentDescription = null,
                        modifier = Modifier.size(17.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                }
                Text(
                    text = if (tab.count > 0) "${tab.label} ${tab.count}" else tab.label,
                    style = if (compact) {
                        MaterialTheme.typography.labelMediumEmphasized
                    } else {
                        MaterialTheme.typography.labelLargeEmphasized
                    },
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}
