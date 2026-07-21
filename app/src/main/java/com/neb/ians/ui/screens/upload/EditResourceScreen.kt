package com.neb.ians.ui.screens.upload

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Image
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.WebEmptyState

/**
 * Owner-only resource editor — mirrors everything the upload flow collects:
 * all metadata, the link, a file replacement, and the cover (upload/URL/clear).
 * Saving re-submits the resource for review (server resets approval).
 */
@Composable
fun EditResourceScreen(
    resourceId: String,
    onNavigateBack: () -> Unit,
    viewModel: EditResourceViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }

    val filePicker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            var name: String? = null
            var size = 0L
            runCatching {
                context.contentResolver.query(uri, null, null, null, null)?.use { cursor ->
                    if (cursor.moveToFirst()) {
                        val nameIdx = cursor.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                        val sizeIdx = cursor.getColumnIndex(android.provider.OpenableColumns.SIZE)
                        if (nameIdx >= 0) name = cursor.getString(nameIdx)
                        if (sizeIdx >= 0) size = cursor.getLong(sizeIdx)
                    }
                }
            }
            viewModel.setReplaceFile(
                SelectedFile(uri = uri, name = name ?: uri.lastPathSegment ?: "file", size = size)
            )
        }
    }
    val thumbnailPicker = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        if (uri != null) viewModel.setThumbnail(uri)
    }

    LaunchedEffect(uiState.submitted) {
        if (uiState.submitted) {
            snackbarHostState.showSnackbar("Saved — your edit is back in review")
            onNavigateBack()
        }
    }
    LaunchedEffect(uiState.submitError) {
        uiState.submitError?.let { snackbarHostState.showSnackbar(it) }
    }

    Scaffold(
        topBar = { NebTopBar(showBrand = false, title = "Edit resource", onBack = onNavigateBack) },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
        when {
            uiState.isLoading -> Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) { CircularProgressIndicator() }

            uiState.notAllowed -> Box(
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {
                WebEmptyState(
                    title = "Owner only",
                    message = "You can only edit resources you uploaded.",
                    modifier = Modifier.padding(24.dp)
                )
            }

            uiState.loadError != null -> ErrorCard(
                message = uiState.loadError ?: "Couldn't load the resource",
                onRetry = { viewModel.load() },
                modifier = Modifier.padding(16.dp)
            )

            else -> EditResourceForm(
                uiState = uiState,
                viewModel = viewModel,
                onPickFile = { filePicker.launch(arrayOf("*/*")) },
                onPickThumbnail = { thumbnailPicker.launch("image/*") },
                onSave = { viewModel.save(context) },
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun EditResourceForm(
    uiState: EditResourceUiState,
    viewModel: EditResourceViewModel,
    onPickFile: () -> Unit,
    onPickThumbnail: () -> Unit,
    onSave: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 16.dp)
            .navigationBarsPadding(),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Spacer(Modifier.height(2.dp))

        if (uiState.approvalStatus != null) {
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = MaterialTheme.colorScheme.tertiaryContainer.copy(alpha = 0.45f)
            ) {
                Text(
                    text = "Status: ${uiState.approvalStatus}. Saving re-submits this resource for review — it may be hidden until approved again.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(12.dp)
                )
            }
        }

        EditSection("Basics") {
            EditField("Title *", uiState.title, { v -> viewModel.update { copy(title = v) } })
            EditField("Subject *", uiState.subject, { v -> viewModel.update { copy(subject = v) } }, hint = "e.g. Physics or Physics, Mathematics")
            EditField("Description", uiState.description, { v -> viewModel.update { copy(description = v) } }, singleLine = false)
            EditField("Type", uiState.type, { v -> viewModel.update { copy(type = v) } }, hint = "PDF, Note, Video, Audio, Image, Link, Textbook...")
            EditField("Level / class", uiState.gradeLevel, { v -> viewModel.update { copy(gradeLevel = v) } }, hint = "e.g. Class 12, Bachelor")
            EditField("Tags", uiState.tags, { v -> viewModel.update { copy(tags = v) } }, hint = "Comma separated")
        }

        EditSection("Classification") {
            EditField("Exam type", uiState.examType, { v -> viewModel.update { copy(examType = v) } }, hint = "Final, Midterm, Board, Entrance...")
            EditField("Faculty", uiState.faculty, { v -> viewModel.update { copy(faculty = v) } })
            EditField("Program", uiState.program, { v -> viewModel.update { copy(program = v) } })
            EditField("Year", uiState.year, { v -> viewModel.update { copy(year = v) } })
            EditField("School / college", uiState.school, { v -> viewModel.update { copy(school = v) } })
            EditField("Province", uiState.pradesh, { v -> viewModel.update { copy(pradesh = v) } })
            EditField("District", uiState.district, { v -> viewModel.update { copy(district = v) } })
        }

        EditSection("Attribution") {
            EditField("Author name", uiState.authorName, { v -> viewModel.update { copy(authorName = v) } })
            EditField("Source label", uiState.sourceLabel, { v -> viewModel.update { copy(sourceLabel = v) } })
            EditField("Source URL", uiState.sourceUrl, { v -> viewModel.update { copy(sourceUrl = v) } })
        }

        EditSection("File / link") {
            if (uiState.currentFileLabel.isNotBlank()) {
                Text(
                    text = "Current: ${uiState.currentFileLabel}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                OutlinedButton(onClick = onPickFile) { Text("Replace file") }
                uiState.replaceFile?.let { selected ->
                    Spacer(Modifier.width(8.dp))
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = MaterialTheme.colorScheme.surfaceContainerHigh
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(start = 10.dp, end = 2.dp, top = 4.dp, bottom = 4.dp)
                        ) {
                            Text(
                                selected.name,
                                style = MaterialTheme.typography.labelSmall,
                                maxLines = 1
                            )
                            IconButton(onClick = { viewModel.setReplaceFile(null) }, modifier = Modifier.size(26.dp)) {
                                Icon(Icons.Filled.Close, contentDescription = "Clear file", modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                }
            }
            EditField(
                "Link / external URL",
                uiState.fileUrl,
                { v -> viewModel.setFileUrl(v) },
                hint = "Used when no file is uploaded (Link, video URLs...)"
            )
        }

        EditSection("Cover image") {
            val preview = uiState.thumbnailUri ?: uiState.thumbnailUrl.takeIf { it.isNotBlank() }
            if (preview != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                ) {
                    AsyncImage(
                        model = preview,
                        contentDescription = "Cover preview",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                }
                Spacer(Modifier.height(8.dp))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onPickThumbnail) {
                    Icon(Icons.Filled.Image, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(Modifier.width(6.dp))
                    Text(if (preview == null) "Upload cover" else "Change cover")
                }
                if (uiState.thumbnailUri != null) {
                    OutlinedButton(onClick = { viewModel.setThumbnail(null) }) { Text("Undo pick") }
                }
                if (uiState.thumbnailUrl.isNotBlank() && uiState.thumbnailUri == null) {
                    OutlinedButton(onClick = { viewModel.setThumbnailUrl("") }) { Text("Remove cover") }
                }
            }
            EditField(
                "Cover URL",
                uiState.thumbnailUrl,
                { v -> viewModel.setThumbnailUrl(v) },
                hint = "Paste an image URL — an uploaded cover wins; empty auto-captures a video frame"
            )
        }

        uiState.submitError?.let { error ->
            Text(
                text = error,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.error
            )
        }

        Button(
            onClick = onSave,
            enabled = uiState.title.isNotBlank() && uiState.subject.isNotBlank() && !uiState.isSubmitting,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            shape = RoundedCornerShape(50)
        ) {
            if (uiState.isSubmitting) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    strokeWidth = 2.dp,
                    color = MaterialTheme.colorScheme.onPrimary
                )
                Spacer(Modifier.width(10.dp))
            }
            Text(if (uiState.isSubmitting) "Saving..." else "Save changes", fontWeight = FontWeight.Bold)
        }

        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun EditSection(title: String, content: @Composable () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )
        content()
    }
}

@Composable
private fun EditField(
    label: String,
    value: String,
    onChange: (String) -> Unit,
    hint: String? = null,
    singleLine: Boolean = true
) {
    OutlinedTextField(
        value = value,
        onValueChange = onChange,
        label = { Text(label) },
        placeholder = if (hint != null) ({ Text(hint, style = MaterialTheme.typography.bodySmall) }) else null,
        singleLine = singleLine,
        minLines = if (singleLine) 1 else 3,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    )
}
