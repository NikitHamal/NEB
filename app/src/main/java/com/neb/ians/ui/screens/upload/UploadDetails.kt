@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.upload

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebSpatialSpec

/**
 * The two answers that actually matter.
 *
 * Everything else about a resource can be inferred, defaulted or left out, so
 * only the title and the subject are asked for up front — and both usually
 * arrive already filled in, from the filename and from the last upload.
 */
@Composable
fun UploadEssentials(
    state: UploadFormState,
    viewModel: UploadViewModel,
    onOpenSubjectPicker: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        UploadTextField(
            value = state.title,
            onValueChange = viewModel::updateTitle,
            label = "Title",
            placeholder = "Physics chapter 4 notes",
            error = state.titleError
        )

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(onClick = onOpenSubjectPicker)
                .clip(RoundedCornerShape(18.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .padding(horizontal = 14.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Text(
                    text = "Subject",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = state.subject.ifBlank { "Choose one or more" },
                    style = MaterialTheme.typography.bodyLarge,
                    color = if (state.subject.isBlank()) {
                        MaterialTheme.colorScheme.onSurfaceVariant
                    } else {
                        MaterialTheme.colorScheme.onSurface
                    },
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            if (state.subjectError != null) {
                Text(
                    text = "Required",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.error
                )
            }
        }

        UploadPicker(
            label = "Level",
            value = state.gradeLevel,
            options = UploadOptions.GRADE_LEVELS,
            onSelect = viewModel::updateGradeLevel,
            placeholder = "Class 11, Bachelor, …"
        )

        AnimatedVisibility(visible = state.reusedDefaults) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Filled in from your last upload.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f)
                )
                Text(
                    text = "Clear",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier
                        .nebPressable(onClick = viewModel::clearReusedDefaults)
                        .clip(CircleShape)
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                )
            }
        }
    }
}

/**
 * Everything the library would like but nobody has to supply.
 *
 * Folded away by default. The old wizard spent three of its five steps here,
 * which taught people that uploading is long when almost all of it is optional.
 */
