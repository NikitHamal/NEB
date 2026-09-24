package com.neb.ians.ui.screens.reader

import android.content.Intent
import android.net.Uri
import android.view.View
import android.view.WindowInsets
import android.view.WindowInsetsController
import android.widget.FrameLayout
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.BrightnessMedium
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.FastForward
import androidx.compose.material.icons.filled.Forward10
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.FullscreenExit
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Replay10
import androidx.compose.material.icons.filled.ScreenRotation
import androidx.compose.material.icons.filled.VolumeDown
import androidx.compose.material.icons.filled.VolumeOff
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material.icons.outlined.ErrorOutline
import androidx.compose.material.icons.outlined.MusicNote
import androidx.compose.material.icons.outlined.Podcasts
import androidx.compose.material.icons.outlined.Videocam
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.core.view.WindowCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebTopBar
import kotlin.math.abs
import kotlinx.coroutines.delay

private val SPEEDS = listOf(0.5f, 0.75f, 1f, 1.25f, 1.5f, 1.75f, 2f)
private const val SEEK_MS = 10_000L
private enum class GestureType { BRIGHTNESS, VOLUME, SEEK }

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun MediaPlayerScreen(
    onNavigateBack: () -> Unit,
    startFullscreen: Boolean = false,
    viewModel: MediaPlayerViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val activity = context as? android.app.Activity
    val player = viewModel.getPlayer()
    var isFullscreen by remember { mutableStateOf(startFullscreen) }

    LaunchedEffect(Unit) {
        if (startFullscreen) {
            activity?.let { act ->
                WindowCompat.setDecorFitsSystemWindows(act.window, false)
                act.requestedOrientation = android.content.pm.ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                act.window?.let { w ->
                    val decor = w.decorView
                    if (android.os.Build.VERSION.SDK_INT >= 30) {
                        val ctrl = decor.windowInsetsController
                        ctrl?.hide(WindowInsets.Type.systemBars())
                        ctrl?.systemBarsBehavior = WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                    } else {
                        @Suppress("DEPRECATION")
                        decor.systemUiVisibility = (View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                            or View.SYSTEM_UI_FLAG_FULLSCREEN
                            or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION)
                    }
                }
            }
        }
    }

    val subjectName = uiState.resource?.subject?.split(",")?.firstOrNull()?.trim().orEmpty().ifBlank { "General" }
    val sc = MaterialTheme.colorScheme.onSurface

    DisposableEffect(uiState.speed) {
        player?.setPlaybackSpeed(uiState.speed)
        onDispose {}
    }

    fun toggleFullscreen(fs: Boolean) {
        isFullscreen = fs
        activity?.let { act ->
            WindowCompat.setDecorFitsSystemWindows(act.window, !fs)
            act.requestedOrientation = if (fs) {
                android.content.pm.ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
            } else {
                android.content.pm.ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
            }
            act.window?.let { w ->
                val decor = w.decorView
                if (fs) {
                    if (android.os.Build.VERSION.SDK_INT >= 30) {
                        val ctrl = decor.windowInsetsController
                        ctrl?.hide(WindowInsets.Type.systemBars())
                        ctrl?.systemBarsBehavior = WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                    } else {
                        @Suppress("DEPRECATION")
                        decor.systemUiVisibility = (View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                            or View.SYSTEM_UI_FLAG_FULLSCREEN
                            or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION)
                    }
                } else {
                    if (android.os.Build.VERSION.SDK_INT >= 30) {
                        decor.windowInsetsController?.show(WindowInsets.Type.systemBars())
                    } else {
                        @Suppress("DEPRECATION")
                        decor.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
                    }
                }
            }
        }
    }

    BackHandler(enabled = isFullscreen) { toggleFullscreen(false) }

    DisposableEffect(activity) {
        onDispose {
            activity?.let { act ->
                WindowCompat.setDecorFitsSystemWindows(act.window, true)
                act.requestedOrientation = android.content.pm.ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                if (android.os.Build.VERSION.SDK_INT >= 30) {
                    act.window.decorView.windowInsetsController?.show(WindowInsets.Type.systemBars())
                } else {
                    @Suppress("DEPRECATION")
                    run { act.window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE }
                }
            }
        }
    }

    if (isFullscreen) {
        FullscreenPlayer(
            uiState = uiState,
            player = player,
            subjectColor = sc,
            activity = activity,
            onExitFullscreen = {
                toggleFullscreen(false)
            },
            onNavigateBack = {
                toggleFullscreen(false)
                onNavigateBack()
            },
            onTogglePlay = { viewModel.togglePlay() },
            onSeekBy = { viewModel.seekBy(it) },
            onSeekRatio = { viewModel.seekToRatio(it) },
            onSetSpeed = { viewModel.setSpeed(it) },
            onToggleSpeedMenu = { viewModel.toggleSpeedMenu() },
            onDismissSpeedMenu = { viewModel.dismissSpeedMenu() },
            onSetVolumeFraction = { viewModel.setVolumeFraction(it) },
            onGetVolumeFraction = { viewModel.getVolumeFraction() }
        )
        return
    }

    Scaffold(
        topBar = {
            NebTopBar(
                showBrand = false,
                title = uiState.title.ifBlank { "Media" },
                onBack = onNavigateBack,
                titleFontWeight = FontWeight.Normal
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
        when {
            uiState.isLoading -> Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
            uiState.resource == null -> Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text(uiState.errorMessage ?: "Resource not found", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            else -> {
                val resource = uiState.resource!!
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(top = padding.calculateTopPadding())
                ) {
                    Column(modifier = Modifier.fillMaxSize()) {
                        NmpHeader(
                            isVideo = uiState.isVideo,
                            title = resource.title,
                            subjectColor = sc,
                            fileUrl = resource.fileUrl,
                            onDownload = { url -> context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) },
                            onOpenNew = { url -> context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) }
                        )

                        if (uiState.isVideo) {
                            NmpVideoStage(
                                player = player,
                                subjectColor = sc,
                                hasError = uiState.hasError,
                                isBuffering = uiState.isBuffering,
                                errorMessage = uiState.errorMessage,
                                fileUrl = resource.fileUrl,
                                resumePositionMs = uiState.resumePositionMs,
                                onPlay = { viewModel.play() },
                                onResume = { viewModel.resumeFromSaved() },
                                onSkipResume = { viewModel.skipResume() },
                                onOpenExternal = { url ->
                                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                                },
                                onDoubleTap = { toggleFullscreen(true) },
                                videoWidth = uiState.videoWidth,
                                videoHeight = uiState.videoHeight,
                                modifier = Modifier.weight(1f)
                            )
                        } else {
                            NmpAudioBody(
                                title = resource.title,
                                authorName = resource.authorName,
                                type = resource.type,
                                gradeLevel = resource.gradeLevel,
                                subjectColor = sc,
                                isPlaying = uiState.isPlaying,
                                hasError = uiState.hasError,
                                modifier = Modifier.weight(1f)
                            )
                        }

                        NmpControls(
                            isPlaying = uiState.isPlaying,
                            currentTimeMs = uiState.currentTimeMs,
                            durationMs = uiState.durationMs,
                            bufferedPercent = uiState.bufferedPercent,
                            speed = uiState.speed,
                            speedMenuOpen = uiState.speedMenuOpen,
                            showFullscreen = uiState.isVideo,
                            subjectColor = sc,
                            onPlayPause = { viewModel.togglePlay() },
                            onBack = { viewModel.seekBy(-SEEK_MS) },
                            onFwd = { viewModel.seekBy(SEEK_MS) },
                            onSeekRatio = { viewModel.seekToRatio(it) },
                            onSpeedToggle = { viewModel.toggleSpeedMenu() },
                            onSpeedSelect = { viewModel.setSpeed(it) },
                            onDismissSpeed = { viewModel.dismissSpeedMenu() },
                            onFullscreen = { toggleFullscreen(true) }
                        )
                    }

                    if (uiState.hasError && !uiState.isVideo) {
                        NmpErrorOverlay(
                            message = uiState.errorMessage ?: "Playback unavailable",
                            fileUrl = resource.fileUrl,
                            onOpen = { url -> context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) },
                            modifier = Modifier.align(Alignment.Center).padding(24.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun FullscreenPlayer(
    uiState: MediaPlayerUiState,
    player: androidx.media3.exoplayer.ExoPlayer?,
    subjectColor: Color,
    activity: android.app.Activity?,
    onExitFullscreen: () -> Unit,
    onNavigateBack: () -> Unit,
    onTogglePlay: () -> Unit,
    onSeekBy: (Long) -> Unit,
    onSeekRatio: (Float) -> Unit,
    onSetSpeed: (Float) -> Unit,
    onToggleSpeedMenu: () -> Unit,
    onDismissSpeedMenu: () -> Unit,
    onSetVolumeFraction: (Float) -> Unit,
    onGetVolumeFraction: () -> Float
) {
    val aspectRatio = if (uiState.videoWidth > 0 && uiState.videoHeight > 0) {
        uiState.videoWidth.toFloat() / uiState.videoHeight.toFloat()
    } else {
        16f / 9f
    }

    var showControls by remember { mutableStateOf(true) }

    LaunchedEffect(showControls, uiState.isPlaying) {
        if (showControls && uiState.isPlaying) {
            delay(4000L)
            showControls = false
        }
    }

    LaunchedEffect(uiState.isPlaying) {
        if (!uiState.isPlaying) showControls = true
    }

    val orientation = LocalConfiguration.current.orientation

    fun rotateVideo() {
        activity?.requestedOrientation = if (orientation == android.content.res.Configuration.ORIENTATION_LANDSCAPE) {
            android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        } else {
            android.content.pm.ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        }
        showControls = true
    }

    var gestureType by remember { mutableStateOf<GestureType?>(null) }
    var gestureDelta by remember { mutableFloatStateOf(0f) }
    var gestureStartBrightness by remember { mutableFloatStateOf(0.5f) }
    var gestureStartVolume by remember { mutableFloatStateOf(0.5f) }
    var gestureStartPosition by remember { mutableLongStateOf(0L) }
    var gestureSeekPosition by remember { mutableLongStateOf(0L) }
    var seekBadge by remember { mutableStateOf<Int?>(null) }
    var seekBadgeVisible by remember { mutableStateOf(false) }

    fun applyBrightness(fraction: Float) {
        val lp = activity?.window?.attributes
        if (lp != null) {
            lp.screenBrightness = fraction.coerceIn(0.01f, 1f)
            activity.window?.attributes = lp
        }
    }

    var screenWidth by remember { mutableFloatStateOf(1f) }

    LaunchedEffect(seekBadgeVisible) {
        if (seekBadgeVisible) {
            delay(700L)
            seekBadgeVisible = false
        }
    }

    val progress by remember(uiState.currentTimeMs, uiState.durationMs) {
        derivedStateOf {
            if (uiState.durationMs > 0) (uiState.currentTimeMs.toFloat() / uiState.durationMs).coerceIn(0f, 1f) else 0f
        }
    }
    val remainingMs = (uiState.durationMs - uiState.currentTimeMs).coerceAtLeast(0L)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
            .onSizeChanged { screenWidth = it.width.toFloat() }
            .pointerInput(Unit) {
                detectTapGestures(
                    onTap = { showControls = !showControls },
                    onDoubleTap = { offset ->
                        val isLeft = offset.x < screenWidth / 2f
                        val delta = if (isLeft) -10_000L else 10_000L
                        onSeekBy(delta)
                        seekBadge = if (isLeft) -10 else 10
                        seekBadgeVisible = true
                        showControls = true
                    }
                )
            }
            .pointerInput(Unit) {
                detectDragGestures(
                    onDragStart = { offset ->
                        gestureStartPosition = player?.currentPosition ?: 0L
                        gestureSeekPosition = gestureStartPosition
                        val lp = activity?.window?.attributes
                        gestureStartBrightness = if (lp?.screenBrightness ?: -1f < 0f) 0.5f else lp?.screenBrightness ?: 0.5f
                        gestureStartVolume = onGetVolumeFraction()
                        gestureDelta = 0f
                        gestureType = when {
                            abs(offset.x - screenWidth / 2) < screenWidth * 0.15f -> GestureType.SEEK
                            offset.x < screenWidth / 2 -> GestureType.BRIGHTNESS
                            else -> GestureType.VOLUME
                        }
                    },
                    onDrag = { change, dragAmount ->
                        change.consume()
                        val totalHeight = size.height.toFloat().coerceAtLeast(1f)
                        when (gestureType) {
                            GestureType.SEEK -> {
                                gestureDelta += dragAmount.x
                                val p = player ?: return@detectDragGestures
                                val d = p.duration.coerceAtLeast(0)
                                if (d > 0) {
                                    val seekPct = gestureDelta / screenWidth.coerceAtLeast(1f)
                                    val newPos = (gestureStartPosition + (seekPct * d).toLong()).coerceIn(0, d)
                                    gestureSeekPosition = newPos
                                    p.seekTo(newPos)
                                }
                            }
                            GestureType.BRIGHTNESS -> {
                                val deltaNorm = -dragAmount.y / totalHeight
                                gestureDelta += deltaNorm
                                val frac = (gestureStartBrightness + gestureDelta).coerceIn(0f, 1f)
                                applyBrightness(frac)
                            }
                            GestureType.VOLUME -> {
                                val deltaNorm = -dragAmount.y / totalHeight
                                gestureDelta += deltaNorm
                                val frac = (gestureStartVolume + gestureDelta).coerceIn(0f, 1f)
                                onSetVolumeFraction(frac)
                            }
                            null -> {}
                        }
                    },
                    onDragEnd = {
                        gestureType = null
                        gestureDelta = 0f
                    },
                    onDragCancel = {
                        gestureType = null
                        gestureDelta = 0f
                    }
                )
            },
        contentAlignment = Alignment.Center
    ) {
        AndroidView(
            factory = { ctx -> android.view.SurfaceView(ctx) },
            update = { sv -> player?.setVideoSurfaceView(sv) },
            modifier = Modifier
                .aspectRatio(aspectRatio)
                .align(Alignment.Center)
        )

        if (uiState.isBuffering) {
            CircularProgressIndicator(
                color = Color.White,
                strokeWidth = 2.5.dp,
                trackColor = Color.White.copy(alpha = 0.2f),
                modifier = Modifier.size(36.dp)
            )
        }

        AnimatedVisibility(
            visible = showControls,
            enter = fadeIn(tween(200)),
            exit = fadeOut(tween(300)),
            modifier = Modifier.fillMaxSize()
        ) {
            Box(modifier = Modifier.fillMaxSize()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(140.dp)
                        .align(Alignment.TopCenter)
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Black.copy(alpha = 0.75f), Color.Transparent)
                            )
                        )
                )
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp)
                        .align(Alignment.BottomCenter)
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.85f))
                            )
                        )
                )

                Row(
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .statusBarsPadding()
                        .padding(horizontal = 4.dp, vertical = 4.dp)
                        .fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.Default.ArrowBack,
                            contentDescription = "Back",
                            tint = Color.White
                        )
                    }
                    Text(
                        text = uiState.title,
                        color = Color.White,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 14.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f)
                    )
                    Spacer(Modifier.width(4.dp))
                    IconButton(
                        onClick = { rotateVideo() },
                        modifier = Modifier
                            .size(40.dp)
                            .background(Color.Black.copy(alpha = 0.35f), CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Filled.ScreenRotation,
                            contentDescription = "Rotate video",
                            tint = Color.White,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                    Spacer(Modifier.width(4.dp))
                }

                Row(
                    modifier = Modifier.align(Alignment.Center),
                    horizontalArrangement = Arrangement.spacedBy(28.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(
                        onClick = { onSeekBy(-SEEK_MS); showControls = true },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Icon(Icons.Filled.Replay10, "Rewind 10s", tint = Color.White, modifier = Modifier.size(28.dp))
                    }
                    IconButton(
                        onClick = { onTogglePlay(); showControls = true },
                        modifier = Modifier
                            .size(68.dp)
                            .background(Color.White.copy(alpha = 0.15f), CircleShape)
                            .border(1.5.dp, Color.White.copy(alpha = 0.3f), CircleShape)
                    ) {
                        Icon(
                            imageVector = if (uiState.isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                            contentDescription = if (uiState.isPlaying) "Pause" else "Play",
                            tint = Color.White,
                            modifier = Modifier.size(38.dp)
                        )
                    }
                    IconButton(
                        onClick = { onSeekBy(SEEK_MS); showControls = true },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Icon(Icons.Filled.Forward10, "Forward 10s", tint = Color.White, modifier = Modifier.size(28.dp))
                    }
                }

                Column(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .navigationBarsPadding()
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 10.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    NmpProgressBarFullscreen(
                        currentMs = uiState.currentTimeMs,
                        durationMs = uiState.durationMs,
                        bufferedPercent = uiState.bufferedPercent,
                        subjectColor = subjectColor,
                        onSeek = { ratio ->
                            onSeekRatio(ratio)
                            showControls = true
                        }
                    )

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = fmtTime(uiState.currentTimeMs),
                            color = Color.White,
                            fontSize = 12.sp,
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Medium
                        )
                        Text(
                            text = " / -${fmtTime(remainingMs)}",
                            color = Color.White.copy(alpha = 0.55f),
                            fontSize = 12.sp,
                            fontFamily = FontFamily.Monospace
                        )

                        Spacer(modifier = Modifier.weight(1f))

                        var speedExpanded by remember { mutableStateOf(false) }
                        Box {
                            Button(
                                onClick = { speedExpanded = !speedExpanded; showControls = true },
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = Color.White.copy(alpha = 0.12f),
                                    contentColor = Color.White
                                ),
                                border = BorderStroke(1.dp, Color.White.copy(alpha = 0.3f)),
                                shape = RoundedCornerShape(999.dp),
                                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 0.dp),
                                modifier = Modifier.height(30.dp)
                            ) {
                                Text(
                                    text = if (uiState.speed == 1f) "1×" else "${uiState.speed}×",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 12.sp
                                )
                            }
                            SpeedDropdown(
                                visible = speedExpanded,
                                currentSpeed = uiState.speed,
                                subjectColor = subjectColor,
                                onSelect = { s ->
                                    onSetSpeed(s)
                                    speedExpanded = false
                                    showControls = true
                                },
                                onDismiss = { speedExpanded = false },
                                modifier = Modifier
                                    .align(Alignment.BottomEnd)
                                    .padding(bottom = 36.dp)
                            )
                        }

                        Spacer(modifier = Modifier.width(8.dp))

                        IconButton(
                            onClick = { onExitFullscreen(); showControls = true },
                            modifier = Modifier.size(36.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Filled.FullscreenExit,
                                contentDescription = "Exit Fullscreen",
                                tint = Color.White,
                                modifier = Modifier.size(22.dp)
                            )
                        }
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
                    .padding(horizontal = 32.dp)
                    .background(Color.Black.copy(alpha = 0.55f), RoundedCornerShape(10.dp))
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = if ((seekBadge ?: 0) < 0) "−10s" else "+10s",
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp
                )
            }
        }

        if (gestureType != null) {
            val icon = when (gestureType) {
                GestureType.BRIGHTNESS -> Icons.Filled.BrightnessMedium
                GestureType.VOLUME -> {
                    val frac = (gestureStartVolume + gestureDelta).coerceIn(0f, 1f)
                    if (frac == 0f) Icons.Filled.VolumeOff else if (frac < 0.5f) Icons.Filled.VolumeDown else Icons.Filled.VolumeUp
                }
                GestureType.SEEK -> Icons.Filled.FastForward
                null -> null
            }
            val label = when (gestureType) {
                GestureType.BRIGHTNESS -> {
                    val pct = ((gestureStartBrightness + gestureDelta).coerceIn(0f, 1f) * 100).toInt()
                    "$pct%"
                }
                GestureType.VOLUME -> {
                    val pct = ((gestureStartVolume + gestureDelta).coerceIn(0f, 1f) * 100).toInt()
                    "$pct%"
                }
                GestureType.SEEK -> fmtTime(gestureSeekPosition)
                null -> ""
            }
            Box(
                modifier = Modifier
                    .align(Alignment.Center)
                    .background(Color.Black.copy(alpha = 0.65f), RoundedCornerShape(14.dp))
                    .padding(horizontal = 20.dp, vertical = 14.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    icon?.let {
                        Icon(imageVector = it, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
                    }
                    Text(
                        text = label,
                        color = Color.White,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = if (gestureType == GestureType.SEEK) FontFamily.Monospace else FontFamily.Default
                    )
                }
            }
        }
    }
}

