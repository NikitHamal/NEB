package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.ProfileBanner
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebKpiCard
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.bannerPresetFor
import com.neb.ians.ui.components.compactCount
import com.neb.ians.util.formatTimeAgo
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

// ---------------------------------------------------------------------------
// Client-side helpers mirroring web `_user_badge_info` / achievements / levels
// ---------------------------------------------------------------------------

/** Builds the role badge with web's priority: bot → admin → mod → teacher → institution → explorer → verified. */
private fun buildBadgeInfo(p: UserProfileResponse): ApiBadgeInfo? = when {
    p.isBot -> ApiBadgeInfo(type = "bot", label = "AI", color = "#7C4DFF")
    p.isAdmin -> ApiBadgeInfo(type = "admin", label = "Admin", color = "#F59E0B")
    p.moderatorLevel > 0 -> when (p.moderatorLevel) {
        1 -> ApiBadgeInfo(type = "moderator", label = "Community Mod", color = "#1B9AF0")
        2 -> ApiBadgeInfo(type = "moderator", label = "Senior Mod", color = "#00897B")
        else -> ApiBadgeInfo(type = "moderator", label = "Community Lead", color = "#7B1FA2")
    }
    p.role == "teacher" -> ApiBadgeInfo(
        type = "teacher",
        label = if (p.verificationLevel > 0) "Verified Teacher" else "Teacher",
        color = "#10B981"
    )
    p.role == "institution" -> ApiBadgeInfo(type = "institution", label = "Institution", color = "#6366F1")
    p.role == "explorer" -> ApiBadgeInfo(type = "explorer", label = "Explorer", color = "#F59E0B")
    p.verificationLevel > 0 -> when (p.verificationLevel) {
        1 -> ApiBadgeInfo(type = "verified", label = "Verified", color = "#1B9AF0")
        2 -> ApiBadgeInfo(type = "verified", label = "Expert Verified", color = "#2E7D32")
        3 -> ApiBadgeInfo(type = "verified", label = "Premium Verified", color = "#F59E0B")
        else -> ApiBadgeInfo(type = "verified", label = "Elite Verified", color = "#1a1a1a")
    }
    else -> null
}

private data class AchievementPill(val key: String, val label: String, val color: Color)

private fun parseAchievements(raw: String?): List<AchievementPill> {
    if (raw.isNullOrBlank()) return emptyList()
    return raw.split(",")
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .mapNotNull { key ->
            when (key) {
                "top_contributor" -> AchievementPill(key, "Top Contributor", Color(0xFFF59E0B))
                "helpful" -> AchievementPill(key, "Helpful", Color(0xFFEC407A))
                "scholar" -> AchievementPill(key, "Scholar", Color(0xFF1B9AF0))
                "streak" -> AchievementPill(key, "Streak", Color(0xFFFF6D00))
                "first_post" -> AchievementPill(key, "First Post", Color(0xFF2E7D32))
                "100_likes" -> AchievementPill(key, "100 Likes", Color(0xFFE53935))
                "bookworm" -> AchievementPill(key, "Bookworm", Color(0xFF00897B))
                "problem_solver" -> AchievementPill(key, "Problem Solver", Color(0xFFF9A825))
                else -> null
            }
        }
}

private fun contributionLevelTitle(score: Int): String = when {
    score >= 2000 -> "Level 5 Scholar"
    score >= 1000 -> "Level 4 Tutor"
    score >= 500 -> "Level 3 Helper"
    score >= 100 -> "Level 2 Guide"
    else -> "Level 1 Novice"
}

/** Crude markdown → plain text for compact post previews. */
private fun plainTextPreview(content: String): String {
    return content
        .replace(Regex("!\\[[^\\]]*\\]\\([^)]*\\)"), "")       // images
        .replace(Regex("\\[([^\\]]*)\\]\\([^)]*\\)"), "$1")    // links → label
        .replace(Regex("[*_`#>~]"), "")                           // md tokens
        .replace(Regex("\\s+"), " ")
        .trim()
}

private fun formatJoined(createdAtMs: Long): String {
    if (createdAtMs <= 0) return ""
    return try {
        "Joined " + SimpleDateFormat("MMM yyyy", Locale.US).format(Date(createdAtMs))
    } catch (_: Exception) {
        ""
    }
}

