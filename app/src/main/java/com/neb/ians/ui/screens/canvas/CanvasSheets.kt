package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.CanvasNode
import com.neb.ians.data.api.CanvasNodeMeta
import com.neb.ians.data.api.CanvasSnapshot
import com.neb.ians.data.api.CanvasTemplate
import com.neb.ians.ui.components.luminanceIsDark

internal val CANVAS_KINDS = listOf("ai", "note", "question", "source", "comparison", "practice", "summary", "task", "decision", "warning")
internal val CANVAS_META_COLORS = listOf("default", "blue", "green", "amber", "rose", "purple", "slate")
internal val CANVAS_WIDGET_KINDS = listOf("quiz", "flash", "flow", "timeline", "poll")

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CanvasSheetShell(
    onDismiss: () -> Unit,
    content: @Composable () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val isDark = MaterialTheme.colorScheme.surface.luminanceIsDark()
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
        scrimColor = Color.Black.copy(alpha = if (isDark) 0.54f else 0.32f),
        shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp),
        dragHandle = null
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(start = 16.dp, top = 10.dp, end = 16.dp, bottom = 18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Box(
                modifier = Modifier
                    .align(Alignment.CenterHorizontally)
                    .width(42.dp)
                    .height(4.dp)
                    .background(MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.28f), CircleShape)
            )
            content()
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun NodeInspectorSheet(
    node: CanvasNode,
    onDismiss: () -> Unit,
    onSave: (title: String, body: String, kind: String, meta: CanvasNodeMeta) -> Unit,
    onDelete: () -> Unit,
    onRetry: () -> Unit,
    onFocus: () -> Unit
) {
    var title by remember(node.id) { mutableStateOf(node.content?.str("title")?.takeIf { it.isNotBlank() } ?: node.title) }
    var body by remember(node.id) { mutableStateOf(node.content?.str("summary") ?: "") }
    var kind by remember(node.id) { mutableStateOf(node.kind.ifBlank { "note" }) }
    var color by remember(node.id) { mutableStateOf(node.meta?.str("color")?.ifBlank { "default" } ?: "default") }
    var tagsText by remember(node.id) {
        mutableStateOf(node.meta?.arr("tags")?.map { it.asStr() }?.joinToString(", ") ?: "")
    }
    var pinned by remember(node.id) { mutableStateOf(node.meta?.bool("pinned") ?: false) }
    var showDelete by remember { mutableStateOf(false) }

    CanvasSheetShell(onDismiss = onDismiss) {
        Column(
            modifier = Modifier.verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Card", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                TextButton(onClick = onFocus) { Text("Focus") }
                if (node.status == "failed") {
                    TextButton(onClick = onRetry) { Text("Retry") }
                }
                IconButton(onClick = { showDelete = true }) {
                    Icon(Icons.Filled.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                }
            }
            OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, singleLine = true, modifier = Modifier.fillMaxWidth())
            OutlinedTextField(value = body, onValueChange = { body = it }, label = { Text("Body") }, minLines = 3, modifier = Modifier.fillMaxWidth())
            Text("Kind", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CANVAS_KINDS.forEach { k ->
                    FilterChip(selected = kind == k, onClick = { kind = k }, label = { Text(k) })
                }
            }
            Text("Color", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CANVAS_META_COLORS.forEach { c ->
                    FilterChip(selected = color == c, onClick = { color = c }, label = { Text(c) })
                }
            }
            OutlinedTextField(value = tagsText, onValueChange = { tagsText = it }, label = { Text("Tags (comma separated)") }, singleLine = true, modifier = Modifier.fillMaxWidth())
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Pinned", style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
                Switch(checked = pinned, onCheckedChange = { pinned = it })
            }
            Button(
                onClick = {
                    onSave(
                        title, body, kind,
                        CanvasNodeMeta(color, tagsText.split(",").map { it.trim() }.filter { it.isNotBlank() }.take(8), pinned)
                    )
                },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Save card") }
        }
    }

    if (showDelete) {
        AlertDialog(
            onDismissRequest = { showDelete = false },
            title = { Text("Delete card?") },
            text = { Text("This card will be removed from the canvas.") },
            confirmButton = {
                TextButton(onClick = {
                    showDelete = false
                    onDelete()
                }) { Text("Delete") }
            },
            dismissButton = { TextButton(onClick = { showDelete = false }) { Text("Cancel") } }
        )
    }
}

@Composable
fun NoteComposerSheet(
    kinds: List<String> = listOf("note", "question", "source", "task"),
    onDismiss: () -> Unit,
    onSave: (title: String, body: String, kind: String) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var body by remember { mutableStateOf("") }
    var kind by remember { mutableStateOf("note") }

    CanvasSheetShell(onDismiss = onDismiss) {
        Text("New card", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, singleLine = true, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(value = body, onValueChange = { body = it }, label = { Text("Body") }, minLines = 4, modifier = Modifier.fillMaxWidth())
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            kinds.forEach { k ->
                FilterChip(selected = kind == k, onClick = { kind = k }, label = { Text(k) })
            }
        }
        Button(
            onClick = { onSave(title.trim(), body.trim(), kind) },
            modifier = Modifier.fillMaxWidth()
        ) { Text("Add card") }
    }
}

