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
import androidx.compose.ui.unit.IntRect
import com.neb.ians.ui.theme.LocalSiteTheme
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
 * - [look] is what Neby wears; null follows the server (an admin's pick, or the festival's dress).
 * - [avatar] frames Neby for a round avatar: the figure centred, no ground shadow, hats kept.
 */
@Composable
fun NebyPixel(
    state: NebyState = NebyState.Idle,
    modifier: Modifier = Modifier,
    size: Dp = 64.dp,
    interactive: Boolean = false,
    ambient: Boolean = true,
    intro: NebyState? = null,
    look: NebyLook? = null,
    avatar: Boolean = false,
    onReaction: ((NebyState) -> Unit)? = null,
) {
    val server = LocalSiteTheme.current.theme?.neby
    val dress = look ?: NebyLook.fromKey(server?.look)
    val alive = ambient && server?.ambient != false
    val tappable = interactive && server?.reactions != false
    // a hello plays the season's own animation when there is one (tika at Dashain), as on the web
    val festiveHello = server?.greet?.let { NebyState.fromName(it) }?.takeIf { it != NebyState.Idle }
    var reaction by remember { mutableStateOf(if (intro != null) festiveHello ?: intro else null) }
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
    LaunchedEffect(state, alive, reduced) {
        if (!alive || reduced || state != NebyState.Idle) return@LaunchedEffect
        while (true) {
            delay(Random.nextLong(7_000, 14_000))
            flourish = listOf(NebyState.LookAround, NebyState.Wave, NebyState.Blink, NebyState.Hop).random()
            delay(flourish!!.sprite.durationMs.toLong().coerceAtLeast(900L))
            flourish = null
        }
    }

    val shown = reaction ?: flourish ?: state
    var m = modifier.size(size).semantics { contentDescription = "Neby" }
    if (tappable) m = m.nebPressable {
        val next = NebyState.reactions[taps % NebyState.reactions.size]
        taps++
        reaction = next
        onReaction?.invoke(next)
    }
    PixelSpriteView(sprite = shown.sprite(dress), modifier = m, src = if (avatar) avatarCrop(dress) else null)
}

/**
 * The part of the 48 x 48 sprite a round avatar shows. The body is centred in it and the ground
 * shadow is left out; a look with a hat gets a taller window so the hat is not cut off.
 */
fun avatarCrop(look: NebyLook): IntRect = if (look.hat) IntRect(3, 2, 45, 44) else IntRect(6, 10, 42, 46)
