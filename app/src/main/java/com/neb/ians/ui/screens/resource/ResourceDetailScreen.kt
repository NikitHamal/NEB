package com.neb.ians.ui.screens.resource

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.ui.graphics.Color
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.ZoomableImageDialog

@Composable
fun ResourceDetailScreen(
    onNavigateBack: () -> Unit,
    onOpenPdf: (resourceId: String, fileUrl: String, title: String) -> Unit,
    onOpenMedia: (resourceId: String) -> Unit = {},
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
                title = "Resource",
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
                val subjectColor = Color(
                    com.neb.ians.util.getSubjectColor(
                        resource.subject.split(",").firstOrNull()?.trim().orEmpty().ifBlank { "General" }
                    )
                )
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
                                    ResourceMediaType.Video, ResourceMediaType.Audio -> onOpenMedia(resource.id)
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

                    if (mediaType == ResourceMediaType.Video || mediaType == ResourceMediaType.Audio) {
                        item(key = "embedded_player") {
                            EmbeddedMediaPlayer(
                                resourceId = resource.id,
                                fileUrl = resource.fileUrl,
                                isVideo = mediaType == ResourceMediaType.Video,
                                subjectColor = subjectColor,
                                title = resource.title,
                                onFullscreenClick = { onOpenMedia(resource.id) },
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
                                    .clickable { zoomImageUrl = resource.fileUrl }
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
