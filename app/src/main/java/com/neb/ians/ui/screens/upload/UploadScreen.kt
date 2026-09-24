@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.AttachFile
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Upload
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.LoadingIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.core.content.FileProvider
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.nebPressable
import java.io.File

/**
 * One screen, in the order the upload actually happens.
 *
 * The old version was a five step wizard: basics, files, details, attribution,
 * review. Somebody who has just spent an hour photographing a hundred pages of
 * notes then had to walk through four more screens before the app would take
 * them, and their pages were posted as a hundred separate resources at the end
 * of it. Here the pages come first, the two questions that cannot be guessed
 * come second, everything else is folded away, and publish is always visible.
 */
@Composable
fun UploadScreen(
    onNavigateBack: () -> Unit,
    onUploadSuccess: () -> Unit,
    viewModel: UploadViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current

    var showSubjectPicker by remember { mutableStateOf(false) }
    var showTagPicker by remember { mutableStateOf(false) }
    var showMore by rememberSaveable { mutableStateOf(false) }
    var linkMode by rememberSaveable { mutableStateOf(false) }

    val photoPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.PickMultipleVisualMedia()
    ) { uris ->
        viewModel.addFiles(uris.mapNotNull { describe(context, it) })
    }

    val filePicker = rememberLauncherForActivityResult(
        ActivityResultContracts.GetMultipleContents()
    ) { uris ->
        val described = uris.mapNotNull { describe(context, it) }
        val small = described.filter { it.size <= UploadOptions.MAX_FILE_SIZE }
        viewModel.addFiles(small)
        if (small.size < described.size) {
            viewModel.setFileError("Files over 50 MB were left out.")
        }
    }

    val coverPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.PickVisualMedia()
    ) { uri -> if (uri != null) viewModel.setThumbnail(uri) }

    // The scanning loop: every successful shot is added and the camera reopens,
    // so a hundred pages is a hundred shutter taps and one back press.
    var captureTick by remember { mutableIntStateOf(0) }
    var captureUri by remember { mutableStateOf<Uri?>(null) }
    val cameraLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.TakePicture()
    ) { saved ->
        val uri = captureUri
        if (saved && uri != null) {
            describe(context, uri)?.let { viewModel.addFiles(listOf(it.copy(isImage = true))) }
            captureTick++
        }
    }
    LaunchedEffect(captureTick) {
        if (captureTick == 0) return@LaunchedEffect
        val uri = createCaptureUri(context) ?: return@LaunchedEffect
        captureUri = uri
        runCatching { cameraLauncher.launch(uri) }
    }

    if (uiState.submitSuccess && !uiState.isEditMode) {
        UploadSuccessScreen(
            onUploadAnother = {
                viewModel.resetSuccess()
                showMore = false
                linkMode = false
            },
            onBrowseLibrary = onUploadSuccess
        )
        return
    }

    LaunchedEffect(uiState.editSuccess) {
        if (uiState.editSuccess) onUploadSuccess()
    }

    if (uiState.isEditMode && EditGate(uiState, onNavigateBack, viewModel::loadEditResource)) return

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = if (uiState.isEditMode) "Edit resource" else "New upload",
                        style = MaterialTheme.typography.titleLargeEmphasized,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        bottomBar = {
            PublishBar(
                state = uiState,
                onSubmit = { viewModel.submit(context) }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding(),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item(key = "problem") {
                ProblemBanner(
                    message = uiState.submitError ?: uiState.fileError,
                    onDismiss = viewModel::dismissError
                )
            }

            item(key = "source") {
                if (linkMode) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        UploadLinkField(uiState, viewModel)
                        Row(
                            modifier = Modifier
                                .nebPressable(onClick = { linkMode = false })
                                .clip(RoundedCornerShape(14.dp))
                                .padding(vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.AttachFile,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                                tint = MaterialTheme.colorScheme.primary
                            )
                            Text(
                                text = "Attach the file instead",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                } else {
                    UploadSourceSection(
                        state = uiState,
                        onCapturePages = { captureTick++ },
                        onPickPhotos = {
                            photoPicker.launch(
                                PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                            )
                        },
                        onPickFiles = { filePicker.launch("*/*") },
                        onUseLink = { linkMode = true },
                        onRemovePage = viewModel::removeFileAt,
                        onCombineChange = viewModel::setCombinePages
                    )
                }
            }

            item(key = "essentials") {
                UploadEssentials(
                    state = uiState,
                    viewModel = viewModel,
                    onOpenSubjectPicker = { showSubjectPicker = true }
                )
            }

            item(key = "divider") {
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
            }

            item(key = "more") {
                UploadMoreDetails(
                    state = uiState,
                    viewModel = viewModel,
                    expanded = showMore,
                    onToggle = { showMore = !showMore },
                    onOpenTagPicker = { showTagPicker = true },
                    onPickCover = {
                        coverPicker.launch(
                            PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                        )
                    }
                )
            }

            item(key = "tail") { Spacer(Modifier.height(24.dp)) }
        }
    }

    if (showSubjectPicker) {
        ChipPickerDialog(
            title = "Subject",
            items = UploadOptions.SUBJECTS,
            selectedItems = uiState.subject.asCsvList(),
            allowCustom = true,
            customPlaceholder = "Add a subject",
            onDismiss = { showSubjectPicker = false },
            onConfirm = {
                viewModel.updateSubject(it.joinToString(", "))
                showSubjectPicker = false
            }
        )
    }

    if (showTagPicker) {
        ChipPickerDialog(
            title = "Tags",
            items = UploadOptions.COMMON_TAGS,
            selectedItems = uiState.tags.asCsvList(),
            allowCustom = true,
            customPlaceholder = "Add a tag",
            onDismiss = { showTagPicker = false },
            onConfirm = {
                viewModel.updateTags(it.joinToString(", "))
                showTagPicker = false
            }
        )
    }
}

