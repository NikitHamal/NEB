package com.neb.ians.ui.screens.canvas

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Redo
import androidx.compose.material.icons.automirrored.filled.Undo
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.ViewSidebar
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.DriveFileRenameOutline
import androidx.compose.material.icons.outlined.FitScreen
import androidx.compose.material.icons.outlined.GridView
import androidx.compose.material.icons.outlined.Remove
import androidx.compose.material.icons.outlined.RestartAlt
import androidx.compose.material.icons.outlined.SpaceDashboard
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec

// ---------------------------------------------------------------------------
// The chrome around the board.
//
// Two anchors and one rail. Back on the left, the boards drawer on the right,
// and between them a single grouped toolbar — view, zoom, everything else —
// so the middle of the screen stays the drawing and not the controls. History
// and delete sit just under it, on the side you reach with your thumb.
// ---------------------------------------------------------------------------

@Composable
fun CanvasTopBar(
    scale: Float,
    hasSelection: Boolean,
    onNavigateBack: () -> Unit,
    onToggleSidebar: () -> Unit,
    onFitView: () -> Unit,
    onZoomIn: () -> Unit,
    onZoomOut: () -> Unit,
    onResetZoom: () -> Unit,
    onAutoLayout: () -> Unit,
    onDuplicateSelected: () -> Unit,
    onRenameBoard: () -> Unit,
    onNewBoard: () -> Unit,
    onOpenTemplates: () -> Unit,
    onDeleteBoard: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isDark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    var menuOpen by remember { mutableStateOf(false) }

    Row(
        modifier = modifier
            .fillMaxWidth()
            .statusBarsPadding()
            .height(56.dp)
            .padding(horizontal = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        CanvasChromeButton(
            icon = Icons.AutoMirrored.Outlined.ArrowBack,
            label = "Back",
            onClick = onNavigateBack,
            size = 42.dp
        )

        Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.Center) {
            CanvasRail(isDark = isDark) {
                CanvasChromeButton(
                    icon = Icons.Outlined.FitScreen,
                    label = "Fit board to screen",
                    onClick = onFitView
                )
                CanvasRailDivider()
                CanvasChromeButton(
                    icon = Icons.Outlined.Remove,
                    label = "Zoom out",
                    onClick = onZoomOut,
                    size = 36.dp,
                    iconSize = 17.dp
                )
                Text(
                    text = zoomLabel(scale),
                    style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Medium),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.widthIn(min = 40.dp),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )
                CanvasChromeButton(
                    icon = Icons.Outlined.Add,
                    label = "Zoom in",
                    onClick = onZoomIn,
                    size = 36.dp,
                    iconSize = 17.dp
                )
                CanvasRailDivider()
                Box {
                    CanvasChromeButton(
                        icon = Icons.Filled.MoreVert,
                        label = "Canvas options",
                        onClick = { menuOpen = true }
                    )
                    CanvasOverflowMenu(
                        expanded = menuOpen,
                        hasSelection = hasSelection,
                        onDismiss = { menuOpen = false },
                        onAutoLayout = onAutoLayout,
                        onResetZoom = onResetZoom,
                        onDuplicateSelected = onDuplicateSelected,
                        onRenameBoard = onRenameBoard,
                        onNewBoard = onNewBoard,
                        onOpenTemplates = onOpenTemplates,
                        onDeleteBoard = onDeleteBoard
                    )
                }
            }
        }

        CanvasChromeButton(
            icon = Icons.AutoMirrored.Outlined.ViewSidebar,
            label = "Canvases",
            onClick = onToggleSidebar,
            size = 42.dp
        )
    }
}

@Composable
fun CanvasQuickActions(
    canUndo: Boolean,
    canRedo: Boolean,
    hasSelection: Boolean,
    onUndo: () -> Unit,
    onRedo: () -> Unit,
    onDeleteSelected: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isDark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    CanvasRail(isDark = isDark, modifier = modifier) {
        CanvasChromeButton(
            icon = Icons.AutoMirrored.Filled.Undo,
            label = "Undo",
            onClick = onUndo,
            enabled = canUndo,
            size = 38.dp,
            iconSize = 17.dp
        )
        CanvasChromeButton(
            icon = Icons.AutoMirrored.Filled.Redo,
            label = "Redo",
            onClick = onRedo,
            enabled = canRedo,
            size = 38.dp,
            iconSize = 17.dp
        )
        CanvasRailDivider()
        CanvasChromeButton(
            icon = Icons.Outlined.DeleteOutline,
            label = "Delete selected card",
            onClick = onDeleteSelected,
            enabled = hasSelection,
            size = 38.dp,
            iconSize = 17.dp,
            tint = MaterialTheme.colorScheme.error
        )
    }
}

