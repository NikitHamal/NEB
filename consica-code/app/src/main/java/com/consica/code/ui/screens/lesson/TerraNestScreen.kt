package com.consica.code.ui.screens.lesson

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.Lesson
import com.consica.code.core.model.LessonType
import com.consica.code.core.model.TerraExpression
import com.consica.code.data.content.LessonCatalog
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.character.CharacterGuide
import com.consica.code.ui.common.LeafConfetti
import com.consica.code.ui.common.appViewModel
import com.consica.code.util.SoundManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class LessonUiState(
    val stepIndex: Int = 0,
    val completed: Boolean = false,
    val newBadges: List<String> = emptyList(),
)

class LessonViewModel(
    private val container: AppContainer,
    val lesson: Lesson,
) : ViewModel() {

    val user: StateFlow<UserState?> = container.prefs.userState
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)

    private val _state = MutableStateFlow(LessonUiState())
    val state: StateFlow<LessonUiState> = _state

    fun nextStep() {
        val s = _state.value
        if (s.stepIndex < lesson.steps.lastIndex) {
            _state.value = s.copy(stepIndex = s.stepIndex + 1)
        }
    }

    val isLastStep: Boolean get() = _state.value.stepIndex >= lesson.steps.lastIndex

    /** Completes TUTORIAL lessons directly (no code/puzzle phase). */
    fun completeTutorial() {
        if (_state.value.completed) return
        viewModelScope.launch {
            val badges = container.learning.completeLesson(lesson)
            container.sound.play(SoundManager.Effect.REWARD)
            _state.value = _state.value.copy(completed = true, newBadges = badges)
        }
    }
}

@Composable
fun TerraNestScreen(
    lessonId: String,
    onStartCoding: () -> Unit,
    onStartPuzzle: () -> Unit,
    onBack: () -> Unit,
    onLessonComplete: () -> Unit,
    onNextLesson: (nextId: String, isPuzzle: Boolean) -> Unit,
) {
    val lesson = LessonCatalog.byId[lessonId] ?: run {
        onBack()
        return
    }
    val viewModel = appViewModel(key = "lesson_$lessonId") { LessonViewModel(it, lesson) }
    val state by viewModel.state.collectAsState()
    val user = viewModel.user.collectAsState().value ?: return

    val ageGroup = user.ageGroup

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f),
                        MaterialTheme.colorScheme.background,
                    ),
                ),
            ),
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .navigationBarsPadding(),
        ) {
            // Top bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                IconButton(onClick = onBack) {
                    Icon(
                        Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = stringResource(R.string.action_back),
                    )
                }
                Column(Modifier.weight(1f)) {
                    Text(
                        stringResource(lesson.titleRes),
                        style = MaterialTheme.typography.titleMedium,
                        maxLines = 1,
                    )
                    Text(
                        stringResource(lesson.biome.titleRes),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                if (ageGroup == AgeGroup.PRO && lesson.type == LessonType.CODE) {
                    TextButton(onClick = onStartCoding) {
                        Text(stringResource(R.string.lesson_skip_to_code))
                    }
                }
            }

            if (lesson.steps.isNotEmpty()) {
                LinearProgressIndicator(
                    progress = { (state.stepIndex + 1f) / lesson.steps.size },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp),
                )
            }

            Box(Modifier.weight(1f))

            if (!state.completed) {
                val step = lesson.steps.getOrNull(state.stepIndex)
                if (step != null) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .verticalScroll(rememberScrollState())
                            .padding(16.dp),
                    ) {
                        CharacterGuide(
                            text = stringResource(step.text.resFor(ageGroup)),
                            expression = step.expression,
                            ageGroup = ageGroup,
                            guidance = user.guidance,
                            codeSnippet = step.codeSnippet,
                            onTap = {
                                if (!viewModel.isLastStep) viewModel.nextStep()
                            },
                        )
                        Box(Modifier.height(16.dp))

                        if (viewModel.isLastStep || state.stepIndex == lesson.steps.lastIndex) {
                            FinalActionButton(
                                lesson = lesson,
                                onStartCoding = onStartCoding,
                                onStartPuzzle = onStartPuzzle,
                                onCompleteTutorial = viewModel::completeTutorial,
                            )
                        } else {
                            Text(
                                stringResource(R.string.lesson_tap_to_continue),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                textAlign = TextAlign.Center,
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }
                    }
                }
            } else {
                CompletionPanel(
                    lesson = lesson,
                    onLessonComplete = onLessonComplete,
                    onNextLesson = onNextLesson,
                )
            }
        }

        if (state.completed) {
            LeafConfetti(modifier = Modifier.fillMaxSize())
        }
    }
}

@Composable
private fun FinalActionButton(
    lesson: Lesson,
    onStartCoding: () -> Unit,
    onStartPuzzle: () -> Unit,
    onCompleteTutorial: () -> Unit,
) {
    when (lesson.type) {
        LessonType.CODE -> Button(
            onClick = onStartCoding,
            shape = PillShape,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text(stringResource(R.string.lesson_start_coding), style = MaterialTheme.typography.labelLarge)
        }
        LessonType.PUZZLE -> Button(
            onClick = onStartPuzzle,
            shape = PillShape,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text(stringResource(R.string.lesson_start_puzzle), style = MaterialTheme.typography.labelLarge)
        }
        LessonType.TUTORIAL -> Button(
            onClick = onCompleteTutorial,
            shape = PillShape,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text(stringResource(R.string.action_done), style = MaterialTheme.typography.labelLarge)
        }
    }
}

@Composable
private fun CompletionPanel(
    lesson: Lesson,
    onLessonComplete: () -> Unit,
    onNextLesson: (nextId: String, isPuzzle: Boolean) -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        com.consica.code.ui.character.TerraAvatar(
            expression = TerraExpression.PROUD,
            size = 110.dp,
        )
        Box(Modifier.height(12.dp))
        Text(
            stringResource(R.string.lesson_complete_title),
            style = MaterialTheme.typography.headlineSmall,
            textAlign = TextAlign.Center,
        )
        Box(Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Text(
                stringResource(R.string.lesson_xp_earned, lesson.xpReward),
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(
                stringResource(R.string.lesson_sun_earned, lesson.sunReward),
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.tertiary,
            )
            Text(
                stringResource(R.string.lesson_water_earned, lesson.waterReward),
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.secondary,
            )
        }
        Box(Modifier.height(24.dp))
        val next = LessonCatalog.nextAfter(lesson.id)
        if (next != null) {
            Button(
                onClick = { onNextLesson(next.id, false) },
                shape = PillShape,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp),
            ) {
                Text(stringResource(R.string.lesson_next_lesson))
            }
            Box(Modifier.height(8.dp))
        }
        TextButton(onClick = onLessonComplete) {
            Text(stringResource(R.string.lesson_back_to_map))
        }
    }
}
