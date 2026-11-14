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
import androidx.compose.material.icons.filled.Cancel
import androidx.compose.material.icons.filled.ChatBubble
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.FormatListNumbered
import androidx.compose.material.icons.filled.Functions
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.Report
import androidx.compose.material.icons.filled.Rule
import androidx.compose.material.icons.filled.TaskAlt
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.filled.VolunteerActivism
import androidx.compose.material.icons.filled.ArrowDownward
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.layout.height
import com.neb.ians.ui.theme.nebAnimationsReduced
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.clickable
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
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
    ReplyKindSpec("comment", "Comment", Icons.Filled.ChatBubble),
    ReplyKindSpec("answer", "Answer", Icons.Filled.TaskAlt),
    ReplyKindSpec("solution", "Solution", Icons.Filled.FormatListNumbered),
    ReplyKindSpec("hint", "Hint", Icons.Filled.Lightbulb),
    ReplyKindSpec("formula", "Formula", Icons.Filled.Functions)
)

val REPLY_LABELS = listOf(
    ReplyLabelSpec("accepted", "Accepted answer", Icons.Filled.CheckCircle, "good", "This solved it"),
    ReplyLabelSpec("correct", "Correct", Icons.Filled.Verified, "good", "The working and result are right"),
    ReplyLabelSpec("partial", "Partly correct", Icons.Filled.Rule, "warn", "Right idea, something is missing"),
    ReplyLabelSpec("incorrect", "Incorrect", Icons.Filled.Cancel, "bad", "There is a mistake in it"),
    ReplyLabelSpec("helpful", "Helpful", Icons.Filled.VolunteerActivism, "info", "Useful, even if not the answer"),
    ReplyLabelSpec("spam", "Spam", Icons.Filled.Report, "bad", "Off topic, ads or noise")
)

fun replyKind(key: String): ReplyKindSpec = REPLY_KINDS.firstOrNull { it.key == key } ?: REPLY_KINDS.first()

fun replyLabel(key: String): ReplyLabelSpec? = REPLY_LABELS.firstOrNull { it.key == key }

private val ChipShape = RoundedCornerShape(12.dp)

/** Web tokens `--fl-good/warn/bad/info` and their `on` colours (`app-forum.css`), light and dark. */
object ReplyTones {
    val goodLight = Color(0xFFD3F1DE); val onGoodLight = Color(0xFF0A3A1C); val goodLineLight = Color(0xFF7CCF9B)
    val goodDark = Color(0xFF14402A); val onGoodDark = Color(0xFFC3F2D5); val goodLineDark = Color(0xFF3F9B69)
    fun good(dark: Boolean) = if (dark) goodDark else goodLight
    fun onGood(dark: Boolean) = if (dark) onGoodDark else onGoodLight
    fun goodLine(dark: Boolean) = if (dark) goodLineDark else goodLineLight
}

/** Container and content colours for a label tone, the same values the web chips use. */
@Composable
private fun labelColors(tone: String): Pair<Color, Color> {
    val cs = MaterialTheme.colorScheme
    val dark = cs.surface.luminance() < 0.5f
    return when (tone) {
        "good" -> ReplyTones.good(dark) to ReplyTones.onGood(dark)
        "warn" -> (if (dark) Color(0xFF4A3708) else Color(0xFFFDE8BD)) to (if (dark) Color(0xFFFFE2A6) else Color(0xFF432B00))
        "bad" -> (if (dark) Color(0xFF6B1B1B) else Color(0xFFFFDAD6)) to (if (dark) Color(0xFFFFDAD6) else Color(0xFF5C0008))
        else -> cs.primaryContainer to cs.onPrimaryContainer
    }
}

/** The web's `.fl-chip`: 24dp, 12dp corners, 16dp filled glyph, 12sp bold, pops in on a spring. */
@Composable
private fun TonalTag(icon: ImageVector, text: String, container: Color, content: Color, modifier: Modifier = Modifier) {
    val reduced = nebAnimationsReduced()
    val pop = remember { Animatable(if (reduced) 1f else 0.8f) }
    LaunchedEffect(Unit) {
        if (!reduced) pop.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow))
    }
    Row(
        modifier = modifier
            .graphicsLayer {
                scaleX = pop.value
                scaleY = pop.value
                alpha = ((pop.value - 0.8f) / 0.2f).coerceIn(0f, 1f)
            }
            .height(24.dp)
            .clip(ChipShape)
            .background(container)
            .padding(start = 7.dp, end = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = content, modifier = Modifier.size(16.dp))
        Spacer(Modifier.width(4.dp))
        Text(text, fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.12.sp, color = content, maxLines = 1)
    }
}

/**
 * The web's `.fl-solved-chip`: a good-tone pill with a filled check and a small arrow that
 * points at the accepted answer; tapping it scrolls there. Springs on press, arrow nudges on entry.
 */
@Composable
fun SolvedChip(onClick: () -> Unit, modifier: Modifier = Modifier) {
    val reduced = nebAnimationsReduced()
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val container = ReplyTones.good(dark)
    val content = ReplyTones.onGood(dark)
    val pop = remember { Animatable(if (reduced) 1f else 0.8f) }
    val nudge = remember { Animatable(0f) }
    val press = remember { androidx.compose.foundation.interaction.MutableInteractionSource() }
    val pressed by press.collectIsPressedAsState()
    val pressScale by androidx.compose.animation.core.animateFloatAsState(
        if (pressed) 0.95f else 1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium), label = "solvedPress"
    )
    LaunchedEffect(Unit) {
        if (!reduced) {
            pop.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow))
            repeat(2) {
                nudge.animateTo(1f, androidx.compose.animation.core.tween(220))
                nudge.animateTo(0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium))
            }
        }
    }
    Row(
        modifier = modifier
            .graphicsLayer {
                val k = pop.value * pressScale
                scaleX = k
                scaleY = k
                alpha = ((pop.value - 0.8f) / 0.2f).coerceIn(0f, 1f)
            }
            .height(26.dp)
            .clip(RoundedCornerShape(13.dp))
            .background(container)
            .clickable(interactionSource = press, indication = null, onClick = onClick)
            .semantics { contentDescription = "Go to the accepted answer" }
            .padding(start = 8.dp, end = 11.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(Icons.Filled.CheckCircle, contentDescription = null, tint = content, modifier = Modifier.size(17.dp))
        Spacer(Modifier.width(4.dp))
        Text("Solved", fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.12.sp, color = content)
        Icon(
            Icons.Filled.ArrowDownward,
            contentDescription = null,
            tint = content.copy(alpha = 0.8f),
            modifier = Modifier
                .padding(start = 0.dp)
                .size(15.dp)
                .graphicsLayer { translationY = nudge.value * 2.dp.toPx() }
        )
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
