package com.neb.ians.ui.sim

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.api.ApiInteractiveLessonFull
import com.neb.ians.data.api.ApiInteractiveQuizQuestion
import com.neb.ians.data.api.ApiService
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.nebPressable
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class NativeLessonViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val api: ApiService
) : ViewModel() {
    private val course: String = savedStateHandle.get<String>("courseSlug").orEmpty()
    private val lesson: String = savedStateHandle.get<String>("lessonSlug").orEmpty()
    private val _lesson = MutableStateFlow<ApiInteractiveLessonFull?>(null)
    val lessonDetail: StateFlow<ApiInteractiveLessonFull?> = _lesson

    init {
        viewModelScope.launch { runCatching { api.getInteractiveLessonDetail(course, lesson) }.onSuccess { _lesson.value = it.lesson } }
    }
}

/**
 * A lesson whose simulation is native: the simulation and its controls first, then the lesson
 * (objectives, explanations, a fun fact and the quiz) loaded from the same API as the web page.
 * The simulation works offline; the text appears when it arrives.
 */
@Composable
fun NativeLessonScreen(sim: String, onNavigateBack: () -> Unit, viewModel: NativeLessonViewModel = hiltViewModel()) {
    val lesson by viewModel.lessonDetail.collectAsStateWithLifecycle()
    Column(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.surface)) {
        NebTopBar(showBrand = false, title = lesson?.title ?: "Lesson", onBack = onNavigateBack)
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
            NativeSims.Render(sim, Modifier.fillMaxWidth())
            lesson?.let { LessonBody(it) }
        }
    }
}

@Composable
private fun LessonBody(l: ApiInteractiveLessonFull) {
    Column(Modifier.padding(horizontal = 16.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
        if (l.summary.isNotBlank()) Text(l.summary, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
        if (l.objectives.isNotEmpty()) Card("What you'll discover") { l.objectives.forEach { Text("→  $it", style = MaterialTheme.typography.bodyMedium) } }
        l.knowledge.forEach { k ->
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(k.heading, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                k.body.split("\n\n").forEach { Text(it.trim(), style = MaterialTheme.typography.bodyMedium) }
            }
        }
        if (l.funFact.isNotBlank()) Card("Fun fact") { Text(l.funFact, style = MaterialTheme.typography.bodyMedium) }
        if (l.quiz.isNotEmpty()) Quiz(l.quiz)
        Text(" ", Modifier.padding(bottom = 24.dp))
    }
}

@Composable
private fun Card(title: String, content: @Composable () -> Unit) {
    val shape = RoundedCornerShape(18.dp)
    Column(
        Modifier.fillMaxWidth().clip(shape).background(MaterialTheme.colorScheme.surfaceContainerLow).padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        content()
    }
}

@Composable
private fun Quiz(questions: List<ApiInteractiveQuizQuestion>) {
    val picked = remember { mutableStateMapOf<Int, Int>() }
    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Text("Check your knowledge", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        questions.forEachIndexed { qi, q ->
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("${qi + 1}. ${q.q}", style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
                val chosen = picked[qi]
                q.options.forEachIndexed { oi, o ->
                    val shape = RoundedCornerShape(12.dp)
                    val right = chosen != null && oi == q.answer; val wrong = chosen == oi && oi != q.answer
                    Text(
                        o,
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.fillMaxWidth().clip(shape)
                            .border(1.dp, when { right -> androidx.compose.ui.graphics.Color(0xFF16A34A); wrong -> MaterialTheme.colorScheme.error; else -> MaterialTheme.colorScheme.outlineVariant }, shape)
                            .background(when { right -> androidx.compose.ui.graphics.Color(0x1A16A34A); wrong -> MaterialTheme.colorScheme.error.copy(alpha = 0.08f); else -> MaterialTheme.colorScheme.surface })
                            .nebPressable(enabled = chosen == null) { picked[qi] = oi }
                            .padding(12.dp)
                    )
                }
                if (chosen != null && q.explain.isNotBlank()) Text(q.explain, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        if (picked.size == questions.size) {
            val score = questions.indices.count { picked[it] == questions[it].answer }
            Text("You got $score of ${questions.size}.", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        }
    }
}
