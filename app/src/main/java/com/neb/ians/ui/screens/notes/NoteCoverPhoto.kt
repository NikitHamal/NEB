package com.neb.ians.ui.screens.notes

import android.graphics.BitmapFactory
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.matchParentSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

/** A gallery cover. Decoded off the main thread; `light` halves it for list cards. */
@Composable
fun NoteCoverPhoto(file: File, modifier: Modifier = Modifier, light: Boolean = false) {
    val bmp by produceState<ImageBitmap?>(null, file.path, light) {
        value = withContext(Dispatchers.IO) {
            runCatching {
                val opts = BitmapFactory.Options().apply { inSampleSize = if (light) 2 else 1 }
                BitmapFactory.decodeFile(file.path, opts)?.asImageBitmap()
            }.getOrNull()
        }
    }
    Box(modifier.clipToBounds().background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
        bmp?.let { Image(it, null, Modifier.matchParentSize(), contentScale = ContentScale.Crop) }
    }
}

/** Built-in banner or gallery picture, whichever the note uses. */
@Composable
fun NoteCover(cover: Int, photo: File?, modifier: Modifier = Modifier, animate: Boolean = true, light: Boolean = false) {
    if (cover < 0 && photo != null) NoteCoverPhoto(photo, modifier, light) else NoteCoverBanner(cover, modifier, animate)
}
