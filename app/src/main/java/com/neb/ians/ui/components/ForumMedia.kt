package com.neb.ians.ui.components

import android.content.Intent
import android.net.Uri
import android.view.SurfaceView
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.FullscreenExit
import androidx.compose.material.icons.filled.InsertDriveFile
import androidx.compose.material.icons.filled.MusicNote
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Videocam
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
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import com.neb.ians.data.api.ApiMediaAttachment
import com.neb.ians.ui.screens.forum.PendingForumAttachment
import kotlinx.coroutines.delay
import java.lang.ref.WeakReference
import java.util.Locale

/** Only one forum media element plays at a time across the whole app. */
private object ForumMediaSession {
    var active: WeakReference<ExoPlayer>? = null

    fun requestFocus(player: ExoPlayer) {
        active?.get()?.takeIf { it !== player }?.pause()
        active = WeakReference(player)
    }
}

private fun formatMediaTime(ms: Long): String {
    if (ms <= 0) return "0:00"
    val totalSec = ms / 1000
    val m = totalSec / 60
    val s = totalSec % 60
    return String.format(Locale.US, "%d:%02d", m, s)
}

fun formatAttachmentSize(bytes: Long): String {
    if (bytes <= 0) return ""
    val kb = 1024.0
    val mb = kb * 1024
    val gb = mb * 1024
    return when {
        bytes < kb * 1024 -> String.format(Locale.US, "%.0f KB", bytes / kb)
        bytes < gb -> String.format(Locale.US, "%.1f MB", bytes / mb)
        else -> String.format(Locale.US, "%.2f GB", bytes / gb)
    }
}

/**
 * Renders a post/reply's media attachments: inline video player, inline audio
 * player, and a file chip that opens externally. Used on forum cards, the post
 * detail screen, and shared comment cards.
 */
@Composable
fun ForumMediaAttachments(
    attachments: List<ApiMediaAttachment>,
    modifier: Modifier = Modifier
) {
    if (attachments.isEmpty()) return
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(10.dp)) {
        attachments.sortedBy { it.order }.forEach { attachment ->
            when (attachment.kind) {
                "video" -> ForumVideoPlayer(attachment)
                "audio" -> ForumAudioPlayer(attachment)
                else -> ForumFileChip(attachment)
            }
        }
    }
}

@Composable
private fun rememberMediaPlayer(url: String): ExoPlayer {
    val context = LocalContext.current
    val player = remember(url) {
        ExoPlayer.Builder(context).build().apply {
            setMediaItem(MediaItem.fromUri(url))
            prepare()
            playWhenReady = false
        }
    }
    DisposableEffect(player) {
        onDispose { player.release() }
    }
    return player
}

@Composable
private fun PlayerPositionPoller(player: ExoPlayer, isPlaying: Boolean, onTick: (Long, Long) -> Unit) {
    LaunchedEffect(player, isPlaying) {
        while (true) {
            onTick(player.currentPosition.coerceAtLeast(0), player.duration.coerceAtLeast(0))
            delay(if (isPlaying) 250 else 900)
        }
    }
}

// ---------- Inline video ----------

