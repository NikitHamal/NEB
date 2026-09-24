package com.neb.ians.ui.screens.news

import android.content.Intent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.news.NewsComment
import com.neb.ians.data.news.toSafeColor
import com.neb.ians.ui.components.CommentCard
import com.neb.ians.ui.components.CommentSortPillsRow
import com.neb.ians.ui.components.ConfirmDeleteDialog
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.ShimmerCard
import com.neb.ians.ui.components.ShimmerCircle
import com.neb.ians.ui.components.ShimmerLine
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.screens.home.NewsCategoryBadge
import com.neb.ians.ui.screens.home.newsIcon
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewsDetailScreen(
    slug: String,
    onNavigateBack: () -> Unit,
    onRelatedNewsClick: (String) -> Unit = {},
    viewModel: NewsDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    var activeThreadParentId by remember { mutableStateOf<String?>(null) }
    var activeThreadTargetId by remember { mutableStateOf<String?>(null) }
    var deletingCommentId by remember { mutableStateOf<String?>(null) }
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(uiState.snackbarMessage) {
        val message = uiState.snackbarMessage ?: return@LaunchedEffect
        snackbarHostState.showSnackbar(message)
        viewModel.consumeSnackbar()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = uiState.detail?.announcement?.categoryLabel ?: "Blog",
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    uiState.detail?.let { detail ->
                        IconButton(onClick = { shareArticle(context, detail.announcement) }) {
                            Icon(Icons.Filled.Share, contentDescription = "Share article")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                )
            )
        },
        bottomBar = {
            if (uiState.detail != null && !uiState.isLoading) {
                NebCommentComposerBar(
                    value = uiState.commentDraft,
                    onValueChange = viewModel::onCommentDraftChange,
                    placeholder = if (uiState.isAuthenticated) "Join the discussion" else "Sign in to comment",
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
    ) { innerPadding ->
        when {
            uiState.isLoading -> {
                NewsDetailSkeleton(modifier = Modifier.padding(innerPadding))
            }
            uiState.error != null -> {
                ErrorCard(
                    message = uiState.error ?: "Couldn't load blog post",
                    onRetry = viewModel::retry,
                    modifier = Modifier
                        .padding(innerPadding)
                        .padding(16.dp)
                )
            }
            uiState.detail != null -> {
                val detail = uiState.detail!!
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding)
                        .verticalScroll(rememberScrollState())
                ) {
                    NewsArticleHeader(item = detail.announcement)

                    if (detail.announcement.coverImageUrl.isNotBlank()) {
                        AsyncImage(
                            model = detail.announcement.coverImageUrl,
                            contentDescription = detail.announcement.title,
                            modifier = Modifier
                                .padding(horizontal = 20.dp)
                                .fillMaxWidth()
                                .aspectRatio(16f / 10f)
                                .clip(RoundedCornerShape(18.dp)),
                            contentScale = ContentScale.Crop
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                    }

                    MarkdownText(
                        markdown = detail.content.ifBlank { detail.announcement.summary.ifBlank { detail.announcement.title } },
                        modifier = Modifier.padding(horizontal = 20.dp),
                        style = MaterialTheme.typography.bodyLarge.copy(lineHeight = 30.sp),
                        onLinkClick = { url -> safeOpenUri(uriHandler, context, url) }
                    )

                    if (detail.externalUrl.isNotBlank()) {
                        Spacer(modifier = Modifier.height(24.dp))
                        NebButton(
                            text = "Read the original",
                            onClick = { safeOpenUri(uriHandler, context, detail.externalUrl) },
                            modifier = Modifier.padding(horizontal = 20.dp),
                            icon = Icons.Filled.OpenInNew,
                            tone = NebButtonTone.Outlined,
                            fillWidth = true
                        )
                    }

                    Spacer(modifier = Modifier.height(32.dp))
                    HorizontalDivider(
                        color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f),
                        modifier = Modifier.padding(horizontal = 20.dp)
                    )
                    Spacer(modifier = Modifier.height(24.dp))

                    NewsCommentsSection(
                        uiState = uiState,
                        onLikeClick = viewModel::toggleCommentLike,
                        onSortSelect = viewModel::setCommentSort,
                        onReplyClick = { comment ->
                            activeThreadParentId = comment.id
                            activeThreadTargetId = comment.id
                            val tag = "@${comment.authorName} "
                            if (!uiState.threadDraft.startsWith(tag)) {
                                viewModel.onThreadDraftChange(tag + uiState.threadDraft.removePrefix(tag))
                            }
                        },
                        onOpenThread = { comment -> activeThreadParentId = comment.id },
                        onDeleteClick = { comment -> deletingCommentId = comment.id },
                        onLinkClick = { url -> safeOpenUri(uriHandler, context, url) },
                        modifier = Modifier.padding(horizontal = 20.dp)
                    )

                    if (detail.related.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(32.dp))
                        Text(
                            text = "More from the blog",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                            modifier = Modifier.padding(horizontal = 20.dp)
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        detail.related.forEachIndexed { index, related ->
                            NewsIndexRow(
                                item = related,
                                onClick = { onRelatedNewsClick(related.slug) },
                                showDivider = index < detail.related.lastIndex
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                }
            }
        }
    }

    // ----- Comment thread bottom sheet (same system as the forum post viewer) -----
    activeThreadParentId?.let { parentId ->
        val parent = uiState.comments.firstOrNull { it.id == parentId }
        if (parent != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            val threadReplies = uiState.childrenOf(parentId)
            val replyTarget = activeThreadTargetId?.let { targetId ->
                uiState.comments.firstOrNull { it.id == targetId }
            }

            NebModalSheet(
                onDismiss = {
                    activeThreadParentId = null
                    activeThreadTargetId = null
                },
                sheetState = sheetState
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .fillMaxHeight(0.85f)
                        .padding(bottom = 16.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "@${parent.authorName}",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.weight(1f)
                        )
                        if (threadReplies.isNotEmpty()) {
                            Surface(
                                shape = WebPillShape,
                                color = MaterialTheme.colorScheme.primaryContainer,
                                modifier = Modifier.padding(end = 12.dp)
                            ) {
                                Text(
                                    text = "${threadReplies.size} ${if (threadReplies.size == 1) "reply" else "replies"}",
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                                    fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                )
                            }
                        }
                        IconButton(onClick = {
                            activeThreadParentId = null
                            activeThreadTargetId = null
                        }) {
                            Icon(Icons.Default.Close, contentDescription = "Close")
                        }
                    }

                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)

                    LazyColumn(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxWidth(),
                        contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp)
                    ) {
                        item(key = "parent_${parent.id}") {
                            CommentCard(
                                reply = parent.toApiReply(),
                                isOwn = parent.isOwner,
                                onThumbsUpClick = { viewModel.toggleCommentLike(parent.id) },
                                onReplyClick = {
                                    activeThreadTargetId = parent.id
                                    val tag = "@${parent.authorName} "
                                    if (!uiState.threadDraft.startsWith(tag)) {
                                        viewModel.onThreadDraftChange(tag + uiState.threadDraft.removePrefix(tag))
                                    }
                                },
                                onDeleteClick = if (parent.isOwner) ({ deletingCommentId = parent.id }) else null,
                                onProfileClick = {},
                                onAuthorLongPress = {},
                                onLinkClick = { url -> safeOpenUri(uriHandler, context, url) }
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                            Spacer(modifier = Modifier.height(16.dp))
                        }

                        if (threadReplies.isEmpty()) {
                            item(key = "empty_thread") {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 32.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = "No replies yet in this thread.",
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        } else {
                            items(threadReplies, key = { it.id }) { child ->
                                Column(modifier = Modifier.padding(bottom = 12.dp)) {
                                    val parentOfChild = uiState.comments.firstOrNull { it.id == child.parentCommentId }
                                    val replyingTo = if (child.parentCommentId != parentId) {
                                        parentOfChild?.authorName
                                    } else null

                                    CommentCard(
                                        reply = child.toApiReply(),
                                        isOwn = child.isOwner,
                                        onThumbsUpClick = { viewModel.toggleCommentLike(child.id) },
                                        onReplyClick = {
                                            activeThreadTargetId = child.id
                                            val tag = "@${child.authorName} "
                                            if (!uiState.threadDraft.startsWith(tag)) {
                                                viewModel.onThreadDraftChange(tag + uiState.threadDraft.removePrefix(tag))
                                            }
                                        },
                                        onDeleteClick = if (child.isOwner) ({ deletingCommentId = child.id }) else null,
                                        onProfileClick = {},
                                        onAuthorLongPress = {},
                                        onLinkClick = { url -> safeOpenUri(uriHandler, context, url) },
                                        replyingToUsername = replyingTo,
                                        quotedContent = parentOfChild?.text
                                    )
                                }
                            }
                        }
                    }

                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    NebCommentComposerBar(
                        value = uiState.threadDraft,
                        onValueChange = viewModel::onThreadDraftChange,
                        placeholder = if (replyTarget != null) "Reply to @${replyTarget.authorName}..." else "Write a reply...",
                        enabled = !uiState.isPostingComment,
                        canSend = uiState.threadDraft.isNotBlank() && !uiState.isPostingComment,
                        posting = uiState.isPostingComment,
                        onSend = {
                            val targetId = activeThreadTargetId ?: parentId
                            viewModel.postThreadReply(targetId) {
                                activeThreadTargetId = null
                            }
                        }
                    ) {
                        replyTarget?.let { target ->
                            if (target.id != parentId) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(bottom = 8.dp)
                                        .background(
                                            color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                                            shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)
                                        )
                                        .padding(horizontal = 12.dp, vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Close,
                                        contentDescription = "Clear reply target",
                                        modifier = Modifier
                                            .size(16.dp)
                                            .clickable { activeThreadTargetId = null },
                                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(
                                        text = "Replying to @${target.authorName}",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                }
                            }
                        }
                    }
                }
            }
        } else {
            // Parent comment vanished (e.g. deleted): close the sheet.
            SideEffect {
                activeThreadParentId = null
                activeThreadTargetId = null
            }
        }
    }

    deletingCommentId?.let { commentId ->
        ConfirmDeleteDialog(
            message = "Delete this comment? This cannot be undone.",
            onDismiss = { deletingCommentId = null },
            onConfirm = {
                deletingCommentId = null
                viewModel.deleteComment(commentId)
            }
        )
    }
}


