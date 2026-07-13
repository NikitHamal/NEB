package com.neb.ians.ui.screens.forum

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.Reply
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
import androidx.compose.ui.unit.sp
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.material.icons.filled.Close
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.launch
import androidx.compose.runtime.rememberCoroutineScope
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.ConfirmDeleteDialog
import com.neb.ians.ui.components.EditContentDialog
import com.neb.ians.ui.components.LikePill
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.ExpandableMarkdownText
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.PollView
import com.neb.ians.ui.components.PostMoreMenu
import com.neb.ians.ui.components.ReportDialog
import com.neb.ians.ui.components.UserPopoverDialog
import com.neb.ians.ui.components.ZoomableImageDialog
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.resolveMediaUrl
import com.neb.ians.ui.components.sharePost
import com.neb.ians.ui.components.MentionsVisualTransformation
import com.neb.ians.ui.components.MentionSuggestions
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ForumPostDetailScreen(
    postId: String,
    onNavigateBack: () -> Unit,
    onReplyClick: (String?) -> Unit,
    onEditPostClick: (String) -> Unit = {},
    onProfileClick: (String) -> Unit = {},
    viewModel: PostDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val mainReplyText by viewModel.mainReplyText.collectAsStateWithLifecycle()
    val mainMentionSuggestions by viewModel.mainMentionSuggestions.collectAsStateWithLifecycle()
    val threadReplyText by viewModel.threadReplyText.collectAsStateWithLifecycle()
    val threadMentionSuggestions by viewModel.threadMentionSuggestions.collectAsStateWithLifecycle()
    val isSubmittingReply by viewModel.isSubmittingReply.collectAsStateWithLifecycle()

    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    val mainFocusRequester = remember { FocusRequester() }
    val keyboardController = LocalSoftwareKeyboardController.current
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }

    // Bottom sheet state for thread
    var activeThreadParent by remember { mutableStateOf<ApiReply?>(null) }
    var activeThreadTargetReply by remember { mutableStateOf<ApiReply?>(null) }
    var zoomImageUrl by remember { mutableStateOf<String?>(null) }

    // Dialog state
    var reportTarget by remember { mutableStateOf<Pair<String, String>?>(null) } // type to id
    var editingReply by remember { mutableStateOf<ApiReply?>(null) }
    var deletingPost by remember { mutableStateOf(false) }
    var deletingReplyId by remember { mutableStateOf<String?>(null) }
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
        bottomBar = {
            if (uiState.currentUserId != null && uiState.post != null) {
                NebCommentComposerBar(
                    value = mainReplyText,
                    onValueChange = viewModel::onMainReplyChange,
                    placeholder = "Write a comment...",
                    enabled = !isSubmittingReply,
                    canSend = mainReplyText.text.isNotBlank() && !isSubmittingReply,
                    posting = isSubmittingReply,
                    textFieldModifier = Modifier.focusRequester(mainFocusRequester),
                    visualTransformation = MentionsVisualTransformation(MaterialTheme.colorScheme.primary),
                    onSend = {
                        keyboardController?.hide()
                        viewModel.submitReply(
                            content = mainReplyText.text,
                            parentReplyId = null,
                            onSuccess = {}
                        )
                    }
                ) {
                    if (mainMentionSuggestions.isNotEmpty()) {
                        MentionSuggestions(
                            users = mainMentionSuggestions,
                            onSelect = viewModel::selectMainMention,
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                    }
                }
            }
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

                PullToRefreshBox(
                    isRefreshing = isRefreshing,
                    onRefresh = {
                        scope.launch {
                            isRefreshing = true
                            viewModel.refresh().join()
                            isRefreshing = false
                        }
                    },
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                ) {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize(),
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
                            onEditClick = { onEditPostClick(post.id) },
                            onArchiveClick = viewModel::archivePost,
                            onDeleteClick = { deletingPost = true },
                            onReplyClick = { mainFocusRequester.requestFocus() },
                            onVote = viewModel::votePoll,
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = post.authorName },
                            onLinkClick = openLink,
                            onImageClick = { url -> zoomImageUrl = url }
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
                        ReplyItem(
                            reply = reply,
                            isOwn = uiState.currentUserId != null && reply.authorId == uiState.currentUserId,
                            onThumbsUpClick = { viewModel.toggleReplyThumbsUp(reply.id) },
                            onReplyClick = {
                                activeThreadParent = reply
                                activeThreadTargetReply = reply
                                val tag = "@${reply.authorName} "
                                viewModel.onThreadReplyChange(
                                    androidx.compose.ui.text.input.TextFieldValue(
                                        text = tag,
                                        selection = androidx.compose.ui.text.TextRange(tag.length)
                                    )
                                )
                            },
                            onBookmarkClick = { viewModel.toggleReplyBookmark(reply.id) },
                            onReportClick = { reportTarget = "reply" to reply.id },
                            onEditClick = { editingReply = reply },
                            onArchiveClick = { viewModel.archiveReply(reply.id) },
                            onDeleteClick = { deletingReplyId = reply.id },
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = reply.authorName },
                            onLinkClick = openLink,
                            children = children,
                            onRepliesBarClick = { activeThreadParent = reply }
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                    }

                    item(key = "bottom_spacer") {
                        Spacer(modifier = Modifier.height(72.dp))
                    }
                }
                } // end PullToRefreshBox
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

    // ----- Thread Bottom Sheet -----
    zoomImageUrl?.let { url ->
        ZoomableImageDialog(
            imageUrl = url,
            contentDescription = "Post image",
            onDismiss = { zoomImageUrl = null }
        )
    }

    activeThreadParent?.let { parent ->
        val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
        val threadReplies = uiState.childrenOf(parent.id)

        ModalBottomSheet(
            onDismissRequest = {
                activeThreadParent = null
                activeThreadTargetReply = null
            },
            sheetState = sheetState,
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
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

                    val replyCount = threadReplies.size
                    if (replyCount > 0) {
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = MaterialTheme.colorScheme.primaryContainer,
                            modifier = Modifier.padding(end = 12.dp)
                        ) {
                            Text(
                                text = "$replyCount ${if (replyCount == 1) "reply" else "replies"}",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onPrimaryContainer,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                            )
                        }
                    }

                    IconButton(onClick = { activeThreadParent = null }) {
                        Icon(Icons.Default.Close, contentDescription = "Close")
                    }
                }

                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)

                LazyColumn(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    contentPadding = PaddingValues(16.dp)
                ) {
                    item(key = "parent_${parent.id}") {
                        ReplyItem(
                            reply = parent,
                            isOwn = uiState.currentUserId != null && parent.authorId == uiState.currentUserId,
                            onThumbsUpClick = { viewModel.toggleReplyThumbsUp(parent.id) },
                             onReplyClick = {
                                 activeThreadTargetReply = parent
                                 val currentText = threadReplyText.text
                                 val tag = "@${parent.authorName} "
                                 if (!currentText.startsWith(tag)) {
                                     val newText = tag + currentText.removePrefix(tag)
                                     viewModel.onThreadReplyChange(
                                         androidx.compose.ui.text.input.TextFieldValue(
                                             text = newText,
                                             selection = androidx.compose.ui.text.TextRange(newText.length)
                                         )
                                     )
                                 }
                             },
                            onBookmarkClick = { viewModel.toggleReplyBookmark(parent.id) },
                            onReportClick = { reportTarget = "reply" to parent.id },
                            onEditClick = { editingReply = parent },
                            onArchiveClick = { viewModel.archiveReply(parent.id) },
                            onDeleteClick = { deletingReplyId = parent.id },
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = parent.authorName },
                            onLinkClick = openLink
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
                                val parentOfChild = uiState.replies.firstOrNull { it.id == child.parentReplyId }
                                val replyingTo = if (child.parentReplyId != parent.id) {
                                    parentOfChild?.authorName
                                } else null

                                ReplyItem(
                                    reply = child,
                                    isOwn = uiState.currentUserId != null && child.authorId == uiState.currentUserId,
                                    onThumbsUpClick = { viewModel.toggleReplyThumbsUp(child.id) },
                                     onReplyClick = {
                                         activeThreadTargetReply = child
                                         val currentText = threadReplyText.text
                                         val tag = "@${child.authorName} "
                                         if (!currentText.startsWith(tag)) {
                                             val newText = tag + currentText.removePrefix(tag)
                                             viewModel.onThreadReplyChange(
                                                 androidx.compose.ui.text.input.TextFieldValue(
                                                     text = newText,
                                                     selection = androidx.compose.ui.text.TextRange(newText.length)
                                                 )
                                             )
                                         }
                                     },
                                    onBookmarkClick = { viewModel.toggleReplyBookmark(child.id) },
                                    onReportClick = { reportTarget = "reply" to child.id },
                                    onEditClick = { editingReply = child },
                                    onArchiveClick = { viewModel.archiveReply(child.id) },
                                    onDeleteClick = { deletingReplyId = child.id },
                                    onProfileClick = onProfileClick,
                                    onAuthorLongPress = { popoverUsername = child.authorName },
                                    onLinkClick = openLink,
                                    replyingToUsername = replyingTo,
                                    quotedContent = parentOfChild?.content
                                )
                            }
                        }
                    }
                }

                if (uiState.currentUserId != null) {
                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    NebCommentComposerBar(
                        value = threadReplyText,
                        onValueChange = viewModel::onThreadReplyChange,
                        placeholder = if (activeThreadTargetReply != null) "Reply to @${activeThreadTargetReply?.authorName}..." else "Write a reply...",
                        enabled = !isSubmittingReply,
                        canSend = threadReplyText.text.isNotBlank() && !isSubmittingReply,
                        posting = isSubmittingReply,
                        visualTransformation = MentionsVisualTransformation(MaterialTheme.colorScheme.primary),
                        onSend = {
                            val targetId = activeThreadTargetReply?.id ?: parent.id
                            viewModel.submitReply(
                                content = threadReplyText.text,
                                parentReplyId = targetId,
                                onSuccess = {
                                    activeThreadTargetReply = null
                                }
                            )
                        }
                    ) {
                        if (threadMentionSuggestions.isNotEmpty()) {
                            MentionSuggestions(
                                users = threadMentionSuggestions,
                                onSelect = viewModel::selectThreadMention,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )
                        }

                        activeThreadTargetReply?.let { target ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(bottom = 8.dp)
                                    .background(
                                        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                                        shape = RoundedCornerShape(8.dp)
                                    )
                                    .padding(horizontal = 12.dp, vertical = 6.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Close,
                                    contentDescription = "Clear reply target",
                                    modifier = Modifier
                                        .size(16.dp)
                                        .clickable { activeThreadTargetReply = null },
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    text = "Replying to @${target.authorName}: \"${target.content.take(40)}${if (target.content.length > 40) "..." else ""}\"",
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
    onProfileClick: (String) -> Unit,
    onAuthorLongPress: () -> Unit,
    onLinkClick: (String) -> Unit,
    onImageClick: (String) -> Unit
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
                val postLevel = remember(post.authorBadgeInfo) {
                    if (post.authorBadgeInfo?.type == "verified") {
                        when (post.authorBadgeInfo.color?.trim()?.lowercase()) {
                            "#1b9af0" -> 1
                            "#2e7d32" -> 2
                            "#f59e0b" -> 3
                            "#1a1a1a" -> 4
                            else -> 1
                        }
                    } else 0
                }
                Avatar(name = post.authorName, imageUrl = post.authorPhotoUrl, size = 38.dp, verificationLevel = postLevel)
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

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = post.title,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )

        Spacer(modifier = Modifier.height(8.dp))

        ExpandableMarkdownText(
            markdown = post.content,
            style = MaterialTheme.typography.bodyMedium,
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
                            .clip(RoundedCornerShape(12.dp))
                            .clickable { resolveMediaUrl(image.imageUrl)?.let(onImageClick) },
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
    onReportClick: () -> Unit,
    onEditClick: () -> Unit,
    onArchiveClick: () -> Unit,
    onDeleteClick: () -> Unit,
    onProfileClick: (String) -> Unit,
    onAuthorLongPress: () -> Unit,
    onLinkClick: (String) -> Unit,
    replyingToUsername: String? = null,
    quotedContent: String? = null,
    children: List<ApiReply> = emptyList(),
    onRepliesBarClick: (() -> Unit)? = null
) {
    Surface(
        shape = RoundedCornerShape(8.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
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
                    val replyLevel = remember(reply.authorBadgeInfo) {
                        if (reply.authorBadgeInfo?.type == "verified") {
                            when (reply.authorBadgeInfo.color?.trim()?.lowercase()) {
                                "#1b9af0" -> 1
                                "#2e7d32" -> 2
                                "#f59e0b" -> 3
                                "#1a1a1a" -> 4
                                else -> 1
                            }
                        } else 0
                    }
                    Avatar(name = reply.authorName, imageUrl = reply.authorPhotoUrl, size = 28.dp, verificationLevel = replyLevel)
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
                    onReport = onReportClick,
                    onEdit = onEditClick,
                    onArchive = onArchiveClick,
                    onDelete = onDeleteClick
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            if (!quotedContent.isNullOrBlank()) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Text(
                            text = "“",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = quotedContent,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }

            if (!replyingToUsername.isNullOrBlank() && quotedContent.isNullOrBlank()) {
                Surface(
                    shape = RoundedCornerShape(4.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    modifier = Modifier.padding(bottom = 6.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Replying to ",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = "@$replyingToUsername",
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }

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
                modifier = Modifier.fillMaxWidth()
            ) {
                LikePill(
                    count = reply.thumbsUpCount,
                    liked = reply.isThumbedUp,
                    onClick = onThumbsUpClick
                )
                Spacer(modifier = Modifier.width(12.dp))
                Row(
                    modifier = Modifier
                        .clip(WebPillShape)
                        .clickable(onClick = onReplyClick)
                        .padding(horizontal = 8.dp, vertical = 5.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Outlined.Reply,
                        contentDescription = "Reply",
                        modifier = Modifier.size(16.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = "Reply",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Spacer(modifier = Modifier.weight(1f))
            }

            if (children.isNotEmpty() && onRepliesBarClick != null) {
                Spacer(modifier = Modifier.height(8.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .clickable(onClick = onRepliesBarClick)
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val firstChild = children.first()
                    val childLevel = remember(firstChild.authorBadgeInfo) {
                        if (firstChild.authorBadgeInfo?.type == "verified") {
                            when (firstChild.authorBadgeInfo.color?.trim()?.lowercase()) {
                                "#1b9af0" -> 1
                                "#2e7d32" -> 2
                                "#f59e0b" -> 3
                                "#1a1a1a" -> 4
                                else -> 1
                            }
                        } else 0
                    }
                    Avatar(
                        name = firstChild.authorName,
                        imageUrl = firstChild.authorPhotoUrl,
                        size = 20.dp,
                        verificationLevel = childLevel
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "${children.size} ${if (children.size == 1) "reply" else "replies"}",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.weight(1f))
                    Icon(
                        imageVector = Icons.Outlined.ChatBubbleOutline,
                        contentDescription = "View thread",
                        modifier = Modifier.size(16.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    }
}