@Composable
private fun NmpProgressBarFullscreen(
    currentMs: Long,
    durationMs: Long,
    bufferedPercent: Int,
    subjectColor: Color,
    onSeek: (Float) -> Unit
) {
    var barWidth by remember { mutableIntStateOf(0) }
    var isDragging by remember { mutableStateOf(false) }
    val progress by remember(currentMs, durationMs) {
        derivedStateOf {
            if (durationMs > 0) (currentMs.toFloat() / durationMs).coerceIn(0f, 1f) else 0f
        }
    }
    val thumbScale by animateFloatAsState(
        targetValue = if (isDragging) 1.5f else 1f,
        animationSpec = tween(150),
        label = "fsThumbScale"
    )

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(28.dp)
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
                .background(Color.White.copy(alpha = 0.25f))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth((bufferedPercent / 100f).coerceIn(0f, 1f))
                    .background(Color.White.copy(alpha = 0.40f))
            )
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(progress)
                    .background(subjectColor)
            )
        }
        val thumbSizeDp = 14.dp * thumbScale
        Box(
            modifier = Modifier
                .offset { IntOffset(x = ((progress * barWidth) - (thumbSizeDp.toPx() / 2)).toInt().coerceAtLeast(0), y = 0) }
                .size(thumbSizeDp)
                .clip(CircleShape)
                .background(Color.White)
        )
    }
}

