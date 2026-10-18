package com.neb.ians.ui.pixel

import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebAnimationsReduced
import kotlinx.coroutines.delay
import kotlin.random.Random

/**
 * Pixel Neby, the mascot, wherever Neby appears in the app. (The 3D avatar in ui/avatar/neby is
 * kept for later but no longer shown.)
 *
 * - [state] is what Neby is doing: idle, thinking, talking, sleeping... see [NebyState].
 * - [ambient] lets an idle Neby come alive now and then: a look around, a wave, a blink.
 * - [interactive] makes Neby tappable; each tap plays the next reaction, then Neby settles back.
 *   [onReaction] hears which one, so a screen can answer it.
 * - [intro] plays once when Neby first appears (a wave hello, say).
 */
@Composable
fun NebyPixel(
    state: NebyState = NebyState.Idle,
    modifier: Modifier = Modifier,
    size: Dp = 64.dp,
    interactive: Boolean = false,
    ambient: Boolean = true,
    intro: NebyState? = null,
    onReaction: ((NebyState) -> Unit)? = null,
) {
    var reaction by remember { mutableStateOf(intro) }
    var flourish by remember { mutableStateOf<NebyState?>(null) }
    var taps by remember { mutableIntStateOf(0) }
    val reduced = nebAnimationsReduced()

    // a tapped reaction plays twice through, then hands back to the base state
    LaunchedEffect(reaction) {
        val r = reaction ?: return@LaunchedEffect
        delay((r.sprite.durationMs * 2L).coerceIn(900L, 2600L))
        reaction = null
    }
    // ambient life for an idle Neby: something small every 7 to 14 seconds
    LaunchedEffect(state, ambient, reduced) {
        if (!ambient || reduced || state != NebyState.Idle) return@LaunchedEffect
        while (true) {
            delay(Random.nextLong(7_000, 14_000))
            flourish = listOf(NebyState.LookAround, NebyState.Wave, NebyState.Blink, NebyState.Hop).random()
            delay(flourish!!.sprite.durationMs.toLong().coerceAtLeast(900L))
            flourish = null
        }
    }

    val shown = reaction ?: flourish ?: state
    var m = modifier.size(size).semantics { contentDescription = "Neby" }
    if (interactive) m = m.nebPressable {
        val next = NebyState.reactions[taps % NebyState.reactions.size]
        taps++
        reaction = next
        onReaction?.invoke(next)
    }
    PixelSpriteView(sprite = shown.sprite, modifier = m)
}
