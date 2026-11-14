package com.neb.ians.ui.components

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Cancel
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiPoll
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.rounded.Poll
import androidx.compose.material.icons.rounded.Quiz
import androidx.compose.material.icons.rounded.Schedule
import androidx.compose.material3.IconButton
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.theme.nebFastSpatialSpec

// ---------------------------------------------------------------------------
// Poll UI model
// ---------------------------------------------------------------------------

data class PollOptionUi(
    val id: String,
    val text: String,
    val correct: Boolean,
    val votes: Int,
    val addedByMe: Boolean = false,
    val isAdded: Boolean = false
)

data class PollUi(
    val id: String,
    val question: String,
    val pollType: String,
    val allowMultiple: Boolean,
    val allowAddOptions: Boolean,
    val canAddOption: Boolean,
    val canRetract: Boolean,
    val explanation: String,
    val totalVotes: Int,
    val isExpired: Boolean,
    val expiresAt: Long,
    val leaderId: String?,
    val options: List<PollOptionUi>,
    val votedIds: Set<String>
) {
    val hasVoted: Boolean get() = votedIds.isNotEmpty()
    val isMcq: Boolean get() = pollType == "mcq"
    val showResults: Boolean get() = hasVoted || isExpired
}

fun ApiPoll.toPollUi(): PollUi = PollUi(
    id = id,
    question = question,
    pollType = pollType,
    allowMultiple = allowMultiple,
    allowAddOptions = allowAddOptions,
    canAddOption = canAddOption,
    canRetract = canRetract,
    explanation = explanation,
    totalVotes = totalVotes,
    isExpired = isExpired,
    expiresAt = expiresAt,
    leaderId = leaderId,
    options = options.sortedBy { it.order }.map {
        PollOptionUi(it.id, it.text, it.correct, it.votes, it.addedByMe, it.isAdded)
    },
    votedIds = userVoteIds.toSet()
)

private fun endsLabel(poll: PollUi): String {
    if (poll.isExpired) return "Ended"
    if (poll.expiresAt <= 0L) return ""
    val left = poll.expiresAt - System.currentTimeMillis()
    if (left <= 0L) return "Ended"
    val mins = left / 60_000
    return when {
        mins < 60 -> "Ends in ${mins.coerceAtLeast(1)} min"
        mins < 60 * 24 -> "Ends in ${mins / 60} h"
        else -> "Ends in ${mins / (60 * 24)} d"
    }
}

private fun votesLabel(n: Int) = if (n == 1) "1 vote" else "$n votes"

// ---------------------------------------------------------------------------
// The card (post page and comments)
// ---------------------------------------------------------------------------

