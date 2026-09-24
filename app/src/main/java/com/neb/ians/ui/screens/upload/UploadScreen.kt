@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
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
import androidx.compose.material.icons.automirrored.rounded.ArrowForward
import androidx.compose.material.icons.rounded.AttachFile
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Upload
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
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
import com.neb.ians.ui.components.NebChoiceSheet
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import java.io.File

/**
 * Three steps, in the order the upload actually happens.
 *
 * The pages come first, because that is the work the user has already done.
 * The two questions that cannot be guessed come second. Everything the library
 * would merely like sits in its own optional step, which ends in Skip until it
 * is given something. Publish is the last thing, and it stays grey until the
 * upload would actually go through.
 */
private enum class UploadStep { Basics, Details, Review }

private enum class UploadSheet { Subject, Level, Type, Exam, Province, Tags }

@Composable
fun UploadScreen(
    onNavigateBack: () -> Unit,
    onUploadSuccess: () -> Unit,
    viewModel: UploadViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current

    var stepIndex by rememberSaveable { mutableIntStateOf(0) }
    var sheet by remember { mutableStateOf<UploadSheet?>(null) }
    var linkMode by rememberSaveable { mutableStateOf(false) }
    val step = UploadStep.entries[stepIndex.coerceIn(0, UploadStep.entries.lastIndex)]

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
                stepIndex = 0
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

    BackHandler(enabled = stepIndex > 0) { stepIndex-- }

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
                    IconButton(onClick = { if (stepIndex > 0) stepIndex-- else onNavigateBack() }) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        bottomBar = {
            UploadActionBar(
                state = uiState,
                step = step,
                onBack = { if (stepIndex > 0) stepIndex-- },
                onAdvance = { stepIndex = (stepIndex + 1).coerceAtMost(UploadStep.entries.lastIndex) },
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
            item(key = "header") {
                UploadStepHeader(
                    stepIndex = stepIndex,
                    total = UploadStep.entries.size,
                    title = when (step) {
                        UploadStep.Basics -> if (uiState.isEditMode) "The resource" else "Bring the file in"
                        UploadStep.Details -> "More details"
                        UploadStep.Review -> if (uiState.isEditMode) "Check the changes" else "Ready to publish"
                    },
                    caption = when (step) {
                        UploadStep.Basics -> "The file, a title and a subject. Nothing else is required."
                        UploadStep.Details -> "All optional. Everything here helps people find it later."
                        UploadStep.Review -> "This is how the library will show it."
                    }
                )
            }

            item(key = "problem") {
                ProblemBanner(
                    message = uiState.submitError ?: uiState.fileError,
                    onDismiss = viewModel::dismissError
                )
            }

            when (step) {
                UploadStep.Basics -> {
                    item(key = "source") {
                        if (linkMode) {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                UploadLinkField(uiState, viewModel)
                                SwitchSourceRow(
                                    label = "Attach the file instead",
                                    onClick = { linkMode = false }
                                )
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
                            onOpenSubjectPicker = { sheet = UploadSheet.Subject },
                            onOpenLevelPicker = { sheet = UploadSheet.Level }
                        )
                    }
                }

                UploadStep.Details -> {
                    item(key = "details") {
                        UploadMoreDetails(
                            state = uiState,
                            viewModel = viewModel,
                            onOpenTagPicker = { sheet = UploadSheet.Tags },
                            onOpenTypePicker = { sheet = UploadSheet.Type },
                            onOpenExamPicker = { sheet = UploadSheet.Exam },
                            onOpenProvincePicker = { sheet = UploadSheet.Province },
                            onPickCover = {
                                coverPicker.launch(
                                    PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                                )
                            }
                        )
                    }
                }

                UploadStep.Review -> {
                    item(key = "review") {
                        UploadReviewStep(
                            state = uiState,
                            onEditBasics = { stepIndex = 0 },
                            onEditDetails = { stepIndex = 1 }
                        )
                    }
                }
            }

            item(key = "tail") { Spacer(Modifier.height(24.dp)) }
        }
    }

    UploadSheets(
        sheet = sheet,
        state = uiState,
        viewModel = viewModel,
        onDismiss = { sheet = null }
    )
}

