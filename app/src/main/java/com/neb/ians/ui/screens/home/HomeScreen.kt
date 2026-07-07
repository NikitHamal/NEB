package com.neb.ians.ui.screens.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.ui.components.ConfirmDeleteDialog
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.ForumPostCard
import com.neb.ians.ui.components.ShimmerHomeScreen
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.WebSectionHeader
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.sharePost

@Composable
fun HomeScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onViewAllClick: () -> Unit,
    onSubjectClick: (String) -> Unit = {},
    onForumClick: () -> Unit = {},
    onStudyLabClick: () -> Unit = {},
    onNebyAiClick: () -> Unit = {},
    onNewsClick: () -> Unit = {},
    onResultCheckerClick: () -> Unit = {},
    onNewsItemClick: (String) -> Unit = {},
    onPostClick: (String) -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    onUserProfileClick: (String) -> Unit = {},
    viewModel: HomeViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val snackbarHostState = remember { SnackbarHostState() }
    var deletingPostId by remember { mutableStateOf<String?>(null) }

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
                onNotificationsClick = onNotificationsClick,
                onProfileClick = onProfileClick,
                avatarInitial = uiState.userName,
                avatarUrl = uiState.userPhotoUrl
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
        ) {
            when {
                uiState.isLoading -> ShimmerHomeScreen()
                uiState.error != null && uiState.recentResources.isEmpty() && uiState.recentPosts.isEmpty() -> {
                    ErrorCard(
                        message = uiState.error ?: "Something went wrong",
                        onRetry = { viewModel.refresh() },
                        modifier = Modifier.padding(16.dp)
                    )
                }
                else -> {
                    if (uiState.error != null) {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = { viewModel.refresh() },
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                        )
                    }

                    HomeHero(
                        userName = uiState.userName
                    )

                    HomeNewsSection(
                        items = uiState.latestNews,
                        onViewAllClick = onNewsClick,
                        onNewsClick = { news -> onNewsItemClick(news.slug) },
                        onResultCheckerClick = onResultCheckerClick
                    )

                    if (uiState.latestNews.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(18.dp))
                    }

                    WebSectionHeader(
                        title = "Recent Resources",
                        actionLabel = "View all",
                        onActionClick = onViewAllClick
                    )
                    ResourceRow(
                        resources = uiState.recentResources,
                        emptyMessage = "No resources yet. Check the Library to explore.",
                        onResourceClick = onResourceClick
                    )

                    Spacer(modifier = Modifier.height(18.dp))
                    WebSectionHeader(
                        title = "Popular Resources",
                        actionLabel = "View all",
                        onActionClick = onViewAllClick
                    )
                    ResourceRow(
                        resources = uiState.popularResources,
                        emptyMessage = "Popular resources will appear here.",
                        onResourceClick = onResourceClick
                    )

                    Spacer(modifier = Modifier.height(18.dp))
                    WebSectionHeader(
                        title = "Trending Discussions",
                        actionLabel = "View all",
                        onActionClick = onForumClick
                    )

                    if (uiState.recentPosts.isEmpty()) {
                        WebEmptyState(
                            title = "No discussions yet",
                            message = "Start a question or browse the forum when posts appear.",
                            icon = painterResource(id = R.drawable.ic_forum_outlined),
                            modifier = Modifier.padding(horizontal = 16.dp)
                        )
                    } else {
                        val trendingPosts = remember(uiState.recentPosts) { uiState.recentPosts.take(4) }
                        Column(
                            modifier = Modifier.padding(horizontal = 16.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            trendingPosts.forEach { post ->
                                ForumPostCard(
                                    post = post,
                                    isOwnPost = uiState.currentUserId != null && post.authorId == uiState.currentUserId,
                                    onClick = { onPostClick(post.id) },
                                    onLikeClick = { viewModel.toggleThumbsUp(post.id) },
                                    onBookmarkClick = { viewModel.toggleBookmark(post.id) },
                                    onShareClick = { sharePost(context, post.id) },
                                    onReportClick = {},
                                    onDeleteClick = { deletingPostId = post.id },
                                    onAuthorClick = { onUserProfileClick(post.authorName) }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(110.dp))
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

@Composable
private fun HomeHero(
    userName: String
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Welcome to NEBians",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.ExtraBold,
            color = MaterialTheme.colorScheme.onSurface,
            textAlign = TextAlign.Center,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
    }
}


@Composable
private fun ResourceRow(
    resources: List<com.neb.ians.data.api.ApiResource>,
    emptyMessage: String,
    onResourceClick: (String) -> Unit
) {
    if (resources.isEmpty()) {
        WebEmptyState(
            title = "Nothing here yet",
            message = emptyMessage,
            icon = painterResource(id = R.drawable.ic_document),
            modifier = Modifier.padding(horizontal = 16.dp)
        )
    } else {
        val rowItems = remember(resources) { resources.take(12) }
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(rowItems, key = { it.id }) { resource ->
                WebResourceCard(
                    resource = resource,
                    onClick = { onResourceClick(resource.id) },
                    minWidth = 224.dp
                )
            }
        }
    }
}
