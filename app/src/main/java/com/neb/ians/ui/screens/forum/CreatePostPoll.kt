@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import com.neb.ians.ui.components.NebChoiceChips
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.nebPressable

/**
 * The poll builder, as the web draws it: a title row with Remove, a Voting / MCQ pill pair,
 * the question, the options, then Add option beside the closing time.
 *
 * It only exists while the poll tool in the footer is on.
 */
@Composable
fun PostPollPanel(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    modifier: Modifier = Modifier
) {
    val isQuiz = state.pollType == "mcq"
    val scheme = MaterialTheme.colorScheme

    PostPanel(modifier = modifier) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            com.neb.ians.ui.components.NebIcon(
                com.neb.ians.ui.components.NebIcons.Poll, null, size = 20.dp, tint = scheme.primary
            )
            Text(
                text = "Poll / Quiz",
                style = MaterialTheme.typography.titleSmall,
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 8.dp)
            )
            NebButton(
                text = "Remove",
                onClick = { viewModel.togglePoll(false) },
                icon = Icons.Rounded.Close,
                tone = NebButtonTone.Tonal,
                size = NebButtonSize.Small,
                enabled = !state.isSubmitting
            )
        }

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 12.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            NebChoiceChips(
                options = listOf("Voting poll", "MCQ quiz"),
                selectedIndex = if (isQuiz) 1 else 0,
                onSelect = { viewModel.onPollTypeChange(if (it == 1) "mcq" else "voting") },
                enabled = !state.isSubmitting
            )

            PostInput(
                value = state.pollQuestion,
                onValueChange = viewModel::onPollQuestionChange,
                placeholder = "Ask a poll question...",
                enabled = !state.isSubmitting
            )

            state.pollOptions.forEachIndexed { index, option ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    PostInput(
                        value = option.text,
                        onValueChange = { viewModel.onPollOptionChange(index, it) },
                        placeholder = "Option ${index + 1}",
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

            Text(
                text = "Closes",
                style = MaterialTheme.typography.labelLarge,
                color = scheme.onSurfaceVariant
            )
            NebChoiceChips(
                options = CreatePostUiState.POLL_DURATIONS.map { it.second },
                selectedIndex = CreatePostUiState.POLL_DURATIONS.indexOfFirst { it.first == state.pollDurationMs },
                onSelect = { viewModel.onPollDurationChange(CreatePostUiState.POLL_DURATIONS[it].first) },
                enabled = !state.isSubmitting
            )

            if (isQuiz) {
                Text(
                    text = "Tick the correct answer",
                    style = MaterialTheme.typography.labelLarge,
                    color = scheme.onSurfaceVariant
                )
                PostInput(
                    value = state.pollExplanation,
                    onValueChange = viewModel::onPollExplanationChange,
                    placeholder = "Explanation for the correct answer (optional)...",
                    singleLine = false,
                    minLines = 2,
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
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Let others add options",
                        style = MaterialTheme.typography.bodyLarge,
                        modifier = Modifier.weight(1f)
                    )
                    Switch(
                        checked = state.pollAllowAddOptions,
                        onCheckedChange = viewModel::onPollAllowAddOptionsChange,
                        enabled = !state.isSubmitting
                    )
                }
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
        com.neb.ians.ui.components.NebIcon(
            com.neb.ians.ui.components.NebIcons.Check,
            if (correct) "Correct answer" else "Mark as correct",
            size = 18.dp,
            tint = if (correct) MaterialTheme.colorScheme.surface
            else MaterialTheme.colorScheme.onSurfaceVariant
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
        com.neb.ians.ui.components.NebIcon(
            com.neb.ians.ui.components.NebIcons.Close, description, size = 16.dp,
            tint = MaterialTheme.colorScheme.onSurfaceVariant
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
