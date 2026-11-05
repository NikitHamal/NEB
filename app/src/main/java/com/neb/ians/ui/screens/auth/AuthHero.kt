@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoStories
import androidx.compose.material.icons.rounded.Forum
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.State
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.R
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebMorphBlob
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.nebShape
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebSlowSpatialSpec
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.PI
import kotlin.math.sin

/**
 * The sign-in hero, taken from the landing page's glyph stage: one tonal blob that keeps
 * morphing through the landing silhouettes with the N mark sitting in it, and three glyph
 * tiles (search, forum, library) that spring out of it and then drift. A tap squeezes the
 * mark and lands a haptic. Flat fills only, no shadows, no outlines.
 */
@Composable
fun AuthHero(modifier: Modifier = Modifier, dark: Boolean = false) {
    val reduced = nebAnimationsReduced()
    val tactile = rememberTactileFeedback()
    val scope = rememberCoroutineScope()
    val enter = remember { Animatable(if (reduced) 1f else 0f) }
    val squish = remember { Animatable(1f) }
    val morph = remember { Animatable(0f) }
    val enterSpec = nebSlowSpatialSpec<Float>()
    val tapSpec = nebFastSpatialSpec<Float>()
    val shapes = remember {
        listOf(
            NebGlyphShapes.Cookie,
            NebGlyphShapes.Sunny,
            NebGlyphShapes.Flower,
            NebGlyphShapes.Clover,
            NebGlyphShapes.Cookie
        )
    }

    LaunchedEffect(Unit) {
        if (!reduced) enter.animateTo(1f, enterSpec)
    }
    LaunchedEffect(reduced) {
        if (reduced) return@LaunchedEffect
        delay(900)
        while (true) {
            for (i in 1..4) {
                morph.animateTo(
                    i.toFloat(),
                    spring(dampingRatio = 0.6f, stiffness = Spring.StiffnessVeryLow)
                )
                delay(1500)
            }
            morph.snapTo(0f)
        }
    }

    val loop = rememberInfiniteTransition(label = "auth_hero_loop")
    val spin = loop.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(tween(56000, easing = LinearEasing), RepeatMode.Restart),
        label = "auth_hero_spin"
    )
    val bob = loop.animateFloat(
        initialValue = 0f,
        targetValue = (2 * PI).toFloat(),
        animationSpec = infiniteRepeatable(tween(5200, easing = LinearEasing), RepeatMode.Restart),
        label = "auth_hero_bob"
    )

    BoxWithConstraints(
        modifier = modifier.clickable(
            interactionSource = remember { MutableInteractionSource() },
            indication = null
        ) {
            tactile.perform(TactileType.LightTap)
            scope.launch {
                squish.snapTo(0.84f)
                squish.animateTo(1f, tapSpec)
            }
        }
    ) {
        val blob = minOf(maxWidth * 0.64f, maxHeight * 0.84f)

        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .size(blob)
                .graphicsLayer {
                    val s = 0.4f + 0.6f * enter.value
                    scaleX = s
                    scaleY = s
                    alpha = enter.value.coerceIn(0f, 1f)
                }
        ) {
            NebMorphBlob(
                shapes = shapes,
                color = NebTone.Azure.container(dark),
                modifier = Modifier.fillMaxSize(),
                rotation = { spin.value },
                position = { morph.value }
            )
            Image(
                painter = painterResource(R.drawable.ic_launcher_foreground),
                contentDescription = null,
                modifier = Modifier
                    .align(Alignment.Center)
                    .fillMaxSize()
                    .graphicsLayer {
                        val s = (0.86f + 0.14f * enter.value) * squish.value * 1.12f
                        scaleX = s
                        scaleY = s
                        rotationZ = (1f - enter.value) * -14f
                    }
            )
        }

        Satellite(
            polygon = NebGlyphShapes.Sunny,
            tone = NebTone.Sky,
            icon = Icons.Rounded.Search,
            size = 62.dp,
            dx = -blob * 0.50f,
            dy = -blob * 0.30f,
            delayMs = 380,
            phase = 0f,
            reduced = reduced,
            dark = dark,
            bob = bob
        )
        Satellite(
            polygon = NebGlyphShapes.Flower,
            tone = NebTone.Aqua,
            icon = Icons.Rounded.Forum,
            size = 56.dp,
            dx = blob * 0.52f,
            dy = -blob * 0.10f,
            delayMs = 520,
            phase = 2.1f,
            reduced = reduced,
            dark = dark,
            bob = bob
        )
        Satellite(
            polygon = NebGlyphShapes.Clover,
            tone = NebTone.Peri,
            icon = Icons.Rounded.AutoStories,
            size = 58.dp,
            dx = -blob * 0.40f,
            dy = blob * 0.36f,
            delayMs = 660,
            phase = 4.2f,
            reduced = reduced,
            dark = dark,
            bob = bob
        )
    }
}

@Composable
private fun androidx.compose.foundation.layout.BoxScope.Satellite(
    polygon: RoundedPolygon,
    tone: NebTone,
    icon: ImageVector,
    size: Dp,
    dx: Dp,
    dy: Dp,
    delayMs: Long,
    phase: Float,
    reduced: Boolean,
    dark: Boolean,
    bob: State<Float>
) {
    val pop = remember { Animatable(if (reduced) 1f else 0f) }
    val spec = nebSlowSpatialSpec<Float>()
    LaunchedEffect(Unit) {
        if (!reduced) {
            delay(delayMs)
            pop.animateTo(1f, spec)
        }
    }
    Box(
        modifier = Modifier
            .align(Alignment.Center)
            .offset(x = dx, y = dy)
            .size(size)
            .graphicsLayer {
                val p = pop.value
                val s = p.coerceAtLeast(0f)
                scaleX = s
                scaleY = s
                alpha = p.coerceIn(0f, 1f)
                translationY = if (reduced) 0f else sin(bob.value + phase) * 6.dp.toPx()
                rotationZ = (1f - p) * 40f
            }
            .background(tone.container(dark), nebShape(polygon)),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = tone.deep(dark),
            modifier = Modifier.size(size * 0.46f)
        )
    }
}
