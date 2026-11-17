package com.neb.ians.ui.screens.notes

import android.graphics.BitmapFactory
import android.util.LruCache
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * M3X art library v7 note covers (concepts/art-v7, kind `note`, android = true). Flat WebP pictures,
 * one set for Light and one for Dark, shipped in `assets/note_covers/`. Cover indexes continue after the
 * 40 drawn banners: 41 to 112. The index is stored in `NoteEntity.cover`, so it never changes meaning.
 */
object NoteArtCovers {
    const val first = 41
    const val count = 72
    fun has(cover: Int): Boolean = cover >= first && cover < first + count
    fun asset(cover: Int, dark: Boolean): String =
        "note_covers/" + (if (dark) "dark" else "light") + "/nc_" + (cover - first + 1).toString().padStart(3, '0') + ".webp"
}

private val artCache = object : LruCache<String, ImageBitmap>(24 * 1024 * 1024) {
    override fun sizeOf(key: String, value: ImageBitmap): Int = value.width * value.height * 4
}

/** Picture cover. `small` halves the decode for list cards and the picker. */
@Composable
fun NoteArtCover(cover: Int, modifier: Modifier = Modifier, small: Boolean = false) {
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val context = LocalContext.current
    val path = NoteArtCovers.asset(cover, dark)
    val key = if (small) "$path#s" else path
    val bmp by produceState<ImageBitmap?>(artCache.get(key), key) {
        if (value == null) {
            value = withContext(Dispatchers.IO) {
                runCatching {
                    val opts = BitmapFactory.Options().apply { inSampleSize = if (small) 2 else 1 }
                    context.assets.open(path).use { BitmapFactory.decodeStream(it, null, opts) }
                        ?.asImageBitmap()?.also { artCache.put(key, it) }
                }.getOrNull()
            }
        }
    }
    Box(modifier.clipToBounds().background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
        bmp?.let { Image(it, null, Modifier.matchParentSize(), contentScale = ContentScale.Crop) }
    }
}
