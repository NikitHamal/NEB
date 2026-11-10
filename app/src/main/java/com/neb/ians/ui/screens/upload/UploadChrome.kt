@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.upload

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialShapes
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebMorphBlob
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

private val StepLabels = listOf("File", "Details", "Publish")

/**
 * Where you are, as three pills.
 *
 * The pill you are on is the one that opens up: it is ink, it grows to carry its
 * own name, and the other two shrink to a number. A step you have finished turns
 * into a tick and takes you back when you tap it. There is no caption under the
 * title, the title is the whole instruction.
 */
@Composable
internal fun UploadStepper(
    stepIndex: Int,
    title: String,
    onJump: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            StepLabels.forEachIndexed { index, label ->
                val active = index == stepIndex
                val done = index < stepIndex
                val weight by animateFloatAsState(
                    targetValue = if (active) 2.4f else 1f,
                    animationSpec = nebSpatialSpec(),
                    label = "upload_step_weight_$index"
                )
                val container by animateColorAsState(
                    targetValue = when {
                        active -> MaterialTheme.colorScheme.onSurface
                        done -> MaterialTheme.colorScheme.secondaryContainer
                        else -> MaterialTheme.colorScheme.surfaceContainerHigh
                    },
                    animationSpec = nebEffectsSpec(),
                    label = "upload_step_container_$index"
                )
                val ink by animateColorAsState(
                    targetValue = when {
                        active -> MaterialTheme.colorScheme.surface
                        done -> MaterialTheme.colorScheme.onSecondaryContainer
                        else -> MaterialTheme.colorScheme.onSurfaceVariant
                    },
                    animationSpec = nebEffectsSpec(),
                    label = "upload_step_ink_$index"
                )
                Row(
                    modifier = Modifier
                        .weight(weight)
                        .height(44.dp)
                        .then(if (done) Modifier.nebPressable(onClick = { onJump(index) }) else Modifier)
                        .clip(RoundedCornerShape(50))
                        .background(container)
                        .padding(horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterHorizontally)
                ) {
                    if (done) {
                        Icon(
                            imageVector = Icons.Rounded.Check,
                            contentDescription = label,
                            tint = ink,
                            modifier = Modifier.size(18.dp)
                        )
                    } else {
                        Text(
                            text = "${index + 1}",
                            style = MaterialTheme.typography.labelLarge,
                            color = ink,
                            maxLines = 1
                        )
                    }
                    if (active) {
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelLarge,
                            color = ink,
                            maxLines = 1,
                            softWrap = false,
                            overflow = TextOverflow.Clip
                        )
                    }
                }
            }
        }
        val titleFade = nebEffectsSpec<Float>()
        AnimatedContent(
            targetState = title,
            transitionSpec = { fadeIn(titleFade) togetherWith fadeOut(titleFade) },
            label = "upload_title"
        ) { text ->
            Text(
                text = text,
                style = MaterialTheme.typography.headlineSmallEmphasized,
                color = MaterialTheme.colorScheme.onSurface
            )
        }
    }
}

/**
 * Covers the screen while the upload runs.
 *
 * A shape keeps changing into other shapes behind the percentage, so a long
 * upload looks alive instead of stuck, and the number is the only thing that has
 * to be read. The screen underneath cannot be touched until it is over.
 */
@Composable
internal fun UploadPublishingOverlay(
    visible: Boolean,
    progress: Float,
    label: String,
    modifier: Modifier = Modifier
) {
    AnimatedVisibility(
        visible = visible,
        enter = fadeIn(nebEffectsSpec()),
        exit = fadeOut(nebEffectsSpec()),
        modifier = modifier
    ) {
        val dark = isSystemInDarkTheme()
        val transition = rememberInfiniteTransition(label = "upload_publish")
        val position by transition.animateFloat(
            initialValue = 0f,
            targetValue = BlobShapes.size - 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 4200, easing = FastOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ),
            label = "upload_publish_morph"
        )
        val rotation by transition.animateFloat(
            initialValue = 0f,
            targetValue = 360f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 12000, easing = LinearEasing)
            ),
            label = "upload_publish_turn"
        )
        val smooth by animateFloatAsState(
            targetValue = progress.coerceIn(0f, 1f),
            animationSpec = nebEffectsSpec(),
            label = "upload_publish_progress"
        )

        Surface(
            color = MaterialTheme.colorScheme.surface,
            modifier = Modifier
                .fillMaxSize()
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = {}
                )
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 40.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Box(modifier = Modifier.size(240.dp), contentAlignment = Alignment.Center) {
                    NebMorphBlob(
                        shapes = BlobShapes,
                        color = NebTone.Azure.container(dark),
                        modifier = Modifier.fillMaxSize(),
                        rotation = { rotation },
                        position = { position }
                    )
                    Text(
                        text = "${(smooth * 100).toInt()}%",
                        style = MaterialTheme.typography.displaySmall.copy(fontWeight = FontWeight.SemiBold),
                        color = NebTone.Azure.deep(dark)
                    )
                }
                Box(
                    modifier = Modifier
                        .padding(top = 28.dp)
                        .fillMaxWidth()
                        .height(10.dp)
                        .clip(RoundedCornerShape(50))
                        .background(MaterialTheme.colorScheme.surfaceContainerHighest)
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxHeight()
                            .fillMaxWidth(smooth.coerceAtLeast(0.04f))
                            .clip(RoundedCornerShape(50))
                            .background(MaterialTheme.colorScheme.primary)
                    )
                }
                Text(
                    text = label,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurface,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(top = 16.dp)
                )
            }
        }
    }
}

private val BlobShapes by lazy {
    listOf(
        MaterialShapes.Cookie9Sided,
        MaterialShapes.Clover4Leaf,
        MaterialShapes.SoftBurst,
        MaterialShapes.Flower
    )
}