@Composable
fun AnnotateDialog(
    isSticky: Boolean,
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit
) {
    var text by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isSticky) "New sticky" else "New text") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                label = { Text("Text") },
                minLines = if (isSticky) 3 else 1,
                modifier = Modifier.fillMaxWidth()
            )
        },
        confirmButton = {
            TextButton(
                enabled = text.isNotBlank(),
                onClick = {
                    onConfirm(text.trim())
                }
            ) { Text("Place") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel") } }
    )
}

@Composable
fun HistorySheet(
    snapshots: List<CanvasSnapshot>,
    onCreate: (String) -> Unit,
    onRestore: (String) -> Unit,
    onDismiss: () -> Unit
) {
    var label by remember { mutableStateOf("") }
    var restoreId by remember { mutableStateOf<String?>(null) }

    CanvasSheetShell(onDismiss = onDismiss) {
        Text("Checkpoints", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Row(verticalAlignment = Alignment.CenterVertically) {
            OutlinedTextField(
                value = label,
                onValueChange = { label = it },
                label = { Text("Checkpoint label") },
                singleLine = true,
                modifier = Modifier.weight(1f)
            )
            Spacer(Modifier.width(8.dp))
            IconButton(onClick = {
                onCreate(label.trim())
                label = ""
            }) {
                Icon(Icons.Filled.Add, contentDescription = "Save checkpoint")
            }
        }
        if (snapshots.isEmpty()) {
            Text("No checkpoints yet — save one before big changes.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        } else {
            snapshots.forEach { snapshot ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.surfaceContainerLow)
                        .clickable { restoreId = snapshot.id }
                        .padding(14.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(snapshot.label.ifBlank { "Checkpoint" }, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text("${snapshot.nodeCount} cards", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Icon(Icons.Filled.Refresh, contentDescription = "Restore", tint = MaterialTheme.colorScheme.primary)
                }
            }
        }
    }

    restoreId?.let { id ->
        AlertDialog(
            onDismissRequest = { restoreId = null },
            title = { Text("Restore checkpoint?") },
            text = { Text("Current cards are checkpointed first, then replaced.") },
            confirmButton = {
                TextButton(onClick = {
                    onRestore(id)
                    restoreId = null
                }) { Text("Restore") }
            },
            dismissButton = { TextButton(onClick = { restoreId = null }) { Text("Cancel") } }
        )
    }
}

@Composable
fun ShareSheet(
    shareUrl: String,
    onEnable: () -> Unit,
    onRevoke: () -> Unit,
    onCopy: (String) -> Unit,
    onDismiss: () -> Unit
) {
    CanvasSheetShell(onDismiss = onDismiss) {
        Text("Share canvas", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        if (shareUrl.isBlank()) {
            Text("Anyone with the link can view a read-only copy.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Button(onClick = onEnable, modifier = Modifier.fillMaxWidth()) { Text("Enable share link") }
        } else {
            OutlinedTextField(value = shareUrl, onValueChange = {}, readOnly = true, singleLine = true, modifier = Modifier.fillMaxWidth())
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = { onCopy(shareUrl) }, modifier = Modifier.weight(1f)) { Text("Copy link") }
                OutlinedButton(onClick = onRevoke, modifier = Modifier.weight(1f)) { Text("Revoke") }
            }
        }
    }
}

@Composable
fun TemplatesSheet(
    templates: List<CanvasTemplate>,
    onPick: (CanvasTemplate) -> Unit,
    onDismiss: () -> Unit
) {
    CanvasSheetShell(onDismiss = onDismiss) {
        Text("Templates", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        if (templates.isEmpty()) {
            Text("No templates available.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        } else {
            templates.forEach { template ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.surfaceContainerLow)
                        .clickable { onPick(template) }
                        .padding(14.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(template.name, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                        if (template.description.isNotBlank()) {
                            Text(template.description, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CommandPaletteSheet(
    nodes: List<CanvasNode>,
    onPick: (CanvasNode) -> Unit,
    onDismiss: () -> Unit
) {
    var query by remember { mutableStateOf("") }
    val hits = remember(query, nodes) {
        if (query.isBlank()) nodes.take(20)
        else nodes.filter {
            it.title.contains(query, ignoreCase = true) ||
                (it.content?.str("title")?.contains(query, ignoreCase = true) == true) ||
                (it.content?.str("summary")?.contains(query, ignoreCase = true) == true)
        }.take(40)
    }

    CanvasSheetShell(onDismiss = onDismiss) {
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            label = { Text("Jump to card…") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        Column(
            modifier = Modifier.height(320.dp).verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            hits.forEach { node ->
                val title = node.content?.str("title")?.takeIf { it.isNotBlank() } ?: node.title.ifBlank { "Untitled" }
                Text(
                    title,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .clickable { onPick(node) }
                        .padding(horizontal = 12.dp, vertical = 10.dp)
                )
            }
        }
    }
}
