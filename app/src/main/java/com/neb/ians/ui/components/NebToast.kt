package com.neb.ians.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Info
import androidx.compose.material.icons.rounded.Warning
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SnackbarData
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.theme.Poppins
import kotlinx.coroutines.launch
import kotlin.math.abs
import kotlin.math.roundToInt

private enum class NebToastKind { Success, Problem, Info }

private val ProblemWords = Regex("fail|error|couldn't|could not|can't|cannot|unable|invalid|wrong|denied|not allowed|problem|try again|expired|no internet|offline|missing|required")
private val SuccessWords = Regex("^(saved|sent|posted|copied|added|removed|deleted|updated|done|welcome|thanks|thank you|reported|published|shared|bookmarked|unlocked|joined|followed|verified|submitted|created|marked)|success|\\bsaved\\b|\\bcopied\\b|\\bsent\\b|\\bposted\\b")

private fun kindOf(message: String): NebToastKind {
    val s = message.lowercase()
    return when {
        ProblemWords.containsMatchIn(s) -> NebToastKind.Problem
        SuccessWords.containsMatchIn(s) -> NebToastKind.Success
        else -> NebToastKind.Info
    }
}

/**
 * The app's toast host: the same state and calls as a snackbar host, drawn as [NebToast]. It floats above the
 * content with a margin all round; the scaffold it sits in already keeps it clear of the system bars.
 */
@Composable
fun NebToastHost(hostState: SnackbarHostState, modifier: Modifier = Modifier) {
    SnackbarHost(
        hostState = hostState,
        modifier = modifier.padding(horizontal = 14.dp, vertical = 10.dp),
        snackbar = { data -> NebToast(data) }
    )
}

/**
 * A toast in the app's own language: a dark (in dark mode light) rounded card, a tonal tile that says what kind of
 * message it is, the message, an optional action as a pill. It springs
 * in from below, and a swipe sideways throws it away.
 */
@Composable
fun NebToast(data: SnackbarData) {
    val visuals = data.visuals
    val scheme = MaterialTheme.colorScheme
    val kind = remember(visuals.message) { kindOf(visuals.message) }
    val tileColor: Color
    val tileInk: Color
    val icon = when (kind) {
        NebToastKind.Success -> Icons.Rounded.Check
        NebToastKind.Problem -> Icons.Rounded.Warning
        NebToastKind.Info -> Icons.Rounded.Info
    }
    when (kind) {
        NebToastKind.Success -> { tileColor = scheme.tertiaryContainer; tileInk = scheme.onTertiaryContainer }
        NebToastKind.Problem -> { tileColor = scheme.errorContainer; tileInk = scheme.onErrorContainer }
        NebToastKind.Info -> { tileColor = scheme.primaryContainer; tileInk = scheme.onPrimaryContainer }
    }
    val appear = remember { Animatable(0f) }
    val drag = remember { Animatable(0f) }
    val scope = rememberCoroutineScope()
    LaunchedEffect(Unit) { appear.animateTo(1f, spring(dampingRatio = 0.7f, stiffness = 480f)) }

    val shape = RoundedCornerShape(24.dp)
    Row(
        Modifier
            .fillMaxWidth()
            .widthIn(max = 560.dp)
            .graphicsLayer {
                val a = appear.value
                translationY = (1f - a) * 36.dp.toPx()
                alpha = (a * 1.4f).coerceIn(0f, 1f) * (1f - (abs(drag.value) / (size.width * 0.9f)).coerceIn(0f, 1f))
                val s = 0.94f + 0.06f * a.coerceAtMost(1.04f)
                scaleX = s
                scaleY = s
            }
            .offset { IntOffset(drag.value.roundToInt(), 0) }
            .pointerInput(data) {
                detectHorizontalDragGestures(
                    onDragEnd = {
                        scope.launch {
                            if (abs(drag.value) > size.width * 0.28f) {
                                drag.animateTo(if (drag.value > 0) size.width.toFloat() else -size.width.toFloat(), tween(140))
                                data.dismiss()
                            } else drag.animateTo(0f, spring(dampingRatio = 0.8f, stiffness = 600f))
                        }
                    },
                    onDragCancel = { scope.launch { drag.animateTo(0f) } }
                ) { change, amount ->
                    change.consume()
                    scope.launch { drag.snapTo(drag.value + amount) }
                }
            }
            .semantics { liveRegion = LiveRegionMode.Polite }
            .clip(shape)
            .background(scheme.inverseSurface)
            .heightIn(min = 56.dp)
            .padding(horizontal = 10.dp, vertical = 9.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(Modifier.size(38.dp).clip(RoundedCornerShape(13.dp)).background(tileColor), contentAlignment = Alignment.Center) {
            Icon(icon, null, tint = tileInk, modifier = Modifier.size(20.dp))
        }
        Text(
            visuals.message,
            style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Medium, fontSize = 14.sp, lineHeight = 20.sp, color = scheme.inverseOnSurface),
            maxLines = 3,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        val action = visuals.actionLabel
        if (action != null) {
            Box(
                Modifier
                    .clip(CircleShape)
                    .background(scheme.inversePrimary.copy(alpha = 0.18f))
                    .clickable(onClickLabel = action) { data.performAction() }
                    .padding(horizontal = 14.dp, vertical = 9.dp)
            ) {
                Text(action, style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = 13.sp, color = scheme.inversePrimary))
            }
        } else if (visuals.withDismissAction) {
            Box(
                Modifier.size(36.dp).clip(CircleShape).clickable(onClickLabel = "Dismiss") { data.dismiss() },
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Rounded.Close, "Dismiss", tint = scheme.inverseOnSurface, modifier = Modifier.size(18.dp))
            }
        }
    }
}
