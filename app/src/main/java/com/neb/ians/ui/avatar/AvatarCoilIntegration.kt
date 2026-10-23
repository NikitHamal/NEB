package com.neb.ians.ui.avatar

import android.graphics.drawable.BitmapDrawable
import coil.ImageLoader
import coil.decode.DataSource
import coil.fetch.DrawableResult
import coil.fetch.FetchResult
import coil.fetch.Fetcher
import coil.request.Options
import com.neb.ians.ui.avatar.blobatar.blobatarBitmap

/** The pixel size an avatar is drawn at for a request (Coil's resolved width, within 48..384). */
private fun targetPx(options: Options): Int = when (val w = options.size.width) {
    is coil.size.Dimension.Pixels -> w.px.coerceIn(48, 384)
    else -> 128
}

class AvatarFetcher(
    private val spec: AvatarSpec,
    private val options: Options
) : Fetcher {

    override suspend fun fetch(): FetchResult {
        val bmp = blobatarBitmap(spec.seed, spec.opts, targetPx(options))
        val drawable = BitmapDrawable(options.context.resources, bmp)
        return DrawableResult(drawable, false, DataSource.MEMORY)
    }

    class Factory : Fetcher.Factory<AvatarSpec> {
        override fun create(data: AvatarSpec, options: Options, imageLoader: ImageLoader): Fetcher =
            AvatarFetcher(data, options)
    }
}

class AvatarMapper : coil.map.Mapper<String, AvatarSpec> {
    override fun map(data: String, options: Options): AvatarSpec? = parseAvatarUrl(data)
}

/**
 * Lets Coil's memory cache hold generated avatars. Without a key Coil never cached them, so an
 * avatar scrolling back into view was drawn again and faded in again. The size is in the key so a
 * small list avatar is never stretched for a large header.
 */
class AvatarKeyer : coil.key.Keyer<AvatarSpec> {
    override fun key(data: AvatarSpec, options: Options): String = "blobatar:${data.seed}|${data.opts}|${targetPx(options)}"
}
