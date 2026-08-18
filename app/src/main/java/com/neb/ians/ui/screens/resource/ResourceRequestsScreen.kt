package com.neb.ians.ui.screens.resource

import com.neb.ians.ui.components.LinkifyText

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.Inbox
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiResourceRequest
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.util.formatTimeAgo
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourceRequestsScreen(
    onNavigateBack: () -> Unit,
    viewModel: ResourceRequestsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var showCreateDialog by rememberSaveable { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(uiState.error) {
        uiState.error?.let { err ->
            snackbarHostState.showSnackbar(err)
            viewModel.clearError()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Resource Requests", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(bottom = 80.dp)
            ) {
                // Header block matching Web layout
                item {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        shape = RoundedCornerShape(20.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                        ),
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                    ) {
                        Column(
                            modifier = Modifier.padding(24.dp)
                        ) {
                            Text(
                                text = "Resource Requests",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Spacer(modifier = Modifier.height(6.dp))
                            Text(
                                text = "Can't find what you need? Request it here and the community will help.",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(
                                onClick = { showCreateDialog = true },
                                shape = WebPillShape,
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = MaterialTheme.colorScheme.primary
                                )
                            ) {
                                Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("New Request", fontWeight = FontWeight.SemiBold)
                            }
                        }
                    }
                }

                // Filter chips matching Web filter chips (Open, Fulfilled, Closed, All)
                item {
                    val scrollState = rememberScrollState()
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(scrollState)
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        listOf(
                            "open" to "Open",
                            "fulfilled" to "Fulfilled",
                            "closed" to "Closed",
                            null to "All"
                        ).forEach { (value, label) ->
                            val isSelected = uiState.statusFilter == value
                            Surface(
                                shape = WebPillShape,
                                color = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
                                border = BorderStroke(
                                    1.dp,
                                    if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant
                                ),
                                modifier = Modifier.clickable {
                                    viewModel.loadRequests(value)
                                }
                            ) {
                                Text(
                                    text = label,
                                    style = MaterialTheme.typography.labelLarge,
                                    fontWeight = FontWeight.Medium,
                                    color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                                )
                            }
                        }
                    }
                }

                // List contents
                if (uiState.isLoading && uiState.requests.isEmpty()) {
                    item {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(48.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            CircularProgressIndicator()
                        }
                    }
                } else if (uiState.requests.isEmpty()) {
                    item {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(48.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Inbox,
                                contentDescription = null,
                                modifier = Modifier.size(48.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(
                                text = "No requests yet. Be the first to request a resource!",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                textAlign = TextAlign.Center
                            )
                        }
                    }
                } else {
                    items(uiState.requests, key = { it.id }) { request ->
                        ResourceRequestCard(
                            request = request,
                            onUpvoteClick = { viewModel.toggleUpvote(request.id) }
                        )
                    }
                }
            }
        }
    }

    if (showCreateDialog) {
        CreateRequestDialog(
            isSubmitting = uiState.isSubmitting,
            onDismiss = { showCreateDialog = false },
            onSubmit = { title, desc, subject, grade ->
                viewModel.createRequest(title, desc, subject, grade) {
                    showCreateDialog = false
                }
            }
        )
    }
}

