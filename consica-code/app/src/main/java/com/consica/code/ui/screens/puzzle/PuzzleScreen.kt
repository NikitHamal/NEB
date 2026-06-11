package com.consica.code.ui.screens.puzzle

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.designsystem.CodeTextStyle
import com.consica.code.core.designsystem.EditorBackground
import com.consica.code.core.designsystem.EditorText
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.Lesson
import com.consica.code.core.model.TerraExpression
import com.consica.code.data.content.LessonCatalog
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.common.LeafConfetti
import com.consica.code.ui.common.appViewModel
import com.consica.code.util.SoundManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class PuzzleUiState(
    val tray: List<String> = emptyList(),
    val placed: List<String> = emptyList(),
    val checked: Boolean = false,
    val correct: Boolean = false,
    val completed: Boolean = false,
)

class PuzzleViewModel(
    private val container: AppContainer,
    val lesson: Lesson,
) : ViewModel() {

    val user: StateFlow<UserState?> = container.prefs.userState
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)

    private val puzzle = lesson.puzzle!!

    private val _state = MutableStateFlow(
        PuzzleUiState(tray = (puzzle.solution + puzzle.distractors).shuffled()),
    )
    val state: StateFlow<PuzzleUiState> = _state

    val hasDistractors: Boolean get() = puzzle.distractors.isNotEmpty()

    fun place(block: String) {
        val s = _state.value
        val trayIndex = s.tray.indexOf(block)
        if (trayIndex == -1) return
        _state.value = s.copy(
            tray = s.tray.toMutableList().also { it.removeAt(trayIndex) },
            placed = s.placed + block,
            checked = false,
        )
        container.sound.play(SoundManager.Effect.TAP)
    }

    fun remove(index: Int) {
        val s = _state.value
        if (index !in s.placed.indices) return
        val block = s.placed[index]
        _state.value = s.copy(
            tray = s.tray + block,
            placed = s.placed.toMutableList().also { it.removeAt(index) },
            checked = false,
        )
    }

    fun move(from: Int, to: Int) {
        val s = _state.value
        if (from !in s.placed.indices || to !in s.placed.indices || from == to) return
        val list = s.placed.toMutableList()
        val item = list.removeAt(from)
        list.add(to, item)
        _state.value = s.copy(placed = list, checked = false)
    }

    fun shuffleTray() {
        _state.value = _state.value.copy(tray = _state.value.tray.shuffled())
    }

    fun check() {
        val s = _state.value
        val correct = s.placed == puzzle.solution
        _state.value = s.copy(checked = true, correct = correct)
        if (correct) {
            container.sound.play(SoundManager.Effect.REWARD)
            viewModelScope.launch {
                container.learning.completeLesson(lesson)
                _state.value = _state.value.copy(completed = true)
            }
        } else {
            container.sound.play(SoundManager.Effect.GENTLE_ERROR)
            viewModelScope.launch { container.learning.recordAttempt(lesson.id, null) }
        }
    }
}

