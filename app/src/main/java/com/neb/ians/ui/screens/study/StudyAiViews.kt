package com.neb.ians.ui.screens.study

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiStudyDocument
import com.neb.ians.data.api.ApiStudyFlashcard
import com.neb.ians.data.api.ApiStudyMindmap
import com.neb.ians.data.api.ApiStudyMindmapNode
import com.neb.ians.data.api.ApiStudyQuizDetail
import com.neb.ians.data.api.ApiStudyQuizQuestion
import com.neb.ians.data.api.ApiStudyQuizSummary
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.KaTeXText
import com.neb.ians.ui.components.NebChipRow
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebFilterChip
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebPrimaryButton
import retrofit2.HttpException

// -------------------------------------------------------------
// Shared Study Lab helpers + composables used by both the
// document-level (Study Lab) and space-level (Study Space) flows.
// -------------------------------------------------------------

internal val STUDY_ALLOWED_EXTENSIONS = setOf(
    "pdf", "txt", "doc", "docx",
    "png", "jpg", "jpeg", "gif", "webp", "bmp", "svg",
    "mp4", "avi", "mov", "mkv", "webm",
    "mp3", "wav", "ogg", "flac", "aac", "m4a"
)

internal const val STUDY_MAX_UPLOAD_BYTES: Long = 20L * 1024L * 1024L

internal val STUDY_TERMINAL_PARSE_STATES = setOf("ready", "failed")

internal fun studyParseStatusOf(doc: ApiStudyDocument): String =
    doc.parseStatus.ifBlank { doc.status }.ifBlank { "pending" }

internal fun studyUploadValidationError(fileName: String, sizeBytes: Long): String? {
    val ext = fileName.substringAfterLast('.', "").lowercase()
    if (ext.isBlank() || ext !in STUDY_ALLOWED_EXTENSIONS) {
        return "Unsupported file type${if (ext.isNotBlank()) " .$ext" else ""}. Allowed: PDF, TXT, DOC, images, audio, video."
    }
    if (sizeBytes > STUDY_MAX_UPLOAD_BYTES) {
        return "File too large (max 20 MB)."
    }
    return null
}

internal fun studyErrorMessage(e: Throwable): String = when (e) {
    is HttpException -> when (e.code()) {
        202 -> "Documents are still being parsed — try again shortly"
        422 -> "Parsing failed — re-upload or retry"
        502 -> "AI generation failed, try again"
        429 -> "Slow down — too many requests"
        else -> "Request failed (HTTP ${e.code()})"
    }
    else -> e.localizedMessage ?: "Something went wrong"
}

internal data class PickedStudyFile(
    val name: String,
    val size: Long,
    val mime: String?,
    val bytes: ByteArray
)

/** Reads a picked content Uri into memory (call from Dispatchers.IO). */
internal fun readPickedStudyFile(context: Context, uri: Uri): PickedStudyFile? {
    val resolver = context.contentResolver
    var name = "upload.bin"
    var size = -1L
    try {
        resolver.query(uri, null, null, null, null)?.use { cursor ->
            if (cursor.moveToFirst()) {
                val nameIdx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (nameIdx >= 0) cursor.getString(nameIdx)?.let { name = it }
                val sizeIdx = cursor.getColumnIndex(OpenableColumns.SIZE)
                if (sizeIdx >= 0 && !cursor.isNull(sizeIdx)) size = cursor.getLong(sizeIdx)
            }
        }
    } catch (_: Exception) {
        // keep defaults; bytes read below still validates size
    }
    val bytes = try {
        resolver.openInputStream(uri)?.use { it.readBytes() }
    } catch (_: Exception) {
        null
    } ?: return null
    return PickedStudyFile(
        name = name,
        size = if (size >= 0) size else bytes.size.toLong(),
        mime = resolver.getType(uri),
        bytes = bytes
    )
}

/** Row of one quiz result, normalized across document and space quiz shapes. */
data class StudyQuizResultRow(
    val number: Int,
    val question: String,
    val userAnswer: String,
    val correctAnswer: String,
    val isCorrect: Boolean,
    val explanation: String
)

