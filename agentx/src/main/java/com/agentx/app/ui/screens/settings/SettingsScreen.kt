package com.agentx.app.ui.screens.settings

import android.Manifest
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Memory
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.filled.Sms
import androidx.compose.material.icons.filled.Contacts
import androidx.compose.material.icons.filled.FlashlightOn
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.agentx.app.BuildConfig
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.ui.components.AxCard
import com.agentx.app.ui.components.AxFilledButton
import com.agentx.app.ui.components.AxInfoRow
import com.agentx.app.ui.components.AxOutlinedButton
import com.agentx.app.ui.components.AxSectionHeader
import com.agentx.app.ui.components.AxTextButton
import com.agentx.app.util.FormatUtils
import com.agentx.app.util.PermissionUtils

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onBack: () -> Unit,
    viewModel: SettingsViewModel = hiltViewModel()
) {
    val modelState by viewModel.modelState.collectAsStateWithLifecycle()
    val isDark by viewModel.isDarkMode.collectAsStateWithLifecycle()
    val threshold by viewModel.confirmThreshold.collectAsStateWithLifecycle()
    val confirmDestructive by viewModel.confirmDestructive.collectAsStateWithLifecycle()
    val context = LocalContext.current
    var showDeleteModel by remember { mutableStateOf(false) }
    var sliderValue by remember(threshold) { mutableStateOf(threshold) }

    var refreshTick by remember { mutableStateOf(0) }
    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { refreshTick++ }
    refreshTick.let { }

    Column(modifier = Modifier.fillMaxSize().statusBarsPadding()) {
        TopAppBar(
            title = { Text("Settings", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold) },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                }
            }
        )
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                AxSectionHeader(title = "On-device model")
                Spacer(Modifier.height(6.dp))
                AxCard(modifier = Modifier.fillMaxWidth()) {
                    ModelRow(
                        state = modelState,
                        onDownload = { viewModel.downloadModel() },
                        onDelete = { showDeleteModel = true },
                        onResetRuntime = { viewModel.resetRuntime() }
                    )
                }
            }
            item {
                AxSectionHeader(title = "Permissions")
                Spacer(Modifier.height(6.dp))
                AxCard(modifier = Modifier.fillMaxWidth()) {
                    PermRow(
                        icon = Icons.Filled.Notifications,
                        title = "Notifications",
                        refresh = refreshTick,
                        granted = { PermissionUtils.has(context, Manifest.permission.POST_NOTIFICATIONS) },
                        onGrant = { permissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS) }
                    )
                    PermRow(
                        icon = Icons.Filled.Phone,
                        title = "Phone calls",
                        refresh = refreshTick,
                        granted = { PermissionUtils.has(context, Manifest.permission.CALL_PHONE) },
                        onGrant = { permissionLauncher.launch(Manifest.permission.CALL_PHONE) }
                    )
                    PermRow(
                        icon = Icons.Filled.Sms,
                        title = "SMS messages",
                        refresh = refreshTick,
                        granted = { PermissionUtils.has(context, Manifest.permission.SEND_SMS) },
                        onGrant = { permissionLauncher.launch(Manifest.permission.SEND_SMS) }
                    )
                    PermRow(
                        icon = Icons.Filled.Contacts,
                        title = "Contacts",
                        refresh = refreshTick,
                        granted = { PermissionUtils.has(context, Manifest.permission.READ_CONTACTS) },
                        onGrant = { permissionLauncher.launch(Manifest.permission.READ_CONTACTS) }
                    )
                    PermRow(
                        icon = Icons.Filled.FlashlightOn,
                        title = "Camera (flashlight)",
                        refresh = refreshTick,
                        granted = { PermissionUtils.has(context, Manifest.permission.CAMERA) },
                        onGrant = { permissionLauncher.launch(Manifest.permission.CAMERA) }
                    )
                    AxInfoRow(
                        icon = Icons.Filled.Tune,
                        title = "Modify system settings",
                        subtitle = if (PermissionUtils.canWriteSettings(context)) "Granted" else "Needed for brightness, timeout, rotation",
                        trailing = {
                            if (!PermissionUtils.canWriteSettings(context)) {
                                AxTextButton(text = "Open", onClick = { PermissionUtils.openWriteSettings(context) })
                            }
                        }
                    )
                    AxInfoRow(
                        icon = Icons.Filled.Security,
                        title = "Do Not Disturb access",
                        subtitle = if (PermissionUtils.hasDndAccess(context)) "Granted" else "Needed for quiet hours",
                        trailing = {
                            if (!PermissionUtils.hasDndAccess(context)) {
                                AxTextButton(text = "Open", onClick = { PermissionUtils.openDndSettings(context) })
                            }
                        }
                    )
                }
            }
            item {
                AxSectionHeader(title = "Assistant")
                Spacer(Modifier.height(6.dp))
                AxCard(modifier = Modifier.fillMaxWidth()) {
                    Text("Ask me before acting below " + (sliderValue * 100).toInt() + "% confidence", style = MaterialTheme.typography.bodyMedium)
                    Slider(
                        value = sliderValue,
                        onValueChange = { sliderValue = it },
                        onValueChangeFinished = { viewModel.setConfirmThreshold(sliderValue) },
                        valueRange = 0.1f..0.69f
                    )
                    AxInfoRow(
                        icon = Icons.Filled.Security,
                        title = "Always confirm calls and texts",
                        trailing = {
                            Switch(checked = confirmDestructive, onCheckedChange = { viewModel.setConfirmDestructive(it) })
                        }
                    )
                }
            }
            item {
                AxSectionHeader(title = "Appearance")
                Spacer(Modifier.height(6.dp))
                AxCard(modifier = Modifier.fillMaxWidth()) {
                    AxInfoRow(
                        icon = Icons.Filled.DarkMode,
                        title = "Dark mode",
                        trailing = {
                            Switch(checked = isDark, onCheckedChange = { viewModel.setDarkMode(it) })
                        }
                    )
                }
            }
            item {
                AxSectionHeader(title = "Data")
                Spacer(Modifier.height(6.dp))
                AxCard(modifier = Modifier.fillMaxWidth()) {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        AxOutlinedButton(text = "Clear chat", onClick = { viewModel.clearChat() }, modifier = Modifier.weight(1f))
                        AxOutlinedButton(text = "Clear activity", onClick = { viewModel.clearActivity() }, modifier = Modifier.weight(1f))
                    }
                }
            }
            item {
                AxSectionHeader(title = "About")
                Spacer(Modifier.height(6.dp))
                AxCard(modifier = Modifier.fillMaxWidth()) {
                    AxInfoRow(
                        icon = Icons.Filled.SmartToy,
                        title = "AgentX " + BuildConfig.VERSION_NAME,
                        subtitle = "Needle 3 on-device AI · 121M params · tool calls, extraction and embeddings. No account, no cloud."
                    )
                    AxInfoRow(
                        icon = Icons.Filled.Memory,
                        title = "Fully offline",
                        subtitle = "After the one-time model download, every request is processed on this phone."
                    )
                }
                Spacer(Modifier.height(24.dp))
            }
        }
    }

    if (showDeleteModel) {
        AlertDialog(
            onDismissRequest = { showDeleteModel = false },
            title = { Text("Remove the model?") },
            text = { Text("This frees 35 MB. The assistant stops working until you download it again.") },
            confirmButton = {
                AxFilledButton(text = "Remove", onClick = { showDeleteModel = false; viewModel.deleteModel() })
            },
            dismissButton = { AxTextButton(text = "Cancel", onClick = { showDeleteModel = false }) }
        )
    }
}

