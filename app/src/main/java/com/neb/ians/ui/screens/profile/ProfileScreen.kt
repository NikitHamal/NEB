@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)

package com.neb.ians.ui.screens.profile

import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.outlined.BarChart
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.InsertDriveFile
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebTabRail
import com.neb.ians.ui.components.ZoomableImageDialog
import kotlinx.coroutines.launch

// ---------------------------------------------------------------------------
// Someone's profile.
//
// One scroll, front to back: who they are, then what they have made. The
// banner runs edge to edge under a solid top bar that takes over their name
// once the identity block has gone by, and the tab rail pins itself under
// that bar so you never lose your place in a long feed.
// ---------------------------------------------------------------------------

private const val PROFILE_LINK_BASE = "https://nebians.consica.com.np/profile/"

@Composable
fun ProfileScreen(
    username: String,
    showRequests: Boolean = false,
    onNavigateBack: () -> Unit,
    onEditProfile: () -> Unit,
    onPostClick: (String) -> Unit,
    onFollowerClick: (String) -> Unit,
    onAnalyticsClick: () -> Unit = {},
    onSearchClick: () -> Unit = {},
    onProfileClick: (String) -> Unit = {},
    onResourceClick: (String) -> Unit = {},
    viewModel: ProfileViewModel = hiltViewModel()
) {
    LaunchedEffect(username) {
        viewModel.loadProfile(username)
    }

    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(uiState.profile, showRequests) {
        if (showRequests && uiState.profile?.isSelf == true) {
            viewModel.openFollowRequests()
        }
    }

    val scope = rememberCoroutineScope()
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current
    var isRefreshing by remember { mutableStateOf(false) }

    val listState = rememberLazyListState()
    // The header's identity block is roughly 260dp in; past that the top bar
    // is the only thing still saying whose profile this is.
    val showBarTitle by remember {
        derivedStateOf {
            listState.firstVisibleItemIndex > 0 || listState.firstVisibleItemScrollOffset > 260
        }
    }

    val profile = uiState.profile
    val isSelf = profile?.isSelf == true

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    AnimatedVisibility(
                        visible = showBarTitle && profile != null,
                        enter = fadeIn(),
                        exit = fadeOut()
                    ) {
                        Column {
                            Text(
                                text = profile?.displayName?.takeIf { it.isNotBlank() }
                                    ?: profile?.username.orEmpty(),
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = postsLabel(profile?.postCount ?: 0),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1
                            )
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (isSelf) {
                        IconButton(onClick = onAnalyticsClick) {
                            Icon(Icons.Outlined.BarChart, contentDescription = "Analytics")
                        }
                    }
                    IconButton(
                        onClick = {
                            val handle = profile?.username ?: username
                            clipboard.setText(AnnotatedString("$PROFILE_LINK_BASE$handle/"))
                            Toast.makeText(context, "Profile link copied", Toast.LENGTH_SHORT).show()
                        }
                    ) {
                        Icon(Icons.Outlined.Link, contentDescription = "Copy link")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        PullToRefreshBox(
            isRefreshing = isRefreshing,
            onRefresh = {
                scope.launch {
                    isRefreshing = true
                    viewModel.loadProfile(username).join()
                    isRefreshing = false
                }
            },
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                profile != null -> ProfileBody(
                    uiState = uiState,
                    listState = listState,
                    onEditProfile = onEditProfile,
                    onFollowClick = viewModel::toggleFollow,
                    onPostClick = onPostClick,
                    onResourceClick = onResourceClick,
                    onTabSelected = viewModel::selectTab,
                    onLoadMorePosts = { viewModel.loadPosts(reset = false) },
                    onLoadMoreReplies = { viewModel.loadReplies(reset = false) },
                    onLoadMoreResources = { viewModel.loadResources(reset = false) },
                    onRetryPosts = { viewModel.loadPosts(reset = true) },
                    onRetryReplies = { viewModel.loadReplies(reset = true) },
                    onRetryResources = { viewModel.loadResources(reset = true) },
                    onAvatarClick = {
                        if (isSelf) viewModel.openPhotoGallery() else viewModel.openAvatarPreview()
                    },
                    onFollowersClick = viewModel::openFollowers,
                    onFollowingClick = viewModel::openFollowing,
                    onFollowRequestsClick = viewModel::openFollowRequests,
                    onProfileClick = onProfileClick,
                    onSocialLinkClick = { link -> viewModel.trackSocialClick(link, profile.id) }
                )

                uiState.error != null -> Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    NebEmptyState(
                        icon = Icons.Outlined.CloudOff,
                        title = "Profile unavailable",
                        subtitle = uiState.error,
                        action = {
                            NebButton(
                                text = "Try again",
                                onClick = { viewModel.loadProfile(username) },
                                tone = NebButtonTone.Outlined,
                                size = NebButtonSize.Small
                            )
                        }
                    )
                }

                else -> ProfileHeaderSkeleton(modifier = Modifier.fillMaxWidth())
            }
        }
    }

    if (uiState.showPhotoGallery) {
        PhotoGalleryDialog(
            photos = uiState.photos,
            isLoading = uiState.photosLoading,
            isBusy = uiState.photoBusy,
            onDismiss = viewModel::closePhotoGallery,
            onActivatePhoto = viewModel::activatePhoto,
            onUploadPhoto = viewModel::uploadPhoto
        )
    }

    if (uiState.showAvatarPreview && uiState.avatarPreviewUrl.isNotBlank()) {
        ZoomableImageDialog(
            imageUrl = uiState.avatarPreviewUrl,
            contentDescription = "Profile photo",
            onDismiss = viewModel::closeAvatarPreview
        )
    }

    if (uiState.showFollowersList) {
        FollowersDialog(
            title = "Followers",
            users = uiState.followersList,
            isLoading = uiState.followersLoading,
            error = uiState.followersError,
            onDismiss = viewModel::closeFollowers,
            onUserClick = onFollowerClick
        )
    }

    if (uiState.showFollowingList) {
        FollowersDialog(
            title = "Following",
            users = uiState.followingList,
            isLoading = uiState.followingLoading,
            error = uiState.followingError,
            onDismiss = viewModel::closeFollowing,
            onUserClick = onFollowerClick
        )
    }

    if (uiState.showFollowRequestsList) {
        FollowRequestsDialog(
            requests = uiState.followRequestsList,
            isLoading = uiState.followRequestsLoading,
            error = uiState.followRequestsError,
            onDismiss = viewModel::closeFollowRequests,
            onAccept = viewModel::acceptFollowRequest,
            onReject = viewModel::rejectFollowRequest,
            onUserClick = onFollowerClick
        )
    }
}

