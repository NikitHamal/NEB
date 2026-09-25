package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Apartment
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.Chat
import androidx.compose.material.icons.outlined.ChatBubble
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Leaderboard
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.TrendingUp
import androidx.compose.material.icons.outlined.WorkspacePremium
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.compactCount

// ---------------------------------------------------------------------------
// The About tab: Stats, Achievements, Details, Progress.
//
// Four bordered cards, each headed by a glyph and a bold title. Every card is
// a panel on the lowest surface with a hairline border, so the tab reads as a
// set rather than four unrelated blocks.
// ---------------------------------------------------------------------------

@Composable
fun AboutStatsCard(
    profile: UserProfileResponse,
    followerCount: Int,
    modifier: Modifier = Modifier
) {
    AboutCard(icon = Icons.Outlined.Leaderboard, title = "Stats", modifier = modifier) {
        Row(modifier = Modifier.fillMaxWidth()) {
            Box(modifier = Modifier.weight(1f)) {
                AboutStatItem(value = compactCount(profile.postCount), label = "Discussions")
            }
            Box(modifier = Modifier.weight(1f)) {
                AboutStatItem(value = compactCount(profile.replyCount), label = "Replies")
            }
            Box(modifier = Modifier.weight(1f)) {
                AboutStatItem(value = compactCount(followerCount), label = "Followers")
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        Row(modifier = Modifier.fillMaxWidth()) {
            Box(modifier = Modifier.weight(1f)) {
                AboutStatItem(value = compactCount(profile.likesReceivedCount), label = "Likes Received")
            }
            Box(modifier = Modifier.weight(1f)) {
                AboutStatItem(
                    value = compactCount(profile.contributionScore),
                    label = "NEBian Score",
                    isAcademic = true
                )
            }
            Box(modifier = Modifier.weight(1f)) {
                AboutStatItem(value = compactCount(profile.followingCount), label = "Following")
            }
        }
    }
}

@Composable
private fun AboutStatItem(value: String, label: String, isAcademic: Boolean = false) {
    Column(
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.ExtraBold,
            color = if (isAcademic) {
                MaterialTheme.colorScheme.primary
            } else {
                MaterialTheme.colorScheme.onSurface
            }
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun AboutAchievementsCard(
    profile: UserProfileResponse,
    modifier: Modifier = Modifier
) {
    val achievements = remember(profile.achievementBadges) { parseAchievements(profile.achievementBadges) }
    val postCount = profile.postCount
    val replyCount = profile.replyCount
    val likesReceived = profile.likesReceivedCount

    AboutCard(icon = Icons.Outlined.WorkspacePremium, title = "Achievements", modifier = modifier) {
        val hasEarned = achievements.isNotEmpty() || postCount >= 1 || replyCount >= 1 || likesReceived >= 1
        if (!hasEarned) {
            Text(
                text = "No achievements unlocked yet. Post or reply in the forum to begin!",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            @OptIn(ExperimentalLayoutApi::class)
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                achievements.forEach { ach ->
                    AchievementBadgePill(label = ach.label, icon = Icons.Outlined.WorkspacePremium)
                }
                if (postCount >= 1) {
                    AchievementBadgePill(label = "First Discussion", icon = Icons.Outlined.Chat)
                }
                if (replyCount >= 1) {
                    AchievementBadgePill(label = "First Reply", icon = Icons.Outlined.ChatBubble)
                }
                if (likesReceived >= 1) {
                    AchievementBadgePill(label = "First Thumb Received", icon = Icons.Outlined.ThumbUp)
                }
            }
        }
    }
}

@Composable
private fun AchievementBadgePill(label: String, icon: ImageVector) {
    val accent = MaterialTheme.colorScheme.onSurface
    Surface(
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.surfaceContainerHigh,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = accent,
                modifier = Modifier.size(16.dp)
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                color = accent
            )
        }
    }
}

@Composable
fun AboutDetailsCard(
    profile: UserProfileResponse,
    onProfileClick: (String) -> Unit = {},
    modifier: Modifier = Modifier
) {
    val location = remember(profile.district, profile.pradesh) { profileLocation(profile) }
    val joinedText = remember(profile.createdAt) { formatJoined(profile.createdAt) }

    AboutCard(icon = Icons.Outlined.Info, title = "Details", modifier = modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            if (!profile.classLevel.isNullOrBlank()) {
                AboutDetailRow(
                    icon = Icons.Outlined.School,
                    label = "Class",
                    value = classLabel(profile.classLevel)
                )
            }
            if (!profile.subjects.isNullOrBlank()) {
                AboutDetailRow(
                    icon = Icons.Outlined.MenuBook,
                    label = "Subjects",
                    value = subjectList(profile.subjects)
                )
            }
            if (!profile.school.isNullOrBlank()) {
                val schoolUsername = profile.schoolUsername
                AboutDetailRow(
                    icon = Icons.Outlined.Apartment,
                    label = "School",
                    value = profile.school,
                    onClick = if (!schoolUsername.isNullOrBlank()) {
                        { onProfileClick(schoolUsername) }
                    } else null
                )
            }
            if (location.isNotBlank()) {
                AboutDetailRow(icon = Icons.Outlined.LocationOn, label = "Location", value = location)
            }
            if (joinedText.isNotBlank()) {
                AboutDetailRow(icon = Icons.Outlined.CalendarMonth, label = "Joined", value = joinedText)
            }
            if (!profile.gender.isNullOrBlank()) {
                AboutDetailRow(icon = Icons.Outlined.Person, label = "Gender", value = profile.gender)
            }
        }
    }
}

@Composable
private fun AboutDetailRow(
    icon: ImageVector,
    label: String,
    value: String,
    onClick: (() -> Unit)? = null
) {
    val isClickable = onClick != null
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .then(if (isClickable) Modifier.clickable { onClick?.invoke() } else Modifier),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = if (isClickable) {
                MaterialTheme.colorScheme.primary
            } else {
                MaterialTheme.colorScheme.onSurfaceVariant
            },
            modifier = Modifier.size(20.dp)
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.width(80.dp)
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            color = if (isClickable) {
                MaterialTheme.colorScheme.primary
            } else {
                MaterialTheme.colorScheme.onSurface
            },
            modifier = Modifier.weight(1f)
        )
    }
}

@Composable
fun AboutProgressCard(
    profile: UserProfileResponse,
    modifier: Modifier = Modifier
) {
    val subjects = remember(profile.subjects) {
        if (profile.subjects.isNullOrBlank()) {
            emptyList()
        } else {
            profile.subjects.split(",").map { it.trim() }.filter { it.isNotBlank() }
        }
    }
    if (subjects.isEmpty() || profile.isBot) return

    AboutCard(icon = Icons.Outlined.TrendingUp, title = "Progress", modifier = modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            subjects.forEach { subject ->
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(
                        text = subject,
                        style = MaterialTheme.typography.bodyMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    LinearProgressIndicator(
                        progress = { 0f },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(6.dp)
                            .clip(CircleShape),
                        color = MaterialTheme.colorScheme.primary,
                        trackColor = MaterialTheme.colorScheme.surfaceContainerHigh
                    )
                }
            }
        }
    }
}

/** The shell every About card shares: panel, hairline, glyph, bold title. */
@Composable
private fun AboutCard(
    icon: ImageVector,
    title: String,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
        ),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            content()
        }
    }
}
