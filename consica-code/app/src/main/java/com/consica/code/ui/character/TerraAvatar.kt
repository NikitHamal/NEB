package com.consica.code.ui.character

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
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.platform.testTag
import com.consica.code.domain.model.TerraExpression
import com.consica.code.ui.theme.LocalReducedMotion

private val BodyColor = Color(0xFF8D6E63)
private val BellyColor = Color(0xFFD7CCC8)
private val WingColor = Color(0xFF6D4C41)
private val BeakColor = Color(0xFFFFB300)
private val EyeWhite = Color(0xFFFFFFFF)
private val EyeDark = Color(0xFF1A1A1A)
private val BrowColor = Color(0xFF4E342E)
private val GlassColor = Color(0xFF37474F)
private val BlushColor = Color(0x55EF9A9A)

/**
 * Terra the Owl, fully vector-drawn so she scales to any size and theme.
 * Gently bobs unless reduced motion is enabled.
 */
@Composable
fun TerraAvatar(
    expression: TerraExpression,
    modifier: Modifier = Modifier,
    animated: Boolean = true,
) {
    val reducedMotion = LocalReducedMotion.current
    val bob: Float = if (animated && !reducedMotion) {
        val transition = rememberInfiniteTransition(label = "terraBob")
        val value by transition.animateFloat(
            initialValue = 0f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 1600),
                repeatMode = RepeatMode.Reverse,
            ),
            label = "terraBobValue",
        )
        value
    } else 0f

    Canvas(modifier = modifier.testTag("terra_avatar")) {
        val w = size.width
        val h = size.height
        translate(top = bob * h * 0.03f) {
            drawTerra(w, h, expression)
        }
    }
}

