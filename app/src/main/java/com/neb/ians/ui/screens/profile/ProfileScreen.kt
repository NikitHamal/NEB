package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
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
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.compactCount

@OptIn(ExperimentalMaterial3Api::class)
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
    onProfileClick: (String) -> Unit = {},
    viewModel: ProfileViewModel = hiltViewModel()
) {
    LaunchedEffect(username) {
        viewModel.loadProfile(username)
    }

    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = "@${uiState.profile?.username ?: username}",
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (uiState.profile?.isSelf == true) {
                        IconButton(onClick = onEditProfile) {
                            Icon(Icons.Filled.Edit, contentDescription = "Edit")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
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
                    isSelf = uiState.profile?.isSelf == true,
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
    isSelf: Boolean,
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
                    val resolvedBannerUrl = remember(profile.bannerUrl) {
                        if (profile.bannerUrl.isNullOrBlank()) null
                        else if (profile.bannerUrl.startsWith("http://") || profile.bannerUrl.startsWith("https://")) profile.bannerUrl
                        else "https://nebians.consica.com.np${if (profile.bannerUrl.startsWith("/")) "" else "/"}${profile.bannerUrl}"
                    }
                    if (!resolvedBannerUrl.isNullOrBlank()) {
                        AsyncImage(
                            model = resolvedBannerUrl,
                            contentDescription = null,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                }
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Avatar(
                            name = profile.displayName ?: profile.username,
                            imageUrl = profile.photoUrl,
                            size = 64.dp,
                            modifier = Modifier.clip(CircleShape)
                        )
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username,
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.ExtraBold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = "@${profile.username}",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }

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

                    Spacer(modifier = Modifier.height(10.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        profile.classLevel?.takeIf { it.isNotBlank() }?.let { WebChip(text = it) }
                        profile.school?.takeIf { it.isNotBlank() }?.let { WebChip(text = it) }
                        profile.role?.takeIf { it.isNotBlank() && it != "student" }?.let {
                            WebChip(
                                text = it.replaceFirstChar { c -> c.uppercase() },
                                selected = true
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (isSelf) {
                            OutlinedButton(
                                onClick = onEditProfile,
                                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
                            ) {
                                Icon(
                                    Icons.Filled.Edit,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.size(6.dp))
                                Text("Edit Profile")
                            }
                        } else {
                            OutlinedButton(
                                onClick = onFollowClick,
                                border = BorderStroke(
                                    1.dp,
                                    if (isFollowing) MaterialTheme.colorScheme.outline
                                    else MaterialTheme.colorScheme.primary
                                ),
                                colors = if (isFollowing)
                                    androidx.compose.material3.ButtonDefaults.outlinedButtonColors(
                                        containerColor = MaterialTheme.colorScheme.surfaceVariant
                                    )
                                else
                                    androidx.compose.material3.ButtonDefaults.outlinedButtonColors(
                                        containerColor = MaterialTheme.colorScheme.primary,
                                        contentColor = MaterialTheme.colorScheme.onPrimary
                                    )
                            ) {
                                Text(if (isFollowing) "Following" else "Follow", fontWeight = FontWeight.SemiBold)
                            }
                        }
                        OutlinedButton(
                            onClick = onBookmarksClick,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
                        ) {
                            Icon(
                                painter = painterResource(id = R.drawable.ic_bookmark),
                                contentDescription = null,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(modifier = Modifier.size(6.dp))
                            Text("Bookmarks")
                        }
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