@Composable
fun ForumVideoPlayer(attachment: ApiMediaAttachment, modifier: Modifier = Modifier) {
    val url = resolveMediaUrl(attachment.url) ?: return
    val player = rememberMediaPlayer(url)
    var isPlaying by remember { mutableStateOf(false) }
    var positionMs by remember { mutableLongStateOf(0L) }
    var durationMs by remember { mutableLongStateOf(0L) }
    var dragging by remember { mutableStateOf(false) }
    var dragPosition by remember { mutableLongStateOf(0L) }
    var controlsVisible by remember { mutableStateOf(true) }
    var fullscreen by remember { mutableStateOf(false) }

    DisposableEffect(player) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
                if (playing) ForumMediaSession.requestFocus(player)
            }
        }
        player.addListener(listener)
        onDispose { player.removeListener(listener) }
    }
    PlayerPositionPoller(player, isPlaying) { pos, dur ->
        if (!dragging) positionMs = pos
        durationMs = dur
    }

    // Collapse controls while playing after a few idle seconds.
    LaunchedEffect(controlsVisible, isPlaying) {
        if (controlsVisible && isPlaying) {
            delay(3200)
            controlsVisible = false
        }
    }

    val safeDuration = if (durationMs > 0) durationMs else 1L
    val shownPosition = if (dragging) dragPosition else positionMs

    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        color = Color.Black
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) {
                    controlsVisible = !controlsVisible
                    if (!controlsVisible && !isPlaying) controlsVisible = true
                }
        ) {
            AndroidView(
                factory = { ctx ->
                    SurfaceView(ctx).also { player.setVideoSurfaceView(it) }
                },
                modifier = Modifier.fillMaxSize()
            )

            if (controlsVisible) {
                // Center play/pause
                Surface(
                    onClick = {
                        ForumMediaSession.requestFocus(player)
                        if (player.isPlaying) player.pause() else player.play()
                    },
                    shape = CircleShape,
                    color = Color.Black.copy(alpha = 0.55f),
                    modifier = Modifier
                        .align(Alignment.Center)
                        .size(56.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = if (isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                            contentDescription = if (isPlaying) "Pause" else "Play",
                            tint = Color.White,
                            modifier = Modifier.size(30.dp)
                        )
                    }
                }

                // Bottom control bar
                Surface(
                    color = Color.Black.copy(alpha = 0.55f),
                    modifier = Modifier.align(Alignment.BottomCenter)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                    ) {
                        IconButton(onClick = {
                            ForumMediaSession.requestFocus(player)
                            if (player.isPlaying) player.pause() else player.play()
                        }) {
                            Icon(
                                imageVector = if (isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                                contentDescription = null,
                                tint = Color.White
                            )
                        }
                        Text(
                            text = formatMediaTime(shownPosition),
                            color = Color.White,
                            style = MaterialTheme.typography.labelSmall
                        )
                        Slider(
                            value = (shownPosition.toFloat() / safeDuration.toFloat()).coerceIn(0f, 1f),
                            onValueChange = { fraction ->
                                dragging = true
                                dragPosition = (fraction * safeDuration).toLong()
                            },
                            onValueChangeFinished = {
                                positionMs = dragPosition
                                player.seekTo(dragPosition)
                                dragging = false
                            },
                            modifier = Modifier
                                .weight(1f)
                                .padding(horizontal = 6.dp),
                            colors = SliderDefaults.colors(
                                thumbColor = Color.White,
                                activeTrackColor = Color.White,
                                inactiveTrackColor = Color.White.copy(alpha = 0.35f)
                            )
                        )
                        Text(
                            text = formatMediaTime(durationMs),
                            color = Color.White,
                            style = MaterialTheme.typography.labelSmall
                        )
                        IconButton(onClick = { fullscreen = true }) {
                            Icon(
                                imageVector = Icons.Filled.Fullscreen,
                                contentDescription = "Fullscreen",
                                tint = Color.White
                            )
                        }
                    }
                }
            }
        }
    }

    if (fullscreen) {
        ForumVideoFullscreenDialog(
            player = player,
            isPlaying = isPlaying,
            onDismiss = { fullscreen = false }
        )
    }
}

@Composable
private fun ForumVideoFullscreenDialog(
    player: ExoPlayer,
    isPlaying: Boolean,
    onDismiss: () -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black)
        ) {
            AndroidView(
                factory = { ctx ->
                    SurfaceView(ctx).also { player.setVideoSurfaceView(it) }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(16f / 9f)
                    .align(Alignment.Center)
            )
            Surface(
                onClick = onDismiss,
                shape = CircleShape,
                color = Color.Black.copy(alpha = 0.6f),
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(18.dp)
                    .size(44.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Filled.FullscreenExit,
                        contentDescription = "Exit fullscreen",
                        tint = Color.White
                    )
                }
            }
            if (!isPlaying) {
                Surface(
                    onClick = {
                        ForumMediaSession.requestFocus(player)
                        player.play()
                    },
                    shape = CircleShape,
                    color = Color.Black.copy(alpha = 0.6f),
                    modifier = Modifier
                        .align(Alignment.Center)
                        .size(64.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Filled.PlayArrow,
                            contentDescription = "Play",
                            tint = Color.White,
                            modifier = Modifier.size(34.dp)
                        )
                    }
                }
            }
        }
    }
}

// ---------- Inline audio ----------

