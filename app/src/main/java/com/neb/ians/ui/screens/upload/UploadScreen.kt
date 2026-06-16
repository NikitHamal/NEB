package com.neb.ians.ui.screens.upload

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CloudUpload
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberTopAppBarState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
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
import com.neb.ians.ui.components.NebCard
import com.neb.ians.ui.theme.getSubjectColor

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

    var showSubjectPicker by remember { mutableStateOf(false) }
    var showTagPicker by remember { mutableStateOf(false) }
    var showMoreDetails by remember { mutableStateOf(false) }

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
            onUploadAnother = { viewModel.resetSuccess() },
            onBrowseLibrary = onUploadSuccess
        )
        return
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
        }) { padding ->
        LazyColumn(
            state = rememberLazyListState(),
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding()
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            item { IntroText() }

            item { ErrorBanner(uiState.submitError) }

            item {
                BasicInfoCard(
                    uiState = uiState,
                    viewModel = viewModel,
                    onOpenSubjectPicker = { showSubjectPicker = true },
                    onOpenTagPicker = { showTagPicker = true }
                )
            }

            item {
                MoreDetailsSection(
                    expanded = showMoreDetails,
                    onToggle = { showMoreDetails = !showMoreDetails },
                    faculty = uiState.faculty,
                    onFacultyChange = viewModel::updateFaculty,
                    program = uiState.program,
                    onProgramChange = viewModel::updateProgram,
                    year = uiState.year,
                    onYearChange = viewModel::updateYear,
                    school = uiState.school,
                    onSchoolChange = viewModel::updateSchool,
                    pradesh = uiState.pradesh,
                    onPradeshChange = viewModel::updatePradesh,
                    district = uiState.district,
                    onDistrictChange = viewModel::updateDistrict
                )
            }

            item {
                UploadFileCard(
                    uiState = uiState,
                    viewModel = viewModel,
                    onPickFiles = { filePicker.launch("application/*") },
                    onRemoveFile = viewModel::removeFileAt,
                    onClearFiles = viewModel::clearFiles
                )
            }

            item {
                AttributionCard(
                    uiState = uiState,
                    viewModel = viewModel
                )
            }

            item {
                SubmitFooter(
                    uiState = uiState,
                    onSubmit = { viewModel.submit(context) }
                )
            }

            item { Spacer(modifier = Modifier.height(32.dp)) }
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
private fun IntroText() {
    Text(
        text = "Help fellow learners by sharing study materials. Your contribution will be reviewed before publishing.",
        style = MaterialTheme.typography.bodyMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.padding(top = 8.dp)
    )
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
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun BasicInfoCard(
    uiState: UploadFormState,
    viewModel: UploadViewModel,
    onOpenSubjectPicker: () -> Unit,
    onOpenTagPicker: () -> Unit
) {
    NebCard(
        shape = RoundedCornerShape(20.dp),
        containerColor = MaterialTheme.colorScheme.surfaceContainerLow,
        border = null
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            UploadSectionHeader(
                icon = Icons.Filled.Description,
                title = "Basic Info"
            )

            OutlinedTextField(
                value = uiState.title,
                onValueChange = viewModel::updateTitle,
                label = { Text("Title *") },
                placeholder = { Text("e.g. Class 12 Computer Engineering Final Exam 2081") },
                isError = uiState.titleError != null,
                supportingText = uiState.titleError?.let { { Text(it) } },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            val subjects = uiState.subject.asCsvList()
            AttributeChipRow(
                label = "Subject *",
                placeholder = "Choose at least one",
                values = subjects,
                onRemove = { removed ->
                    viewModel.updateSubject(subjects.filter { it != removed }.joinToString(", "))
                },
                onAddClick = onOpenSubjectPicker,
                error = uiState.subjectError,
                accentColor = subjects.firstOrNull()?.let { getSubjectColor(it) }
            )

            Text(
                text = "Resource type",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            ResourceTypeChips(
                selected = uiState.type,
                options = UploadViewModel.RESOURCE_TYPES,
                onSelect = viewModel::updateType
            )

            GradeAndExamRow(
                uiState = uiState,
                viewModel = viewModel
            )

            OutlinedTextField(
                value = uiState.description,
                onValueChange = viewModel::updateDescription,
                label = { Text("Description") },
                placeholder = { Text("Briefly describe this resource...") },
                modifier = Modifier.fillMaxWidth(),
                minLines = 3,
                maxLines = 5
            )

            AttributeChipRow(
                label = "Tags",
                placeholder = "Add tags",
                values = uiState.tags.asCsvList(),
                onRemove = { removed ->
                    viewModel.updateTags(uiState.tags.asCsvList().filter { it != removed }.joinToString(", "))
                },
                onAddClick = onOpenTagPicker
            )
        }
    }
}

@Composable
private fun GradeAndExamRow(
    uiState: UploadFormState,
    viewModel: UploadViewModel
) {
    val showExamType = uiState.type in listOf(
        "Past Paper", "Model Paper", "Guide", "Solution", "Note", "PDF"
    )
    if (showExamType) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            DropdownField(
                label = "Level / Grade",
                value = uiState.gradeLevel,
                options = UploadViewModel.GRADE_LEVELS,
                onValueChange = viewModel::updateGradeLevel,
                modifier = Modifier.weight(1f)
            )
            DropdownField(
                label = "Exam Type",
                value = uiState.examType,
                options = UploadViewModel.EXAM_TYPES,
                onValueChange = viewModel::updateExamType,
                modifier = Modifier.weight(1f)
            )
        }
    } else {
        DropdownField(
            label = "Level / Grade",
            value = uiState.gradeLevel,
            options = UploadViewModel.GRADE_LEVELS,
            onValueChange = viewModel::updateGradeLevel,
            modifier = Modifier.fillMaxWidth()
        )
    }
}

@Composable
private fun UploadFileCard(
    uiState: UploadFormState,
    viewModel: UploadViewModel,
    onPickFiles: () -> Unit,
    onRemoveFile: (Int) -> Unit,
    onClearFiles: () -> Unit
) {
    NebCard(
        shape = RoundedCornerShape(20.dp),
        containerColor = MaterialTheme.colorScheme.surfaceContainerLow,
        border = null
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            UploadSectionHeader(
                icon = Icons.Filled.CloudUpload,
                title = "Upload File"
            )

            FileDropzone(
                selectedFiles = uiState.selectedFiles,
                fileError = uiState.fileError,
                onPickFiles = onPickFiles,
                onRemoveFile = onRemoveFile,
                onClearFiles = onClearFiles
            )

            LinkAlternativeFields(
                uiState = uiState,
                viewModel = viewModel
            )
        }
    }
}

@Composable
private fun LinkAlternativeFields(
    uiState: UploadFormState,
    viewModel: UploadViewModel
) {
    val enabled = uiState.selectedFiles.isEmpty()

    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        HorizontalDivider(modifier = Modifier.weight(1f))
        Text(
            text = "or paste a link",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        HorizontalDivider(modifier = Modifier.weight(1f))
    }

    OutlinedTextField(
        value = uiState.fileUrl,
        onValueChange = viewModel::updateFileUrl,
        label = { Text("File URL") },
        placeholder = { Text("https://drive.google.com/...") },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true,
        enabled = enabled,
        supportingText = if (!enabled) {
            { Text("Remove selected files to use a link instead") }
        } else null
    )

    OutlinedTextField(
        value = uiState.thumbnailUrl,
        onValueChange = viewModel::updateThumbnailUrl,
        label = { Text("Thumbnail URL") },
        placeholder = { Text("https://... (optional cover image)") },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true
    )
}

@Composable
private fun AttributionCard(
    uiState: UploadFormState,
    viewModel: UploadViewModel
) {
    NebCard(
        shape = RoundedCornerShape(20.dp),
        containerColor = MaterialTheme.colorScheme.surfaceContainerLow,
        border = null
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            UploadSectionHeader(
                icon = Icons.Filled.Person,
                title = "Attribution"
            )

            OutlinedTextField(
                value = uiState.authorName,
                onValueChange = viewModel::updateAuthorName,
                label = { Text("Author / Credit") },
                placeholder = { Text("e.g. Prof. Sharma, Curriculum Board") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedTextField(
                    value = uiState.sourceLabel,
                    onValueChange = viewModel::updateSourceLabel,
                    label = { Text("Source Label") },
                    placeholder = { Text("e.g. Curriculum Board") },
                    modifier = Modifier.weight(1f),
                    singleLine = true
                )
                OutlinedTextField(
                    value = uiState.sourceUrl,
                    onValueChange = viewModel::updateSourceUrl,
                    label = { Text("Source URL") },
                    placeholder = { Text("https://...") },
                    modifier = Modifier.weight(1f),
                    singleLine = true
                )
            }
        }
    }
}

@Composable
private fun SubmitFooter(
    uiState: UploadFormState,
    onSubmit: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(20.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = "Your upload will be reviewed before being published.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f)
                )
            }

            Button(
                onClick = onSubmit,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp),
                shape = CircleShape,
                enabled = !uiState.isSubmitting,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                )
            ) {
                if (uiState.isSubmitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(22.dp),
                        color = MaterialTheme.colorScheme.onPrimary,
                        strokeWidth = 2.dp
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = if (uiState.selectedFiles.size > 1)
                            "Uploading ${((uiState.uploadProgress * uiState.selectedFiles.size).toInt() + 1)}/${uiState.selectedFiles.size}..."
                        else "Uploading...",
                        fontWeight = FontWeight.SemiBold
                    )
                } else {
                    Icon(
                        imageVector = Icons.Filled.CloudUpload,
                        contentDescription = null,
                        modifier = Modifier.size(22.dp)
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text("Submit for Review", fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}

private fun String.asCsvList(): List<String> =
    split(",").map { it.trim() }.filter { it.isNotBlank() }
