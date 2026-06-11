package com.consica.code.ui.character

import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.consica.code.core.designsystem.LocalEcoUiConfig
import com.consica.code.core.model.TerraExpression

/**
 * Terra the Owl, drawn entirely with Compose Canvas — no image assets, crisp at
 * any size, and recolorable. Expression changes eyes/brows/cheeks; an optional
 * gentle bounce plays unless reduced motion is on.
 */
@Composable
fun TerraAvatar(
    expression: TerraExpression,
    modifier: Modifier = Modifier,
    size: Dp = 96.dp,
    bounce: Boolean = true,
) {
    val config = LocalEcoUiConfig.current
    val offsetY: Float
    if (bounce && !config.reducedMotion) {
        val transition = rememberInfiniteTransition(label = "terraBounce")
        val animated by transition.animateFloat(
            initialValue = 0f,
            targetValue = -6f,
            animationSpec = infiniteRepeatable(
                animation = tween(900),
                repeatMode = RepeatMode.Reverse,
            ),
            label = "terraBounceY",
        )
        offsetY = animated
    } else {
        offsetY = 0f
    }

    Canvas(modifier = modifier.size(size)) {
        translate(top = offsetY) {
            drawTerra(expression)
        }
    }
}

private fun DrawScope.drawTerra(expression: TerraExpression) {
    val w = size.width
    val h = size.height
    val cx = w / 2f

    val bodyColor = Color(0xFF6D4C41)
    val bellyColor = Color(0xFFD7CCC8)
    val faceColor = Color(0xFF8D6E63)
    val beakColor = Color(0xFFFFB300)
    val eyeWhite = Color(0xFFFFFFFF)
    val pupil = Color(0xFF1A1A1A)
    val leafColor = Color(0xFF66BB6A)

    // Ears / tufts
    val earPath = Path().apply {
        moveTo(cx - w * 0.30f, h * 0.22f)
        lineTo(cx - w * 0.38f, h * 0.04f)
        lineTo(cx - w * 0.16f, h * 0.14f)
        close()
        moveTo(cx + w * 0.30f, h * 0.22f)
        lineTo(cx + w * 0.38f, h * 0.04f)
        lineTo(cx + w * 0.16f, h * 0.14f)
        close()
    }
    drawPath(earPath, bodyColor)

    // Body
    drawOval(
        color = bodyColor,
        topLeft = Offset(cx - w * 0.38f, h * 0.10f),
        size = Size(w * 0.76f, h * 0.84f),
    )

    // Belly
    drawOval(
        color = bellyColor,
        topLeft = Offset(cx - w * 0.24f, h * 0.42f),
        size = Size(w * 0.48f, h * 0.46f),
    )

    // Face disc
    drawOval(
        color = faceColor,
        topLeft = Offset(cx - w * 0.30f, h * 0.16f),
        size = Size(w * 0.60f, h * 0.36f),
    )

    val eyeY = h * 0.32f
    val eyeRadius = w * 0.10f
    val leftEye = Offset(cx - w * 0.14f, eyeY)
    val rightEye = Offset(cx + w * 0.14f, eyeY)

    val sleepy = expression == TerraExpression.SLEEPY
    val thinking = expression == TerraExpression.THINKING
    val confused = expression == TerraExpression.CONFUSED
    val focusedLook = expression == TerraExpression.FOCUSED || expression == TerraExpression.PROFESSIONAL

    if (sleepy) {
        // closed eyes: arcs
        drawArc(
            color = pupil,
            startAngle = 0f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(leftEye.x - eyeRadius, leftEye.y - eyeRadius / 2),
            size = Size(eyeRadius * 2, eyeRadius),
            style = Stroke(width = w * 0.02f),
        )
        drawArc(
            color = pupil,
            startAngle = 0f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(rightEye.x - eyeRadius, rightEye.y - eyeRadius / 2),
            size = Size(eyeRadius * 2, eyeRadius),
            style = Stroke(width = w * 0.02f),
        )
    } else {
        drawCircle(eyeWhite, eyeRadius, leftEye)
        drawCircle(eyeWhite, eyeRadius, rightEye)
        val pupilOffset = when {
            thinking -> Offset(eyeRadius * 0.35f, -eyeRadius * 0.35f)
            confused -> Offset(-eyeRadius * 0.3f, 0f)
            else -> Offset(0f, eyeRadius * 0.1f)
        }
        val pupilR = if (expression == TerraExpression.EXCITED) eyeRadius * 0.55f else eyeRadius * 0.45f
        drawCircle(pupil, pupilR, leftEye + pupilOffset)
        drawCircle(pupil, pupilR, rightEye + pupilOffset)
        // sparkle
        if (expression == TerraExpression.EXCITED || expression == TerraExpression.PROUD) {
            drawCircle(eyeWhite, pupilR * 0.3f, leftEye + pupilOffset + Offset(-pupilR * 0.3f, -pupilR * 0.3f))
            drawCircle(eyeWhite, pupilR * 0.3f, rightEye + pupilOffset + Offset(-pupilR * 0.3f, -pupilR * 0.3f))
        }
    }

    // Brows for focused/professional
    if (focusedLook) {
        val browStroke = w * 0.025f
        drawLine(
            pupil,
            Offset(leftEye.x - eyeRadius, leftEye.y - eyeRadius * 1.2f),
            Offset(leftEye.x + eyeRadius * 0.7f, leftEye.y - eyeRadius * 1.5f),
            strokeWidth = browStroke,
        )
        drawLine(
            pupil,
            Offset(rightEye.x - eyeRadius * 0.7f, rightEye.y - eyeRadius * 1.5f),
            Offset(rightEye.x + eyeRadius, rightEye.y - eyeRadius * 1.2f),
            strokeWidth = browStroke,
        )
    }

    // Beak
    val beak = Path().apply {
        moveTo(cx - w * 0.05f, h * 0.40f)
        lineTo(cx + w * 0.05f, h * 0.40f)
        lineTo(cx, h * 0.48f)
        close()
    }
    drawPath(beak, beakColor)

    // Cheeks for happy/proud/encouraging
    if (expression in setOf(TerraExpression.HAPPY, TerraExpression.PROUD, TerraExpression.ENCOURAGING, TerraExpression.EXCITED)) {
        val cheek = Color(0xFFFFAB91).copy(alpha = 0.6f)
        drawCircle(cheek, w * 0.05f, Offset(cx - w * 0.24f, h * 0.42f))
        drawCircle(cheek, w * 0.05f, Offset(cx + w * 0.24f, h * 0.42f))
    }

    // Wings
    drawOval(
        color = bodyColor.copy(alpha = 0.9f),
        topLeft = Offset(cx - w * 0.46f, h * 0.40f),
        size = Size(w * 0.18f, h * 0.36f),
    )
    drawOval(
        color = bodyColor.copy(alpha = 0.9f),
        topLeft = Offset(cx + w * 0.28f, h * 0.40f),
        size = Size(w * 0.18f, h * 0.36f),
    )

    // Tiny leaf on the head — Terra's signature
    val leaf = Path().apply {
        moveTo(cx, h * 0.10f)
        quadraticTo(cx + w * 0.10f, h * 0.02f, cx + w * 0.16f, h * 0.08f)
        quadraticTo(cx + w * 0.08f, h * 0.12f, cx, h * 0.10f)
        close()
    }
    drawPath(leaf, leafColor)
    drawLine(
        leafColor,
        Offset(cx, h * 0.13f),
        Offset(cx + w * 0.04f, h * 0.08f),
        strokeWidth = w * 0.015f,
    )

    // Feet
    drawOval(beakColor, Offset(cx - w * 0.18f, h * 0.90f), Size(w * 0.12f, h * 0.07f))
    drawOval(beakColor, Offset(cx + w * 0.06f, h * 0.90f), Size(w * 0.12f, h * 0.07f))
}
