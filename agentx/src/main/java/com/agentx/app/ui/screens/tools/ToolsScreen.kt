package com.agentx.app.ui.screens.tools

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Alarm
import androidx.compose.material.icons.filled.Apps
import androidx.compose.material.icons.filled.Call
import androidx.compose.material.icons.filled.EventNote
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.agentx.app.data.tools.ToolCatalog
import com.agentx.app.data.tools.ToolMeta
import com.agentx.app.ui.components.AxCard
import com.agentx.app.ui.components.AxSectionHeader
import com.agentx.app.ui.components.AxTextButton

private fun groupIcon(group: String): ImageVector = when (group) {
    "Display and sound" -> Icons.Filled.Tune
    "Apps" -> Icons.Filled.Apps
    "Calls and messages" -> Icons.Filled.Call
    "Time" -> Icons.Filled.Alarm
    "Reminders and notes" -> Icons.Filled.EventNote
    "Routines" -> Icons.Filled.Repeat
    else -> Icons.Filled.Settings
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ToolsScreen(
    onTryInAssistant: (String) -> Unit,
    viewModel: ToolsViewModel = hiltViewModel()
) {
    val snackbar = remember { SnackbarHostState() }
    var resultText by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        viewModel.result.collect { resultText = it }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbar) },
        topBar = {
            TopAppBar(
                title = { Text("Device tools", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold) },
                modifier = Modifier.statusBarsPadding()
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.padding(padding).fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            ToolCatalog.groups.forEach { group ->
                item(key = "header-" + group) {
                    AxSectionHeader(title = group)
                }
                items(viewModel.metasFor(group), key = { it.name }) { meta ->
                    ToolRow(
                        meta = meta,
                        group = group,
                        permState = viewModel.permissionState(meta),
                        direct = viewModel.isDirect(meta),
                        onRunDirect = { viewModel.runDirect(meta.name) },
                        onTry = { onTryInAssistant(viewModel.samplePrompt(meta.name)) }
                    )
                }
            }
        }
    }

    resultText?.let { text ->
        AlertDialog(
            onDismissRequest = { resultText = null },
            title = { Text("Result") },
            text = { Text(text) },
            confirmButton = { AxTextButton(text = "Close", onClick = { resultText = null }) }
        )
    }
}

@Composable
private fun ToolRow(
    meta: ToolMeta,
    group: String,
    permState: ToolsViewModel.PermState,
    direct: Boolean,
    onRunDirect: () -> Unit,
    onTry: () -> Unit
) {
    AxCard(modifier = Modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(groupIcon(group), contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(22.dp))
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(meta.title, style = MaterialTheme.typography.bodyLarge)
                    if (permState != ToolsViewModel.PermState.NONE) {
                        Spacer(Modifier.width(6.dp))
                        Surface(
                            shape = CircleShape,
                            color = when (permState) {
                                ToolsViewModel.PermState.GRANTED -> MaterialTheme.colorScheme.primaryContainer
                                else -> MaterialTheme.colorScheme.errorContainer
                            },
                            modifier = Modifier.size(8.dp)
                        ) {}
                    }
                }
                Text(
                    meta.description + (if (meta.permissionLabel != null) " · needs " + meta.permissionLabel else ""),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Spacer(Modifier.width(8.dp))
            Column(horizontalAlignment = Alignment.End) {
                AxTextButton(text = if (direct) "Run" else "Try", onClick = if (direct) onRunDirect else onTry)
                if (!direct) {
                    Icon(Icons.Filled.PlayArrow, contentDescription = null, modifier = Modifier.size(14.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}