@Composable
fun PuzzleScreen(
    lessonId: String,
    onBack: () -> Unit,
    onComplete: () -> Unit,
) {
    val lesson = LessonCatalog.byId[lessonId]
    if (lesson?.puzzle == null) {
        onBack()
        return
    }
    val viewModel = appViewModel(key = "puzzle_$lessonId") { PuzzleViewModel(it, lesson) }
    val state by viewModel.state.collectAsState()
    val user = viewModel.user.collectAsState().value ?: return

    Box(Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .navigationBarsPadding(),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.action_back))
                }
                Column(Modifier.weight(1f)) {
                    Text(stringResource(lesson.titleRes), style = MaterialTheme.typography.titleMedium, maxLines = 1)
                    Text(
                        stringResource(R.string.puzzle_title),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                TextButton(onClick = viewModel::shuffleTray) {
                    Text(stringResource(R.string.action_shuffle))
                }
            }

            Column(
                modifier = Modifier
                    .weight(1f)
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 16.dp),
            ) {
                // Prompt
                Text(
                    stringResource(lesson.puzzle.prompt.resFor(user.ageGroup)),
                    style = MaterialTheme.typography.bodyLarge,
                )
                if (viewModel.hasDistractors && user.ageGroup != AgeGroup.KIDS) {
                    Text(
                        stringResource(R.string.puzzle_distractor_hint),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.tertiary,
                        modifier = Modifier.padding(top = 4.dp),
                    )
                }

                Box(Modifier.height(12.dp))

                // Answer area
                Text(
                    stringResource(R.string.puzzle_answer_title),
                    style = MaterialTheme.typography.titleSmall,
                )
                Box(Modifier.height(6.dp))
                Surface(
                    shape = RoundedCornerShape(20.dp),
                    color = EditorBackground,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(Modifier.padding(10.dp)) {
                        if (state.placed.isEmpty()) {
                            Text(
                                stringResource(R.string.puzzle_tap_to_place),
                                style = MaterialTheme.typography.bodySmall,
                                color = EditorText.copy(alpha = 0.5f),
                                modifier = Modifier.padding(12.dp),
                            )
                        } else {
                            ReorderableBlocks(
                                blocks = state.placed,
                                wrongHighlight = state.checked && !state.correct,
                                onMove = viewModel::move,
                                onRemove = viewModel::remove,
                            )
                        }
                    }
                }

                Box(Modifier.height(16.dp))

                // Tray
                Text(
                    stringResource(R.string.puzzle_tray_title),
                    style = MaterialTheme.typography.titleSmall,
                )
                Box(Modifier.height(6.dp))
                state.tray.forEach { block ->
                    Surface(
                        shape = MaterialTheme.shapes.medium,
                        color = MaterialTheme.colorScheme.surface,
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 3.dp)
                            .clickable { viewModel.place(block) },
                    ) {
                        Text(
                            text = block,
                            style = CodeTextStyle,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
                        )
                    }
                }
                Box(Modifier.height(16.dp))
            }

            // Feedback + check button
            if (state.checked) {
                val feedbackRes = if (state.correct) {
                    when (user.ageGroup) {
                        AgeGroup.KIDS -> R.string.puzzle_correct_kids
                        AgeGroup.TEENS -> R.string.puzzle_correct_teens
                        AgeGroup.PRO -> R.string.puzzle_correct_pro
                    }
                } else {
                    when (user.ageGroup) {
                        AgeGroup.KIDS -> R.string.puzzle_wrong_kids
                        AgeGroup.TEENS -> R.string.puzzle_wrong_teens
                        AgeGroup.PRO -> R.string.puzzle_wrong_pro
                    }
                }
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(horizontal = 16.dp),
                ) {
                    TerraAvatar(
                        expression = if (state.correct) TerraExpression.EXCITED else TerraExpression.ENCOURAGING,
                        size = 48.dp,
                        bounce = false,
                    )
                    Box(Modifier.width(8.dp))
                    Text(
                        stringResource(feedbackRes),
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.weight(1f),
                    )
                }
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                if (state.completed) {
                    Button(
                        onClick = onComplete,
                        shape = PillShape,
                        modifier = Modifier
                            .weight(1f)
                            .height(54.dp),
                    ) {
                        Text(stringResource(R.string.lesson_back_to_map))
                    }
                } else {
                    Button(
                        onClick = viewModel::check,
                        enabled = state.placed.isNotEmpty(),
                        shape = PillShape,
                        modifier = Modifier
                            .weight(1f)
                            .height(54.dp),
                    ) {
                        Text(stringResource(R.string.action_check), style = MaterialTheme.typography.labelLarge)
                    }
                }
            }
        }

        if (state.completed) {
            LeafConfetti(Modifier.fillMaxSize())
        }
    }
}

/**
 * Placed blocks with native Compose drag-to-reorder (long-press drag) plus
 * accessible up/down/remove buttons as a non-gesture alternative.
 */
