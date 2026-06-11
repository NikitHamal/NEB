package com.consica.code.ui.screens.workspaces

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.CodeLanguage
import com.consica.code.core.model.TerraExpression
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.common.EcoCard
import com.consica.code.ui.common.appViewModel
import com.consica.code.util.TimeFormat
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class WorkspacesUiState(
    val user: UserState = UserState(),
    val workspaces: List<WorkspaceEntity> = emptyList(),
    val loaded: Boolean = false,
)

data class WorkspaceTemplate(
    val nameRes: Int,
    val language: CodeLanguage,
    val code: String,
)

val workspaceTemplates = listOf(
    WorkspaceTemplate(R.string.workspaces_template_blank_py, CodeLanguage.PYTHON, "# New Python playground\n"),
    WorkspaceTemplate(R.string.workspaces_template_blank_html, CodeLanguage.HTML, "<h1>My Page</h1>\n"),
    WorkspaceTemplate(
        R.string.workspaces_template_story,
        CodeLanguage.PYTHON,
        "hero = \"Aarav\"\nplace = \"Pokhara\"\nprint(hero + \" begins an adventure in \" + place + \"!\")\n",
    ),
    WorkspaceTemplate(
        R.string.workspaces_template_portfolio,
        CodeLanguage.HTML,
        "<style>\n  body { font-family: sans-serif; }\n  h1 { color: green; }\n</style>\n<h1>My Portfolio</h1>\n<p>Projects I have grown:</p>\n<ul>\n  <li>My first web page</li>\n  <li>Python rain counter</li>\n</ul>\n",
    ),
    WorkspaceTemplate(
        R.string.workspaces_template_quiz,
        CodeLanguage.PYTHON,
        "score = 0\nanswer = \"kathmandu\"\nguess = \"kathmandu\"\nif guess == answer:\n    score = score + 1\n    print(\"Correct!\")\nprint(\"Score:\", score)\n",
    ),
)

class WorkspacesViewModel(private val container: AppContainer) : ViewModel() {

    val state: StateFlow<WorkspacesUiState> = combine(
        container.prefs.userState,
        container.workspaces.all,
    ) { user, list ->
        WorkspacesUiState(user, list, loaded = true)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), WorkspacesUiState())

    fun create(name: String, template: WorkspaceTemplate, onCreated: (Long) -> Unit) {
        viewModelScope.launch {
            val id = container.workspaces.create(name, template.language, template.code)
            onCreated(id)
        }
    }

    fun delete(id: Long) {
        viewModelScope.launch { container.workspaces.delete(id) }
    }
}

@Composable
fun WorkspacesScreen(onOpenWorkspace: (Long) -> Unit) {
    val viewModel = appViewModel { WorkspacesViewModel(it) }
    val state by viewModel.state.collectAsState()
    val user = state.user

    var showNewMenu by remember { mutableStateOf(false) }
    var deleteTarget by remember { mutableStateOf<WorkspaceEntity?>(null) }

    if (state.loaded && !user.proToolsUnlocked) {
        LockedView()
        return
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                stringResource(R.string.workspaces_title),
                style = MaterialTheme.typography.headlineSmall,
                modifier = Modifier.weight(1f),
            )
            Box {
                Button(onClick = { showNewMenu = true }, shape = PillShape) {
                    Icon(Icons.Filled.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                    Box(Modifier.width(6.dp))
                    Text(stringResource(R.string.workspaces_new))
                }
                DropdownMenu(expanded = showNewMenu, onDismissRequest = { showNewMenu = false }) {
                    workspaceTemplates.forEach { template ->
                        val label = stringResource(template.nameRes)
                        DropdownMenuItem(
                            text = { Text(label) },
                            onClick = {
                                showNewMenu = false
                                viewModel.create(label, template) { id -> onOpenWorkspace(id) }
                            },
                        )
                    }
                }
            }
        }

        if (state.loaded && state.workspaces.isEmpty()) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                TerraAvatar(expression = TerraExpression.THINKING, size = 96.dp)
                Box(Modifier.height(16.dp))
                Text(stringResource(R.string.workspaces_empty_title), style = MaterialTheme.typography.titleLarge)
                Text(
                    stringResource(R.string.workspaces_empty_body),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = androidx.compose.foundation.layout.PaddingValues(
                    start = 16.dp, end = 16.dp, bottom = 32.dp,
                ),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(state.workspaces, key = { it.id }) { ws ->
                    EcoCard(modifier = Modifier.fillMaxWidth()) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Icon(
                                Icons.Filled.Code,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.primary,
                            )
                            Box(Modifier.width(12.dp))
                            Column(
                                modifier = Modifier
                                    .weight(1f)
                                    .padding(end = 8.dp),
                            ) {
                                Text(
                                    ws.name,
                                    style = MaterialTheme.typography.titleSmall,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis,
                                )
                                Text(
                                    text = ws.language + "  ·  " +
                                        stringResource(
                                            if (ws.isFreePlay) R.string.workspaces_free_play
                                            else R.string.workspaces_lesson_linked,
                                        ) + "  ·  " +
                                        stringResource(
                                            R.string.workspaces_updated_at,
                                            TimeFormat.relative(ws.updatedAt),
                                        ),
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis,
                                )
                            }
                            TextButton(onClick = { onOpenWorkspace(ws.id) }) {
                                Text(stringResource(R.string.action_open))
                            }
                            IconButton(onClick = { deleteTarget = ws }) {
                                Icon(
                                    Icons.Filled.Delete,
                                    contentDescription = stringResource(R.string.action_delete),
                                    tint = MaterialTheme.colorScheme.error,
                                )
                            }
                        }
                    }
                }
            }
        }
    }

    val target = deleteTarget
    if (target != null) {
        AlertDialog(
            onDismissRequest = { deleteTarget = null },
            title = { Text(stringResource(R.string.action_delete)) },
            text = { Text(stringResource(R.string.workspaces_delete_confirm)) },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.delete(target.id)
                        deleteTarget = null
                    },
                ) { Text(stringResource(R.string.action_delete)) }
            },
            dismissButton = {
                TextButton(onClick = { deleteTarget = null }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
        )
    }
}

@Composable
private fun LockedView() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(
            Icons.Filled.Lock,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.outline,
            modifier = Modifier.size(48.dp),
        )
        Box(Modifier.height(16.dp))
        Text(
            stringResource(R.string.workspaces_locked_title),
            style = MaterialTheme.typography.titleLarge,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
        )
        Box(Modifier.height(8.dp))
        Text(
            stringResource(R.string.workspaces_locked_body),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
        )
    }
}
