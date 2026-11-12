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
 * One poll, M3 Expressive. Tonal surface, no frame, no shadow. Voting rows turn into result
 * bars once the viewer has voted or the poll has ended; the leading option takes the stronger
 * container. When the author allows it, anyone can add an option from the card.
 */
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

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .animateContentSize(),
        shape = RoundedCornerShape(28.dp),
        color = scheme.surfaceContainerLow
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                PollTag(if (poll.isMcq) "Quiz" else "Poll", strong = true)
                if (poll.allowMultiple) PollTag("Multiple answers")
                if (poll.allowAddOptions && !poll.isMcq) PollTag("Open options")
            }

            if (poll.question.isNotBlank()) {
                Text(
                    text = poll.question,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = scheme.onSurface
                )
            }

            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                poll.options.forEach { option ->
                    if (poll.showResults) {
                        PollResultRow(poll, option)
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
                            .clip(RoundedCornerShape(percent = 50))
                            .clickable(enabled = !busy) { adding = true }
                            .heightIn(min = 40.dp)
                            .padding(horizontal = 12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(Icons.Rounded.Add, null, Modifier.size(18.dp), tint = scheme.primary)
                        Text(
                            "Add option",
                            style = MaterialTheme.typography.labelLarge,
                            color = scheme.primary
                        )
                    }
                }
            }

            if (!poll.showResults && poll.allowMultiple && picked.isNotEmpty()) {
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
                Surface(
                    shape = RoundedCornerShape(16.dp),
                    color = scheme.secondaryContainer,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = poll.explanation,
                        style = MaterialTheme.typography.bodySmall,
                        color = scheme.onSecondaryContainer,
                        modifier = Modifier.padding(12.dp)
                    )
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                val ends = endsLabel(poll)
                Text(
                    text = if (ends.isEmpty()) votesLabel(poll.totalVotes) else "${votesLabel(poll.totalVotes)}  \u00B7  $ends",
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
                            .clip(RoundedCornerShape(percent = 50))
                            .clickable { onRetract() }
                            .padding(horizontal = 10.dp, vertical = 6.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun PollTag(label: String, strong: Boolean = false) {
    val scheme = MaterialTheme.colorScheme
    Surface(
        shape = RoundedCornerShape(percent = 50),
        color = if (strong) scheme.primaryContainer else scheme.secondaryContainer
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.SemiBold,
            color = if (strong) scheme.onPrimaryContainer else scheme.onSecondaryContainer,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
        )
    }
}

@Composable
private fun PollChoiceRow(
    option: PollOptionUi,
    multiple: Boolean,
    selected: Boolean,
    enabled: Boolean,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val markShape = if (multiple) RoundedCornerShape(7.dp) else RoundedCornerShape(percent = 50)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(20.dp))
            .background(if (selected) scheme.primaryContainer else scheme.surfaceContainerHighest)
            .clickable(enabled = enabled, onClick = onClick)
            .heightIn(min = 52.dp)
            .padding(horizontal = 14.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .size(22.dp)
                .clip(markShape)
                .background(if (selected) scheme.primary else scheme.outline),
            contentAlignment = Alignment.Center
        ) {
            if (selected) {
                Icon(Icons.Rounded.Check, null, Modifier.size(16.dp), tint = scheme.onPrimary)
            } else {
                Box(
                    Modifier
                        .size(18.dp)
                        .clip(markShape)
                        .background(scheme.surfaceContainerHighest)
                )
            }
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = option.text,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
                color = if (selected) scheme.onPrimaryContainer else scheme.onSurface
            )
            val by = when {
                option.addedByMe -> "Added by you"
                option.isAdded -> "Added by a member"
                else -> ""
            }
            if (by.isNotEmpty()) {
                Text(
                    by,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (selected) scheme.onPrimaryContainer else scheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun PollResultRow(poll: PollUi, option: PollOptionUi) {
    val scheme = MaterialTheme.colorScheme
    val total = poll.totalVotes.coerceAtLeast(1)
    val fraction = option.votes.toFloat() / total
    val animated by animateFloatAsState(fraction, tween(550), label = "pollFill")
    val mine = option.id in poll.votedIds
    val leader = option.id == poll.leaderId
    val quiz = poll.isMcq && poll.hasVoted
    val wrongPick = quiz && mine && !option.correct
    val rightOne = quiz && option.correct

    val fill = when {
        wrongPick -> scheme.errorContainer
        rightOne -> scheme.tertiaryContainer
        leader -> scheme.primaryContainer
        else -> scheme.secondaryContainer
    }
    val pct = if (poll.totalVotes > 0) option.votes * 100 / poll.totalVotes else 0

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 52.dp)
            .clip(RoundedCornerShape(20.dp))
            .background(scheme.surfaceContainerHighest)
    ) {
        Box(
            modifier = Modifier
                .matchParentSize()
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(animated.coerceIn(0f, 1f))
                    .background(fill)
            )
        }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            when {
                rightOne -> Icon(Icons.Rounded.CheckCircle, "Correct", Modifier.size(18.dp), tint = scheme.onSurface)
                wrongPick -> Icon(Icons.Rounded.Cancel, "Your answer", Modifier.size(18.dp), tint = scheme.error)
                mine -> Icon(Icons.Rounded.CheckCircle, "Your vote", Modifier.size(18.dp), tint = scheme.primary)
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = option.text,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = if (mine || leader) FontWeight.SemiBold else FontWeight.Medium,
                    color = scheme.onSurface,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
                if (option.addedByMe) {
                    Text("Added by you", style = MaterialTheme.typography.labelSmall, color = scheme.onSurfaceVariant)
                }
            }
            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = "$pct%",
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    color = scheme.onSurface
                )
                Text(
                    text = option.votes.toString(),
                    style = MaterialTheme.typography.labelSmall,
                    color = scheme.onSurfaceVariant
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
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        TextField(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            singleLine = true,
            placeholder = { Text("Your option") },
            shape = RoundedCornerShape(20.dp),
            colors = TextFieldDefaults.colors(
                focusedIndicatorColor = Color.Transparent,
                unfocusedIndicatorColor = Color.Transparent,
                disabledIndicatorColor = Color.Transparent,
                focusedContainerColor = scheme.surfaceContainerHighest,
                unfocusedContainerColor = scheme.surfaceContainerHighest
            ),
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
            keyboardActions = KeyboardActions(onDone = { onSubmit() }),
            modifier = Modifier.weight(1f)
        )
        Box(
            modifier = Modifier
                .size(44.dp)
                .clip(RoundedCornerShape(percent = 50))
                .background(if (value.isBlank()) scheme.surfaceContainerHighest else scheme.primary)
                .clickable(enabled = enabled && value.isNotBlank(), onClick = onSubmit),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                Icons.Rounded.Check, "Add",
                tint = if (value.isBlank()) scheme.onSurfaceVariant else scheme.onPrimary,
                modifier = Modifier.size(20.dp)
            )
        }
        Box(
            modifier = Modifier
                .size(44.dp)
                .clip(RoundedCornerShape(percent = 50))
                .clickable(onClick = onCancel),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Rounded.Close, "Cancel", tint = scheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
        }
    }
}