@Composable
private fun ProfileBody(
    uiState: ProfileUiState,
    listState: androidx.compose.foundation.lazy.LazyListState,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    onPostClick: (String) -> Unit,
    onResourceClick: (String) -> Unit,
    onTabSelected: (Int) -> Unit,
    onLoadMorePosts: () -> Unit,
    onLoadMoreReplies: () -> Unit,
    onLoadMoreResources: () -> Unit,
    onRetryPosts: () -> Unit,
    onRetryReplies: () -> Unit,
    onRetryResources: () -> Unit,
    onAvatarClick: () -> Unit,
    onFollowersClick: () -> Unit,
    onFollowingClick: () -> Unit,
    onFollowRequestsClick: () -> Unit,
    onProfileClick: (String) -> Unit,
    onSocialLinkClick: (com.neb.ians.data.api.ApiSocialLink) -> Unit
) {
    val profile = uiState.profile ?: return
    val isSelf = profile.isSelf == true
    val isPrivate = profile.isLocked == 1 && !isSelf && !uiState.isFollowing
    val handle = "@${profile.username}"

    LazyColumn(
        state = listState,
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 8.dp)
    ) {
        item(key = "header") {
            ProfileHeader(
                profile = profile,
                isSelf = isSelf,
                isFollowing = uiState.isFollowing,
                isRequested = uiState.isRequested,
                followRequestsCount = uiState.followRequestsCount,
                followerCount = uiState.followerCount,
                onEditProfile = onEditProfile,
                onFollowClick = onFollowClick,
                onAvatarClick = onAvatarClick,
                onFollowersClick = onFollowersClick,
                onFollowingClick = onFollowingClick,
                onFollowRequestsClick = onFollowRequestsClick,
                onProfileClick = onProfileClick,
                onSocialLinkClick = onSocialLinkClick
            )
        }

        if (isPrivate) {
            item(key = "private") {
                NebEmptyState(
                    icon = Icons.Outlined.Lock,
                    title = "This profile is private",
                    subtitle = "Follow $handle to see their posts, replies and resources."
                )
            }
            return@LazyColumn
        }

        stickyHeader(key = "tabs") { _: Int ->
            Column(modifier = Modifier.background(MaterialTheme.colorScheme.surface)) {
                NebTabRail(
                    tabs = listOf(
                        NebRailTab("Posts", count = profile.postCount),
                        NebRailTab("Replies", count = uiState.repliesCount),
                        NebRailTab("Resources", count = uiState.resourcesCount),
                        NebRailTab("About")
                    ),
                    selectedIndex = uiState.selectedTab,
                    onSelect = onTabSelected,
                    contentPadding = PaddingValues(horizontal = 14.dp, vertical = 4.dp)
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
            }
        }

        when (uiState.selectedTab) {
            0 -> feedSection(
                prefix = "post",
                count = uiState.posts.size,
                isLoading = uiState.postsLoading,
                isLoaded = uiState.postsLoaded,
                hasMore = uiState.postsHasMore,
                error = uiState.postsError,
                emptyIcon = Icons.Outlined.Forum,
                emptyTitle = if (isSelf) "You haven't posted yet" else "No posts yet",
                emptySubtitle = if (isSelf) {
                    "Anything you post in the forum shows up here."
                } else {
                    "$handle hasn't posted anything yet."
                },
                errorTitle = "Couldn't load posts",
                onRetry = onRetryPosts,
                onLoadMore = onLoadMorePosts,
                skeleton = { ProfileRowSkeleton() },
                key = { idx -> uiState.posts[idx].id },
                row = { idx, showDivider ->
                    val post = uiState.posts[idx]
                    ProfilePostRow(
                        post = post,
                        onClick = { onPostClick(post.id) },
                        showDivider = showDivider
                    )
                }
            )

            1 -> feedSection(
                prefix = "reply",
                count = uiState.replies.size,
                isLoading = uiState.repliesLoading,
                isLoaded = uiState.repliesLoaded,
                hasMore = uiState.repliesHasMore,
                error = uiState.repliesError,
                emptyIcon = Icons.AutoMirrored.Outlined.Reply,
                emptyTitle = if (isSelf) "You haven't replied yet" else "No replies yet",
                emptySubtitle = if (isSelf) {
                    "Answers you leave on other people's posts collect here."
                } else {
                    "$handle hasn't replied to anything yet."
                },
                errorTitle = "Couldn't load replies",
                onRetry = onRetryReplies,
                onLoadMore = onLoadMoreReplies,
                skeleton = { ProfileReplySkeleton() },
                key = { idx -> uiState.replies[idx].id },
                row = { idx, showDivider ->
                    val reply = uiState.replies[idx]
                    ProfileReplyRow(
                        reply = reply,
                        onClick = { onPostClick(reply.postId) },
                        showDivider = showDivider
                    )
                }
            )

            2 -> feedSection(
                prefix = "res",
                count = uiState.resources.size,
                isLoading = uiState.resourcesLoading,
                isLoaded = uiState.resourcesLoaded,
                hasMore = uiState.resourcesHasMore,
                error = uiState.resourcesError,
                emptyIcon = Icons.Outlined.InsertDriveFile,
                emptyTitle = if (isSelf) "You haven't shared resources yet" else "No resources yet",
                emptySubtitle = if (isSelf) {
                    "Notes and past papers you upload appear here once approved."
                } else {
                    "$handle hasn't shared any notes or papers yet."
                },
                errorTitle = "Couldn't load resources",
                onRetry = onRetryResources,
                onLoadMore = onLoadMoreResources,
                skeleton = { ProfileRowSkeleton(leading = true) },
                key = { idx -> uiState.resources[idx].id },
                row = { idx, showDivider ->
                    val resource = uiState.resources[idx]
                    ProfileResourceRow(
                        resource = resource,
                        onClick = { onResourceClick(resource.id) },
                        showDivider = showDivider
                    )
                }
            )

            3 -> item(key = "about") {
                Spacer(modifier = Modifier.height(18.dp))
                ProfileAbout(
                    profile = profile,
                    followerCount = uiState.followerCount,
                    repliesCount = uiState.repliesCount,
                    resourcesCount = uiState.resourcesCount
                )
            }
        }

        item(key = "bottom_spacer") {
            Spacer(
                modifier = Modifier
                    .navigationBarsPadding()
                    .height(72.dp)
            )
        }
    }
}

