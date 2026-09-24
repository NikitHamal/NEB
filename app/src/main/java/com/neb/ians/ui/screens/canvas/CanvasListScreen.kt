package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.OpenInNew
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Draw
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.SpaceDashboard
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebChipRow
import com.neb.ians.ui.components.NebConfirmDialog
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebFilterChip
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.util.formatTimeAgo

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CanvasListScreen(
    onOpenCanvas: (String) -> Unit,
    onSearchClick: () -> Unit = {},
    onUploadClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    viewModel: CanvasListViewModel = hiltViewModel()
) {
    val allBoards by viewModel.allBoards.collectAsStateWithLifecycle()
    val filteredBoards by viewModel.filteredBoards.collectAsStateWithLifecycle()
    val searchQuery by viewModel.searchQuery.collectAsStateWithLifecycle()
    val createDialogOpen by viewModel.createDialogOpen.collectAsStateWithLifecycle()
    val renameBoardTarget by viewModel.renameBoardTarget.collectAsStateWithLifecycle()
    val deleteBoardTarget by viewModel.deleteBoardTarget.collectAsStateWithLifecycle()
    val isCreating by viewModel.isCreating.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            WebTopBar(
                onSearchClick = onSearchClick,
                onUploadClick = onUploadClick,
                onNotificationsClick = onNotificationsClick,
                onProfileClick = onProfileClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface,
        floatingActionButton = {
            if (allBoards.isNotEmpty()) {
                FloatingActionButton(
                    onClick = { viewModel.openCreateDialog() },
                    modifier = Modifier
                        .navigationBarsPadding()
                        .padding(bottom = 88.dp, end = 12.dp),
                    shape = CircleShape,
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                ) {
                    Icon(
                        imageVector = Icons.Filled.Add,
                        contentDescription = "Create New Canvas"
                    )
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            if (allBoards.isNotEmpty()) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { viewModel.onSearchQueryChange(it) },
                    placeholder = {
                        Text(
                            text = "Search canvases",
                            style = MaterialTheme.typography.bodyLarge,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Outlined.Search,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(20.dp)
                        )
                    },
                    trailingIcon = {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { viewModel.onSearchQueryChange("") }) {
                                Icon(
                                    imageVector = Icons.Filled.Clear,
                                    contentDescription = "Clear search",
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                    },
                    singleLine = true,
                    maxLines = 1,
                    textStyle = MaterialTheme.typography.bodyLarge,
                    shape = RoundedCornerShape(50),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                        focusedBorderColor = MaterialTheme.colorScheme.onSurface,
                        unfocusedBorderColor = Color.Transparent
                    ),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                        .heightIn(min = 52.dp)
                )
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(1f)
            ) {
                if (allBoards.isEmpty()) {
                    EmptyCanvasState(
                        onCreateNew = { viewModel.openCreateDialog() },
                        onSelectTemplate = { templateKey, title ->
                            viewModel.createCanvas(title, templateKey) { newId ->
                                onOpenCanvas(newId)
                            }
                        },
                        modifier = Modifier.fillMaxSize()
                    )
                } else if (filteredBoards.isEmpty()) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Search,
                                contentDescription = null,
                                modifier = Modifier.size(48.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(
                                text = "No canvases matching \"$searchQuery\"",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            TextButton(onClick = { viewModel.onSearchQueryChange("") }) {
                                Text("Clear search")
                            }
                        }
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        item {
                            Text(
                                text = "My Canvases (${filteredBoards.size})",
                                style = MaterialTheme.typography.titleSmall,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                            )
                        }

                        items(filteredBoards, key = { it.id }) { board ->
                            CanvasBoardCard(
                                board = board,
                                onClick = { onOpenCanvas(board.id) },
                                onRename = { viewModel.setRenameBoardTarget(board) },
                                onDuplicate = {
                                    viewModel.duplicateCanvas(board.id) { copyId ->
                                        onOpenCanvas(copyId)
                                    }
                                },
                                onDelete = { viewModel.setDeleteBoardTarget(board) }
                            )
                        }
                    }
                }
            }
        }
    }

    if (createDialogOpen) {
        CreateCanvasDialog(
            isCreating = isCreating,
            onDismiss = { viewModel.closeCreateDialog() },
            onCreate = { title, templateKey ->
                viewModel.createCanvas(title, templateKey) { newId ->
                    onOpenCanvas(newId)
                }
            }
        )
    }

    renameBoardTarget?.let { board ->
        RenameCanvasDialog(
            currentTitle = board.title,
            onDismiss = { viewModel.setRenameBoardTarget(null) },
            onConfirm = { newTitle ->
                viewModel.renameCanvas(board.id, newTitle)
            }
        )
    }

    deleteBoardTarget?.let { board ->
        NebConfirmDialog(
            title = "Delete canvas?",
            message = "\"${board.title}\" and every node in it will be permanently removed.",
            confirmLabel = "Delete",
            onConfirm = { viewModel.deleteCanvas(board.id) },
            onDismiss = { viewModel.setDeleteBoardTarget(null) },
            icon = Icons.Outlined.Delete,
            destructive = true
        )
    }
}