/**
 * Standard comment section — identical system to the forum post viewer:
 * header count, Oldest/Newest/Top sort pills, CommentCard list with
 * like / reply / replies-bar that opens the thread bottom sheet.
 */
@Composable
private fun NewsCommentsSection(
    uiState: NewsDetailUiState,
    onLikeClick: (String) -> Unit,
    onSortSelect: (String) -> Unit,
    onReplyClick: (NewsComment) -> Unit,
    onOpenThread: (NewsComment) -> Unit,
    onDeleteClick: (NewsComment) -> Unit,
    onLinkClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        Text(
            text = "${uiState.comments.size} ${if (uiState.comments.size == 1) "Comment" else "Comments"}",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(Modifier.height(10.dp))
        CommentSortPillsRow(
            currentSort = uiState.commentSort,
            onSelect = onSortSelect
        )
        Spacer(Modifier.height(12.dp))
        when {
            uiState.commentsLoading && uiState.comments.isEmpty() -> {
                repeat(3) { NewsCommentSkeleton() }
            }
            uiState.comments.isEmpty() -> {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 26.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Forum,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(24.dp)
                    )
                    Text(
                        text = "No comments yet",
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = "Be the first NEBian to share a thought.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            else -> uiState.topLevelComments.forEach { comment ->
                val children = uiState.childrenOf(comment.id)
                CommentCard(
                    reply = comment.toApiReply(),
                    isOwn = comment.isOwner,
                    onThumbsUpClick = { onLikeClick(comment.id) },
                    onReplyClick = { onReplyClick(comment) },
                    onDeleteClick = if (comment.isOwner) ({ onDeleteClick(comment) }) else null,
                    onProfileClick = {},
                    onAuthorLongPress = {},
                    onLinkClick = onLinkClick,
                    children = children.map { it.toApiReply() },
                    onRepliesBarClick = if (children.isNotEmpty()) ({ onOpenThread(comment) }) else null
                )
                Spacer(Modifier.height(10.dp))
            }
        }
    }
}

