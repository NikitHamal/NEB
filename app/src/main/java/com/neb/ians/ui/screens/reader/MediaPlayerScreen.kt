package com.neb.ians.ui.screens.reader

import android.content.Intent
import android.net.Uri
import android.view.View
import android.view.WindowInsets
import android.view.WindowInsetsController
import android.widget.FrameLayout
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.Canvas
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Forward10
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Replay10
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
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.util.getSubjectColor

private val SPEEDS = listOf(0.5f, 0.75f, 1f, 1.25f, 1.5f, 1.75f, 2f)
private const val SEEK_MS = 10_000L

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun MediaPlayerScreen(
    onNavigateBack: () -> Unit,
    viewModel: MediaPlayerViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val activity = context as? android.app.Activity
    val player = viewModel.getPlayer()
    var isFullscreen by remember { mutableStateOf(false) }

    val subjectName = uiState.resource?.subject?.split(",")?.firstOrNull()?.trim().orEmpty().ifBlank { "General" }
    val sc = Color(getSubjectColor(subjectName))

    DisposableEffect(uiState.speed) {
        player?.setPlaybackSpeed(uiState.speed)
        onDispose {}
    }

    fun toggleFullscreen(fs: Boolean) {
        isFullscreen = fs
        activity?.window?.let { w ->
            val decor = w.decorView
            if (fs) {
                if (android.os.Build.VERSION.SDK_INT >= 35) {
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
                if (android.os.Build.VERSION.SDK_INT >= 35) {
                    decor.windowInsetsController?.show(WindowInsets.Type.systemBars())
                } else {
                    @Suppress("DEPRECATION")
                    decor.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
                }
            }
        }
    }

    if (isFullscreen) {
        Box(modifier = Modifier.fillMaxSize().background(Color.Black).clickable { toggleFullscreen(false) }) {
            AndroidView(
                factory = { ctx ->
                    FrameLayout(ctx).apply {
                        setBackgroundColor(android.graphics.Color.BLACK)
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
        }
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
                            volume = uiState.volume,
                            isMuted = uiState.isMuted,
                            speed = uiState.speed,
                            speedMenuOpen = uiState.speedMenuOpen,
                            showFullscreen = uiState.isVideo,
                            subjectColor = sc,
                            onPlayPause = { viewModel.togglePlay() },
                            onBack = { viewModel.seekBy(-SEEK_MS) },
                            onFwd = { viewModel.seekBy(SEEK_MS) },
                            onSeekRatio = { viewModel.seekToRatio(it) },
                            onVolumeChange = { viewModel.setVolume(it) },
                            onMuteToggle = { viewModel.toggleMute() },
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
    modifier: Modifier = Modifier
) {
    val showResume = resumePositionMs > 8000L
    var stageSize by remember { mutableStateOf(IntSize.Zero) }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .background(Color(0xFF0A0F18))
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
            factory = { ctx ->
                android.view.SurfaceView(ctx).also { sv ->
                    sv.setBackgroundColor(android.graphics.Color.BLACK)
                }
            },
            update = { sv -> player?.setVideoSurfaceView(sv) },
            modifier = Modifier.fillMaxSize()
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
                    .size(28.dp)
                    .align(Alignment.TopEnd)
                    .padding(12.dp),
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
                    .background(Color(0xFF0F172A).copy(alpha = 0.88f))
                    .border(1.dp, Color.White.copy(alpha = 0.08f), RoundedCornerShape(999.dp))
                    .padding(start = 12.dp, end = 4.dp, top = 4.dp, bottom = 4.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "Resume from ${fmtTime(resumePositionMs)}",
                    color = Color.White,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Button(
                    onClick = onResume,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = subjectColor.copy(alpha = 0.90f)
                    ),
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
                .background(Color(0xFF0A0F18))
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
                            colors = listOf(subjectColor.copy(alpha = 0.18f), Color(0xFF0A0F18)),
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
    volume: Float,
    isMuted: Boolean,
    speed: Float,
    speedMenuOpen: Boolean,
    showFullscreen: Boolean,
    subjectColor: Color,
    onPlayPause: () -> Unit,
    onBack: () -> Unit,
    onFwd: () -> Unit,
    onSeekRatio: (Float) -> Unit,
    onVolumeChange: (Float) -> Unit,
    onMuteToggle: () -> Unit,
    onSpeedToggle: () -> Unit,
    onSpeedSelect: (Float) -> Unit,
    onDismissSpeed: () -> Unit,
    onFullscreen: () -> Unit
) {
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
                text = "${fmtTime(currentTimeMs)} / ${fmtTime(durationMs)}",
                fontSize = 12.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(Modifier.weight(1f))

            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(2.dp)) {
                val volIcon = when {
                    isMuted || volume == 0f -> Icons.Filled.VolumeOff
                    volume < 0.4f -> Icons.Filled.VolumeDown
                    else -> Icons.Filled.VolumeUp
                }
                IconButton(onClick = onMuteToggle, modifier = Modifier.size(36.dp)) {
                    Icon(volIcon, "Volume", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
                }
                Slider(
                    value = if (isMuted) 0f else volume,
                    onValueChange = onVolumeChange,
                    valueRange = 0f..1f,
                    modifier = Modifier.width(72.dp).height(24.dp),
                    colors = SliderDefaults.colors(thumbColor = subjectColor, activeTrackColor = subjectColor, inactiveTrackColor = MaterialTheme.colorScheme.surfaceContainerHigh)
                )
            }

            Box {
                Button(
                    onClick = onSpeedToggle,
                    colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent, contentColor = MaterialTheme.colorScheme.onSurfaceVariant),
                    shape = RoundedCornerShape(999.dp),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text(text = if (speed == 1f) "1x" else "${speed}x", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
                SpeedDropdown(
                    visible = speedMenuOpen,
                    currentSpeed = speed,
                    subjectColor = subjectColor,
                    onSelect = onSpeedSelect,
                    onDismiss = onDismissSpeed,
                    modifier = Modifier.align(Alignment.TopEnd).padding(top = 36.dp)
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
    val density = LocalDensity.current
    var barWidth by remember { mutableIntStateOf(0) }
    val progress = if (durationMs > 0) (currentMs.toFloat() / durationMs).coerceIn(0f, 1f) else 0f

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(28.dp)
            .pointerInput(barWidth) {
                detectDragGestures(
                    onDragStart = { offset -> val w = barWidth.coerceAtLeast(1).toFloat(); onSeek((offset.x / w).coerceIn(0f, 1f)) },
                    onDrag = { change, _ -> change.consume(); val w = barWidth.coerceAtLeast(1).toFloat(); onSeek((change.position.x / w).coerceIn(0f, 1f)) }
                )
            }
            .pointerInput(barWidth) {
                detectTapGestures { offset -> val w = barWidth.coerceAtLeast(1).toFloat(); onSeek((offset.x / w).coerceIn(0f, 1f)) }
            }
            .onSizeChanged { barWidth = it.width },
        contentAlignment = Alignment.CenterStart
    ) {
        Box(modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)).background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
            Box(modifier = Modifier.fillMaxHeight().fillMaxWidth((bufferedPercent / 100f).coerceIn(0f, 1f)).clip(RoundedCornerShape(2.dp)).background(MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.28f)))
            Box(modifier = Modifier.fillMaxHeight().fillMaxWidth(progress).clip(RoundedCornerShape(2.dp)).background(subjectColor))
        }
        Box(
            modifier = Modifier
                .offset(x = with(density) { ((progress * barWidth) - 6.dp.toPx()).coerceAtLeast(0f) }.dp)
                .size(12.dp).clip(CircleShape).background(subjectColor)
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
                .width(96.dp)
                .clip(RoundedCornerShape(10.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(10.dp))
                .padding(4.dp)
        ) {
            SPEEDS.forEach { s ->
                val isActive = s == currentSpeed
                Text(
                    text = if (s == 1f) "Normal" else "${s}x",
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(6.dp))
                        .then(if (isActive) Modifier.background(subjectColor.copy(alpha = 0.10f)) else Modifier)
                        .clickable { onSelect(s) }
                        .padding(horizontal = 12.dp, vertical = 8.dp),
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
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFB4C5FF), contentColor = Color(0xFF00174B)),
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