@Composable
private fun NmpHeader(
    isVideo: Boolean,
    title: String,
    subjectColor: Color,
    fileUrl: String,
    onDownload: (String) -> Unit,
    onOpenNew: (String) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(subjectColor.copy(alpha = 0.04f))
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Row(
            modifier = Modifier
                .clip(RoundedCornerShape(999.dp))
                .background(subjectColor.copy(alpha = 0.10f))
                .border(1.dp, subjectColor.copy(alpha = 0.22f), RoundedCornerShape(999.dp))
                .padding(horizontal = 10.dp, vertical = 3.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Icon(
                imageVector = if (isVideo) Icons.Outlined.Videocam else Icons.Outlined.Podcasts,
                contentDescription = null,
                tint = subjectColor,
                modifier = Modifier.size(14.dp)
            )
            Text(
                text = if (isVideo) "Video" else "Audio",
                color = subjectColor,
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 0.4.sp
            )
        }
        Text(
            text = title,
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 13.sp,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        if (fileUrl.isNotBlank()) {
            IconButton(onClick = { onDownload(fileUrl) }, modifier = Modifier.size(36.dp)) {
                Icon(Icons.Filled.Download, "Download", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
            }
            IconButton(onClick = { onOpenNew(fileUrl) }, modifier = Modifier.size(36.dp)) {
                Icon(Icons.Filled.OpenInNew, "Open in new tab", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
            }
        }
    }
}

@Composable
private fun NmpVideoStage(
    player: androidx.media3.common.Player?,
    subjectColor: Color,
    hasError: Boolean,
    isBuffering: Boolean,
    errorMessage: String?,
    fileUrl: String,
    resumePositionMs: Long,
    onPlay: () -> Unit,
    onResume: () -> Unit,
    onSkipResume: () -> Unit,
    onOpenExternal: (String) -> Unit,
    onDoubleTap: () -> Unit,
    videoWidth: Int,
    videoHeight: Int,
    modifier: Modifier = Modifier
) {
    val showResume = resumePositionMs > 8000L
    var stageSize by remember { mutableStateOf(IntSize.Zero) }
    val aspectRatio = if (videoWidth > 0 && videoHeight > 0) {
        videoWidth.toFloat() / videoHeight.toFloat()
    } else {
        16f / 9f
    }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .background(Color(0xFF0A0A0B))
            .pointerInput(Unit) {
                detectTapGestures(
                    onDoubleTap = { onDoubleTap() },
                    onTap = { onPlay() }
                )
            }
            .onSizeChanged { stageSize = it },
        contentAlignment = Alignment.Center
    ) {
        AndroidView(
            factory = { ctx -> android.view.SurfaceView(ctx) },
            update = { sv -> player?.setVideoSurfaceView(sv) },
            modifier = Modifier
                .aspectRatio(aspectRatio)
                .align(Alignment.Center)
        )

        if (!hasError) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.radialGradient(
                            colors = listOf(subjectColor.copy(alpha = 0.28f), Color.Transparent),
                            center = Offset(
                                if (stageSize.width > 0) 0.7f * stageSize.width else 0f,
                                if (stageSize.height > 0) 0.2f * stageSize.height else 0f
                            ),
                            radius = if (stageSize.width > 0) 0.7f * stageSize.width else 1f
                        )
                    )
            )
        }
        if (!hasError) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(Color.Black.copy(alpha = 0.15f), Color.Black.copy(alpha = 0.55f))
                        )
                    )
            )
        }

        if (isBuffering && !hasError) {
            CircularProgressIndicator(
                modifier = Modifier
                    .size(32.dp)
                    .align(Alignment.Center),
                color = Color.White,
                strokeWidth = 2.5.dp,
                trackColor = Color.White.copy(alpha = 0.25f)
            )
        }

        if (!hasError && !showResume) {
            Box(
                modifier = Modifier
                    .size(72.dp)
                    .clip(CircleShape)
                    .background(subjectColor.copy(alpha = 0.92f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Filled.PlayArrow,
                    contentDescription = "Play",
                    tint = Color.White,
                    modifier = Modifier.size(40.dp)
                )
            }
        }

        if (showResume) {
            Row(
                modifier = Modifier
                    .align(Alignment.BottomStart)
                    .padding(12.dp)
                    .clip(RoundedCornerShape(999.dp))
                    .background(Color(0xFF101012).copy(alpha = 0.88f))
                    .border(1.dp, Color.White.copy(alpha = 0.08f), RoundedCornerShape(999.dp))
                    .padding(start = 12.dp, end = 4.dp, top = 4.dp, bottom = 4.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "Resume from ${fmtTime(resumePositionMs)}",
                    color = Color.White,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.SemiBold,
                    fontFamily = FontFamily.Monospace
                )
                Button(
                    onClick = onResume,
                    colors = ButtonDefaults.buttonColors(containerColor = subjectColor.copy(alpha = 0.90f)),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 5.dp),
                    shape = RoundedCornerShape(999.dp),
                    modifier = Modifier.height(28.dp)
                ) {
                    Text("Resume", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
                IconButton(onClick = onSkipResume, modifier = Modifier.size(28.dp)) {
                    Icon(Icons.Filled.PlayArrow, "Start from beginning", tint = Color.White.copy(alpha = 0.7f), modifier = Modifier.size(16.dp))
                }
            }
        }

        if (hasError) {
            NmpErrorOverlay(
                message = errorMessage ?: "Playback unavailable",
                fileUrl = fileUrl,
                onOpen = onOpenExternal,
                modifier = Modifier.padding(24.dp)
            )
        }
    }
}

