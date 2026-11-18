package com.neb.ians.ui.components

import android.content.Context
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.neb.ians.ui.theme.subjectFamily
import org.json.JSONObject

/**
 * The M3X art library as vector pieces the site serves (tools/art/export_m3x_assets.js writes them, `img/m3x/`).
 *
 * Nothing is bundled in the APK except the 7 KB manifest `assets/m3x/covers.json`. Covers are the v7 `cover` pieces
 * (ids `cover-NNN`), resource thumbnails the v1 `thumb` pieces (6 per subject family). Each is a 2 to 60 KB SVG that
 * Coil fetches once, rasterises at the size it is drawn (sharp on any screen) and keeps on disk for a year.
 */
object M3xArt {
    const val THUMB_VARIANTS = 6

    class Cover(val id: String, val layout: String, val palette: String)

    @Volatile private var cached: List<Cover>? = null

    fun covers(context: Context): List<Cover> = cached ?: synchronized(this) {
        cached ?: runCatching {
            val text = context.applicationContext.assets.open("m3x/covers.json").bufferedReader().use { it.readText() }
            val rows = JSONObject(text).getJSONArray("covers")
            List(rows.length()) { i -> rows.getJSONArray(i).let { Cover(it.getString(0), it.getString(1), it.getString(2)) } }
        }.getOrDefault(emptyList()).also { cached = it }
    }

    /** FNV-1a over the UTF-8 bytes, unsigned 32 bit. Same as api/cover_art.py `default_cover`. */
    private fun fnv(text: String): Long {
        var h = 2166136261L
        for (b in text.toByteArray(Charsets.UTF_8)) h = ((h xor (b.toLong() and 0xFF)) * 16777619L) and 0xFFFFFFFFL
        return h
    }

    /** The cover a member who never chose one has: a stable pick from the username. */
    fun defaultCover(context: Context, username: String): String {
        val list = covers(context)
        return if (list.isEmpty()) "cover-001" else list[(fnv("cover|$username") % list.size).toInt()].id
    }

    private const val BASE = "https://nebians.consica.com.np/static/web/img/m3x/"

    fun coverUri(id: String, dark: Boolean) = "${BASE}cover/${if (dark) "dark" else "light"}/$id.svg"

    fun thumbUri(family: String, variant: Int, dark: Boolean) =
        "${BASE}thumb/${if (dark) "dark" else "light"}/${family.lowercase()}-$variant.svg"
}

@Composable
private fun isDarkSurface() = MaterialTheme.colorScheme.surface.luminance() < 0.5f

@Composable
private fun M3xImage(uri: String, modifier: Modifier) {
    val context = LocalContext.current
    val request = remember(uri) { ImageRequest.Builder(context).data(uri).crossfade(false).allowHardware(true).build() }
    // a tonal well shows until the vector arrives, and stays if the phone is offline
    Box(modifier.background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
        AsyncImage(model = request, contentDescription = null, modifier = Modifier.matchParentSize(), contentScale = ContentScale.Crop)
    }
}

/** A profile cover from the library. [coverId] blank or unknown falls back to the username's stable pick. */
@Composable
fun M3xCover(coverId: String?, username: String, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val dark = isDarkSurface()
    val id = remember(coverId, username) {
        val known = coverId?.takeIf { c -> c.isNotBlank() && M3xArt.covers(context).any { it.id == c } }
        known ?: M3xArt.defaultCover(context, username)
    }
    M3xImage(M3xArt.coverUri(id, dark), modifier)
}

/** A resource's thumbnail when it has no picture of its own: the v1 piece for its subject family. */
@Composable
fun M3xThumb(seed: String, subject: String, modifier: Modifier = Modifier) {
    val dark = isDarkSurface()
    val family = remember(subject) { subjectFamily(subject).name }
    val variant = remember(seed) { ((stableSeed(seed) ushr 3) and 0x7FFFFFFF) % M3xArt.THUMB_VARIANTS }
    Box(modifier) { M3xImage(M3xArt.thumbUri(family, variant, dark), Modifier.matchParentSize()) }
}

/** One cover tile in the picker, drawn at its own size. */
@Composable
fun M3xCoverTile(id: String, modifier: Modifier = Modifier) = M3xImage(M3xArt.coverUri(id, isDarkSurface()), modifier)
