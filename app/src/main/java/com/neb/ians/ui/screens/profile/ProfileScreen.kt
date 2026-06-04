package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.compose.ui.platform.LocalContext
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.data.api.UserStatsResponse
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.UserAvatar
import com.neb.ians.ui.theme.BadgeThemes
import com.neb.ians.ui.theme.getBadgeKey
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    username: String,
    onNavigateBack: () -> Unit,
    onEditProfile: () -> Unit,
    onPostClick: (String) -> Unit,
    onFollowerClick: (String) -> Unit,
    viewModel: ProfileViewModel = hiltViewModel()
) {
    LaunchedEffect(username) { viewModel.loadProfile(username) }

    val uiState by viewModel.uiState.collectAsState()
    val profile = uiState.profile

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("@${profile?.username ?: username}", maxLines = 1) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        when {
            uiState.isLoading -> {
                Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }
            uiState.error != null && profile == null -> {
                Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                    ErrorCard(message = uiState.error ?: "Something went wrong", onRetry = { viewModel.loadProfile(username) })
                }
            }
            profile != null -> {
                ProfileContent(
                    modifier = Modifier.padding(padding),
                    profile = profile,
                    stats = uiState.stats,
                    isSelf = uiState.isSelf,
                    isFollowing = uiState.isFollowing,
                    followerCount = uiState.followerCount,
                    followLoading = uiState.followLoading,
                    onEditProfile = onEditProfile,
                    onToggleFollow = viewModel::toggleFollow,
                    onFollowersClick = { onFollowerClick(profile.username) }
                )
            }
        }
    }
}

@Composable
private fun ProfileContent(
    modifier: Modifier,
    profile: UserProfileResponse,
    stats: UserStatsResponse?,
    isSelf: Boolean,
    isFollowing: Boolean,
    followerCount: Int,
    followLoading: Boolean,
    onEditProfile: () -> Unit,
    onToggleFollow: () -> Unit,
    onFollowersClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val displayName = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username
    val postCount = stats?.postCount ?: profile.postCount
    val followingCount = stats?.followingCount ?: profile.followingCount

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        // Banner
        Box(modifier = Modifier.fillMaxWidth().height(140.dp)) {
            if (!profile.bannerUrl.isNullOrBlank()) {
                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current).data(profile.bannerUrl).crossfade(true).build(),
                    contentDescription = "Banner",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
            } else {
                Box(Modifier.fillMaxSize().background(scheme.primaryContainer))
            }
        }

        // Avatar overlapping the banner
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 20.dp)) {
            Box(modifier = Modifier.offset(y = (-44).dp)) {
                Surface(
                    shape = androidx.compose.foundation.shape.CircleShape,
                    color = scheme.surface,
                    tonalElevation = 2.dp,
                    modifier = Modifier.padding(2.dp)
                ) {
                    UserAvatar(
                        photoUrl = profile.photoUrl,
                        name = displayName,
                        size = 88.dp,
                        modifier = Modifier.padding(4.dp)
                    )
                }
            }
        }

        Column(modifier = Modifier.padding(horizontal = 20.dp).offset(y = (-32).dp)) {
            // Name + badge
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = displayName,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.width(8.dp))
                RoleBadge(profile)
            }
            Text(
                text = "@${profile.username}",
                style = MaterialTheme.typography.bodyMedium,
                color = scheme.onSurfaceVariant
            )

            Spacer(Modifier.height(6.dp))
            Text(
                text = buildHeadline(profile),
                style = MaterialTheme.typography.bodyMedium,
                color = scheme.onSurfaceVariant
            )

            Spacer(Modifier.height(16.dp))
            // Stats row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                StatPill("Followers", followerCount, Modifier.weight(1f).clickable { onFollowersClick() })
                StatPill("Following", followingCount, Modifier.weight(1f))
                StatPill("Posts", postCount, Modifier.weight(1f))
            }

            Spacer(Modifier.height(16.dp))
            // Action buttons
            if (isSelf) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    Button(onClick = onEditProfile, modifier = Modifier.weight(1f)) {
                        Icon(Icons.Filled.Edit, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Edit Profile")
                    }
                    OutlinedButton(onClick = { }, modifier = Modifier.weight(1f)) {
                        Icon(Icons.Filled.Share, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Share")
                    }
                }
            } else {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    if (isFollowing) {
                        OutlinedButton(
                            onClick = onToggleFollow,
                            enabled = !followLoading,
                            modifier = Modifier.weight(1f)
                        ) {
                            if (followLoading) {
                                CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                            } else {
                                Icon(Icons.Filled.CheckCircle, contentDescription = null, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(6.dp))
                                Text("Following")
                            }
                        }
                    } else {
                        Button(
                            onClick = onToggleFollow,
                            enabled = !followLoading,
                            modifier = Modifier.weight(1f)
                        ) {
                            if (followLoading) {
                                CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp, color = scheme.onPrimary)
                            } else {
                                Icon(Icons.Filled.Person, contentDescription = null, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(6.dp))
                                Text("Follow")
                            }
                        }
                    }
                    OutlinedButton(onClick = { }, modifier = Modifier.weight(1f)) {
                        Icon(Icons.Filled.Share, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Share")
                    }
                }
            }

            // Bio
            if (!profile.bio.isNullOrBlank()) {
                Spacer(Modifier.height(20.dp))
                Text("About", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(6.dp))
                Text(profile.bio, style = MaterialTheme.typography.bodyMedium)
            }

            // Meta details
            val locationParts = listOfNotNull(
                profile.district?.takeIf { it.isNotBlank() },
                profile.pradesh?.takeIf { it.isNotBlank() }
            )
            val hasMeta = locationParts.isNotEmpty() || !profile.school.isNullOrBlank() || profile.createdAt > 0
            if (hasMeta) {
                Spacer(Modifier.height(20.dp))
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (locationParts.isNotEmpty()) {
                        MetaRow(Icons.Filled.LocationOn, locationParts.joinToString(", "))
                    }
                    if (!profile.school.isNullOrBlank()) {
                        MetaRow(Icons.Filled.Person, profile.school)
                    }
                    if (profile.createdAt > 0) {
                        MetaRow(Icons.Filled.Star, "Joined ${formatJoinedDate(profile.createdAt)}")
                    }
                }
            }

            // Stats grid
            Spacer(Modifier.height(24.dp))
            Text("Activity", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Spacer(Modifier.height(12.dp))
            StatsGrid(profile = profile, stats = stats, followerCount = followerCount)

            Spacer(Modifier.height(32.dp))
        }
    }
}

