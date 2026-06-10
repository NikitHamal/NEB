package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.KeyboardArrowRight
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.PersonAdd
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.outlined.BarChart
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.NebAvatar
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.NebCard
import com.neb.ians.ui.components.NebColors
import com.neb.ians.ui.components.NebFilledButton
import com.neb.ians.ui.components.NebOutlinedButton
import com.neb.ians.ui.components.NebTopBar
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
    onBookmarks: () -> Unit = {},
    onSettings: () -> Unit = {},
    onNebyAi: () -> Unit = {},
    onAnalytics: () -> Unit = {},
    isDark: Boolean = false,
    onToggleTheme: () -> Unit = {},
    viewModel: ProfileViewModel = hiltViewModel()
) {
    LaunchedEffect(username) {
        viewModel.loadProfile(username)
    }

    val uiState by viewModel.uiState.collectAsState()
    val profile = uiState.profile

    Scaffold(
        topBar = {
            NebTopBar(
                showBrand = false,
                title = if (profile != null) "@${profile.username}" else "Profile",
                onBack = onNavigateBack,
                isDark = isDark,
                onToggleTheme = onToggleTheme
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
        when {
            uiState.isLoading -> Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) { CircularProgressIndicator() }

            uiState.error != null || profile == null -> Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = uiState.error ?: "Profile not available",
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            else -> ProfileContent(
                profile = profile,
                isFollowing = uiState.isFollowing,
                followerCount = uiState.followerCount,
                contentPadding = padding,
                onEditProfile = onEditProfile,
                onToggleFollow = viewModel::toggleFollow,
                onBookmarks = onBookmarks,
                onSettings = onSettings,
                onNebyAi = onNebyAi,
                onAnalytics = onAnalytics
            )
        }
    }
}

@Composable
private fun ProfileContent(
    profile: UserProfileResponse,
    isFollowing: Boolean,
    followerCount: Int,
    contentPadding: PaddingValues,
    onEditProfile: () -> Unit,
    onToggleFollow: () -> Unit,
    onBookmarks: () -> Unit = {},
    onSettings: () -> Unit = {},
    onNebyAi: () -> Unit = {},
    onAnalytics: () -> Unit = {}
) {
    val isSelf = profile.isSelf == true
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(top = contentPadding.calculateTopPadding())
            .verticalScroll(rememberScrollState())
            .padding(bottom = 32.dp)
    ) {
        // Banner + overlapping avatar
        Box {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(132.dp)
                    .background(NebColors.brandBrush)
            )
            NebAvatar(
                photoUrl = profile.photoUrl,
                name = profile.displayName ?: profile.username,
                size = 96.dp,
                ring = true,
                modifier = Modifier
                    .align(Alignment.BottomStart)
                    .padding(start = 20.dp)
                    .offset(y = 48.dp)
            )
        }

        Spacer(Modifier.height(56.dp))

        Column(modifier = Modifier.padding(horizontal = 20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(
                    text = profile.displayName ?: profile.username,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f, fill = false)
                )
                deriveBadge(profile)?.let { NebBadge(it) }
            }
            Spacer(Modifier.height(2.dp))
            Text(
                text = "@${profile.username}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            if (!profile.bio.isNullOrBlank()) {
                Spacer(Modifier.height(12.dp))
                Text(
                    text = profile.bio,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }

            Spacer(Modifier.height(16.dp))

            // Action button
            if (isSelf) {
                NebOutlinedButton(
                    text = "Edit Profile",
                    onClick = onEditProfile,
                    leadingIcon = Icons.Filled.Edit,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(12.dp))
                NebCard(modifier = Modifier.fillMaxWidth()) {
                    Column {
                        SelfActionRow(
                            icon = Icons.Filled.AutoAwesome,
                            label = "Neby AI",
                            onClick = onNebyAi
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                        SelfActionRow(
                            icon = Icons.Outlined.BookmarkBorder,
                            label = "Bookmarks",
                            onClick = onBookmarks
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                        SelfActionRow(
                            icon = Icons.Outlined.BarChart,
                            label = "Analytics",
                            onClick = onAnalytics
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                        SelfActionRow(
                            icon = Icons.Outlined.Settings,
                            label = "Settings",
                            onClick = onSettings
                        )
                    }
                }
            } else {
                if (isFollowing) {
                    NebOutlinedButton(
                        text = "Following",
                        onClick = onToggleFollow,
                        modifier = Modifier.fillMaxWidth()
                    )
                } else {
                    NebFilledButton(
                        text = "Follow",
                        onClick = onToggleFollow,
                        leadingIcon = Icons.Filled.PersonAdd,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }

            Spacer(Modifier.height(16.dp))

            // Stats card
            NebCard(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 16.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    StatCell(profile.postCount.toString(), "Posts")
                    StatDivider()
                    StatCell(followerCount.toString(), "Followers")
                    StatDivider()
                    StatCell(profile.followingCount.toString(), "Following")
                    StatDivider()
                    StatCell(profile.contributionScore.toString(), "Score")
                }
            }

            // Info rows
            val joined = remember(profile.createdAt) {
                if (profile.createdAt > 0)
                    SimpleDateFormat("MMMM yyyy", Locale.getDefault()).format(Date(profile.createdAt))
                else null
            }
            val location = listOfNotNull(
                profile.district?.takeIf { it.isNotBlank() },
                profile.pradesh?.takeIf { it.isNotBlank() }
            ).joinToString(", ").takeIf { it.isNotBlank() }

            val hasInfo = !profile.school.isNullOrBlank() || location != null || joined != null
            if (hasInfo) {
                Spacer(Modifier.height(16.dp))
                NebCard(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        if (!profile.school.isNullOrBlank()) {
                            InfoRow(Icons.Outlined.School, profile.school)
                        }
                        if (location != null) {
                            InfoRow(Icons.Outlined.LocationOn, location)
                        }
                        if (joined != null) {
                            InfoRow(Icons.Outlined.CalendarMonth, "Joined $joined")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun RowScope.StatCell(value: String, label: String) {
    Column(
        modifier = Modifier.weight(1f),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
        Text(
            label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 11.sp
        )
    }
}

@Composable
private fun StatDivider() {
    Box(
        modifier = Modifier
            .width(1.dp)
            .height(32.dp)
            .background(MaterialTheme.colorScheme.outlineVariant)
    )
}

@Composable
private fun InfoRow(icon: ImageVector, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Icon(icon, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(18.dp))
        Text(
            text,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
private fun SelfActionRow(icon: ImageVector, label: String, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Icon(icon, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(22.dp))
        Text(
            label,
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.weight(1f)
        )
        Icon(
            Icons.AutoMirrored.Outlined.KeyboardArrowRight,
            null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

/** Mirrors web _user_badge_info priority: bot → admin → moderator → verified. */
private fun deriveBadge(p: UserProfileResponse): ApiBadgeInfo? = when {
    p.isBot -> ApiBadgeInfo(type = "verified", label = "Bot")
    p.isAdmin -> ApiBadgeInfo(type = "admin", label = "Admin")
    p.moderatorLevel > 0 -> ApiBadgeInfo(type = "moderator", label = "Moderator")
    p.verificationLevel > 0 -> ApiBadgeInfo(type = "verified", label = "Verified")
    else -> null
}
