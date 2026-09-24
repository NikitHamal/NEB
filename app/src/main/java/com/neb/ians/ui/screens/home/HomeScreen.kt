package com.neb.ians.ui.screens.home

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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
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
import com.neb.ians.ui.components.ShimmerHomeScreen
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.sharePost
import kotlinx.coroutines.launch

private const val FEED_PREFETCH_DISTANCE = 6

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onViewAllClick: () -> Unit,
    onForumClick: () -> Unit = {},
    onCanvasClick: () -> Unit = {},
    onStudyLabClick: () -> Unit = {},
    onNebyAiClick: () -> Unit = {},
    onNewsClick: () -> Unit = {},
    onUploadClick: () -> Unit = {},
    onNewsItemClick: (String) -> Unit = {},
    onPostClick: (String) -> Unit = {},
    onEditPostClick: (String) -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onUserProfileClick: (String) -> Unit = {},
    onSeeAllPeopleClick: () -> Unit = {},
    viewModel: HomeViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val suggestedPeers by viewModel.suggestedPeers.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    var deletingPostId by remember { mutableStateOf<String?>(null) }
    var isRefreshing by remember { mutableStateOf(false) }

    val listState = rememberLazyListState()
    val shouldLoadMore by remember {
        derivedStateOf {
            val layout = listState.layoutInfo
            val totalItems = layout.totalItemsCount
            val lastVisibleItemIndex = layout.visibleItemsInfo.lastOrNull()?.index ?: 0
            totalItems > 0 && lastVisibleItemIndex >= totalItems - FEED_PREFETCH_DISTANCE
        }
    }

    LaunchedEffect(shouldLoadMore, uiState.hasMorePosts, uiState.isLoadingMore) {
        if (shouldLoadMore && uiState.hasMorePosts && !uiState.isLoadingMore) {
            viewModel.loadMore()
        }
    }

    LaunchedEffect(Unit) {
        viewModel.snackbarMessage.collect { message ->
            message?.let { snackbarHostState.showSnackbar(it) }
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(hostState = snackbarHostState) },
        topBar = {
            WebTopBar(
                onSearchClick = onSearchClick,
                onUploadClick = onUploadClick,
                onNotificationsClick = onNotificationsClick,
                onProfileClick = onProfileClick,
                avatarInitial = uiState.userName,
                avatarUrl = uiState.userPhotoUrl
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLow
    ) { innerPadding ->
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
                        suggestedPeers
                    ) {
                        buildHomeFeed(
                            posts = feedPosts,
                            currentUserId = uiState.currentUserId,
                            suggestedResources = suggestedResources,
                            recentResources = uiState.recentResources,
                            news = uiState.latestNews,
                            peers = suggestedPeers
                        )
                    }

                    LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.spacedBy(16.dp),
                        contentPadding = PaddingValues(top = 10.dp, bottom = 24.dp)
                    ) {
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
                                    title = "No posts available",
                                    message = "Be the first to ask a question, share notes or start a discussion!",
                                    icon = painterResource(id = R.drawable.ic_forum_outlined),
                                    modifier = Modifier.padding(horizontal = 16.dp)
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
                                        onClick = { onPostClick(entry.post.id) },
                                        onLikeClick = { viewModel.toggleThumbsUp(entry.post.id) },
                                        onBookmarkClick = { viewModel.toggleBookmark(entry.post.id) },
                                        onShareClick = { sharePost(context, entry.post.id) },
                                        onReportClick = {},
                                        onEditClick = { onEditPostClick(entry.post.id) },
                                        onDeleteClick = { deletingPostId = entry.post.id },
                                        onAuthorClick = { onUserProfileClick(entry.post.authorName) },
                                        modifier = Modifier.padding(horizontal = 16.dp)
                                    )

                                    is HomeFeedEntry.ResourceCarousel -> Column(
                                        verticalArrangement = Arrangement.spacedBy(10.dp)
                                    ) {
                                        HomeSectionTitle(
                                            title = "Suggested for you",
                                            actionLabel = "See All",
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
                                        onNewsClick = { news -> onNewsItemClick(news.slug) }
                                    )

                                    is HomeFeedEntry.Peers -> HomeSuggestedPeersRail(
                                        peers = entry.peers,
                                        onPeerClick = onUserProfileClick,
                                        onFollowClick = { authorId -> viewModel.toggleFollowUser(authorId) },
                                        onSeeAllClick = onSeeAllPeopleClick
                                    )

                                    is HomeFeedEntry.ResourceHighlight -> if (entry.titled) {
                                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                            HomeSectionTitle(
                                                title = "Featured Study Guide",
                                                actionLabel = "See All",
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

                                    is HomeFeedEntry.NewResources -> HomeNewResourcesRail(
                                        resources = entry.resources,
                                        onViewAllClick = onViewAllClick,
                                        onResourceClick = onResourceClick
                                    )
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
                                    CircularProgressIndicator(
                                        modifier = Modifier.size(20.dp),
                                        strokeWidth = 2.dp,
                                        color = MaterialTheme.colorScheme.primary
                                    )
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
                                    onForumClick = onForumClick,
                                    onViewAllClick = onViewAllClick
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
}