@Composable
private fun NmpAudioBody(
    title: String,
    authorName: String?,
    type: String,
    gradeLevel: String,
    subjectColor: Color,
    isPlaying: Boolean,
    hasError: Boolean,
    modifier: Modifier = Modifier
) {
    Row(modifier = modifier.fillMaxWidth()) {
        Box(
            modifier = Modifier
                .width(148.dp)
                .fillMaxHeight()
                .background(Color(0xFF0A0A0B))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.radialGradient(
                            colors = listOf(subjectColor.copy(alpha = 0.40f), Color.Transparent),
                            center = Offset(0.3f, 0.3f),
                            radius = 0.55f
                        )
                    )
                    .background(
                        Brush.radialGradient(
                            colors = listOf(subjectColor.copy(alpha = 0.22f), Color.Transparent),
                            center = Offset(0.8f, 0.7f),
                            radius = 0.50f
                        )
                    )
                    .background(
                        Brush.linearGradient(
                            colors = listOf(subjectColor.copy(alpha = 0.18f), Color(0xFF0A0A0B)),
                            start = Offset.Zero, end = Offset(1f, 1f)
                        )
                    )
            )
            Canvas(modifier = Modifier.size(88.dp).align(Alignment.Center)) {
                drawCircle(color = Color.White.copy(alpha = 0.18f), style = Stroke(width = 1.5f))
            }
            Canvas(modifier = Modifier.size(58.dp).align(Alignment.Center)) {
                drawCircle(color = Color.White.copy(alpha = 0.12f), style = Stroke(width = 1.5f))
            }
            Box(
                modifier = Modifier
                    .size(64.dp)
                    .clip(CircleShape)
                    .background(subjectColor.copy(alpha = 0.85f))
                    .align(Alignment.Center),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Outlined.MusicNote, null, tint = Color.White, modifier = Modifier.size(30.dp))
            }
            if (isPlaying && !hasError) {
                Row(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .padding(bottom = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(3.dp),
                    verticalAlignment = Alignment.Bottom
                ) {
                    AudioBar(playing = isPlaying, delay = 0f, barHeight = 6)
                    AudioBar(playing = isPlaying, delay = 0.12f, barHeight = 10)
                    AudioBar(playing = isPlaying, delay = 0.24f, barHeight = 16)
                    AudioBar(playing = isPlaying, delay = 0.08f, barHeight = 8)
                    AudioBar(playing = isPlaying, delay = 0.2f, barHeight = 12)
                }
            }
        }

        Column(
            modifier = Modifier
                .weight(1f)
                .padding(horizontal = 18.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.Center
        ) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold,
                color = MaterialTheme.colorScheme.onSurface, maxLines = 2, overflow = TextOverflow.Ellipsis)
            Spacer(Modifier.height(4.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                if (!authorName.isNullOrBlank()) {
                    Text(authorName, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text("·", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f))
                }
                Text("$type · $gradeLevel", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun AudioBar(playing: Boolean, delay: Float, barHeight: Int) {
    val transition = rememberInfiniteTransition(label = "bar")
    val scale by transition.animateFloat(
        initialValue = 0.45f,
        targetValue = 1.2f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1000, delayMillis = (delay * 1000).toInt(), easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "barScale"
    )
    Box(
        modifier = Modifier
            .width(3.dp)
            .height(22.dp),
        contentAlignment = Alignment.BottomCenter
    ) {
        Box(
            modifier = Modifier
                .width(3.dp)
                .height((barHeight * (if (playing) scale else 0.45f)).dp)
                .clip(RoundedCornerShape(2.dp))
                .background(Color.White.copy(alpha = 0.55f))
        )
    }
}

@Composable
private fun NmpControls(
    isPlaying: Boolean,
    currentTimeMs: Long,
    durationMs: Long,
    bufferedPercent: Int,
    speed: Float,
    speedMenuOpen: Boolean,
    showFullscreen: Boolean,
    subjectColor: Color,
    onPlayPause: () -> Unit,
    onBack: () -> Unit,
    onFwd: () -> Unit,
    onSeekRatio: (Float) -> Unit,
    onSpeedToggle: () -> Unit,
    onSpeedSelect: (Float) -> Unit,
    onDismissSpeed: () -> Unit,
    onFullscreen: () -> Unit
) {
    val remainingMs = (durationMs - currentTimeMs).coerceAtLeast(0L)
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .padding(start = 12.dp, end = 12.dp, top = 10.dp, bottom = 12.dp)
    ) {
        NmpProgressBar(currentMs = currentTimeMs, durationMs = durationMs, bufferedPercent = bufferedPercent, subjectColor = subjectColor, onSeek = onSeekRatio)
        Spacer(Modifier.height(4.dp))
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            IconButton(onClick = onPlayPause, modifier = Modifier.size(36.dp)) {
                Icon(
                    imageVector = if (isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                    contentDescription = if (isPlaying) "Pause" else "Play",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(20.dp)
                )
            }
            IconButton(onClick = onBack, modifier = Modifier.size(32.dp)) {
                Icon(Icons.Filled.Replay10, "Rewind 10s", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(18.dp))
            }
            IconButton(onClick = onFwd, modifier = Modifier.size(32.dp)) {
                Icon(Icons.Filled.Forward10, "Forward 10s", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(18.dp))
            }
            Text(
                text = fmtTime(currentTimeMs),
                fontSize = 12.sp,
                fontWeight = FontWeight.Medium,
                fontFamily = FontFamily.Monospace,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = " / -${fmtTime(remainingMs)}",
                fontSize = 11.sp,
                fontFamily = FontFamily.Monospace,
                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.55f)
            )
            Spacer(Modifier.weight(1f))

            Box {
                Button(
                    onClick = onSpeedToggle,
                    colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent, contentColor = MaterialTheme.colorScheme.onSurfaceVariant),
                    shape = RoundedCornerShape(999.dp),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp),
                    modifier = Modifier.height(30.dp)
                ) {
                    Text(text = if (speed == 1f) "1×" else "${speed}×", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
                SpeedDropdown(
                    visible = speedMenuOpen,
                    currentSpeed = speed,
                    subjectColor = subjectColor,
                    onSelect = onSpeedSelect,
                    onDismiss = onDismissSpeed,
                    modifier = Modifier.align(Alignment.TopEnd).padding(top = 34.dp)
                )
            }

            if (showFullscreen) {
                IconButton(onClick = onFullscreen, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Fullscreen, "Fullscreen", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
                }
            }
        }
    }
}

@Composable
private fun NmpProgressBar(
    currentMs: Long,
    durationMs: Long,
    bufferedPercent: Int,
    subjectColor: Color,
    onSeek: (Float) -> Unit
) {
    var barWidth by remember { mutableIntStateOf(0) }
    var isDragging by remember { mutableStateOf(false) }
    val progress by remember(currentMs, durationMs) {
        derivedStateOf {
            if (durationMs > 0) (currentMs.toFloat() / durationMs).coerceIn(0f, 1f) else 0f
        }
    }
    val thumbScale by animateFloatAsState(
        targetValue = if (isDragging) 1.4f else 1f,
        animationSpec = tween(150),
        label = "portraitThumbScale"
    )
    val density = androidx.compose.ui.platform.LocalDensity.current

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(28.dp)
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
            .pointerInput(barWidth) {
                detectTapGestures { offset ->
                    val w = barWidth.coerceAtLeast(1).toFloat()
                    onSeek((offset.x / w).coerceIn(0f, 1f))
                }
            }
            .onSizeChanged { barWidth = it.width },
        contentAlignment = Alignment.CenterStart
    ) {
        Box(modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)).background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
            Box(modifier = Modifier.fillMaxHeight().fillMaxWidth((bufferedPercent / 100f).coerceIn(0f, 1f)).clip(RoundedCornerShape(2.dp)).background(MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.28f)))
            Box(modifier = Modifier.fillMaxHeight().fillMaxWidth(progress).clip(RoundedCornerShape(2.dp)).background(subjectColor))
        }
        val thumbSizeDp = 12.dp * thumbScale
        Box(
            modifier = Modifier
                .offset { IntOffset(x = ((progress * barWidth) - (thumbSizeDp.toPx() / 2)).toInt().coerceAtLeast(0), y = 0) }
                .size(thumbSizeDp)
                .clip(CircleShape)
                .background(subjectColor)
        )
    }
}

