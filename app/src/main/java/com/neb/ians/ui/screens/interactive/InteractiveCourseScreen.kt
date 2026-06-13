package com.neb.ians.ui.screens.interactive

import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiInteractiveCourseDetailResponse
import com.neb.ians.data.api.ApiInteractiveLessonSummary
import com.neb.ians.data.api.ApiService
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebPillShape
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class InteractiveCourseUiState(
    val course: ApiInteractiveCourseDetailResponse? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class InteractiveCourseViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {
    private val _uiState = MutableStateFlow(InteractiveCourseUiState())
    val uiState: StateFlow<InteractiveCourseUiState> = _uiState.asStateFlow()

    fun loadCourse(courseSlug: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val response = apiService.getInteractiveCourseDetail(courseSlug)
                _uiState.update { it.copy(course = response, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.message ?: "Failed to load course") }
            }
        }
    }
}

@Composable
fun InteractiveCourseScreen(
    courseSlug: String,
    onLessonClick: (String, String) -> Unit,
    onNavigateBack: () -> Unit,
    viewModel: InteractiveCourseViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(courseSlug) {
        viewModel.loadCourse(courseSlug)
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Surface(
            modifier = Modifier.fillMaxWidth(),
            color = MaterialTheme.colorScheme.surface
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                }
                Text(
                    text = uiState.course?.title ?: "Course",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
            }
        }

        when {
            uiState.isLoading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            uiState.error != null -> {
                Column(
                    modifier = Modifier.fillMaxSize().padding(16.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = uiState.error ?: "Something went wrong",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.error
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Surface(
                        onClick = { viewModel.loadCourse(courseSlug) },
                        shape = RoundedCornerShape(8.dp),
                        color = MaterialTheme.colorScheme.primaryContainer
                    ) {
                        Text(
                            text = "Retry",
                            modifier = Modifier.padding(horizontal = 24.dp, vertical = 10.dp),
                            style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                }
            }
            uiState.course != null -> {
                CourseDetailContent(
                    course = uiState.course!!,
                    onLessonClick = onLessonClick
                )
            }
        }
    }
}

@Composable
private fun CourseDetailContent(
    course: ApiInteractiveCourseDetailResponse,
    onLessonClick: (String, String) -> Unit
) {
    val categoryColor = try {
        Color(android.graphics.Color.parseColor(course.color))
    } catch (_: Exception) {
        MaterialTheme.colorScheme.primary
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 16.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item(key = "header") {
            Column(modifier = Modifier.fillMaxWidth()) {
                Surface(
                    shape = WebPillShape,
                    color = categoryColor.copy(alpha = 0.12f),
                    modifier = Modifier.align(Alignment.Start)
                ) {
                    Text(
                        text = course.categoryLabel.ifBlank { course.category },
                        style = MaterialTheme.typography.labelSmall,
                        color = categoryColor,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = course.title,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
                if (course.tagline.isNotBlank()) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = course.tagline,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (course.level.isNotBlank()) {
                        WebChip(text = course.level, selected = false)
                    }
                    if (course.ageRange.isNotBlank()) {
                        WebChip(text = "Ages ${course.ageRange}", selected = false)
                    }
                    WebChip(text = "${course.lessonCount} lessons", selected = false)
                    if (course.totalMinutes > 0) {
                        WebChip(text = "${course.totalMinutes} min", selected = false)
                    }
                }
                if (course.description.isNotBlank()) {
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        text = course.description,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 5,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                if (course.skills.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    val scrollState = rememberScrollState()
                    Row(
                        modifier = Modifier.horizontalScroll(scrollState),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        course.skills.forEach { skill ->
                            Surface(
                                shape = WebPillShape,
                                color = MaterialTheme.colorScheme.surfaceContainer,
                                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                            ) {
                                Text(
                                    text = skill,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }
                    }
                }
            }
        }

        item(key = "lessons_header") {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Lessons",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
        }

        items(count = course.lessons.size, key = { course.lessons[it].slug }) { index ->
            val lesson = course.lessons[index]
            LessonRow(
                lesson = lesson,
                index = index + 1,
                total = course.lessons.size,
                onClick = { onLessonClick(course.slug, lesson.slug) }
            )
        }

        item(key = "bottom_spacer") { Spacer(modifier = Modifier.height(92.dp)) }
    }
}

@Composable
private fun LessonRow(
    lesson: ApiInteractiveLessonSummary,
    index: Int,
    total: Int,
    onClick: () -> Unit
) {
    val simTypeLabel = when (lesson.simType) {
        "3d" -> "3D"
        "2d" -> "2D"
        "lab" -> "Lab"
        "coding" -> "Code"
        else -> ""
    }

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(10.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Surface(
                shape = WebPillShape,
                color = MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier.size(36.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Text(
                        text = "$index",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = lesson.title,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                if (lesson.summary.isNotBlank()) {
                    Text(
                        text = lesson.summary,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(4.dp))
                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (lesson.minutes > 0) {
                        Text(
                            text = "${lesson.minutes} min",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    if (simTypeLabel.isNotEmpty()) {
                        Text(
                            text = "\u00B7",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f)
                        )
                        Surface(
                            shape = WebPillShape,
                            color = MaterialTheme.colorScheme.secondaryContainer
                        ) {
                            Text(
                                text = simTypeLabel,
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onSecondaryContainer,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                }
            }
            Icon(
                imageVector = Icons.Filled.PlayArrow,
                contentDescription = "Start",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(24.dp)
            )
        }
    }
}