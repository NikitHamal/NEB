package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.nebEffectsSpec

/**
 * One row of single-choice chips, the Android counterpart of the web composer's
 * poll-duration chips. The picked chip is a tonal secondary-container fill with a
 * check; the rest are outlined. Scrolls sideways when the labels outgrow the row.
 */
@Composable
fun NebChoiceChips(
    options: List<String>,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .nebHorizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        options.forEachIndexed { index, label ->
            val selected = index == selectedIndex
            val fill by animateColorAsState(
                targetValue = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
                animationSpec = nebEffectsSpec(),
                label = "chipFill"
            )
            val ink by animateColorAsState(
                targetValue = if (selected) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
                animationSpec = nebEffectsSpec(),
                label = "chipInk"
            )
            val outline by animateColorAsState(
                targetValue = if (selected) Color.Transparent else MaterialTheme.colorScheme.outlineVariant,
                animationSpec = nebEffectsSpec(),
                label = "chipOutline"
            )
            Row(
                modifier = Modifier
                    .clip(WebPillShape)
                    .border(1.dp, outline, WebPillShape)
                    .nebPressable(enabled = enabled, onClick = { onSelect(index) })
                    .background(fill)
                    .padding(horizontal = 14.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                if (selected) {
                    Icon(
                        imageVector = Icons.Rounded.Check,
                        contentDescription = null,
                        tint = ink,
                        modifier = Modifier.size(16.dp)
                    )
                }
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
                    color = ink,
                    maxLines = 1
                )
            }
        }
    }
}
