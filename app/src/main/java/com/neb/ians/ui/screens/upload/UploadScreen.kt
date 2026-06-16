package com.neb.ians.ui.screens.upload

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CloudUpload
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@OptIn(ExperimentalMaterial3Api::class)
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
        }
    }

    if (uiState.submitSuccess) {
        UploadSuccessScreen(
            onUploadAnother = {
                viewModel.resetSuccess()
            },
            onBrowseLibrary = onUploadSuccess
        )
        return
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.surface
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Top bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(start = 4.dp, end = 16.dp, top = 4.dp, bottom = 4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                }
                Text(
                    text = "Share a Resource",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
            }

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(
                    text = "Help fellow learners by sharing study materials. Your contribution will be reviewed before publishing.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    lineHeight = 20.sp
                )

                // Errors
                if (uiState.submitError != null) {
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = MaterialTheme.colorScheme.errorContainer,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = uiState.submitError ?: "",
                            color = MaterialTheme.colorScheme.onErrorContainer,
                            style = MaterialTheme.typography.bodySmall,
                            modifier = Modifier.padding(12.dp)
                        )
                    }
                }

                UploadSectionHeader(icon = Icons.Filled.Description, title = "Basic Info")

                // Title
                OutlinedTextField(
                    value = uiState.title,
                    onValueChange = viewModel::updateTitle,
                    label = { Text("Title *") },
                    placeholder = { Text("e.g. Class 12 Computer Engineering — Final Exam 2081") },
                    isError = uiState.titleError != null,
                    supportingText = uiState.titleError?.let { { Text(it) } },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )

                // Subject
                SubjectField(
                    subject = uiState.subject,
                    onSubjectChange = viewModel::updateSubject,
                    error = uiState.subjectError,
                    onOpenPicker = { showSubjectPicker = true }
                )

                // Grade + Type row
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
                        label = "Type",
                        value = uiState.type,
                        options = UploadViewModel.RESOURCE_TYPES,
                        onValueChange = viewModel::updateType,
                        modifier = Modifier.weight(1f)
                    )
                }

                // Exam type (conditional)
                val showExamType = uiState.type in listOf("Past Paper", "Model Paper", "Guide", "Solution", "Note", "PDF")
                AnimatedVisibility(visible = showExamType) {
                    DropdownField(
                        label = "Exam Type",
                        value = uiState.examType,
                        options = UploadViewModel.EXAM_TYPES,
                        onValueChange = viewModel::updateExamType,
                        modifier = Modifier.fillMaxWidth()
                    )
                }

                // Description
                OutlinedTextField(
                    value = uiState.description,
                    onValueChange = viewModel::updateDescription,
                    label = { Text("Description") },
                    placeholder = { Text("Briefly describe this resource...") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    maxLines = 5
                )

                // Tags
                TagsField(
                    tags = uiState.tags,
                    onTagsChange = viewModel::updateTags,
                    onOpenPicker = { showTagPicker = true }
                )

                // More Details (collapsible)
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

                // Upload File section
                UploadSectionHeader(icon = Icons.Filled.CloudUpload, title = "Upload File")

                FileDropzone(
                    selectedFiles = uiState.selectedFiles,
                    fileError = uiState.fileError,
                    onPickFiles = { filePicker.launch("*/*") },
                    onRemoveFile = viewModel::removeFileAt,
                    onClearFiles = viewModel::clearFiles
                )

                // File URL (alternative)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Spacer(modifier = Modifier.weight(1f))
                    Surface(
                        shape = RoundedCornerShape(2.dp),
                        color = MaterialTheme.colorScheme.outlineVariant,
                        modifier = Modifier.weight(2f)
                    ) { Spacer(modifier = Modifier.height(1.dp)) }
                    Text(
                        text = "or paste a link",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 8.dp)
                    )
                    Surface(
                        shape = RoundedCornerShape(2.dp),
                        color = MaterialTheme.colorScheme.outlineVariant,
                        modifier = Modifier.weight(2f)
                    ) { Spacer(modifier = Modifier.height(1.dp)) }
                }

                Spacer(modifier = Modifier.height(4.dp))

                OutlinedTextField(
                    value = uiState.fileUrl,
                    onValueChange = viewModel::updateFileUrl,
                    label = { Text("File URL") },
                    placeholder = { Text("https://drive.google.com/... or https://...pdf") },
                    isError = uiState.fileError != null && uiState.selectedFiles.isEmpty() && uiState.fileUrl.isBlank(),
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    enabled = uiState.selectedFiles.isEmpty()
                )
                Text(
                    text = "Paste a direct link to the file. Google Drive, Dropbox, and direct links work.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(top = 2.dp)
                )

                Spacer(modifier = Modifier.height(8.dp))

                OutlinedTextField(
                    value = uiState.thumbnailUrl,
                    onValueChange = viewModel::updateThumbnailUrl,
                    label = { Text("Thumbnail URL") },
                    placeholder = { Text("https://... (optional cover image)") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )

                // Attribution section
                UploadSectionHeader(icon = Icons.Filled.Person, title = "Attribution")

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

                // Submit
                Spacer(modifier = Modifier.height(8.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Filled.Info,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Your upload will be reviewed before being published.",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.weight(1f)
                    )
                }

                Spacer(modifier = Modifier.height(8.dp))

                Button(
                    onClick = { viewModel.submit(context) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = CircleShape,
                    enabled = !uiState.isSubmitting,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.onPrimary
                    )
                ) {
                    if (uiState.isSubmitting) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            color = MaterialTheme.colorScheme.onPrimary,
                            strokeWidth = 2.dp
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = if (uiState.selectedFiles.size > 1)
                                "Uploading ${((uiState.uploadProgress * uiState.selectedFiles.size).toInt() + 1)}/${uiState.selectedFiles.size}..."
                            else "Uploading...",
                            fontWeight = FontWeight.SemiBold
                        )
                    } else {
                        Icon(Icons.Filled.CloudUpload, contentDescription = null, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Submit for Review", fontWeight = FontWeight.SemiBold)
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }

    if (showSubjectPicker) {
        ChipPickerDialog(
            title = "Select Subjects",
            items = UploadViewModel.SUBJECTS,
            selectedItems = if (uiState.subject.isNotBlank()) uiState.subject.split(",").map { it.trim() } else emptyList(),
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
            selectedItems = if (uiState.tags.isNotBlank()) uiState.tags.split(",").map { it.trim() } else emptyList(),
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