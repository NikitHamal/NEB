package com.neb.ians.ui.screens.forum

import com.neb.ians.ui.components.GateReason
import com.neb.ians.ui.components.GuestReplyBar
import com.neb.ians.ui.components.LocalAuthGate
import com.neb.ians.ui.components.inlineGallery
import com.neb.ians.ui.components.boundedWidth
import com.neb.ians.ui.components.NebToastHost
import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.extractPostAttachments
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
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
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
import com.neb.ians.ui.components.KaTeXText
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.ExpandableMarkdownText
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.nebGhostRowStart
import com.neb.ians.ui.components.NebPollCard
import com.neb.ians.ui.components.toPollUi
import com.neb.ians.ui.components.PostMoreMenu
import com.neb.ians.ui.components.ReportDialog
import com.neb.ians.ui.components.UserPopoverDialog
import com.neb.ians.ui.components.ZoomableImageDialog
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.resolveMediaUrl
import com.neb.ians.ui.components.sharePost
import com.neb.ians.ui.components.MentionsVisualTransformation
import com.neb.ians.ui.components.MentionSuggestions
import com.neb.ians.ui.components.CommentCard
import com.neb.ians.ui.components.CommentSortPillsRow
import com.neb.ians.ui.components.ComposerAnonymousButton
import com.neb.ians.ui.components.ReplyLabelSheet
import com.neb.ians.ui.components.ComposerAttachMenu
import com.neb.ians.ui.components.ComposerPoll
import com.neb.ians.ui.components.ComposerAttachmentChips
import com.neb.ians.ui.components.ForumAttachmentChip
import com.neb.ians.ui.components.ForumMediaAttachments
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.components.rememberVoiceNoteRecorder
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo
import com.neb.ians.ui.components.NebLoader

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ForumPostDetailScreen(
    postId: String,
    onNavigateBack: () -> Unit,
    onEditPostClick: (String) -> Unit = {},
    onProfileClick: (String) -> Unit = {},
    viewModel: PostDetailViewModel = hiltViewModel()
) {
    val gate = LocalAuthGate.current
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var labelTarget by remember { mutableStateOf<com.neb.ians.data.api.ApiReply?>(null) }
    labelTarget?.let { target ->
        ReplyLabelSheet(
            current = target.label,
            onPick = { viewModel.labelReply(target.id, it) },
            onDismiss = { labelTarget = null }
        )
    }

    val composerMediaPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenMultipleDocuments()
    ) { uris -> if (!uris.isNullOrEmpty()) viewModel.addMediaAttachments(uris) }

    val voiceNote = rememberVoiceNoteRecorder(
        onVoiceNote = { file, durationMs -> viewModel.addVoiceNote(file, durationMs) },
        onError = viewModel::showSnackbar
    )

    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    val mainFocusRequester = remember { FocusRequester() }
    val keyboardController = LocalSoftwareKeyboardController.current
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }
    val listState = androidx.compose.foundation.lazy.rememberLazyListState()
    var flashReplyId by remember { mutableStateOf<String?>(null) }

    // Bottom sheet state for thread
    // Id-based so the sheet always renders from live state (likes/bookmarks recompose).
    var activeThreadParentId by remember { mutableStateOf<String?>(null) }
    var activeThreadTargetReply by remember { mutableStateOf<ApiReply?>(null) }
    var zoomImageUrls by remember { mutableStateOf<List<String>?>(null) }
    var zoomImageIndex by remember { mutableIntStateOf(0) }

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

    val openLink: (String) -> Unit = remember(context) {
        { url ->
            try {
                context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
            } catch (_: Exception) {
            }
        }
    }

    val mainComposer: @Composable () -> Unit = {
        if (gate.signedIn) {
            MainReplyComposerSlot(
                viewModel = viewModel,
                gate = gate,
                voiceNote = voiceNote,
                mainFocusRequester = mainFocusRequester,
                keyboardController = keyboardController,
                onLaunchMediaPicker = { composerMediaPicker.launch(it) }
            )
        } else {
            GuestReplyBar(onClick = { gate.ask(GateReason.Reply) })
        }
    }

    Scaffold(
        topBar = {
            DiscussionHeader(
                category = uiState.post?.category?.ifBlank { "General" } ?: "",
                onBack = onNavigateBack
            )
        },
        snackbarHost = { NebToastHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        when {
            uiState.isLoading -> Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                NebLoader()
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
                val isOwnPost = post.isOwner || (uiState.currentUserId != null && post.authorId == uiState.currentUserId)
                val topLevel = uiState.topLevelReplies

                com.neb.ians.ui.components.NebRefreshBox(
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
                val hasComposer = uiState.currentUserId != null
                LazyColumn(
                    state = listState,
                    modifier = Modifier
                        .fillMaxSize()
                        .imePadding(),
                    contentPadding = PaddingValues(bottom = 24.dp)
                ) {
                    item(key = "post_header") {
                        com.neb.ians.ui.components.PostLookPage(post.look) {
                        PostContentSection(
                            post = post,
                            poll = uiState.poll,
                            isOwnPost = isOwnPost,
                            solved = uiState.isSolved,
                            onSolvedClick = {
                                val at = topLevel.indexOfFirst { it.label == "accepted" }
                                if (at >= 0) scope.launch {
                                    // post header, composer (signed in), replies header, then the replies
                                    listState.animateScrollToItem(2 + (if (hasComposer) 1 else 0) + at)
                                    flashReplyId = topLevel[at].id
                                    kotlinx.coroutines.delay(1200)
                                    flashReplyId = null
                                }
                            },
                            busy = uiState.busyPollId != null,
                            onThumbsUpClick = viewModel::toggleThumbsUp,
                            onBookmarkClick = viewModel::togglePostBookmark,
                            onShareClick = { sharePost(context, post.id) },
                            onReportClick = { reportTarget = "post" to post.id },
                            onEditClick = { onEditPostClick(post.id) },
                            onArchiveClick = viewModel::archivePost,
                            onDeleteClick = { deletingPost = true },
                            onReplyClick = { mainFocusRequester.requestFocus() },
                            onVote = { ids -> gate.require(GateReason.Like) { uiState.poll?.let { viewModel.votePoll(it.id, ids, it.allowMultiple) } } },
                            onAddOption = { text -> uiState.poll?.let { viewModel.addPollOption(it.id, text) } },
                            onRetract = { uiState.poll?.let { viewModel.retractPollVote(it.id) } },
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = post.authorName },
                            onLinkClick = openLink,
                            onImageClick = { urls, index ->
                                zoomImageUrls = urls
                                zoomImageIndex = index
                            }
                        )
                        }
                    }

                    if (uiState.currentUserId != null) {
                        item(key = "composer") {
                            Column {
                                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                                mainComposer()
                            }
                        }
                    }

                    item(key = "replies_header") {
                        Column {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(start = 16.dp, end = 12.dp, top = 6.dp, bottom = 12.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Text(
                                    text = "Replies",
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Text(
                                    text = uiState.replies.size.toString(),
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.SemiBold,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.weight(1f)
                                )
                                CommentSortPillsRow(
                                    currentSort = uiState.replySort,
                                    onSelect = viewModel::setReplySort
                                )
                            }
                            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                        }
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

                    items(topLevel, key = { it.id }, contentType = { "reply" }) { reply ->
                        val children = uiState.childrenOf(reply.id)
                        CommentCard(
                            reply = reply,
                            pollContent = { api -> ReplyPollSlot(api, uiState.busyPollId, viewModel) },
                            highlighted = flashReplyId == reply.id,
                            isOwn = reply.isOwner || (uiState.currentUserId != null && reply.authorId == uiState.currentUserId),
                            onThumbsUpClick = { gate.require(GateReason.Like) { viewModel.toggleReplyThumbsUp(reply.id) } },
                            onLabelClick = { labelTarget = reply },
                            onReplyClick = {
                                activeThreadParentId = reply.id
                                activeThreadTargetReply = reply
                                val tag = "@${reply.authorName} "
                                viewModel.onThreadReplyChange(
                                    androidx.compose.ui.text.input.TextFieldValue(
                                        text = tag,
                                        selection = androidx.compose.ui.text.TextRange(tag.length)
                                    )
                                )
                            },
                            onBookmarkClick = { gate.require(GateReason.Save) { viewModel.toggleReplyBookmark(reply.id) } },
                            onReportClick = { reportTarget = "reply" to reply.id },
                            onEditClick = { editingReply = reply },
                            onArchiveClick = { viewModel.archiveReply(reply.id) },
                            onDeleteClick = { deletingReplyId = reply.id },
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = reply.authorName },
                            onLinkClick = openLink,
                            children = children,
                            onRepliesBarClick = { activeThreadParentId = reply.id },
                            onInlineImageClick = { url -> inlineGallery(url, reply.content).let { (list, at) -> zoomImageUrls = list; zoomImageIndex = at } }
                        )
                    }

                    item(key = "bottom_spacer") {
                        Spacer(modifier = Modifier.height(24.dp))
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
    zoomImageUrls?.let { urls ->
        ZoomableImageDialog(
            imageUrls = urls,
            initialIndex = zoomImageIndex,
            contentDescription = "Post image",
            onDismiss = { zoomImageUrls = null }
        )
    }

    activeThreadParentId?.let { parentId ->
        // Resolve from live state (not a cached snapshot) so like/bookmark toggles
        // recompose the parent card inside the thread sheet.
        val parent = uiState.replies.firstOrNull { it.id == parentId }
        if (parent == null) {
            // Parent reply was deleted while the sheet was open — close the sheet.
            LaunchedEffect(parentId) {
                activeThreadParentId = null
                activeThreadTargetReply = null
            }
            return@let
        }
        val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
        val threadReplies = uiState.childrenOf(parent.id)
        val repliesById = remember(uiState.replies) { uiState.replies.associateBy { it.id } }

        NebModalSheet(
            onDismiss = {
                activeThreadParentId = null
                activeThreadTargetReply = null
            },
            sheetState = sheetState,
                fullBleed = true, // bleed: content pads itself or draws edge to edge rows
                bottomGap = 0.dp
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .fillMaxHeight()
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

                    IconButton(onClick = { viewModel.refresh() }) {
                        Icon(
                            Icons.Filled.Refresh,
                            contentDescription = "Refresh thread",
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    IconButton(onClick = { activeThreadParentId = null }) {
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
                        CommentCard(
                            reply = parent,
                            pollContent = { api -> ReplyPollSlot(api, uiState.busyPollId, viewModel) },
                            isOwn = parent.isOwner || (uiState.currentUserId != null && parent.authorId == uiState.currentUserId),
                            onThumbsUpClick = { gate.require(GateReason.Like) { viewModel.toggleReplyThumbsUp(parent.id) } },
                            onLabelClick = { labelTarget = parent },
                            onReplyClick = {
                                activeThreadTargetReply = parent
                                val currentText = viewModel.threadReplyText.value.text
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
                            onBookmarkClick = { gate.require(GateReason.Save) { viewModel.toggleReplyBookmark(parent.id) } },
                            onReportClick = { reportTarget = "reply" to parent.id },
                            onEditClick = { editingReply = parent },
                            onArchiveClick = { viewModel.archiveReply(parent.id) },
                            onDeleteClick = { deletingReplyId = parent.id },
                            onProfileClick = onProfileClick,
                            onAuthorLongPress = { popoverUsername = parent.authorName },
                            onLinkClick = openLink,
                            onInlineImageClick = { url -> inlineGallery(url, parent.content).let { (list, at) -> zoomImageUrls = list; zoomImageIndex = at } }
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
                        items(threadReplies, key = { it.id }, contentType = { "thread_reply" }) { child ->
                            Column(modifier = Modifier.padding(bottom = 12.dp)) {
                                val parentOfChild = repliesById[child.parentReplyId]
                                val replyingTo = if (child.parentReplyId != parent.id) {
                                    parentOfChild?.authorName
                                } else null

                                CommentCard(
                                    reply = child,
                                    pollContent = { api -> ReplyPollSlot(api, uiState.busyPollId, viewModel) },
                                    isOwn = child.isOwner || (uiState.currentUserId != null && child.authorId == uiState.currentUserId),
                                    onThumbsUpClick = { gate.require(GateReason.Like) { viewModel.toggleReplyThumbsUp(child.id) } },
                                    onReplyClick = {
                                        activeThreadTargetReply = child
                                        val currentText = viewModel.threadReplyText.value.text
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
                                    onBookmarkClick = { gate.require(GateReason.Save) { viewModel.toggleReplyBookmark(child.id) } },
                                    onReportClick = { reportTarget = "reply" to child.id },
                                    onEditClick = { editingReply = child },
                                    onArchiveClick = { viewModel.archiveReply(child.id) },
                                    onDeleteClick = { deletingReplyId = child.id },
                                    onProfileClick = onProfileClick,
                                    onAuthorLongPress = { popoverUsername = child.authorName },
                                    onLinkClick = openLink,
                                    replyingToUsername = replyingTo,
                                    quotedContent = parentOfChild?.content,
                                    onInlineImageClick = { url -> inlineGallery(url, child.content).let { (list, at) -> zoomImageUrls = list; zoomImageIndex = at } }
                                )
                            }
                        }
                    }
                }

                if (uiState.currentUserId != null) {
                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    ThreadReplyComposerSlot(
                        viewModel = viewModel,
                        gate = gate,
                        parentId = parent.id,
                        activeThreadTargetReply = activeThreadTargetReply,
                        onClearTargetReply = { activeThreadTargetReply = null },
                        voiceNote = voiceNote,
                        onLaunchMediaPicker = { composerMediaPicker.launch(it) }
                    )
                }
            }
        }
    }
}

@Composable
private fun MainReplyComposerSlot(
    viewModel: PostDetailViewModel,
    gate: com.neb.ians.ui.components.AuthGate,
    voiceNote: com.neb.ians.ui.components.VoiceNoteRecorder,
    mainFocusRequester: FocusRequester,
    keyboardController: androidx.compose.ui.platform.SoftwareKeyboardController?,
    onLaunchMediaPicker: (Array<String>) -> Unit
) {
    val mainReplyText by viewModel.mainReplyText.collectAsStateWithLifecycle()
    val mainMentionSuggestions by viewModel.mainMentionSuggestions.collectAsStateWithLifecycle()
    val isSubmittingReply by viewModel.isSubmittingReply.collectAsStateWithLifecycle()
    val composerMediaAttachments by viewModel.mediaAttachments.collectAsStateWithLifecycle()
    val composerAnonymous by viewModel.composerAnonymous.collectAsStateWithLifecycle()
    val composerKind by viewModel.composerKind.collectAsStateWithLifecycle()
    val composerPoll by viewModel.composerPoll.collectAsStateWithLifecycle()
    val identityName by viewModel.userName.collectAsStateWithLifecycle()
    val identityPhoto by viewModel.userPhotoUrl.collectAsStateWithLifecycle()
    val identityHandle by viewModel.userHandle.collectAsStateWithLifecycle()
    val identityAnonTag by viewModel.anonTag.collectAsStateWithLifecycle()
    NebCommentComposerBar(
        value = mainReplyText,
        onValueChange = viewModel::onMainReplyChange,
        placeholder = "Post your reply...",
        enabled = !isSubmittingReply,
        canSend = (mainReplyText.text.isNotBlank() || composerMediaAttachments.isNotEmpty() || composerPoll?.isReady == true) && !isSubmittingReply,
        posting = isSubmittingReply,
        voiceNote = voiceNote,
        docked = false,
        kind = composerKind,
        onKindChange = viewModel::setComposerKind,
        textFieldModifier = Modifier.focusRequester(mainFocusRequester),
        visualTransformation = MentionsVisualTransformation(MaterialTheme.colorScheme.primary),
        leadingContent = {
            com.neb.ians.ui.components.NebIdentityAvatarMenu(
                isAnonymous = composerAnonymous,
                userName = identityName,
                handle = identityHandle,
                photoUrl = identityPhoto,
                anonTag = identityAnonTag,
                onSelect = viewModel::setComposerAnonymous,
                enabled = !isSubmittingReply,
                modifier = Modifier.padding(start = 4.dp)
            )
        },
        trailingContent = {
            ComposerAttachMenu(
                enabled = !isSubmittingReply,
                onPick = onLaunchMediaPicker,
                poll = ComposerPoll(active = composerPoll != null, onToggle = viewModel::toggleComposerPoll)
            )
        },
        onSend = send@{
            if (!gate.signedIn) { gate.ask(GateReason.Reply); return@send }
            keyboardController?.hide()
            viewModel.submitReply(content = mainReplyText.text, parentReplyId = null, onSuccess = {})
        }
    ) {
        composerPoll?.let { draft ->
            CommentPollBuilder(
                draft = draft,
                onChange = viewModel::updateComposerPoll,
                onClose = viewModel::toggleComposerPoll,
                enabled = !isSubmittingReply
            )
        }
        ComposerAttachmentChips(
            attachments = composerMediaAttachments,
            onRemoveAttachment = viewModel::removeMediaAttachment
        )
        if (mainMentionSuggestions.isNotEmpty()) {
            MentionSuggestions(
                users = mainMentionSuggestions,
                onSelect = viewModel::selectMainMention,
                modifier = Modifier.padding(bottom = 8.dp)
            )
        }
    }
}

@Composable
private fun ThreadReplyComposerSlot(
    viewModel: PostDetailViewModel,
    gate: com.neb.ians.ui.components.AuthGate,
    parentId: String,
    activeThreadTargetReply: ApiReply?,
    onClearTargetReply: () -> Unit,
    voiceNote: com.neb.ians.ui.components.VoiceNoteRecorder,
    onLaunchMediaPicker: (Array<String>) -> Unit
) {
    val threadReplyText by viewModel.threadReplyText.collectAsStateWithLifecycle()
    val threadMentionSuggestions by viewModel.threadMentionSuggestions.collectAsStateWithLifecycle()
    val isSubmittingReply by viewModel.isSubmittingReply.collectAsStateWithLifecycle()
    val composerMediaAttachments by viewModel.mediaAttachments.collectAsStateWithLifecycle()
    val composerAnonymous by viewModel.composerAnonymous.collectAsStateWithLifecycle()
    val identityName by viewModel.userName.collectAsStateWithLifecycle()
    val identityPhoto by viewModel.userPhotoUrl.collectAsStateWithLifecycle()
    val identityHandle by viewModel.userHandle.collectAsStateWithLifecycle()
    val identityAnonTag by viewModel.anonTag.collectAsStateWithLifecycle()
    NebCommentComposerBar(
        value = threadReplyText,
        onValueChange = viewModel::onThreadReplyChange,
        placeholder = if (activeThreadTargetReply != null) "Reply to @${activeThreadTargetReply.authorName}..." else "Write a reply...",
        enabled = !isSubmittingReply,
        canSend = (threadReplyText.text.isNotBlank() || composerMediaAttachments.isNotEmpty()) && !isSubmittingReply,
        posting = isSubmittingReply,
        voiceNote = voiceNote,
        visualTransformation = MentionsVisualTransformation(MaterialTheme.colorScheme.primary),
        leadingContent = {
            com.neb.ians.ui.components.NebIdentityAvatarMenu(
                isAnonymous = composerAnonymous,
                userName = identityName,
                handle = identityHandle,
                photoUrl = identityPhoto,
                anonTag = identityAnonTag,
                onSelect = viewModel::setComposerAnonymous,
                enabled = !isSubmittingReply,
                modifier = Modifier.padding(start = 4.dp)
            )
        },
        trailingContent = {
            ComposerAttachMenu(enabled = !isSubmittingReply, onPick = onLaunchMediaPicker)
        },
        onSend = {
            if (!gate.signedIn) { gate.ask(GateReason.Reply); return@NebCommentComposerBar }
            val targetId = activeThreadTargetReply?.id ?: parentId
            viewModel.submitReply(content = threadReplyText.text, parentReplyId = targetId, onSuccess = onClearTargetReply)
        }
    ) {
        ComposerAttachmentChips(
            attachments = composerMediaAttachments,
            onRemoveAttachment = viewModel::removeMediaAttachment
        )
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
                    .background(color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), shape = RoundedCornerShape(8.dp))
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.Close,
                    contentDescription = "Clear reply target",
                    modifier = Modifier.size(16.dp).clickable(onClick = onClearTargetReply),
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

@Composable
@OptIn(ExperimentalFoundationApi::class)
private fun PostContentSection(
    post: ApiPost,
    poll: com.neb.ians.ui.components.PollUi?,
    isOwnPost: Boolean,
    solved: Boolean,
    onSolvedClick: () -> Unit,
    busy: Boolean,
    onThumbsUpClick: () -> Unit,
    onBookmarkClick: () -> Unit,
    onShareClick: () -> Unit,
    onReportClick: () -> Unit,
    onEditClick: () -> Unit,
    onArchiveClick: () -> Unit,
    onDeleteClick: () -> Unit,
    onReplyClick: () -> Unit,
    onVote: (List<String>) -> Unit,
    onAddOption: (String) -> Unit,
    onRetract: () -> Unit,
    onProfileClick: (String) -> Unit,
    onAuthorLongPress: () -> Unit,
    onLinkClick: (String) -> Unit,
    onImageClick: (imageUrls: List<String>, index: Int) -> Unit
) {
    val category = post.category.ifBlank { "General" }
    val categoryTheme = getSubjectTheme(category)
    val bookmarked = post.isBookmarked == true

    Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 16.dp)) {
        // ----- Meta row -----
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
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
                Avatar(name = post.authorName, imageUrl = post.authorPhotoUrl, size = 44.dp, verificationLevel = postLevel)
            }
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = post.authorName,
                        style = MaterialTheme.typography.titleSmall,
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
                Text(
                    text = (if (post.authorName.startsWith("Anon")) "" else "@${post.authorName} \u00B7 ") + formatTimeAgo(post.createdAt),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
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
            PostMoreMenu(
                isOwn = isOwnPost,
                isBookmarked = bookmarked,
                isArchived = post.isArchived == true,
                onBookmark = onBookmarkClick,
                onShare = onShareClick,
                onReport = onReportClick,
                onEdit = onEditClick,
                onArchive = onArchiveClick,
                onDelete = onDeleteClick,
                onInsights = com.neb.ians.ui.components.PostInsightsNav.open?.let { open -> { open(post.id) } }
            )
        }

        if (solved) {
            Spacer(modifier = Modifier.height(12.dp))
            com.neb.ians.ui.components.SolvedChip(onClick = onSolvedClick)
        }

        Spacer(modifier = Modifier.height(10.dp))

        KaTeXText(
            text = post.title,
            style = MaterialTheme.typography.titleLarge.copy(fontSize = 19.sp, lineHeight = 25.sp),
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )

        Spacer(modifier = Modifier.height(6.dp))

        ExpandableMarkdownText(
            markdown = post.content,
            style = MaterialTheme.typography.bodyLarge.copy(fontSize = 14.5.sp, lineHeight = 21.sp),
            color = MaterialTheme.colorScheme.onSurface,
            onMentionClick = onProfileClick,
            onLinkClick = onLinkClick,
            tickKey = "post:" + post.id,
            onInlineImageClick = { url -> inlineGallery(url, post.content, post.images.sortedBy { it.order }.mapNotNull { resolveMediaUrl(it.imageUrl) }).let { (list, at) -> onImageClick(list, at) } }
        )

        // ----- Attached images: horizontal carousel (swipe), tap opens fullscreen -----
        if (post.images.isNotEmpty()) {
            Spacer(modifier = Modifier.height(12.dp))
            val imageUrls = remember(post.images) {
                post.images.sortedBy { it.order }.mapNotNull { resolveMediaUrl(it.imageUrl) }
            }
            if (imageUrls.size == 1) {
                AsyncImage(
                    model = imageUrls.first(),
                    contentDescription = null,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .clickable { onImageClick(imageUrls, 0) },
                    contentScale = ContentScale.FillWidth
                )
            } else {
                val pagerState = rememberPagerState(pageCount = { imageUrls.size })
                Column {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .aspectRatio(4f / 3f)
                            .clip(RoundedCornerShape(12.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.boundedWidth().fillMaxSize()
                        ) { page ->
                            AsyncImage(
                                model = imageUrls[page],
                                contentDescription = "Image ${page + 1} of ${imageUrls.size}",
                                modifier = Modifier
                                    .fillMaxSize()
                                    .clickable { onImageClick(imageUrls, page) },
                                contentScale = ContentScale.Crop
                            )
                        }
                        Surface(
                            modifier = Modifier
                                .align(Alignment.TopEnd)
                                .padding(10.dp),
                            shape = CircleShape,
                            color = Color.Black.copy(alpha = 0.45f)
                        ) {
                            Text(
                                text = "${pagerState.currentPage + 1}/${imageUrls.size}",
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                                style = MaterialTheme.typography.labelSmall,
                                color = Color.White
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center
                    ) {
                        repeat(imageUrls.size) { index ->
                            val active = pagerState.currentPage == index
                            Box(
                                modifier = Modifier
                                    .padding(horizontal = 3.dp)
                                    .size(if (active) 7.dp else 6.dp)
                                    .clip(CircleShape)
                                    .background(
                                        if (active) MaterialTheme.colorScheme.primary
                                        else MaterialTheme.colorScheme.outlineVariant
                                    )
                            )
                        }
                    }
                }
            }
        }

        // ----- Media attachments (video / audio / files) -----
        val allAttachments = remember(post) { extractPostAttachments(post) }
        if (allAttachments.isNotEmpty()) {
            Spacer(modifier = Modifier.height(12.dp))
            ForumMediaAttachments(
                attachments = allAttachments,
                modifier = Modifier.fillMaxWidth()
            )
        }

        // ----- Poll -----
        poll?.let {
            Spacer(modifier = Modifier.height(12.dp))
            NebPollCard(poll = it, busy = busy, onVote = onVote, onAddOption = onAddOption, onRetract = onRetract)
        }

        Spacer(modifier = Modifier.height(14.dp))
        Text(
            text = formatTimeAgo(post.createdAt),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(modifier = Modifier.height(12.dp))
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
        Spacer(modifier = Modifier.height(4.dp))

        // ----- Action row: like, comments, bookmark, share (ghost, like the web) -----
        val muted = MaterialTheme.colorScheme.onSurfaceVariant
        Row(
            modifier = Modifier.fillMaxWidth().nebGhostRowStart(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp)
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
                    .padding(horizontal = 12.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                com.neb.ians.ui.components.NebIcon(com.neb.ians.ui.components.NebIcons.Comment, "Reply", size = 18.dp, tint = muted)
                Text(
                    text = post.replyCount.toString(),
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Medium,
                    color = muted
                )
            }
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .clickable(onClick = onBookmarkClick),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (bookmarked) Icons.Filled.Bookmark else Icons.Filled.BookmarkBorder,
                    contentDescription = if (bookmarked) "Remove bookmark" else "Bookmark",
                    modifier = Modifier.size(20.dp),
                    tint = if (bookmarked) MaterialTheme.colorScheme.primary else muted
                )
            }
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .clickable(onClick = onShareClick),
                contentAlignment = Alignment.Center
            ) {
                com.neb.ians.ui.components.NebIcon(com.neb.ians.ui.components.NebIcons.Share, "Share", size = 20.dp, tint = muted)
            }
        }
    }
}

/** The web's discussion header: back, "Discussion", the `#category` tag, a hairline under it. */
@Composable
private fun DiscussionHeader(category: String, onBack: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(scheme.surface)
            .statusBarsPadding()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(60.dp)
                .padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = scheme.onSurface)
            }
            Text(
                text = "Discussion",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = scheme.onSurface
            )
            if (category.isNotBlank()) {
                Surface(shape = WebPillShape, color = scheme.secondaryContainer) {
                    Text(
                        text = "#$category",
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 3.dp),
                        style = MaterialTheme.typography.labelMedium,
                        color = scheme.onSecondaryContainer,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
        HorizontalDivider(color = scheme.outlineVariant)
    }
}


/** A comment's poll, fed by the same view model as the post's own poll. */
@Composable
private fun ReplyPollSlot(poll: com.neb.ians.data.api.ApiPoll, busyPollId: String?, viewModel: PostDetailViewModel) {
    val ui = poll.toPollUi()
    NebPollCard(
        poll = ui,
        busy = busyPollId != null,
        onVote = { ids -> viewModel.votePoll(ui.id, ids, ui.allowMultiple) },
        onAddOption = { text -> viewModel.addPollOption(ui.id, text) },
        onRetract = { viewModel.retractPollVote(ui.id) },
        modifier = Modifier.padding(top = 8.dp)
    )
}
