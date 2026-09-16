package com.neb.ians.ui.screens.canvas

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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Dashboard
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.DriveFileRenameOutline
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.CanvasBoard
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebCard
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebTopBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CanvasListScreen(
    onNavigateBack: () -> Unit,
    onOpenBoard: (String) -> Unit,
    viewModel: CanvasListViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val snackbarHostState = remember { SnackbarHostState() }
    var showNewDialog by remember { mutableStateOf(false) }
    var templateKey by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(uiState.snackbarMessage) {
        uiState.snackbarMessage?.let {
            snackbarHostState.showSnackbar(it)
            viewModel.consumeSnackbar()
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            NebTopBar(
                showBrand = false,
                title = "Canvas",
                onBack = onNavigateBack
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        PullToRefreshBox(
            isRefreshing = uiState.isRefreshing,
            onRefresh = { viewModel.refresh(pull = true) },
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when {
                uiState.isLoading && uiState.boards.isEmpty() -> {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                uiState.error != null && uiState.boards.isEmpty() -> {
                    Box(Modifier.fillMaxSize().padding(16.dp), contentAlignment = Alignment.Center) {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = { viewModel.refresh() }
                        )
                    }
                }
                else -> {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        item(key = "new") {
                            Button(
                                onClick = { showNewDialog = true },
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Icon(Icons.Filled.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(8.dp))
                                Text("New canvas")
                            }
                        }
                        if (uiState.templates.isNotEmpty()) {
                            item(key = "templates_title") {
                                Text(
                                    "Start from a template",
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                            }
                            item(key = "templates") {
                                LazyRow(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                                    items(uiState.templates, key = { it.key }) { template ->
                                        NebCard(
                                            onClick = {
                                                templateKey = template.key
                                                showNewDialog = true
                                            },
                                            modifier = Modifier.width(180.dp)
                                        ) {
                                            Column(Modifier.padding(14.dp)) {
                                                Text(
                                                    template.name,
                                                    style = MaterialTheme.typography.titleMedium,
                                                    fontWeight = FontWeight.SemiBold,
                                                    color = MaterialTheme.colorScheme.onSurface,
                                                    maxLines = 1,
                                                    overflow = TextOverflow.Ellipsis
                                                )
                                                Spacer(Modifier.height(4.dp))
                                                Text(
                                                    template.description.ifBlank { "Guided knowledge map" },
                                                    style = MaterialTheme.typography.bodySmall,
                                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                                    maxLines = 2,
                                                    overflow = TextOverflow.Ellipsis
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        item(key = "boards_title") {
                            Text(
                                "Your canvases",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                        if (uiState.boards.isEmpty()) {
                            item(key = "empty") {
                                NebEmptyState(
                                    icon = Icons.Filled.Dashboard,
                                    title = "No canvases yet",
                                    subtitle = "Create one to start mapping what you learn with Neby AI."
                                )
                            }
                        } else {
                            items(uiState.boards, key = { it.id }) { board ->
                                CanvasBoardRow(
                                    board = board,
                                    onOpen = { onOpenBoard(board.id) },
                                    onRename = { viewModel.renameBoard(board.id, it) },
                                    onDelete = { viewModel.deleteBoard(board.id) }
                                )
                            }
                        }
                    }
                }
            }
        }
    }

    if (showNewDialog) {
        var name by remember(templateKey) { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = {
                showNewDialog = false
                templateKey = null
            },
            title = { Text(if (templateKey == null) "New canvas" else "New from template") },
            text = {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Canvas name") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(
                    enabled = !uiState.isWorking,
                    onClick = {
                        val key = templateKey
                        templateKey = null
                        showNewDialog = false
                        if (key == null) viewModel.createBoard(name, onOpenBoard)
                        else viewModel.createFromTemplate(key, name, onOpenBoard)
                    }
                ) { Text("Create") }
            },
            dismissButton = {
                TextButton(onClick = {
                    showNewDialog = false
                    templateKey = null
                }) { Text("Cancel") }
            }
        )
    }
}

@Composable
private fun CanvasBoardRow(
    board: CanvasBoard,
    onOpen: () -> Unit,
    onRename: (String) -> Unit,
    onDelete: () -> Unit
) {
    var menuOpen by remember { mutableStateOf(false) }
    var showRename by remember { mutableStateOf(false) }
    var showDelete by remember { mutableStateOf(false) }

    NebCard(onClick = onOpen, modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    board.title.ifBlank { "Untitled canvas" },
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    "${board.nodeCount} cards",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Box {
                IconButton(onClick = { menuOpen = true }) {
                    Icon(Icons.Outlined.MoreVert, contentDescription = "Options")
                }
                DropdownMenu(expanded = menuOpen, onDismissRequest = { menuOpen = false }) {
                    DropdownMenuItem(
                        text = { Text("Rename") },
                        leadingIcon = { Icon(Icons.Outlined.DriveFileRenameOutline, contentDescription = null) },
                        onClick = {
                            menuOpen = false
                            showRename = true
                        }
                    )
                    DropdownMenuItem(
                        text = { Text("Delete") },
                        leadingIcon = { Icon(Icons.Outlined.Delete, contentDescription = null) },
                        onClick = {
                            menuOpen = false
                            showDelete = true
                        }
                    )
                }
            }
        }
    }

    if (showRename) {
        var name by remember { mutableStateOf(board.title) }
        AlertDialog(
            onDismissRequest = { showRename = false },
            title = { Text("Rename canvas") },
            text = {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Canvas name") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    showRename = false
                    onRename(name)
                }) { Text("Save") }
            },
            dismissButton = { TextButton(onClick = { showRename = false }) { Text("Cancel") } }
        )
    }

    if (showDelete) {
        AlertDialog(
            onDismissRequest = { showDelete = false },
            title = { Text("Delete canvas?") },
            text = { Text("“${board.title.ifBlank { "Untitled canvas" }}” and all its cards will be deleted.") },
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
