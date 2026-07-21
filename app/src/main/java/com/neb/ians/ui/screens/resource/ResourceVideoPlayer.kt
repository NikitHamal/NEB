package com.neb.ians.ui.screens.resource

import android.view.SurfaceView
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.draggable
import androidx.compose.foundation.gestures.rememberDraggableState
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Forward10
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Replay10
import androidx.compose.material.icons.filled.VolumeOff
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material.icons.outlined.AudioFile
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.screens.reader.MediaPlayerViewModel
import kotlinx.coroutines.delay

@Composable
fun EmbeddedMediaPlayer(
    resourceId: String,
    fileUrl: String,
    isVideo: Boolean,
    subjectColor: Color,
    title: String,
    onFullscreenClick: () -> Unit,
    onMinimize: () -> Unit = {},
    modifier: Modifier = Modifier,
    fullWidth: Boolean = false,
    viewModel: MediaPlayerViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    LaunchedEffect(resourceId) { viewModel.setResource(resourceId) }
    val player = viewModel.getPlayer()

    val shape = if (fullWidth) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)
    Surface(
        modifier = modifier.fillMaxWidth(),
        color = if (fullWidth) Color.Black else MaterialTheme.colorScheme.surfaceContainerLowest,
        shape = shape,
        border = if (fullWidth) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            if (uiState.isLoading) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(16f / 9f)
                        .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = subjectColor)
                }
            } else if (uiState.hasError) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(16f / 9f)
                        .background(MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.2f)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = uiState.errorMessage ?: "Failed to load media",
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            } else {
                if (isVideo) {
                    EmbeddedVideoStage(
                        player = player,
                        subjectColor = subjectColor,
                        isPlaying = uiState.isPlaying,
                        isBuffering = uiState.isBuffering,
                        isMuted = uiState.isMuted,
                        currentTimeMs = uiState.currentTimeMs,
                        durationMs = uiState.durationMs,
                        bufferedPercent = uiState.bufferedPercent,
                        onTogglePlay = { viewModel.togglePlay() },
                        onSeekBy = { viewModel.seekBy(it) },
                        onSeekRatio = { viewModel.seekToRatio(it) },
                        onToggleMute = { viewModel.toggleMute() },
                        onFullscreenClick = onFullscreenClick,
                        onMinimize = onMinimize
                    )
                } else {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(120.dp)
                            .background(subjectColor.copy(alpha = 0.08f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(
                                imageVector = Icons.Outlined.AudioFile,
                                contentDescription = null,
                                tint = subjectColor,
                                modifier = Modifier.size(48.dp)
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = title,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }

                    val trackColor = if (fullWidth) Color.White.copy(alpha = 0.2f) else MaterialTheme.colorScheme.surfaceContainerHigh
                    EmbeddedProgressBar(
                        currentMs = uiState.currentTimeMs,
                        durationMs = uiState.durationMs,
                        bufferedPercent = uiState.bufferedPercent,
                        subjectColor = subjectColor,
                        onSeek = { ratio -> viewModel.seekToRatio(ratio) },
                        trackColor = trackColor
                    )

                    val iconTint = if (fullWidth) Color.White else MaterialTheme.colorScheme.onSurface
                    val timeColor = if (fullWidth) Color.White.copy(alpha = 0.85f) else MaterialTheme.colorScheme.onSurfaceVariant

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(onClick = viewModel::togglePlay) {
                            Icon(
                                imageVector = if (uiState.isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                                contentDescription = if (uiState.isPlaying) "Pause" else "Play",
                                tint = iconTint
                            )
                        }

                        IconButton(onClick = { viewModel.seekBy(-10000L) }) {
                            Icon(
                                imageVector = Icons.Filled.Replay10,
                                contentDescription = "Rewind 10s",
                                tint = iconTint
                            )
                        }

                        IconButton(onClick = { viewModel.seekBy(10000L) }) {
                            Icon(
                                imageVector = Icons.Filled.Forward10,
                                contentDescription = "Forward 10s",
                                tint = iconTint
                            )
                        }

                        Spacer(modifier = Modifier.width(6.dp))

                        Text(
                            text = "${fmtTime(uiState.currentTimeMs)} / ${fmtTime(uiState.durationMs)}",
                            style = MaterialTheme.typography.bodyMedium,
                            fontFamily = FontFamily.Monospace,
                            color = timeColor
                        )

                        Spacer(modifier = Modifier.weight(1f))

                        IconButton(onClick = onFullscreenClick) {
                            Icon(
                                imageVector = Icons.Filled.Fullscreen,
                                contentDescription = "Fullscreen",
                                tint = iconTint
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun EmbeddedVideoStage(
    player: androidx.media3.common.Player?,
    subjectColor: Color,
    isPlaying: Boolean,
    isBuffering: Boolean,
    isMuted: Boolean,
    currentTimeMs: Long,
    durationMs: Long,
    bufferedPercent: Int,
    onTogglePlay: () -> Unit,
    onSeekBy: (Long) -> Unit,
    onSeekRatio: (Float) -> Unit,
    onToggleMute: () -> Unit,
    onFullscreenClick: () -> Unit,
    onMinimize: () -> Unit
) {
    var showControls by remember { mutableStateOf(true) }
    var seekBadge by remember { mutableStateOf<Int?>(null) }
    var seekBadgeVisible by remember { mutableStateOf(false) }
    var minimizeDragY by remember { mutableFloatStateOf(0f) }
    val minimizeThreshold = with(LocalDensity.current) { 48.dp.toPx() }
    val minimizeDragState = rememberDraggableState { delta -> minimizeDragY += delta }

    // Real stream aspect (16:9 until the decoder reports size) — the stage
    // frame stays 16:9 and the surface letterboxes inside it.
    var videoAspectRatio by remember { mutableFloatStateOf(16f / 9f) }
    // Handle on the stage surface: the ViewModel's player is shared with the
    // fullscreen screen and mini player, so the output surface must be
    // re-attached on resume and released on dispose — otherwise the player
    // keeps a dead surface and plays to a black view (progress still moves).
    var stageSurface by remember { mutableStateOf<SurfaceView?>(null) }

    DisposableEffect(player) {
        if (player == null) return@DisposableEffect onDispose {}
        val listener = object : androidx.media3.common.Player.Listener {
            override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    videoAspectRatio =
                        (videoSize.width.toFloat() / videoSize.height.toFloat()) * videoSize.pixelWidthHeightRatio
                }
            }
        }
        player.addListener(listener)
        onDispose { player.removeListener(listener) }
    }

    val surfaceLifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(surfaceLifecycleOwner, player, stageSurface) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                stageSurface?.let { sv -> player?.setVideoSurfaceView(sv) }
            }
        }
        surfaceLifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            surfaceLifecycleOwner.lifecycle.removeObserver(observer)
            stageSurface?.let { sv -> player?.clearVideoSurfaceView(sv) }
        }
    }

    LaunchedEffect(showControls, isPlaying) {
        if (showControls && isPlaying) {
            delay(3000L)
            showControls = false
        }
    }

    LaunchedEffect(isPlaying) {
        if (!isPlaying) showControls = true
    }

    LaunchedEffect(seekBadgeVisible) {
        if (seekBadgeVisible) {
            delay(700L)
            seekBadgeVisible = false
        }
    }

    val iconTint = Color.White
    val timeColor = Color.White.copy(alpha = 0.9f)
    val trackColor = Color.White.copy(alpha = 0.25f)
    val progress by remember(currentTimeMs, durationMs) {
        derivedStateOf {
            if (durationMs > 0) (currentTimeMs.toFloat() / durationMs).coerceIn(0f, 1f) else 0f
        }
    }
    val remainingMs = (durationMs - currentTimeMs).coerceAtLeast(0L)

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(16f / 9f)
            .background(Color.Black)
            .pointerInput(Unit) {
                detectTapGestures(
                    onTap = { showControls = !showControls },
                    onDoubleTap = { offset ->
                        val isLeft = offset.x < size.width / 2f
                        val delta = if (isLeft) -10_000L else 10_000L
                        onSeekBy(delta)
                        seekBadge = if (isLeft) -10 else 10
                        seekBadgeVisible = true
                        showControls = true
                    }
                )
            }
            .draggable(
                state = minimizeDragState,
                orientation = Orientation.Vertical,
                onDragStarted = { minimizeDragY = 0f },
                onDragStopped = {
                    if (minimizeDragY > minimizeThreshold) onMinimize()
                    minimizeDragY = 0f
                }
            )
    ) {
        AndroidView(
            factory = { ctx ->
                SurfaceView(ctx).also { sv ->
                    stageSurface = sv
                    player?.setVideoSurfaceView(sv)
                }
            },
            update = { sv ->
                stageSurface = sv
                player?.setVideoSurfaceView(sv)
            },
            modifier = Modifier
                .align(Alignment.Center)
                .aspectRatio(videoAspectRatio.coerceIn(0.4f, 2.6f))
        )

        if (isBuffering) {
            CircularProgressIndicator(
                color = subjectColor,
                strokeWidth = 2.5.dp,
                trackColor = Color.White.copy(alpha = 0.2f),
                modifier = Modifier
                    .size(32.dp)
                    .align(Alignment.Center)
            )
        }

        AnimatedVisibility(
            visible = showControls,
            enter = fadeIn(tween(200)),
            exit = fadeOut(tween(300)),
            modifier = Modifier.fillMaxSize()
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.verticalGradient(
                            0f to Color.Black.copy(alpha = 0.55f),
                            0.38f to Color.Transparent,
                            1f to Color.Black.copy(alpha = 0.78f)
                        )
                    )
            ) {
                IconButton(
                    onClick = {
                        onTogglePlay()
                        showControls = true
                    },
                    modifier = Modifier
                        .align(Alignment.Center)
                        .size(52.dp)
                        .background(Color.Black.copy(alpha = 0.45f), CircleShape)
                ) {
                    Icon(
                        imageVector = if (isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                        contentDescription = if (isPlaying) "Pause" else "Play",
                        tint = iconTint,
                        modifier = Modifier.size(30.dp)
                    )
                }

                Row(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .fillMaxWidth()
                        .padding(horizontal = 6.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    IconButton(
                        onClick = { onToggleMute(); showControls = true },
                        modifier = Modifier.size(30.dp)
                    ) {
                        Icon(
                            imageVector = if (isMuted) Icons.Filled.VolumeOff else Icons.Filled.VolumeUp,
                            contentDescription = if (isMuted) "Unmute" else "Mute",
                            tint = iconTint,
                            modifier = Modifier.size(16.dp)
                        )
                    }

                    Text(
                        text = fmtTime(currentTimeMs),
                        color = timeColor,
                        fontSize = 10.sp,
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Medium
                    )

                    EmbeddedProgressBar(
                        currentMs = currentTimeMs,
                        durationMs = durationMs,
                        bufferedPercent = bufferedPercent,
                        subjectColor = subjectColor,
                        onSeek = { ratio ->
                            onSeekRatio(ratio)
                            showControls = true
                        },
                        trackColor = trackColor,
                        modifier = Modifier.weight(1f)
                    )

                    Text(
                        text = "-${fmtTime(remainingMs)}",
                        color = timeColor.copy(alpha = 0.65f),
                        fontSize = 10.sp,
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Medium
                    )

                    IconButton(
                        onClick = { onFullscreenClick() },
                        modifier = Modifier.size(30.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Filled.Fullscreen,
                            contentDescription = "Fullscreen",
                            tint = iconTint,
                            modifier = Modifier.size(16.dp)
                        )
                    }
                }
            }
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
                    .padding(horizontal = 16.dp)
                    .background(Color.Black.copy(alpha = 0.55f), RoundedCornerShape(8.dp))
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = if ((seekBadge ?: 0) < 0) "−10s" else "+10s",
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 13.sp
                )
            }
        }

        Box(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .height(2.dp)
                .background(Color.White.copy(alpha = 0.10f))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(progress)
                    .background(subjectColor)
            )
        }
    }
}

