package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeOff
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.FullscreenExit
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.media3.common.Player
import androidx.media3.common.VideoSize
import kotlinx.coroutines.delay
import kotlin.math.abs

/**
 * Full-screen player dialog with the SAME control set as the resource
 * viewer's fullscreen player, but working against any media3 [Player] —
 * forum/comment players own plain ExoPlayers instead of MediaPlayerViewModel.
 *
 * Controls: tap toggles chrome, double-tap ±10s with side badges, vertical
 * drags = brightness (left) / volume (right), horizontal drag anywhere seeks,
 * top bar with close + title, bottom bar with mute / times / seek slider /
 * playback-speed cycler / exit-fullscreen, auto-hide after 4 s of playback.
 * The video surface is the shared TextureView-backed [NebPlayerView].
 */
@Composable
fun FullscreenVideoDialog(
    player: Player,
    title: String,
    onDismiss: () -> Unit,
    accentColor: Color = MaterialTheme.colorScheme.primary
) {
    var isPlaying by remember { mutableStateOf(player.isPlaying) }
    var isBuffering by remember { mutableStateOf(false) }
    var positionMs by remember { mutableLongStateOf(player.currentPosition.coerceAtLeast(0L)) }
    var durationMs by remember { mutableLongStateOf(player.duration.coerceAtLeast(0L)) }
    var videoAspectRatio by remember { mutableFloatStateOf(16f / 9f) }
    var controlsVisible by remember { mutableStateOf(true) }
    var dragging by remember { mutableStateOf(false) }
    var dragPositionMs by remember { mutableLongStateOf(0L) }
    var seekBadge by remember { mutableStateOf<Int?>(null) }
    var seekBadgeVisible by remember { mutableStateOf(false) }
    var screenWidth by remember { mutableFloatStateOf(1f) }
    var isMuted by remember { mutableStateOf(player.volume <= 0.001f) }
    var speedIndex by remember { mutableIntStateOf(2) } // index into SPEEDS, 1.0x default
    val activity = LocalContext.current as? android.app.Activity

    DisposableEffect(player) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }

            override fun onPlaybackStateChanged(playbackState: Int) {
                isBuffering = playbackState == Player.STATE_BUFFERING
                durationMs = player.duration.coerceAtLeast(0L)
            }

            override fun onVideoSizeChanged(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    videoAspectRatio =
                        (videoSize.width.toFloat() / videoSize.height.toFloat()) * videoSize.pixelWidthHeightRatio
                }
            }
        }
        player.addListener(listener)
        onDispose { player.removeListener(listener) }
    }

    LaunchedEffect(player, isPlaying) {
        while (true) {
            if (!dragging) positionMs = player.currentPosition.coerceAtLeast(0L)
            durationMs = player.duration.coerceAtLeast(0L)
            delay(250L)
        }
    }

    LaunchedEffect(controlsVisible, isPlaying) {
        if (controlsVisible && isPlaying) {
            delay(4000L)
            controlsVisible = false
        }
    }
    LaunchedEffect(seekBadgeVisible) {
        if (seekBadgeVisible) {
            delay(700L)
            seekBadgeVisible = false
        }
    }

    val safeDuration = if (durationMs > 0) durationMs else 1L
    val shownPosition = if (dragging) dragPositionMs else positionMs
    val remainingMs = (safeDuration - shownPosition).coerceAtLeast(0L)

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black)
                .onSizeChanged { screenWidth = it.width.toFloat() }
                .pointerInput(Unit) {
                    detectTapGestures(
                        onTap = {
                            controlsVisible = !controlsVisible
                            if (!controlsVisible && !isPlaying) controlsVisible = true
                        },
                        onDoubleTap = { offset ->
                            val delta = if (offset.x < screenWidth / 2f) -10_000L else 10_000L
                            val target = (player.currentPosition + delta)
                                .coerceIn(0L, player.duration.coerceAtLeast(0L))
                            player.seekTo(target)
                            seekBadge = if (delta < 0) -10 else 10
                            seekBadgeVisible = true
                            controlsVisible = true
                        }
                    )
                }
                .pointerInput(Unit) {
                    detectDragGestures(
                        onDragStart = { offset ->
                            dragging = true
                            dragPositionMs = player.currentPosition.coerceAtLeast(0L)
                        },
                        onDrag = { change, dragAmount ->
                            change.consume()
                            when {
                                // Vertical drag on the left/right edge = brightness / volume
                                abs(dragAmount.y) > abs(dragAmount.x) && screenWidth > 0f -> {
                                    val totalH = size.height.toFloat().coerceAtLeast(1f)
                                    if (change.position.x < screenWidth * 0.25f) {
                                        val lp = activity?.window?.attributes ?: return@detectDragGestures
                                        val cur = if (lp.screenBrightness < 0f) 0.5f else lp.screenBrightness
                                        lp.screenBrightness = (cur - dragAmount.y / totalH).coerceIn(0.05f, 1f)
                                        activity?.window?.attributes = lp
                                    } else if (change.position.x > screenWidth * 0.75f) {
                                        val newVol = (player.volume - dragAmount.y / totalH).coerceIn(0f, 1f)
                                        player.volume = newVol
                                        isMuted = newVol <= 0.001f
                                    }
                                }
                                else -> {
                                    val d = player.duration.coerceAtLeast(0L)
                                    if (d > 0 && screenWidth > 0f) {
                                        val seekPct = dragAmount.x / screenWidth
                                        dragPositionMs =
                                            (dragPositionMs + (seekPct * d).toLong()).coerceIn(0L, d)
                                    }
                                }
                            }
                        },
                        onDragEnd = {
                            if (dragging) player.seekTo(dragPositionMs)
                            dragging = false
                        },
                        onDragCancel = { dragging = false }
                    )
                },
            contentAlignment = Alignment.Center
        ) {
            NebPlayerView(
                player = player,
                modifier = Modifier
                    .fillMaxWidth()
                    .align(Alignment.Center)
            )

            if (isBuffering) {
                CircularProgressIndicator(
                    color = Color.White,
                    strokeWidth = 2.5.dp,
                    trackColor = Color.White.copy(alpha = 0.2f),
                    modifier = Modifier.size(36.dp)
                )
            }

            AnimatedVisibility(
                visible = seekBadgeVisible,
                enter = fadeIn(tween(120)),
                exit = fadeOut(tween(350)),
                modifier = Modifier.align(
                    if ((seekBadge ?: 0) < 0) Alignment.CenterStart else Alignment.CenterEnd
                )
            ) {
                Box(
                    modifier = Modifier
                        .padding(horizontal = 24.dp)
                        .background(Color.Black.copy(alpha = 0.55f), RoundedCornerShape(8.dp))
                        .padding(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Text(
                        text = if ((seekBadge ?: 0) < 0) "−10s" else "+10s",
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp
                    )
                }
            }

            AnimatedVisibility(
                visible = controlsVisible,
                enter = fadeIn(tween(200)),
                exit = fadeOut(tween(300)),
                modifier = Modifier.fillMaxSize()
            ) {
                Box(modifier = Modifier.fillMaxSize()) {
                    // Chrome gradients
                    Box(
                        Modifier
                            .fillMaxWidth()
                            .height(140.dp)
                            .align(Alignment.TopCenter)
                            .background(
                                Brush.verticalGradient(
                                    listOf(Color.Black.copy(alpha = 0.75f), Color.Transparent)
                                )
                            )
                    )
                    Box(
                        Modifier
                            .fillMaxWidth()
                            .height(180.dp)
                            .align(Alignment.BottomCenter)
                            .background(
                                Brush.verticalGradient(
                                    listOf(Color.Transparent, Color.Black.copy(alpha = 0.85f))
                                )
                            )
                    )

                    // Top bar: close + title
                    Row(
                        modifier = Modifier
                            .align(Alignment.TopStart)
                            .statusBarsPadding()
                            .padding(horizontal = 4.dp, vertical = 4.dp)
                            .fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(onClick = onDismiss) {
                            Icon(
                                imageVector = Icons.Filled.Close,
                                contentDescription = "Close",
                                tint = Color.White
                            )
                        }
                        Text(
                            text = title.ifBlank { "Video" },
                            color = Color.White,
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }

                    // Center play/pause
                    Surface(
                        onClick = { if (isPlaying) player.pause() else player.play() },
                        shape = CircleShape,
                        color = Color.Black.copy(alpha = 0.45f),
                        modifier = Modifier
                            .align(Alignment.Center)
                            .size(56.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = if (isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                                contentDescription = if (isPlaying) "Pause" else "Play",
                                tint = Color.White,
                                modifier = Modifier.size(32.dp)
                            )
                        }
                    }

                    // Bottom control bar
                    Column(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .navigationBarsPadding()
                            .fillMaxWidth()
                            .padding(horizontal = 6.dp, vertical = 6.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(2.dp)
                        ) {
                            IconButton(
                                onClick = {
                                    val newMuted = !isMuted
                                    player.volume = if (newMuted) 0f else 1f
                                    isMuted = newMuted
                                },
                                modifier = Modifier.size(34.dp)
                            ) {
                                Icon(
                                    imageVector = if (isMuted) Icons.AutoMirrored.Filled.VolumeOff
                                    else Icons.AutoMirrored.Filled.VolumeUp,
                                    contentDescription = if (isMuted) "Unmute" else "Mute",
                                    tint = Color.White,
                                    modifier = Modifier.size(18.dp)
                                )
                            }

                            Text(
                                text = formatFullscreenTime(shownPosition),
                                color = Color.White,
                                fontSize = 11.sp,
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Medium
                            )

                            Slider(
                                value = (shownPosition.toFloat() / safeDuration.toFloat()).coerceIn(0f, 1f),
                                onValueChange = { fraction ->
                                    dragging = true
                                    dragPositionMs = (fraction * safeDuration).toLong()
                                },
                                onValueChangeFinished = {
                                    player.seekTo(dragPositionMs)
                                    positionMs = dragPositionMs
                                    dragging = false
                                },
                                modifier = Modifier
                                    .weight(1f)
                                    .padding(horizontal = 4.dp),
                                colors = SliderDefaults.colors(
                                    thumbColor = accentColor,
                                    activeTrackColor = accentColor,
                                    inactiveTrackColor = Color.White.copy(alpha = 0.3f)
                                )
                            )

                            Text(
                                text = "-${formatFullscreenTime(remainingMs)}",
                                color = Color.White.copy(alpha = 0.65f),
                                fontSize = 11.sp,
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Medium
                            )

                            // Playback-speed cycler
                            Surface(
                                onClick = {
                                    speedIndex = (speedIndex + 1) % FS_SPEEDS.size
                                    player.setPlaybackSpeed(FS_SPEEDS[speedIndex])
                                },
                                shape = RoundedCornerShape(7.dp),
                                color = Color.White.copy(alpha = 0.14f)
                            ) {
                                Text(
                                    text = "${FS_SPEEDS[speedIndex]}x",
                                    color = Color.White,
                                    fontSize = 11.sp,
                                    fontFamily = FontFamily.Monospace,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 7.dp, vertical = 3.dp)
                                )
                            }

                            IconButton(
                                onClick = onDismiss,
                                modifier = Modifier.size(34.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Filled.FullscreenExit,
                                    contentDescription = "Exit fullscreen",
                                    tint = Color.White,
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

private val FS_SPEEDS = floatArrayOf(0.5f, 0.75f, 1f, 1.25f, 1.5f, 2f)

private fun formatFullscreenTime(ms: Long): String {
    val totalSec = (ms / 1000).coerceAtLeast(0)
    val h = totalSec / 3600
    val m = (totalSec % 3600) / 60
    val s = totalSec % 60
    return if (h > 0) "%d:%02d:%02d".format(h, m, s) else "%d:%02d".format(m, s)
}