@Composable
private fun EmptyCanvasState(
    onCreateNew: () -> Unit,
    onSelectTemplate: (templateKey: String?, title: String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.padding(horizontal = 20.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        contentPadding = PaddingValues(top = 28.dp, bottom = 96.dp)
    ) {
        item {
            Box(
                modifier = Modifier
                    .size(96.dp)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            colors = listOf(
                                MaterialTheme.colorScheme.primaryContainer,
                                MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)
                            )
                        )
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.Draw,
                    contentDescription = null,
                    modifier = Modifier.size(46.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
            }

            Spacer(modifier = Modifier.height(20.dp))

            Text(
                text = "No Canvases Yet",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Create your first visual board to brainstorm concepts, generate AI study cards, and organize complex topics.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                lineHeight = 22.sp,
                modifier = Modifier.padding(horizontal = 16.dp)
            )

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = onCreateNew,
                shape = RoundedCornerShape(14.dp),
                contentPadding = PaddingValues(horizontal = 24.dp, vertical = 12.dp)
            ) {
                Icon(
                    imageVector = Icons.Filled.Add,
                    contentDescription = null,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "Create New Canvas",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.SemiBold
                )
            }

            Spacer(modifier = Modifier.height(36.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                HorizontalDivider(modifier = Modifier.weight(1f))
                Text(
                    text = "Or start with a template",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(horizontal = 12.dp)
                )
                HorizontalDivider(modifier = Modifier.weight(1f))
            }

            Spacer(modifier = Modifier.height(20.dp))
        }

        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                TemplateQuickCard(
                    title = "Concept Mastery",
                    subtitle = "Feynman Technique for breaking down difficult concepts simply",
                    icon = Icons.Outlined.Psychology,
                    badgeColor = MaterialTheme.colorScheme.onSurface,
                    onClick = { onSelectTemplate("concept-master", "Concept Mastery") }
                )
                TemplateQuickCard(
                    title = "Blank Canvas",
                    subtitle = "Freeform exploration with custom node connections & Neby AI",
                    icon = Icons.Outlined.SpaceDashboard,
                    badgeColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    onClick = { onSelectTemplate("blank", "Untitled Canvas") }
                )
            }
        }
    }
}

@Composable
private fun TemplateQuickCard(
    title: String,
    subtitle: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    badgeColor: Color,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerLow
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(badgeColor.copy(alpha = 0.12f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = badgeColor,
                    modifier = Modifier.size(24.dp)
                )
            }
            Spacer(modifier = Modifier.width(14.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    lineHeight = 16.sp
                )
            }
            Icon(
                imageVector = Icons.AutoMirrored.Outlined.OpenInNew,
                contentDescription = "Use template",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(18.dp)
            )
        }
    }
}

