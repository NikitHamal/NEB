package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Article
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
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
import com.neb.ians.data.api.ApiSyllabusChapter
import com.neb.ians.data.api.ApiSyllabusNavItem
import com.neb.ians.data.api.ApiSyllabusQaItem
import com.neb.ians.data.api.ApiSyllabusSubjectDetailResponse
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebResourceCard

@Composable
fun SyllabusSubjectDetail(
    detail: ApiSyllabusSubjectDetailResponse,
    error: String?,
    onBack: () -> Unit,
    onSwitchGrade: (ApiSyllabusNavItem) -> Unit,
    onSwitchSubject: (ApiSyllabusNavItem) -> Unit,
    onRetry: () -> Unit,
    onResourceClick: (String) -> Unit
) {
    val chapters = detail.chapters
    var selectedChapterId by rememberSaveable(detail.gradeSlug, detail.subjectSlug, chapters.size) {
        mutableStateOf(chapters.firstOrNull()?.id.orEmpty())
    }
    if (selectedChapterId.isBlank() && chapters.isNotEmpty()) selectedChapterId = chapters.first().id
    val selectedChapter = chapters.firstOrNull { it.id == selectedChapterId } ?: chapters.firstOrNull()

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item(key = "breadcrumbs") {
            SyllabusBreadcrumbs(
                detail = detail,
                onBack = onBack,
                onSwitchGrade = onSwitchGrade,
                onSwitchSubject = onSwitchSubject
            )
        }
        if (error != null) {
            item(key = "detail_error") {
                ErrorCard(message = error, onRetry = onRetry)
            }
        }
        item(key = "subject_title") {
            SyllabusSubjectHeader(detail = detail)
        }
        if (chapters.isNotEmpty()) {
            item(key = "chapter_picker") {
                ChapterPicker(
                    chapters = chapters,
                    selectedChapterId = selectedChapterId,
                    onSelect = { selectedChapterId = it }
                )
            }
            selectedChapter?.let { chapter ->
                item(key = "viewer_${chapter.id}") {
                    ChapterViewer(
                        chapter = chapter,
                        onResourceClick = onResourceClick
                    )
                }
            }
        } else {
            item(key = "empty_detail") {
                WebEmptyState(
                    title = "No chapters found",
                    message = "This subject is mapped, but detailed syllabus content has not been added yet.",
                    icon = painterResource(id = R.drawable.ic_document),
                    modifier = Modifier.padding(top = 16.dp)
                )
            }
        }
        item(key = "bottom_spacer") { Spacer(modifier = Modifier.height(92.dp)) }
    }
}

@Composable
private fun SyllabusBreadcrumbs(
    detail: ApiSyllabusSubjectDetailResponse,
    onBack: () -> Unit,
    onSwitchGrade: (ApiSyllabusNavItem) -> Unit,
    onSwitchSubject: (ApiSyllabusNavItem) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState()),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        BreadcrumbLink(text = "Digital Library", onClick = onBack)
        BreadcrumbSeparator()
        BreadcrumbLink(text = "Syllabus", onClick = onBack)
        BreadcrumbSeparator()
        BreadcrumbDropdown(
            label = detail.grade.ifBlank { "Class" },
            menuLabel = "Switch Class",
            items = detail.gradeList,
            activeName = detail.grade,
            onSelect = onSwitchGrade
        )
        BreadcrumbSeparator()
        BreadcrumbDropdown(
            label = detail.subject.ifBlank { "Subject" },
            menuLabel = "Switch Subject",
            items = detail.subjectList,
            activeName = detail.subject,
            onSelect = onSwitchSubject
        )
    }
}

@Composable
private fun BreadcrumbLink(text: String, onClick: () -> Unit) {
    Text(
        text = text,
        modifier = Modifier.clickable(onClick = onClick),
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.primary,
        fontWeight = FontWeight.SemiBold,
        maxLines = 1
    )
}

@Composable
private fun BreadcrumbSeparator() {
    Text(
        text = "/",
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.outlineVariant,
        fontWeight = FontWeight.SemiBold
    )
}

@Composable
private fun BreadcrumbDropdown(
    label: String,
    menuLabel: String,
    items: List<ApiSyllabusNavItem>,
    activeName: String,
    onSelect: (ApiSyllabusNavItem) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    Box {
        Row(
            modifier = Modifier.clickable { expanded = true },
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(1.dp)
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold,
                maxLines = 1
            )
            Icon(
                imageVector = Icons.Outlined.ExpandMore,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .size(14.dp)
                    .rotate(if (expanded) 180f else 0f)
            )
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false },
            modifier = Modifier
                .widthIn(min = 156.dp, max = 280.dp)
                .heightIn(max = 300.dp)
                .background(MaterialTheme.colorScheme.surface)
        ) {
            Text(
                text = menuLabel.uppercase(),
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.68f),
                fontWeight = FontWeight.Bold
            )
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.4f))
            items.forEach { item ->
                DropdownMenuItem(
                    text = {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Text(
                                text = item.name,
                                style = MaterialTheme.typography.labelMedium,
                                color = if (item.name == activeName) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
                                fontWeight = if (item.name == activeName) FontWeight.Bold else FontWeight.Normal,
                                modifier = Modifier.weight(1f),
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            if (item.name == activeName) {
                                Icon(
                                    imageVector = Icons.Outlined.Check,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(14.dp)
                                )
                            }
                        }
                    },
                    onClick = {
                        expanded = false
                        onSelect(item)
                    }
                )
            }
        }
    }
}