@Composable
private fun CanvasRail(
    isDark: Boolean,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(18.dp),
        color = if (isDark) MaterialTheme.colorScheme.surfaceContainerHigh else Color.White,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.7f)),
        tonalElevation = 0.dp,
        shadowElevation = 2.dp
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 3.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(1.dp)
        ) {
            content()
        }
    }
}

@Composable
private fun CanvasRailDivider() {
    VerticalDivider(
        modifier = Modifier
            .height(20.dp)
            .padding(horizontal = 3.dp),
        color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.8f)
    )
}

@Composable
private fun CanvasChromeButton(
    icon: ImageVector,
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    size: Dp = 40.dp,
    iconSize: Dp = 19.dp,
    tint: Color = MaterialTheme.colorScheme.onSurface
) {
    val resolved by animateColorAsState(
        targetValue = if (enabled) tint else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.28f),
        animationSpec = nebEffectsSpec(),
        label = "chromeTint"
    )
    Box(
        modifier = modifier
            .nebPressable(enabled = enabled, onClick = onClick)
            .size(size)
            .clip(CircleShape),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = label,
            tint = resolved,
            modifier = Modifier.size(iconSize)
        )
    }
}

@Composable
private fun CanvasOverflowMenu(
    expanded: Boolean,
    hasSelection: Boolean,
    onDismiss: () -> Unit,
    onAutoLayout: () -> Unit,
    onResetZoom: () -> Unit,
    onDuplicateSelected: () -> Unit,
    onRenameBoard: () -> Unit,
    onNewBoard: () -> Unit,
    onOpenTemplates: () -> Unit,
    onDeleteBoard: () -> Unit
) {
    DropdownMenu(expanded = expanded, onDismissRequest = onDismiss) {
        CanvasMenuItem("Organise layout", Icons.Outlined.AccountTree) { onDismiss(); onAutoLayout() }
        CanvasMenuItem("Reset zoom", Icons.Outlined.RestartAlt) { onDismiss(); onResetZoom() }
        CanvasMenuItem(
            text = "Duplicate card",
            icon = Icons.Outlined.ContentCopy,
            enabled = hasSelection
        ) { onDismiss(); onDuplicateSelected() }

        HorizontalDivider(modifier = Modifier.padding(vertical = 6.dp))

        CanvasMenuItem("Rename canvas", Icons.Outlined.DriveFileRenameOutline) { onDismiss(); onRenameBoard() }
        CanvasMenuItem("New canvas", Icons.Outlined.SpaceDashboard) { onDismiss(); onNewBoard() }
        CanvasMenuItem("Browse templates", Icons.Outlined.GridView) { onDismiss(); onOpenTemplates() }

        HorizontalDivider(modifier = Modifier.padding(vertical = 6.dp))

        CanvasMenuItem(
            text = "Delete canvas",
            icon = Icons.Outlined.DeleteOutline,
            tint = MaterialTheme.colorScheme.error
        ) { onDismiss(); onDeleteBoard() }
    }
}

@Composable
private fun CanvasMenuItem(
    text: String,
    icon: ImageVector,
    enabled: Boolean = true,
    tint: Color = MaterialTheme.colorScheme.onSurface,
    onClick: () -> Unit
) {
    DropdownMenuItem(
        enabled = enabled,
        text = {
            Text(
                text = text,
                style = MaterialTheme.typography.bodyMedium,
                color = if (enabled) tint else tint.copy(alpha = 0.4f)
            )
        },
        leadingIcon = {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = if (enabled) tint else tint.copy(alpha = 0.4f),
                modifier = Modifier.size(18.dp)
            )
        },
        onClick = onClick
    )
}