/**
 * Feed-row preview of a poll: the question and the two leading options as slim bars. The row
 * itself opens the post, where the full card lives.
 */
@Composable
fun NebPollPreview(poll: PollUi, modifier: Modifier = Modifier) {
    val scheme = MaterialTheme.colorScheme
    val shown = poll.options.sortedByDescending { it.votes }.take(2)
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        color = scheme.surfaceContainerLow
    ) {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                PollTag(if (poll.isMcq) "Quiz" else "Poll", strong = true)
                Text(
                    text = votesLabel(poll.totalVotes),
                    style = MaterialTheme.typography.labelMedium,
                    color = scheme.onSurfaceVariant
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
            shown.forEach { option ->
                val frac = if (poll.totalVotes > 0) option.votes.toFloat() / poll.totalVotes else 0f
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 34.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(scheme.surfaceContainerHighest)
                ) {
                    Box(Modifier.matchParentSize()) {
                        Box(
                            Modifier
                                .fillMaxHeight()
                                .fillMaxWidth(frac.coerceIn(0f, 1f))
                                .background(
                                    if (option.id == poll.leaderId) scheme.primaryContainer else scheme.secondaryContainer
                                )
                        )
                    }
                    Row(
                        Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            option.text,
                            style = MaterialTheme.typography.labelLarge,
                            color = scheme.onSurface,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                        Box(Modifier.width(8.dp))
                        Text(
                            "${(frac * 100).toInt()}%",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            color = scheme.onSurface
                        )
                    }
                }
            }
            if (poll.options.size > 2) {
                Text(
                    "+${poll.options.size - 2} more",
                    style = MaterialTheme.typography.labelSmall,
                    color = scheme.onSurfaceVariant
                )
            }
        }
    }
}
