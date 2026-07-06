package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Article
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.School
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.R
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiSyllabusCategory
import com.neb.ians.data.api.ApiSyllabusChapter
import com.neb.ians.data.api.ApiSyllabusNavItem
import com.neb.ians.data.api.ApiSyllabusQaItem
import com.neb.ians.data.api.ApiSyllabusSubject
import com.neb.ians.data.api.ApiSyllabusSubjectDetailResponse
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebResourceCard

@Composable
fun SyllabusContent(
    uiState: LibraryUiState,
    onRetry: () -> Unit,
    onOpenSubject: (String, ApiSyllabusSubject) -> Unit,
    onCloseSubject: () -> Unit,
    onSwitchGrade: (ApiSyllabusNavItem) -> Unit,
    onSwitchSubject: (ApiSyllabusNavItem) -> Unit,
    onResourceClick: (String) -> Unit
) {
    when {
        uiState.isSyllabusSubjectLoading -> SyllabusDetailLoading()
        uiState.syllabusSubjectError != null && uiState.selectedSyllabusDetail == null -> {
            ErrorCard(
                message = uiState.syllabusSubjectError ?: "Failed to load syllabus",
                onRetry = {
                    val gradeSlug = uiState.selectedSyllabusGradeSlug
                    val subjectSlug = uiState.selectedSyllabusSubjectSlug
                    if (gradeSlug != null && subjectSlug != null) {
                        onSwitchSubject(ApiSyllabusNavItem(uiState.selectedSyllabusDetail?.subject.orEmpty(), subjectSlug))
                    } else {
                        onRetry()
                    }
                },
                modifier = Modifier.padding(16.dp)
            )
        }
        uiState.selectedSyllabusDetail != null -> {
            SyllabusSubjectDetail(
                detail = uiState.selectedSyllabusDetail,
                error = uiState.syllabusSubjectError,
                onBack = onCloseSubject,
                onSwitchGrade = onSwitchGrade,
                onSwitchSubject = onSwitchSubject,
                onRetry = {
                    onSwitchSubject(
                        ApiSyllabusNavItem(
                            name = uiState.selectedSyllabusDetail.subject,
                            slug = uiState.selectedSyllabusSubjectSlug ?: uiState.selectedSyllabusDetail.subjectSlug
                        )
                    )
                },
                onResourceClick = onResourceClick
            )
        }
        else -> SyllabusCategoryList(
            uiState = uiState,
            onRetry = onRetry,
            onOpenSubject = onOpenSubject
        )
    }
}

@Composable
private fun SyllabusDetailLoading() {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(4) {
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(96.dp),
                shape = WebPanelShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(modifier = Modifier.size(26.dp), strokeWidth = 2.dp)
                }
            }
        }
    }
}

@Composable
private fun SyllabusCategoryList(
    uiState: LibraryUiState,
    onRetry: () -> Unit,
    onOpenSubject: (String, ApiSyllabusSubject) -> Unit
) {
    val categories = uiState.syllabusCategories.ifEmpty {
        LibraryUiState.GRADE_LEVELS.mapIndexed { index, grade ->
            ApiSyllabusCategory(
                grade = grade.replace("Grade", "Class"),
                order = index,
                subjects = LibraryUiState.SUBJECTS.map { ApiSyllabusSubject(name = it) }
            )
        }
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item(key = "syllabus_intro") {
            SyllabusIntroCard(isLoading = uiState.isSyllabusLoading)
        }
        if (uiState.syllabusError != null) {
            item(key = "syllabus_error") {
                ErrorCard(
                    message = "Using cached syllabus while the latest syllabus loads.",
                    onRetry = onRetry
                )
            }
        }
        items(categories, key = { it.grade }) { category ->
            SyllabusAccordionCard(
                category = category,
                initiallyExpanded = category == categories.firstOrNull(),
                onSubjectClick = { subject -> onOpenSubject(category.grade, subject) }
            )
        }
        item(key = "bottom_spacer") { Spacer(modifier = Modifier.height(92.dp)) }
    }
}

@Composable
private fun SyllabusIntroCard(isLoading: Boolean) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.10f), WebPillShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.School,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(22.dp)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "NEB syllabus by class",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.ExtraBold
                )
                Text(
                    text = "Browse class-wise subjects, open chapters, solved Q&As and matching study files.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            if (isLoading) {
                CircularProgressIndicator(modifier = Modifier.size(22.dp), strokeWidth = 2.dp)
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SyllabusAccordionCard(
    category: ApiSyllabusCategory,
    initiallyExpanded: Boolean,
    onSubjectClick: (ApiSyllabusSubject) -> Unit
) {
    var expanded by remember(category.grade) { mutableStateOf(initiallyExpanded) }
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { expanded = !expanded }
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .padding(horizontal = 16.dp, vertical = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.MenuBook,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = category.grade.ifBlank { "Syllabus" },
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.ExtraBold,
                    modifier = Modifier.weight(1f),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.primary.copy(alpha = 0.10f)) {
                    Text(
                        text = "${category.subjects.size} subjects",
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp)
                    )
                }
                Icon(
                    imageVector = Icons.Outlined.ExpandMore,
                    contentDescription = if (expanded) "Collapse" else "Expand",
                    modifier = Modifier.rotate(if (expanded) 180f else 0f),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (expanded) {
                FlowRow(
                    modifier = Modifier.padding(14.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    category.subjects.forEach { subject ->
                        SyllabusSubjectChip(
                            subject = subject.name,
                            onClick = { onSubjectClick(subject) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun SyllabusSubjectChip(subject: String, onClick: () -> Unit) {
    Surface(
        modifier = Modifier.clickable(onClick = onClick),
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Text(
            text = subject,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurface,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}
