package com.neb.ians.ui.screens.forum

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.ConfirmDeleteDialog
import com.neb.ians.ui.components.EditContentDialog
import com.neb.ians.ui.components.EditHistoryDialog
import com.neb.ians.ui.components.LikePill
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.PollView
import com.neb.ians.ui.components.PostMoreMenu
import com.neb.ians.ui.components.ReportDialog
import com.neb.ians.ui.components.UserPopoverDialog
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.resolveMediaUrl
import com.neb.ians.ui.components.sharePost
import com.neb.ians.ui.components.shareText
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ForumPostDetailScreen(
    postId: String,
    onNavigateBack: () -> Unit,
    onReplyClick: (String?) -> Unit,
    onProfileClick: (String) -> Unit = {},
    viewModel: PostDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }

    // Dialog state
    var reportTarget by remember { mutableStateOf<Pair<String, String>?>(null) } // type to id
    var editingPost by remember { mutableStateOf(false) }
    var editingReply by remember { mutableStateOf<ApiReply?>(null) }
    var deletingPost by remember { mutableStateOf(false) }
    var deletingReplyId by remember { mutableStateOf<String?>(null) }
    var historyTarget by remember { mutableStateOf<Pair<String, String>?>(null) }
    var popoverUsername by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(uiState.snackbarMessage) {
        uiState.snackbarMessage?.let { message ->
            snackbarHostState.showSnackbar(message)
            viewModel.consumeSnackbar()
        }
    }

    val openLink: (String) -> Unit = { url ->
        try {
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
        } catch (_: Exception) {
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(text = "Post", maxLines = 1, overflow = TextOverflow.Ellipsis) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { paddingValues ->
        when {
            uiState.isLoading -> Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
            uiState.post == null -> Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "Post not found",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            else -> {
                val post = uiState.post!!
                val isOwnPost = uiState.currentUserId != null && post.authorId == uiState.currentUserId
                val topLevel = uiState.topLevelReplies

                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    contentPadding = PaddingValues(16.dp)
                ) {
                    item(key = "post_header") {
                        PostContentSection(
                            post = post,
                            poll = uiState.poll,
                            isOwnPost = isOwnPost,
                            isVoting = uiState.isVoting,
                            onThumbsUpClick = viewModel::toggleThumbsUp,
                            onBookmarkClick = viewModel::togglePostBookmark,
                            onShareClick = { sharePost(context, post.id) },
                            onReportClick = { reportTarget = "post" to post.id },
                            onEditClick = { editingPost = true },
                            onArchiveClick = viewModel::archivePost,
                            onDeleteClick = { deletingPost = true },
                            onReplyClick = { onReplyClick(null) },
                            onVote = viewModel::votePoll,
                            onEditedClick = { historyTarget = "post" to post.id },
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = post.authorName },
                            onLinkClick = openLink
                        )
                    }

                    item(key = "divider") {
                        HorizontalDivider(
                            modifier = Modifier.padding(vertical = 12.dp),
                            color = MaterialTheme.colorScheme.outlineVariant
                        )
                    }

                    item(key = "replies_header") {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "${uiState.replies.size} ${if (uiState.replies.size == 1) "Reply" else "Replies"}",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.weight(1f)
                            )
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        // Reply sort pills: Oldest / Newest / Top
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            ReplySortPill("Oldest", "oldest", uiState.replySort, viewModel::setReplySort)
                            ReplySortPill("Newest", "newest", uiState.replySort, viewModel::setReplySort)
                            ReplySortPill("Top", "top", uiState.replySort, viewModel::setReplySort)
                        }
                        Spacer(modifier = Modifier.height(12.dp))
                    }

                    if (uiState.replies.isEmpty()) {
                        item(key = "no_replies") {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 32.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "No replies yet. Be the first to reply!",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }

                    items(topLevel, key = { it.id }) { reply ->
                        val children = uiState.childrenOf(reply.id)
                        Column {
                            ReplyItem(
                                reply = reply,
                                isOwn = uiState.currentUserId != null && reply.authorId == uiState.currentUserId,
                                onThumbsUpClick = { viewModel.toggleReplyThumbsUp(reply.id) },
                                onReplyClick = { onReplyClick(reply.id) },
                                onBookmarkClick = { viewModel.toggleReplyBookmark(reply.id) },
                                onShareClick = {
                                    shareText(context, "https://nebians.consica.com.np/forum/post/$postId/")
                                },
                                onReportClick = { reportTarget = "reply" to reply.id },
                                onEditClick = { editingReply = reply },
                                onArchiveClick = { viewModel.archiveReply(reply.id) },
                                onDeleteClick = { deletingReplyId = reply.id },
                                onEditedClick = { historyTarget = "reply" to reply.id },
                                onProfileClick = onProfileClick,
                                onAuthorLongPress = { popoverUsername = reply.authorName },
                                onLinkClick = openLink
                            )
                            if (children.isNotEmpty()) {
                                Row(
                                    modifier = Modifier
                                        .padding(start = 24.dp, top = 8.dp)
                                        .height(IntrinsicSize.Min)
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .width(2.dp)
                                            .fillMaxHeight()
                                            .background(MaterialTheme.colorScheme.outlineVariant)
                                    )
                                    Column(
                                        modifier = Modifier
                                            .padding(start = 10.dp)
                                            .weight(1f),
                                        verticalArrangement = Arrangement.spacedBy(8.dp)
                                    ) {
                                        children.forEach { child ->
                                            ReplyItem(
                                                reply = child,
                                                isOwn = uiState.currentUserId != null && child.authorId == uiState.currentUserId,
                                                onThumbsUpClick = { viewModel.toggleReplyThumbsUp(child.id) },
                                                onReplyClick = { onReplyClick(reply.id) },
                                                onBookmarkClick = { viewModel.toggleReplyBookmark(child.id) },
                                                onShareClick = {
                                                    shareText(context, "https://nebians.consica.com.np/forum/post/$postId/")
                                                },
                                                onReportClick = { reportTarget = "reply" to child.id },
                                                onEditClick = { editingReply = child },
                                                onArchiveClick = { viewModel.archiveReply(child.id) },
                                                onDeleteClick = { deletingReplyId = child.id },
                                                onEditedClick = { historyTarget = "reply" to child.id },
                                                onProfileClick = onProfileClick,
                                                onAuthorLongPress = { popoverUsername = child.authorName },
                                                onLinkClick = openLink
                                            )
                                        }
                                    }
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                    }

                    item(key = "bottom_spacer") {
                        Spacer(modifier = Modifier.height(72.dp))
                    }
                }
            }
        }
    }

    // ----- Dialogs -----
    reportTarget?.let { (type, id) ->
        ReportDialog(
            onDismiss = { reportTarget = null },
            onSubmit = { reason, description ->
                viewModel.report(type, id, reason, description)
                reportTarget = null
            }
        )
    }

    if (editingPost) {
        uiState.post?.let { post ->
            EditContentDialog(
                dialogTitle = "Edit post",
                initialTitle = post.title,
                initialContent = post.content,
                onDismiss = { editingPost = false },
                onSave = { title, content ->
                    viewModel.editPost(title ?: post.title, content)
                    editingPost = false
                }
            )
        }
    }

    editingReply?.let { reply ->
        EditContentDialog(
            dialogTitle = "Edit reply",
            initialTitle = null,
            initialContent = reply.content,
            onDismiss = { editingReply = null },
            onSave = { _, content ->
                viewModel.editReply(reply.id, content)
                editingReply = null
            }
        )
    }

    if (deletingPost) {
        ConfirmDeleteDialog(
            message = "Delete post? This cannot be undone.",
            onDismiss = { deletingPost = false },
            onConfirm = {
                deletingPost = false
                viewModel.deletePost(onDeleted = onNavigateBack)
            }
        )
    }

    deletingReplyId?.let { replyId ->
        ConfirmDeleteDialog(
            message = "Delete reply? This cannot be undone.",
            onDismiss = { deletingReplyId = null },
            onConfirm = {
                viewModel.deleteReply(replyId)
                deletingReplyId = null
            }
        )
    }

    historyTarget?.let { (type, id) ->
        EditHistoryDialog(
            targetType = type,
            targetId = id,
            onDismiss = { historyTarget = null }
        )
    }

    popoverUsername?.let { username ->
        UserPopoverDialog(
            username = username,
            onDismiss = { popoverUsername = null },
            onViewProfile = { profileUsername ->
                popoverUsername = null
                onProfileClick(profileUsername)
            }
        )
    }
}

