package com.consica.code.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.rotate
import com.consica.code.ui.theme.LocalReducedMotion
import kotlin.math.sin
import kotlin.random.Random

private val LeafColors = listOf(
    Color(0xFF4CAF50), Color(0xFF2D5A27), Color(0xFF8BC34A),
    Color(0xFFFFD54F), Color(0xFF4DA8DA), Color(0xFFA5D6A7),
)

private data class LeafParticle(
    val xFraction: Float,
    val speed: Float,
    val phase: Float,
    val size: Float,
    val color: Color,
    val spin: Float,
)

/**
 * Celebratory falling-leaf overlay. Draw it above content while [active];
 * renders nothing when reduced motion is enabled.
 */
@Composable
fun LeafConfetti(
    active: Boolean,
    modifier: Modifier = Modifier,
    particleCount: Int = 28,
) {
    val reducedMotion = LocalReducedMotion.current
    if (!active || reducedMotion) return

    val particles = remember {
        List(particleCount) {
            val random = Random(it * 7919)
            LeafParticle(
                xFraction = random.nextFloat(),
                speed = 0.5f + random.nextFloat() * 0.8f,
                phase = random.nextFloat() * 6.28f,
                size = 14f + random.nextFloat() * 16f,
                color = LeafColors[it % LeafColors.size],
                spin = (random.nextFloat() - 0.5f) * 720f,
            )
        }
    }

    val transition = rememberInfiniteTransition(label = "leafFall")
    val time by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(3200, easing = LinearEasing)),
        label = "leafTime",
    )

    Canvas(modifier.fillMaxSize()) {
        for (particle in particles) {
            val progress = (time * particle.speed + particle.phase / 6.28f) % 1f
            val y = progress * (size.height + 80f) - 40f
            val sway = sin(progress * 12f + particle.phase) * size.width * 0.04f
            val x = particle.xFraction * size.width + sway
            rotate(degrees = progress * particle.spin, pivot = Offset(x, y)) {
                drawOval(
                    color = particle.color.copy(alpha = (1f - progress).coerceIn(0.25f, 0.9f)),
                    topLeft = Offset(x - particle.size / 2, y - particle.size / 4),
                    size = Size(particle.size, particle.size / 2),
                )
            }
        }
    }
}
