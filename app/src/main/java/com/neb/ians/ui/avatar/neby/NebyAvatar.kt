package com.neb.ians.ui.avatar.neby

import android.graphics.Color
import android.graphics.Paint
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.shape.CircleShape
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.cos
import kotlin.math.exp
import kotlin.math.pow
import kotlin.math.sin

@Composable
fun NebyAvatar(
    animation: String = "idle",
    modifier: Modifier = Modifier,
    size: Dp = 64.dp,
    interactive: Boolean = true,
    hero: Boolean = false,
    onReaction: ((String) -> Unit)? = null
) {
    val animMap = remember { NEBY_ANIMATIONS }
    var currentAnim by remember(animation) { mutableStateOf(if (animMap.containsKey(animation)) animation else "idle") }
    var currentExprId by remember { mutableStateOf(EXPR_BY_ID.values.first().id) }
    var targetExprId by remember { mutableStateOf(EXPR_BY_ID.values.first().id) }
    var transitionStartT by remember { mutableStateOf(0.0) }
    var transitionDurS by remember { mutableStateOf(0.2) }
    var transitionKind by remember { mutableStateOf("smooth") }
    var blinkAmount by remember { mutableStateOf(1.0) }
    var isBlinking by remember { mutableStateOf(false) }
    var blinkProgress by remember { mutableStateOf(0.0) }
    var timeSec by remember { mutableStateOf(0.0) }
    var blinkClock by remember { mutableStateOf(0.0) }

    val scope = rememberCoroutineScope()

    fun resolveAnim(name: String): NebyAnimation = animMap[name] ?: animMap.getValue("idle")

    fun playSequence(name: String) {
        currentAnim = name
    }

    fun triggerReaction(type: String) {
        val map = mapOf(
            "wink" to "wink", "love" to "love", "kiss" to "kiss", "celebrate" to "celebrate",
            "dance" to "dance", "scanning" to "scanning", "agree" to "agree", "disagree" to "disagree",
            "laughing" to "laughing", "proud" to "proud", "shy" to "shy", "sleepy" to "sleeping",
            "dizzy" to "dizzy", "angry" to "angry", "notification" to "notification"
        )
        val anim = map[type] ?: if (animMap.containsKey(type)) type else "celebrate"
        playSequence(anim)
        onReaction?.invoke(anim)
        if (anim != "idle") {
            scope.launch {
                delay(3400)
                if (currentAnim == anim) playSequence("idle")
            }
        }
    }

    LaunchedEffect(currentAnim) {
        val first = resolveAnim(currentAnim)
        if (first.steps.isEmpty()) return@LaunchedEffect
        var idx = 0
        var dir = 1
        while (true) {
            val a = resolveAnim(currentAnim)
            if (idx !in a.steps.indices) {
                if (a.playbackMode == "once") break
                idx = if (a.playbackMode == "pingPong" && a.steps.size > 1) {
                    if (idx >= a.steps.size) { dir = -1; a.steps.size - 2 } else { dir = 1; 0 }
                } else 0
                if (idx !in a.steps.indices) idx = 0
            }
            val step = a.steps[idx]
            targetExprId = step.expressionId
            transitionStartT = timeSec
            transitionDurS = (step.transitionMs / 1000.0).coerceAtLeast(0.01)
            transitionKind = step.transition
            delay((step.transitionMs + step.holdMs).toLong())
            currentExprId = step.expressionId
            idx += if (a.playbackMode == "pingPong" && a.steps.size > 1) {
                if (idx + dir >= a.steps.size || idx + dir < 0) { dir = -dir; dir } else dir
            } else 1
            if (a.playbackMode == "loop") idx %= a.steps.size.coerceAtLeast(1)
        }
    }

    LaunchedEffect(Unit) {
        var last = System.nanoTime()
        while (true) {
            delay(16)
            val now = System.nanoTime()
            val dt = (now - last) / 1e9
            last = now
            timeSec += dt
            blinkClock += dt
            val a = resolveAnim(currentAnim)
            if (isBlinking) {
                blinkProgress += dt * 1000 / a.blinkDurMs.coerceAtLeast(60)
                if (blinkProgress >= 1.0) {
                    isBlinking = false; blinkAmount = 1.0; blinkProgress = 0.0
                    blinkClock = 0.0
                } else {
                    val p = blinkProgress
                    blinkAmount = if (p < 0.5) 1 - p / 0.5 else (p - 0.5) / 0.5
                }
            } else if (a.blinkEnabled) {
                val window = (a.blinkMinMs + ((a.blinkMaxMs - a.blinkMinMs) * 0.7)).toDouble()
                if (blinkClock * 1000 > a.blinkInitialMs + window) {
                    isBlinking = true; blinkProgress = 0.0
                }
            }
        }
    }

    val density = LocalDensity.current
    val px = with(density) { size.toPx() }
    val viewScale = px / 300f

    val renderer = remember { NebyRenderer() }

    Box(
        modifier = modifier
            .size(size)
            .clip(CircleShape)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                enabled = interactive
            ) {
                val reactions = listOf("wink", "love", "kiss", "celebrate", "dance", "scanning", "agree", "disagree", "dizzy", "proud")
                triggerReaction(reactions.random())
            }
    ) {
        Canvas(modifier = Modifier.matchParentSize()) {
            val fromExpr = EXPR_BY_ID[currentExprId] ?: EXPR_BY_ID.values.first()
            val toExpr = EXPR_BY_ID[targetExprId] ?: EXPR_BY_ID.values.first()
            val rawT = ((timeSec - transitionStartT) / transitionDurS).coerceIn(0.0, 1.0)
            val eased = when (transitionKind) {
                "smooth" -> rawT * rawT * (3 - 2 * rawT)
                "snappy" -> 1 - (1 - rawT).pow(3.0)
                else -> 1 - exp(-6 * rawT) * cos(8 * rawT)
            }
            val blended = lerpExpression(fromExpr, toExpr, eased)
            val (ambientExpr, eyeOff) = applyAmbient(blended, timeSec, 1.0)
            val pose = poseFromExpression(ambientExpr)
            val frame = renderer.render(pose, blinkAmount, timeSec, eyeOff)

            drawIntoCanvas { c ->
                val nc = c.nativeCanvas
                nc.save()
                nc.translate(this.size.width / 2f, this.size.height / 2f)
                nc.scale(viewScale, viewScale)
                nc.translate(frame.bodyOffsetX.toFloat(), frame.bodyOffsetY.toFloat())

                val bodyColorHex = ambientExpr.bodyColor ?: "#cce2ff"
                val bodyPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                    color = try { Color.parseColor(bodyColorHex) } catch (_: Exception) { Color.parseColor("#cce2ff") }
                    style = Paint.Style.FILL
                }
                val eyePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                    color = Color.parseColor("#0a1c4d"); style = Paint.Style.FILL
                }
                val decalPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }

                nc.drawPath(frame.headPath, bodyPaint)
                for ((path, col) in frame.decals) {
                    decalPaint.color = col
                    nc.drawPath(path, decalPaint)
                }
                if (frame.leftVisible) nc.drawPath(frame.leftEyePath, eyePaint)
                if (frame.rightVisible) nc.drawPath(frame.rightEyePath, eyePaint)

                frame.effectDraw?.invoke(nc, timeSec)
                nc.restore()
            }
        }
    }
}

@Composable
fun NebyAvatarMini(
    animation: String = "idle",
    modifier: Modifier = Modifier,
    size: Dp = 36.dp,
    interactive: Boolean = false
) = NebyAvatar(animation = animation, modifier = modifier, size = size, interactive = interactive, hero = false)

@Composable
fun NebyAvatarHero(
    animation: String = "idle",
    modifier: Modifier = Modifier,
    size: Dp = 96.dp,
    interactive: Boolean = true
) = NebyAvatar(animation = animation, modifier = modifier, size = size, interactive = interactive, hero = true)
