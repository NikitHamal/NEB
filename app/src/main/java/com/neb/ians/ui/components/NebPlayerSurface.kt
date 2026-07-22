package com.neb.ians.ui.components

import android.view.LayoutInflater
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.Player
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView
import com.neb.ians.R

/**
 * The one and only video surface the app binds players to.
 *
 * Deliberately TextureView-backed (see res/layout/neb_player_view.xml): the
 * default SurfaceView races the decoder's first frame when it attaches after
 * playback has started, which manifested as "audio plays, stage stays black
 * until fullscreen". TextureView renders inside the regular view hierarchy so
 * the first frame always lands — and it survives Compose clipping, rounded
 * corners and animated resizes without punch-through artifacts.
 *
 * Controller chrome is never taken from the view itself; every screen draws
 * its own Compose controls on top.
 */
@Composable
fun NebPlayerView(
    player: Player?,
    modifier: Modifier = Modifier,
    resizeMode: Int = AspectRatioFrameLayout.RESIZE_MODE_FIT
) {
    AndroidView(
        factory = { ctx ->
            (LayoutInflater.from(ctx).inflate(R.layout.neb_player_view, null) as PlayerView).apply {
                setShutterBackgroundColor(android.graphics.Color.TRANSPARENT)
                this.resizeMode = resizeMode
                this.player = player
                (videoSurfaceView as? android.view.TextureView)?.let { tv ->
                    if (tv.isAvailable && player != null) {
                        player.setVideoTextureView(tv)
                    }
                }
            }
        },
        update = { pv ->
            if (pv.resizeMode != resizeMode) pv.resizeMode = resizeMode
            if (pv.player !== player) pv.player = player
            if (player != null) {
                (pv.videoSurfaceView as? android.view.TextureView)?.let { tv ->
                    if (tv.isAvailable) {
                        player.setVideoTextureView(tv)
                    }
                }
            }
        },
        modifier = modifier
    )
}