/**
 * One poll, M3 Expressive. A white card with a hairline, no shadow. Options are white fields whose
 * stroke turns primary when picked; once the viewer has voted (or it ended) they become result bars
 * that spring out to their share, the leader in the stronger container, quiz answers in right and
 * wrong tones. When the author allows it, anyone can add an option from the card.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun NebPollCard(
    poll: PollUi,
    busy: Boolean,
    onVote: (List<String>) -> Unit,
    onAddOption: (String) -> Unit,
    onRetract: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    var picked by remember(poll.id, poll.votedIds) { mutableStateOf(setOf<String>()) }
    var adding by rememberSaveable(poll.id) { mutableStateOf(false) }
    var draft by rememberSaveable(poll.id) { mutableStateOf("") }
    val shape = RoundedCornerShape(24.dp)

    Column(
        modifier = modifier
            .fillMaxWidth()
            .animateContentSize(nebFastSpatialSpec())
            .clip(shape)
            .background(scheme.surfaceContainerLowest)
            .border(BorderStroke(1.dp, scheme.outlineVariant), shape)
            .padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Box(
                Modifier.size(34.dp).clip(RoundedCornerShape(12.dp)).background(scheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    if (poll.isMcq) Icons.Rounded.Quiz else Icons.Rounded.Poll, null,
                    Modifier.size(20.dp), tint = scheme.onPrimaryContainer
                )
            }
            Text(
                text = if (poll.isMcq) "Quiz" else "Poll",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                color = scheme.onSurface,
                modifier = Modifier.weight(1f)
            )
            val ends = endsLabel(poll)
            if (ends.isNotEmpty()) PollChip(ends, Icons.Rounded.Schedule, strong = !poll.isExpired)
        }

        if (poll.allowMultiple || (poll.allowAddOptions && !poll.isMcq)) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                if (poll.allowMultiple) PollChip("Multiple answers")
                if (poll.allowAddOptions && !poll.isMcq) PollChip("Open options")
            }
        }

        if (poll.question.isNotBlank()) {
            Text(
                text = poll.question,
                style = MaterialTheme.typography.titleMedium.copy(fontSize = 16.sp, lineHeight = 22.sp),
                fontWeight = FontWeight.SemiBold,
                color = scheme.onSurface
            )
        }

        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            poll.options.forEachIndexed { index, option ->
                if (poll.showResults) {
                    PollResultRow(poll, option, index)
                } else {
                    PollChoiceRow(
                        option = option,
                        multiple = poll.allowMultiple,
                        selected = option.id in picked,
                        enabled = !busy,
                        onClick = {
                            if (poll.allowMultiple) {
                                picked = if (option.id in picked) picked - option.id else picked + option.id
                            } else {
                                onVote(listOf(option.id))
                            }
                        }
                    )
                }
            }
        }

        if (poll.canAddOption) {
            if (adding) {
                AddOptionField(
                    value = draft,
                    onValueChange = { if (it.length <= 120) draft = it },
                    enabled = !busy,
                    onCancel = { adding = false; draft = "" },
                    onSubmit = {
                        val text = draft.trim()
                        if (text.isNotEmpty()) {
                            onAddOption(text)
                            draft = ""
                            adding = false
                        }
                    }
                )
            } else {
                Row(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .nebPressable(enabled = !busy, onClick = { adding = true })
                        .heightIn(min = 40.dp)
                        .padding(horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Icon(Icons.Rounded.Add, null, Modifier.size(18.dp), tint = scheme.primary)
                    Text("Add option", style = MaterialTheme.typography.labelLarge, color = scheme.primary)
                }
            }
        }

        AnimatedVisibility(visible = !poll.showResults && poll.allowMultiple && picked.isNotEmpty()) {
            NebButton(
                text = "Vote (${picked.size})",
                onClick = { onVote(picked.toList()) },
                size = NebButtonSize.Small,
                enabled = !busy,
                loading = busy,
                fillWidth = true
            )
        }

        if (poll.isMcq && poll.hasVoted && poll.explanation.isNotBlank()) {
            Text(
                text = poll.explanation,
                style = MaterialTheme.typography.bodySmall,
                color = scheme.onSurface,
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(scheme.surfaceContainerLow)
                    .padding(12.dp)
            )
        }

        Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = votesLabel(poll.totalVotes),
                style = MaterialTheme.typography.labelMedium,
                color = scheme.onSurfaceVariant,
                modifier = Modifier.weight(1f)
            )
            if (poll.canRetract && !busy) {
                Text(
                    text = "Change vote",
                    style = MaterialTheme.typography.labelLarge,
                    color = scheme.primary,
                    modifier = Modifier
                        .clip(RoundedCornerShape(18.dp))
                        .nebPressable(onClick = onRetract)
                        .padding(horizontal = 12.dp, vertical = 8.dp)
                )
            }
        }
    }
}

@Composable
private fun AddOptionField(
    value: String,
    onValueChange: (String) -> Unit,
    enabled: Boolean,
    onCancel: () -> Unit,
    onSubmit: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val focus = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
    val shape = RoundedCornerShape(18.dp)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 52.dp)
            .clip(shape)
            .background(scheme.surfaceContainerLowest)
            .border(BorderStroke(1.5.dp, scheme.primary), shape)
            .padding(start = 14.dp, end = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(Modifier.weight(1f)) {
            if (value.isEmpty()) {
                Text("New option", style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
            }
            BasicTextField(
                value = value,
                onValueChange = onValueChange,
                enabled = enabled,
                singleLine = true,
                textStyle = MaterialTheme.typography.bodyMedium.copy(color = scheme.onSurface),
                cursorBrush = SolidColor(scheme.primary),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                keyboardActions = KeyboardActions(onDone = { onSubmit() }),
                modifier = Modifier.fillMaxWidth().focusRequester(focus)
            )
        }
        IconButton(onClick = onCancel, enabled = enabled) {
            Icon(Icons.Rounded.Close, "Cancel", tint = scheme.onSurfaceVariant)
        }
        IconButton(onClick = onSubmit, enabled = enabled && value.isNotBlank()) {
            Icon(
                Icons.Rounded.Check, "Add option",
                tint = if (value.isNotBlank()) scheme.primary else scheme.outline
            )
        }
    }
}

// ---------------------------------------------------------------------------
// The feed preview
// ---------------------------------------------------------------------------

/**
 * A poll on a feed card: the same white card, smaller. It shows the question, up to three options
 * (as result bars once there is something to show) and how many more there are; tapping the card
 * opens the post, where the full card lives.
 */