@Composable
private fun RoleBadge(profile: UserProfileResponse) {
    val key = getBadgeKey(profile) ?: return
    val theme = BadgeThemes[key] ?: return
    val icon: ImageVector = when (theme.icon) {
        "crown" -> Icons.Filled.Star
        else -> Icons.Filled.CheckCircle
    }
    Surface(
        shape = RoundedCornerShape(50),
        color = theme.background
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = theme.text, modifier = Modifier.size(14.dp))
            Spacer(Modifier.width(4.dp))
            Text(
                text = key.substringBefore('-').replaceFirstChar { it.uppercase() },
                color = theme.text,
                fontSize = 11.sp,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
private fun StatPill(label: String, value: Int, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainer
    ) {
        Column(
            modifier = Modifier.padding(vertical = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("$value", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text(label, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun MetaRow(icon: ImageVector, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, contentDescription = null, modifier = Modifier.size(18.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
        Spacer(Modifier.width(8.dp))
        Text(text, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun StatsGrid(profile: UserProfileResponse, stats: UserStatsResponse?, followerCount: Int) {
    val items = listOf(
        "Discussions" to (stats?.postCount ?: profile.postCount),
        "Replies" to (stats?.replyCount ?: profile.replyCount),
        "Followers" to followerCount,
        "Likes Received" to (stats?.likesReceived ?: profile.likesReceivedCount),
        "NEBian Score" to (stats?.contributionScore ?: profile.contributionScore),
        "Following" to (stats?.followingCount ?: profile.followingCount)
    )
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        items.chunked(3).forEach { row ->
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                row.forEach { (label, value) ->
                    val highlighted = label == "NEBian Score"
                    Surface(
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(14.dp),
                        color = if (highlighted) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceContainer
                    ) {
                        Column(
                            modifier = Modifier.padding(vertical = 14.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                "$value",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = if (highlighted) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface
                            )
                            Text(
                                label,
                                style = MaterialTheme.typography.labelSmall,
                                textAlign = TextAlign.Center,
                                color = if (highlighted) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

private fun buildHeadline(profile: UserProfileResponse): String {
    if (profile.isBot) return "AI Study Companion"
    val base = when (profile.classLevel) {
        "11" -> "Class 11"
        "12" -> "Class 12"
        "Both" -> "Class 11 & 12"
        "Passout" -> "Graduate"
        "Teacher" -> "Teacher / Educator"
        "Bachelors" -> "Bachelors"
        null, "" -> "NEBians Member"
        else -> profile.classLevel
    }
    val subjects = profile.subjects?.takeIf { it.isNotBlank() }?.split(",")?.joinToString(", ") { it.trim() }
    return if (subjects != null) "$base · $subjects" else base
}

private fun formatJoinedDate(createdAtMs: Long): String {
    return try {
        SimpleDateFormat("MMM yyyy", Locale.getDefault()).format(Date(createdAtMs))
    } catch (_: Exception) {
        ""
    }
}