@Composable
private fun ModelRow(
    state: AxModelState,
    onDownload: () -> Unit,
    onDelete: () -> Unit,
    onResetRuntime: () -> Unit
) {
    when (state) {
        is AxModelState.Ready -> {
            AxInfoRow(
                icon = Icons.Filled.SmartToy,
                title = "Needle 3 ready",
                subtitle = FormatUtils.formatBytes(state.sizeBytes) + " · verified on device"
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                AxOutlinedButton(text = "Reset runtime", onClick = onResetRuntime, modifier = Modifier.weight(1f))
                AxOutlinedButton(text = "Remove", onClick = onDelete, modifier = Modifier.weight(1f))
            }
        }
        is AxModelState.Downloading -> {
            Text("Downloading… " + FormatUtils.formatBytes(state.downloadedBytes), style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.height(8.dp))
            LinearProgressIndicator(
                progress = { (state.downloadedBytes.toFloat() / state.totalBytes.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f) },
                modifier = Modifier.fillMaxWidth()
            )
        }
        is AxModelState.Verifying -> {
            Text("Verifying integrity…", style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.height(8.dp))
            LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
        }
        is AxModelState.Error -> {
            Text(state.message, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.error)
            Spacer(Modifier.height(8.dp))
            AxFilledButton(text = if (state.resumableBytes > 0) "Resume" else "Retry", onClick = onDownload, modifier = Modifier.fillMaxWidth())
        }
        else -> {
            Text("The 35 MB model is not installed.", style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.height(8.dp))
            AxFilledButton(
                text = "Download",
                onClick = onDownload,
                leadingIcon = Icons.Filled.Download,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
private fun PermRow(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    refresh: Int,
    granted: () -> Boolean,
    onGrant: () -> Unit
) {
    refresh.let { }
    val ok = remember(refresh) { granted() }
    AxInfoRow(
        icon = icon,
        title = title,
        subtitle = if (ok) "Granted" else "Not granted",
        trailing = {
            if (!ok) {
                AxTextButton(text = "Grant", onClick = onGrant)
            }
        }
    )
}
