package com.consica.code.ui.mascot

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
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.EcoPalette
import com.consica.code.core.design.LocalReducedMotion

/**
 * Terra the Owl — the app mascot, drawn entirely with Compose Canvas (no image assets, fully
 * offline and crisp at any size). Subtly bounces unless reduced-motion is on, and changes face
 * to reflect the current [TerraExpression].
 */
@Composable
fun Terra(
    expression: TerraExpression,
    modifier: Modifier = Modifier,
    size: Dp = 96.dp,
) {
    val reducedMotion = LocalReducedMotion.current
    val cd = stringResource(R.string.cd_mascot_terra)

    val bounce by if (reducedMotion) {
        rememberStaticFloat(0f)
    } else {
        val transition = rememberInfiniteTransition(label = "terra")
        transition.animateFloat(
            initialValue = 0f, targetValue = 1f,
            animationSpec = infiniteRepeatable(tween(1400), RepeatMode.Reverse),
            label = "bounce",
        )
    }

    Canvas(
        modifier = modifier
            .size(size)
            .semantics { contentDescription = cd }
    ) {
        val dy = if (reducedMotion) 0f else -(bounce * this.size.height * 0.04f)
        translate(top = dy) { drawOwl(expression) }
    }
}

@Composable
private fun rememberStaticFloat(value: Float) = androidx.compose.runtime.remember {
    androidx.compose.runtime.mutableFloatStateOf(value)
}

private fun DrawScope.drawOwl(expression: TerraExpression) {
    val w = size.width
    val h = size.height
    val body = EcoPalette.ForestGreen
    val belly = EcoPalette.LeafLight
    val accent = EcoPalette.SunYellow
    val dark = EcoPalette.SoilDark

    // Ear tufts
    val tuft = Path().apply {
        moveTo(w * 0.28f, h * 0.18f); lineTo(w * 0.36f, h * 0.30f); lineTo(w * 0.22f, h * 0.30f); close()
        moveTo(w * 0.72f, h * 0.18f); lineTo(w * 0.78f, h * 0.30f); lineTo(w * 0.64f, h * 0.30f); close()
    }
    drawPath(tuft, body)

    // Body
    drawOval(
        color = body,
        topLeft = Offset(w * 0.16f, h * 0.22f),
        size = Size(w * 0.68f, h * 0.66f),
    )
    // Belly
    drawOval(
        color = belly,
        topLeft = Offset(w * 0.30f, h * 0.42f),
        size = Size(w * 0.40f, h * 0.42f),
    )

    // Eyes (white discs)
    val eyeR = w * 0.15f
    val eyeY = h * 0.42f
    val lx = w * 0.37f
    val rx = w * 0.63f
    drawCircle(belly, eyeR, Offset(lx, eyeY))
    drawCircle(belly, eyeR, Offset(rx, eyeY))

    // Pupils + expression
    val pupilR = eyeR * pupilScale(expression)
    val pupilDy = pupilOffsetY(expression) * eyeR
    if (expression == TerraExpression.Sleepy) {
        // Closed eyes as arcs
        drawArc(dark, 200f, 140f, false, Offset(lx - eyeR, eyeY - eyeR), Size(eyeR * 2, eyeR * 2), style = Stroke(w * 0.02f))
        drawArc(dark, 200f, 140f, false, Offset(rx - eyeR, eyeY - eyeR), Size(eyeR * 2, eyeR * 2), style = Stroke(w * 0.02f))
    } else {
        drawCircle(dark, pupilR, Offset(lx, eyeY + pupilDy))
        drawCircle(dark, pupilR, Offset(rx, eyeY + pupilDy))
        // Sparkle
        drawCircle(belly, pupilR * 0.35f, Offset(lx + pupilR * 0.3f, eyeY + pupilDy - pupilR * 0.3f))
        drawCircle(belly, pupilR * 0.35f, Offset(rx + pupilR * 0.3f, eyeY + pupilDy - pupilR * 0.3f))
    }

    // Brows convey mood
    when (expression) {
        TerraExpression.Thinking, TerraExpression.Focused, TerraExpression.Professional -> {
            drawLine(dark, Offset(lx - eyeR, eyeY - eyeR * 1.1f), Offset(lx + eyeR, eyeY - eyeR * 1.3f), w * 0.025f)
            drawLine(dark, Offset(rx - eyeR, eyeY - eyeR * 1.3f), Offset(rx + eyeR, eyeY - eyeR * 1.1f), w * 0.025f)
        }
        TerraExpression.Confused -> {
            drawLine(dark, Offset(lx - eyeR, eyeY - eyeR * 1.4f), Offset(lx + eyeR, eyeY - eyeR * 1.0f), w * 0.025f)
        }
        else -> { /* relaxed */ }
    }

    // Beak
    val beak = Path().apply {
        moveTo(w * 0.5f, eyeY + eyeR * 0.7f)
        lineTo(w * 0.45f, eyeY + eyeR * 1.3f)
        lineTo(w * 0.55f, eyeY + eyeR * 1.3f)
        close()
    }
    drawPath(beak, accent)

    // Excited/Proud: rosy cheeks
    if (expression == TerraExpression.Excited || expression == TerraExpression.Proud || expression == TerraExpression.Happy) {
        drawCircle(accent.copy(alpha = 0.5f), w * 0.05f, Offset(w * 0.30f, h * 0.56f))
        drawCircle(accent.copy(alpha = 0.5f), w * 0.05f, Offset(w * 0.70f, h * 0.56f))
    }

    // Feet
    drawLine(accent, Offset(w * 0.42f, h * 0.88f), Offset(w * 0.42f, h * 0.93f), w * 0.03f)
    drawLine(accent, Offset(w * 0.58f, h * 0.88f), Offset(w * 0.58f, h * 0.93f), w * 0.03f)
}

private fun pupilScale(e: TerraExpression): Float = when (e) {
    TerraExpression.Excited -> 0.7f
    TerraExpression.Proud, TerraExpression.Happy, TerraExpression.Encouraging -> 0.6f
    TerraExpression.Focused, TerraExpression.Professional -> 0.45f
    else -> 0.55f
}

private fun pupilOffsetY(e: TerraExpression): Float = when (e) {
    TerraExpression.Thinking, TerraExpression.Confused -> -0.25f
    TerraExpression.Proud -> -0.1f
    else -> 0f
}