/**
 * One tab's worth of list: skeletons, then rows, then whatever comes after
 * them — a load-more button, a spinner, an empty state or a retry. All three
 * feeds behave identically, so they are described once.
 */
private fun LazyListScope.feedSection(
    prefix: String,
    count: Int,
    isLoading: Boolean,
    isLoaded: Boolean,
    hasMore: Boolean,
    error: String?,
    emptyIcon: androidx.compose.ui.graphics.vector.ImageVector,
    emptyTitle: String,
    emptySubtitle: String,
    errorTitle: String,
    onRetry: () -> Unit,
    onLoadMore: () -> Unit,
    skeleton: @Composable () -> Unit,
    key: (Int) -> String,
    row: @Composable (Int, Boolean) -> Unit
) {
    // First load: show the shape of what is coming rather than a spinner.
    if (count == 0 && isLoading) {
        items(4, key = { idx -> "${prefix}_skeleton_$idx" }) { skeleton() }
        return
    }

    if (count == 0 && error != null) {
        item(key = "${prefix}_error") {
            NebEmptyState(
                icon = Icons.Outlined.CloudOff,
                title = errorTitle,
                subtitle = error,
                action = {
                    NebButton(
                        text = "Try again",
                        onClick = onRetry,
                        tone = NebButtonTone.Outlined,
                        size = NebButtonSize.Small
                    )
                }
            )
        }
        return
    }

    if (count == 0 && isLoaded) {
        item(key = "${prefix}_empty") {
            NebEmptyState(icon = emptyIcon, title = emptyTitle, subtitle = emptySubtitle)
        }
        return
    }

    items(count, key = { idx -> "${prefix}_${key(idx)}" }) { idx ->
        row(idx, idx < count - 1 || hasMore)
    }

    when {
        isLoading -> item(key = "${prefix}_more_loading") {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 20.dp),
                contentAlignment = Alignment.Center
            ) {
                NebLoader(size = NebLoaderSize.Small)
            }
        }

        error != null -> item(key = "${prefix}_more_error") {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = error,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                NebButton(
                    text = "Try again",
                    onClick = onRetry,
                    tone = NebButtonTone.Outlined,
                    size = NebButtonSize.Small
                )
            }
        }

        hasMore -> item(key = "${prefix}_more") {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 14.dp),
                contentAlignment = Alignment.Center
            ) {
                NebButton(
                    text = "Show more",
                    onClick = onLoadMore,
                    tone = NebButtonTone.Outlined,
                    size = NebButtonSize.Small,
                    fillWidth = true
                )
            }
        }
    }
}

private fun postsLabel(count: Int): String = when (count) {
    0 -> "No posts"
    1 -> "1 post"
    else -> "$count posts"
}
