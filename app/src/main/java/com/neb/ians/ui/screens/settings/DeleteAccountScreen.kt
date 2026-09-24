package com.neb.ians.ui.screens.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebLoader

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DeleteAccountScreen(
    viewModel: SettingsViewModel,
    onNavigateBack: () -> Unit
) {
    val deletionState by viewModel.deletionRequestState.collectAsStateWithLifecycle()
    var reason by remember { mutableStateOf("") }
    var confirmed by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        viewModel.fetchDeletionRequestStatus()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Delete Account", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                }
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when (val state = deletionState) {
                is DeletionRequestUiState.Loading -> {
                    NebLoader(modifier = Modifier.align(Alignment.Center))
                }
                is DeletionRequestUiState.Error -> {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = state.message,
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodyLarge,
                            modifier = Modifier.padding(bottom = 16.dp)
                        )
                        NebButton(
                            text = "Retry",
                            onClick = { viewModel.fetchDeletionRequestStatus() }
                        )
                    }
                }
                is DeletionRequestUiState.Loaded -> {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .verticalScroll(rememberScrollState())
                            .padding(24.dp)
                    ) {
                        if (state.hasPending && state.request != null) {
                            val formattedDate = remember(state.request.scheduledDeleteAt) {
                                try {
                                    val sdf = SimpleDateFormat("MMMM dd, yyyy", Locale.getDefault())
                                    sdf.format(Date(state.request.scheduledDeleteAt))
                                } catch (e: Exception) {
                                    "30 days"
                                }
                            }

                            Card(
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.errorContainer,
                                    contentColor = MaterialTheme.colorScheme.onErrorContainer
                                ),
                                shape = RoundedCornerShape(16.dp),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(bottom = 24.dp)
                            ) {
                                Column(
                                    modifier = Modifier.padding(16.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        modifier = Modifier.padding(bottom = 8.dp)
                                    ) {
                                        Icon(
                                            imageVector = Icons.Default.Warning,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.error
                                        )
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text(
                                            text = "Deletion Scheduled",
                                            style = MaterialTheme.typography.titleMedium,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                    Text(
                                        text = "Your account is scheduled for permanent deletion on $formattedDate.",
                                        style = MaterialTheme.typography.bodyMedium,
                                        modifier = Modifier.padding(bottom = 16.dp)
                                    )
                                    NebButton(
                                        text = "Cancel deletion request",
                                        onClick = { viewModel.cancelAccountDeletion() },
                                        tone = NebButtonTone.Danger,
                                        fillWidth = true
                                    )
                                }
                            }
                        } else {
                            Text(
                                text = "Important Information",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.error,
                                modifier = Modifier.padding(bottom = 12.dp)
                            )

                            Text(
                                text = "Before requesting deletion, please review what happens to your data:",
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )

                            Card(
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                                ),
                                shape = RoundedCornerShape(12.dp),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(bottom = 24.dp)
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    BulletItem("Your profile, posts, comments, replies, bookmarks, and follows will be permanently erased.")
                                    Spacer(modifier = Modifier.height(8.dp))
                                    BulletItem("Your contributed study resources will remain in the library but authorship will show as 'Anonymous'.")
                                    Spacer(modifier = Modifier.height(8.dp))
                                    BulletItem("Deletions are processed after a 30-day grace period. You can cancel this request at any time before then.")
                                }
                            }

                            OutlinedTextField(
                                value = reason,
                                onValueChange = { reason = it },
                                label = { Text("Why are you requesting deletion? (Optional)") },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(bottom = 24.dp),
                                shape = RoundedCornerShape(12.dp),
                                maxLines = 4
                            )

                            Row(
                                verticalAlignment = Alignment.Top,
                                modifier = Modifier.padding(bottom = 24.dp)
                            ) {
                                Checkbox(
                                    checked = confirmed,
                                    onCheckedChange = { confirmed = it }
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    text = "I understand that my account will be permanently deleted after 30 days and my uploaded study resources will be anonymized.",
                                    style = MaterialTheme.typography.bodyMedium
                                )
                            }

                            NebButton(
                                text = "Request account deletion",
                                onClick = { viewModel.requestAccountDeletion(reason) },
                                enabled = confirmed,
                                tone = NebButtonTone.Danger,
                                size = NebButtonSize.Hero,
                                fillWidth = true
                            )
                        }
                    }
                }
                else -> {}
            }
        }
    }
}

@Composable
private fun BulletItem(text: String) {
    Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Box(
            modifier = Modifier
                .padding(top = 9.dp)
                .width(7.dp)
                .height(1.5.dp)
                .background(MaterialTheme.colorScheme.onSurfaceVariant)
        )
        Text(text = text, style = MaterialTheme.typography.bodyMedium)
    }
}
