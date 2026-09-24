@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.forum

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Poll
import androidx.compose.material.icons.rounded.Schedule
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebSelectField
import com.neb.ians.ui.components.NebTabRail
import com.neb.ians.ui.components.nebPressable

/**
 * The poll builder, folded away until it is asked for.
 *
 * A poll is two different things behind one switch: a vote, where every option
 * is equal, and a quiz, where one of them is right. The rail says which, and
 * the option rows change with it rather than growing a second set of controls.
 */
@Composable
fun PostPollPanel(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    onOpenDuration: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isQuiz = state.pollType == "mcq"

    PostPanel(modifier = modifier) {
        PostSwitchRow(
            icon = Icons.Rounded.Poll,
            title = "Add a poll",
            subtitle = if (state.pollEnabled) "Nebians answer before they reply" else "Ask a question with options",
            checked = state.pollEnabled,
            onCheckedChange = viewModel::togglePoll,
            enabled = !state.isSubmitting
        )

        AnimatedVisibility(visible = state.pollEnabled) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 12.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                NebTabRail(
                    tabs = listOf(NebRailTab("Vote"), NebRailTab("Quiz")),
                    selectedIndex = if (isQuiz) 1 else 0,
                    onSelect = { viewModel.onPollTypeChange(if (it == 1) "mcq" else "voting") },
                    contentPadding = PaddingValues(0.dp)
                )

                PostTextField(
                    value = state.pollQuestion,
                    onValueChange = viewModel::onPollQuestionChange,
                    label = "Question",
                    placeholder = if (isQuiz) "What is the SI unit of force?" else "Which one do you prefer?",
                    enabled = !state.isSubmitting
                )

                state.pollOptions.forEachIndexed { index, option ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        PostTextField(
                            value = option.text,
                            onValueChange = { viewModel.onPollOptionChange(index, it) },
                            label = "Option ${index + 1}",
                            modifier = Modifier.weight(1f),
                            enabled = !state.isSubmitting
                        )
                        if (isQuiz) {
                            CorrectMark(
                                correct = option.isCorrect,
                                onClick = { viewModel.togglePollOptionCorrect(index) }
                            )
                        }
                        if (state.pollOptions.size > 2) {
                            OptionAction(
                                onClick = { viewModel.removePollOption(index) },
                                description = "Remove option ${index + 1}"
                            )
                        }
                    }
                }

                if (state.pollOptions.size < 6) {
                    NebButton(
                        text = "Add option",
                        onClick = viewModel::addPollOption,
                        icon = Icons.Rounded.Add,
                        tone = NebButtonTone.Tonal,
                        size = NebButtonSize.Small,
                        enabled = !state.isSubmitting
                    )
                }

                if (isQuiz) {
                    PostTextField(
                        value = state.pollExplanation,
                        onValueChange = viewModel::onPollExplanationChange,
                        label = "Explanation",
                        placeholder = "Shown after answering",
                        singleLine = false,
                        minLines = 2,
                        supporting = "Optional",
                        enabled = !state.isSubmitting
                    )
                } else {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Allow more than one answer",
                            style = MaterialTheme.typography.bodyLarge,
                            modifier = Modifier.weight(1f)
                        )
                        Switch(
                            checked = state.pollAllowMultiple,
                            onCheckedChange = viewModel::onPollAllowMultipleChange,
                            enabled = !state.isSubmitting
                        )
                    }
                }

                NebSelectField(
                    label = "Closes",
                    values = listOfNotNull(
                        CreatePostUiState.POLL_DURATIONS
                            .firstOrNull { it.first == state.pollDurationMs }
                            ?.second
                            ?.takeIf { state.pollDurationMs != 0L }
                    ),
                    placeholder = "Never",
                    icon = Icons.Rounded.Schedule,
                    onClick = onOpenDuration
                )
            }
        }
    }
}

@Composable
private fun CorrectMark(correct: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .nebPressable(onClick = onClick)
            .size(40.dp)
            .clip(CircleShape)
            .background(
                if (correct) MaterialTheme.colorScheme.onSurface
                else MaterialTheme.colorScheme.surfaceContainerHighest
            ),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = Icons.Rounded.Check,
            contentDescription = if (correct) "Correct answer" else "Mark as correct",
            tint = if (correct) MaterialTheme.colorScheme.surface
            else MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(18.dp)
        )
    }
}

@Composable
private fun OptionAction(onClick: () -> Unit, description: String) {
    Box(
        modifier = Modifier
            .nebPressable(onClick = onClick)
            .size(40.dp)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = Icons.Rounded.Close,
            contentDescription = description,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(16.dp)
        )
    }
}

/** Nothing here yet is a poll the server would accept. */
fun pollProblem(state: CreatePostUiState): String? {
    if (!state.pollEnabled || state.isEditMode) return null
    val filled = state.pollOptions.filter { it.text.isNotBlank() }
    return when {
        state.pollQuestion.isBlank() -> "Your poll needs a question"
        filled.size < 2 -> "Your poll needs two options"
        state.pollType == "mcq" && filled.none { it.isCorrect } -> "Mark the correct answer"
        else -> null
    }
}
