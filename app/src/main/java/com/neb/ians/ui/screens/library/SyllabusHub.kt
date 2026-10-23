package com.neb.ians.ui.screens.library

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.automirrored.outlined.TrendingUp
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.AutoStories
import androidx.compose.material.icons.outlined.Biotech
import androidx.compose.material.icons.outlined.Bolt
import androidx.compose.material.icons.outlined.Calculate
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Functions
import androidx.compose.material.icons.outlined.History
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Science
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.SelfImprovement
import androidx.compose.material.icons.outlined.Terminal
import androidx.compose.material.icons.outlined.Translate
import androidx.compose.material.icons.outlined.WaterDrop
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiSyllabusGrade
import com.neb.ians.data.api.ApiSyllabusHit
import com.neb.ians.data.api.ApiSyllabusSubjectCard
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

@Composable
fun SyllabusContent(
    state: SyllabusUiState,
    viewModel: SyllabusViewModel,
    onOpenDoc: (grade: String, subject: String, kind: String, no: Int) -> Unit = { _, _, _, _ -> }
) {
    if (state.openSubject != null) {
        SyllabusSubject(state = state, viewModel = viewModel, onOpenDoc = onOpenDoc)
    } else {
        SyllabusHub(state = state, viewModel = viewModel, onOpenDoc = onOpenDoc)
    }
}