@Composable
fun ResourceRequestCard(
    request: ApiResourceRequest,
    onUpvoteClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerLow
        ),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            // Vote Area
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(2.dp),
                modifier = Modifier.width(40.dp)
            ) {
                val buttonColor = if (request.isUpvoted) {
                    MaterialTheme.colorScheme.primaryContainer
                } else {
                    Color.Transparent
                }
                val iconColor = if (request.isUpvoted) {
                    MaterialTheme.colorScheme.primary
                } else {
                    MaterialTheme.colorScheme.onSurfaceVariant
                }
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = buttonColor,
                    modifier = Modifier
                        .size(36.dp)
                        .clickable { onUpvoteClick() }
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Default.ArrowUpward,
                            contentDescription = "Upvote",
                            tint = iconColor,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
                Text(
                    text = request.upvoteCount.toString(),
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }

            // Info Content
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = request.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                if (!request.description.isNullOrBlank()) {
                    Spacer(modifier = Modifier.height(2.dp))
                    LinkifyText(
                        text = request.description,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 3,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (!request.subject.isNullOrBlank()) {
                        TagChip(label = request.subject)
                    }
                    if (!request.gradeLevel.isNullOrBlank()) {
                        TagChip(label = request.gradeLevel)
                    }
                    Text(
                        text = "·",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                    )
                    Text(
                        text = request.requestedByName ?: "Anonymous",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = FontWeight.Medium,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "·",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                    )
                    Text(
                        text = formatTimeAgo(request.createdAt),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1
                    )
                }
            }

            // Status Indicator tag
            val statusColor = when (request.status.lowercase()) {
                "open" -> Color(0xFF2E7D32)
                "fulfilled" -> Color(0xFF1565C0)
                else -> Color(0xFF616161)
            }
            val statusBg = statusColor.copy(alpha = 0.1f)
            Surface(
                color = statusBg,
                shape = RoundedCornerShape(6.dp),
                modifier = Modifier.padding(top = 2.dp)
            ) {
                Text(
                    text = request.status.uppercase(),
                    color = statusColor,
                    fontSize = 10.sp,
                    fontWeight = FontWeight.ExtraBold,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                )
            }
        }
    }
}

@Composable
fun TagChip(label: String) {
    Surface(
        color = MaterialTheme.colorScheme.secondaryContainer,
        shape = RoundedCornerShape(6.dp)
    ) {
        Text(
            text = label,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSecondaryContainer,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateRequestDialog(
    isSubmitting: Boolean,
    onDismiss: () -> Unit,
    onSubmit: (String, String, String, String) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var subject by remember { mutableStateOf("") }
    var gradeLevel by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var showGradeDropdown by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New Request", fontWeight = FontWeight.Bold) },
        text = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("What do you need? *") },
                    placeholder = { Text("e.g. Grade 12 Physics past papers") },
                    modifier = Modifier.fillMaxWidth()
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedTextField(
                        value = subject,
                        onValueChange = { subject = it },
                        label = { Text("Subject") },
                        placeholder = { Text("e.g. Physics") },
                        modifier = Modifier.weight(1f)
                    )

                    Box(modifier = Modifier.weight(1f)) {
                        OutlinedTextField(
                            value = gradeLevel.ifEmpty { "Any" },
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Grade") },
                            trailingIcon = {
                                ExposedDropdownMenuDefaults.TrailingIcon(expanded = showGradeDropdown)
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { showGradeDropdown = true }
                        )
                        DropdownMenu(
                            expanded = showGradeDropdown,
                            onDismissRequest = { showGradeDropdown = false }
                        ) {
                            listOf("", "Grade 11", "Grade 12", "Both").forEach { option ->
                                DropdownMenuItem(
                                    text = { Text(option.ifEmpty { "Any" }) },
                                    onClick = {
                                        gradeLevel = option
                                        showGradeDropdown = false
                                    }
                                )
                            }
                        }
                    }
                }

                OutlinedTextField(
                    value = description,
                    onValueChange = { description = it },
                    label = { Text("Details (optional)") },
                    placeholder = { Text("More details about what you're looking for...") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 2
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { onSubmit(title, description, subject, gradeLevel) },
                enabled = title.isNotBlank() && !isSubmitting,
                shape = WebPillShape
            ) {
                if (isSubmitting) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), color = MaterialTheme.colorScheme.onPrimary)
                } else {
                    Text("Submit")
                }
            }
        },
        dismissButton = {
            TextButton(
                onClick = onDismiss,
                enabled = !isSubmitting
            ) {
                Text("Cancel")
            }
        }
    )
}
