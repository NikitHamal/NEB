@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.upload

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.material.icons.rounded.Assignment
import androidx.compose.material.icons.rounded.Category
import androidx.compose.material.icons.rounded.Description
import androidx.compose.material.icons.rounded.Image
import androidx.compose.material.icons.rounded.LocalOffer
import androidx.compose.material.icons.rounded.Public
import androidx.compose.material.icons.rounded.School
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebSelectField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.art.NebStateArt
import com.neb.ians.ui.components.art.NebStateKind
import com.neb.ians.ui.components.nebPressable

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
    onOpenLevelPicker: () -> Unit,
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

        NebSelectField(
            label = "Subject",
            values = state.subject.asCsvList(),
            placeholder = "Choose one or more",
            icon = Icons.Rounded.Category,
            onClick = onOpenSubjectPicker,
            isError = state.subjectError != null,
            errorText = "Pick at least one subject"
        )

        NebSelectField(
            label = "Level",
            values = listOfNotNull(state.gradeLevel.takeIf { it.isNotBlank() }),
            placeholder = "Class 11, Bachelor, your own…",
            icon = Icons.Rounded.School,
            onClick = onOpenLevelPicker
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
                    color = MaterialTheme.colorScheme.onSurface,
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
 * Its own step, after the upload is already valid, so the screen can be left at
 * any point without losing the thing the user came to do. The step ends in Skip
 * until something here is filled in, and in Next once something is.
 */
@Composable
fun UploadMoreDetails(
    state: UploadFormState,
    viewModel: UploadViewModel,
    onOpenTagPicker: () -> Unit,
    onOpenTypePicker: () -> Unit,
    onOpenExamPicker: () -> Unit,
    onOpenProvincePicker: () -> Unit,
    onPickCover: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        NebSectionLabel(text = "What is inside")
        UploadTextField(
            value = state.description,
            onValueChange = viewModel::updateDescription,
            label = "Description",
            placeholder = "What is inside, in a line or two",
            singleLine = false,
            minLines = 3
        )
        NebSelectField(
            label = "Type",
            values = listOfNotNull(state.type.takeIf { it.isNotBlank() }),
            placeholder = "PDF, note, video…",
            icon = Icons.Rounded.Description,
            onClick = onOpenTypePicker
        )
        NebSelectField(
            label = "Tags",
            values = state.tags.asCsvList(),
            placeholder = "Helps people find this",
            icon = Icons.Rounded.LocalOffer,
            onClick = onOpenTagPicker
        )

        Spacer(modifier = Modifier.height(4.dp))
        NebSectionLabel(text = "Where it comes from")
        NebSelectField(
            label = "Exam",
            values = listOfNotNull(state.examType.takeIf { it.isNotBlank() }),
            placeholder = "Any",
            icon = Icons.Rounded.Assignment,
            onClick = onOpenExamPicker
        )
        NebSelectField(
            label = "Province",
            values = listOfNotNull(state.pradesh.takeIf { it.isNotBlank() }),
            placeholder = "Any",
            icon = Icons.Rounded.Public,
            onClick = onOpenProvincePicker
        )
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

        Spacer(modifier = Modifier.height(4.dp))
        NebSectionLabel(text = "How it looks and what it costs")
        CoverRow(state = state, onPickCover = onPickCover)

        val sellShape = RoundedCornerShape(20.dp)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(sellShape)
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, sellShape)
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

@Composable
private fun CoverRow(state: UploadFormState, onPickCover: () -> Unit) {
    val cover: Any? = state.thumbnailUri ?: state.thumbnailUrl.takeIf { it.isNotBlank() }
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        NebSelectField(
            label = "Cover image",
            values = listOfNotNull(if (cover != null) "Chosen" else null),
            placeholder = if (state.willCombine) "First page is used automatically" else "Optional",
            icon = Icons.Rounded.Image,
            onClick = onPickCover
        )
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
        NebStateArt(kind = NebStateKind.Success, height = 150.dp)
        Spacer(Modifier.height(20.dp))
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
