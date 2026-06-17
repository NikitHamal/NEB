package com.neb.ians.ui.screens.upload

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.CloudUpload
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberTopAppBarState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

private enum class UploadStep(val title: String, val subtitle: String, val optional: Boolean) {
    Basics("Basics", "Title, subject and type", false),
    Files("Files", "Upload or paste a link", false),
    Details("Details", "Description and tags", true),
    Attribution("Attribution", "Credit the original source", true),
    Review("Review", "Confirm and submit", false)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UploadScreen(
    onNavigateBack: () -> Unit,
    onUploadSuccess: () -> Unit,
    viewModel: UploadViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val scrollBehavior = TopAppBarDefaults.pinnedScrollBehavior(rememberTopAppBarState())

    var currentStep by rememberSaveable { mutableStateOf(0) }
    var showSubjectPicker by remember { mutableStateOf(false) }
    var showTagPicker by remember { mutableStateOf(false) }

    val filePicker = rememberLauncherForActivityResult(
        ActivityResultContracts.GetMultipleContents()
    ) { uris: List<Uri> ->
        if (uris.isNotEmpty()) {
            val files = uris.mapNotNull { uri ->
                val info = viewModel.getFileInfo(context, uri)
                if (info != null) SelectedFile(uri, info.first, info.second) else null
            }
            val validFiles = files.filter { it.size <= UploadViewModel.MAX_FILE_SIZE }
            viewModel.addFiles(validFiles)
            if (validFiles.size < files.size) {
                viewModel.setFileError("Some files exceeded 50 MB and were skipped.")
            }
        }
    }

    if (uiState.submitSuccess) {
        UploadSuccessScreen(
            onUploadAnother = { viewModel.resetSuccess(); currentStep = 0 },
            onBrowseLibrary = onUploadSuccess
        )
        return
    }

    val steps = UploadStep.entries
    val step = steps[currentStep]
    val isLastStep = currentStep == steps.lastIndex
    val canGoNext = when (step) {
        UploadStep.Basics -> uiState.title.isNotBlank() && uiState.subject.isNotBlank()
        UploadStep.Files -> uiState.selectedFiles.isNotEmpty() || uiState.fileUrl.isNotBlank()
        else -> true
    }

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(
                        text = "New Resource",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        bottomBar = {
            WizardBottomBar(
                step = step,
                stepIndex = currentStep,
                totalSteps = steps.size,
                isLastStep = isLastStep,
                canGoNext = canGoNext,
                isSubmitting = uiState.isSubmitting,
                uploadProgress = uiState.uploadProgress,
                fileCount = uiState.selectedFiles.size,
                onBack = { if (currentStep > 0) currentStep-- },
                onNext = { if (currentStep < steps.lastIndex) currentStep++ },
                onSubmit = { viewModel.submit(context) }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 12.dp)
                .navigationBarsPadding(),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            ErrorBanner(uiState.submitError)

            StepIndicator(
                currentStep = currentStep,
                totalSteps = steps.size,
                stepTitles = steps.map { it.title }
            )

            AnimatedContent(
                targetState = currentStep,
                transitionSpec = {
                    fadeIn(tween(150)) togetherWith fadeOut(tween(100))
                },
                label = "stepTransition"
            ) { stepIndex ->
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    when (steps[stepIndex]) {
                        UploadStep.Basics -> BasicsStep(
                            uiState = uiState,
                            viewModel = viewModel,
                            onOpenSubjectPicker = { showSubjectPicker = true }
                        )
                        UploadStep.Files -> FilesStep(
                            uiState = uiState,
                            viewModel = viewModel,
                            onPickFiles = { filePicker.launch("application/*") },
                            onRemoveFile = viewModel::removeFileAt,
                            onClearFiles = viewModel::clearFiles
                        )
                        UploadStep.Details -> DetailsStep(
                            uiState = uiState,
                            viewModel = viewModel,
                            onOpenTagPicker = { showTagPicker = true }
                        )
                        UploadStep.Attribution -> AttributionStep(
                            uiState = uiState,
                            viewModel = viewModel
                        )
                        UploadStep.Review -> ReviewStep(
                            uiState = uiState,
                            onEdit = { currentStep = it }
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
        }
    }

    if (showSubjectPicker) {
        ChipPickerDialog(
            title = "Select Subjects",
            items = UploadViewModel.SUBJECTS,
            selectedItems = uiState.subject.asCsvList(),
            allowCustom = true,
            customPlaceholder = "Add a custom subject",
            onDismiss = { showSubjectPicker = false },
            onConfirm = { selected ->
                viewModel.updateSubject(selected.joinToString(", "))
                showSubjectPicker = false
            }
        )
    }

    if (showTagPicker) {
        ChipPickerDialog(
            title = "Select Tags",
            items = UploadViewModel.COMMON_TAGS,
            selectedItems = uiState.tags.asCsvList(),
            allowCustom = true,
            customPlaceholder = "Add a custom tag",
            onDismiss = { showTagPicker = false },
            onConfirm = { selected ->
                viewModel.updateTags(selected.joinToString(", "))
                showTagPicker = false
            }
        )
    }
}

@Composable
private fun StepIndicator(
    currentStep: Int,
    totalSteps: Int,
    stepTitles: List<String>
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        stepTitles.forEachIndexed { index, _ ->
            val isCurrent = index == currentStep
            val isDone = index < currentStep
            val color = when {
                isCurrent -> MaterialTheme.colorScheme.primary
                isDone -> MaterialTheme.colorScheme.primary.copy(alpha = 0.6f)
                else -> MaterialTheme.colorScheme.surfaceContainerHighest
            }
            val onColor = when {
                isCurrent || isDone -> MaterialTheme.colorScheme.onPrimary
                else -> MaterialTheme.colorScheme.onSurfaceVariant
            }
            Surface(
                shape = CircleShape,
                color = color,
                modifier = Modifier.size(24.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    if (isDone) {
                        Icon(
                            imageVector = Icons.Filled.Check,
                            contentDescription = null,
                            tint = onColor,
                            modifier = Modifier.size(14.dp)
                        )
                    } else {
                        Text(
                            text = (index + 1).toString(),
                            color = onColor,
                            fontWeight = FontWeight.Bold,
                            style = MaterialTheme.typography.labelSmall,
                            maxLines = 1
                        )
                    }
                }
            }
            if (index < totalSteps - 1) {
                HorizontalDivider(
                    modifier = Modifier.weight(1f),
                    thickness = 2.dp,
                    color = if (isDone) MaterialTheme.colorScheme.primary.copy(alpha = 0.6f)
                    else MaterialTheme.colorScheme.surfaceContainerHighest
                )
            }
        }
    }
}

@Composable
private fun WizardBottomBar(
    step: UploadStep,
    stepIndex: Int,
    totalSteps: Int,
    isLastStep: Boolean,
    canGoNext: Boolean,
    isSubmitting: Boolean,
    uploadProgress: Float,
    fileCount: Int,
    onBack: () -> Unit,
    onNext: () -> Unit,
    onSubmit: () -> Unit
) {
    Surface(
        color = MaterialTheme.colorScheme.surface,
        shadowElevation = 8.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            if (stepIndex > 0) {
                OutlinedButton(
                    onClick = onBack,
                    shape = CircleShape,
                    enabled = !isSubmitting,
                    modifier = Modifier.height(46.dp)
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = null,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Back", maxLines = 1, fontWeight = FontWeight.SemiBold)
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            if (isLastStep) {
                Button(
                    onClick = onSubmit,
                    shape = CircleShape,
                    enabled = !isSubmitting,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.onPrimary
                    ),
                    modifier = Modifier.height(46.dp)
                ) {
                    if (isSubmitting) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(18.dp),
                            color = MaterialTheme.colorScheme.onPrimary,
                            strokeWidth = 2.dp
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = if (fileCount > 1)
                                "${((uploadProgress * fileCount).toInt() + 1)}/$fileCount"
                            else "Uploading...",
                            maxLines = 1,
                            fontWeight = FontWeight.SemiBold
                        )
                    } else {
                        Icon(
                            imageVector = Icons.Filled.CloudUpload,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Submit", maxLines = 1, fontWeight = FontWeight.SemiBold)
                    }
                }
            } else {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (step.optional) {
                        TextButton(
                            onClick = onNext,
                            shape = CircleShape,
                            enabled = !isSubmitting
                        ) {
                            Text("Skip", maxLines = 1, fontWeight = FontWeight.SemiBold)
                        }
                    }
                    Button(
                        onClick = onNext,
                        shape = CircleShape,
                        enabled = canGoNext && !isSubmitting,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.primary,
                            contentColor = MaterialTheme.colorScheme.onPrimary
                        ),
                        modifier = Modifier.height(46.dp)
                    ) {
                        Text("Next", maxLines = 1, fontWeight = FontWeight.SemiBold)
                        Spacer(modifier = Modifier.width(6.dp))
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ErrorBanner(error: String?) {
    AnimatedVisibility(visible = error != null) {
        Surface(
            shape = RoundedCornerShape(12.dp),
            color = MaterialTheme.colorScheme.errorContainer,
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onErrorContainer,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = error ?: "",
                    color = MaterialTheme.colorScheme.onErrorContainer,
                    style = MaterialTheme.typography.bodyMedium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

internal fun String.asCsvList(): List<String> =
    split(",").map { it.trim() }.filter { it.isNotBlank() }