@Composable
private fun ReorderableBlocks(
    blocks: List<String>,
    wrongHighlight: Boolean,
    onMove: (from: Int, to: Int) -> Unit,
    onRemove: (index: Int) -> Unit,
) {
    var draggingIndex by remember { mutableStateOf(-1) }
    var dragOffset by remember { mutableStateOf(0f) }
    var itemHeightPx by remember { mutableStateOf(1f) }

    val blockDescription = stringResource(R.string.a11y_drag_block)

    Column {
        blocks.forEachIndexed { index, block ->
            val isDragging = index == draggingIndex
            val borderColor by animateColorAsState(
                targetValue = when {
                    wrongHighlight -> MaterialTheme.colorScheme.error
                    isDragging -> MaterialTheme.colorScheme.tertiary
                    else -> MaterialTheme.colorScheme.outline
                },
                label = "blockBorder",
            )
            Surface(
                shape = MaterialTheme.shapes.small,
                color = if (isDragging) {
                    MaterialTheme.colorScheme.primaryContainer
                } else {
                    EditorBackground.copy(alpha = 0.4f)
                },
                border = BorderStroke(1.dp, borderColor),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 2.dp)
                    .zIndex(if (isDragging) 1f else 0f)
                    .graphicsLayer {
                        translationY = if (isDragging) dragOffset else 0f
                    }
                    .onSizeChanged { size -> if (size.height > 0) itemHeightPx = size.height.toFloat() }
                    .pointerInput(index, blocks.size) {
                        detectDragGesturesAfterLongPress(
                            onDragStart = {
                                draggingIndex = index
                                dragOffset = 0f
                            },
                            onDrag = { change, amount ->
                                change.consume()
                                dragOffset += amount.y
                                val shift = (dragOffset / itemHeightPx).toInt()
                                if (shift != 0) {
                                    val target = (draggingIndex + shift).coerceIn(0, blocks.lastIndex)
                                    if (target != draggingIndex) {
                                        onMove(draggingIndex, target)
                                        draggingIndex = target
                                        dragOffset -= shift * itemHeightPx
                                    }
                                }
                            },
                            onDragEnd = {
                                draggingIndex = -1
                                dragOffset = 0f
                            },
                            onDragCancel = {
                                draggingIndex = -1
                                dragOffset = 0f
                            },
                        )
                    }
                    .semantics { contentDescription = blockDescription },
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = block,
                        style = CodeTextStyle,
                        color = if (isDragging) MaterialTheme.colorScheme.onPrimaryContainer else EditorText,
                        modifier = Modifier
                            .weight(1f)
                            .padding(horizontal = 12.dp, vertical = 10.dp),
                    )
                    IconButton(
                        onClick = { if (index > 0) onMove(index, index - 1) },
                        modifier = Modifier.size(34.dp),
                    ) {
                        Icon(
                            Icons.Filled.KeyboardArrowUp,
                            contentDescription = stringResource(R.string.a11y_move_up),
                            tint = if (isDragging) MaterialTheme.colorScheme.onPrimaryContainer else EditorText.copy(alpha = 0.7f),
                        )
                    }
                    IconButton(
                        onClick = { if (index < blocks.lastIndex) onMove(index, index + 1) },
                        modifier = Modifier.size(34.dp),
                    ) {
                        Icon(
                            Icons.Filled.KeyboardArrowDown,
                            contentDescription = stringResource(R.string.a11y_move_down),
                            tint = if (isDragging) MaterialTheme.colorScheme.onPrimaryContainer else EditorText.copy(alpha = 0.7f),
                        )
                    }
                    IconButton(
                        onClick = { onRemove(index) },
                        modifier = Modifier.size(34.dp),
                    ) {
                        Icon(
                            Icons.Filled.Close,
                            contentDescription = stringResource(R.string.a11y_remove_block),
                            tint = if (isDragging) MaterialTheme.colorScheme.onPrimaryContainer else EditorText.copy(alpha = 0.7f),
                        )
                    }
                }
            }
        }
    }
}


