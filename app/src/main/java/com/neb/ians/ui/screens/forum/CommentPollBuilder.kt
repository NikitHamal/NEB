package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiPollCreate
import com.neb.ians.data.api.ApiPollOptionCreate
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChoiceChips

/** A poll being written inside the comment bar. */
data class CommentPollDraft(
    val question: String = "",
    val options: List<String> = listOf("", ""),
    val allowMultiple: Boolean = false,
    val allowAddOptions: Boolean = true,
    val durationMs: Long = 0L
) {
    private val filled: List<String> get() = options.map { it.trim() }.filter { it.isNotEmpty() }

    /** Two different, non-empty options and a question. */
    val isReady: Boolean
        get() = question.isNotBlank() &&
            filled.size >= 2 &&
            filled.map { it.lowercase() }.toSet().size == filled.size

    fun toRequest(): ApiPollCreate = ApiPollCreate(
        question = question.trim(),
        pollType = "voting",
        allowMultiple = allowMultiple,
        allowAddOptions = allowAddOptions,
        durationMs = durationMs,
        options = filled.mapIndexed { i, t -> ApiPollOptionCreate(text = t, index = i) }
    )
}

/**
 * The poll builder for a comment: a question, up to six options, whether more than one answer is
 * allowed and whether members can add their own option, then the closing time.
 */
@Composable
fun CommentPollBuilder(
    draft: CommentPollDraft,
    onChange: (CommentPollDraft) -> Unit,
    onClose: () -> Unit,
    enabled: Boolean,
    modifier: Modifier = Modifier
) {
    PostPanel(modifier = modifier.padding(bottom = 8.dp), padding = 12) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Poll",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.weight(1f)
            )
            NebButton(
                text = "Remove",
                onClick = onClose,
                icon = Icons.Rounded.Close,
                tone = NebButtonTone.Tonal,
                size = NebButtonSize.Compact,
                enabled = enabled
            )
        }
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            PostInput(
                value = draft.question,
                onValueChange = { if (it.length <= 300) onChange(draft.copy(question = it)) },
                placeholder = "Ask a question",
                enabled = enabled
            )
            draft.options.forEachIndexed { index, text ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    PostInput(
                        value = text,
                        onValueChange = { v ->
                            if (v.length <= 120) {
                                onChange(draft.copy(options = draft.options.mapIndexed { i, o -> if (i == index) v else o }))
                            }
                        },
                        placeholder = "Option ${index + 1}",
                        modifier = Modifier.weight(1f),
                        enabled = enabled
                    )
                    if (draft.options.size > 2) {
                        NebButton(
                            text = "Remove",
                            onClick = { onChange(draft.copy(options = draft.options.filterIndexed { i, _ -> i != index })) },
                            icon = Icons.Rounded.Close,
                            tone = NebButtonTone.Text,
                            size = NebButtonSize.Compact,
                            enabled = enabled
                        )
                    }
                }
            }
            if (draft.options.size < 6) {
                NebButton(
                    text = "Add option",
                    onClick = { onChange(draft.copy(options = draft.options + "")) },
                    icon = Icons.Rounded.Add,
                    tone = NebButtonTone.Tonal,
                    size = NebButtonSize.Small,
                    enabled = enabled
                )
            }
            SwitchLine("Allow more than one answer", draft.allowMultiple, enabled) {
                onChange(draft.copy(allowMultiple = it))
            }
            SwitchLine("Let others add options", draft.allowAddOptions, enabled) {
                onChange(draft.copy(allowAddOptions = it))
            }
            NebChoiceChips(
                options = CreatePostUiState.POLL_DURATIONS.map { it.second },
                selectedIndex = CreatePostUiState.POLL_DURATIONS.indexOfFirst { it.first == draft.durationMs },
                onSelect = { onChange(draft.copy(durationMs = CreatePostUiState.POLL_DURATIONS[it].first)) },
                enabled = enabled
            )
        }
    }
}

@Composable
private fun SwitchLine(label: String, checked: Boolean, enabled: Boolean, onChange: (Boolean) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.weight(1f)
        )
        Switch(checked = checked, onCheckedChange = onChange, enabled = enabled)
    }
}
