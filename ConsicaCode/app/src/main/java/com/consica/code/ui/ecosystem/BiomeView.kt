package com.consica.code.ui.ecosystem

import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import com.consica.code.core.design.EcoPalette
import com.consica.code.core.design.LocalReducedMotion
import com.consica.code.core.model.EcosystemItemType

/**
 * Canvas-drawn biome scene. Grows nothing by itself — it simply renders the items the learner has
 * earned. Sky-dwellers (sun, bird, butterfly) float at the top; ground items line the soil. No
 * image assets, so it stays crisp and fully offline.
 */
@Composable
fun BiomeScene(
    items: List<EcosystemItemType>,
    modifier: Modifier = Modifier,
) {
    val reducedMotion = LocalReducedMotion.current
    val sway by if (reducedMotion) {
        rememberStatic(0f)
    } else {
        val t = rememberInfiniteTransition(label = "biome")
        t.animateFloat(
            initialValue = -1f, targetValue = 1f,
            animationSpec = infiniteRepeatable(tween(2600), RepeatMode.Reverse),
            label = "sway",
        )
    }

    Canvas(modifier) {
        val w = size.width
        val h = size.height
        val groundY = h * 0.78f

        // Sky
        drawRect(
            brush = Brush.verticalGradient(
                listOf(EcoPalette.SkyTop, EcoPalette.LeafLight),
                startY = 0f, endY = groundY,
            ),
            size = Size(w, groundY),
        )
        // Soil
        drawRect(
            color = EcoPalette.SoilStrip,
            topLeft = Offset(0f, groundY),
            size = Size(w, h - groundY),
        )
        // Grass line
        drawRect(
            color = EcoPalette.GrowthGreen,
            topLeft = Offset(0f, groundY - h * 0.012f),
            size = Size(w, h * 0.03f),
        )

        val ground = items.filter { it.isGround }
        val sky = items.filter { !it.isGround }

        // Ground items spaced along the soil line.
        val gCount = ground.size.coerceAtLeast(1)
        ground.forEachIndexed { i, type ->
            val x = w * ((i + 1f) / (gCount + 1f))
            drawGroundItem(type, Offset(x, groundY), h, sway)
        }

        // Sky items spread across the upper third.
        val sCount = sky.size.coerceAtLeast(1)
        sky.forEachIndexed { i, type ->
            val x = w * ((i + 1f) / (sCount + 1f))
            val y = h * (0.12f + 0.10f * (i % 3))
            drawSkyItem(type, Offset(x, y), w, sway)
        }
    }
}

private val EcosystemItemType.isGround: Boolean
    get() = this in setOf(
        EcosystemItemType.SPROUT, EcosystemItemType.FLOWER, EcosystemItemType.TREE,
        EcosystemItemType.MUSHROOM, EcosystemItemType.ROCK, EcosystemItemType.WATER,
    )

@Composable
private fun rememberStatic(value: Float) =
    androidx.compose.runtime.remember { androidx.compose.runtime.mutableFloatStateOf(value) }