// ---------------------------------------------------------------------------
// Screen
// ---------------------------------------------------------------------------

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
                    uiState = uiState,
                    onEditProfile = onEditProfile,
                    onFollowClick = viewModel::toggleFollow,
                    onBookmarksClick = onBookmarksClick,
                    onPostClick = onPostClick,
                    onTabSelected = viewModel::selectTab,
                    onLoadMorePosts = { viewModel.loadPosts(reset = false) },
                    onAvatarClick = viewModel::openPhotoGallery
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
    onBookmarksClick: () -> Unit,
    onPostClick: (String) -> Unit,
    onTabSelected: (Int) -> Unit,
    onLoadMorePosts: () -> Unit,
    onAvatarClick: () -> Unit
) {
    val profile = uiState.profile ?: return
    val isSelf = profile.isSelf == true
    val isPrivate = profile.isLocked == 1 && !isSelf

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item(key = "header") {
            ProfileHeaderCard(
                profile = profile,
                isSelf = isSelf,
                isFollowing = uiState.isFollowing,
                onEditProfile = onEditProfile,
                onFollowClick = onFollowClick,
                onBookmarksClick = onBookmarksClick,
                onAvatarClick = onAvatarClick
            )
        }

        if (isPrivate) {
            item(key = "private") {
                PrivateProfileNotice()
            }
        } else {
            item(key = "stats1") {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                    WebKpiCard(
                        label = "Followers",
                        value = compactCount(uiState.followerCount),
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
            }
            item(key = "stats2") {
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
            }
            item(key = "level") {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = WebPillShape,
                    color = MaterialTheme.colorScheme.secondaryContainer
                ) {
                    Text(
                        text = contributionLevelTitle(profile.contributionScore),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 14.dp, vertical = 8.dp),
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSecondaryContainer,
                        textAlign = TextAlign.Center,
                        maxLines = 1
                    )
                }
            }

            item(key = "tabs") {
                TabRow(
                    selectedTabIndex = uiState.selectedTab,
                    containerColor = MaterialTheme.colorScheme.surface
                ) {
                    Tab(
                        selected = uiState.selectedTab == 0,
                        onClick = { onTabSelected(0) },
                        text = { Text("Posts", fontWeight = FontWeight.SemiBold) }
                    )
                    Tab(
                        selected = uiState.selectedTab == 1,
                        onClick = { onTabSelected(1) },
                        text = { Text("About", fontWeight = FontWeight.SemiBold) }
                    )
                }
            }

            if (uiState.selectedTab == 0) {
                if (uiState.posts.isEmpty() && !uiState.postsLoading && uiState.postsLoaded) {
                    item(key = "posts_empty") {
                        WebEmptyState(
                            title = "No posts yet",
                            message = "Posts from @${profile.username} will appear here.",
                            icon = painterResource(id = R.drawable.ic_forum_outlined)
                        )
                    }
                }
                items(uiState.posts.size, key = { idx -> "post_${uiState.posts[idx].id}" }) { idx ->
                    val post = uiState.posts[idx]
                    ProfilePostCard(post = post, onClick = { onPostClick(post.id) })
                }
                if (uiState.postsLoading) {
                    item(key = "posts_loading") {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            CircularProgressIndicator(modifier = Modifier.size(26.dp), strokeWidth = 3.dp)
                        }
                    }
                } else if (uiState.postsHasMore) {
                    item(key = "posts_more") {
                        OutlinedButton(
                            onClick = onLoadMorePosts,
                            modifier = Modifier.fillMaxWidth(),
                            shape = WebPillShape,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                        ) {
                            Text("Load more", fontWeight = FontWeight.SemiBold)
                        }
                    }
                }
            } else {
                item(key = "about") {
                    AboutCard(profile = profile)
                }
            }
        }

        item(key = "bottom_spacer") {
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

// ---------------------------------------------------------------------------
// Header card — banner + overlapping avatar + identity + actions
// ---------------------------------------------------------------------------

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun ProfileHeaderCard(
    profile: UserProfileResponse,
    isSelf: Boolean,
    isFollowing: Boolean,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    onBookmarksClick: () -> Unit,
    onAvatarClick: () -> Unit
) {
    val badge = remember(profile) { buildBadgeInfo(profile) }
    val achievements = remember(profile.achievementBadges) { parseAchievements(profile.achievementBadges) }
    val preset = remember(profile) { bannerPresetFor(profile) }

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
                    .zIndex(1f)
            ) {
                ProfileBanner(
                    bannerUrl = profile.bannerUrl,
                    bannerType = preset.first,
                    decoText = preset.second,
                    modifier = Modifier.fillMaxWidth()
                )
                // Avatar overlapping the bottom of the banner (web .pf-card-avatar)
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 16.dp)
                        .offset(y = 46.dp)
                        .background(MaterialTheme.colorScheme.surface, CircleShape)
                        .padding(4.dp)
                ) {
                    Avatar(
                        name = profile.displayName ?: profile.username,
                        imageUrl = profile.photoUrl,
                        size = 84.dp,
                        modifier = Modifier
                            .clip(CircleShape)
                            .then(
                                if (isSelf) Modifier.clickable(onClick = onAvatarClick)
                                else Modifier
                            )
                    )
                }
            }

            Column(modifier = Modifier.padding(16.dp)) {
                Spacer(modifier = Modifier.height(42.dp))

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username,
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.ExtraBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false)
                    )
                    if (badge != null) {
                        Spacer(modifier = Modifier.width(8.dp))
                        NebBadge(badge)
                    }
                }
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

                Spacer(modifier = Modifier.height(10.dp))
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    profile.classLevel?.takeIf { it.isNotBlank() }?.let { WebChip(text = it) }
                    profile.school?.takeIf { it.isNotBlank() }?.let { WebChip(text = it) }
                    profile.role?.takeIf { it.isNotBlank() && it != "student" }?.let {
                        WebChip(
                            text = it.replaceFirstChar { c -> c.uppercase() },
                            selected = true
                        )
                    }
                }

                if (achievements.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(10.dp))
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        achievements.forEach { pill ->
                            Surface(
                                shape = WebPillShape,
                                color = pill.color.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = pill.label,
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = pill.color,
                                    maxLines = 1
                                )
                            }
                        }
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
                                ButtonDefaults.outlinedButtonColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                                )
                            else
                                ButtonDefaults.outlinedButtonColors(
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
}