@Composable
fun ForumAudioPlayer(attachment: ApiMediaAttachment, modifier: Modifier = Modifier) {
    val url = resolveMediaUrl(attachment.url) ?: return
    val player = rememberMediaPlayer(url)
    var isPlaying by remember { mutableStateOf(false) }
    var positionMs by remember { mutableLongStateOf(0L) }
    var durationMs by remember { mutableLongStateOf(0L) }
    var dragging by remember { mutableStateOf(false) }
    var dragPosition by remember { mutableLongStateOf(0L) }

    DisposableEffect(player) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
                if (playing) ForumMediaSession.requestFocus(player)
            }
        }
        player.addListener(listener)
        onDispose { player.removeListener(listener) }
    }
    PlayerPositionPoller(player, isPlaying) { pos, dur ->
        if (!dragging) positionMs = pos
        durationMs = dur
    }

    val safeDuration = if (durationMs > 0) durationMs else 1L
    val shownPosition = if (dragging) dragPosition else positionMs

    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp)
        ) {
            Surface(
                onClick = {
                    ForumMediaSession.requestFocus(player)
                    if (player.isPlaying) player.pause() else player.play()
                },
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(42.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = if (isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                        contentDescription = if (isPlaying) "Pause" else "Play",
                        tint = MaterialTheme.colorScheme.onPrimary
                    )
                }
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Filled.MusicNote,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(14.dp)
                    )
                    Spacer(modifier = Modifier.width(5.dp))
                    Text(
                        text = attachment.name.ifBlank { "Audio track" },
                        style = MaterialTheme.typography.bodySmall,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurface,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(4.dp))
                Slider(
                    value = (shownPosition.toFloat() / safeDuration.toFloat()).coerceIn(0f, 1f),
                    onValueChange = { fraction ->
                        dragging = true
                        dragPosition = (fraction * safeDuration).toLong()
                    },
                    onValueChangeFinished = {
                        positionMs = dragPosition
                        player.seekTo(dragPosition)
                        dragging = false
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(18.dp),
                    colors = SliderDefaults.colors(
                        thumbColor = MaterialTheme.colorScheme.primary,
                        activeTrackColor = MaterialTheme.colorScheme.primary,
                        inactiveTrackColor = MaterialTheme.colorScheme.surfaceContainerHighest
                    )
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = formatMediaTime(shownPosition),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = formatMediaTime(durationMs),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

// ---------- File chip ----------

@Composable
fun ForumFileChip(attachment: ApiMediaAttachment, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val url = resolveMediaUrl(attachment.url) ?: return
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        onClick = {
            try {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                context.startActivity(intent)
            } catch (_: Exception) {}
        }
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp)
        ) {
            Surface(
                shape = RoundedCornerShape(10.dp),
                color = MaterialTheme.colorScheme.secondaryContainer,
                modifier = Modifier.size(40.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Filled.InsertDriveFile,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSecondaryContainer,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = attachment.name.ifBlank { "Attachment" },
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                val sizeLabel = formatAttachmentSize(attachment.sizeBytes)
                Text(
                    text = if (sizeLabel.isBlank()) "Tap to open" else "$sizeLabel · Tap to open",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Icon(
                imageVector = Icons.Filled.Download,
                contentDescription = "Open file",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(20.dp)
            )
        }
    }
}

// ---------- Compact media badges (feed cards) ----------

/**
 * Compact indicator used inside whole-tappable feed cards — the full players
 * live on the detail screen; nesting them inside a clickable card would make
 * touches ambiguous and scrolling heavy.
 */
@Composable
fun ForumMediaBadges(
    attachments: List<ApiMediaAttachment>,
    modifier: Modifier = Modifier
) {
    if (attachments.isEmpty()) return
    val videos = attachments.count { it.kind == "video" }
    val audios = attachments.count { it.kind == "audio" }
    val files = attachments.size - videos - audios
    Row(modifier = modifier, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        if (videos > 0) MediaBadge(icon = { Icon(Icons.Filled.Videocam, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(14.dp)) }, label = if (videos > 1) "$videos videos" else "Video")
        if (audios > 0) MediaBadge(icon = { Icon(Icons.Filled.MusicNote, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(14.dp)) }, label = if (audios > 1) "$audios audio" else "Audio")
        if (files > 0) MediaBadge(icon = { Icon(Icons.Filled.InsertDriveFile, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(14.dp)) }, label = if (files > 1) "$files files" else "File")
    }
}

@Composable
private fun MediaBadge(icon: @Composable () -> Unit, label: String) {
    Surface(
        shape = RoundedCornerShape(999.dp),
        color = MaterialTheme.colorScheme.surfaceContainerHigh
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(5.dp),
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp)
        ) {
            icon()
            Text(
                text = label,
                style = MaterialTheme.typography.labelSmall,
                fontWeight = FontWeight.Medium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

// ---------- Composer pending-attachment chip ----------

@Composable
fun ForumAttachmentChip(
    attachment: PendingForumAttachment,
    onRemove: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainerHigh,
        border = if (attachment.error != null) {
            androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error)
        } else null
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp)
        ) {
            Surface(
                shape = RoundedCornerShape(8.dp),
                color = if (attachment.error != null) MaterialTheme.colorScheme.errorContainer
                else MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(32.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = when (attachment.kind) {
                            "video" -> Icons.Filled.Videocam
                            "audio" -> Icons.Filled.MusicNote
                            else -> Icons.Filled.InsertDriveFile
                        },
                        contentDescription = null,
                        tint = if (attachment.error != null) MaterialTheme.colorScheme.onErrorContainer
                        else MaterialTheme.colorScheme.onPrimary,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.width(10.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = attachment.name,
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    color = MaterialTheme.colorScheme.onSurface
                )
                val meta = when {
                    attachment.uploading -> "Uploading…"
                    attachment.error != null -> attachment.error
                    else -> attachment.kind.replaceFirstChar { it.uppercase(Locale.US) } +
                        formatAttachmentSize(attachment.sizeBytes).let { s -> if (s.isBlank()) "" else " · $s" }
                }
                Text(
                    text = meta ?: "",
                    style = MaterialTheme.typography.labelSmall,
                    color = if (attachment.error != null) MaterialTheme.colorScheme.error
                    else MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            if (attachment.uploading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(18.dp),
                    strokeWidth = 2.dp,
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.width(8.dp))
            }
            IconButton(onClick = onRemove, modifier = Modifier.size(28.dp)) {
                Icon(
                    imageVector = Icons.Filled.Close,
                    contentDescription = "Remove attachment",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(16.dp)
                )
            }
        }
    }
}
