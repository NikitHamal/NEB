package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Cancel
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/** Right and wrong tones for quizzes: the web's `--fl-good` and `--fl-bad` pairs, so a quiz reads like a marked reply. */
internal data class PollTones(val good: Color, val onGood: Color, val bad: Color, val onBad: Color)

@Composable
internal fun rememberPollTones(): PollTones {
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    return PollTones(
        good = ReplyTones.good(dark),
        onGood = ReplyTones.onGood(dark),
        bad = if (dark) Color(0xFF6B1B1B) else Color(0xFFFFDAD6),
        onBad = if (dark) Color(0xFFFFDAD6) else Color(0xFF5C0008)
    )
}

/** A 24dp tonal chip: the poll's kind, its status, its options. Chips keep their fill. */
@Composable
internal fun PollChip(label: String, icon: ImageVector? = null, strong: Boolean = false) {
    val scheme = MaterialTheme.colorScheme
    val container = if (strong) scheme.primaryContainer else scheme.secondaryContainer
    val content = if (strong) scheme.onPrimaryContainer else scheme.onSecondaryContainer
    Row(
        modifier = Modifier
            .height(24.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(container)
            .padding(start = if (icon != null) 7.dp else 10.dp, end = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (icon != null) {
            Icon(icon, null, Modifier.size(15.dp), tint = content)
            Spacer(Modifier.width(4.dp))
        }
        Text(label, fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight.Bold, color = content, maxLines = 1)
    }
}

/**
 * An option before the viewer has voted: a white field with one stroke that turns primary when
 * picked, a radio or checkbox mark that springs in, and a press that squeezes the row.
 */
@Composable
internal fun PollChoiceRow(
    option: PollOptionUi,
    multiple: Boolean,
    selected: Boolean,
    enabled: Boolean,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val stroke by animateColorAsState(if (selected) scheme.primary else scheme.outlineVariant, label = "pollStroke")
    val tint by animateColorAsState(if (selected) scheme.primary.copy(alpha = 0.08f) else scheme.surfaceContainerLowest, label = "pollTint")
    val pop = remember { Animatable(if (selected) 1f else 0f) }
    LaunchedEffect(selected) {
        pop.animateTo(if (selected) 1f else 0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium))
    }
    val markShape = if (multiple) RoundedCornerShape(7.dp) else RoundedCornerShape(11.dp)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 52.dp)
            .clip(RoundedCornerShape(18.dp))
            .background(tint)
            .border(BorderStroke(1.5.dp, stroke), RoundedCornerShape(18.dp))
            .nebPressable(enabled = enabled, scale = 0.98f, onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .size(22.dp)
                .clip(markShape)
                .border(BorderStroke(2.dp, if (selected) scheme.primary else scheme.outline), markShape)
                .drawBehind { drawRect(scheme.primary.copy(alpha = pop.value.coerceIn(0f, 1f))) },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                Icons.Rounded.Check, null,
                modifier = Modifier.size(15.dp).graphicsLayer { scaleX = pop.value; scaleY = pop.value },
                tint = scheme.onPrimary
            )
        }
        Column(Modifier.weight(1f)) {
            Text(
                option.text,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
                color = scheme.onSurface
            )
            val by = when {
                option.addedByMe -> "Added by you"
                option.isAdded -> "Added by a member"
                else -> ""
            }
            if (by.isNotEmpty()) Text(by, style = MaterialTheme.typography.labelSmall, color = scheme.onSurfaceVariant)
        }
    }
}

/**
 * An option once results show: a track with a bar that springs out to its share (drawn, never laid out
 * per frame), your pick ticked, the leader in the stronger container, quiz answers in right and wrong tones.
 */
@Composable
internal fun PollResultRow(poll: PollUi, option: PollOptionUi, index: Int) {
    val scheme = MaterialTheme.colorScheme
    val tones = rememberPollTones()
    val fraction = if (poll.totalVotes > 0) option.votes.toFloat() / poll.totalVotes else 0f
    val grow = remember { Animatable(0f) }
    LaunchedEffect(fraction) {
        kotlinx.coroutines.delay(index * 45L)
        grow.animateTo(fraction.coerceIn(0f, 1f), spring(Spring.DampingRatioLowBouncy, Spring.StiffnessLow))
    }
    val mine = option.id in poll.votedIds
    val leader = option.id == poll.leaderId
    val quiz = poll.isMcq && poll.hasVoted
    val wrongPick = quiz && mine && !option.correct
    val rightOne = quiz && option.correct
    val fill = when {
        wrongPick -> tones.bad
        rightOne -> tones.good
        leader -> scheme.primaryContainer
        else -> scheme.secondaryContainer
    }
    val ink = when {
        wrongPick -> tones.onBad
        rightOne -> tones.onGood
        leader -> scheme.onPrimaryContainer
        else -> scheme.onSecondaryContainer
    }
    val pct = if (poll.totalVotes > 0) option.votes * 100 / poll.totalVotes else 0
    val shape = RoundedCornerShape(18.dp)
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 52.dp)
            .clip(shape)
            .background(scheme.surfaceContainerLow)
            .drawBehind { drawRect(fill, size = Size(size.width * grow.value, size.height)) }
            .border(BorderStroke(1.dp, if (mine) scheme.primary else scheme.outlineVariant), shape)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            if (wrongPick || rightOne || mine) {
                Icon(
                    imageVector = if (wrongPick) Icons.Rounded.Cancel else Icons.Rounded.CheckCircle,
                    contentDescription = if (mine) "Your vote" else "Correct answer",
                    tint = if (quiz) ink else scheme.primary,
                    modifier = Modifier.size(20.dp)
                )
            }
            Column(Modifier.weight(1f)) {
                Text(
                    option.text,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = if (leader || mine) FontWeight.SemiBold else FontWeight.Medium,
                    color = scheme.onSurface
                )
                if (option.addedByMe || option.isAdded) {
                    Text(
                        if (option.addedByMe) "Added by you" else "Added by a member",
                        style = MaterialTheme.typography.labelSmall,
                        color = scheme.onSurfaceVariant
                    )
                }
            }
            Column(horizontalAlignment = Alignment.End) {
                Text("$pct%", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = scheme.onSurface)
                Text(
                    if (option.votes == 1) "1 vote" else "${option.votes} votes",
                    style = MaterialTheme.typography.labelSmall,
                    color = scheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Clip
                )
            }
        }
    }
}
