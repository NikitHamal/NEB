package com.neb.ians.ui.pixel

import android.graphics.Bitmap
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.withFrameMillis
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.FilterQuality
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.IntRect
import androidx.compose.ui.unit.IntSize
import com.neb.ians.ui.theme.nebAnimationsReduced
import kotlinx.coroutines.delay
import kotlin.math.ceil
import kotlin.math.roundToInt

/** Pixel art plays at a pixel-art frame rate: smooth enough, and a third of the work of 60 fps. */
private const val PIXEL_FRAME_MS = 1000L / 24

/**
 * The loops below sleep between frames instead of waking on every vsync (60 to 120 times a
 * second, mostly to find nothing to draw), and wake this much early so the next vsync shows it.
 */
private const val WAKE_EARLY_MS = 6L

/**
 * The auth hero: [PixelSkyScene], scaled up by a whole number so every pixel is the same size,
 * cropped to fill, and kept centred on the book. Renders into one small bitmap (about 330 KB);
 * frames stop by themselves when the screen is not drawing, and reduced motion shows a still.
 */
@Composable
fun PixelSkyHero(modifier: Modifier = Modifier, ground: Int = Px.rgb(0xFFFFFF)) {
    val scene = remember(ground) { PixelSkyScene(ground) }
    val bitmap = remember { Bitmap.createBitmap(PixelSkyScene.WIDTH, PixelSkyScene.HEIGHT, Bitmap.Config.ARGB_8888) }
    val image = remember(bitmap) { bitmap.asImageBitmap() }
    var tick by remember { mutableLongStateOf(-1L) }
    val still = nebAnimationsReduced()

    LaunchedEffect(scene, still) {
        fun draw(t: Long) {
            scene.render(t)
            bitmap.setPixels(scene.canvas.pixels, 0, PixelSkyScene.WIDTH, 0, 0, PixelSkyScene.WIDTH, PixelSkyScene.HEIGHT)
            tick = t
        }
        if (still) { draw(2000L); return@LaunchedEffect }
        val start = withFrameMillis { it }
        while (true) {
            withFrameMillis { now -> draw(now - start) }
            delay(PIXEL_FRAME_MS - WAKE_EARLY_MS)
        }
    }

    Canvas(modifier.graphicsLayer()) {
        if (tick < 0) return@Canvas
        val scale = ceil(maxOf(size.width / PixelSkyScene.WIDTH, size.height / PixelSkyScene.HEIGHT)).toInt().coerceAtLeast(1)
        val w = PixelSkyScene.WIDTH * scale
        val h = PixelSkyScene.HEIGHT * scale
        // keep the book at the same height in the frame however much is cropped
        val focusY = PixelSkyScene.BOOK_Y * scale - size.height * 0.56f
        val y = (-focusY).coerceIn(size.height - h, 0f)
        drawImage(
            image,
            dstOffset = IntOffset(((size.width - w) / 2f).roundToInt(), y.roundToInt()),
            dstSize = IntSize(w, h),
            filterQuality = FilterQuality.None
        )
    }
}

/**
 * Plays any [PixelSprite] crisp, at the largest whole-number scale that fits the view.
 * Loops unless the sprite says otherwise; a one-shot sprite stops on its last frame.
 */
@Composable
fun PixelSpriteView(sprite: PixelSprite, modifier: Modifier = Modifier, playing: Boolean = true, src: IntRect? = null) {
    val bitmap = remember(sprite) { Bitmap.createBitmap(sprite.width, sprite.height, Bitmap.Config.ARGB_8888) }
    val image = remember(bitmap) { bitmap.asImageBitmap() }
    var frame by remember(sprite) { mutableLongStateOf(-1L) }
    // a single-frame sprite (Neby's still pose) has nothing to play
    val still = nebAnimationsReduced() || !playing || sprite.frames.size < 2

    LaunchedEffect(sprite, still) {
        fun show(i: Int) {
            bitmap.setPixels(sprite.frames[i], 0, sprite.width, 0, 0, sprite.width, sprite.height)
            frame = i.toLong()
        }
        if (still) { show(if (sprite.loop) 0 else sprite.frames.size - 1); return@LaunchedEffect }
        val start = withFrameMillis { it }
        var shown = -1
        while (true) {
            val t = withFrameMillis { now ->
                val i = sprite.frameAt(now - start)
                if (i != shown) { show(i); shown = i }
                now - start
            }
            if (!sprite.loop && t >= sprite.durationMs) break
            delay((sprite.frameMs - t % sprite.frameMs - WAKE_EARLY_MS).coerceAtLeast(0L))
        }
    }

    // its own layer: a new frame redraws the sprite, not the card or list row around it
    Canvas(modifier.graphicsLayer()) {
        if (frame < 0) return@Canvas
        // [src] shows part of the sprite (an avatar's head-and-shoulders crop) scaled to the view
        val sw = src?.width ?: sprite.width; val sh = src?.height ?: sprite.height
        val fit = minOf(size.width / sw, size.height / sh)
        // whole-number scale keeps pixels even; tiny views (avatars) would shrink too much, so fill them
        val scale = fit.toInt().let { if (it < 1 || it < fit * 0.8f) fit else it.toFloat() }
        val w = (sw * scale).roundToInt(); val h = (sh * scale).roundToInt()
        drawImage(
            image,
            srcOffset = IntOffset(src?.left ?: 0, src?.top ?: 0),
            srcSize = IntSize(sw, sh),
            dstOffset = IntOffset(((size.width - w) / 2f).roundToInt(), ((size.height - h) / 2f).roundToInt()),
            dstSize = IntSize(w, h),
            filterQuality = FilterQuality.None
        )
    }
}
