package com.consica.code.ui.components

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.rotate
import com.consica.code.core.design.EcoPalette
import com.consica.code.core.design.LocalReducedMotion
import kotlin.random.Random

private data class Leaf(
    val xFraction: Float,
    val delay: Float,
    val size: Float,
    val rotation: Float,
    val drift: Float,
    val color: androidx.compose.ui.graphics.Color,
)

/**
 * A burst of falling leaves used to celebrate growth/success. Purely decorative and skipped
 * entirely when reduced-motion is enabled. [play] drives a single fall when toggled true.
 */
@Composable
fun LeafConfetti(play: Boolean, modifier: Modifier = Modifier, count: Int = 24) {
    if (LocalReducedMotion.current) return

    val leaves = remember {
        val palette = listOf(
            EcoPalette.GrowthGreen, EcoPalette.ForestGreenLight,
            EcoPalette.SunYellow, EcoPalette.ForestGreen,
        )
        List(count) {
            Leaf(
                xFraction = Random.nextFloat(),
                delay = Random.nextFloat() * 0.3f,
                size = 14f + Random.nextFloat() * 16f,
                rotation = Random.nextFloat() * 360f,
                drift = (Random.nextFloat() - 0.5f) * 0.25f,
                color = palette[Random.nextInt(palette.size)],
            )
        }
    }

    val progress by animateFloatAsState(
        targetValue = if (play) 1f else 0f,
        animationSpec = tween(1600),
        label = "confetti",
    )

    if (progress <= 0f) return

    Canvas(modifier.fillMaxSize()) {
        leaves.forEach { leaf ->
            val local = ((progress - leaf.delay) / (1f - leaf.delay)).coerceIn(0f, 1f)
            if (local <= 0f) return@forEach
            val x = (leaf.xFraction + leaf.drift * local) * size.width
            val y = local * (size.height + 40f) - 20f
            val alpha = (1f - local).coerceIn(0f, 1f)
            rotate(degrees = leaf.rotation + local * 220f, pivot = Offset(x, y)) {
                drawLeaf(Offset(x, y), leaf.size, leaf.color.copy(alpha = alpha))
            }
        }
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawLeaf(
    center: Offset,
    s: Float,
    color: androidx.compose.ui.graphics.Color,
) {
    val path = Path().apply {
        moveTo(center.x, center.y - s / 2f)
        cubicTo(
            center.x + s / 2f, center.y - s / 2f,
            center.x + s / 2f, center.y + s / 2f,
            center.x, center.y + s / 2f,
        )
        cubicTo(
            center.x - s / 2f, center.y + s / 2f,
            center.x - s / 2f, center.y - s / 2f,
            center.x, center.y - s / 2f,
        )
        close()
    }
    drawPath(path, color)
    // central vein
    drawLine(
        color = color.copy(alpha = color.alpha * 0.6f),
        start = Offset(center.x, center.y - s / 2f),
        end = Offset(center.x, center.y + s / 2f),
        strokeWidth = s * 0.06f,
    )
}