@Composable
private fun SpeedDropdown(
    visible: Boolean,
    currentSpeed: Float,
    subjectColor: Color,
    onSelect: (Float) -> Unit,
    onDismiss: () -> Unit,
    modifier: Modifier = Modifier
) {
    AnimatedVisibility(
        visible = visible,
        enter = fadeIn() + slideInVertically(initialOffsetY = { it / 2 }),
        exit = fadeOut(),
        modifier = modifier
    ) {
        Column(
            modifier = Modifier
                .width(100.dp)
                .clip(RoundedCornerShape(10.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(10.dp))
                .padding(4.dp)
        ) {
            SPEEDS.forEach { s ->
                val isActive = s == currentSpeed
                Text(
                    text = if (s == 1f) "Normal" else "${s}×",
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(6.dp))
                        .then(if (isActive) Modifier.background(subjectColor.copy(alpha = 0.10f)) else Modifier)
                        .clickable { onSelect(s) }
                        .padding(horizontal = 12.dp, vertical = 9.dp),
                    color = if (isActive) subjectColor else MaterialTheme.colorScheme.onSurface,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 13.sp
                )
            }
        }
    }
}

@Composable
private fun NmpErrorOverlay(
    message: String,
    fileUrl: String,
    onOpen: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(Icons.Outlined.ErrorOutline, null, tint = Color.White.copy(alpha = 0.7f), modifier = Modifier.size(36.dp))
        Text(message, color = Color.White.copy(alpha = 0.8f), fontSize = 14.sp, textAlign = TextAlign.Center, maxLines = 3, modifier = Modifier.widthIn(max = 280.dp))
        if (fileUrl.isNotBlank()) {
            Button(
                onClick = { onOpen(fileUrl) },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF1F1F3), contentColor = Color(0xFF101012)),
                shape = RoundedCornerShape(999.dp),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Text("Open file directly", fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
            }
        }
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