private fun DrawScope.drawTerra(w: Float, h: Float, expression: TerraExpression) {
    val cx = w / 2f

    // Ear tufts
    val tuft = Path().apply {
        moveTo(cx - w * 0.30f, h * 0.22f)
        lineTo(cx - w * 0.38f, h * 0.04f)
        lineTo(cx - w * 0.16f, h * 0.14f)
        close()
        moveTo(cx + w * 0.30f, h * 0.22f)
        lineTo(cx + w * 0.38f, h * 0.04f)
        lineTo(cx + w * 0.16f, h * 0.14f)
        close()
    }
    drawPath(tuft, BodyColor)

    // Body
    drawOval(
        color = BodyColor,
        topLeft = Offset(cx - w * 0.40f, h * 0.10f),
        size = Size(w * 0.80f, h * 0.85f),
    )

    // Wings
    rotate(degrees = -14f, pivot = Offset(cx - w * 0.36f, h * 0.50f)) {
        drawOval(
            color = WingColor,
            topLeft = Offset(cx - w * 0.52f, h * 0.36f),
            size = Size(w * 0.24f, h * 0.42f),
        )
    }
    rotate(degrees = 14f, pivot = Offset(cx + w * 0.36f, h * 0.50f)) {
        drawOval(
            color = WingColor,
            topLeft = Offset(cx + w * 0.28f, h * 0.36f),
            size = Size(w * 0.24f, h * 0.42f),
        )
    }

    // Belly
    drawOval(
        color = BellyColor,
        topLeft = Offset(cx - w * 0.26f, h * 0.40f),
        size = Size(w * 0.52f, h * 0.50f),
    )

    // Feet
    drawOval(BeakColor, Offset(cx - w * 0.22f, h * 0.88f), Size(w * 0.16f, h * 0.09f))
    drawOval(BeakColor, Offset(cx + w * 0.06f, h * 0.88f), Size(w * 0.16f, h * 0.09f))

    val eyeY = h * 0.34f
    val eyeRadius = w * 0.135f
    val leftEye = Offset(cx - w * 0.17f, eyeY)
    val rightEye = Offset(cx + w * 0.17f, eyeY)

    when (expression) {
        TerraExpression.PROUD, TerraExpression.SLEEPY -> {
            // Closed, content arcs
            val stroke = Stroke(width = w * 0.035f)
            val sweep = if (expression == TerraExpression.PROUD) -160f else 160f
            for (center in listOf(leftEye, rightEye)) {
                drawArc(
                    color = EyeDark,
                    startAngle = if (sweep < 0) 190f else 10f,
                    sweepAngle = sweep,
                    useCenter = false,
                    topLeft = Offset(center.x - eyeRadius * 0.8f, center.y - eyeRadius * 0.55f),
                    size = Size(eyeRadius * 1.6f, eyeRadius * 1.1f),
                    style = stroke,
                )
            }
        }
        else -> {
            val pupilScale = when (expression) {
                TerraExpression.EXCITED -> 0.62f
                TerraExpression.CONFUSED -> 0.42f
                TerraExpression.FOCUSED, TerraExpression.PROFESSIONAL -> 0.46f
                else -> 0.52f
            }
            val pupilOffset = when (expression) {
                TerraExpression.THINKING -> Offset(eyeRadius * 0.25f, -eyeRadius * 0.3f)
                TerraExpression.CONFUSED -> Offset(-eyeRadius * 0.2f, 0f)
                else -> Offset.Zero
            }
            for (center in listOf(leftEye, rightEye)) {
                drawCircle(EyeWhite, eyeRadius, center)
                drawCircle(EyeDark, eyeRadius * pupilScale, center + pupilOffset)
                drawCircle(EyeWhite, eyeRadius * 0.16f, center + pupilOffset + Offset(eyeRadius * 0.18f, -eyeRadius * 0.18f))
            }
            // Half-lids for focused looks
            if (expression == TerraExpression.FOCUSED || expression == TerraExpression.PROFESSIONAL) {
                for (center in listOf(leftEye, rightEye)) {
                    drawArc(
                        color = BodyColor,
                        startAngle = 180f,
                        sweepAngle = 180f,
                        useCenter = true,
                        topLeft = Offset(center.x - eyeRadius, center.y - eyeRadius * 1.45f),
                        size = Size(eyeRadius * 2f, eyeRadius * 1.3f),
                    )
                }
            }
        }
    }

    // Brows
    val browStroke = Stroke(width = w * 0.035f)
    when (expression) {
        TerraExpression.THINKING, TerraExpression.CONFUSED -> {
            rotate(degrees = -12f, pivot = leftEye) {
                drawLine(BrowColor, Offset(leftEye.x - eyeRadius, eyeY - eyeRadius * 1.35f), Offset(leftEye.x + eyeRadius * 0.7f, eyeY - eyeRadius * 1.35f), browStroke.width)
            }
            rotate(degrees = 16f, pivot = rightEye) {
                drawLine(BrowColor, Offset(rightEye.x - eyeRadius * 0.7f, eyeY - eyeRadius * 1.5f), Offset(rightEye.x + eyeRadius, eyeY - eyeRadius * 1.5f), browStroke.width)
            }
        }
        TerraExpression.EXCITED, TerraExpression.ENCOURAGING -> {
            for (center in listOf(leftEye, rightEye)) {
                drawArc(
                    color = BrowColor,
                    startAngle = 200f,
                    sweepAngle = 140f,
                    useCenter = false,
                    topLeft = Offset(center.x - eyeRadius * 0.9f, center.y - eyeRadius * 1.8f),
                    size = Size(eyeRadius * 1.8f, eyeRadius * 1.0f),
                    style = browStroke,
                )
            }
        }
        else -> Unit
    }

    // Professional glasses
    if (expression == TerraExpression.PROFESSIONAL) {
        val stroke = Stroke(width = w * 0.025f)
        for (center in listOf(leftEye, rightEye)) {
            drawCircle(GlassColor, eyeRadius * 1.15f, center, style = stroke)
        }
        drawLine(GlassColor, Offset(leftEye.x + eyeRadius * 1.15f, eyeY), Offset(rightEye.x - eyeRadius * 1.15f, eyeY), stroke.width)
    }

    // Beak
    val beak = Path().apply {
        moveTo(cx - w * 0.06f, h * 0.46f)
        lineTo(cx + w * 0.06f, h * 0.46f)
        lineTo(cx, h * 0.56f)
        close()
    }
    drawPath(beak, BeakColor)

    // Blush for warm expressions
    if (expression == TerraExpression.HAPPY || expression == TerraExpression.ENCOURAGING || expression == TerraExpression.PROUD) {
        drawOval(BlushColor, Offset(cx - w * 0.34f, h * 0.46f), Size(w * 0.13f, h * 0.07f))
        drawOval(BlushColor, Offset(cx + w * 0.21f, h * 0.46f), Size(w * 0.13f, h * 0.07f))
    }

    // Sleepy "zzz" dots
    if (expression == TerraExpression.SLEEPY) {
        drawCircle(EyeDark, w * 0.015f, Offset(cx + w * 0.34f, h * 0.16f))
        drawCircle(EyeDark, w * 0.022f, Offset(cx + w * 0.40f, h * 0.10f))
    }
}

/** Tiny helper rect kept for potential hit-testing extensions. */
@Suppress("unused")
private fun terraBounds(w: Float, h: Float): Rect = Rect(0f, 0f, w, h)
