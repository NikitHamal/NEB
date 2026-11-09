package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Cancel
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.FormatListNumbered
import androidx.compose.material.icons.outlined.Functions
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.Report
import androidx.compose.material.icons.outlined.Rule
import androidx.compose.material.icons.outlined.TaskAlt
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material.icons.outlined.VolunteerActivism
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.nebEffectsSpec

/**
 * What a reply says it is, and how the discussion's author rated it. The keys are the ones
 * the server stores (`web/forum_labels.py`), so the app, the site and the API agree.
 */
data class ReplyKindSpec(val key: String, val label: String, val icon: ImageVector)

data class ReplyLabelSpec(val key: String, val label: String, val icon: ImageVector, val tone: String, val hint: String)

val REPLY_KINDS = listOf(
    ReplyKindSpec("comment", "Comment", Icons.Outlined.ChatBubbleOutline),
    ReplyKindSpec("answer", "Answer", Icons.Outlined.TaskAlt),
    ReplyKindSpec("solution", "Solution", Icons.Outlined.FormatListNumbered),
    ReplyKindSpec("hint", "Hint", Icons.Outlined.Lightbulb),
    ReplyKindSpec("formula", "Formula", Icons.Outlined.Functions)
)

val REPLY_LABELS = listOf(
    ReplyLabelSpec("accepted", "Accepted answer", Icons.Outlined.CheckCircle, "good", "This solved it"),
    ReplyLabelSpec("correct", "Correct", Icons.Outlined.Verified, "good", "The working and result are right"),
    ReplyLabelSpec("partial", "Partly correct", Icons.Outlined.Rule, "warn", "Right idea, something is missing"),
    ReplyLabelSpec("incorrect", "Incorrect", Icons.Outlined.Cancel, "bad", "There is a mistake in it"),
    ReplyLabelSpec("helpful", "Helpful", Icons.Outlined.VolunteerActivism, "info", "Useful, even if not the answer"),
    ReplyLabelSpec("spam", "Spam", Icons.Outlined.Report, "bad", "Off topic, ads or noise")
)

fun replyKind(key: String): ReplyKindSpec = REPLY_KINDS.firstOrNull { it.key == key } ?: REPLY_KINDS.first()

fun replyLabel(key: String): ReplyLabelSpec? = REPLY_LABELS.firstOrNull { it.key == key }

private val ChipShape = RoundedCornerShape(28.dp)

/** Container and content colours for a label tone, from the same tonal family as the web chips. */
@Composable
private fun labelColors(tone: String): Pair<Color, Color> {
    val cs = MaterialTheme.colorScheme
    val dark = cs.surface.luminance() < 0.5f
    return when (tone) {
        "good" -> NebTone.Aqua.container(dark) to NebTone.Aqua.deep(dark)
        "info" -> NebTone.Sky.container(dark) to NebTone.Sky.deep(dark)
        "bad" -> cs.errorContainer to cs.onErrorContainer
        else -> cs.secondaryContainer to cs.onSecondaryContainer
    }
}

@Composable
private fun TonalTag(icon: ImageVector, text: String, container: Color, content: Color, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .clip(ChipShape)
            .background(container)
            .padding(horizontal = 10.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = content, modifier = Modifier.size(14.dp))
        Spacer(Modifier.width(5.dp))
        Text(text, style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.SemiBold, color = content)
    }
}

/** What the reply is, shown on its card. A plain comment shows nothing. */
@Composable
fun ReplyKindTag(kind: String, modifier: Modifier = Modifier) {
    if (kind.isBlank() || kind == "comment") return
    val spec = replyKind(kind)
    val cs = MaterialTheme.colorScheme
    TonalTag(spec.icon, spec.label, cs.secondaryContainer, cs.onSecondaryContainer, modifier)
}

/** How the discussion's author rated it. Empty when it has not been rated. */
@Composable
fun ReplyLabelTag(label: String, modifier: Modifier = Modifier) {
    val spec = replyLabel(label) ?: return
    val (container, content) = labelColors(spec.tone)
    TonalTag(spec.icon, spec.label, container, content, modifier)
}

/**
 * The reply type sheet, opened from the composer's type tool: one row per kind, the chosen one on
 * the primary container with a tick, the web's `fc-kindsheet`. It replaces the old chip row above
 * the field, which the web does not have.
 */
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun ReplyKindSheet(selected: String, onSelect: (String) -> Unit, onDismiss: () -> Unit) {
    val cs = MaterialTheme.colorScheme
    NebModalSheet(onDismiss = onDismiss, horizontalPadding = 12.dp) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 12.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            REPLY_KINDS.forEach { spec ->
                val chosen = spec.key == selected
                Row(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(if (chosen) cs.primaryContainer else Color.Transparent)
                        .nebPressable(onClick = { onSelect(spec.key); onDismiss() })
                        .padding(horizontal = 16.dp, vertical = 14.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        spec.icon,
                        contentDescription = null,
                        tint = if (chosen) cs.onPrimaryContainer else cs.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
                    )
                    Spacer(Modifier.width(16.dp))
                    Text(
                        spec.label,
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = if (chosen) cs.onPrimaryContainer else cs.onSurface,
                        modifier = Modifier.weight(1f)
                    )
                    if (chosen) NebIcon(NebIcons.Check, "Selected", size = 20.dp, tint = cs.onPrimaryContainer)
                }
            }
        }
    }
}

/** The discussion author's sheet for rating a reply. Picking the current label again clears it. */
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun ReplyLabelSheet(current: String, onPick: (String) -> Unit, onDismiss: () -> Unit) {
    NebModalSheet(onDismiss = onDismiss, title = "Mark this reply") {
        Column(Modifier.fillMaxWidth().padding(bottom = 16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            REPLY_LABELS.forEach { spec ->
                val chosen = current == spec.key
                val (container, content) = labelColors(spec.tone)
                Row(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(20.dp))
                        .background(if (chosen) container else Color.Transparent)
                        .nebPressable(onClick = { onPick(if (chosen) "" else spec.key); onDismiss() })
                        .padding(horizontal = 14.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(spec.icon, contentDescription = null, tint = if (chosen) content else MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.width(14.dp))
                    Column(Modifier.weight(1f)) {
                        Text(spec.label, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
                        Text(spec.hint, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (chosen) Icon(Icons.Outlined.Check, contentDescription = "Selected", tint = content)
                }
            }
        }
    }
}
