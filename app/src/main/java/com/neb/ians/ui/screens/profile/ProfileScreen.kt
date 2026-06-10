package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.R
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebKpiCard
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPrimaryButton
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.compactCount

@Composable
fun ProfileScreen(
    username: String,
    onNavigateBack: () -> Unit,
    onEditProfile: () -> Unit,
    onPostClick: (String) -> Unit,
    onFollowerClick: (String) -> Unit,
    onAnalyticsClick: () -> Unit = {},
    onBookmarksClick: () -> Unit = {},
    onSearchClick: () -> Unit = {},
    viewModel: ProfileViewModel = hiltViewModel()
) {
    LaunchedEffect(username) {
        viewModel.loadProfile(username)
    }

    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            WebTopBar(
                title = "@${uiState.profile?.username ?: username}",
                subtitle = "Profile",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick
            )
        },
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
                    profile = uiState.profile!!,
                    followerCount = uiState.followerCount,
                    isFollowing = uiState.isFollowing,
                    onEditProfile = onEditProfile,
                    onFollowClick = viewModel::toggleFollow,
                    onAnalyticsClick = onAnalyticsClick,
                    onBookmarksClick = onBookmarksClick
                )
            }
        }
    }
}

@Composable
private fun ProfileContent(
    profile: UserProfileResponse,
    followerCount: Int,
    isFollowing: Boolean,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    onAnalyticsClick: () -> Unit,
    onBookmarksClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Surface(
            modifier = Modifier.fillMaxWidth(),
            shape = WebPanelShape,
            color = MaterialTheme.colorScheme.surfaceContainerLowest,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
        ) {
            Column {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(120.dp)
                        .background(
                            Brush.linearGradient(
                                listOf(
                                    MaterialTheme.colorScheme.primaryContainer,
                                    MaterialTheme.colorScheme.surfaceContainerHigh
                                )
                            )
                        )
                ) {
                    if (!profile.bannerUrl.isNullOrBlank()) {
                        AsyncImage(
                            model = profile.bannerUrl,
                            contentDescription = null,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                }
                Column(modifier = Modifier.padding(16.dp)) {
                    Avatar(
                        name = profile.displayName ?: profile.username,
                        imageUrl = profile.photoUrl,
                        size = 76.dp,
                        modifier = Modifier
                            .clip(CircleShape)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        text = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username,
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.ExtraBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "@${profile.username}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    if (!profile.bio.isNullOrBlank()) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = profile.bio,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 5,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        profile.classLevel?.takeIf { it.isNotBlank() }?.let { WebChip(text = it) }
                        profile.school?.takeIf { it.isNotBlank() }?.let { WebChip(text = it) }
                        if (profile.isPrivate) WebChip(text = "Private", selected = true)
                    }
                    Spacer(modifier = Modifier.height(14.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (profile.isSelf == true) {
                            WebPrimaryButton(
                                text = "Edit Profile",
                                imageVector = Icons.Filled.Edit,
                                onClick = onEditProfile
                            )
                        } else {
                            WebPrimaryButton(
                                text = if (isFollowing) "Following" else "Follow",
                                onClick = onFollowClick
                            )
                        }
                        WebOutlinedButton(
                            text = "Analytics",
                            painter = painterResource(id = R.drawable.ic_science),
                            onClick = onAnalyticsClick
                        )
                        WebOutlinedButton(
                            text = "Bookmarks",
                            painter = painterResource(id = R.drawable.ic_bookmark),
                            onClick = onBookmarksClick
                        )
                    }
                }
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            WebKpiCard(
                label = "Followers",
                value = compactCount(followerCount),
                detail = "${compactCount(profile.followingCount)} following",
                painter = painterResource(id = R.drawable.ic_school),
                modifier = Modifier.weight(1f)
            )
            WebKpiCard(
                label = "Posts",
                value = compactCount(profile.postCount),
                detail = "${compactCount(profile.replyCount)} replies",
                painter = painterResource(id = R.drawable.ic_forum_outlined),
                modifier = Modifier.weight(1f)
            )
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            WebKpiCard(
                label = "Likes",
                value = compactCount(profile.likesReceivedCount),
                detail = "${compactCount(profile.likesGivenCount)} given",
                painter = painterResource(id = R.drawable.ic_bookmark),
                modifier = Modifier.weight(1f)
            )
            WebKpiCard(
                label = "Score",
                value = compactCount(profile.contributionScore),
                detail = "Contribution score",
                painter = painterResource(id = R.drawable.ic_science),
                modifier = Modifier.weight(1f)
            )
        }
        Spacer(modifier = Modifier.height(32.dp))
    }
}