@Composable
private fun ReplySortPill(
    label: String,
    value: String,
    currentSort: String,
    onSelect: (String) -> Unit
) {
    val selected = currentSort == value
    Surface(
        shape = WebPillShape,
        color = if (selected) MaterialTheme.colorScheme.secondaryContainer
        else MaterialTheme.colorScheme.surfaceContainerLow,
        modifier = Modifier.clip(WebPillShape).clickable { onSelect(value) }
    ) {
        Text(
            text = label,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
            color = if (selected) MaterialTheme.colorScheme.onSecondaryContainer
            else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun PostContentSection(
    post: ApiPost,
    poll: com.neb.ians.ui.components.PollUi?,
    isOwnPost: Boolean,
    isVoting: Boolean,
    onThumbsUpClick: () -> Unit,
    onBookmarkClick: () -> Unit,
    onShareClick: () -> Unit,
    onReportClick: () -> Unit,
    onEditClick: () -> Unit,
    onArchiveClick: () -> Unit,
    onDeleteClick: () -> Unit,
    onReplyClick: () -> Unit,
    onVote: (List<String>) -> Unit,
    onEditedClick: () -> Unit,
    onProfileClick: (String) -> Unit,
    onAuthorLongPress: () -> Unit,
    onLinkClick: (String) -> Unit
) {
    val category = post.category.ifBlank { "General" }
    val categoryTheme = getSubjectTheme(category)
    val bookmarked = post.isBookmarked == true

    Column {
        // ----- Meta row -----
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Box(
                modifier = Modifier.combinedClickable(
                    onClick = { onProfileClick(post.authorName) },
                    onLongClick = onAuthorLongPress
                )
            ) {
                Avatar(name = post.authorName, imageUrl = post.authorPhotoUrl, size = 38.dp)
            }
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = post.authorName,
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier
                            .weight(1f, fill = false)
                            .combinedClickable(
                                onClick = { onProfileClick(post.authorName) },
                                onLongClick = onAuthorLongPress
                            )
                    )
                    post.authorBadgeInfo?.let { badge ->
                        Spacer(modifier = Modifier.width(5.dp))
                        NebBadge(badge)
                    }
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(shape = WebPillShape, color = categoryTheme.container) {
                        Text(
                            text = category,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = FontWeight.Bold,
                            color = categoryTheme.onContainer
                        )
                    }
                    Text(
                        text = " · ${formatTimeAgo(post.createdAt)}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    if (post.isEdited == true) {
                        Text(
                            text = " · edited",
                            style = MaterialTheme.typography.labelSmall.copy(textDecoration = TextDecoration.Underline),
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.clickable(onClick = onEditedClick)
                        )
                    }
                }
            }
            if (post.isArchived == true) {
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.surfaceContainerHigh) {
                    Text(
                        text = "Archived",
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = post.title,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )

        Spacer(modifier = Modifier.height(8.dp))

        MarkdownText(
            markdown = post.content,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurface,
            onMentionClick = onProfileClick,
            onLinkClick = onLinkClick
        )

        // ----- Full-width images -----
        if (post.images.isNotEmpty()) {
            Spacer(modifier = Modifier.height(12.dp))
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                post.images.sortedBy { it.order }.forEach { image ->
                    AsyncImage(
                        model = resolveMediaUrl(image.imageUrl),
                        contentDescription = null,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp)),
                        contentScale = ContentScale.FillWidth
                    )
                }
            }
        }

        // ----- Poll -----
        poll?.let {
            Spacer(modifier = Modifier.height(12.dp))
            PollView(poll = it, isVoting = isVoting, onVote = onVote)
        }

        Spacer(modifier = Modifier.height(14.dp))

        // ----- Action row -----
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            LikePill(
                count = post.thumbsUpCount,
                liked = post.isThumbedUp,
                onClick = onThumbsUpClick
            )
            Row(
                modifier = Modifier
                    .clip(WebPillShape)
                    .clickable(onClick = onReplyClick)
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(5.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.ChatBubbleOutline,
                    contentDescription = "Reply",
                    modifier = Modifier.size(15.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "${post.replyCount} Replies",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Spacer(modifier = Modifier.weight(1f))
            IconButton(onClick = onBookmarkClick, modifier = Modifier.size(36.dp)) {
                Icon(
                    imageVector = if (bookmarked) Icons.Filled.Bookmark else Icons.Filled.BookmarkBorder,
                    contentDescription = if (bookmarked) "Remove bookmark" else "Bookmark",
                    modifier = Modifier.size(20.dp),
                    tint = if (bookmarked) MaterialTheme.colorScheme.primary
                    else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            IconButton(onClick = onShareClick, modifier = Modifier.size(36.dp)) {
                Icon(
                    imageVector = Icons.Outlined.Share,
                    contentDescription = "Share",
                    modifier = Modifier.size(20.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            PostMoreMenu(
                isOwn = isOwnPost,
                isBookmarked = bookmarked,
                isArchived = post.isArchived == true,
                onBookmark = onBookmarkClick,
                onShare = onShareClick,
                onReport = onReportClick,
                onEdit = onEditClick,
                onArchive = onArchiveClick,
                onDelete = onDeleteClick
            )
        }
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun ReplyItem(
    reply: ApiReply,
    isOwn: Boolean,
    onThumbsUpClick: () -> Unit,
    onReplyClick: () -> Unit,
    onBookmarkClick: () -> Unit,
    onShareClick: () -> Unit,
    onReportClick: () -> Unit,
    onEditClick: () -> Unit,
    onArchiveClick: () -> Unit,
    onDeleteClick: () -> Unit,
    onEditedClick: () -> Unit,
    onProfileClick: (String) -> Unit,
    onAuthorLongPress: () -> Unit,
    onLinkClick: (String) -> Unit
) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Box(
                    modifier = Modifier.combinedClickable(
                        onClick = { onProfileClick(reply.authorName) },
                        onLongClick = onAuthorLongPress
                    )
                ) {
                    Avatar(name = reply.authorName, imageUrl = reply.authorPhotoUrl, size = 28.dp)
                }
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = reply.authorName,
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier
                                .weight(1f, fill = false)
                                .combinedClickable(
                                    onClick = { onProfileClick(reply.authorName) },
                                    onLongClick = onAuthorLongPress
                                )
                        )
                        reply.authorBadgeInfo?.let { badge ->
                            Spacer(modifier = Modifier.width(5.dp))
                            NebBadge(badge)
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = formatTimeAgo(reply.createdAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        if (reply.isEdited == true) {
                            Text(
                                text = " · edited",
                                style = MaterialTheme.typography.labelSmall.copy(textDecoration = TextDecoration.Underline),
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.clickable(onClick = onEditedClick)
                            )
                        }
                        if (reply.isArchived == true) {
                            Text(
                                text = " · archived",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
                PostMoreMenu(
                    isOwn = isOwn,
                    isBookmarked = reply.isBookmarked == true,
                    isArchived = reply.isArchived == true,
                    onBookmark = onBookmarkClick,
                    onShare = onShareClick,
                    onReport = onReportClick,
                    onEdit = onEditClick,
                    onArchive = onArchiveClick,
                    onDelete = onDeleteClick
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            MarkdownText(
                markdown = reply.content,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                onMentionClick = onProfileClick,
                onLinkClick = onLinkClick
            )

            Spacer(modifier = Modifier.height(8.dp))

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                LikePill(
                    count = reply.thumbsUpCount,
                    liked = reply.isThumbedUp,
                    onClick = onThumbsUpClick
                )
                Row(
                    modifier = Modifier
                        .clip(WebPillShape)
                        .clickable(onClick = onReplyClick)
                        .padding(horizontal = 8.dp, vertical = 5.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.ChatBubbleOutline,
                        contentDescription = "Reply",
                        modifier = Modifier.size(14.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = "Reply",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