@Composable
private fun EmbeddedProgressBar(
    currentMs: Long,
    durationMs: Long,
    bufferedPercent: Int,
    subjectColor: Color,
    onSeek: (Float) -> Unit,
    trackColor: Color = MaterialTheme.colorScheme.surfaceContainerHigh,
    modifier: Modifier = Modifier
) {
    var barWidth by remember { mutableStateOf(0) }
    var isDragging by remember { mutableStateOf(false) }
    val progress by remember(currentMs, durationMs) {
        derivedStateOf {
            if (durationMs > 0) (currentMs.toFloat() / durationMs).coerceIn(0f, 1f) else 0f
        }
    }
    val thumbScale by animateFloatAsState(
        targetValue = if (isDragging) 1.5f else 1f,
        animationSpec = tween(150),
        label = "thumbScale"
    )

    Box(
        modifier = modifier
            .height(20.dp)
            .background(Color.Transparent)
            .pointerInput(barWidth) {
                detectTapGestures { offset ->
                    val w = barWidth.coerceAtLeast(1).toFloat()
                    onSeek((offset.x / w).coerceIn(0f, 1f))
                }
            }
            .pointerInput(barWidth) {
                detectDragGestures(
                    onDragStart = { offset ->
                        isDragging = true
                        val w = barWidth.coerceAtLeast(1).toFloat()
                        onSeek((offset.x / w).coerceIn(0f, 1f))
                    },
                    onDrag = { change, _ ->
                        change.consume()
                        val w = barWidth.coerceAtLeast(1).toFloat()
                        onSeek((change.position.x / w).coerceIn(0f, 1f))
                    },
                    onDragEnd = { isDragging = false },
                    onDragCancel = { isDragging = false }
                )
            }
            .onSizeChanged { barWidth = it.width },
        contentAlignment = Alignment.CenterStart
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(3.dp)
                .clip(RoundedCornerShape(2.dp))
                .background(trackColor)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth((bufferedPercent / 100f).coerceIn(0f, 1f))
                    .background(Color.White.copy(alpha = 0.30f))
            )
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(progress)
                    .background(subjectColor)
            )
        }
        val thumbSizeDp = 10.dp * thumbScale
        Box(
            modifier = Modifier
                .offset { IntOffset(x = ((progress * barWidth) - (thumbSizeDp.toPx() / 2)).toInt().coerceAtLeast(0), y = 0) }
                .size(thumbSizeDp)
                .clip(CircleShape)
                .background(subjectColor)
        )
    }
}

private fun fmtTime(ms: Long): String {
    if (ms <= 0) return "0:00"
    val totalSec = ms / 1000
    val h = totalSec / 3600
    val m = (totalSec % 3600) / 60
    val s = totalSec % 60
    return if (h > 0) "%d:%02d:%02d".format(h, m, s) else "%d:%02d".format(m, s)
}