@Composable
private fun CanvasBoardCard(
    board: CanvasBoard,
    onClick: () -> Unit,
    onRename: () -> Unit,
    onDuplicate: () -> Unit,
    onDelete: () -> Unit
) {
    var menuExpanded by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(
                    modifier = Modifier.weight(1f),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(38.dp)
                            .clip(RoundedCornerShape(10.dp))
                            .background(MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Draw,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Text(
                            text = board.title,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Spacer(modifier = Modifier.height(2.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.AccountTree,
                                contentDescription = null,
                                modifier = Modifier.size(13.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = if (board.nodeCount > 0) "${board.nodeCount} nodes" else "Blank canvas",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "·",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Icon(
                                imageVector = Icons.Outlined.Schedule,
                                contentDescription = null,
                                modifier = Modifier.size(13.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = formatTimeAgo(board.updatedAt),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }

                Box {
                    IconButton(onClick = { menuExpanded = true }) {
                        Icon(
                            imageVector = Icons.Filled.MoreVert,
                            contentDescription = "Options",
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    DropdownMenu(
                        expanded = menuExpanded,
                        onDismissRequest = { menuExpanded = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Open Canvas") },
                            leadingIcon = {
                                Icon(
                                    Icons.AutoMirrored.Outlined.OpenInNew,
                                    contentDescription = null,
                                    modifier = Modifier.size(18.dp)
                                )
                            },
                            onClick = {
                                menuExpanded = false
                                onClick()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Rename") },
                            leadingIcon = {
                                Icon(
                                    Icons.Outlined.Edit,
                                    contentDescription = null,
                                    modifier = Modifier.size(18.dp)
                                )
                            },
                            onClick = {
                                menuExpanded = false
                                onRename()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Duplicate") },
                            leadingIcon = {
                                Icon(
                                    Icons.Outlined.ContentCopy,
                                    contentDescription = null,
                                    modifier = Modifier.size(18.dp)
                                )
                            },
                            onClick = {
                                menuExpanded = false
                                onDuplicate()
                            }
                        )
                        HorizontalDivider()
                        DropdownMenuItem(
                            text = {
                                Text(
                                    "Delete",
                                    color = MaterialTheme.colorScheme.error
                                )
                            },
                            leadingIcon = {
                                Icon(
                                    Icons.Outlined.Delete,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.error,
                                    modifier = Modifier.size(18.dp)
                                )
                            },
                            onClick = {
                                menuExpanded = false
                                onDelete()
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun CreateCanvasDialog(
    isCreating: Boolean,
    onDismiss: () -> Unit,
    onCreate: (title: String, templateKey: String?) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var selectedTemplateKey by remember { mutableStateOf<String?>(null) }

    val templates = remember {
        listOf(
            "blank" to "Blank Canvas",
            "concept-master" to "Concept Mastery"
        )
    }

    NebDialog(
        onDismissRequest = { if (!isCreating) onDismiss() },
        title = "New canvas",
        supportingText = "Name the board and pick a starting shape.",
        icon = Icons.Outlined.SpaceDashboard,
        dismissOnClickOutside = !isCreating,
        confirm = NebDialogAction(
            label = if (isCreating) "Creating…" else "Create & open",
            onClick = {
                val finalTitle = title.trim().ifBlank {
                    if (selectedTemplateKey == "concept-master") "Concept Mastery" else "Untitled Canvas"
                }
                onCreate(finalTitle, selectedTemplateKey)
            },
            enabled = !isCreating
        ),
        dismiss = NebDialogAction("Cancel", onDismiss, enabled = !isCreating)
    ) {
        NebDialogTextField(
            value = title,
            onValueChange = { title = it },
            label = "Canvas title",
            placeholder = "e.g. Physics Optics"
        )
        NebSectionLabel(text = "Starting template")
        NebChipRow {
            templates.forEach { (key, name) ->
                val isSelected = selectedTemplateKey == key || (key == "blank" && selectedTemplateKey == null)
                NebFilterChip(
                    label = name,
                    selected = isSelected,
                    enabled = !isCreating,
                    onClick = { selectedTemplateKey = key }
                )
            }
        }
    }
}

@Composable
private fun RenameCanvasDialog(
    currentTitle: String,
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit
) {
    var title by remember { mutableStateOf(currentTitle) }

    NebDialog(
        onDismissRequest = onDismiss,
        title = "Rename canvas",
        icon = Icons.Outlined.Edit,
        confirm = NebDialogAction(
            label = "Save",
            onClick = { if (title.isNotBlank()) onConfirm(title.trim()) },
            enabled = title.isNotBlank()
        ),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebDialogTextField(
            value = title,
            onValueChange = { title = it },
            label = "Title"
        )
    }
}