@Composable
fun UploadMoreDetails(
    state: UploadFormState,
    viewModel: UploadViewModel,
    expanded: Boolean,
    onToggle: () -> Unit,
    onOpenTagPicker: () -> Unit,
    onPickCover: () -> Unit,
    modifier: Modifier = Modifier
) {
    val chevron by animateFloatAsState(
        targetValue = if (expanded) 180f else 0f,
        animationSpec = nebSpatialSpec(),
        label = "upload_more_chevron"
    )

    Column(
        modifier = modifier
            .fillMaxWidth()
            .animateContentSize(animationSpec = nebSpatialSpec()),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(onClick = onToggle)
                .clip(RoundedCornerShape(18.dp))
                .padding(vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Text("More details", style = MaterialTheme.typography.titleSmallEmphasized)
                Text(
                    text = "Description, tags, source, price — all optional",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Icon(
                imageVector = Icons.Rounded.ExpandMore,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.rotate(chevron)
            )
        }

        if (expanded) {
            UploadTextField(
                value = state.description,
                onValueChange = viewModel::updateDescription,
                label = "Description",
                placeholder = "What is inside, in a line or two",
                singleLine = false,
                minLines = 3
            )
            UploadPicker(
                label = "Type",
                value = state.type,
                options = UploadOptions.RESOURCE_TYPES,
                onSelect = viewModel::updateType,
                allowClear = false
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                UploadPicker(
                    label = "Exam",
                    value = state.examType,
                    options = UploadOptions.EXAM_TYPES,
                    onSelect = viewModel::updateExamType,
                    modifier = Modifier.weight(1f),
                    placeholder = "Any"
                )
                UploadPicker(
                    label = "Province",
                    value = state.pradesh,
                    options = UploadOptions.PROVINCES,
                    onSelect = viewModel::updatePradesh,
                    modifier = Modifier.weight(1f),
                    placeholder = "Any"
                )
            }
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                UploadTextField(
                    value = state.school,
                    onValueChange = viewModel::updateSchool,
                    label = "School",
                    modifier = Modifier.weight(1f)
                )
                UploadTextField(
                    value = state.year,
                    onValueChange = viewModel::updateYear,
                    label = "Year",
                    modifier = Modifier.weight(1f),
                    keyboardType = KeyboardType.Number
                )
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .nebPressable(onClick = onOpenTagPicker)
                    .clip(RoundedCornerShape(18.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .padding(horizontal = 14.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(Modifier.weight(1f)) {
                    Text(
                        text = "Tags",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = state.tags.ifBlank { "Helps people find this" },
                        style = MaterialTheme.typography.bodyLarge,
                        color = if (state.tags.isBlank()) {
                            MaterialTheme.colorScheme.onSurfaceVariant
                        } else {
                            MaterialTheme.colorScheme.onSurface
                        },
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }

            UploadTextField(
                value = state.authorName,
                onValueChange = viewModel::updateAuthorName,
                label = "Original author",
                placeholder = "Credit whoever made it",
                supporting = "Leave blank if this is your own work"
            )
            UploadTextField(
                value = state.sourceUrl,
                onValueChange = viewModel::updateSourceUrl,
                label = "Source link",
                keyboardType = KeyboardType.Uri
            )

            CoverRow(state = state, onPickCover = onPickCover)

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(18.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .padding(horizontal = 14.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Column(Modifier.weight(1f)) {
                    Text("Sell this resource", style = MaterialTheme.typography.bodyLarge)
                    Text(
                        text = "Buyers pay once, you keep the credit",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(checked = state.isPaid, onCheckedChange = viewModel::updateIsPaid)
            }
            AnimatedVisibility(visible = state.isPaid) {
                UploadTextField(
                    value = state.price,
                    onValueChange = viewModel::updatePrice,
                    label = "Price (Rs.)",
                    keyboardType = KeyboardType.Number
                )
            }
        }
    }
}

@Composable
private fun CoverRow(state: UploadFormState, onPickCover: () -> Unit) {
    val cover: Any? = state.thumbnailUri ?: state.thumbnailUrl.takeIf { it.isNotBlank() }
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(onClick = onPickCover)
                .clip(RoundedCornerShape(18.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .padding(horizontal = 14.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Text(
                    text = "Cover image",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = when {
                        cover != null -> "Chosen"
                        state.willCombine -> "First page is used automatically"
                        else -> "Optional"
                    },
                    style = MaterialTheme.typography.bodyLarge
                )
            }
        }
        CoverPreview(model = state.thumbnailUri)
    }
}

/** Link uploads — one field, only shown when the user asked for it. */
@Composable
fun UploadLinkField(state: UploadFormState, viewModel: UploadViewModel, modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        UploadTextField(
            value = state.fileUrl,
            onValueChange = viewModel::updateFileUrl,
            label = "Link to the resource",
            placeholder = "https://…",
            keyboardType = KeyboardType.Uri,
            error = state.fileError
        )
    }
}

@Composable
fun UploadSuccessScreen(onUploadAnother: () -> Unit, onBrowseLibrary: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(84.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Rounded.Check,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.size(40.dp)
            )
        }
        Spacer(Modifier.height(24.dp))
        Text(
            text = "Sent for review",
            style = MaterialTheme.typography.headlineSmallEmphasized,
            textAlign = TextAlign.Center,
            maxLines = 1
        )
        Spacer(Modifier.height(8.dp))
        Text(
            text = "A moderator checks every upload before it reaches the library. Yours will appear once it passes.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
        Spacer(Modifier.height(28.dp))
        NebButton(
            text = "Upload another",
            onClick = onUploadAnother,
            icon = Icons.Rounded.Add,
            size = NebButtonSize.Hero
        )
        Spacer(Modifier.height(8.dp))
        NebButton(
            text = "Browse library",
            onClick = onBrowseLibrary,
            tone = NebButtonTone.Text
        )
    }
}