/** Normalized quiz result payload shown in the results view. */
data class StudyQuizResultData(
    val score: Int,
    val total: Int,
    val xp: Int,
    val rows: List<StudyQuizResultRow>
)

// -------------------------------------------------------------
// Parse status pill
// -------------------------------------------------------------

@Composable
fun ParseStatusPill(status: String, modifier: Modifier = Modifier) {
    val (bg, fg) = when (status) {
        "ready" -> MaterialTheme.colorScheme.surfaceContainerHighest to MaterialTheme.colorScheme.onSurface
        "failed" -> MaterialTheme.colorScheme.errorContainer to MaterialTheme.colorScheme.onErrorContainer
        else -> MaterialTheme.colorScheme.surfaceContainerHigh to MaterialTheme.colorScheme.onSurfaceVariant
    }
    Row(
        modifier = modifier
            .clip(WebPillShape)
            .background(bg)
            .padding(horizontal = 10.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        if (status !in STUDY_TERMINAL_PARSE_STATES) {
            CircularProgressIndicator(
                modifier = Modifier.size(10.dp),
                strokeWidth = 1.5.dp,
                color = fg
            )
        }
        Text(
            text = status.replaceFirstChar { it.uppercase() },
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.Bold,
            color = fg,
            maxLines = 1
        )
    }
}

// -------------------------------------------------------------
// Feature tab row (Summary / Mindmap / Quiz / Flashcards)
// -------------------------------------------------------------

@Composable
fun StudyFeatureTabRow(
    selected: String,
    onSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        listOf(
            "summary" to "Summary",
            "mindmap" to "Mindmap",
            "quiz" to "Quiz",
            "flashcards" to "Flashcards"
        ).forEach { (key, label) ->
            WebChip(text = label, selected = selected == key, onClick = { onSelect(key) })
        }
    }
}

@Composable
internal fun StudySectionCard(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            content()
        }
    }
}

// -------------------------------------------------------------
// Summary
// -------------------------------------------------------------

