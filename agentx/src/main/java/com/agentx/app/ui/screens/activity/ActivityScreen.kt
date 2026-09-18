package com.agentx.app.ui.screens.activity

import androidx.compose.foundation.clickable
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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Block
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
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
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.agentx.app.data.local.entity.ActivityEntity
import com.agentx.app.ui.components.AxCard
import com.agentx.app.ui.components.AxEmptyState
import com.agentx.app.ui.components.AxTextButton
import com.agentx.app.util.FormatUtils

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ActivityScreen(viewModel: ActivityViewModel = hiltViewModel()) {
    val entries by viewModel.entries.collectAsStateWithLifecycle()
    var selected by remember { mutableStateOf<ActivityEntity?>(null) }

    Column(modifier = Modifier.fillMaxSize().statusBarsPadding()) {
        TopAppBar(
            title = { Text("Activity", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold) },
            actions = {
                if (entries.isNotEmpty()) {
                    IconButton(onClick = { viewModel.clear() }) {
                        Icon(Icons.Filled.Delete, contentDescription = "Clear log")
                    }
                }
            }
        )
        if (entries.isEmpty()) {
            AxEmptyState(
                icon = Icons.Filled.History,
                title = "Nothing yet",
                subtitle = "Every action AgentX takes is logged here with its confidence.",
                modifier = Modifier.fillMaxSize()
            )
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(entries, key = { it.id }) { entry ->
                    AxCard(modifier = Modifier.fillMaxWidth().clickable { selected = entry }) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                statusIcon(entry.status),
                                contentDescription = null,
                                tint = statusTint(entry.status),
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(Modifier.width(10.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(entry.label, style = MaterialTheme.typography.bodyMedium, maxLines = 2)
                                Text(
                                    FormatUtils.formatTimeAgo(entry.ts) +
                                        if (entry.confidence != null) " · " + (entry.confidence * 100).toInt() + "%" else "",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }
        }
    }

    selected?.let { entry ->
        AlertDialog(
            onDismissRequest = { selected = null },
            title = { Text(entry.label) },
            text = {
                Column {
                    Text("Status: " + entry.status, style = MaterialTheme.typography.bodySmall)
                    Text(FormatUtils.formatDateTime(entry.ts), style = MaterialTheme.typography.bodySmall)
                    if (entry.detailJson.isNotBlank()) {
                        Text("Detail: " + entry.detailJson, style = MaterialTheme.typography.bodySmall)
                    }
                }
            },
            confirmButton = { AxTextButton(text = "Close", onClick = { selected = null }) }
        )
    }
}

@Composable
private fun statusIcon(status: String): ImageVector = when (status) {
    "done" -> Icons.Filled.CheckCircle
    "failed" -> Icons.Filled.Error
    "denied" -> Icons.Filled.Block
    else -> Icons.Filled.Info
}

@Composable
private fun statusTint(status: String): androidx.compose.ui.graphics.Color = when (status) {
    "done" -> MaterialTheme.colorScheme.primary
    "failed" -> MaterialTheme.colorScheme.error
    "denied" -> MaterialTheme.colorScheme.tertiary
    else -> MaterialTheme.colorScheme.onSurfaceVariant
}
