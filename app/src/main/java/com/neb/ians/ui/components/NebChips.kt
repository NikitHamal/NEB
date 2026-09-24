@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.layout.ExperimentalLayoutApi::class
)

package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.expandHorizontally
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.shrinkHorizontally
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.FlowRowScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec

@Composable
fun NebFilterChip(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    icon: ImageVector? = null,
    enabled: Boolean = true
) {
    val corner by animateDpAsState(
        targetValue = if (selected) 14.dp else 22.dp,
        animationSpec = nebFastSpatialSpec(),
        label = "neb_chip_corner"
    )
    val container by animateColorAsState(
        targetValue = if (selected) {
            MaterialTheme.colorScheme.onSurface
        } else {
            MaterialTheme.colorScheme.surfaceContainerHighest
        },
        animationSpec = nebEffectsSpec(),
        label = "neb_chip_container"
    )
    val content by animateColorAsState(
        targetValue = if (selected) {
            MaterialTheme.colorScheme.surface
        } else {
            MaterialTheme.colorScheme.onSurfaceVariant
        },
        animationSpec = nebEffectsSpec(),
        label = "neb_chip_content"
    )
    val outline by animateColorAsState(
        targetValue = if (selected) {
            MaterialTheme.colorScheme.onSurface
        } else {
            MaterialTheme.colorScheme.outlineVariant
        },
        animationSpec = nebEffectsSpec(),
        label = "neb_chip_outline"
    )
    val shape = RoundedCornerShape(corner)

    Row(
        modifier = modifier
            .defaultMinSize(minHeight = 40.dp)
            .nebPressable(enabled = enabled, onClick = onClick)
            .clip(shape)
            .background(container)
            .border(BorderStroke(1.dp, outline), shape)
            .padding(horizontal = 14.dp, vertical = 9.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        AnimatedVisibility(
            visible = selected,
            enter = fadeIn(nebEffectsSpec()) + expandHorizontally(nebFastSpatialSpec()),
            exit = fadeOut(nebEffectsSpec()) + shrinkHorizontally(nebFastSpatialSpec())
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Rounded.Check,
                    contentDescription = null,
                    tint = content,
                    modifier = Modifier.size(16.dp)
                )
                Spacer(modifier = Modifier.width(6.dp))
            }
        }
        if (icon != null && !selected) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = content,
                modifier = Modifier.size(16.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
        }
        Text(
            text = label,
            style = MaterialTheme.typography.labelLargeEmphasized,
            color = content,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun NebChipRow(
    modifier: Modifier = Modifier,
    content: @Composable FlowRowScope.() -> Unit
) {
    FlowRow(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        content = content
    )
}

@Composable
fun NebChipGroup(
    options: List<String>,
    selected: String?,
    onSelect: (String?) -> Unit,
    modifier: Modifier = Modifier,
    toggleable: Boolean = true
) {
    NebChipRow(modifier = modifier) {
        options.forEach { option ->
            val isSelected = selected == option
            NebFilterChip(
                label = option,
                selected = isSelected,
                onClick = { onSelect(if (isSelected && toggleable) null else option) }
            )
        }
    }
}

@Composable
fun NebSectionLabel(
    text: String,
    modifier: Modifier = Modifier
) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelMediumEmphasized,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = modifier
    )
}

@Composable
fun NebSelectIndicator(
    selected: Boolean,
    modifier: Modifier = Modifier
) {
    val container by animateColorAsState(
        targetValue = if (selected) {
            MaterialTheme.colorScheme.onSurface
        } else {
            MaterialTheme.colorScheme.surfaceContainerHighest
        },
        animationSpec = nebEffectsSpec(),
        label = "neb_select_container"
    )
    val outline by animateColorAsState(
        targetValue = if (selected) {
            MaterialTheme.colorScheme.onSurface
        } else {
            MaterialTheme.colorScheme.outlineVariant
        },
        animationSpec = nebEffectsSpec(),
        label = "neb_select_outline"
    )
    val corner by animateDpAsState(
        targetValue = if (selected) 8.dp else 11.dp,
        animationSpec = nebFastSpatialSpec(),
        label = "neb_select_corner"
    )
    val shape = RoundedCornerShape(corner)

    Box(
        modifier = modifier
            .size(22.dp)
            .clip(shape)
            .background(container)
            .border(BorderStroke(1.dp, outline), shape),
        contentAlignment = Alignment.Center
    ) {
        AnimatedVisibility(
            visible = selected,
            enter = fadeIn(nebEffectsSpec()) + scaleIn(nebFastSpatialSpec(), initialScale = 0.5f),
            exit = fadeOut(nebEffectsSpec()) + scaleOut(nebFastSpatialSpec(), targetScale = 0.5f)
        ) {
            Icon(
                imageVector = Icons.Rounded.Check,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.surface,
                modifier = Modifier.size(15.dp)
            )
        }
    }
}

@Composable
fun NebSelectRow(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    supportingText: String? = null
) {
    val container by animateColorAsState(
        targetValue = if (selected) {
            MaterialTheme.colorScheme.surfaceContainerHigh
        } else {
            Color.Transparent
        },
        animationSpec = nebEffectsSpec(),
        label = "neb_select_row"
    )

    Row(
        modifier = modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = 52.dp)
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(18.dp))
            .background(container)
            .padding(horizontal = 14.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        NebSelectIndicator(selected = selected)
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = label,
                style = if (selected) {
                    MaterialTheme.typography.bodyLargeEmphasized
                } else {
                    MaterialTheme.typography.bodyLarge
                },
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            if (supportingText != null) {
                Text(
                    text = supportingText,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}