private fun shareArticle(context: android.content.Context, item: NewsAnnouncement) {
    val intent = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_SUBJECT, item.title)
        putExtra(Intent.EXTRA_TEXT, item.url)
    }
    context.startActivity(Intent.createChooser(intent, "Share article"))
}

/**
 * The masthead of one article: what kind of piece it is, its headline, its
 * standfirst, and who filed it. Grey line, black headline, rule underneath —
 * the order a reader expects from a page of prose.
 */
@Composable
private fun NewsArticleHeader(item: NewsAnnouncement) {
    val scheme = MaterialTheme.colorScheme
    Column(modifier = Modifier.padding(start = 20.dp, end = 20.dp, top = 8.dp, bottom = 22.dp)) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(5.dp)
        ) {
            if (item.isPinned) {
                Icon(
                    imageVector = Icons.Filled.PushPin,
                    contentDescription = "Pinned",
                    tint = scheme.onSurface,
                    modifier = Modifier.size(12.dp)
                )
            }
            Text(
                text = item.categoryLabel.uppercase(),
                style = MaterialTheme.typography.labelSmall,
                color = scheme.onSurfaceVariant
            )
        }
        Spacer(modifier = Modifier.height(10.dp))
        Text(
            text = item.title,
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.SemiBold,
            color = scheme.onSurface
        )
        if (item.summary.isNotBlank()) {
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = item.summary,
                style = MaterialTheme.typography.bodyLarge.copy(lineHeight = 27.sp),
                color = scheme.onSurfaceVariant
            )
        }
        Spacer(modifier = Modifier.height(18.dp))
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(
                text = item.authorName,
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.Medium,
                color = scheme.onSurface
            )
            Text(
                text = bylineTail(item),
                style = MaterialTheme.typography.labelMedium,
                color = scheme.onSurfaceVariant
            )
        }
        Spacer(modifier = Modifier.height(18.dp))
        HorizontalDivider(color = scheme.outlineVariant.copy(alpha = 0.6f))
    }
}

