@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)

package com.neb.ians.ui.screens.profile

import com.neb.ians.ui.components.nebToast
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.statusBars
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
import com.neb.ians.ui.components.WebResourceCard
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

private const val PROFILE_LINK_BASE = "https://nebians.consica.com.np/app/profile/"

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
    val profile = uiState.profile
    val isSelf = profile?.isSelf == true

    var showCovers by remember { mutableStateOf(false) }
    val density = androidx.compose.ui.platform.LocalDensity.current
    val screenWidth = androidx.compose.ui.platform.LocalConfiguration.current.screenWidthDp.dp
    val statusPx = WindowInsets.statusBars.getTop(density)
    // The bar turns solid as the cover's lower edge slides under it. Read only while drawing the bar.
    val barProgress: () -> Float = remember(density, screenWidth, statusPx) {
        val coverPx = statusPx + with(density) { com.neb.ians.ui.components.profileCoverHeight(screenWidth, statusPx.toDp()).toPx() }
        val barBottom = statusPx + with(density) { 56.dp.toPx() }
        // The bar stays away until the name in the header has slid under it (cover, avatar overhang and the name row), then fades in.
        val start = coverPx + with(density) { 72.dp.toPx() } - barBottom
        val range = with(density) { 56.dp.toPx() }
        val read: () -> Float = {
            if (listState.firstVisibleItemIndex > 0) 1f
            else ((listState.firstVisibleItemScrollOffset - start) / range).coerceIn(0f, 1f)
        }
        read
    }

    Scaffold(
        contentWindowInsets = androidx.compose.foundation.layout.WindowInsets(0, 0, 0, 0),
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Box(Modifier.fillMaxSize()) {
        com.neb.ians.ui.components.NebRefreshBox(
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
                .then(if (profile == null) Modifier.statusBarsPadding().padding(top = 48.dp) else Modifier)
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
                    onSocialLinkClick = { link -> viewModel.trackSocialClick(link, profile.id) },
                    onBack = onNavigateBack,
                    onCopyLink = {
                        clipboard.setText(AnnotatedString("$PROFILE_LINK_BASE${profile.username}/"))
                        context.nebToast("Profile link copied")
                    },
                    onAnalytics = if (isSelf) onAnalyticsClick else null,
                    onChangeCover = { showCovers = true }
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
        if (profile == null) {
            IconButton(onClick = onNavigateBack, modifier = Modifier.statusBarsPadding().padding(4.dp)) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
            }
        } else {
            val actions = remember(isSelf, profile.username) {
                buildList {
                    if (isSelf) add(ProfileBarAction(Icons.Outlined.BarChart, "Analytics", onAnalyticsClick))
                    add(ProfileBarAction(Icons.Outlined.Link, "Copy profile link") {
                        clipboard.setText(AnnotatedString("$PROFILE_LINK_BASE${profile.username}/"))
                        context.nebToast("Profile link copied")
                    })
                }
            }
            ProfileTopBar(
                progress = barProgress,
                name = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username,
                photoUrl = profile.photoUrl,
                badge = remember(profile) { buildBadgeInfo(profile) },
                verified = profile.verificationLevel > 0,
                onBack = onNavigateBack,
                actions = actions,
                modifier = Modifier.align(Alignment.TopCenter)
            )
        }
        }
    }

    if (showCovers && profile != null && isSelf) {
        CoverPickerSheet(
            currentId = profile.coverArt,
            onPick = { viewModel.setCoverArt(it); showCovers = false },
            onDefault = { viewModel.setCoverArt(""); showCovers = false },
            onDismiss = { showCovers = false }
        )
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
    onSocialLinkClick: (com.neb.ians.data.api.ApiSocialLink) -> Unit,
    onBack: () -> Unit,
    onCopyLink: () -> Unit,
    onAnalytics: (() -> Unit)?,
    onChangeCover: () -> Unit
) {
    val profile = uiState.profile ?: return
    val isSelf = profile.isSelf == true
    val isPrivate = profile.isLocked == 1 && !isSelf && !uiState.isFollowing
    val handle = "@${profile.username}"
    // An institution's page is its portfolio: open on About the first time.
    androidx.compose.runtime.LaunchedEffect(profile.id) {
        if (profile.role == "institution" && !profile.schoolSlug.isNullOrBlank() && uiState.selectedTab == ProfileTab.OVERVIEW) onTabSelected(ProfileTab.ABOUT)
    }

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
                onSocialLinkClick = onSocialLinkClick,
                onBack = onBack,
                onCopyLink = onCopyLink,
                onAnalytics = onAnalytics,
                onChangeCover = if (isSelf) onChangeCover else null
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
                        NebRailTab("Overview"),
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
            ProfileTab.OVERVIEW -> overviewTab(
                profile = profile, isSelf = isSelf, uiState = uiState,
                onEditProfile = onEditProfile, onPostClick = onPostClick, onResourceClick = onResourceClick,
                onProfileClick = onProfileClick, onTabSelected = onTabSelected
            )
            ProfileTab.POSTS -> feedSection(
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
                skeleton = { ProfileCardSkeleton() },
                key = { idx -> uiState.posts[idx].id },
                row = { idx ->
                    val post = uiState.posts[idx]
                    ProfilePostCard(post = post, onClick = { onPostClick(post.id) })
                }
            )

            ProfileTab.REPLIES -> feedSection(
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
                row = { idx ->
                    val reply = uiState.replies[idx]
                    ProfileReplyCard(reply = reply, onClick = { onPostClick(reply.postId) })
                }
            )

            ProfileTab.RESOURCES -> feedSection(
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
                skeleton = { ProfileCardSkeleton() },
                key = { idx -> uiState.resources[idx].id },
                row = { idx ->
                    val resource = uiState.resources[idx]
                    WebResourceCard(
                        resource = resource,
                        onClick = { onResourceClick(resource.id) },
                        minWidth = null
                    )
                }
            )

            ProfileTab.ABOUT -> {
                val instSlug = profile.schoolSlug.orEmpty()
                if (profile.role == "institution" && instSlug.isNotBlank()) {
                    item(key = "about_institution") {
                        CardSlot {
                            com.neb.ians.ui.screens.institutions.InstitutionPortfolioHost(
                                slug = instSlug, load = true,
                                vm = androidx.hilt.navigation.compose.hiltViewModel(key = "inst_$instSlug")
                            )
                        }
                    }
                } else {
                    if (isSelf) item(key = "about_strength") {
                        CardSlot { ProfileStrengthCard(profile = profile, onEditProfile = onEditProfile) }
                    }
                    item(key = "about_portfolio") {
                        CardSlot { ProfilePortfolioCard(profile = profile, isSelf = isSelf, onEditProfile = onEditProfile) }
                    }
                }
                item(key = "about_stats") {
                    CardSlot { AboutStatsCard(profile = profile, followerCount = uiState.followerCount) }
                }
                item(key = "about_achievements") {
                    CardSlot { AboutAchievementsCard(profile = profile) }
                }
                item(key = "about_details") {
                    CardSlot { AboutDetailsCard(profile = profile, onProfileClick = onProfileClick) }
                }
                item(key = "about_progress") {
                    CardSlot { AboutProgressCard(profile = profile) }
                }
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
    row: @Composable (Int) -> Unit
) {
    // First load: show the shape of what is coming rather than a spinner.
    if (count == 0 && isLoading) {
        items(4, key = { idx -> "${prefix}_skeleton_$idx" }, contentType = { "${prefix}_skeleton" }) { CardSlot { skeleton() } }
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

    items(count, key = { idx -> "${prefix}_${key(idx)}" }, contentType = { prefix }) { idx ->
        CardSlot { row(idx) }
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

/**
 * Where a card sits in the feed. The header runs edge to edge, so the cards
 * need their own inset -- the same 16dp the forum and library use, with 6dp
 * above and below so stacked cards sit 12dp apart.
 */
@Composable
private fun CardSlot(content: @Composable () -> Unit) {
    Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp)) { content() }
}

private fun postsLabel(count: Int): String = when (count) {
    0 -> "No posts"
    1 -> "1 post"
    else -> "$count posts"
}
