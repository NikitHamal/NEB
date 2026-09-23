package com.neb.ians.ui.avatar

import android.provider.Settings
import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.Dp
import androidx.compose.foundation.shape.CircleShape
import com.neb.ians.ui.avatar.blobatar.BlobatarOpts
import com.neb.ians.ui.avatar.blobatar.blobatarBitmap
import com.neb.ians.util.DevicePerformance

@Composable
fun BlobatarCanvas(
    seed: String,
    opts: BlobatarOpts,
    modifier: Modifier = Modifier,
    sizePx: Int = 256
) {
    val bitmap = remember(seed, opts, sizePx) {
        blobatarBitmap(seed, opts, sizePx.coerceIn(32, 512))
    }
    Image(
        bitmap = bitmap.asImageBitmap(),
        contentDescription = null,
        modifier = modifier
    )
}

@Composable
fun Modifier.blobatarAnim(anim: String?): Modifier {
    if (anim == null) return this
    val ctx = LocalContext.current
    if (DevicePerformance.isLowEndDevice(ctx)) return this
    val durationScale = remember {
        try { Settings.Global.getFloat(ctx.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) } catch (_: Exception) { 1f }
    }
    if (durationScale == 0f) return this
    return when (anim) {
        "bob" -> {
            val t = rememberInfiniteTransition(label = "bob")
            val dy = t.animateFloat(
                initialValue = 0f, targetValue = 0f,
                animationSpec = infiniteRepeatable(
                    animation = keyframes {
                        durationMillis = 3000
                        0f at 0 using FastOutSlowInEasing
                        -0.07f at 1500 using FastOutSlowInEasing
                        0f at 3000
                    }
                ), label = "bobY"
            )
            this.graphicsLayer { translationY = dy.value * size.height }
        }
        "wave" -> {
            val t = rememberInfiniteTransition(label = "wave")
            val rot = t.animateFloat(
                initialValue = 0f, targetValue = 0f,
                animationSpec = infiniteRepeatable(
                    animation = keyframes {
                        durationMillis = 4000
                        0f at 0 using FastOutSlowInEasing
                        5f at 1000 using FastOutSlowInEasing
                        0f at 2000 using FastOutSlowInEasing
                        -5f at 3000 using FastOutSlowInEasing
                        0f at 4000
                    }
                ), label = "waveRot"
            )
            this.graphicsLayer { rotationZ = rot.value; transformOrigin = androidx.compose.ui.graphics.TransformOrigin(0.5f, 0.5f) }
        }
        "spin" -> {
            val t = rememberInfiniteTransition(label = "spin")
            val rot = t.animateFloat(0f, 360f, infiniteRepeatable(tween(6000, easing = LinearEasing)), label = "spinRot")
            this.graphicsLayer { rotationZ = rot.value; transformOrigin = androidx.compose.ui.graphics.TransformOrigin(0.5f, 0.5f) }
        }
        "pulse" -> {
            val t = rememberInfiniteTransition(label = "pulse")
            val s = t.animateFloat(
                initialValue = 1f, targetValue = 1f,
                animationSpec = infiniteRepeatable(
                    animation = keyframes {
                        durationMillis = 3000
                        1f at 0 using FastOutSlowInEasing
                        1.06f at 1500 using FastOutSlowInEasing
                        1f at 3000
                    }
                ), label = "pulseS"
            )
            this.graphicsLayer { scaleX = s.value; scaleY = s.value; transformOrigin = androidx.compose.ui.graphics.TransformOrigin(0.5f, 0.5f) }
        }
        else -> this
    }
}

@Composable
fun BlobatarImage(
    seed: String,
    opts: BlobatarOpts,
    modifier: Modifier = Modifier,
    size: Dp,
    anim: String? = opts.anim
) {
    Box(modifier = modifier.size(size).clip(CircleShape).blobatarAnim(anim)) {
        BlobatarCanvas(seed = seed, opts = opts, modifier = Modifier.matchParentSize())
    }
}