private fun bylineTail(item: NewsAnnouncement): String = listOf(
    item.publishedAgo.ifBlank { "Latest" },
    if (item.viewCount.isBlank()) "" else "${item.viewCount} views"
).filter { it.isNotBlank() }.joinToString(" · ", prefix = "· ")

/**
 * A comment that has not arrived yet. It used to be two flat grey boxes inside
 * a card, which read as content rather than as absence; the shimmer primitives
 * are what every other list in the app waits with, so the reader waits the
 * same way.
 */
@Composable
private fun NewsCommentSkeleton() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        ShimmerCircle(size = 38.dp)
        Column(modifier = Modifier.weight(1f)) {
            ShimmerLine(widthFraction = 0.34f, height = 10.dp)
            Spacer(modifier = Modifier.height(8.dp))
            ShimmerLine(widthFraction = 0.96f, height = 13.dp)
            Spacer(modifier = Modifier.height(7.dp))
            ShimmerLine(widthFraction = 0.62f, height = 13.dp)
        }
    }
}

@Composable
private fun NewsDetailSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(horizontal = 20.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        ShimmerLine(widthFraction = 0.24f, height = 9.dp)
        ShimmerLine(widthFraction = 0.95f, height = 26.dp)
        ShimmerLine(widthFraction = 0.7f, height = 26.dp)
        Spacer(modifier = Modifier.height(2.dp))
        ShimmerLine(widthFraction = 0.4f, height = 11.dp)
        Spacer(modifier = Modifier.height(6.dp))
        ShimmerCard(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), height = 190.dp)
        Spacer(modifier = Modifier.height(6.dp))
        repeat(7) { index ->
            ShimmerLine(widthFraction = if (index == 6) 0.55f else 1f, height = 14.dp)
        }
    }
}

private fun safeOpenUri(uriHandler: androidx.compose.ui.platform.UriHandler, context: android.content.Context, url: String) {
    if (url.isBlank()) return
    val trimmed = url.trim()
    try {
        val uri = android.net.Uri.parse(trimmed)
        val scheme = uri.scheme?.lowercase() ?: ""
        if (scheme == "http" || scheme == "https") {
            uriHandler.openUri(trimmed)
        } else {
            val intent = Intent(Intent.ACTION_VIEW, uri).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            if (intent.resolveActivity(context.packageManager) != null) {
                context.startActivity(intent)
            } else {
                android.widget.Toast.makeText(context, "No app found to open link", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
    } catch (e: Exception) {
        try {
            android.widget.Toast.makeText(context, "Invalid link", android.widget.Toast.LENGTH_SHORT).show()
        } catch (_: Exception) {}
    }
}
