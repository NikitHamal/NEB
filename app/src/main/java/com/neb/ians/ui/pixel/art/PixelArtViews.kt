package com.neb.ians.ui.pixel.art

import android.graphics.Bitmap
import android.util.LruCache
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.ui.draw.clip
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.FilterQuality
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.stableSeed
import com.neb.ians.ui.pixel.PixelCanvas
import com.neb.ians.ui.theme.subjectFamily
import kotlin.math.roundToInt

/** Draws a pixel picture to fill the box (cropping like ContentScale.Crop), every pixel square and crisp. */
@Composable
private fun PixelPicture(image: ImageBitmap, modifier: Modifier) {
    Canvas(modifier.clipToBounds()) {
        val scale = maxOf(size.width / image.width, size.height / image.height)
        val w = (image.width * scale).roundToInt(); val h = (image.height * scale).roundToInt()
        drawImage(
            image,
            dstOffset = IntOffset(((size.width - w) / 2f).roundToInt(), ((size.height - h) / 2f).roundToInt()),
            dstSize = IntSize(w, h),
            filterQuality = FilterQuality.None,
        )
    }
}

/**
 * An onboarding scene ([PixelOnboarding]) with a live pixel Neby standing in it. The picture is
 * re-rendered only when the answer changes; Neby animates on top and reacts with the state the
 * scene asks for (a hop when a path is picked, a celebration when the birthday is set).
 */
private object PixelOnboardingCache {
    private val lru = LruCache<String, Pair<ImageBitmap, PixelOnboarding.NebyMark>>(32)

    fun get(
        kind: PixelOnboarding.Kind,
        a: Int,
        b: Int,
        flag: Boolean,
        handle: PixelOnboarding.Handle,
        night: Boolean
    ): Pair<ImageBitmap, PixelOnboarding.NebyMark> {
        val key = "${kind.ordinal}|$a|$b|$flag|${handle.ordinal}|$night"
        synchronized(this) { lru.get(key) }?.let { return it }
        val scene = PixelOnboarding.render(kind, a, b, flag, handle, night)
        val cv = scene.canvas
        val bmp = Bitmap.createBitmap(cv.width, cv.height, Bitmap.Config.ARGB_8888)
            .apply { setPixels(cv.pixels, 0, cv.width, 0, 0, cv.width, cv.height) }
            .asImageBitmap()
        return (bmp to scene.neby).also { synchronized(this) { lru.put(key, it) } }
    }
}

@Composable
fun PixelOnboardingArt(
    kind: PixelOnboarding.Kind,
    modifier: Modifier = Modifier,
    a: Int = -1,
    b: Int = 0,
    flag: Boolean = false,
    handle: PixelOnboarding.Handle = PixelOnboarding.Handle.Idle,
    height: androidx.compose.ui.unit.Dp = 160.dp,
) {
    val night = com.neb.ians.ui.theme.LocalNebAuthPalette.current.isDark
    val (image, mark) = remember(kind, a, b, flag, handle, night) {
        PixelOnboardingCache.get(kind, a, b, flag, handle, night)
    }
    androidx.compose.foundation.layout.BoxWithConstraints(
        modifier.fillMaxWidth().height(height).clip(androidx.compose.foundation.shape.RoundedCornerShape(28.dp))
    ) {
        val density = androidx.compose.ui.platform.LocalDensity.current
        val w = with(density) { maxWidth.toPx() }; val h = with(density) { maxHeight.toPx() }
        val scale = maxOf(w / image.width, h / image.height)
        val ox = (w - image.width * scale) / 2f; val oy = (h - image.height * scale) / 2f
        PixelPicture(image, Modifier.matchParentSize())
        val sizePx = 48f * scale
        androidx.compose.runtime.key(mark.state) {
            com.neb.ians.ui.pixel.NebyPixel(
                state = mark.state,
                size = with(density) { sizePx.toDp() },
                modifier = Modifier.offset { IntOffset((ox + (mark.x - 24) * scale).roundToInt(), (oy + (mark.ground - 46) * scale).roundToInt()) },
            )
        }
    }
}
