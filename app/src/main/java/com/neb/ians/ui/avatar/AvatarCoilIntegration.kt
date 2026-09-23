package com.neb.ians.ui.avatar

import android.graphics.drawable.BitmapDrawable
import coil.ImageLoader
import coil.decode.DataSource
import coil.fetch.DrawableResult
import coil.fetch.FetchResult
import coil.fetch.Fetcher
import coil.request.Options
import com.neb.ians.ui.avatar.blobatar.blobatarBitmap

class AvatarFetcher(
    private val spec: AvatarSpec,
    private val options: Options
) : Fetcher {

    override suspend fun fetch(): FetchResult {
        val targetPx = when (val w = options.size.width) {
            is coil.size.Dimension.Pixels -> w.px.coerceIn(48, 384)
            else -> 128
        }
        val bmp = blobatarBitmap(spec.seed, spec.opts, targetPx)
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
