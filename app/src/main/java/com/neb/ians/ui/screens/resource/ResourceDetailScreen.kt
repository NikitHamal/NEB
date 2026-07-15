package com.neb.ians.ui.screens.resource

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
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
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.ExpandableText
import com.neb.ians.ui.components.NebAvatar
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.ZoomableImageDialog
import com.neb.ians.util.formatTimeAgo

@Composable
fun ResourceDetailScreen(
    onNavigateBack: () -> Unit,
    onOpenPdf: (resourceId: String, fileUrl: String, title: String) -> Unit,
    onOpenMedia: (resourceId: String, startFullscreen: Boolean) -> Unit = { _, _ -> },
    onUserProfileClick: (String) -> Unit = {},
    viewModel: ResourceDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    var zoomImageUrl by remember { mutableStateOf<String?>(null) }

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

    LaunchedEffect(uiState.snackbarMessage) {
        uiState.snackbarMessage?.let { message ->
            snackbarHostState.showSnackbar(message)
            viewModel.consumeSnackbar()
        }
    }

    Scaffold(
        topBar = {
            NebTopBar(
                showBrand = false,
                title = if (uiState.resource != null && detectResourceMedia(uiState.resource!!.fileUrl, uiState.resource!!.type) == ResourceMediaType.Video) "Video" else "Resource",
                onBack = onNavigateBack
            )
        },
        bottomBar = {
            if (uiState.resource != null) {
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
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
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
                        onOpenMedia = onOpenMedia,
                        onUserProfileClick = onUserProfileClick,
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
                        onOpenMedia = onOpenMedia,
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

    zoomImageUrl?.let { url ->
        ZoomableImageDialog(
            imageUrl = url,
            contentDescription = uiState.resource?.title,
            onDismiss = { zoomImageUrl = null }
        )
    }

}

@Composable
private fun VideoYouTubeLayout(
    resource: ApiResource,
    subjectColor: Color,
    uiState: ResourceDetailUiState,
    viewModel: ResourceDetailViewModel,
    onOpenMedia: (String, Boolean) -> Unit,
    onUserProfileClick: (String) -> Unit,
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
                onFullscreenClick = { onOpenMedia(resource.id, true) },
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
                    photoUrl = null,
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
                    icon = Icons.Filled.Download,
                    selected = false,
                    contentDescription = "Download",
                    onClick = { openExternal(resource.fileUrl) }
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
    onOpenMedia: (resourceId: String, startFullscreen: Boolean) -> Unit,
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
                        ResourceMediaType.Video, ResourceMediaType.Audio -> onOpenMedia(resource.id, false)
                        else -> openExternal(resource.fileUrl)
                    }
                },
                onDownload = { openExternal(resource.fileUrl) },
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
                    onFullscreenClick = { onOpenMedia(resource.id, true) },
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
