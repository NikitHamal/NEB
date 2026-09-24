@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.MarkdownInlineText
import com.neb.ians.ui.components.NebConfirmDialog
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebShapes
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.components.nebShape

@Composable
fun NewBoardDialog(
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit
) {
    var title by remember { mutableStateOf("") }

    NebDialog(
        onDismissRequest = onDismiss,
        title = "New canvas",
        supportingText = "Give the board a name. You can rename it later.",
        icon = Icons.Outlined.SpaceDashboard,
        confirm = NebDialogAction("Create", { onConfirm(title.trim().ifBlank { "Untitled Canvas" }) }),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebDialogTextField(
            value = title,
            onValueChange = { title = it },
            placeholder = "e.g. Quantum Physics"
        )
    }
}

@Composable
fun RenameBoardDialog(
    initialTitle: String,
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit
) {
    var title by remember { mutableStateOf(initialTitle) }

    NebDialog(
        onDismissRequest = onDismiss,
        title = "Rename canvas",
        icon = Icons.Outlined.DriveFileRenameOutline,
        confirm = NebDialogAction("Save", { onConfirm(title.trim().ifBlank { "Untitled Canvas" }) }),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebDialogTextField(
            value = title,
            onValueChange = { title = it },
            placeholder = "Canvas title"
        )
    }
}

@Composable
fun DeleteBoardDialog(
    boardTitle: String,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    NebConfirmDialog(
        title = "Delete canvas",
        message = "\"$boardTitle\" and every card in it will be permanently removed. This cannot be undone.",
        confirmLabel = "Delete",
        onConfirm = onConfirm,
        onDismiss = onDismiss,
        icon = Icons.Outlined.DeleteOutline,
        destructive = true
    )
}

@Composable
fun TemplatePickerModalSheet(
    onDismiss: () -> Unit,
    onSelectTemplate: (CanvasTemplate) -> Unit
) {
    val templates = remember { CanvasTemplates.getTemplates() }

    NebModalSheet(
        onDismiss = onDismiss,
        title = "Templates",
        subtitle = "Start from a blueprint instead of a blank board.",
        showClose = true
    ) {
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(horizontal = 22.dp),
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(max = 460.dp)
        ) {
            itemsIndexed(templates, key = { _, it -> it.key }) { index, template ->
                Surface(
                    shape = RoundedCornerShape(if (index % 2 == 0) 22.dp else 14.dp),
                    color = MaterialTheme.colorScheme.surfaceContainerHigh,
                    contentColor = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier
                        .fillMaxWidth()
                        .nebPressable { onSelectTemplate(template) }
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Box(
                            modifier = Modifier
                                .size(38.dp)
                                .clip(nebShape(NebShapes.option(index)))
                                .background(MaterialTheme.colorScheme.secondaryContainer),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = when (template.iconName) {
                                    "school" -> Icons.Outlined.School
                                    "travel_explore" -> Icons.Outlined.TravelExplore
                                    "edit_note" -> Icons.Outlined.EditNote
                                    "account_tree" -> Icons.Outlined.AccountTree
                                    "psychology" -> Icons.Outlined.Psychology
                                    else -> Icons.Outlined.SpaceDashboard
                                },
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSecondaryContainer,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                        Spacer(Modifier.height(12.dp))
                        Text(
                            text = template.name,
                            style = MaterialTheme.typography.titleSmallEmphasized
                        )
                        Text(
                            text = template.subtitle,
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = template.description,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 3,
                            modifier = Modifier.padding(top = 6.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun NodeDetailDialog(
    node: CanvasNode,
    onDismiss: () -> Unit
) {
    NebDialog(
        onDismissRequest = onDismiss,
        title = node.title.ifBlank { node.prompt },
        dismiss = NebDialogAction("Close", onDismiss)
    ) {
        if (node.content.summary.isNotBlank()) {
            MarkdownInlineText(
                markdown = node.content.summary,
                style = MaterialTheme.typography.bodyMedium.copy(lineHeight = 22.sp),
                color = MaterialTheme.colorScheme.onSurface
            )
        }

        node.content.sections.forEach { sec ->
            sec.title?.let { t ->
                Text(
                    text = t,
                    style = MaterialTheme.typography.titleSmallEmphasized,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.padding(top = 6.dp)
                )
            }
            sec.content?.let { c ->
                MarkdownInlineText(
                    markdown = c,
                    style = MaterialTheme.typography.bodySmall.copy(lineHeight = 20.sp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            sec.bulletItems?.forEach { b ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Box(
                        modifier = Modifier
                            .padding(top = 8.dp)
                            .width(7.dp)
                            .height(1.5.dp)
                            .background(MaterialTheme.colorScheme.onSurfaceVariant)
                    )
                    Text(
                        text = b,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