@Composable
fun NebPollPreview(poll: PollUi, modifier: Modifier = Modifier) {
    val scheme = MaterialTheme.colorScheme
    val ordered = if (poll.showResults) poll.options.sortedByDescending { it.votes } else poll.options
    val shown = ordered.take(3)
    val more = poll.options.size - shown.size
    val shape = RoundedCornerShape(20.dp)
    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(shape)
            .background(scheme.surfaceContainerLowest)
            .border(BorderStroke(1.dp, scheme.outlineVariant), shape)
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(
                Modifier.size(26.dp).clip(RoundedCornerShape(9.dp)).background(scheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    if (poll.isMcq) Icons.Rounded.Quiz else Icons.Rounded.Poll, null,
                    Modifier.size(16.dp), tint = scheme.onPrimaryContainer
                )
            }
            Text(
                if (poll.isMcq) "Quiz" else "Poll",
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.Bold,
                color = scheme.onSurface,
                modifier = Modifier.weight(1f)
            )
            val ends = endsLabel(poll)
            Text(
                text = if (ends.isEmpty()) votesLabel(poll.totalVotes) else "${votesLabel(poll.totalVotes)} \u00B7 $ends",
                style = MaterialTheme.typography.labelSmall,
                color = scheme.onSurfaceVariant,
                maxLines = 1
            )
        }
        if (poll.question.isNotBlank()) {
            Text(
                poll.question,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                color = scheme.onSurface,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
        }
        shown.forEach { option -> PollPreviewRow(poll, option) }
        if (more > 0) {
            Text("+$more more", style = MaterialTheme.typography.labelMedium, color = scheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun PollPreviewRow(poll: PollUi, option: PollOptionUi) {
    val scheme = MaterialTheme.colorScheme
    val shape = RoundedCornerShape(14.dp)
    val frac = if (poll.totalVotes > 0) option.votes.toFloat() / poll.totalVotes else 0f
    val fill = if (option.id == poll.leaderId) scheme.primaryContainer else scheme.secondaryContainer
    val track = if (poll.showResults) scheme.surfaceContainerLow else scheme.surfaceContainerLowest
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 38.dp)
            .clip(shape)
            .background(track)
            .drawBehind { if (poll.showResults) drawRect(fill, size = Size(size.width * frac.coerceIn(0f, 1f), size.height)) }
            .border(BorderStroke(1.dp, scheme.outlineVariant), shape)
    ) {
        Row(
            Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                option.text,
                style = MaterialTheme.typography.labelLarge,
                color = scheme.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f)
            )
            if (poll.showResults) {
                Text(
                    "${if (poll.totalVotes > 0) option.votes * 100 / poll.totalVotes else 0}%",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = scheme.onSurface
                )
            }
        }
    }
}
