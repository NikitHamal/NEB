package com.consica.code.ui.common

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.rotate
import com.consica.code.core.designsystem.LeafMid
import com.consica.code.core.designsystem.LocalEcoUiConfig
import com.consica.code.core.designsystem.RiverBlue
import com.consica.code.core.designsystem.SunYellow
import kotlin.random.Random

private data class LeafParticle(
    val xFraction: Float,
    val speed: Float,
    val size: Float,
    val phase: Float,
    val spin: Float,
    val color: Color,
)

/**
 * Celebratory falling-leaf confetti overlay. Respects reduced-motion by
 * rendering nothing when motion is reduced.
 */
@Composable
fun LeafConfetti(
    modifier: Modifier = Modifier,
    particleCount: Int = 28,
) {
    val config = LocalEcoUiConfig.current
    if (config.reducedMotion) return

    val particles = remember {
        val colors = listOf(LeafMid, SunYellow, RiverBlue, Color(0xFF66BB6A), Color(0xFF9CCC65))
        List(particleCount) {
            LeafParticle(
                xFraction = Random.nextFloat(),
                speed = 0.5f + Random.nextFloat() * 0.8f,
                size = 14f + Random.nextFloat() * 16f,
                phase = Random.nextFloat(),
                spin = (Random.nextFloat() - 0.5f) * 720f,
                color = colors[Random.nextInt(colors.size)],
            )
        }
    }

    val transition = rememberInfiniteTransition(label = "confetti")
    val t by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(4000, easing = LinearEasing)),
        label = "confettiT",
    )

    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height
        for (p in particles) {
            val progress = ((t * p.speed) + p.phase) % 1f
            val y = progress * (h + 80f) - 40f
            val sway = kotlin.math.sin(progress * 6f * Math.PI.toFloat() + p.phase * 10f) * 40f
            val x = p.xFraction * w + sway
            rotate(degrees = p.spin * progress, pivot = Offset(x, y)) {
                val path = Path().apply {
                    moveTo(x, y - p.size / 2)
                    quadraticTo(x + p.size / 2, y, x, y + p.size / 2)
                    quadraticTo(x - p.size / 2, y, x, y - p.size / 2)
                    close()
                }
                drawPath(path, p.color.copy(alpha = 0.85f))
            }
        }
    }
}
