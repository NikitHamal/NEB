package com.agentx.app.ui.screens.routines

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.filled.Schedule
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
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
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.agentx.app.data.local.entity.RoutineEntity
import com.agentx.app.ui.components.AxCard
import com.agentx.app.ui.components.AxChip
import com.agentx.app.ui.components.AxEmptyState
import com.agentx.app.ui.components.AxFilledButton
import com.agentx.app.ui.components.AxOutlinedButton
import com.agentx.app.ui.components.AxTextButton

private val dayLabels = listOf("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RoutinesScreen(viewModel: RoutinesViewModel = hiltViewModel()) {
    val routines by viewModel.routines.collectAsStateWithLifecycle()
    val busy by viewModel.busy.collectAsStateWithLifecycle()
    val draft by viewModel.draft.collectAsStateWithLifecycle()
    val snackbar = remember { SnackbarHostState() }
    var showCreate by remember { mutableStateOf(false) }
    var scheduleFor by remember { mutableStateOf<RoutineEntity?>(null) }

    LaunchedEffect(Unit) {
        viewModel.message.collect { snackbar.showSnackbar(it) }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbar) },
        topBar = {
            TopAppBar(
                title = { Text("Routines", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold) },
                modifier = Modifier.statusBarsPadding()
            )
        },
        floatingActionButton = {
            androidx.compose.material3.FloatingActionButton(onClick = { showCreate = true }) {
                Icon(Icons.Filled.Add, contentDescription = "New routine")
            }
        }
    ) { padding ->
        if (routines.isEmpty()) {
            AxEmptyState(
                icon = Icons.Filled.Repeat,
                title = "No routines yet",
                subtitle = "Describe one in plain words - AgentX turns it into steps that run on-device.",
                modifier = Modifier.padding(padding).fillMaxSize(),
                action = { AxFilledButton(text = "Create a routine", onClick = { showCreate = true }) }
            )
        } else {
            LazyColumn(
                modifier = Modifier.padding(padding).fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(routines, key = { it.id }) { routine ->
                    RoutineCard(
                        routine = routine,
                        busy = busy,
                        stepCount = null,
                        onRun = { viewModel.run(routine.id) },
                        onSchedule = { scheduleFor = routine },
                        onDelete = { viewModel.delete(routine) }
                    )
                }
            }
        }
    }

    if (showCreate) {
        CreateRoutineDialog(
            busy = busy,
            draft = draft,
            stepTitle = { viewModel.stepTitle(it) },
            onGenerate = { name, description -> viewModel.generateDraft(name, description) },
            onSave = { hour, minute, days -> viewModel.saveDraft(hour, minute, days) },
            onDismiss = {
                showCreate = false
                viewModel.clearDraft()
            }
        )
    }

    scheduleFor?.let { routine ->
        ScheduleDialog(
            routine = routine,
            onSave = { hour, minute, days -> viewModel.saveSchedule(routine, hour, minute, days) },
            onClear = { viewModel.clearSchedule(routine) },
            onDismiss = { scheduleFor = null }
        )
    }
}

