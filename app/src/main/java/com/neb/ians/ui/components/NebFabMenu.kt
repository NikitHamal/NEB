@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.MutableTransitionState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.ripple
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import kotlinx.coroutines.delay
import com.neb.ians.ui.theme.resolve
import com.neb.ians.ui.theme.NebAccents
import com.neb.ians.ui.theme.NebAccent
import androidx.compose.foundation.border

@Immutable
data class NebFabAction(
    val label: String,
    val icon: ImageVector,
    val onClick: () -> Unit,
    val accent: NebAccent? = null,
    val destructive: Boolean = false,
    val testTag: String? = null
)

private const val StaggerStepMillis = 40L

@Composable
fun NebFabMenu(
    actions: List<NebFabAction>,
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
    spacing: Dp = 14.dp,
    anchor: @Composable () -> Unit
) {
    val gap by animateDpAsState(
        targetValue = if (expanded) spacing else 0.dp,
        animationSpec = nebFastSpatialSpec(),
        label = "fab_menu_gap"
    )

    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.End
    ) {
        NebFabMenuItems(
            actions = actions,
            expanded = expanded,
            onDismissRequest = onDismissRequest
        )
        Spacer(modifier = Modifier.height(gap))
        anchor()
    }
}

@Composable
fun NebFabMenuItems(
    actions: List<NebFabAction>,
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
    itemSpacing: Dp = 10.dp
) {
    if (actions.isEmpty()) return

    val reduced = nebAnimationsReduced()
    val states = remember(actions.size) {
        List(actions.size) { MutableTransitionState(false) }
    }

    LaunchedEffect(expanded, reduced) {
        val order = if (expanded) actions.indices.reversed() else actions.indices
        order.forEach { index ->
            states[index].targetState = expanded
            if (!reduced) delay(StaggerStepMillis)
        }
    }

    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.End,
        verticalArrangement = Arrangement.spacedBy(itemSpacing)
    ) {
        actions.forEachIndexed { index, action ->
            NebFabMenuItem(
                action = action,
                visibleState = states[index],
                onDismissRequest = onDismissRequest
            )
        }
    }
}

@Composable
private fun NebFabMenuItem(
    action: NebFabAction,
    visibleState: MutableTransitionState<Boolean>,
    onDismissRequest: () -> Unit
) {
    val spatial = nebFastSpatialSpec<Float>()
    val slide = nebFastSpatialSpec<androidx.compose.ui.unit.IntOffset>()
    val effects = nebFastEffectsSpec<Float>()

    AnimatedVisibility(
        visibleState = visibleState,
        enter = fadeIn(animationSpec = effects) +
            scaleIn(
                animationSpec = spatial,
                initialScale = 0.72f,
                transformOrigin = TransformOrigin(1f, 1f)
            ) +
            slideInVertically(animationSpec = slide) { it / 2 },
        exit = fadeOut(animationSpec = effects) +
            scaleOut(
                animationSpec = spatial,
                targetScale = 0.72f,
                transformOrigin = TransformOrigin(1f, 1f)
            ) +
            slideOutVertically(animationSpec = slide) { it / 2 }
    ) {
        NebFabMenuPill(action = action, onDismissRequest = onDismissRequest)
    }
}

@Composable
private fun NebFabMenuPill(
    action: NebFabAction,
    onDismissRequest: () -> Unit
) {
    val tactile = rememberTactileFeedback()
    val interaction = remember { MutableInteractionSource() }

    val accent = when {
        action.destructive -> NebAccents.Rose.resolve()
        action.accent != null -> action.accent.resolve()
        else -> null
    }

    // Every pill in the menu wears the same container. Three differently tinted
    // backgrounds stacked above the create button read as three unrelated
    // controls, and the tints fought the scrim behind them. The hue now lives in
    // exactly one place per row — the glyph — which is enough to tell them apart
    // and leaves the menu looking like one object.
    val container = MaterialTheme.colorScheme.surfaceContainerLowest
    val outline = MaterialTheme.colorScheme.outlineVariant

    /** The label is always ink: three colours of text would be unreadable. */
    val labelColor = MaterialTheme.colorScheme.onSurface

    /** The glyph is the one thing allowed to carry the action's own colour. */
    val iconColor = accent ?: MaterialTheme.colorScheme.onSurface

    Row(
        modifier = Modifier
            .then(action.testTag?.let { Modifier.testTag(it) } ?: Modifier)
            .heightIn(min = 56.dp)
            .widthIn(max = 280.dp)
            .clip(RoundedCornerShape(50))
            .background(container)
            .border(1.dp, outline, RoundedCornerShape(50))
            .clickable(
                interactionSource = interaction,
                indication = ripple(bounded = true, color = iconColor),
                onClick = {
                    tactile.perform(TactileType.ButtonTap)
                    onDismissRequest()
                    action.onClick()
                }
            )
            .padding(horizontal = 22.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Icon(
            imageVector = action.icon,
            contentDescription = null,
            tint = iconColor,
            modifier = Modifier.size(22.dp)
        )
        Text(
            text = action.label,
            style = MaterialTheme.typography.labelLargeEmphasized,
            color = labelColor,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun NebFabMenuScrim(
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isDark = MaterialTheme.colorScheme.surface.luminanceIsDark()
    val interaction = remember { MutableInteractionSource() }

    AnimatedVisibility(
        visible = expanded,
        modifier = modifier,
        enter = fadeIn(animationSpec = nebEffectsSpec()),
        exit = fadeOut(animationSpec = nebEffectsSpec())
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    if (isDark) Color.Black.copy(alpha = 0.62f) else Color.Black.copy(alpha = 0.34f)
                )
                .clickable(
                    interactionSource = interaction,
                    indication = null,
                    onClick = onDismissRequest
                )
                .semantics { }
        )
    }
}

private fun Color.luminanceIsDark(): Boolean {
    val l = 0.299f * red + 0.587f * green + 0.114f * blue
    return l < 0.5f
}