@Composable
private fun UploadSheets(
    sheet: UploadSheet?,
    state: UploadFormState,
    viewModel: UploadViewModel,
    onDismiss: () -> Unit
) {
    when (sheet) {
        null -> Unit

        UploadSheet.Subject -> NebChoiceSheet(
            title = "Subject",
            subtitle = "Pick every subject this covers, or add your own.",
            options = UploadOptions.SUBJECTS,
            selected = state.subject.asCsvList(),
            multiSelect = true,
            allowCustom = true,
            customPlaceholder = "Add a subject",
            onDismiss = onDismiss,
            onConfirm = {
                viewModel.updateSubject(it.joinToString(", "))
                onDismiss()
            }
        )

        UploadSheet.Level -> NebChoiceSheet(
            title = "Level",
            subtitle = "Who is this written for? Add yours if it is not listed.",
            options = state.levelOptions,
            selected = listOfNotNull(state.gradeLevel.takeIf { it.isNotBlank() }),
            multiSelect = false,
            allowCustom = true,
            customPlaceholder = "Add a level",
            onAddCustom = viewModel::addCustomLevel,
            onDismiss = onDismiss,
            onConfirm = {
                viewModel.updateGradeLevel(it.firstOrNull().orEmpty())
                onDismiss()
            }
        )

        UploadSheet.Type -> NebChoiceSheet(
            title = "Type",
            options = UploadOptions.RESOURCE_TYPES,
            selected = listOfNotNull(state.type.takeIf { it.isNotBlank() }),
            multiSelect = false,
            onDismiss = onDismiss,
            onConfirm = {
                viewModel.updateType(it.firstOrNull().orEmpty())
                onDismiss()
            }
        )

        UploadSheet.Exam -> NebChoiceSheet(
            title = "Exam",
            options = UploadOptions.EXAM_TYPES,
            selected = listOfNotNull(state.examType.takeIf { it.isNotBlank() }),
            multiSelect = false,
            onDismiss = onDismiss,
            onConfirm = {
                viewModel.updateExamType(it.firstOrNull().orEmpty())
                onDismiss()
            }
        )

        UploadSheet.Province -> NebChoiceSheet(
            title = "Province",
            options = UploadOptions.PROVINCES,
            selected = listOfNotNull(state.pradesh.takeIf { it.isNotBlank() }),
            multiSelect = false,
            onDismiss = onDismiss,
            onConfirm = {
                viewModel.updatePradesh(it.firstOrNull().orEmpty())
                onDismiss()
            }
        )

        UploadSheet.Tags -> NebChoiceSheet(
            title = "Tags",
            subtitle = "A few words people would search for.",
            options = UploadOptions.COMMON_TAGS,
            selected = state.tags.asCsvList(),
            multiSelect = true,
            allowCustom = true,
            customPlaceholder = "Add a tag",
            onDismiss = onDismiss,
            onConfirm = {
                viewModel.updateTags(it.joinToString(", "))
                onDismiss()
            }
        )
    }
}

/** Where you are, what this step is for. Three bars, filled as you go. */
@Composable
private fun UploadStepHeader(
    stepIndex: Int,
    total: Int,
    title: String,
    caption: String
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 2.dp, bottom = 2.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            repeat(total) { index ->
                val filled = index <= stepIndex
                val color by animateColorAsState(
                    targetValue = if (filled) {
                        MaterialTheme.colorScheme.onSurface
                    } else {
                        MaterialTheme.colorScheme.outlineVariant
                    },
                    animationSpec = nebEffectsSpec(),
                    label = "upload_step_$index"
                )
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height(4.dp)
                        .clip(RoundedCornerShape(50))
                        .background(color)
                )
            }
        }
        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(
                text = title,
                style = MaterialTheme.typography.headlineSmallEmphasized,
                color = MaterialTheme.colorScheme.onSurface
            )
            Text(
                text = caption,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

/**
 * The one action for the step you are on.
 *
 * On the first step it is greyed out until the upload would actually go
 * through, so the button never lies about what pressing it will do. On the
 * optional step it reads Skip until something is filled in, then Next. On the
 * last step it publishes.
 */
@Composable
private fun UploadActionBar(
    state: UploadFormState,
    step: UploadStep,
    onBack: () -> Unit,
    onAdvance: () -> Unit,
    onSubmit: () -> Unit
) {
    val working = state.isSubmitting || state.isPreparing
    val status = when {
        state.isPreparing -> "Preparing page ${state.pagesPrepared} of ${state.selectedFiles.size}"
        state.isSubmitting -> "Uploading…"
        step == UploadStep.Basics && state.missing.isNotEmpty() ->
            "Add ${state.missing.filterNot { it == "a price" }.joinToString(", ")}"
        step == UploadStep.Review && state.missing.isNotEmpty() ->
            "Add ${state.missing.joinToString(", ")}"
        else -> null
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
            if (status != null && status.isNotBlank()) {
                Text(
                    text = status,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                if (step != UploadStep.Basics) {
                    NebButton(
                        text = "Back",
                        onClick = onBack,
                        tone = NebButtonTone.Outlined,
                        size = NebButtonSize.Hero,
                        enabled = !working
                    )
                }
                when (step) {
                    UploadStep.Basics -> NebButton(
                        text = "Continue",
                        onClick = onAdvance,
                        trailingIcon = Icons.AutoMirrored.Rounded.ArrowForward,
                        size = NebButtonSize.Hero,
                        fillWidth = true,
                        enabled = state.essentialsReady,
                        modifier = Modifier.weight(1f)
                    )

                    UploadStep.Details -> NebButton(
                        text = if (state.hasDetails) "Next" else "Skip for now",
                        onClick = onAdvance,
                        trailingIcon = Icons.AutoMirrored.Rounded.ArrowForward,
                        tone = if (state.hasDetails) NebButtonTone.Primary else NebButtonTone.Tonal,
                        size = NebButtonSize.Hero,
                        fillWidth = true,
                        modifier = Modifier.weight(1f)
                    )

                    UploadStep.Review -> NebButton(
                        text = if (state.isEditMode) "Save changes" else "Publish",
                        onClick = onSubmit,
                        icon = Icons.Rounded.Upload,
                        size = NebButtonSize.Hero,
                        fillWidth = true,
                        enabled = state.canSubmit,
                        loading = working,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}

@Composable
private fun SwitchSourceRow(label: String, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(14.dp))
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(
            imageVector = Icons.Rounded.AttachFile,
            contentDescription = null,
            modifier = Modifier.size(18.dp),
            tint = MaterialTheme.colorScheme.onSurface
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSurface
        )
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
                NebLoader(size = NebLoaderSize.Screen)
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
