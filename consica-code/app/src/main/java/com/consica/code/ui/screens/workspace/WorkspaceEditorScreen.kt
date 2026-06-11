package com.consica.code.ui.screens.workspace

import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.ui.playground.CodeEditor
import com.consica.code.ui.playground.CodeKeyboard
import com.consica.code.ui.playground.HtmlPreview
import com.consica.code.ui.theme.CodeTextStyle
import com.consica.code.ui.theme.EditorBackground
import com.consica.code.ui.theme.EditorText

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WorkspaceEditorScreen(
    onBack: () -> Unit,
    viewModel: WorkspaceEditorViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()
    val code by viewModel.code.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }
    var showAddFile by remember { mutableStateOf(false) }

    val savedMessage = stringResource(R.string.workspace_saved)
    LaunchedEffect(state.justSaved) {
        if (state.justSaved) {
            snackbarHostState.showSnackbar(savedMessage)
            viewModel.dismissSaved()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        state.workspace?.name ?: "",
                        style = MaterialTheme.typography.titleLarge,
                        maxLines = 1,
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
                actions = {
                    IconButton(onClick = viewModel::save) {
                        Icon(Icons.Default.Save, contentDescription = stringResource(R.string.workspace_save))
                    }
                    IconButton(onClick = viewModel::run, enabled = !state.running) {
                        Icon(
                            Icons.Default.PlayArrow,
                            contentDescription = stringResource(R.string.playground_run),
                            tint = MaterialTheme.colorScheme.primary,
                        )
                    }
                },
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
    ) { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
        ) {
            if (state.files.size > 1 || state.language == TrackLanguage.HTML) {
                Row(
                    Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    state.files.forEach { file ->
                        FilterChip(
                            selected = file.id == state.selectedFileId,
                            onClick = { viewModel.selectFile(file.id) },
                            label = { Text(file.name, style = MaterialTheme.typography.labelLarge) },
                        )
                    }
                    IconButton(onClick = { showAddFile = true }) {
                        Icon(Icons.Default.Add, contentDescription = stringResource(R.string.workspace_add_file))
                    }
                }
                Spacer(Modifier.height(6.dp))
            }

            CodeEditor(
                value = code,
                onValueChange = viewModel::onCodeChange,
                language = state.language,
                showLineNumbers = state.proEditor,
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
            )

            if (state.ageGroup == AgeGroup.KIDS || !state.proEditor) {
                Spacer(Modifier.height(6.dp))
                CodeKeyboard(language = state.language, onKey = viewModel::onCodeKey)
            }

            if (state.hasRun) {
                Spacer(Modifier.height(8.dp))
                Text(
                    text = stringResource(
                        if (state.language == TrackLanguage.HTML) R.string.playground_preview
                        else R.string.playground_console
                    ),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.height(4.dp))
                Box(
                    Modifier
                        .fillMaxWidth()
                        .weight(0.8f),
                ) {
                    when {
                        state.error != null -> {
                            Column(
                                Modifier
                                    .fillMaxSize()
                                    .clip(RoundedCornerShape(16.dp))
                                    .background(MaterialTheme.colorScheme.errorContainer)
                                    .padding(12.dp)
                                    .verticalScroll(rememberScrollState()),
                            ) {
                                Text(
                                    stringResource(R.string.playground_error_title),
                                    style = MaterialTheme.typography.titleSmall,
                                    color = MaterialTheme.colorScheme.onErrorContainer,
                                )
                                state.error?.line?.let { line ->
                                    Text(
                                        stringResource(R.string.playground_error_line, line),
                                        style = MaterialTheme.typography.labelMedium,
                                        color = MaterialTheme.colorScheme.onErrorContainer,
                                    )
                                }
                                Spacer(Modifier.height(4.dp))
                                Text(
                                    state.error?.message.orEmpty(),
                                    style = CodeTextStyle,
                                    color = MaterialTheme.colorScheme.onErrorContainer,
                                )
                            }
                        }
                        state.language == TrackLanguage.HTML -> {
                            HtmlPreview(
                                html = state.output,
                                modifier = Modifier
                                    .fillMaxSize()
                                    .clip(RoundedCornerShape(16.dp)),
                            )
                        }
                        else -> {
                            Box(
                                Modifier
                                    .fillMaxSize()
                                    .clip(RoundedCornerShape(16.dp))
                                    .background(EditorBackground)
                                    .padding(12.dp),
                            ) {
                                Text(
                                    text = state.output.ifEmpty {
                                        stringResource(R.string.playground_empty_output)
                                    },
                                    style = CodeTextStyle,
                                    color = EditorText,
                                    modifier = Modifier.verticalScroll(rememberScrollState()),
                                )
                            }
                        }
                    }
                }
            }
            Spacer(Modifier.height(16.dp))
        }
    }

    if (showAddFile) {
        AddFileDialog(
            onDismiss = { showAddFile = false },
            onAdd = { name ->
                showAddFile = false
                viewModel.addFile(name)
            },
        )
    }
}

@Composable
private fun AddFileDialog(onDismiss: () -> Unit, onAdd: (String) -> Unit) {
    var name by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(stringResource(R.string.workspace_add_file)) },
        text = {
            OutlinedTextField(
                value = name,
                onValueChange = { name = it.take(60) },
                label = { Text(stringResource(R.string.workspace_file_name_hint)) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
            )
        },
        confirmButton = {
            TextButton(onClick = { onAdd(name) }, enabled = name.trim().isNotEmpty()) {
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