@Composable
fun StudySummarySection(
    summaryCompact: String,
    summaryDetailed: String,
    mode: String,
    onModeChange: (String) -> Unit,
    isGenerating: Boolean,
    onGenerate: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val currentText = if (mode == "detailed") summaryDetailed else summaryCompact
    StudySectionCard(modifier = modifier) {
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            WebChip(text = "Compact", selected = mode == "compact", onClick = { onModeChange("compact") })
            WebChip(text = "Detailed", selected = mode == "detailed", onClick = { onModeChange("detailed") })
        }
        Spacer(modifier = Modifier.height(12.dp))
        when {
            isGenerating -> {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                    Text(
                        text = "Generating ${if (mode == "detailed") "detailed" else "compact"} summary…",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            currentText.isNotBlank() -> {
                MarkdownText(
                    markdown = currentText,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            else -> {
                Text(
                    text = "No ${if (mode == "detailed") "detailed" else "compact"} summary yet. Generate one from your study material.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        Spacer(modifier = Modifier.height(14.dp))
        if (!isGenerating) {
            if (currentText.isBlank()) {
                WebPrimaryButton(text = "Generate summary", onClick = { onGenerate(mode) })
            } else {
                WebOutlinedButton(text = "Regenerate", onClick = { onGenerate(mode) })
            }
        }
    }
}

// -------------------------------------------------------------
// Mindmap
// -------------------------------------------------------------

private val mindmapBulletColors = listOf(
    Color(0xFF47474B),
    Color(0xFF5C5C61),
    Color(0xFF6E6E75),
    Color(0xFF7C7C83),
    Color(0xFF9B9BA1)
)

@Composable
fun StudyMindmapSection(
    mindmap: ApiStudyMindmap?,
    isGenerating: Boolean,
    onGenerate: () -> Unit,
    modifier: Modifier = Modifier
) {
    StudySectionCard(modifier = modifier) {
        when {
            isGenerating -> {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                    Text(
                        text = "Generating mindmap…",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            mindmap == null || mindmap.nodes.isEmpty() -> {
                Text(
                    text = "No mindmap yet. Generate a visual breakdown of the key topics.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(14.dp))
                WebPrimaryButton(text = "Generate mindmap", onClick = onGenerate)
            }
            else -> {
                // Root node pill, centered.
                Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Surface(
                        shape = WebPillShape,
                        color = MaterialTheme.colorScheme.primaryContainer
                    ) {
                        Text(
                            text = mindmap.title.ifBlank { "Mindmap" },
                            modifier = Modifier.padding(horizontal = 18.dp, vertical = 9.dp),
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            textAlign = TextAlign.Center
                        )
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
                mindmap.nodes.forEachIndexed { index, node ->
                    MindmapNodeRow(node = node, depth = 0, branchIndex = index)
                }
                Spacer(modifier = Modifier.height(8.dp))
                WebOutlinedButton(text = "Regenerate", onClick = onGenerate)
            }
        }
    }
}

@Composable
private fun MindmapNodeRow(node: ApiStudyMindmapNode, depth: Int, branchIndex: Int) {
    var expanded by rememberSaveable(node.title, depth) { mutableStateOf(depth < 1) }
    val hasChildren = node.children.isNotEmpty()
    val bulletColor = mindmapBulletColors[branchIndex % mindmapBulletColors.size]
    val chevronRotation by animateFloatAsState(
        targetValue = if (expanded) 0f else -90f,
        animationSpec = tween(200),
        label = "mindmapChevron"
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(start = (depth * 18).dp)
            .animateContentSize()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(10.dp))
                .then(if (hasChildren) Modifier.clickable { expanded = !expanded } else Modifier)
                .padding(vertical = 6.dp, horizontal = 4.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // Connector / bullet
            Box(
                modifier = Modifier
                    .padding(top = 5.dp)
                    .size(9.dp)
                    .background(bulletColor, CircleShape)
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = node.title,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                if (node.note.isNotBlank()) {
                    Text(
                        text = node.note,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            if (hasChildren) {
                Icon(
                    imageVector = Icons.Filled.KeyboardArrowDown,
                    contentDescription = if (expanded) "Collapse" else "Expand",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier
                        .size(20.dp)
                        .graphicsLayer { rotationZ = chevronRotation }
                )
            }
        }
        if (hasChildren && expanded) {
            Row(modifier = Modifier.fillMaxWidth()) {
                // Vertical connector line
                Box(
                    modifier = Modifier
                        .padding(start = 8.dp)
                        .width(2.dp)
                        .heightIn(min = 4.dp)
                        .background(bulletColor.copy(alpha = 0.25f), RoundedCornerShape(1.dp))
                )
                Column(modifier = Modifier.weight(1f)) {
                    node.children.forEachIndexed { index, child ->
                        MindmapNodeRow(node = child, depth = 0, branchIndex = branchIndex + index + 1)
                    }
                }
            }
        }
    }
}

// -------------------------------------------------------------
// Quiz list + count picker
// -------------------------------------------------------------

@Composable
fun StudyQuizListSection(
    quizzes: List<ApiStudyQuizSummary>,
    isGenerating: Boolean,
    openingQuizId: String?,
    onGenerate: (Int) -> Unit,
    onOpenQuiz: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var showCountDialog by remember { mutableStateOf(false) }
    StudySectionCard(modifier = modifier) {
        if (quizzes.isEmpty()) {
            Text(
                text = "No quizzes yet. Generate one to test your knowledge.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            quizzes.forEachIndexed { index, quiz ->
                if (index > 0) Spacer(modifier = Modifier.height(8.dp))
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable(enabled = openingQuizId == null) { onOpenQuiz(quiz.id) },
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.surfaceContainerLow,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = quiz.title.ifBlank { "Study quiz" },
                                style = MaterialTheme.typography.titleSmall,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = buildString {
                                    append("${quiz.questionCount} questions")
                                    if (quiz.attemptCount > 0) {
                                        append(" · Best ${quiz.bestScore}/${quiz.questionCount}")
                                        append(" · ${quiz.attemptCount} attempt${if (quiz.attemptCount == 1) "" else "s"}")
                                    }
                                },
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        if (openingQuizId == quiz.id) {
                            CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                        }
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(14.dp))
        if (isGenerating) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                Text(
                    text = "Generating quiz…",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            WebPrimaryButton(text = "New quiz", onClick = { showCountDialog = true })
        }
    }
    if (showCountDialog) {
        StudyCountDialog(
            title = "How many questions?",
            onDismiss = { showCountDialog = false },
            onPick = { count ->
                showCountDialog = false
                onGenerate(count)
            }
        )
    }
}

@Composable
fun StudyCountDialog(
    title: String,
    onDismiss: () -> Unit,
    onPick: (Int) -> Unit,
    options: List<Int> = listOf(5, 10, 15, 20)
) {
    var chosen by remember { mutableStateOf(options.firstOrNull() ?: 5) }

    NebDialog(
        onDismissRequest = onDismiss,
        title = title,
        supportingText = "Pick how many items to generate.",
        icon = Icons.Outlined.Tune,
        confirm = NebDialogAction("Generate", { onPick(chosen) }),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebChipRow {
            options.forEach { count ->
                NebFilterChip(
                    label = "$count",
                    selected = chosen == count,
                    onClick = { chosen = count }
                )
            }
        }
    }
}

// -------------------------------------------------------------
// Quiz player (one question per screen)
// -------------------------------------------------------------

@Composable
fun StudyQuizPlayer(
    quiz: ApiStudyQuizDetail,
    isSubmitting: Boolean,
    error: String?,
    answerKeyFor: (ApiStudyQuizQuestion) -> String,
    onSubmit: (Map<String, String>) -> Unit,
    onExit: () -> Unit,
    modifier: Modifier = Modifier
) {
    val questions = quiz.questions
    var index by remember(quiz.id) { mutableIntStateOf(0) }
    val answers = remember(quiz.id) { mutableStateMapOf<String, String>() }

    if (questions.isEmpty()) {
        StudySectionCard(modifier = modifier) {
            Text(
                text = "This quiz has no questions.",
                style = MaterialTheme.typography.bodyMedium
            )
            Spacer(modifier = Modifier.height(12.dp))
            WebOutlinedButton(text = "Back", onClick = onExit)
        }
        return
    }

    val question = questions[index.coerceIn(0, questions.lastIndex)]
    val key = answerKeyFor(question)
    val selectedLetter = answers[key]
    val isLast = index == questions.lastIndex
    val allAnswered = questions.all { answers.containsKey(answerKeyFor(it)) }

    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Question ${index + 1} of ${questions.size}",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "${answers.size}/${questions.size} answered",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            LinearProgressIndicator(
                progress = { (index + 1f) / questions.size },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(6.dp)
                    .clip(WebPillShape)
            )
        }

        StudySectionCard {
            MarkdownText(
                markdown = question.displayQuestion,
                style = MaterialTheme.typography.titleMedium
            )
            Spacer(modifier = Modifier.height(14.dp))
            listOf(
                "A" to question.optionA,
                "B" to question.optionB,
                "C" to question.optionC,
                "D" to question.optionD
            ).forEach { (letter, optionText) ->
                val selected = selectedLetter == letter
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp)
                        .clickable(enabled = !isSubmitting) { answers[key] = letter },
                    shape = RoundedCornerShape(12.dp),
                    color = if (selected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent,
                    border = BorderStroke(
                        width = if (selected) 1.5.dp else 1.dp,
                        color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant
                    )
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(26.dp)
                                .clip(CircleShape)
                                .background(
                                    if (selected) MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.surfaceContainerHigh
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = letter,
                                style = MaterialTheme.typography.labelMedium,
                                fontWeight = FontWeight.Bold,
                                color = if (selected) MaterialTheme.colorScheme.onPrimary
                                else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        KaTeXText(
                            text = optionText,
                            style = MaterialTheme.typography.bodyMedium,
                            color = if (selected) MaterialTheme.colorScheme.onPrimaryContainer
                            else MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
        }

        if (error != null) {
            Text(
                text = error,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.error
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            WebOutlinedButton(
                text = "Prev",
                onClick = { if (index > 0) index-- }
            )
            if (isSubmitting) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                    Text(
                        text = "Submitting…",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            } else if (isLast) {
                WebPrimaryButton(
                    text = if (allAnswered) "Submit" else "Submit (${answers.size}/${questions.size})",
                    onClick = { if (allAnswered) onSubmit(answers.toMap()) }
                )
            } else {
                WebPrimaryButton(
                    text = "Next",
                    onClick = { if (index < questions.lastIndex) index++ }
                )
            }
        }
    }
}

// -------------------------------------------------------------
// Quiz results
// -------------------------------------------------------------

@Composable
fun StudyQuizResults(
    result: StudyQuizResultData,
    onDone: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(120.dp)
                    .border(6.dp, MaterialTheme.colorScheme.primary, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "${result.score}/${result.total}",
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.ExtraBold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            if (result.xp > 0) {
                Surface(
                    shape = WebPillShape,
                    color = MaterialTheme.colorScheme.secondaryContainer
                ) {
                    Text(
                        text = "+${result.xp} XP",
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 6.dp),
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSecondaryContainer
                    )
                }
            }
            Text(
                text = when {
                    result.total > 0 && result.score == result.total -> "Perfect score!"
                    result.total > 0 && result.score >= result.total / 2 -> "Nice work — keep practicing."
                    else -> "Review the answers below and try again."
                },
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        result.rows.forEach { row ->
            StudyQuizResultRowCard(row)
        }

        WebPrimaryButton(text = "Done", onClick = onDone, modifier = Modifier.fillMaxWidth())
    }
}

@Composable
private fun StudyQuizResultRowCard(row: StudyQuizResultRow) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(24.dp)
                        .clip(CircleShape)
                        .background(if (row.isCorrect) MaterialTheme.colorScheme.surfaceContainerHighest else MaterialTheme.colorScheme.errorContainer),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = if (row.isCorrect) Icons.Filled.Check else Icons.Filled.Close,
                        contentDescription = if (row.isCorrect) "Correct" else "Incorrect",
                        tint = if (row.isCorrect) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onErrorContainer,
                        modifier = Modifier.size(15.dp)
                    )
                }
                Column(modifier = Modifier.weight(1f)) {
                    KaTeXText(
                        text = "Q${row.number}. ${row.question}",
                        style = MaterialTheme.typography.bodyMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    KaTeXText(
                        text = if (row.isCorrect) {
                            "Your answer: ${row.userAnswer.ifBlank { "—" }} ✓"
                        } else {
                            "Your answer: ${row.userAnswer.ifBlank { "—" }} · Correct: ${row.correctAnswer.ifBlank { "—" }}"
                        },
                        style = MaterialTheme.typography.labelMedium,
                        color = if (row.isCorrect) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.error
                    )
                }
            }
            if (row.explanation.isNotBlank()) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.surfaceContainerHigh
                ) {
                    MarkdownText(
                        markdown = row.explanation,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(10.dp)
                    )
                }
            }
        }
    }
}

// -------------------------------------------------------------
// Flashcards (flip + confidence review)
// -------------------------------------------------------------

@Composable
fun StudyFlashcardsSection(
    cards: List<ApiStudyFlashcard>,
    isGenerating: Boolean,
    onReview: (cardId: String, confidence: String) -> Unit,
    onGenerateMore: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    var showCountDialog by remember { mutableStateOf(false) }
    var index by remember(cards.size) { mutableIntStateOf(0) }
    var flipped by remember { mutableStateOf(false) }
    var finished by remember(cards.size) { mutableStateOf(false) }

    StudySectionCard(modifier = modifier) {
        when {
            isGenerating -> {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                    Text(
                        text = "Generating flashcards…",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            cards.isEmpty() -> {
                Text(
                    text = "No flashcards yet. Generate a deck to start active recall practice.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(14.dp))
                WebPrimaryButton(text = "Generate flashcards", onClick = { showCountDialog = true })
            }
            finished || index >= cards.size -> {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Text(
                        text = "Deck complete!",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "You reviewed ${cards.size} card${if (cards.size == 1) "" else "s"}.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        WebOutlinedButton(text = "Review again", onClick = {
                            index = 0
                            flipped = false
                            finished = false
                        })
                        WebPrimaryButton(text = "Generate more", onClick = { showCountDialog = true })
                    }
                }
            }
            else -> {
                val card = cards[index]
                Text(
                    text = "Card ${index + 1} / ${cards.size}",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.fillMaxWidth(),
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(10.dp))
                FlashcardFlip(
                    front = card.front,
                    back = card.back,
                    flipped = flipped,
                    onFlip = { flipped = !flipped }
                )
                Spacer(modifier = Modifier.height(14.dp))
                if (!flipped) {
                    Text(
                        text = "Tap the card to reveal the answer",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.fillMaxWidth(),
                        textAlign = TextAlign.Center
                    )
                } else {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        ConfidenceButton(
                            label = "Hard",
                            container = MaterialTheme.colorScheme.errorContainer,
                            content = MaterialTheme.colorScheme.onErrorContainer,
                            modifier = Modifier.weight(1f),
                            onClick = {
                                onReview(card.id, "hard")
                                flipped = false
                                if (index >= cards.lastIndex) finished = true else index++
                            }
                        )
                        ConfidenceButton(
                            label = "Medium",
                            container = MaterialTheme.colorScheme.surfaceContainerHigh,
                            content = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.weight(1f),
                            onClick = {
                                onReview(card.id, "medium")
                                flipped = false
                                if (index >= cards.lastIndex) finished = true else index++
                            }
                        )
                        ConfidenceButton(
                            label = "Easy",
                            container = MaterialTheme.colorScheme.inverseSurface,
                            content = MaterialTheme.colorScheme.inverseOnSurface,
                            modifier = Modifier.weight(1f),
                            onClick = {
                                onReview(card.id, "easy")
                                flipped = false
                                if (index >= cards.lastIndex) finished = true else index++
                            }
                        )
                    }
                }
            }
        }
    }
    if (showCountDialog) {
        StudyCountDialog(
            title = "How many flashcards?",
            onDismiss = { showCountDialog = false },
            onPick = { count ->
                showCountDialog = false
                onGenerateMore(count)
            }
        )
    }
}

@Composable
private fun FlashcardFlip(
    front: String,
    back: String,
    flipped: Boolean,
    onFlip: () -> Unit
) {
    val rotation by animateFloatAsState(
        targetValue = if (flipped) 180f else 0f,
        animationSpec = tween(durationMillis = 420),
        label = "flashcardFlip"
    )
    val showingBack = rotation > 90f
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 190.dp)
            .graphicsLayer {
                rotationY = rotation
                cameraDistance = 14f * density
            }
            .clip(WebPanelShape)
            .background(
                if (showingBack) MaterialTheme.colorScheme.secondaryContainer
                else MaterialTheme.colorScheme.primaryContainer
            )
            .clickable(onClick = onFlip)
            .padding(22.dp),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier.graphicsLayer {
                // Un-mirror the back face content.
                if (showingBack) rotationY = 180f
            },
            contentAlignment = Alignment.Center
        ) {
            KaTeXText(
                text = if (showingBack) back else front,
                style = if (showingBack) MaterialTheme.typography.bodyLarge else MaterialTheme.typography.titleMedium,
                fontWeight = if (showingBack) FontWeight.Normal else FontWeight.Bold,
                textAlign = TextAlign.Center,
                color = if (showingBack) MaterialTheme.colorScheme.onSecondaryContainer
                else MaterialTheme.colorScheme.onPrimaryContainer
            )
        }
    }
}

@Composable
private fun ConfidenceButton(
    label: String,
    container: Color,
    content: Color,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier
            .clip(WebPillShape)
            .clickable(onClick = onClick),
        shape = WebPillShape,
        color = container
    ) {
        Text(
            text = label,
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 11.dp),
            style = MaterialTheme.typography.labelLarge,
            fontWeight = FontWeight.Bold,
            color = content,
            textAlign = TextAlign.Center
        )
    }
}
