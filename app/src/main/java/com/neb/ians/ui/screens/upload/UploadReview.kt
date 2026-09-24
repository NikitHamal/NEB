@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.layout.ExperimentalLayoutApi::class
)

package com.neb.ians.ui.screens.upload

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Description
import androidx.compose.material.icons.rounded.Link
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone

/**
 * The last look before it goes.
 *
 * Nothing new is asked for here — it is the resource as the library will show
 * it, so the mistake worth catching (wrong subject, wrong level, a title still
 * reading IMG_2043) is the thing the eye lands on first.
 */
@Composable
fun UploadReviewStep(
    state: UploadFormState,
    onEditBasics: () -> Unit,
    onEditDetails: () -> Unit,
    modifier: Modifier = Modifier
) {
    val cover: Any? = state.thumbnailUri
        ?: state.thumbnailUrl.takeIf { it.isNotBlank() }
        ?: state.selectedFiles.firstOrNull { it.isImage }?.uri

    val shape = RoundedCornerShape(24.dp)

    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(shape)
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
                .padding(14.dp),
            horizontalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Box(
                modifier = Modifier
                    .width(74.dp)
                    .height(98.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                contentAlignment = Alignment.Center
            ) {
                if (cover != null) {
                    AsyncImage(
                        model = cover,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Icon(
                        imageVector = if (state.fileUrl.isNotBlank()) Icons.Rounded.Link else Icons.Rounded.Description,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(26.dp)
                    )
                }
            }
            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(
                    text = state.title.ifBlank { "Untitled" },
                    style = MaterialTheme.typography.titleMediumEmphasized,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    (state.subject.asCsvList() + listOfNotNull(state.gradeLevel.takeIf { it.isNotBlank() }))
                        .take(5)
                        .forEach { ReviewPill(it) }
                }
                Text(
                    text = fileLine(state),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }

        ReviewFacts(state)

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NebButton(
                text = "Edit basics",
                onClick = onEditBasics,
                tone = NebButtonTone.Outlined,
                size = NebButtonSize.Small,
                modifier = Modifier.weight(1f)
            )
            NebButton(
                text = "Edit details",
                onClick = onEditDetails,
                tone = NebButtonTone.Outlined,
                size = NebButtonSize.Small,
                modifier = Modifier.weight(1f)
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(
                imageVector = Icons.Rounded.Lock,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(15.dp)
            )
            Text(
                text = "A moderator reads every upload before it reaches the library.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
private fun ReviewFacts(state: UploadFormState) {
    val facts = buildList {
        add("Type" to state.type.ifBlank { "PDF" })
        if (state.examType.isNotBlank()) add("Exam" to state.examType)
        if (state.pradesh.isNotBlank()) add("Province" to state.pradesh)
        if (state.school.isNotBlank()) add("School" to state.school)
        if (state.year.isNotBlank()) add("Year" to state.year)
        if (state.tags.isNotBlank()) add("Tags" to state.tags)
        if (state.authorName.isNotBlank()) add("Original author" to state.authorName)
        add("Price" to if (state.isPaid) "Rs. ${state.price.ifBlank { "0" }}" else "Free")
    }

    val shape = RoundedCornerShape(24.dp)
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(horizontal = 16.dp, vertical = 6.dp)
    ) {
        facts.forEachIndexed { index, (label, value) ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 10.dp),
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.width(110.dp)
                )
                Text(
                    text = value,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.weight(1f)
                )
            }
            if (index != facts.lastIndex) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(1.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f))
                )
            }
        }
    }
}

@Composable
private fun ReviewPill(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelLarge,
        color = MaterialTheme.colorScheme.onSurface,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .padding(horizontal = 10.dp, vertical = 4.dp)
    )
}

private fun fileLine(state: UploadFormState): String {
    val files = state.selectedFiles
    return when {
        files.isEmpty() && state.fileUrl.isNotBlank() -> state.fileUrl
        files.isEmpty() && state.currentFileLabel.isNotBlank() -> state.currentFileLabel
        files.isEmpty() -> "No file attached"
        state.willCombine -> "${files.size} pages, published as one PDF"
        files.size == 1 -> "${files.first().name}  —  ${formatFileSize(files.first().size)}"
        else -> "${files.size} files  —  ${formatFileSize(files.sumOf { it.size })}"
    }
}