/**
 * Publish, and the one sentence explaining why it would not work yet.
 *
 * The button stays live even when something is missing — pressing it marks the
 * fields rather than doing nothing, which is the difference between a screen
 * that answers and a screen that ignores you.
 */
@Composable
private fun PublishBar(state: UploadFormState, onSubmit: () -> Unit) {
    val working = state.isSubmitting || state.isPreparing
    val status = when {
        state.isPreparing -> "Preparing page ${state.pagesPrepared} of ${state.selectedFiles.size}"
        state.isSubmitting -> "Uploading…"
        state.missing.isEmpty() -> null
        else -> "Add ${state.missing.joinToString(", ")}"
    }

    Surface(color = MaterialTheme.colorScheme.surface) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(horizontal = 16.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            AnimatedVisibility(visible = working) {
                LinearProgressIndicator(
                    progress = { state.uploadProgress.coerceIn(0f, 1f) },
                    modifier = Modifier.fillMaxWidth()
                )
            }
            if (status != null) {
                Text(
                    text = status,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            NebButton(
                text = if (state.isEditMode) "Save changes" else "Publish",
                onClick = onSubmit,
                icon = Icons.Rounded.Upload,
                size = NebButtonSize.Hero,
                fillWidth = true,
                loading = working
            )
        }
    }
}

@Composable
private fun ProblemBanner(message: String?, onDismiss: () -> Unit) {
    AnimatedVisibility(visible = message != null) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(18.dp))
                .background(MaterialTheme.colorScheme.errorContainer)
                .padding(start = 14.dp, end = 4.dp, top = 10.dp, bottom = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = message.orEmpty(),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onErrorContainer,
                modifier = Modifier.weight(1f)
            )
            IconButton(onClick = onDismiss, modifier = Modifier.size(36.dp)) {
                Icon(
                    imageVector = Icons.Rounded.Close,
                    contentDescription = "Dismiss",
                    tint = MaterialTheme.colorScheme.onErrorContainer,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
    }
}

/** Returns true when the edit gate handled the screen and nothing else should draw. */
@Composable
private fun EditGate(
    state: UploadFormState,
    onNavigateBack: () -> Unit,
    onRetry: () -> Unit
): Boolean {
    val message = when {
        state.editLoading -> null
        state.notAllowed -> "Only the person who uploaded this can edit it."
        state.editLoadError != null -> state.editLoadError
        else -> return false
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Edit resource", style = MaterialTheme.typography.titleLargeEmphasized) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp),
            contentAlignment = Alignment.Center
        ) {
            if (message == null) {
                LoadingIndicator()
            } else {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = message,
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    if (state.editLoadError != null) {
                        NebButton(text = "Try again", onClick = onRetry, tone = NebButtonTone.Outlined)
                    }
                }
            }
        }
    }
    return true
}

private fun describe(context: Context, uri: Uri): SelectedFile? {
    val info = UploadMedia.getFileInfo(context, uri)
    val name = info?.first?.takeIf { it.isNotBlank() } ?: uri.lastPathSegment ?: return null
    return SelectedFile(
        uri = uri,
        name = name,
        size = info?.second ?: 0L,
        isImage = PageDocumentBuilder.isImage(context, uri, name)
    )
}

private fun createCaptureUri(context: Context): Uri? = try {
    val directory = File(context.cacheDir, "uploads").apply { mkdirs() }
    val file = File(directory, "page_${System.currentTimeMillis()}.jpg")
    FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file)
} catch (_: Exception) {
    null
}

internal fun String.asCsvList(): List<String> =
    split(",").map { it.trim() }.filter { it.isNotBlank() }
