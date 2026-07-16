package com.neb.ians.ui.screens.resource

import android.content.Intent
import android.content.pm.ActivityInfo
import android.net.Uri
import android.view.View
import android.view.WindowInsets
import android.view.WindowInsetsController
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.core.view.WindowCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.media3.common.Player
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.ExpandableText
import com.neb.ians.ui.components.NebAvatar
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.ZoomableImageDialog
import com.neb.ians.ui.screens.reader.MediaPlayerUiState
import com.neb.ians.ui.screens.reader.MediaPlayerViewModel
import com.neb.ians.util.formatTimeAgo
import kotlinx.coroutines.delay
import kotlin.math.abs

@Composable
fun ResourceDetailScreen(
    onNavigateBack: () -> Unit,
    onOpenPdf: (resourceId: String, fileUrl: String, title: String) -> Unit,
    onUserProfileClick: (String) -> Unit = {},
    onRelatedResourceClick: (String) -> Unit = {},
    viewModel: ResourceDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val activity = context as? android.app.Activity
    val snackbarHostState = remember { SnackbarHostState() }
    var zoomImageUrl by remember { mutableStateOf<String?>(null) }
    var isFullscreen by remember { mutableStateOf(false) }
    val mediaViewModel: MediaPlayerViewModel = hiltViewModel()

    fun openExternal(url: String) {
        if (url.isBlank()) return
        runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) }
    }

    fun share(title: String, id: String) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, title)
            putExtra(Intent.EXTRA_TEXT, "$title\nhttps://nebians.consica.com.np/resource/$id/")
        }
        runCatching { context.startActivity(Intent.createChooser(intent, "Share resource")) }
    }

    fun enterFullscreen() {
        isFullscreen = true
        activity?.let { act ->
            WindowCompat.setDecorFitsSystemWindows(act.window, false)
            act.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
            val decor = act.window?.decorView
            if (decor != null) {
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

    fun exitFullscreen() {
        isFullscreen = false
        activity?.let { act ->
            act.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
            WindowCompat.setDecorFitsSystemWindows(act.window, true)
            val decor = act.window?.decorView
            if (decor != null) {
                if (android.os.Build.VERSION.SDK_INT >= 30) {
                    decor.windowInsetsController?.show(WindowInsets.Type.systemBars())
                } else {
                    @Suppress("DEPRECATION")
                    decor.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
                }
            }
        }
    }

    BackHandler(enabled = isFullscreen, onBack = ::exitFullscreen)

    DisposableEffect(activity) {
        onDispose {
            activity?.let { act ->
                act.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                WindowCompat.setDecorFitsSystemWindows(act.window, true)
                if (android.os.Build.VERSION.SDK_INT >= 30) {
                    act.window.decorView.windowInsetsController?.show(WindowInsets.Type.systemBars())
                } else {
                    @Suppress("DEPRECATION")
                    run { act.window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE }
                }
            }
        }
    }

    LaunchedEffect(uiState.snackbarMessage) {
        uiState.snackbarMessage?.let { message ->
            snackbarHostState.showSnackbar(message)
            viewModel.consumeSnackbar()
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Scaffold(
            topBar = {
                if (!isFullscreen) {
                    NebTopBar(
                        showBrand = false,
                        title = if (uiState.resource != null && detectResourceMedia(uiState.resource!!.fileUrl, uiState.resource!!.type) == ResourceMediaType.Video) "Video" else "Resource",
                        onBack = onNavigateBack
                    )
                }
            },
            bottomBar = {
                if (!isFullscreen && uiState.resource != null) {
                    NebCommentComposerBar(
                        value = uiState.commentDraft,
                        onValueChange = viewModel::onCommentDraftChange,
                        placeholder = if (uiState.isAuthenticated) "Write a comment..." else "Sign in to comment",
                        enabled = uiState.isAuthenticated && !uiState.isPostingComment,
                        canSend = uiState.isAuthenticated && uiState.commentDraft.isNotBlank() && !uiState.isPostingComment,
                        posting = uiState.isPostingComment,
                        sendContentDescription = "Post comment",
                        onSend = viewModel::postComment
                    )
                }
            },
            snackbarHost = { if (!isFullscreen) SnackbarHost(snackbarHostState) },
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
        ) { padding ->
            if (!isFullscreen) {
                when {
                    uiState.isLoading && uiState.resource == null -> Box(
                        Modifier.fillMaxSize().padding(padding),
                        contentAlignment = Alignment.Center
                    ) { CircularProgressIndicator() }

                    uiState.resource == null -> Box(
                        Modifier.fillMaxSize().padding(padding),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(uiState.error ?: "Resource not found", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }

                    else -> {
                        val resource = uiState.resource!!
                        val mediaType = detectResourceMedia(resource.fileUrl, resource.type)
                        val subject = resource.subject.split(",").firstOrNull()?.trim().orEmpty().ifBlank { "General" }
                        val subjectColor = Color(com.neb.ians.util.getSubjectColor(subject))

                        if (mediaType == ResourceMediaType.Video) {
                            VideoYouTubeLayout(
                                resource = resource,
                                subjectColor = subjectColor,
                                uiState = uiState,
                                viewModel = viewModel,
                                mediaViewModel = mediaViewModel,
                                onFullscreenClick = ::enterFullscreen,
                                onUserProfileClick = onUserProfileClick,
                                onRelatedResourceClick = onRelatedResourceClick,
                                share = ::share,
                                openExternal = ::openExternal,
                                padding = padding
                            )
                        } else {
                            NonVideoLayout(
                                resource = resource,
                                mediaType = mediaType,
                                subjectColor = subjectColor,
                                uiState = uiState,
                                viewModel = viewModel,
                                onOpenPdf = onOpenPdf,
                                onUserProfileClick = onUserProfileClick,
                                share = ::share,
                                openExternal = ::openExternal,
                                padding = padding,
                                onZoomImage = { zoomImageUrl = it }
                            )
                        }
                    }
                }
            }
        }

        if (isFullscreen) {
            val mediaState by mediaViewModel.uiState.collectAsStateWithLifecycle()
            FullscreenVideoOverlay(
                viewModel = mediaViewModel,
                uiState = mediaState,
                onExit = ::exitFullscreen,
                subjectColor = Color(com.neb.ians.util.getSubjectColor(
                    mediaState.resource?.subject?.split(",")?.firstOrNull()?.trim().orEmpty().ifBlank { "General" }
                ))
            )
        }

        zoomImageUrl?.let { url ->
            ZoomableImageDialog(
                imageUrl = url,
                contentDescription = uiState.resource?.title,
                onDismiss = { zoomImageUrl = null }
            )
        }
    }
}

@Composable
private fun VideoYouTubeLayout(
    resource: ApiResource,
    subjectColor: Color,
    uiState: ResourceDetailUiState,
    viewModel: ResourceDetailViewModel,
    mediaViewModel: MediaPlayerViewModel,
    onFullscreenClick: () -> Unit,
    onUserProfileClick: (String) -> Unit,
    onRelatedResourceClick: (String) -> Unit,
    share: (String, String) -> Unit,
    openExternal: (String) -> Unit,
    padding: PaddingValues
) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(top = padding.calculateTopPadding()),
        contentPadding = PaddingValues(bottom = padding.calculateBottomPadding() + 18.dp)
    ) {
        item(key = "video_player") {
            EmbeddedMediaPlayer(
                resourceId = resource.id,
                fileUrl = resource.fileUrl,
                isVideo = true,
                subjectColor = subjectColor,
                title = resource.title,
                onFullscreenClick = onFullscreenClick,
                viewModel = mediaViewModel,
                fullWidth = true
            )
        }

        item(key = "video_title") {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Text(
                        text = "${resource.viewCount} views",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        "·",
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                    )
                    Text(
                        text = formatTimeAgo(resource.addedAt),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }

        item(key = "video_author") {
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                val uploadUsername = resource.uploadedByUsername.ifBlank { resource.authorName.orEmpty() }
                val authorLabel = uploadUsername.ifBlank { resource.authorName ?: "NEBians Team" }
                val isSelf = uploadUsername.isNotBlank() && uploadUsername.equals(uiState.currentUsername, ignoreCase = true)

                NebAvatar(
                    name = authorLabel.ifEmpty { "N" },
                    photoUrl = uiState.authorPhotoUrl,
                    size = 40.dp
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = authorLabel,
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    if (uploadUsername.isNotBlank()) {
                        Text(
                            text = "@$uploadUsername",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                if (uploadUsername.isNotBlank() && !isSelf) {
                    TextButton(onClick = { onUserProfileClick(uploadUsername) }) {
                        Text("Follow", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                }
            }
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
        }

        item(key = "video_actions") {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                VideoActionPill(
                    icon = if (uiState.isLiked) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
                    text = uiState.likeCount.toString(),
                    selected = uiState.isLiked,
                    enabled = uiState.isAuthenticated,
                    onClick = viewModel::toggleLike
                )
                VideoActionIcon(
                    icon = if (uiState.isBookmarked) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
                    selected = uiState.isBookmarked,
                    enabled = uiState.isAuthenticated,
                    contentDescription = "Bookmark",
                    onClick = viewModel::toggleBookmark
                )
                VideoActionIcon(
                    icon = Icons.Filled.Share,
                    selected = false,
                    contentDescription = "Share",
                    onClick = { share(resource.title, resource.id) }
                )
                VideoActionIcon(
                    icon = when {
                        uiState.isDownloaded -> Icons.Filled.DownloadDone
                        uiState.downloadProgress != null && uiState.downloadProgress in 0..99 -> Icons.Filled.Downloading
                        else -> Icons.Filled.Download
                    },
                    selected = uiState.isDownloaded,
                    contentDescription = if (uiState.isDownloaded) "Downloaded" else "Download for offline playback",
                    onClick = viewModel::downloadResource
                )
            }
        }

        if (resource.description.isNotBlank()) {
            item(key = "video_desc") {
                ExpandableText(
                    text = resource.description,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 15.sp,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                HorizontalDivider(
                    modifier = Modifier.padding(top = 8.dp),
                    color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
                )
            }
        }

        if (uiState.suggestedVideos.isNotEmpty()) {
            item(key = "up_next_title") {
                Text(
                    "Up next",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)
                )
            }
            items(uiState.suggestedVideos, key = { "up_${it.id}" }) { suggested ->
                UpNextVideoCard(
                    resource = suggested,
                    onClick = { onRelatedResourceClick(suggested.id) },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp)
                )
            }
            item(key = "up_next_divider") {
                HorizontalDivider(
                    modifier = Modifier.padding(top = 10.dp),
                    color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
                )
            }
        }

        item(key = "comments_title") {
            ResourceCommentsHeader(
                count = uiState.comments.size,
                modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 18.dp, bottom = 12.dp)
            )
        }

        when {
            uiState.commentsLoading -> item(key = "comments_loading") { ResourceCommentsLoading() }
            uiState.comments.isEmpty() -> item(key = "comments_empty") { ResourceEmptyComments() }
            else -> items(uiState.comments, key = { it.id }) { comment ->
                ResourceCommentItem(
                    comment = comment,
                    canDelete = comment.userId == uiState.currentUserId,
                    onDelete = { viewModel.deleteComment(comment.id) },
                    onThumbsUpClick = { viewModel.toggleCommentLike(comment.id) },
                    onAuthorClick = { userName -> onUserProfileClick(userName) },
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
            }
        }
    }
}

@Composable
private fun NonVideoLayout(
    resource: ApiResource,
    mediaType: ResourceMediaType,
    subjectColor: Color,
    uiState: ResourceDetailUiState,
    viewModel: ResourceDetailViewModel,
    onOpenPdf: (resourceId: String, fileUrl: String, title: String) -> Unit,
    onUserProfileClick: (String) -> Unit,
    share: (String, String) -> Unit,
    openExternal: (String) -> Unit,
    padding: PaddingValues,
    onZoomImage: (String) -> Unit
) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(top = padding.calculateTopPadding()),
        contentPadding = PaddingValues(start = 16.dp, top = 4.dp, end = 16.dp, bottom = padding.calculateBottomPadding() + 18.dp)
    ) {
        item(key = "hero") {
            ResourceHeroCard(
                resource = resource,
                isLiked = uiState.isLiked,
                likeCount = uiState.likeCount,
                isBookmarked = uiState.isBookmarked,
                canLike = uiState.isAuthenticated,
                canBookmark = uiState.isAuthenticated,
                onRead = {
                    when (mediaType) {
                        ResourceMediaType.Pdf -> onOpenPdf(resource.id, resource.fileUrl, resource.title)
                        else -> openExternal(resource.fileUrl)
                    }
                },
                onDownload = viewModel::downloadResource,
                onLike = viewModel::toggleLike,
                onBookmark = viewModel::toggleBookmark,
                onShare = { share(resource.title, resource.id) },
                onUserProfileClick = onUserProfileClick
            )
        }

        if (mediaType == ResourceMediaType.Audio) {
            item(key = "embedded_player") {
                EmbeddedMediaPlayer(
                    resourceId = resource.id,
                    fileUrl = resource.fileUrl,
                    isVideo = false,
                    subjectColor = subjectColor,
                    title = resource.title,
                    onFullscreenClick = {},
                    modifier = Modifier.padding(top = 16.dp)
                )
            }
        }

        if (mediaType == ResourceMediaType.Image && resource.fileUrl.isNotBlank()) {
            item(key = "preview") {
                AsyncImage(
                    model = resource.fileUrl,
                    contentDescription = resource.title,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp)
                        .clickable { onZoomImage(resource.fileUrl) }
                )
            }
        }

        item(key = "comments_title") {
            ResourceCommentsHeader(
                count = uiState.comments.size,
                modifier = Modifier.padding(top = 22.dp, bottom = 12.dp)
            )
        }

        when {
            uiState.commentsLoading -> item(key = "comments_loading") { ResourceCommentsLoading() }
            uiState.comments.isEmpty() -> item(key = "comments_empty") { ResourceEmptyComments() }
            else -> items(uiState.comments, key = { it.id }) { comment ->
                ResourceCommentItem(
                    comment = comment,
                    canDelete = comment.userId == uiState.currentUserId,
                    onDelete = { viewModel.deleteComment(comment.id) },
                    onThumbsUpClick = { viewModel.toggleCommentLike(comment.id) },
                    onAuthorClick = { userName -> onUserProfileClick(userName) }
                )
            }
        }
    }
}

private val FS_SPEEDS = listOf(0.5f, 0.75f, 1f, 1.25f, 1.5f, 1.75f, 2f)
private const val FS_SEEK_MS = 10_000L
private enum class FsGestureType { BRIGHTNESS, VOLUME, SEEK }

@Composable
private fun FullscreenVideoOverlay(
    viewModel: MediaPlayerViewModel,
    uiState: MediaPlayerUiState,
    onExit: () -> Unit,
    subjectColor: Color
) {
    val player = viewModel.getPlayer()
    var showControls by remember { mutableStateOf(true) }
    var gestureType by remember { mutableStateOf<FsGestureType?>(null) }
    var gestureDelta by remember { mutableFloatStateOf(0f) }
    var gestureStartBrightness by remember { mutableFloatStateOf(0.5f) }
    var gestureStartVolume by remember { mutableFloatStateOf(0.5f) }
    var gestureStartPosition by remember { mutableLongStateOf(0L) }
    var gestureSeekPosition by remember { mutableLongStateOf(0L) }
    var seekBadge by remember { mutableStateOf<Int?>(null) }
    var seekBadgeVisible by remember { mutableStateOf(false) }
    var screenWidth by remember { mutableFloatStateOf(1f) }
    var speedExpanded by remember { mutableStateOf(false) }
    val activity = LocalContext.current as? android.app.Activity

    val aspectRatio = if (uiState.videoWidth > 0 && uiState.videoHeight > 0) {
        uiState.videoWidth.toFloat() / uiState.videoHeight.toFloat()
    } else {
        16f / 9f
    }

    val progress by remember(uiState.currentTimeMs, uiState.durationMs) {
        derivedStateOf {
            if (uiState.durationMs > 0) (uiState.currentTimeMs.toFloat() / uiState.durationMs).coerceIn(0f, 1f) else 0f
        }
    }
    val remainingMs = (uiState.durationMs - uiState.currentTimeMs).coerceAtLeast(0L)

    LaunchedEffect(showControls, uiState.isPlaying) {
        if (showControls && uiState.isPlaying) {
            delay(4000L)
            showControls = false
        }
    }
    LaunchedEffect(uiState.isPlaying) {
        if (!uiState.isPlaying) showControls = true
    }
    LaunchedEffect(seekBadgeVisible) {
        if (seekBadgeVisible) { delay(700L); seekBadgeVisible = false }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
            .onSizeChanged { screenWidth = it.width.toFloat() }
            .pointerInput(Unit) {
                detectTapGestures(
                    onTap = { showControls = !showControls },
                    onDoubleTap = { offset ->
                        val delta = if (offset.x < screenWidth / 2f) -10_000L else 10_000L
                        viewModel.seekBy(delta)
                        seekBadge = if (delta < 0) -10 else 10
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
                        gestureStartVolume = viewModel.getVolumeFraction()
                        gestureDelta = 0f
                        gestureType = when {
                            abs(offset.x - screenWidth / 2) < screenWidth * 0.15f -> FsGestureType.SEEK
                            offset.x < screenWidth / 2 -> FsGestureType.BRIGHTNESS
                            else -> FsGestureType.VOLUME
                        }
                    },
                    onDrag = { change, dragAmount ->
                        change.consume()
                        val totalHeight = size.height.toFloat().coerceAtLeast(1f)
                        when (gestureType) {
                            FsGestureType.SEEK -> {
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
                            FsGestureType.BRIGHTNESS -> {
                                gestureDelta += -dragAmount.y / totalHeight
                                val frac = (gestureStartBrightness + gestureDelta).coerceIn(0f, 1f)
                                val lp = activity?.window?.attributes
                                if (lp != null) { lp.screenBrightness = frac; activity?.window?.attributes = lp }
                            }
                            FsGestureType.VOLUME -> {
                                gestureDelta += -dragAmount.y / totalHeight
                                val frac = (gestureStartVolume + gestureDelta).coerceIn(0f, 1f)
                                viewModel.setVolumeFraction(frac)
                            }
                            null -> {}
                        }
                    },
                    onDragEnd = { gestureType = null; gestureDelta = 0f },
                    onDragCancel = { gestureType = null; gestureDelta = 0f }
                )
            },
        contentAlignment = Alignment.Center
    ) {
        AndroidView(
            factory = { ctx -> android.view.SurfaceView(ctx) },
            update = { sv -> player?.setVideoSurfaceView(sv) },
            modifier = Modifier.aspectRatio(aspectRatio).align(Alignment.Center)
        )

        if (uiState.isBuffering) {
            CircularProgressIndicator(
                color = Color.White, strokeWidth = 2.5.dp,
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
                // Gradient overlays
                Box(Modifier.fillMaxWidth().height(140.dp).align(Alignment.TopCenter)
                    .background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.75f), Color.Transparent))))
                Box(Modifier.fillMaxWidth().height(180.dp).align(Alignment.BottomCenter)
                    .background(Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.85f)))))

                // Top bar: back + title
                Row(
                    Modifier.align(Alignment.TopStart).statusBarsPadding()
                        .padding(horizontal = 4.dp, vertical = 4.dp).fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = onExit) {
                        Icon(Icons.Default.ArrowBack, "Back", tint = Color.White)
                    }
                    Text(
                        text = uiState.title,
                        color = Color.White, fontWeight = FontWeight.SemiBold,
                        fontSize = 14.sp, maxLines = 2, overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f)
                    )
                    FullscreenOrientationControls(activity = activity)
                }

                // Center play/pause
                Row(
                    Modifier.align(Alignment.Center),
                    horizontalArrangement = Arrangement.spacedBy(28.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = { viewModel.seekBy(-FS_SEEK_MS); showControls = true }, modifier = Modifier.size(48.dp)) {
                        Icon(Icons.Filled.Replay10, "Rewind 10s", tint = Color.White, modifier = Modifier.size(28.dp))
                    }
                    IconButton(
                        onClick = { viewModel.togglePlay(); showControls = true },
                        modifier = Modifier.size(68.dp)
                            .background(Color.White.copy(alpha = 0.15f), CircleShape)
                            .border(1.5.dp, Color.White.copy(alpha = 0.3f), CircleShape)
                    ) {
                        Icon(
                            imageVector = if (uiState.isPlaying) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                            contentDescription = if (uiState.isPlaying) "Pause" else "Play",
                            tint = Color.White, modifier = Modifier.size(38.dp)
                        )
                    }
                    IconButton(onClick = { viewModel.seekBy(FS_SEEK_MS); showControls = true }, modifier = Modifier.size(48.dp)) {
                        Icon(Icons.Filled.Forward10, "Forward 10s", tint = Color.White, modifier = Modifier.size(28.dp))
                    }
                }

                // Bottom bar: progress + time + speed + exit
                Column(
                    Modifier.align(Alignment.BottomCenter).navigationBarsPadding()
                        .fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    FsProgressBar(
                        currentMs = uiState.currentTimeMs,
                        durationMs = uiState.durationMs,
                        bufferedPercent = uiState.bufferedPercent,
                        subjectColor = subjectColor,
                        onSeek = { viewModel.seekToRatio(it); showControls = true }
                    )
                    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = fmtTime(uiState.currentTimeMs),
                            color = Color.White, fontSize = 12.sp,
                            fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Medium
                        )
                        Text(
                            text = " / -${fmtTime(remainingMs)}",
                            color = Color.White.copy(alpha = 0.55f), fontSize = 12.sp,
                            fontFamily = FontFamily.Monospace
                        )
                        Spacer(Modifier.weight(1f))
                        FsSpeedSelector(
                            speedExpanded = speedExpanded,
                            currentSpeed = uiState.speed,
                            subjectColor = subjectColor,
                            onToggle = { speedExpanded = !speedExpanded; showControls = true },
                            onSelect = { viewModel.setSpeed(it); speedExpanded = false; showControls = true }
                        )
                        Spacer(Modifier.width(8.dp))
                        IconButton(onClick = { onExit() }, modifier = Modifier.size(36.dp)) {
                            Icon(Icons.Filled.FullscreenExit, "Exit Fullscreen", tint = Color.White, modifier = Modifier.size(22.dp))
                        }
                    }
                }
            }
        }

        // Seek badge
        AnimatedVisibility(
            visible = seekBadgeVisible,
            enter = fadeIn(tween(120)), exit = fadeOut(tween(350)),
            modifier = Modifier.align(if ((seekBadge ?: 0) < 0) Alignment.CenterStart else Alignment.CenterEnd)
        ) {
            Box(
                Modifier.padding(horizontal = 32.dp)
                    .background(Color.Black.copy(alpha = 0.55f), RoundedCornerShape(10.dp))
                    .padding(horizontal = 16.dp, vertical = 10.dp)
            ) {
                Text(
                    text = if ((seekBadge ?: 0) < 0) "−10s" else "+10s",
                    color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp
                )
            }
        }

        // Gesture indicator
        if (gestureType != null) {
            val icon = when (gestureType) {
                FsGestureType.BRIGHTNESS -> Icons.Filled.BrightnessMedium
                FsGestureType.VOLUME -> Icons.Filled.VolumeUp
                FsGestureType.SEEK -> Icons.Filled.FastForward
                null -> null
            }
            val label = when (gestureType) {
                FsGestureType.BRIGHTNESS -> "${((gestureStartBrightness + gestureDelta).coerceIn(0f, 1f) * 100).toInt()}%"
                FsGestureType.VOLUME -> "${((gestureStartVolume + gestureDelta).coerceIn(0f, 1f) * 100).toInt()}%"
                FsGestureType.SEEK -> fmtTime(gestureSeekPosition)
                null -> ""
            }
            Box(
                Modifier.align(Alignment.Center)
                    .background(Color.Black.copy(alpha = 0.65f), RoundedCornerShape(14.dp))
                    .padding(horizontal = 20.dp, vertical = 14.dp)
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    icon?.let { Icon(it, null, tint = Color.White, modifier = Modifier.size(28.dp)) }
                    Text(text = label, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
private fun FsSpeedSelector(
    speedExpanded: Boolean,
    currentSpeed: Float,
    subjectColor: Color,
    onToggle: () -> Unit,
    onSelect: (Float) -> Unit,
) {
    Box {
        Button(
            onClick = onToggle,
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
                text = if (currentSpeed == 1f) "1×" else "${currentSpeed}×",
                fontWeight = FontWeight.Bold, fontSize = 12.sp
            )
        }
        AnimatedVisibility(
            visible = speedExpanded,
            enter = fadeIn() + slideInVertically(initialOffsetY = { it / 2 }),
            exit = fadeOut(),
            modifier = Modifier.align(Alignment.BottomEnd).padding(bottom = 36.dp)
        ) {
            Column(
                Modifier.width(100.dp).clip(RoundedCornerShape(10.dp))
                    .background(Color(0xFF1E1E1E)).border(1.dp, Color.White.copy(alpha = 0.12f), RoundedCornerShape(10.dp))
                    .padding(4.dp)
            ) {
                FS_SPEEDS.forEach { s ->
                    val isActive = s == currentSpeed
                    Text(
                        text = if (s == 1f) "Normal" else "${s}×",
                        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(6.dp))
                            .then(if (isActive) Modifier.background(subjectColor.copy(alpha = 0.20f)) else Modifier)
                            .clickable { onSelect(s) }
                            .padding(horizontal = 12.dp, vertical = 9.dp),
                        color = if (isActive) subjectColor else Color.White.copy(alpha = 0.85f),
                        fontWeight = FontWeight.SemiBold, fontSize = 13.sp
                    )
                }
            }
        }
    }
}

@Composable
private fun FsProgressBar(
    currentMs: Long, durationMs: Long, bufferedPercent: Int,
    subjectColor: Color, onSeek: (Float) -> Unit
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
        animationSpec = tween(150), label = "fsThumb"
    )

    Box(
        modifier = Modifier.fillMaxWidth().height(28.dp)
            .pointerInput(barWidth) { detectTapGestures { offset -> val w = barWidth.coerceAtLeast(1).toFloat(); onSeek((offset.x / w).coerceIn(0f, 1f)) } }
            .pointerInput(barWidth) {
                detectDragGestures(
                    onDragStart = { offset -> isDragging = true; val w = barWidth.coerceAtLeast(1).toFloat(); onSeek((offset.x / w).coerceIn(0f, 1f)) },
                    onDrag = { change, _ -> change.consume(); val w = barWidth.coerceAtLeast(1).toFloat(); onSeek((change.position.x / w).coerceIn(0f, 1f)) },
                    onDragEnd = { isDragging = false }, onDragCancel = { isDragging = false }
                )
            }
            .onSizeChanged { barWidth = it.width },
        contentAlignment = Alignment.CenterStart
    ) {
        Box(Modifier.fillMaxWidth().height(3.dp).clip(RoundedCornerShape(2.dp)).background(Color.White.copy(alpha = 0.25f))) {
            Box(Modifier.fillMaxHeight().fillMaxWidth((bufferedPercent / 100f).coerceIn(0f, 1f)).background(Color.White.copy(alpha = 0.40f)))
            Box(Modifier.fillMaxHeight().fillMaxWidth(progress).background(subjectColor))
        }
        val thumbSizeDp = 14.dp * thumbScale
        Box(
            Modifier.offset { IntOffset(x = ((progress * barWidth) - (thumbSizeDp.toPx() / 2)).toInt().coerceAtLeast(0), y = 0) }
                .size(thumbSizeDp).clip(CircleShape).background(Color.White)
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

@Composable
private fun VideoActionPill(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    text: String,
    selected: Boolean,
    enabled: Boolean,
    onClick: () -> Unit
) {
    val color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(999.dp))
            .border(
                BorderStroke(1.dp, if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant),
                RoundedCornerShape(999.dp)
            )
            .background(
                if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.07f)
                else androidx.compose.ui.graphics.Color.Transparent
            )
            .clickable(enabled = enabled, onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, null, tint = color, modifier = Modifier.size(18.dp))
        Text(text, color = color, fontWeight = FontWeight.Bold, fontSize = 13.sp)
    }
}

@Composable
private fun VideoActionIcon(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    selected: Boolean,
    contentDescription: String,
    enabled: Boolean = true,
    onClick: () -> Unit
) {
    val color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
    Box(
        modifier = Modifier
            .size(38.dp)
            .clip(CircleShape)
            .border(
                BorderStroke(1.dp, if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant),
                CircleShape
            )
            .background(
                if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.07f)
                else androidx.compose.ui.graphics.Color.Transparent
            )
            .clickable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Icon(icon, contentDescription, tint = color, modifier = Modifier.size(20.dp))
    }
}
