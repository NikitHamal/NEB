package com.consica.code.ui.screens.workspace

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.ui.components.EcoCard
import java.text.DateFormat
import java.util.Date

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WorkspacesScreen(
    onOpenWorkspace: (Long) -> Unit,
    onBack: () -> Unit,
    viewModel: WorkspacesViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()
    var showCreate by remember { mutableStateOf(false) }
    var pendingDelete by remember { mutableStateOf<WorkspaceEntity?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.workspaces_title), style = MaterialTheme.typography.titleLarge) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { showCreate = true }) {
                Icon(Icons.Default.Add, contentDescription = stringResource(R.string.workspaces_new))
            }
        },
    ) { padding ->
        if (state.workspaces.isEmpty()) {
            Column(
                Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
            ) {
                Text("🪴", style = MaterialTheme.typography.displayMedium)
                Spacer(Modifier.height(12.dp))
                Text(
                    stringResource(R.string.workspaces_empty),
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        } else {
            LazyColumn(
                Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(start = 20.dp, end = 20.dp, bottom = 96.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                items(state.workspaces, key = { it.id }) { workspace ->
                    WorkspaceCard(
                        workspace = workspace,
                        onOpen = { onOpenWorkspace(workspace.id) },
                        onDelete = { pendingDelete = workspace },
                    )
                }
            }
        }
    }

    if (showCreate) {
        CreateWorkspaceDialog(
            onDismiss = { showCreate = false },
            onCreate = { name, language ->
                showCreate = false
                viewModel.create(name, language) { id -> onOpenWorkspace(id) }
            },
        )
    }

    pendingDelete?.let { workspace ->
        AlertDialog(
            onDismissRequest = { pendingDelete = null },
            title = { Text(stringResource(R.string.workspaces_delete)) },
            text = { Text(stringResource(R.string.workspaces_delete_confirm)) },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.delete(workspace.id)
                    pendingDelete = null
                }) {
                    Text(stringResource(R.string.workspaces_delete), color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { pendingDelete = null }) {
                    Text(stringResource(R.string.workspaces_cancel))
                }
            },
        )
    }
}

@Composable
private fun WorkspaceCard(
    workspace: WorkspaceEntity,
    onOpen: () -> Unit,
    onDelete: () -> Unit,
) {
    EcoCard(modifier = Modifier.fillMaxWidth(), onClick = onOpen) {
        Row(
            Modifier.padding(start = 16.dp, end = 8.dp, top = 14.dp, bottom = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                if (workspace.language == TrackLanguage.HTML.name) "🌐" else "🐍",
                style = MaterialTheme.typography.headlineMedium,
            )
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text(workspace.name, style = MaterialTheme.typography.titleMedium)
                Text(
                    stringResource(
                        R.string.workspaces_updated,
                        DateFormat.getDateInstance(DateFormat.MEDIUM).format(Date(workspace.updatedAt)),
                    ),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            IconButton(onClick = onDelete) {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = stringResource(R.string.workspaces_delete),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun CreateWorkspaceDialog(
    onDismiss: () -> Unit,
    onCreate: (String, TrackLanguage) -> Unit,
) {
    var name by remember { mutableStateOf("") }
    var language by remember { mutableStateOf(TrackLanguage.PYTHON) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(stringResource(R.string.workspaces_new)) },
        text = {
            Column {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it.take(40) },
                    label = { Text(stringResource(R.string.workspaces_name_hint)) },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                )
                Spacer(Modifier.height(12.dp))
                Text(
                    stringResource(R.string.workspaces_language),
                    style = MaterialTheme.typography.labelLarge,
                )
                Spacer(Modifier.height(6.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = language == TrackLanguage.PYTHON,
                        onClick = { language = TrackLanguage.PYTHON },
                        label = { Text("🐍 Python") },
                    )
                    FilterChip(
                        selected = language == TrackLanguage.HTML,
                        onClick = { language = TrackLanguage.HTML },
                        label = { Text("🌐 HTML") },
                    )
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = { onCreate(name, language) },
                enabled = name.trim().isNotEmpty(),
            ) {
                Text(stringResource(R.string.workspaces_create))
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text(stringResource(R.string.workspaces_cancel))
            }
        },
    )
}
