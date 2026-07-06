package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Whatshot
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Schedule

import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme

import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.ui.components.ConfirmDeleteDialog
import com.neb.ians.ui.components.EditContentDialog
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.WafWarningBanner
import com.neb.ians.ui.components.ForumPostCard
import com.neb.ians.ui.components.ReportDialog
import com.neb.ians.ui.components.ShimmerForumList
import com.neb.ians.ui.components.UserPopoverDialog
import com.neb.ians.ui.components.WebChipRow
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.sharePost

@Composable
fun ForumScreen(
    onPostClick: (String) -> Unit,
    onCreatePostClick: () -> Unit,
    onSearchClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onUserProfileClick: (String) -> Unit = {},
    viewModel: ForumViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    val listState = rememberLazyListState()
    val lifecycleOwner = LocalLifecycleOwner.current

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                viewModel.syncLikeStates()
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    // Dialog state
    var reportPostId by remember { mutableStateOf<String?>(null) }
    var editingPost by remember { mutableStateOf<ApiPost?>(null) }
    var deletingPostId by remember { mutableStateOf<String?>(null) }
    var popoverUsername by remember { mutableStateOf<String?>(null) }

    // Snackbar messages from the ViewModel
    LaunchedEffect(uiState.snackbarMessage) {
        uiState.snackbarMessage?.let { message ->
            snackbarHostState.showSnackbar(message)
            viewModel.consumeSnackbar()
        }
    }

    // Infinite scroll: load next page when close to the end.
    val shouldLoadMore by remember {
        derivedStateOf {
            val info = listState.layoutInfo
            val lastVisible = info.visibleItemsInfo.lastOrNull()?.index ?: 0
            info.totalItemsCount > 0 && lastVisible >= info.totalItemsCount - 3 && uiState.error != ApiErrorMapper.WAF_ERROR_MESSAGE
        }
    }
    LaunchedEffect(shouldLoadMore, uiState.hasMore) {
        if (shouldLoadMore && uiState.hasMore) viewModel.loadMore()
    }

    Scaffold(
        topBar = {
            WebTopBar(
                onSearchClick = onSearchClick,
                onNotificationsClick = onNotificationsClick,
                onProfileClick = onProfileClick,
                avatarInitial = uiState.userName,
                avatarUrl = uiState.userPhotoUrl
            )
        },
        floatingActionButton = {
            androidx.compose.material3.FloatingActionButton(
                onClick = onCreatePostClick,
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary
            ) {
                Icon(
                    imageVector = Icons.Filled.Add,
                    contentDescription = "New Post"
                )
            }
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {

            // ----- Sort tabs (Hot / New / Top / Discussed) -----
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                SortTab("Hot", "hot", Icons.Filled.Whatshot, uiState.sort, viewModel::selectSort)
                SortTab("New", "new", Icons.Outlined.Schedule, uiState.sort, viewModel::selectSort)
                SortTab("Top", "top", Icons.Outlined.ThumbUp, uiState.sort, viewModel::selectSort)
                SortTab("Discussed", "discussed", Icons.Outlined.ChatBubbleOutline, uiState.sort, viewModel::selectSort)
            }

            // ----- Category chips -----
            WebChipRow(
                items = ForumUiState.CATEGORIES,
                selectedItem = uiState.selectedCategory,
                onItemClick = viewModel::selectCategory,
                modifier = Modifier.padding(bottom = 8.dp)
            )

            when {
                uiState.isLoading -> ShimmerForumList()
                uiState.error != null && uiState.posts.isEmpty() -> {
                    ErrorCard(
                        message = uiState.error ?: "Something went wrong",
                        onRetry = { viewModel.refresh() },
                        modifier = Modifier.padding(16.dp)
                    )
                }
                uiState.posts.isEmpty() -> {
                    WebEmptyState(
                        title = "No posts yet",
                        message = "Start a discussion or change the selected category.",
                        icon = painterResource(id = R.drawable.ic_forum_outlined),
                        modifier = Modifier.padding(16.dp)
                    )
                }
                else -> {
                    LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(start = 16.dp, top = 4.dp, end = 16.dp, bottom = 112.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        if (uiState.error != null) {
                            item(key = "error_banner") {
                                if (uiState.error == ApiErrorMapper.WAF_ERROR_MESSAGE) {
                                    WafWarningBanner()
                                } else {
                                    ErrorCard(
                                        message = uiState.error ?: "Something went wrong",
                                        onRetry = { viewModel.refresh() }
                                    )
                                }
                            }
                        }
                        items(uiState.posts, key = { it.id }) { post ->
                            ForumPostCard(
                                post = post,
                                isOwnPost = uiState.currentUserId != null && post.authorId == uiState.currentUserId,
                                onClick = { onPostClick(post.id) },
                                onLikeClick = { viewModel.toggleThumbsUp(post.id) },
                                onBookmarkClick = { viewModel.toggleBookmark(post.id) },
                                onShareClick = { sharePost(context, post.id) },
                                onReportClick = { reportPostId = post.id },
                                onEditClick = { editingPost = post },
                                onArchiveClick = { viewModel.archivePost(post.id) },
                                onDeleteClick = { deletingPostId = post.id },
                                onAuthorClick = { onUserProfileClick(post.authorName) },
                                onAuthorLongPress = { popoverUsername = post.authorName }
                            )
                        }
                        if (uiState.isLoadingMore) {
                            item(key = "loading_more") {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 16.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.5.dp)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // ----- Dialogs -----
    reportPostId?.let { postId ->
        ReportDialog(
            onDismiss = { reportPostId = null },
            onSubmit = { reason, description ->
                viewModel.reportPost(postId, reason, description)
                reportPostId = null
            }
        )
    }

    editingPost?.let { post ->
        EditContentDialog(
            dialogTitle = "Edit post",
            initialTitle = post.title,
            initialContent = post.content,
            onDismiss = { editingPost = null },
            onSave = { title, content ->
                viewModel.editPost(post.id, title ?: post.title, content)
                editingPost = null
            }
        )
    }

    deletingPostId?.let { postId ->
        ConfirmDeleteDialog(
            message = "Delete post? This cannot be undone.",
            onDismiss = { deletingPostId = null },
            onConfirm = {
                viewModel.deletePost(postId)
                deletingPostId = null
            }
        )
    }

    popoverUsername?.let { username ->
        UserPopoverDialog(
            username = username,
            onDismiss = { popoverUsername = null },
            onViewProfile = { profileUsername ->
                popoverUsername = null
                onUserProfileClick(profileUsername)
            }
        )
    }
}

/** Pill sort tab matching web .forum-sort-tab / .forum-sort-tab-active. */
@Composable
private fun SortTab(
    label: String,
    value: String,
    icon: ImageVector,
    currentSort: String,
    onSelect: (String) -> Unit
) {
    val selected = currentSort == value
    val background = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent
    val contentColor = if (selected) MaterialTheme.colorScheme.onSecondaryContainer
    else MaterialTheme.colorScheme.onSurfaceVariant
    Row(
        modifier = Modifier
            .clip(WebPillShape)
            .background(background)
            .then(
                if (selected) Modifier
                else Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, WebPillShape)
            )
            .clickable { onSelect(value) }
            .padding(horizontal = 14.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(15.dp),
            tint = contentColor
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
            color = contentColor
        )
    }
}
