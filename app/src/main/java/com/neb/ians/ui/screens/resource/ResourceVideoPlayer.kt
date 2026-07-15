package com.neb.ians.ui.screens.resource

import android.view.SurfaceView
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
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
import androidx.compose.material.icons.outlined.AudioFile
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.screens.reader.MediaPlayerViewModel

@Composable
fun EmbeddedMediaPlayer(
    resourceId: String,
    fileUrl: String,
    isVideo: Boolean,
    subjectColor: Color,
    title: String,
    onFullscreenClick: () -> Unit,
    modifier: Modifier = Modifier,
    fullWidth: Boolean = false,
    viewModel: MediaPlayerViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
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
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .aspectRatio(16f / 9f)
                            .background(Color.Black)
                    ) {
                        AndroidView(
                            factory = { ctx ->
                                SurfaceView(ctx)
                            },
                            update = { sv ->
                                player?.setVideoSurfaceView(sv)
                            },
                            modifier = Modifier.fillMaxSize()
                        )
                        
                        if (uiState.isBuffering) {
                            CircularProgressIndicator(
                                color = subjectColor,
                                modifier = Modifier.align(Alignment.Center)
                            )
                        }
                    }
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
                }

                EmbeddedProgressBar(
                    currentMs = uiState.currentTimeMs,
                    durationMs = uiState.durationMs,
                    bufferedPercent = uiState.bufferedPercent,
                    subjectColor = subjectColor,
                    onSeek = { ratio -> viewModel.seekToRatio(ratio) }
                )

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
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }

                    IconButton(onClick = { viewModel.seekBy(-10000L) }) {
                        Icon(
                            imageVector = Icons.Filled.Replay10,
                            contentDescription = "Rewind 10s",
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }

                    IconButton(onClick = { viewModel.seekBy(10000L) }) {
                        Icon(
                            imageVector = Icons.Filled.Forward10,
                            contentDescription = "Forward 10s",
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }

                    Spacer(modifier = Modifier.width(6.dp))

                    Text(
                        text = "${fmtTime(uiState.currentTimeMs)} / ${fmtTime(uiState.durationMs)}",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )

                    Spacer(modifier = Modifier.weight(1f))

                    IconButton(onClick = onFullscreenClick) {
                        Icon(
                            imageVector = Icons.Filled.Fullscreen,
                            contentDescription = "Fullscreen",
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun EmbeddedProgressBar(
    currentMs: Long,
    durationMs: Long,
    bufferedPercent: Int,
    subjectColor: Color,
    onSeek: (Float) -> Unit
) {
    var barWidth by remember { mutableStateOf(0) }
    val progress = if (durationMs > 0) (currentMs.toFloat() / durationMs).coerceIn(0f, 1f) else 0f

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(12.dp)
            .background(Color.Transparent)
            .clickable(
                interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                indication = null
            ) { }
            .pointerInput(barWidth) {
                detectTapGestures { offset ->
                    val w = barWidth.coerceAtLeast(1).toFloat()
                    onSeek((offset.x / w).coerceIn(0f, 1f))
                }
            }
            .pointerInput(barWidth) {
                detectDragGestures(
                    onDragStart = { offset ->
                        val w = barWidth.coerceAtLeast(1).toFloat()
                        onSeek((offset.x / w).coerceIn(0f, 1f))
                    },
                    onDrag = { change, _ ->
                        change.consume()
                        val w = barWidth.coerceAtLeast(1).toFloat()
                        onSeek((change.position.x / w).coerceIn(0f, 1f))
                    }
                )
            }
            .onSizeChanged { barWidth = it.width },
        contentAlignment = Alignment.CenterStart
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(4.dp)
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth((bufferedPercent / 100f).coerceIn(0f, 1f))
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.12f))
            )
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(progress)
                    .background(subjectColor)
            )
        }
    }
}

private fun fmtTime(ms: Long): String {
    val totalSec = ms / 1000
    val min = totalSec / 60
    val sec = totalSec % 60
    return String.format("%d:%02d", min, sec)
}
