package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.FolderOpen
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.ScrollableTabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebResourceCard

@Composable
fun ProfileScreen(
    username: String,
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

    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentAlignment = Alignment.Center
        ) {
            when {
                uiState.isLoading -> CircularProgressIndicator()
                uiState.error != null -> WebEmptyState(
                    title = "Profile unavailable",
                    message = uiState.error ?: "Try again later.",
                    icon = painterResource(id = R.drawable.ic_school)
                )
                uiState.profile != null -> ProfileContent(
                    uiState = uiState,
                    onEditProfile = onEditProfile,
                    onFollowClick = viewModel::toggleFollow,
                    onPostClick = onPostClick,
                    onResourceClick = onResourceClick,
                    onTabSelected = viewModel::selectTab,
                    onLoadMorePosts = { viewModel.loadPosts(reset = false) },
                    onLoadMoreReplies = { viewModel.loadReplies(reset = false) },
                    onLoadMoreResources = { viewModel.loadResources(reset = false) },
                    onAvatarClick = viewModel::openPhotoGallery,
                    onNavigateBack = onNavigateBack,
                    onAnalyticsClick = onAnalyticsClick
                )
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
}

@Composable
private fun ProfileContent(
    uiState: ProfileUiState,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    onPostClick: (String) -> Unit,
    onResourceClick: (String) -> Unit,
    onTabSelected: (Int) -> Unit,
    onLoadMorePosts: () -> Unit,
    onLoadMoreReplies: () -> Unit,
    onLoadMoreResources: () -> Unit,
    onAvatarClick: () -> Unit,
    onNavigateBack: () -> Unit,
    onAnalyticsClick: () -> Unit
) {
    val profile = uiState.profile ?: return
    val isSelf = profile.isSelf == true
    val isPrivate = profile.isLocked == 1 && !isSelf

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item(key = "header") {
            ProfileHeaderCard(
                profile = profile,
                isSelf = isSelf,
                isFollowing = uiState.isFollowing,
                followerCount = uiState.followerCount,
                onEditProfile = onEditProfile,
                onFollowClick = onFollowClick,
                onAvatarClick = onAvatarClick,
                onNavigateBack = onNavigateBack,
                onAnalyticsClick = onAnalyticsClick
            )
        }

        if (isPrivate) {
            item(key = "private") {
                PrivateProfileNotice()
            }
        } else {
            item(key = "tabs") {
                ScrollableTabRow(
                    selectedTabIndex = uiState.selectedTab,
                    containerColor = MaterialTheme.colorScheme.surface,
                    edgePadding = 16.dp,
                    divider = { HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant) }
                ) {
                    listOf("Posts", "Replies", "Resources", "About").forEachIndexed { index, label ->
                        val isSelected = uiState.selectedTab == index
                        val count = when (index) {
                            0 -> profile.postCount
                            1 -> uiState.repliesCount
                            2 -> uiState.resourcesCount
                            else -> 0
                        }
                        Tab(
                            selected = isSelected,
                            onClick = { onTabSelected(index) },
                            text = {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                                ) {
                                    Text(
                                        text = label,
                                        fontWeight = if (isSelected) FontWeight.ExtraBold else FontWeight.SemiBold,
                                        style = MaterialTheme.typography.labelLarge
                                    )
                                    if (index < 3) {
                                        Surface(
                                            shape = CircleShape,
                                            color = if (isSelected) MaterialTheme.colorScheme.primary
                                                    else MaterialTheme.colorScheme.surfaceContainerHigh,
                                            contentColor = if (isSelected) Color.White
                                                          else MaterialTheme.colorScheme.onSurfaceVariant,
                                            modifier = Modifier.defaultMinSize(minWidth = 18.dp, minHeight = 18.dp)
                                        ) {
                                            Box(
                                                contentAlignment = Alignment.Center,
                                                modifier = Modifier.padding(horizontal = 4.dp)
                                            ) {
                                                Text(
                                                    text = count.toString(),
                                                    style = MaterialTheme.typography.labelSmall,
                                                    fontWeight = FontWeight.Bold
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                        )
                    }
                }
            }

            when (uiState.selectedTab) {
                0 -> {
                    if (uiState.posts.isEmpty() && !uiState.postsLoading && uiState.postsLoaded) {
                        item(key = "posts_empty") {
                            ProfileEmptyTabBox(
                                title = "No activity yet",
                                message = "Posts and replies will appear here",
                                icon = Icons.Outlined.Edit
                            )
                        }
                    }
                    items(uiState.posts.size, key = { idx -> "post_${uiState.posts[idx].id}" }) { idx ->
                        val post = uiState.posts[idx]
                        ProfilePostCard(post = post, onClick = { onPostClick(post.id) })
                    }
                    if (uiState.postsLoading) {
                        item(key = "posts_loading") { ProfileProgressIndicator() }
                    } else if (uiState.postsHasMore) {
                        item(key = "posts_more") { ProfileLoadMoreButton(onLoadMorePosts) }
                    }
                }
                1 -> {
                    if (uiState.replies.isEmpty() && !uiState.repliesLoading && uiState.repliesLoaded) {
                        item(key = "replies_empty") {
                            ProfileEmptyTabBox(
                                title = "No activity yet",
                                message = "Posts and replies will appear here",
                                icon = Icons.Outlined.ChatBubbleOutline
                              )
                        }
                    }
                    items(uiState.replies.size, key = { idx -> "reply_${uiState.replies[idx].id}" }) { idx ->
                        val reply = uiState.replies[idx]
                        ProfileReplyCard(reply = reply, onClick = { onPostClick(reply.postId) })
                    }
                    if (uiState.repliesLoading) {
                        item(key = "replies_loading") { ProfileProgressIndicator() }
                    } else if (uiState.repliesHasMore) {
                        item(key = "replies_more") { ProfileLoadMoreButton(onLoadMoreReplies) }
                    }
                }
                2 -> {
                    if (uiState.resources.isEmpty() && !uiState.resourcesLoading && uiState.resourcesLoaded) {
                        item(key = "resources_empty") {
                            ProfileEmptyTabBox(
                                title = "No activity yet",
                                message = "Posts and replies will appear here",
                                icon = Icons.Outlined.FolderOpen
                            )
                        }
                    }
                    items(uiState.resources.size, key = { idx -> "res_${uiState.resources[idx].id}" }) { idx ->
                        val resource = uiState.resources[idx]
                        WebResourceCard(
                            resource = resource,
                            onClick = { onResourceClick(resource.id) },
                            minWidth = null,
                            modifier = Modifier.padding(vertical = 4.dp)
                        )
                    }
                    if (uiState.resourcesLoading) {
                        item(key = "resources_loading") { ProfileProgressIndicator() }
                    } else if (uiState.resourcesHasMore) {
                        item(key = "resources_more") { ProfileLoadMoreButton(onLoadMoreResources) }
                    }
                }
                3 -> {
                    item(key = "about_stats") {
                        AboutStatsCard(profile = profile)
                    }
                    item(key = "about_achievements") {
                        AboutAchievementsCard(profile = profile)
                    }
                    item(key = "about_details") {
                        AboutDetailsCard(profile = profile)
                    }
                    item(key = "about_progress") {
                        AboutProgressCard(profile = profile)
                    }
                }
            }
        }

        item(key = "bottom_spacer") {
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}