private fun DrawScope.drawGroundItem(type: EcosystemItemType, base: Offset, h: Float, sway: Float) {
    val unit = h * 0.13f
    when (type) {
        EcosystemItemType.SPROUT -> {
            drawLine(EcoPalette.GrowthGreen, base, Offset(base.x, base.y - unit), unit * 0.12f)
            leaf(Offset(base.x, base.y - unit), unit * 0.5f, sway * 6f, EcoPalette.GrowthGreen)
            leaf(Offset(base.x, base.y - unit * 0.8f), -unit * 0.5f, sway * 6f, EcoPalette.ForestGreenLight)
        }
        EcosystemItemType.FLOWER -> {
            drawLine(EcoPalette.ForestGreen, base, Offset(base.x, base.y - unit), unit * 0.1f)
            val c = Offset(base.x + sway * 3f, base.y - unit)
            repeat(5) { k ->
                val a = k * (2.0 * Math.PI / 5.0)
                val px = c.x + (unit * 0.4f) * kotlin.math.cos(a).toFloat()
                val py = c.y + (unit * 0.4f) * kotlin.math.sin(a).toFloat()
                drawCircle(EcoPalette.SunYellow, unit * 0.28f, Offset(px, py))
            }
            drawCircle(EcoPalette.SunYellowDeep, unit * 0.26f, c)
        }
        EcosystemItemType.TREE -> {
            drawRect(
                EcoPalette.DryBrown,
                topLeft = Offset(base.x - unit * 0.12f, base.y - unit * 1.4f),
                size = Size(unit * 0.24f, unit * 1.4f),
            )
            drawCircle(EcoPalette.ForestGreen, unit * 0.8f, Offset(base.x + sway * 4f, base.y - unit * 1.7f))
            drawCircle(EcoPalette.GrowthGreen, unit * 0.55f, Offset(base.x - unit * 0.4f, base.y - unit * 1.4f))
            drawCircle(EcoPalette.GrowthGreen, unit * 0.55f, Offset(base.x + unit * 0.4f, base.y - unit * 1.4f))
        }
        EcosystemItemType.MUSHROOM -> {
            drawRect(
                EcoPalette.LeafLight,
                topLeft = Offset(base.x - unit * 0.12f, base.y - unit * 0.5f),
                size = Size(unit * 0.24f, unit * 0.5f),
            )
            drawArc(
                color = Color(0xFFD7674F),
                startAngle = 180f, sweepAngle = 180f, useCenter = true,
                topLeft = Offset(base.x - unit * 0.45f, base.y - unit * 0.8f),
                size = Size(unit * 0.9f, unit * 0.9f),
            )
        }
        EcosystemItemType.ROCK -> {
            drawCircle(EcoPalette.StoneGray, unit * 0.4f, Offset(base.x, base.y - unit * 0.2f))
        }
        EcosystemItemType.WATER -> {
            drawOval(
                EcoPalette.RiverBlue.copy(alpha = 0.7f),
                topLeft = Offset(base.x - unit * 0.6f, base.y - unit * 0.18f),
                size = Size(unit * 1.2f, unit * 0.36f),
            )
        }
        else -> Unit
    }
}

private fun DrawScope.drawSkyItem(type: EcosystemItemType, c: Offset, w: Float, sway: Float) {
    val unit = w * 0.06f
    when (type) {
        EcosystemItemType.SUN -> {
            drawCircle(EcoPalette.SunYellow, unit, c)
            repeat(8) { k ->
                val a = k * (Math.PI / 4.0)
                val sx = c.x + (unit * 1.3f) * kotlin.math.cos(a).toFloat()
                val sy = c.y + (unit * 1.3f) * kotlin.math.sin(a).toFloat()
                drawLine(EcoPalette.SunYellowDeep, c, Offset(sx, sy), unit * 0.12f)
            }
        }
        EcosystemItemType.BUTTERFLY -> {
            val cx = c.x + sway * 8f
            drawCircle(EcoPalette.RiverBlue, unit * 0.45f, Offset(cx - unit * 0.4f, c.y))
            drawCircle(EcoPalette.SunYellow, unit * 0.45f, Offset(cx + unit * 0.4f, c.y))
            drawLine(EcoPalette.SoilDark, Offset(cx, c.y - unit * 0.4f), Offset(cx, c.y + unit * 0.4f), unit * 0.1f)
        }
        EcosystemItemType.BIRD -> {
            val cx = c.x + sway * 10f
            val p = Path().apply {
                moveTo(cx - unit, c.y)
                quadraticTo(cx - unit * 0.5f, c.y - unit * 0.6f, cx, c.y)
                quadraticTo(cx + unit * 0.5f, c.y - unit * 0.6f, cx + unit, c.y)
            }
            drawPath(p, EcoPalette.SoilDark, style = androidx.compose.ui.graphics.drawscope.Stroke(unit * 0.16f))
        }
        else -> Unit
    }
}

private fun DrawScope.leaf(at: Offset, dx: Float, sway: Float, color: Color) {
    drawOval(
        color,
        topLeft = Offset(at.x + (if (dx < 0) dx else 0f) + sway, at.y - dx * 0.15f),
        size = Size(kotlin.math.abs(dx), kotlin.math.abs(dx) * 0.55f),
    )
}
