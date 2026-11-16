package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/** Six bars, one per question. The bar of the question you are on fills as the page arrives; earlier bars stay full. */
@Composable
internal fun QuizProgress(step: Int, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    val track = c.surfaceContainerHigh
    val fill = c.primary
    Row(modifier, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        for (i in 1..6) {
            val a = remember { Animatable(if (i < step) 1f else 0f) }
            LaunchedEffect(step) { a.animateTo(if (i <= step) 1f else 0f, tween(500, easing = FastOutSlowInEasing)) }
            Box(
                Modifier.weight(1f).height(6.dp).clip(RoundedCornerShape(3.dp)).background(track)
                    .drawBehind { drawRect(fill, size = Size(size.width * a.value, size.height)) },
            )
        }
    }
}

@Composable
private fun Tick(on: Boolean, ink: androidx.compose.ui.graphics.Color, modifier: Modifier) {
    val p by animateFloatAsState(if (on) 1f else 0f, spring(0.5f, Spring.StiffnessMediumLow), label = "tick")
    Canvas(modifier.size(16.dp)) {
        if (p <= 0.01f) return@Canvas
        scale(p) {
            val path = Path().apply {
                moveTo(size.width * 0.16f, size.height * 0.54f); lineTo(size.width * 0.42f, size.height * 0.78f); lineTo(size.width * 0.86f, size.height * 0.24f)
            }
            drawPath(path, ink, style = Stroke(2.5.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round))
        }
    }
}

/** One answer card: rounded, turns solid and tighter when picked, a tick springs in, a small shake when the limit of three is hit. */
@Composable
internal fun QOption(title: String, sub: String?, on: Boolean, shake: Int, modifier: Modifier = Modifier, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val src = remember { MutableInteractionSource() }
    val pressed by src.collectIsPressedAsState()
    val r by animateDpAsState(if (on || pressed) 14.dp else 22.dp, spring(0.55f, Spring.StiffnessMediumLow), label = "qr")
    val bg by animateColorAsState(if (on) c.primary else c.surfaceContainerLow, tween(200), label = "qbg")
    val sc by animateFloatAsState(if (pressed) 0.97f else 1f, spring(0.6f, Spring.StiffnessMedium), label = "qsc")
    val sh = remember { Animatable(0f) }
    LaunchedEffect(shake) {
        if (shake > 0) { sh.animateTo(-6f, tween(60)); sh.animateTo(6f, tween(80)); sh.animateTo(0f, tween(60)) }
    }
    val ink = if (on) c.onPrimary else c.onSurface
    Surface(
        onClick = onClick, interactionSource = src, shape = RoundedCornerShape(r), color = bg, contentColor = ink,
        modifier = modifier.heightIn(min = 64.dp).graphicsLayer { scaleX = sc; scaleY = sc; translationX = sh.value.dp.toPx() },
    ) {
        Box(Modifier.fillMaxWidth()) {
            Column(
                Modifier.padding(start = 16.dp, end = 34.dp, top = 14.dp, bottom = 14.dp).align(Alignment.CenterStart),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                if (!sub.isNullOrEmpty()) Text(sub, fontSize = 12.sp, fontWeight = FontWeight.Medium, lineHeight = 15.sp, color = if (on) ink.copy(alpha = 0.8f) else c.onSurfaceVariant)
            }
            Tick(on, ink, Modifier.align(Alignment.CenterEnd).padding(end = 14.dp))
        }
    }
}

/** Answers in a grid with equal row heights. */
@Composable
internal fun QGrid(items: List<Triple<String, String, String?>>, cols: Int, picked: (String) -> Boolean, shakeKey: String, shakeN: Int, onPick: (String) -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        items.chunked(cols).forEach { row ->
            Row(Modifier.fillMaxWidth().height(IntrinsicSize.Min), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                row.forEach { (k, t, s) ->
                    QOption(t, s, picked(k), if (shakeKey == k) shakeN else 0, Modifier.weight(1f).fillMaxHeight()) { onPick(k) }
                }
                repeat(cols - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

/** Full width action; dim and inert until the question has an answer. */
@Composable
internal fun QButton(text: String, enabled: Boolean, filled: Boolean = true, modifier: Modifier = Modifier, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val src = remember { MutableInteractionSource() }
    val pressed by src.collectIsPressedAsState()
    val r by animateDpAsState(if (pressed) 16.dp else 28.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "qbr")
    Surface(
        onClick = onClick, enabled = enabled, interactionSource = src, shape = RoundedCornerShape(r),
        color = if (filled) c.primary else c.primaryContainer, contentColor = if (filled) c.onPrimary else c.onPrimaryContainer,
        modifier = modifier.fillMaxWidth().height(56.dp).graphicsLayer { alpha = if (enabled) 1f else 0.38f },
    ) {
        Box(contentAlignment = Alignment.Center) { Text(text, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.Center) }
    }
}

internal fun matchStageOf(d: PwData, s: PwSel): String =
    d.stages.firstOrNull { it.id == s.matchStage }?.id ?: d.stages.firstOrNull { it.id == s.stage }?.id ?: d.stages.firstOrNull()?.id.orEmpty()

internal fun pwProfile(d: PwData, vm: PathwaysViewModel, district: String): PwProfile = PwProfile(
    matchStageOf(d, vm.sel), vm.set("interests"), vm.set("strengths"), vm.set("priorities"), vm.num("budget"),
    vm.num("myears"), RISKS.getOrNull(vm.num("mrisk"))?.first ?: "mid", district, STREAMS.getOrNull(vm.num("mstream") - 1)?.first.orEmpty(),
)
