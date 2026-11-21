package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.R
import com.neb.ians.data.api.ApiInteractiveCourseSummary
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebChipRow
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.getMaterialIcon

private const val ALL = "All"
private val CardShape = RoundedCornerShape(24.dp)
private val TileShape = RoundedCornerShape(16.dp)

/** One flat list of courses with a category filter. No nested scrollers, no hero, no helper text. */
@Composable
fun InteractiveContent(
    state: InteractiveUiState,
    onCourseClick: (String) -> Unit,
    onRetry: () -> Unit
) {
    when {
        state.isLoading -> Box(Modifier.fillMaxSize(), Alignment.Center) { NebLoader() }
        state.error != null -> ErrorCard(
            message = state.error ?: "Failed to load interactive content",
            onRetry = onRetry,
            modifier = Modifier.padding(16.dp)
        )
        state.categories.none { it.courses.isNotEmpty() } -> WebEmptyState(
            title = "No interactive content yet",
            message = "Lessons and simulations will appear here.",
            icon = painterResource(id = R.drawable.ic_document),
            modifier = Modifier.padding(16.dp)
        )
        else -> {
            val groups = remember(state.categories) { state.categories.filter { it.courses.isNotEmpty() } }
            val labels = remember(groups) { listOf(ALL) + groups.map { it.label } }
            var picked by rememberSaveable { mutableStateOf(ALL) }
            if (picked !in labels) picked = ALL
            val visible = remember(groups, picked) {
                groups.filter { picked == ALL || it.label == picked }
                    .flatMap { g -> g.courses.map { c -> Triple(g.key, g.color, c) } }
            }
            Column(Modifier.fillMaxSize()) {
                WebChipRow(
                    items = labels,
                    selectedItem = picked,
                    onItemClick = { picked = it ?: ALL },
                    modifier = Modifier.padding(top = 8.dp, bottom = 4.dp)
                )
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 108.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    items(visible, key = { it.third.slug }, contentType = { "course_row" }) { (_, color, course) ->
                        CourseRow(course, color) { onCourseClick(course.slug) }
                    }
                }
            }
        }
    }
}

@Composable
private fun CourseRow(course: ApiInteractiveCourseSummary, categoryColor: String, onClick: () -> Unit) {
    val accent = parseWebColor(course.color.ifBlank { categoryColor })
    Surface(
        modifier = Modifier.fillMaxWidth().clip(CardShape).clickable(onClick = onClick),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.7f))
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(
                Modifier.size(48.dp).background(accent.copy(alpha = 0.14f), TileShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(getMaterialIcon(course.icon), null, tint = accent, modifier = Modifier.size(24.dp))
            }
            Column(Modifier.weight(1f).padding(start = 12.dp)) {
                Text(
                    course.title,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(Modifier.height(6.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                    WebChip(text = "${course.lessonCount} lessons", selected = true)
                    if (course.totalMinutes > 0) WebChip(text = "${course.totalMinutes} min")
                }
            }
        }
    }
}

private fun parseWebColor(raw: String): Color = try {
    Color(android.graphics.Color.parseColor(raw))
} catch (_: Exception) {
    Color(0xFF5C5C61)
}
