package com.agentx.app.ui.screens.setup

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.outlined.CloudDownload
import androidx.compose.material.icons.outlined.OfflineBolt
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.ui.components.AxFilledButton
import com.agentx.app.ui.components.AxOutlinedButton
import com.agentx.app.util.FormatUtils

@Composable
fun SetupScreen(
    onReady: () -> Unit,
    viewModel: SetupViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(state) {
        if (state is AxModelState.Ready) onReady()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(28.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Surface(shape = CircleShape, color = MaterialTheme.colorScheme.primaryContainer, modifier = Modifier.size(76.dp)) {
            androidx.compose.foundation.layout.Box(contentAlignment = Alignment.Center) {
                Icon(Icons.Filled.Bolt, contentDescription = null, modifier = Modifier.size(38.dp), tint = MaterialTheme.colorScheme.onPrimaryContainer)
            }
        }
        Spacer(Modifier.height(20.dp))
        Text("Meet AgentX", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        Text(
            "A private AI that controls this phone. The brain downloads once, then everything runs on-device - no account, no cloud, no tracking.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(Modifier.height(20.dp))
        SetupFact(Icons.Outlined.CloudDownload, "35.3 MB one-time model download")
        SetupFact(Icons.Outlined.OfflineBolt, "Works fully offline after setup")
        SetupFact(Icons.Outlined.Shield, "Prompts never leave this device")
        Spacer(Modifier.height(22.dp))
        when (val current = state) {
            is AxModelState.Checking -> Text("Checking for a saved model…", style = MaterialTheme.typography.bodyMedium)
            is AxModelState.NotInstalled -> AxFilledButton(
                text = "Download and set up",
                onClick = { viewModel.download() },
                modifier = Modifier.fillMaxWidth()
            )
            is AxModelState.Downloading -> {
                LinearProgressIndicator(
                    progress = { (current.downloadedBytes.toFloat() / current.totalBytes.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f) },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                Text(
                    FormatUtils.formatBytes(current.downloadedBytes) + " of " + FormatUtils.formatBytes(current.totalBytes),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(Modifier.height(12.dp))
                AxOutlinedButton(text = "Cancel", onClick = { viewModel.cancel() })
            }
            is AxModelState.Verifying -> {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
                Spacer(Modifier.height(8.dp))
                Text("Verifying model integrity…", style = MaterialTheme.typography.bodySmall)
            }
            is AxModelState.Error -> {
                Text(current.message, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                Spacer(Modifier.height(12.dp))
                AxFilledButton(
                    text = if (current.resumableBytes > 0) "Resume download" else "Try again",
                    onClick = { viewModel.download() },
                    modifier = Modifier.fillMaxWidth()
                )
            }
            is AxModelState.Ready -> Text("Ready…", style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
private fun SetupFact(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    androidx.compose.foundation.layout.Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier.fillMaxWidth().padding(vertical = 5.dp)
    ) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
        Text(text, style = MaterialTheme.typography.bodySmall)
    }
}
