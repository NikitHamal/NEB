package com.neb.ians.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.pixel.PixelSpriteView
import com.neb.ians.ui.pixel.PixelUiSprites
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.distinctUntilChanged

private enum class RefreshPhase { Pulling, Armed, Refreshing, Done }

private const val MIN_SHOWN_MS = 650L
private const val DONE_MS = 520L

/**
 * Pull to refresh, the NEBians way. Drop-in for Material's PullToRefreshBox (same parameters):
 *
 * - The content follows the finger with resistance, so the pull feels physical, and a pixel Neby
 *   rises into the gap it opens.
 * - Past the threshold Neby looks up, the label says "Release to refresh" and the phone gives one
 *   light tick; drop below it again and it re-arms.
 * - While the screen reloads Neby thinks. A refresh is shown for at least [MIN_SHOWN_MS] so a fast
 *   reload never flashes, and it ends with a short "Up to date" before the content settles back.
 *
 * Every per-frame value (the pull distance) is read in the draw phase, so dragging never
 * recomposes the screen underneath.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NebRefreshBox(
    isRefreshing: Boolean,
    onRefresh: () -> Unit,
    modifier: Modifier = Modifier,
    content: @Composable BoxScope.() -> Unit,
) {
    val state = rememberPullToRefreshState()
    val haptics = LocalHapticFeedback.current
    val density = LocalDensity.current
    val headerPx = with(density) { 76.dp.toPx() }

    // what the user sees, smoothed over the caller's isRefreshing
    var shown by remember { mutableStateOf(false) }
    var done by remember { mutableStateOf(false) }
    var startedAt by remember { mutableLongStateOf(0L) }
    LaunchedEffect(isRefreshing) {
        if (isRefreshing) {
            done = false
            shown = true
            startedAt = System.currentTimeMillis()
        } else if (shown) {
            val left = MIN_SHOWN_MS - (System.currentTimeMillis() - startedAt)
            if (left > 0) delay(left)
            done = true
            delay(DONE_MS)
            shown = false
            done = false
        }
    }

    // one light tick each time the pull crosses the threshold
    LaunchedEffect(state) {
        snapshotFlow { state.distanceFraction >= 1f }
            .distinctUntilChanged()
            .collect { armed -> if (armed && !shown) haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove) }
    }

    val phase by remember {
        derivedStateOf {
            when {
                done -> RefreshPhase.Done
                shown -> RefreshPhase.Refreshing
                state.distanceFraction >= 1f -> RefreshPhase.Armed
                else -> RefreshPhase.Pulling
            }
        }
    }

    PullToRefreshBox(
        isRefreshing = shown,
        onRefresh = onRefresh,
        modifier = modifier,
        state = state,
        indicator = {
            Box(
                Modifier
                    .align(Alignment.TopCenter)
                    .fillMaxWidth()
                    .height(76.dp)
                    .graphicsLayer {
                        val f = state.distanceFraction
                        alpha = (f * 1.6f).coerceIn(0f, 1f)
                        translationY = headerPx * (resist(f) - 1f) * 0.5f
                    },
                contentAlignment = Alignment.Center
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    val sprite = when (phase) {
                        RefreshPhase.Pulling -> PixelUiSprites.nebyIdle
                        RefreshPhase.Armed -> PixelUiSprites.nebyHop
                        RefreshPhase.Refreshing -> PixelUiSprites.nebyThink
                        RefreshPhase.Done -> PixelUiSprites.nebyIdle
                    }
                    PixelSpriteView(sprite = sprite, modifier = Modifier.size(40.dp))
                    Text(
                        when (phase) {
                            RefreshPhase.Pulling -> "Pull to refresh"
                            RefreshPhase.Armed -> "Release to refresh"
                            RefreshPhase.Refreshing -> "Refreshing"
                            RefreshPhase.Done -> "Up to date"
                        },
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    ) {
        Box(
            Modifier
                .fillMaxSize()
                .graphicsLayer { translationY = headerPx * resist(state.distanceFraction) }
        ) { content() }
    }
}

/** Resistance: 1:1 up to the threshold, then each extra pixel moves the content less. */
private fun resist(f: Float): Float = when {
    f <= 0f -> 0f
    f <= 1f -> f
    else -> 1f + (1f - 1f / (1f + (f - 1f) * 1.4f)) * 0.45f
}
