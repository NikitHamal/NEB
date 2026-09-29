@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Payments
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.NebPriceField
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.nebBorderSubtle

/* The studio's Courses tab: the course list, the editor form behind it and
 * the price control the web studio shares. The shared studio widgets it draws
 * with live in CreatorStudioContent.kt. */

internal fun LazyListScope.studioCoursesTab(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    item(key = "course_list") {
        StudioCard {
            NebSectionLabel("Your offerings")
            NebFieldHint("Paid courses and classes, plus the free ones. Buyers check out by QR on your page.")
            if (uiState.courses.isEmpty()) {
                NebEmptyState(
                    icon = Icons.Outlined.Payments,
                    title = "No offerings yet",
                    subtitle = "Add your first course below — a title and a price are enough to start."
                )
            } else {
                uiState.courses.forEach { course ->
                    CourseStudioRow(
                        course = course,
                        onEdit = { viewModel.editCourse(course) },
                        onDelete = { viewModel.deleteCourse(course.id) }
                    )
                    HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
                }
            }
        }
    }

    item(key = "course_form") {
        val draft = uiState.courseDraft
        StudioCard {
            NebSectionLabel(if (draft.id.isBlank()) "New offering" else "Edit offering")
            NebAuthField(draft.title, { value -> viewModel.updateCourseDraft { it.copy(title = value) } }, "Title")
            NebAuthField(
                draft.summary,
                { value -> viewModel.updateCourseDraft { it.copy(summary = value) } },
                "One-line summary"
            )
            NebAuthField(
                draft.description,
                { value -> viewModel.updateCourseDraft { it.copy(description = value) } },
                "Description",
                singleLine = false,
                minHeight = 108.dp
            )

            NebPriceField(
                isPaid = draft.isPaid,
                price = draft.price,
                onIsPaidChange = { paid -> viewModel.updateCourseDraft { it.copy(isPaid = paid) } },
                onPriceChange = { value -> viewModel.updateCourseDraft { it.copy(price = value) } },
                commissionPercent = uiState.commissionPercent,
                title = "Price this offering",
                subtitle = "Free offerings show in the marketplace for everyone. Paid ones check out by QR, and your share lands in your wallet once verified."
            )

            NebAuthField(draft.level, { value -> viewModel.updateCourseDraft { it.copy(level = value) } }, "Level")
            NebAuthField(
                draft.durationLabel,
                { value -> viewModel.updateCourseDraft { it.copy(durationLabel = value) } },
                "Duration"
            )
            NebAuthField(
                draft.lessonCount,
                { value -> viewModel.updateCourseDraft { it.copy(lessonCount = value.filter { c -> c.isDigit() }) } },
                "Lessons",
                keyboardType = KeyboardType.Number
            )
            NebAuthField(
                draft.seatLimit,
                { value -> viewModel.updateCourseDraft { it.copy(seatLimit = value.filter { c -> c.isDigit() }) } },
                "Seats (0 = unlimited)",
                keyboardType = KeyboardType.Number
            )
            NebAuthField(
                draft.includes,
                { value -> viewModel.updateCourseDraft { it.copy(includes = value) } },
                "What's included (one per line)",
                singleLine = false,
                minHeight = 88.dp
            )
            NebAuthField(draft.tags, { value -> viewModel.updateCourseDraft { it.copy(tags = value) } }, "Tags")
            NebAuthField(
                draft.coverUrl,
                { value -> viewModel.updateCourseDraft { it.copy(coverUrl = value) } },
                "Cover image URL",
                keyboardType = KeyboardType.Uri
            )
            NebSectionLabel("Status")
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("draft", "published", "archived").forEach { status ->
                    NebChip(
                        label = status.replaceFirstChar { it.uppercase() },
                        selected = draft.status == status,
                        onClick = { viewModel.updateCourseDraft { it.copy(status = status) } }
                    )
                }
            }
            NebToggleRow(
                title = "Feature this offering",
                subtitle = "Featured offerings sort first in the marketplace",
                checked = draft.featured,
                onCheckedChange = { value -> viewModel.updateCourseDraft { it.copy(featured = value) } }
            )

            if (uiState.resourceOptions.isNotEmpty()) {
                NebSectionLabel("Attach your library resources")
                uiState.resourceOptions.take(12).forEach { (id, title) ->
                    val selected = draft.resourceIds.contains(id)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(WebCardShape)
                            .clickable {
                                viewModel.updateCourseDraft { current ->
                                    current.copy(
                                        resourceIds = if (selected) {
                                            current.resourceIds - id
                                        } else {
                                            current.resourceIds + id
                                        }
                                    )
                                }
                            }
                            .padding(horizontal = 10.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(18.dp)
                                .clip(CircleShape)
                                .background(
                                    if (selected) {
                                        MaterialTheme.colorScheme.onSurface
                                    } else {
                                        MaterialTheme.colorScheme.surfaceContainerHigh
                                    }
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            if (selected) {
                                Icon(
                                    imageVector = Icons.Filled.Check,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.surface,
                                    modifier = Modifier.size(12.dp)
                                )
                            }
                        }
                        Text(
                            text = title,
                            style = MaterialTheme.typography.bodySmall,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                NebButton(
                    text = if (draft.id.isBlank()) "Save offering" else "Save changes",
                    onClick = viewModel::saveCourse,
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Standard,
                    loading = uiState.isSavingCourse
                )
                if (draft.id.isNotBlank()) {
                    NebButton(
                        text = "Start a new one",
                        onClick = viewModel::newCourse,
                        tone = NebButtonTone.Text,
                        size = NebButtonSize.Standard
                    )
                }
            }
        }
    }
}

@Composable
internal fun CourseStudioRow(course: ApiCreatorCourse, onEdit: () -> Unit, onDelete: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = course.title,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = listOf(
                    if (course.isFree) "Free" else "Rs. ${course.price}",
                    course.status.replaceFirstChar { it.uppercase() },
                    if (course.saleCount > 0) "${course.saleCount} sold" else null
                ).filterNotNull().joinToString(" · "),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        NebButton(
            text = "Edit",
            onClick = onEdit,
            tone = NebButtonTone.Text,
            size = NebButtonSize.Small
        )
        IconButton(onClick = onDelete) {
            Icon(
                imageVector = Icons.Outlined.Delete,
                contentDescription = "Delete offering",
                tint = MaterialTheme.colorScheme.error,
                modifier = Modifier.size(18.dp)
            )
        }
    }
}
