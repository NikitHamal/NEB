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

/**
 * Rendered pictures, shared across the app. A banner is 32 KB and there are 144 per theme; a
 * miss redraws one on the main thread as its card scrolls in, so the cache holds as many as a
 * fortieth of the heap allows: about 100 on a small heap, a whole theme's on most phones.
 */
private val pictures = object : LruCache<String, ImageBitmap>((Runtime.getRuntime().maxMemory() / 40).toInt().coerceIn(2 shl 20, 10 shl 20)) {
    override fun sizeOf(key: String, value: ImageBitmap) = value.width * value.height * 4
}

private fun picture(key: String, render: () -> PixelCanvas): ImageBitmap = pictures.get(key) ?: run {
    val cv = render()
    val bmp = Bitmap.createBitmap(cv.width, cv.height, Bitmap.Config.ARGB_8888)
    bmp.setPixels(cv.pixels, 0, cv.width, 0, 0, cv.width, cv.height)
    bmp.asImageBitmap().also { pictures.put(key, it) }
}

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

/** A resource's banner: its subject's prop in one of four Nepali settings, by night in dark mode. */
@Composable
fun PixelBannerArt(seed: String, subject: String, modifier: Modifier = Modifier) {
    val night = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val family = remember(subject) { subjectFamily(subject).name }
    val variant = remember(seed) { PixelBanners.variantFor(stableSeed(seed)) }
    val image = remember(family, variant, night) { picture("b|$family|$variant|$night") { PixelBanners.render(family, variant, night) } }
    PixelPicture(image, modifier)
}

/** A profile cover: the role's panorama at dawn, dusk or night. */
@Composable
fun PixelCoverArt(role: String, seedKey: String, modifier: Modifier = Modifier) {
    val variant = remember(role, seedKey) { PixelCovers.variantFor(stableSeed("cover|$seedKey|$role")) }
    val image = remember(role, variant) { picture("c|$role|$variant") { PixelCovers.render(role, variant) } }
    PixelPicture(image, modifier)
}

/**
 * An onboarding scene ([PixelOnboarding]) with a live pixel Neby standing in it. The picture is
 * re-rendered only when the answer changes; Neby animates on top and reacts with the state the
 * scene asks for (a hop when a path is picked, a celebration when the birthday is set).
 */
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
    val scene = remember(kind, a, b, flag, handle) { PixelOnboarding.render(kind, a, b, flag, handle) }
    val image = remember(scene) {
        val cv = scene.canvas
        Bitmap.createBitmap(cv.width, cv.height, Bitmap.Config.ARGB_8888).apply { setPixels(cv.pixels, 0, cv.width, 0, 0, cv.width, cv.height) }.asImageBitmap()
    }
    androidx.compose.foundation.layout.BoxWithConstraints(
        modifier.fillMaxWidth().height(height).clip(androidx.compose.foundation.shape.RoundedCornerShape(20.dp))
    ) {
        val density = androidx.compose.ui.platform.LocalDensity.current
        val w = with(density) { maxWidth.toPx() }; val h = with(density) { maxHeight.toPx() }
        val scale = maxOf(w / image.width, h / image.height)
        val ox = (w - image.width * scale) / 2f; val oy = (h - image.height * scale) / 2f
        PixelPicture(image, Modifier.matchParentSize())
        val mark = scene.neby
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
