package com.agentx.app.ui.screens.assistant

import android.Manifest
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.agentx.app.data.engine.AxMessage
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.data.engine.NeedleRuntimeState
import com.agentx.app.data.tools.ToolCatalog
import com.agentx.app.ui.components.AxCard
import com.agentx.app.ui.components.AxChip
import com.agentx.app.ui.components.AxEmptyState
import com.agentx.app.ui.components.AxFilledButton
import com.agentx.app.ui.components.ConfirmActionSheet
import com.agentx.app.ui.components.EngineStatusPill
import com.agentx.app.ui.components.EngineUiState

private val suggestions = listOf(
    "Dim the screen to 20%",
    "Set an alarm for 7 AM",
    "Remind me to drink water in 20 minutes",
    "What apps can you open?",
    "Show device status"
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AssistantScreen(
    prefill: String,
    onOpenSettings: () -> Unit,
    onNeedSetup: () -> Unit,
    viewModel: AssistantViewModel = hiltViewModel()
) {
    val messages by viewModel.messages.collectAsStateWithLifecycle()
    val running by viewModel.running.collectAsStateWithLifecycle()
    val pendingConfirm by viewModel.pendingConfirm.collectAsStateWithLifecycle()
    val modelState by viewModel.modelState.collectAsStateWithLifecycle()
    val runtimeState by viewModel.runtimeState.collectAsStateWithLifecycle()
    var input by remember { mutableStateOf("") }
    val listState = rememberLazyListState()

    LaunchedEffect(prefill) {
        if (prefill.isNotBlank()) input = prefill
    }
    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) listState.animateScrollToItem(messages.size - 1)
    }

    var lastAskedPermission by remember { mutableStateOf<String?>(null) }
    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        lastAskedPermission?.let { viewModel.onPermissionResult(it, granted) }
    }
    LaunchedEffect(Unit) {
        viewModel.permissionAsk.collect { permission ->
            lastAskedPermission = permission
            permissionLauncher.launch(permission)
        }
    }

    val engineUiState = when {
        modelState !is AxModelState.Ready -> EngineUiState.MISSING
        runtimeState is NeedleRuntimeState.Ready -> EngineUiState.READY
        runtimeState is NeedleRuntimeState.Error -> EngineUiState.ERROR
        else -> EngineUiState.LOADING
    }

    Column(modifier = Modifier.fillMaxSize().statusBarsPadding()) {
        TopAppBar(
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Filled.Bolt, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(8.dp))
                    Text("AgentX", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                }
            },
            actions = {
                EngineStatusPill(engineUiState, modifier = Modifier.padding(end = 4.dp))
                IconButton(onClick = onOpenSettings) {
                    Icon(Icons.Filled.Settings, contentDescription = "Settings")
                }
            }
        )

        if (modelState !is AxModelState.Ready && modelState !is AxModelState.Checking) {
            AxCard(modifier = Modifier.padding(horizontal = 16.dp)) {
                Text("The on-device model is not installed.", style = MaterialTheme.typography.bodyMedium)
                Spacer(Modifier.height(8.dp))
                AxFilledButton(text = "Set up the model", onClick = onNeedSetup)
            }
            Spacer(Modifier.height(8.dp))
        }

        if (messages.isEmpty()) {
            AxEmptyState(
                icon = Icons.Filled.SmartToy,
                title = "What should I do?",
                subtitle = "I control this phone directly - brightness, volume, apps, calls, alarms, reminders, notes and routines. All offline.",
                modifier = Modifier.weight(1f)
            )
        } else {
            LazyColumn(
                state = listState,
                modifier = Modifier.weight(1f),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(messages, key = { it.id }) { message ->
                    if (message.isUser) UserBubble(message) else AgentCard(message, onOption = { viewModel.send(it) })
                }
            }
        }

        if (messages.isEmpty()) {
            androidx.compose.foundation.lazy.LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(suggestions.size) { index ->
                    AxChip(label = suggestions[index], selected = false, onClick = { viewModel.send(suggestions[index]) })
                }
            }
            Spacer(Modifier.height(8.dp))
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp)
                .navigationBarsPadding()
                .imePadding()
                .padding(bottom = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text(if (running) "Working…" else "Ask AgentX…") },
                singleLine = false,
                maxLines = 4,
                shape = MaterialTheme.shapes.extraLarge,
                enabled = !running
            )
            Spacer(Modifier.width(8.dp))
            androidx.compose.material3.FilledIconButton(
                onClick = {
                    viewModel.send(input)
                    input = ""
                },
                enabled = !running && input.isNotBlank()
            ) {
                Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send")
            }
        }
    }

    pendingConfirm?.let { pending ->
        val meta = ToolCatalog.metas[pending.spec.name]
        ConfirmActionSheet(
            title = meta?.title ?: pending.spec.name,
            description = describeSpec(pending.spec.name, pending.spec.args),
            detailLines = pending.spec.args.entries.map { (key, value) -> key + ": " + value },
            confidence = pending.confidence,
            onConfirm = { viewModel.confirmPending() },
            onDismiss = { viewModel.dismissPending() }
        )
    }
}

@Composable
private fun UserBubble(message: AxMessage) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
        Surface(
            shape = MaterialTheme.shapes.large,
            color = MaterialTheme.colorScheme.primaryContainer
        ) {
            Text(
                message.text,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp)
            )
        }
    }
}

@Composable
private fun AgentCard(message: AxMessage, onOption: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    AxCard(modifier = Modifier.fillMaxWidth()) {
        Text(message.text, style = MaterialTheme.typography.bodyMedium)
        if (message.toolCalls.isNotEmpty()) {
            Spacer(Modifier.height(8.dp))
            message.toolCalls.forEach { call ->
                val meta = ToolCatalog.metas[call.name]
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Filled.Bolt, contentDescription = null, modifier = Modifier.size(14.dp), tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(6.dp))
                    Text(
                        (meta?.title ?: call.name) + if (message.confidence != null) " · " + (message.confidence * 100).toInt() + "%" else "",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
        if (!message.reasoning.isNullOrBlank()) {
            Spacer(Modifier.height(4.dp))
            Row(
                modifier = Modifier.clickable { expanded = !expanded },
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    if (expanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore,
                    contentDescription = null,
                    modifier = Modifier.size(16.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text("Why this action", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            if (expanded) {
                Text(message.reasoning, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        if (message.options.isNotEmpty()) {
            Spacer(Modifier.height(8.dp))
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                message.options.forEach { option ->
                    AxChip(label = optionLabel(option), selected = false, onClick = { onOption(option) })
                }
            }
        }
    }
}

private fun optionLabel(option: String): String = when {
    option == "action:retry" -> "Retry"
    option == "action:force_run" -> "Run it anyway"
    option.startsWith("action:open_settings:") -> "Open settings"
    else -> option
}

private fun describeSpec(name: String, args: Map<String, String>): String {
    return when (name) {
        "place_call" -> "Call " + (args["target"] ?: "this contact") + " now."
        "send_message" -> "Send an SMS to " + (args["target"] ?: "this contact") + "."
        else -> "Run " + (ToolCatalog.metas[name]?.title ?: name) + " with these arguments."
    }
}
