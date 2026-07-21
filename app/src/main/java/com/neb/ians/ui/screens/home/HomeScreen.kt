package com.neb.ians.ui.screens.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onViewAllClick: () -> Unit,
    onForumClick: () -> Unit = {},
    onNewsClick: () -> Unit = {},
    onUploadClick: () -> Unit = {},
    onNewsItemClick: (String) -> Unit = {},
    onPostClick: (String) -> Unit = {},
    onEditPostClick: (String) -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onUserProfileClick: (String) -> Unit = {},
    viewModel: HomeViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    var deletingPostId by remember { mutableStateOf<String?>(null) }
    var isRefreshing by remember { mutableStateOf(false) }

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
        containerColor = MaterialTheme.colorScheme.surface
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
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.spacedBy(18.dp)
                    ) {
                        item(key = "top_spacing") { Spacer(Modifier.height(2.dp)) }

                        if (uiState.error != null) {
                            item(key = "partial_error") {
                                ErrorCard(
                                    message = uiState.error ?: "Some content could not be loaded",
                                    onRetry = { viewModel.refresh() },
                                    modifier = Modifier.padding(horizontal = 16.dp)
                                )
                            }
                        }

                        item(key = "suggested_title") {
                            HomeSectionTitle(
                                title = "Suggested for you",
                                actionLabel = "Explore",
                                onActionClick = onViewAllClick
                            )
                        }
                        when {
                            uiState.suggestedItems.isNotEmpty() -> {
                                item(key = "suggested_deck") {
                                    HomeSuggestedDeck(
                                        items = uiState.suggestedItems,
                                        onResourceClick = onResourceClick,
                                        onPostClick = onPostClick,
                                        onLikeClick = { viewModel.toggleThumbsUp(it) }
                                    )
                                }
                            }
                            uiState.recentResources.isNotEmpty() -> {
                                // Fallback while the suggestion engine has no
                                // cached deck yet (first ever launch / offline)
                                // — the rail is never empty when content exists.
                                item(key = "suggested_fallback") {
                                    HomeResourceCarousel(
                                        resources = (uiState.recentResources + uiState.popularResources).distinctBy { it.id },
                                        onResourceClick = onResourceClick
                                    )
                                }
                            }
                            else -> {
                                item(key = "suggested_empty") {
                                    WebEmptyState(
                                        title = "New content is on the way",
                                        message = "Browse the library or pull down to check again.",
                                        icon = painterResource(id = R.drawable.ic_document),
                                        modifier = Modifier.padding(horizontal = 16.dp)
                                    )
                                }
                            }
                        }

                        if (uiState.popularResources.isNotEmpty()) {
                            item(key = "trending_title") {
                                HomeSectionTitle(
                                    title = "Trending now",
                                    actionLabel = "View all",
                                    onActionClick = onViewAllClick
                                )
                            }
                            item(key = "trending_resources") {
                                HomeResourceCarousel(
                                    resources = uiState.popularResources,
                                    onResourceClick = onResourceClick
                                )
                            }
                        }

                        if (uiState.latestNews.isNotEmpty()) {
                            item(key = "news") {
                                HomeNewsSection(
                                    items = uiState.latestNews,
                                    onViewAllClick = onNewsClick,
                                    onNewsClick = { news -> onNewsItemClick(news.slug) }
                                )
                            }
                        }

                        item(key = "discussion_title") {
                            HomeSectionTitle(
                                title = "Trending discussions",
                                actionLabel = "Forum",
                                onActionClick = onForumClick
                            )
                        }

                        if (uiState.recentPosts.isEmpty()) {
                            item(key = "discussion_empty") {
                                WebEmptyState(
                                    title = "No discussions yet",
                                    message = "Start a question or browse the forum when posts appear.",
                                    icon = painterResource(id = R.drawable.ic_forum_outlined),
                                    modifier = Modifier.padding(horizontal = 16.dp)
                                )
                            }
                        } else {
                            items(
                                items = uiState.recentPosts.take(3),
                                key = { "discussion_${it.id}" }
                            ) { post ->
                                ForumPostCard(
                                    post = post,
                                    isOwnPost = post.isOwner || (uiState.currentUserId != null && post.authorId == uiState.currentUserId),
                                    onClick = { onPostClick(post.id) },
                                    onLikeClick = { viewModel.toggleThumbsUp(post.id) },
                                    onBookmarkClick = { viewModel.toggleBookmark(post.id) },
                                    onShareClick = { sharePost(context, post.id) },
                                    onReportClick = {},
                                    onEditClick = { onEditPostClick(post.id) },
                                    onDeleteClick = { deletingPostId = post.id },
                                    onAuthorClick = { onUserProfileClick(post.authorName) },
                                    modifier = Modifier.padding(horizontal = 16.dp)
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