@Composable
private fun SyllabusHub(
    state: SyllabusUiState,
    viewModel: SyllabusViewModel,
    onOpenDoc: (grade: String, subject: String, kind: String, no: Int) -> Unit
) {
    val index = state.index
    when {
        index == null && state.isLoading -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            NebLoader(size = NebLoaderSize.Standard)
        }
        index == null -> ErrorCard(
            message = state.error ?: "The syllabus could not be loaded.",
            onRetry = { viewModel.load() },
            modifier = Modifier.padding(16.dp)
        )
        else -> {
            val grade = index.grades.firstOrNull { it.grade == state.grade } ?: index.grades.lastOrNull()
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 14.dp, bottom = 110.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                item(key = "intro") { SyllabusIntro(index.totals.units, index.totals.topics) }
                item(key = "search") { SyllabusSearchField(state.query, viewModel::search) }
                if (state.query.trim().length >= 2) {
                    syllabusHits(state, viewModel)
                } else {
                    state.lastRead?.let { (key, title, label) ->
                        // "11/physics/unit3", "11/physics/bank2" or "11/physics/guide"
                        val m = Regex("""^(\w+)/([\w-]+)/(unit|bank|guide)(\d*)$""").find(key)
                        if (m != null) {
                            val (g, subj, kind, no) = m.destructured
                            item(key = "continue") {
                                ContinueCard(
                                    title = title.ifBlank { label },
                                    label = label,
                                    progress = (state.marks[key]?.read ?: 0) / 100f,
                                    onClick = { onOpenDoc(g, subj, kind, no.toIntOrNull() ?: 0) }
                                )
                            }
                        }
                    }
                    item(key = "grades") { GradeSwitch(index.grades, state.grade, viewModel::selectGrade) }
                    if (grade != null) {
                        val groups = grade.subjects.groupBy { it.group }
                        groups.forEach { (group, cards) ->
                            item(key = "g_$group") {
                                Text(
                                    text = groupTitle(group),
                                    style = MaterialTheme.typography.labelLarge,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(top = 6.dp, start = 4.dp)
                                )
                            }
                            items(cards, key = { "s_${grade.grade}_${it.subject}" }) { card ->
                                SubjectCard(
                                    card = card,
                                    progress = fraction(state.chaptersDone(grade.grade, card.subject), card.unitCount),
                                    onClick = { viewModel.openSubject(grade.grade, card.subject) }
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.syllabusHits(state: SyllabusUiState, viewModel: SyllabusViewModel) {
    if (state.isSearching && state.hits.isEmpty()) {
        item(key = "searching") {
            Box(Modifier.fillMaxWidth().padding(24.dp), contentAlignment = Alignment.Center) {
                NebLoader(size = NebLoaderSize.Small)
            }
        }
    } else if (state.hits.isEmpty()) {
        item(key = "nohits") {
            NebEmptyState(
                icon = Icons.Outlined.Search,
                title = "Nothing found",
                subtitle = "Try a shorter or different word.",
                art = null
            )
        }
    } else {
        item(key = "hitcount") {
            Text(
                text = if (state.hitTotal > state.hits.size) "Best ${state.hits.size} of ${state.hitTotal} matches" else "${state.hitTotal} matches",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(start = 4.dp)
            )
        }
        items(state.hits, key = { "h_${it.grade}_${it.subject}_${it.unit}" }) { hit ->
            HitRow(hit) { viewModel.openSubject(hit.grade, hit.subject, hit.unit) }
        }
    }
}

@Composable
private fun SyllabusIntro(units: Int, topics: Int) {
    Column(Modifier.padding(horizontal = 4.dp)) {
        Text(
            text = "Syllabus and study notes",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(Modifier.height(4.dp))
        Text(
            text = "Every unit of the CDC and NEB syllabus for Class 8, 10, 11 and 12 ($units chapters) with the full chapter from the NEBians books, self-check questions and a question bank in the board's pattern.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
internal fun SyllabusSearchField(
    value: String,
    onChange: (String) -> Unit,
    placeholder: String = "Search any topic across all classes"
) {
    Surface(
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.surfaceContainerHigh,
        modifier = Modifier.fillMaxWidth().height(50.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(start = 16.dp, end = 4.dp)) {
            Icon(Icons.Outlined.Search, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
            Spacer(Modifier.width(10.dp))
            Box(Modifier.weight(1f), contentAlignment = Alignment.CenterStart) {
                if (value.isEmpty()) {
                    Text(placeholder, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                BasicTextField(
                    value = value,
                    onValueChange = onChange,
                    singleLine = true,
                    textStyle = MaterialTheme.typography.bodyLarge.copy(color = MaterialTheme.colorScheme.onSurface),
                    cursorBrush = SolidColor(MaterialTheme.colorScheme.onSurface),
                    modifier = Modifier.fillMaxWidth()
                )
            }
            if (value.isNotEmpty()) {
                NebIconButton(icon = Icons.Outlined.Close, contentDescription = "Clear", onClick = { onChange("") })
            }
        }
    }
}

@Composable
private fun ContinueCard(title: String, label: String, progress: Float, onClick: () -> Unit) {
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth().nebPressable(onClick = onClick)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(14.dp)) {
            Icon(Icons.Outlined.History, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface)
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text("Continue reading" + if (label.isNotBlank()) " · $label" else "", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Spacer(Modifier.height(8.dp))
                SyllabusBar(progress)
            }
        }
    }
}

@Composable
private fun GradeSwitch(grades: List<ApiSyllabusGrade>, selected: String, onSelect: (String) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(20.dp))
            .background(MaterialTheme.colorScheme.surfaceContainer)
            .padding(4.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        grades.forEach { g ->
            val isSelected = g.grade == selected
            val container by animateColorAsState(
                targetValue = if (isSelected) MaterialTheme.colorScheme.onSurface else Color.Transparent,
                animationSpec = nebEffectsSpec(),
                label = "grade_bg"
            )
            val content by animateColorAsState(
                targetValue = if (isSelected) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurfaceVariant,
                animationSpec = nebEffectsSpec(),
                label = "grade_fg"
            )
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier
                    .weight(1f)
                    .clip(RoundedCornerShape(16.dp))
                    .background(container)
                    .nebPressable(onClick = { onSelect(g.grade) })
                    .padding(vertical = 10.dp)
            ) {
                Text(g.grade, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = content)
                Text("Class", style = MaterialTheme.typography.labelSmall, color = content)
            }
        }
    }
}

@Composable
private fun SubjectCard(card: ApiSyllabusSubjectCard, progress: Float, onClick: () -> Unit) {
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth().nebPressable(onClick = onClick)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(14.dp)) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            ) {
                Icon(syllabusIcon(card.icon), contentDescription = null, tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(22.dp))
            }
            Spacer(Modifier.width(14.dp))
            Column(Modifier.weight(1f)) {
                Text(card.name, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                Text(card.nameNe, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Spacer(Modifier.height(2.dp))
                Text(
                    text = listOfNotNull("${card.unitCount} chapters", card.hours?.let { "$it hrs" }).joinToString(" · "),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Spacer(Modifier.width(10.dp))
            SyllabusRing(progress = progress, diameter = 42)
        }
    }
}

@Composable
private fun HitRow(hit: ApiSyllabusHit, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(14.dp))
            .nebPressable(onClick = onClick)
            .padding(horizontal = 6.dp, vertical = 8.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "Class ${hit.grade}",
                style = MaterialTheme.typography.labelSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.surface,
                modifier = Modifier
                    .clip(RoundedCornerShape(8.dp))
                    .background(MaterialTheme.colorScheme.onSurface)
                    .padding(horizontal = 8.dp, vertical = 3.dp)
            )
            Spacer(Modifier.width(10.dp))
            Text(
                text = "${hit.name} · Unit ${hit.unit}",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
        Spacer(Modifier.height(4.dp))
        Text(hit.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        if (hit.match.isNotBlank() && hit.match != hit.title) {
            Text(hit.match, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
        Spacer(Modifier.height(8.dp))
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f))
    }
}

@Composable
internal fun SyllabusRing(progress: Float, diameter: Int, label: Boolean = true) {
    val animated by animateFloatAsState(targetValue = progress, animationSpec = nebSpatialSpec(), label = "ring")
    val track = MaterialTheme.colorScheme.surfaceContainerHighest
    val fill = MaterialTheme.colorScheme.onSurface
    Box(contentAlignment = Alignment.Center, modifier = Modifier.size(diameter.dp)) {
        Canvas(Modifier.size(diameter.dp)) {
            val stroke = 3.5.dp.toPx()
            val inset = stroke / 2
            val arcSize = Size(size.width - stroke, size.height - stroke)
            drawArc(track, 0f, 360f, false, Offset(inset, inset), arcSize, style = Stroke(stroke))
            if (animated > 0f) {
                drawArc(fill, -90f, 360f * animated, false, Offset(inset, inset), arcSize, style = Stroke(stroke, cap = StrokeCap.Round))
            }
        }
        if (label) {
            Text("${(progress * 100).toInt()}%", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
internal fun SyllabusBar(progress: Float, modifier: Modifier = Modifier) {
    val animated by animateFloatAsState(targetValue = progress, animationSpec = nebSpatialSpec(), label = "bar")
    Box(
        modifier
            .fillMaxWidth()
            .height(6.dp)
            .clip(WebPillShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
    ) {
        Box(
            Modifier
                .fillMaxWidth(animated.coerceIn(0f, 1f))
                .height(6.dp)
                .clip(WebPillShape)
                .background(MaterialTheme.colorScheme.onSurface)
        )
    }
}

internal fun fraction(done: Int, total: Int): Float = if (total <= 0) 0f else (done.toFloat() / total).coerceIn(0f, 1f)

private fun groupTitle(group: String): String = when (group) {
    "compulsory" -> "Compulsory subjects"
    "optional" -> "Optional subjects"
    else -> "Science stream"
}

internal fun syllabusIcon(name: String): ImageVector = when (name) {
    "translate" -> Icons.Outlined.Translate
    "menu_book" -> Icons.AutoMirrored.Outlined.MenuBook
    "calculate" -> Icons.Outlined.Calculate
    "science" -> Icons.Outlined.Science
    "public" -> Icons.Outlined.Public
    "self_improvement" -> Icons.Outlined.SelfImprovement
    "functions" -> Icons.Outlined.Functions
    "account_balance" -> Icons.Outlined.AccountBalance
    "trending_up" -> Icons.AutoMirrored.Outlined.TrendingUp
    "bolt" -> Icons.Outlined.Bolt
    "experiment" -> Icons.Outlined.WaterDrop
    "biotech" -> Icons.Outlined.Biotech
    "terminal" -> Icons.Outlined.Terminal
    else -> Icons.Outlined.AutoStories
}
