package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.ShimmerForumList
import com.neb.ians.ui.components.WebChipRow
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPostCard
import com.neb.ians.ui.components.WebTopBar

@Composable
fun ForumScreen(
    onPostClick: (String) -> Unit,
    onCreatePostClick: () -> Unit,
    onSearchClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    viewModel: ForumViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

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
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Forum",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.ExtraBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "Ask questions, share solutions, and follow classroom discussions.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                WebOutlinedButton(
                    text = "New Post",
                    imageVector = Icons.Filled.Add,
                    onClick = onCreatePostClick
                )
            }

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
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(start = 16.dp, top = 4.dp, end = 16.dp, bottom = 112.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        if (uiState.error != null) {
                            item {
                                ErrorCard(
                                    message = uiState.error ?: "Something went wrong",
                                    onRetry = { viewModel.refresh() }
                                )
                            }
                        }
                        items(uiState.posts, key = { it.id }) { post ->
                            WebPostCard(
                                post = post,
                                onClick = { onPostClick(post.id) },
                                onLikeClick = { viewModel.toggleThumbsUp(post.id) }
                            )
                        }
                    }
                }
            }
        }
    }
}