@Composable
private fun SyllabusSubjectHeader(detail: ApiSyllabusSubjectDetailResponse) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Text(
                text = detail.subject.ifBlank { "Subject" },
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.ExtraBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.secondaryContainer) {
                    Text(
                        text = detail.grade.ifBlank { "Syllabus" },
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSecondaryContainer,
                        fontWeight = FontWeight.Bold
                    )
                }
                Text(
                    text = "${detail.chapters.size} chapters · ${detail.totalCount} files",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

@Composable
private fun ChapterPicker(
    chapters: List<ApiSyllabusChapter>,
    selectedChapterId: String,
    onSelect: (String) -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                text = "CHAPTERS & TOPICS",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontWeight = FontWeight.Bold,
                letterSpacing = MaterialTheme.typography.labelSmall.letterSpacing
            )
            Row(
                modifier = Modifier.horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                chapters.forEach { chapter ->
                    val selected = chapter.id == selectedChapterId
                    Surface(
                        modifier = Modifier
                            .widthIn(min = 120.dp, max = 230.dp)
                            .clickable { onSelect(chapter.id) },
                        shape = WebPillShape,
                        color = if (selected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent,
                        border = BorderStroke(1.dp, if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.35f) else MaterialTheme.colorScheme.outlineVariant)
                    ) {
                        Text(
                            text = chapter.name,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 9.dp),
                            style = MaterialTheme.typography.labelMedium,
                            color = if (selected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ChapterViewer(
    chapter: ApiSyllabusChapter,
    onResourceClick: (String) -> Unit
) {
    var subtab by rememberSaveable(chapter.id) { mutableStateOf("guide") }
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = chapter.name,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(16.dp))
            ChapterSubtabs(
                selected = subtab,
                onSelect = { subtab = it }
            )
            Spacer(modifier = Modifier.height(20.dp))
            when (subtab) {
                "qas" -> ChapterQas(chapter = chapter)
                "files" -> ChapterFiles(chapter = chapter, onResourceClick = onResourceClick)
                else -> ChapterGuide(chapter = chapter)
            }
        }
    }
}

@Composable
private fun ChapterSubtabs(selected: String, onSelect: (String) -> Unit) {
    val tabs = listOf(
        "guide" to "Chapter Guide",
        "qas" to "Solved Q&As",
        "files" to "Study Files"
    )
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        tabs.forEach { (key, label) ->
            Column(
                modifier = Modifier.clickable { onSelect(key) },
                horizontalAlignment = Alignment.Start
            ) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelLarge,
                    color = if (selected == key) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
                Spacer(modifier = Modifier.height(8.dp))
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(2.dp),
                    color = if (selected == key) MaterialTheme.colorScheme.primary else Color.Transparent,
                    shape = WebPillShape
                ) {}
            }
        }
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
}

@Composable
private fun ChapterGuide(chapter: ApiSyllabusChapter) {
    if (chapter.guideSections.isEmpty()) {
        EmptyChapterBlock(
            icon = Icons.Outlined.MenuBook,
            message = "No chapter summary or syllabus guide is available yet."
        )
        return
    }
    Column(verticalArrangement = Arrangement.spacedBy(20.dp)) {
        if (chapter.guideSections.size > 1) {
            SectionToc(labels = chapter.guideSections.map { it.title.ifBlank { "Overview" } })
        }
        chapter.guideSections.forEach { section ->
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(
                    text = section.title.ifBlank { "Overview" },
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.primaryContainer, thickness = 2.dp)
                MarkdownText(
                    markdown = section.content,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
        }
    }
}

@Composable
private fun SectionToc(labels: List<String>) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainer,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(horizontal = 20.dp, vertical = 16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                text = "IN THIS CHAPTER",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontWeight = FontWeight.Bold
            )
            Row(
                modifier = Modifier.horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                labels.forEach { label ->
                    Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.primaryContainer) {
                        Text(
                            text = label,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 5.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.primary,
                            fontWeight = FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ChapterQas(chapter: ApiSyllabusChapter) {
    val items = chapter.qaSections.flatMap { section ->
        val parsed = section.parsedItems
        if (parsed.isNotEmpty()) parsed else listOf(ApiSyllabusQaItem(question = section.title, answer = section.content))
    }.filter { it.question.isNotBlank() || it.answer.isNotBlank() }
    if (items.isEmpty()) {
        EmptyChapterBlock(
            icon = Icons.Outlined.Quiz,
            message = "No solved textbook question-answers are available yet."
        )
        return
    }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        items.forEach { qa ->
            QaAccordion(qa = qa)
        }
    }
}

@Composable
private fun QaAccordion(qa: ApiSyllabusQaItem) {
    var expanded by rememberSaveable(qa.question) { mutableStateOf(false) }
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { expanded = !expanded }
                    .padding(horizontal = 14.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Text(
                    text = qa.question.ifBlank { "Question" },
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.weight(1f),
                    maxLines = if (expanded) 4 else 2,
                    overflow = TextOverflow.Ellipsis
                )
                Icon(
                    imageVector = Icons.Outlined.ExpandMore,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.rotate(if (expanded) 180f else 0f)
                )
            }
            if (expanded) {
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.55f))
                MarkdownText(
                    markdown = qa.answer.ifBlank { "No answer added yet." },
                    modifier = Modifier.padding(14.dp),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
        }
    }
}