// ---------------------------------------------------------------------------
// Private profile notice
// ---------------------------------------------------------------------------

@Composable
private fun PrivateProfileNotice() {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(28.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Surface(
                modifier = Modifier.size(54.dp),
                shape = CircleShape,
                color = MaterialTheme.colorScheme.surfaceContainerHigh
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Outlined.Lock,
                        contentDescription = null,
                        modifier = Modifier.size(26.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = "This profile is private",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Only the owner can see this profile's details, stats and posts.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
        }
    }
}

// ---------------------------------------------------------------------------
// Posts tab — compact post card
// ---------------------------------------------------------------------------

@Composable
private fun ProfilePostCard(post: ApiPost, onClick: () -> Unit) {
    val preview = remember(post.content) { plainTextPreview(post.content) }
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebPanelShape)
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Text(
                text = post.title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (preview.isNotBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = preview,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "${post.category.ifBlank { "General" }} \u00B7 ${formatTimeAgo(post.createdAt)} \u00B7 " +
                    "${compactCount(post.thumbsUpCount)} likes \u00B7 ${compactCount(post.replyCount)} replies",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

// ---------------------------------------------------------------------------
// About tab
// ---------------------------------------------------------------------------

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun AboutCard(profile: UserProfileResponse) {
    val subjects = remember(profile.subjects) {
        profile.subjects?.split(",")?.map { it.trim() }?.filter { it.isNotBlank() } ?: emptyList()
    }
    val location = remember(profile.district, profile.pradesh) {
        listOfNotNull(
            profile.district?.takeIf { it.isNotBlank() },
            profile.pradesh?.takeIf { it.isNotBlank() }
        ).joinToString(", ")
    }
    val joined = remember(profile.createdAt) { formatJoined(profile.createdAt) }

    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            profile.school?.takeIf { it.isNotBlank() }?.let { AboutRow(label = "School", value = it) }
            if (location.isNotBlank()) AboutRow(label = "Location", value = location)
            profile.gender?.takeIf { it.isNotBlank() }?.let { AboutRow(label = "Gender", value = it) }
            if (joined.isNotBlank()) AboutRow(label = "Member since", value = joined)

            if (subjects.isNotEmpty()) {
                Column {
                    Text(
                        text = "Subjects",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        subjects.forEach { WebChip(text = it) }
                    }
                }
            }

            if (profile.school.isNullOrBlank() && location.isBlank() &&
                profile.gender.isNullOrBlank() && joined.isBlank() && subjects.isEmpty()
            ) {
                Text(
                    text = "Nothing here yet.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun AboutRow(label: String, value: String) {
    Row(verticalAlignment = Alignment.Top) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.width(110.dp)
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium,
            color = MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.weight(1f)
        )
    }
}
