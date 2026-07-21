package com.neb.ians.ui.screens.upload

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
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
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.neb.ians.ui.components.NebCard
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebFilledButton
import com.neb.ians.ui.theme.getSubjectColor

@Composable
fun StepTitle(
    number: Int,
    title: String,
    subtitle: String,
    optional: Boolean = false
) {
    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "Step $number",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold,
                maxLines = 1
            )
            if (optional) {
                Spacer(modifier = Modifier.width(6.dp))
                Surface(
                    shape = RoundedCornerShape(4.dp),
                    color = MaterialTheme.colorScheme.secondaryContainer
                ) {
                    Text(
                        text = "OPTIONAL",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSecondaryContainer,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        modifier = Modifier.padding(horizontal = 5.dp, vertical = 1.dp)
                    )
                }
            }
        }
        Text(
            text = title,
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        Text(
            text = subtitle,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DropdownField(
    label: String,
    value: String,
    options: List<String>,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    placeholder: String? = null
) {
    var showDialog by remember { mutableStateOf(false) }

    val fieldShape = RoundedCornerShape(14.dp)
    val fieldColors = OutlinedTextFieldDefaults.colors(
        focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerLow,
        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerLow,
        disabledContainerColor = MaterialTheme.colorScheme.surfaceContainerLow,
        focusedBorderColor = MaterialTheme.colorScheme.primary,
        unfocusedBorderColor = MaterialTheme.colorScheme.outlineVariant,
        disabledBorderColor = MaterialTheme.colorScheme.outlineVariant,
        disabledTextColor = MaterialTheme.colorScheme.onSurface,
        disabledLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
        disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .clickable { showDialog = true }
    ) {
        OutlinedTextField(
            value = value.ifBlank { placeholder ?: "" },
            onValueChange = {},
            enabled = false,
            label = { Text(label, maxLines = 1, overflow = TextOverflow.Ellipsis) },
            trailingIcon = {
                Icon(
                    imageVector = Icons.Filled.ArrowDropDown,
                    contentDescription = null,
                    modifier = Modifier.size(20.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
            shape = fieldShape,
            colors = fieldColors,
            textStyle = MaterialTheme.typography.bodyMedium
        )
    }

    if (showDialog) {
        SelectionDialog(
            title = label,
            options = options,
            selectedValue = value,
            onDismiss = { showDialog = false },
            onSelect = {
                onValueChange(it)
                showDialog = false
            }
        )
    }
}

@Composable
fun SelectionDialog(
    title: String,
    options: List<String>,
    selectedValue: String,
    onDismiss: () -> Unit,
    onSelect: (String) -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false, dismissOnClickOutside = true)
    ) {
        Surface(
            shape = RoundedCornerShape(24.dp),
            color = MaterialTheme.colorScheme.surfaceContainerLowest,
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = title,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.weight(1f),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    IconButton(onClick = onDismiss, modifier = Modifier.size(36.dp)) {
                        Icon(
                            imageVector = Icons.Filled.Close,
                            contentDescription = "Close",
                            modifier = Modifier.size(22.dp)
                        )
                    }
                }

                LazyColumn(
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(max = 320.dp),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    items(options, key = { it }) { option ->
                        val selected = option == selectedValue
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(10.dp))
                                .clickable { onSelect(option) }
                                .padding(horizontal = 8.dp, vertical = 10.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            RadioButton(
                                selected = selected,
                                onClick = { onSelect(option) },
                                colors = RadioButtonDefaults.colors(
                                    selectedColor = MaterialTheme.colorScheme.primary,
                                    unselectedColor = MaterialTheme.colorScheme.outline
                                ),
                                modifier = Modifier.size(22.dp)
                            )
                            Text(
                                text = option.ifBlank { "—" },
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
                                color = if (selected) MaterialTheme.colorScheme.primary
                                else MaterialTheme.colorScheme.onSurface,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ResourceTypeChips(
    selected: String,
    options: List<String>,
    onSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        options.forEach { option ->
            NebChip(
                label = option,
                selected = option == selected,
                onClick = { onSelect(option) }
            )
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun AttributeChipRow(
    label: String,
    placeholder: String,
    values: List<String>,
    onRemove: (String) -> Unit,
    onAddClick: () -> Unit,
    modifier: Modifier = Modifier,
    error: String? = null,
    accentColor: Color? = null
) {
    val borderColor = accentColor?.copy(alpha = 0.5f) ?: MaterialTheme.colorScheme.outline
    val containerColor = accentColor?.copy(alpha = 0.08f) ?: MaterialTheme.colorScheme.surfaceContainerLowest

    NebCard(
        modifier = modifier.fillMaxWidth(),
        onClick = if (values.isEmpty()) onAddClick else null,
        shape = RoundedCornerShape(12.dp),
        containerColor = containerColor,
        border = BorderStroke(1.dp, borderColor)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
                .animateContentSize(),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelLarge,
                    color = if (error != null) MaterialTheme.colorScheme.error
                    else MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
                Text(
                    text = if (values.isEmpty()) placeholder else "${values.size} selected",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

            if (values.isNotEmpty()) {
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    values.forEach { value ->
                        SubjectChip(
                            label = value,
                            accentColor = accentColor,
                            onRemove = { onRemove(value) }
                        )
                    }
                    AddChip(onClick = onAddClick)
                }
            } else {
                AddChip(onClick = onAddClick)
            }

            if (error != null) {
                Text(
                    text = error,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.error,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SubjectChip(
    label: String,
    accentColor: Color?,
    onRemove: () -> Unit
) {
    val subjectColor = accentColor ?: getSubjectColor(label)
    val container = subjectColor.copy(alpha = 0.12f)
    Surface(
        shape = CircleShape,
        color = container,
        modifier = Modifier.height(32.dp)
    ) {
        Row(
            modifier = Modifier.padding(start = 12.dp, end = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Surface(
                shape = CircleShape,
                color = subjectColor,
                modifier = Modifier.size(8.dp)
            ) {}
            Text(
                text = label,
                style = MaterialTheme.typography.labelLarge,
                color = subjectColor.copy(alpha = 0.9f),
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Icon(
                imageVector = Icons.Filled.Clear,
                contentDescription = "Remove",
                tint = subjectColor.copy(alpha = 0.9f),
                modifier = Modifier
                    .size(24.dp)
                    .clip(CircleShape)
                    .clickable(onClick = onRemove)
                    .padding(4.dp)
            )
        }
    }
}

@Composable
private fun AddChip(onClick: () -> Unit) {
    Surface(
        shape = CircleShape,
        color = MaterialTheme.colorScheme.secondaryContainer,
        modifier = Modifier
            .height(32.dp)
            .clickable(onClick = onClick)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Icon(
                imageVector = Icons.Filled.Add,
                contentDescription = null,
                modifier = Modifier.size(16.dp),
                tint = MaterialTheme.colorScheme.onSecondaryContainer
            )
            Text(
                text = "Add",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSecondaryContainer,
                maxLines = 1
            )
        }
    }
}

@Composable
fun StepCard(content: @Composable ColumnScope.() -> Unit) {
    NebCard(
        shape = RoundedCornerShape(20.dp),
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .animateContentSize(),
            verticalArrangement = Arrangement.spacedBy(14.dp),
            content = content
        )
    }
}

@Composable
fun BasicsStep(
    uiState: UploadFormState,
    viewModel: UploadViewModel,
    onOpenSubjectPicker: () -> Unit
) {
    StepCard {
        StepTitle(
            number = 1,
            title = "Basics",
            subtitle = "Title, subject and type"
        )
        OutlinedTextField(
            value = uiState.title,
            onValueChange = viewModel::updateTitle,
            label = { Text("Title *", maxLines = 1) },
            placeholder = {
                Text(
                    "e.g. Class 12 Computer Final Exam 2081",
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            },
            isError = uiState.titleError != null,
            supportingText = uiState.titleError?.let { { Text(it, maxLines = 1) } },
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

        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(
                text = "Resource type",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1
            )
            ResourceTypeChips(
                selected = uiState.type,
                options = UploadViewModel.RESOURCE_TYPES,
                onSelect = viewModel::updateType
            )
        }

        GradeAndExamRow(uiState = uiState, viewModel = viewModel)
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
    DropdownField(
        label = "Level / Grade",
        value = uiState.gradeLevel,
        options = UploadViewModel.GRADE_LEVELS,
        onValueChange = viewModel::updateGradeLevel,
        modifier = Modifier.fillMaxWidth()
    )
    if (showExamType) {
        DropdownField(
            label = "Exam Type",
            value = uiState.examType,
            options = UploadViewModel.EXAM_TYPES,
            onValueChange = viewModel::updateExamType,
            modifier = Modifier.fillMaxWidth()
        )
    }
}

@Composable
fun FilesStep(
    uiState: UploadFormState,
    viewModel: UploadViewModel,
    onPickFiles: () -> Unit,
    onRemoveFile: (Int) -> Unit,
    onClearFiles: () -> Unit,
    onPickThumbnail: () -> Unit
) {
    StepCard {
        StepTitle(
            number = 2,
            title = "Files",
            subtitle = if (uiState.isEditMode) "Replace the file or change the link"
            else "Upload or paste a link"
        )
        if (uiState.isEditMode) {
            EditCurrentFileBanner(uiState)
        }
        FileDropzone(
            selectedFiles = uiState.selectedFiles,
            fileError = uiState.fileError,
            onPickFiles = onPickFiles,
            onRemoveFile = onRemoveFile,
            onClearFiles = onClearFiles
        )
        LinkAlternativeFields(uiState = uiState, viewModel = viewModel, onPickThumbnail = onPickThumbnail)
    }
}

/** Shown in edit mode: what is stored today and how replacing works. */
@Composable
private fun EditCurrentFileBanner(uiState: UploadFormState) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.45f),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.25f))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Icon(
                Icons.Outlined.Description,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(20.dp)
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Current: ${uiState.currentFileLabel}",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = "Keep it as-is, pick a replacement file below, or change the link. A blank link never deletes your file.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 3
                )
            }
        }
    }
}

@Composable
private fun LinkAlternativeFields(
    uiState: UploadFormState,
    viewModel: UploadViewModel,
    onPickThumbnail: () -> Unit
) {
    val enabled = uiState.selectedFiles.isEmpty()
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        HorizontalDivider(modifier = Modifier.weight(1f))
        Text(
            text = "or paste a link",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1
        )
        HorizontalDivider(modifier = Modifier.weight(1f))
    }
    OutlinedTextField(
        value = uiState.fileUrl,
        onValueChange = viewModel::updateFileUrl,
        label = { Text("File URL", maxLines = 1) },
        placeholder = {
            Text(
                "https://drive.google.com/...",
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true,
        enabled = enabled,
        supportingText = if (!enabled) {
            { Text("Remove selected files to use a link instead", maxLines = 1) }
        } else null
    )
    // ----- Cover image: manual upload wins; videos auto-capture a frame -----
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .clickable(onClick = onPickThumbnail),
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            if (uiState.thumbnailUri != null) {
                AsyncImage(
                    model = uiState.thumbnailUri,
                    contentDescription = "Cover image",
                    modifier = Modifier
                        .size(44.dp)
                        .clip(RoundedCornerShape(8.dp)),
                    contentScale = ContentScale.Crop
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        "Cover image selected",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1
                    )
                    Text(
                        "Tap to change",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1
                    )
                }
                androidx.compose.material3.IconButton(onClick = { viewModel.setThumbnail(null) }) {
                    Icon(
                        Icons.Filled.Close,
                        contentDescription = "Remove cover image",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            } else {
                Icon(
                    Icons.Outlined.Image,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(22.dp)
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        "Upload cover image (optional)",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        if (viewModel.hasAutoCoverCandidate()) "Leave empty — we'll capture one from your video"
                        else "JPG, PNG, WEBP or GIF, up to 10 MB",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2
                    )
                }
                Icon(
                    Icons.Filled.ChevronRight,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }

    OutlinedTextField(
        value = uiState.thumbnailUrl,
        onValueChange = viewModel::updateThumbnailUrl,
        label = { Text("Thumbnail URL (optional)", maxLines = 1) },
        placeholder = {
            Text(
                "https://... cover image",
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true,
        supportingText = { Text("Only used when no cover image is uploaded above", maxLines = 1) }
    )
}

@Composable
fun DetailsStep(
    uiState: UploadFormState,
    viewModel: UploadViewModel,
    onOpenTagPicker: () -> Unit
) {
    StepCard {
        StepTitle(
            number = 3,
            title = "Details",
            subtitle = "Description and tags",
            optional = true
        )
        OutlinedTextField(
            value = uiState.description,
            onValueChange = viewModel::updateDescription,
            label = { Text("Description", maxLines = 1) },
            placeholder = {
                Text(
                    "Briefly describe this resource...",
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            },
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

@Composable
fun AttributionStep(
    uiState: UploadFormState,
    viewModel: UploadViewModel
) {
    StepCard {
        StepTitle(
            number = 4,
            title = "Attribution",
            subtitle = "Credit the original source",
            optional = true
        )
        OutlinedTextField(
            value = uiState.authorName,
            onValueChange = viewModel::updateAuthorName,
            label = { Text("Author / Credit", maxLines = 1) },
            placeholder = {
                Text(
                    "e.g. Prof. Sharma, Curriculum Board",
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        OutlinedTextField(
            value = uiState.sourceLabel,
            onValueChange = viewModel::updateSourceLabel,
            label = { Text("Source Label", maxLines = 1) },
            placeholder = {
                Text(
                    "e.g. Curriculum Board",
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        OutlinedTextField(
            value = uiState.sourceUrl,
            onValueChange = viewModel::updateSourceUrl,
            label = { Text("Source URL", maxLines = 1) },
            placeholder = {
                Text("https://...", maxLines = 1, overflow = TextOverflow.Ellipsis)
            },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
    }
}

@Composable
fun ReviewStep(
    uiState: UploadFormState,
    onEdit: (Int) -> Unit
) {
    StepCard {
        StepTitle(
            number = 5,
            title = "Review",
            subtitle = "Confirm and submit"
        )
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            ReviewRow(label = "Title", value = uiState.title.ifBlank { "—" }, onEdit = { onEdit(0) })
            ReviewRow(label = "Subject", value = uiState.subject.ifBlank { "—" }, onEdit = { onEdit(0) })
            ReviewRow(label = "Type", value = uiState.type.ifBlank { "—" }, onEdit = { onEdit(0) })
            ReviewRow(label = "Grade", value = uiState.gradeLevel.ifBlank { "—" }, onEdit = { onEdit(0) })
            ReviewRow(
                label = "Files",
                value = when {
                    uiState.isEditMode && uiState.selectedFiles.isNotEmpty() ->
                        "Replace with ${uiState.selectedFiles.first().name}"
                    uiState.isEditMode && uiState.fileUrlDirty && uiState.fileUrl.isNotBlank() ->
                        "New link: ${uiState.fileUrl}"
                    uiState.isEditMode -> "Keep current (${uiState.currentFileLabel})"
                    uiState.selectedFiles.isNotEmpty() ->
                        "${uiState.selectedFiles.size} file${if (uiState.selectedFiles.size == 1) "" else "s"}"
                    else -> uiState.fileUrl.ifBlank { "—" }
                },
                onEdit = { onEdit(1) }
            )
            ReviewRow(label = "Description", value = uiState.description.ifBlank { "—" }, onEdit = { onEdit(2) })
            ReviewRow(label = "Tags", value = uiState.tags.ifBlank { "—" }, onEdit = { onEdit(2) })
            ReviewRow(label = "Author", value = uiState.authorName.ifBlank { "—" }, onEdit = { onEdit(3) })
        }
        Surface(
            shape = RoundedCornerShape(12.dp),
            color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f),
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
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = if (uiState.isEditMode)
                        "Saving changes sends this resource back to review. It reappears publicly once re-approved."
                    else "Your upload will be reviewed before being published.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun ReviewRow(
    label: String,
    value: String,
    onEdit: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(10.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                modifier = Modifier.width(80.dp)
            )
            Text(
                text = value,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f)
            )
            Icon(
                imageVector = Icons.Filled.Edit,
                contentDescription = "Edit",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .size(20.dp)
                    .clip(CircleShape)
                    .clickable(onClick = onEdit)
                    .padding(2.dp)
            )
        }
    }
}

@Composable
fun UploadSuccessScreen(
    onUploadAnother: () -> Unit,
    onBrowseLibrary: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Surface(
            shape = CircleShape,
            color = MaterialTheme.colorScheme.primaryContainer,
            modifier = Modifier.size(88.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Filled.Check,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(44.dp)
                )
            }
        }
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "Submitted for Review!",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center,
            maxLines = 1
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Your resource will be reviewed before being published. This helps keep resources high quality.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
            maxLines = 3,
            overflow = TextOverflow.Ellipsis
        )
        Spacer(modifier = Modifier.height(32.dp))
        NebFilledButton(
            text = "Upload Another",
            leadingIcon = Icons.Filled.Add,
            onClick = onUploadAnother
        )
        Spacer(modifier = Modifier.height(12.dp))
        TextButton(onClick = onBrowseLibrary) {
            Text(
                text = "Browse Library",
                fontWeight = FontWeight.SemiBold,
                style = MaterialTheme.typography.labelLarge,
                maxLines = 1
            )
        }
    }
}

fun formatFileSize(bytes: Long): String {
    if (bytes < 1024) return "$bytes B"
    if (bytes < 1024 * 1024) return "${(bytes / 1024.0).format(1)} KB"
    return "${(bytes / (1024.0 * 1024.0)).format(1)} MB"
}

private fun Double.format(digits: Int): String = String.format("%.${digits}f", this)
