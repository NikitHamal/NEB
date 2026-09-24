@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.NebAccent
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.resolve
import com.neb.ians.util.TactileType

// ---------------------------------------------------------------------------
// Switching between sets of the same thing: the library's shelves, a profile's
// posts and replies, a notification filter.
//
// Not a bar of connected buttons — that reads as one control the user is
// operating, and it squeezes four labels into a width that fits two. Not an
// underline either, which is the platform's tab and not ours. Here the resting
// state is bare text with nothing drawn around it, and only the answer carries
// a container. The rail stays quiet, the selection is unmistakable, and a long
// label is free to be as long as it is because the row scrolls.
// ---------------------------------------------------------------------------

@Immutable
data class NebRailTab(
    val label: String,
    val icon: ImageVector? = null,
    val count: Int = 0,
    val showZero: Boolean = false
)

@Composable
fun NebTabRail(
    tabs: List<NebRailTab>,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier,
    accent: NebAccent? = null,
    contentPadding: PaddingValues = PaddingValues(horizontal = 14.dp, vertical = 6.dp)
) {
    if (tabs.isEmpty()) return

    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(contentPadding),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        tabs.forEachIndexed { index, tab ->
            NebRailItem(
                tab = tab,
                selected = index == selectedIndex,
                accent = accent,
                onClick = { onSelect(index) }
            )
        }
    }
}

@Composable
private fun NebRailItem(
    tab: NebRailTab,
    selected: Boolean,
    accent: NebAccent?,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val isDark = scheme.surface.luminance() < 0.5f
    val accentColor = accent?.resolve()

    val restingContent = scheme.onSurfaceVariant
    val selectedContent = accentColor ?: scheme.onSurface
    val selectedFill = accentColor
        ?.copy(alpha = if (isDark) 0.17f else 0.10f)
        ?.compositeOver(scheme.surfaceContainerLow)
        ?: scheme.surfaceContainerHighest

    val fill by animateColorAsState(
        targetValue = if (selected) selectedFill else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "rail_fill"
    )
    val content by animateColorAsState(
        targetValue = if (selected) selectedContent else restingContent,
        animationSpec = nebEffectsSpec(),
        label = "rail_content"
    )
    val edge by animateColorAsState(
        targetValue = if (selected) {
            accentColor?.copy(alpha = 0.34f) ?: scheme.outlineVariant
        } else {
            Color.Transparent
        },
        animationSpec = nebEffectsSpec(),
        label = "rail_edge"
    )
    val horizontal by animateDpAsState(
        targetValue = if (selected) 18.dp else 14.dp,
        animationSpec = nebFastSpatialSpec(),
        label = "rail_pad"
    )

    val shape = RoundedCornerShape(50)

    Row(
        modifier = Modifier
            .nebPressable(scale = 0.94f, tactile = TactileType.SelectionChange, onClick = onClick)
            .clip(shape)
            .background(fill)
            .border(1.dp, edge, shape)
            .padding(horizontal = horizontal, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(7.dp)
    ) {
        if (tab.icon != null) {
            Icon(
                imageVector = tab.icon,
                contentDescription = null,
                tint = content,
                modifier = Modifier.size(18.dp)
            )
        }
        Text(
            text = tab.label,
            style = MaterialTheme.typography.labelLargeEmphasized,
            color = content,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        if (tab.count > 0 || tab.showZero) {
            Box(
                modifier = Modifier
                    .clip(CircleShape)
                    .background(content.copy(alpha = if (selected) 0.14f else 0.10f))
                    .padding(horizontal = 7.dp, vertical = 2.dp)
            ) {
                Text(
                    text = tab.count.toString(),
                    style = MaterialTheme.typography.labelSmall,
                    color = content
                )
            }
        }
    }
}
