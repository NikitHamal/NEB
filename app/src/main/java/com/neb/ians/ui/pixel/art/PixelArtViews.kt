package com.neb.ians.ui.pixel.art

import android.graphics.Bitmap
import android.util.LruCache
import androidx.compose.foundation.Canvas
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
import com.neb.ians.ui.components.stableSeed
import com.neb.ians.ui.pixel.PixelCanvas
import com.neb.ians.ui.theme.subjectFamily
import kotlin.math.roundToInt

/** Rendered pictures, shared across the app: a few dozen 128 x 64 bitmaps is well under a megabyte. */
private val pictures = LruCache<String, ImageBitmap>(64)

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
