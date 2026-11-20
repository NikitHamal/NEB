package com.neb.ians.ui.screens.home

import com.neb.ians.ui.components.GateReason
import com.neb.ians.ui.components.LocalAuthGate
import com.neb.ians.ui.components.NebToastHost
import com.neb.ians.ui.theme.seasonAmbience
import com.neb.ians.ui.theme.hasGarland
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.ui.components.ConfirmDeleteDialog
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.ForumPostCard
import com.neb.ians.ui.components.NebChipGroup
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.ReportDialog
import com.neb.ians.ui.components.ShimmerHomeScreen
import com.neb.ians.ui.components.UserPopoverDialog
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.sharePost
import kotlinx.coroutines.launch
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebLoader

private const val FEED_PREFETCH_DISTANCE = 6

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onViewAllClick: () -> Unit,
    onNewsClick: () -> Unit = {},
    onUploadClick: () -> Unit = {},
    onNewsItemClick: (String) -> Unit = {},
    onPostClick: (String) -> Unit = {},
    onEditPostClick: (String) -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onUserProfileClick: (String) -> Unit = {},
    onSeeAllPeopleClick: () -> Unit = {},
    onCreatePostClick: () -> Unit = {},
    viewModel: HomeViewModel = hiltViewModel()
) {
    val gate = LocalAuthGate.current
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val suggestedPeers by viewModel.suggestedPeers.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    var deletingPostId by remember { mutableStateOf<String?>(null) }
    var reportPostId by remember { mutableStateOf<String?>(null) }
    var popoverUsername by remember { mutableStateOf<String?>(null) }
    var showTopicSheet by remember { mutableStateOf(false) }
    var isRefreshing by remember { mutableStateOf(false) }

    val listState = rememberLazyListState()
    LaunchedEffect(uiState.sort, uiState.selectedCategory) {
        listState.scrollToItem(0)
    }
    com.neb.ians.ui.components.TrackPostImpressions(
        listState = listState,
        postIdForKey = { (it as? String)?.takeIf { k -> k.startsWith("post_") }?.removePrefix("post_") },
        onVisible = viewModel::reportImpressions
    )
    HomeLoadMoreEffect(
        listState = listState,
        hasMorePosts = uiState.hasMorePosts,
        isLoadingMore = uiState.isLoadingMore,
        onLoadMore = viewModel::loadMore
    )

    LaunchedEffect(Unit) {
        viewModel.snackbarMessage.collect { message ->
            message?.let { snackbarHostState.showSnackbar(it) }
        }
    }

    val openCategories = remember { { showTopicSheet = true } }
    val onFollowPeer = remember(gate, viewModel) {
        { authorId: String -> gate.require(GateReason.Follow) { viewModel.toggleFollowUser(authorId) } }
    }

    Scaffold(
        snackbarHost = { NebToastHost(hostState = snackbarHostState) },
        topBar = {
            Column(modifier = Modifier.fillMaxWidth()) {
                WebTopBar(
                    onSearchClick = onSearchClick,
                    onUploadClick = onUploadClick,
                    onNotificationsClick = onNotificationsClick,
                    onProfileClick = onProfileClick,
                    avatarInitial = uiState.userName,
                    avatarUrl = uiState.userPhotoUrl
                )
                HomeFilterBarSlot(
                    listState = listState,
                    currentSort = uiState.sort,
                    selectedCategory = uiState.selectedCategory,
                    isRefreshing = uiState.isFilterRefreshing,
                    onSelectSort = viewModel::selectSort,
                    onOpenCategories = openCategories
                )
            }
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
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
                .padding(innerPadding)
        ) {
            when {
                uiState.isLoading -> ShimmerHomeScreen()
                uiState.error != null && uiState.popularResources.isEmpty() && uiState.recentPosts.isEmpty() -> {
                    Box(modifier = Modifier.fillMaxSize().padding(16.dp)) {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = { viewModel.refresh() }
                        )
                    }
                }
                else -> {
                    val feedPosts = uiState.recentPosts
                    val suggestedResources = remember(uiState.recentResources, uiState.popularResources) {
                        (uiState.popularResources + uiState.recentResources).distinctBy { it.id }
                    }
                    val feedEntries = remember(
                        feedPosts,
                        uiState.currentUserId,
                        suggestedResources,
                        uiState.recentResources,
                        uiState.latestNews,
                        suggestedPeers,
                        uiState.sort,
                        uiState.selectedCategory
                    ) {
                        buildHomeFeed(
                            posts = feedPosts,
                            currentUserId = uiState.currentUserId,
                            suggestedResources = suggestedResources,
                            recentResources = uiState.recentResources,
                            news = uiState.latestNews,
                            peers = suggestedPeers,
                            sort = uiState.sort,
                            selectedCategory = uiState.selectedCategory
                        )
                    }

                    val siteTheme = com.neb.ians.ui.theme.LocalSiteTheme.current
                    LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize().homeSeasonAmbience(listState),
                        verticalArrangement = Arrangement.spacedBy(0.dp),
                        contentPadding = PaddingValues(
                            top = if (siteTheme.hasGarland) 36.dp else 0.dp,
                            bottom = 24.dp
                        )
                    ) {
                        if (siteTheme.festive && siteTheme.cardOpen) {
                            item(key = "season_card") {
                                com.neb.ians.ui.theme.SeasonCard(
                                    onAction = { url ->
                                        when {
                                            "forum" in url -> onCreatePostClick()
                                            "library" in url -> onViewAllClick()
                                            else -> runCatching {
                                                val full = if (url.startsWith("http")) url else "https://nebians.consica.com.np$url"
                                                context.startActivity(android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(full)))
                                            }
                                        }
                                    },
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp).animateItem()
                                )
                            }
                        }
                        if (uiState.error != null) {
                            item(key = "partial_error") {
                                ErrorCard(
                                    message = uiState.error ?: "Some content could not be loaded",
                                    onRetry = { viewModel.refresh() },
                                    modifier = Modifier.padding(horizontal = 16.dp)
                                )
                            }
                        }

                        if (feedEntries.isEmpty()) {
                            item(key = "feed_empty") {
                                WebEmptyState(
                                    title = if (uiState.selectedCategory != null) "No posts in #${uiState.selectedCategory}" else "No posts available",
                                    message = if (uiState.selectedCategory != null) "Try another topic or start the first discussion in this subject." else "Ask a question, share study notes or start a discussion.",
                                    icon = painterResource(id = R.drawable.ic_forum_outlined),
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)
                                )
                            }
                        } else {
                            items(
                                items = feedEntries,
                                key = { it.key },
                                contentType = { it.contentType }
                            ) { entry ->
                                when (entry) {
                                    is HomeFeedEntry.Post -> ForumPostCard(
                                        post = entry.post,
                                        isOwnPost = entry.isOwnPost,
                                        onClick = {
                                            com.neb.ians.ui.components.PostReachHints.set(entry.post.id, "feed")
                                            onPostClick(entry.post.id)
                                        },
                                        onLikeClick = { gate.require(GateReason.Like) { viewModel.toggleThumbsUp(entry.post.id) } },
                                        onBookmarkClick = { gate.require(GateReason.Save) { viewModel.toggleBookmark(entry.post.id) } },
                                        onShareClick = { sharePost(context, entry.post.id) },
                                        onReportClick = { reportPostId = entry.post.id },
                                        onEditClick = { onEditPostClick(entry.post.id) },
                                        onArchiveClick = { viewModel.archivePost(entry.post.id) },
                                        onDeleteClick = { deletingPostId = entry.post.id },
                                        onAuthorClick = { onUserProfileClick(entry.post.authorName) },
                                        onAuthorLongPress = { popoverUsername = entry.post.authorName }
                                    )

                                    is HomeFeedEntry.ResourceCarousel -> Column(
                                        modifier = Modifier.padding(vertical = 14.dp),
                                        verticalArrangement = Arrangement.spacedBy(10.dp)
                                    ) {
                                        HomeSectionTitle(
                                            title = "Suggested for you",
                                            actionLabel = "See all",
                                            onActionClick = onViewAllClick
                                        )
                                        HomeResourceCarousel(
                                            resources = entry.resources,
                                            onResourceClick = onResourceClick
                                        )
                                    }

                                    is HomeFeedEntry.News -> HomeNewsSection(
                                        items = entry.items,
                                        onViewAllClick = onNewsClick,
                                        onNewsClick = { news -> onNewsItemClick(news.slug) },
                                        modifier = Modifier.padding(vertical = 14.dp)
                                    )

                                    is HomeFeedEntry.Peers -> Box(modifier = Modifier.padding(vertical = 14.dp)) {
                                        HomeSuggestedPeersRail(
                                            peers = entry.peers,
                                            onPeerClick = onUserProfileClick,
                                            onFollowClick = onFollowPeer,
                                            onSeeAllClick = onSeeAllPeopleClick
                                        )
                                    }

                                    is HomeFeedEntry.ResourceHighlight -> Box(modifier = Modifier.padding(vertical = 14.dp)) {
                                        if (entry.titled) {
                                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                                HomeSectionTitle(
                                                    title = "Featured study guide",
                                                    actionLabel = "See all",
                                                    onActionClick = onViewAllClick
                                                )
                                                HomeFeedResourceHighlight(
                                                    resource = entry.resource,
                                                    onClick = { onResourceClick(entry.resource.id) }
                                                )
                                            }
                                        } else {
                                            HomeFeedResourceHighlight(
                                                resource = entry.resource,
                                                onClick = { onResourceClick(entry.resource.id) }
                                            )
                                        }
                                    }

                                    is HomeFeedEntry.NewResources -> Box(modifier = Modifier.padding(vertical = 14.dp)) {
                                        HomeNewResourcesRail(
                                            resources = entry.resources,
                                            onViewAllClick = onViewAllClick,
                                            onResourceClick = onResourceClick
                                        )
                                    }
                                }
                            }
                        }

                        // Infinite scroll loader
                        if (uiState.isLoadingMore) {
                            item(key = "loading_more") {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.Center,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    NebLoader(size = NebLoaderSize.Inline, color = MaterialTheme.colorScheme.primary)
                                    Spacer(Modifier.size(10.dp))
                                    Text(
                                        text = "Loading more updates...",
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }

                        // End of feed card when reached limit
                        if (!uiState.hasMorePosts && feedPosts.isNotEmpty()) {
                            item(key = "end_of_feed") {
                                HomeEndOfFeedCard(
                                    onViewAllClick = onViewAllClick,
                                    onCreatePostClick = onCreatePostClick,
                                    selectedCategory = uiState.selectedCategory,
                                    onClearFilters = viewModel::clearFilters
                                )
                            }
                        }

                        item(key = "bottom_spacing") {
                            Spacer(Modifier.navigationBarsPadding().height(96.dp))
                        }
                    }
                }
            }
        }
    }

    reportPostId?.let { postId ->
        ReportDialog(
            onDismiss = { reportPostId = null },
            onSubmit = { reason, description ->
                viewModel.reportPost(postId, reason, description)
                reportPostId = null
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

    if (showTopicSheet) {
        NebModalSheet(
            onDismiss = { showTopicSheet = false },
            title = "Filter by topic",
            showClose = true
        ) {
            NebChipGroup(
                options = listOf("All") + HomeUiState.CATEGORIES,
                selected = uiState.selectedCategory ?: "All",
                onSelect = { picked ->
                    viewModel.selectCategory(if (picked == null || picked == "All") null else picked)
                    showTopicSheet = false
                },
                toggleable = true
            )
        }
    }
}

@Composable
private fun HomeFilterBarSlot(
    listState: androidx.compose.foundation.lazy.LazyListState,
    currentSort: String,
    selectedCategory: String?,
    isRefreshing: Boolean,
    onSelectSort: (String) -> Unit,
    onOpenCategories: () -> Unit
) {
    val isScrolled by remember(listState) {
        derivedStateOf { listState.firstVisibleItemIndex > 0 || listState.firstVisibleItemScrollOffset > 8 }
    }
    HomePostsFilterBar(
        currentSort = currentSort,
        selectedCategory = selectedCategory,
        isRefreshing = isRefreshing,
        scrolled = isScrolled,
        onSelectSort = onSelectSort,
        onOpenCategories = onOpenCategories
    )
}

@Composable
private fun HomeLoadMoreEffect(
    listState: androidx.compose.foundation.lazy.LazyListState,
    hasMorePosts: Boolean,
    isLoadingMore: Boolean,
    onLoadMore: () -> Unit
) {
    val shouldLoadMore by remember(listState) {
        derivedStateOf {
            val layout = listState.layoutInfo
            val totalItems = layout.totalItemsCount
            val lastVisibleItemIndex = layout.visibleItemsInfo.lastOrNull()?.index ?: 0
            totalItems > 0 && lastVisibleItemIndex >= totalItems - FEED_PREFETCH_DISTANCE
        }
    }
    LaunchedEffect(shouldLoadMore, hasMorePosts, isLoadingMore) {
        if (shouldLoadMore && hasMorePosts && !isLoadingMore) {
            onLoadMore()
        }
    }
}

@Composable
private fun Modifier.homeSeasonAmbience(listState: androidx.compose.foundation.lazy.LazyListState): Modifier {
    val siteTheme = com.neb.ians.ui.theme.LocalSiteTheme.current
    if (!siteTheme.festive) return this
    val homeAtTop by remember(listState) { derivedStateOf { listState.firstVisibleItemIndex == 0 } }
    return this.seasonAmbience(homeAtTop)
}