@Composable
private fun RoutineCard(
    routine: RoutineEntity,
    busy: Boolean,
    stepCount: Int?,
    onRun: () -> Unit,
    onSchedule: () -> Unit,
    onDelete: () -> Unit
) {
    AxCard(modifier = Modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Column(modifier = Modifier.weight(1f)) {
                Text(routine.name, style = MaterialTheme.typography.titleMedium)
                Spacer(Modifier.height(2.dp))
                Text(
                    scheduleText(routine) + if (stepCount != null) " · " + stepCount + " steps" else "",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            IconButton(onClick = onRun, enabled = !busy) {
                Icon(Icons.Filled.PlayArrow, contentDescription = "Run", tint = MaterialTheme.colorScheme.primary)
            }
            IconButton(onClick = onSchedule) {
                Icon(Icons.Filled.Schedule, contentDescription = "Schedule", tint = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Filled.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
            }
        }
    }
}

private fun scheduleText(routine: RoutineEntity): String {
    if (routine.scheduleHour < 0) return "Manual"
    val time = routine.scheduleHour.toString().padStart(2, '0') + ":" + routine.scheduleMinute.toString().padStart(2, '0')
    if (routine.scheduleDays == 0) return "Daily " + time
    val days = dayLabels.filterIndexed { index, _ -> (routine.scheduleDays and (1 shl index)) != 0 }
    return days.joinToString(" ") + " " + time
}

@Composable
private fun CreateRoutineDialog(
    busy: Boolean,
    draft: RoutinesViewModel.Draft?,
    stepTitle: (com.agentx.app.data.engine.ToolCallSpec) -> String,
    onGenerate: (String, String) -> Unit,
    onSave: (Int, Int, Int) -> Unit,
    onDismiss: () -> Unit
) {
    var name by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var hour by remember { mutableStateOf("") }
    var minute by remember { mutableStateOf("") }
    var days by remember { mutableStateOf(0) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New routine") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                if (draft == null) {
                    OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("Name, e.g. Bedtime") }, singleLine = true, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(
                        value = description,
                        onValueChange = { description = it },
                        label = { Text("Describe it in words") },
                        placeholder = { Text("Enable Do Not Disturb and dim to 10 percent") },
                        minLines = 2,
                        modifier = Modifier.fillMaxWidth()
                    )
                    if (busy) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                            Spacer(Modifier.width(8.dp))
                            Text("Turning words into steps…", style = MaterialTheme.typography.bodySmall)
                        }
                    }
                } else {
                    Text(draft.name, style = MaterialTheme.typography.titleMedium)
                    draft.steps.forEachIndexed { index, step ->
                        Text((index + 1).toString() + ". " + stepTitle(step), style = MaterialTheme.typography.bodySmall)
                    }
                    Spacer(Modifier.height(4.dp))
                    Text("Run daily at (optional)", style = MaterialTheme.typography.labelMedium)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = hour,
                            onValueChange = { hour = it.filter { ch -> ch.isDigit() }.take(2) },
                            label = { Text("HH") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            singleLine = true,
                            modifier = Modifier.weight(1f)
                        )
                        OutlinedTextField(
                            value = minute,
                            onValueChange = { minute = it.filter { ch -> ch.isDigit() }.take(2) },
                            label = { Text("MM") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            singleLine = true,
                            modifier = Modifier.weight(1f)
                        )
                    }
                    androidx.compose.foundation.lazy.LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        items(dayLabels.size) { index ->
                            val selected = (days and (1 shl index)) != 0
                            AxChip(
                                label = dayLabels[index],
                                selected = selected,
                                onClick = { days = days xor (1 shl index) }
                            )
                        }
                    }
                }
            }
        },
        confirmButton = {
            if (draft == null) {
                AxFilledButton(
                    text = "Generate steps",
                    onClick = { onGenerate(name, description) },
                    enabled = !busy && name.isNotBlank() && description.isNotBlank()
                )
            } else {
                AxFilledButton(
                    text = "Save routine",
                    onClick = {
                        val h = hour.toIntOrNull() ?: -1
                        val m = minute.toIntOrNull() ?: 0
                        if (h in 0..23 && m in 0..59) onSave(h, m, days) else onSave(-1, 0, 0)
                        onDismiss()
                    }
                )
            }
        },
        dismissButton = { AxTextButton(text = "Cancel", onClick = onDismiss) }
    )
}

@Composable
private fun ScheduleDialog(
    routine: RoutineEntity,
    onSave: (Int, Int, Int) -> Unit,
    onClear: () -> Unit,
    onDismiss: () -> Unit
) {
    var hour by remember { mutableStateOf(if (routine.scheduleHour >= 0) routine.scheduleHour.toString() else "") }
    var minute by remember { mutableStateOf(if (routine.scheduleHour >= 0) routine.scheduleMinute.toString().padStart(2, '0') else "") }
    var days by remember { mutableStateOf(routine.scheduleDays) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Schedule " + routine.name) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = hour,
                        onValueChange = { hour = it.filter { ch -> ch.isDigit() }.take(2) },
                        label = { Text("HH") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                    OutlinedTextField(
                        value = minute,
                        onValueChange = { minute = it.filter { ch -> ch.isDigit() }.take(2) },
                        label = { Text("MM") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                }
                androidx.compose.foundation.lazy.LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    items(dayLabels.size) { index ->
                        val selected = (days and (1 shl index)) != 0
                        AxChip(
                            label = dayLabels[index],
                            selected = selected,
                            onClick = { days = days xor (1 shl index) }
                        )
                    }
                }
                Text("No days ticked means every day.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        },
        confirmButton = {
            AxFilledButton(
                text = "Save",
                onClick = {
                    val h = hour.toIntOrNull()
                    val m = minute.toIntOrNull()
                    if (h != null && m != null && h in 0..23 && m in 0..59) {
                        onSave(h, m, days)
                        onDismiss()
                    }
                }
            )
        },
        dismissButton = {
            Row {
                AxTextButton(text = "Clear", onClick = { onClear(); onDismiss() })
                AxTextButton(text = "Cancel", onClick = onDismiss)
            }
        }
    )
}
