package com.neb.ians.ui.screens.profile

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.CalendarToday
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.GroupAdd
import androidx.compose.material.icons.outlined.HourglassTop
import androidx.compose.material.icons.outlined.Place
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.R
import com.neb.ians.data.api.ApiSocialLink
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.LinkifyText
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.ProfileBanner
import com.neb.ians.ui.components.ShimmerCircle
import com.neb.ians.ui.components.ShimmerLine
import com.neb.ians.ui.components.bannerPresetFor
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.util.TactileType

// ---------------------------------------------------------------------------
// The head of the profile.
//
// One column, no card, no border: the banner runs to both edges, the avatar
// sits across its bottom edge with the primary action opposite it, and
// everything below is left-aligned text at a single indent. The old version
// wrapped all of this in a 24dp rounded panel inside a 16dp-padded list,
// which read as a card floating on a card.
// ---------------------------------------------------------------------------

private val HeaderIndent = 20.dp

@Composable
fun ProfileHeader(
    profile: UserProfileResponse,
    isSelf: Boolean,
    isFollowing: Boolean,
    isRequested: Boolean,
    followRequestsCount: Int,
    followerCount: Int,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    onAvatarClick: () -> Unit,
    onFollowersClick: () -> Unit,
    onFollowingClick: () -> Unit,
    onFollowRequestsClick: () -> Unit,
    onProfileClick: (String) -> Unit,
    onSocialLinkClick: (ApiSocialLink) -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val badge = remember(profile) { buildBadgeInfo(profile) }
    val preset = remember(profile) { bannerPresetFor(profile) }
    val bio = remember(profile) { fallbackBio(profile) }
    val location = remember(profile.district, profile.pradesh) { profileLocation(profile) }
    val joined = remember(profile.createdAt, profile.isBot) { joinedLine(profile) }
    val achievements = remember(profile.achievementBadges) { parseAchievements(profile.achievementBadges) }

    Column(modifier = modifier.fillMaxWidth()) {

        // Banner, with the avatar and the primary action straddling its
        // bottom edge. Nothing clips here, so the avatar can hang below.
        Box(modifier = Modifier.fillMaxWidth()) {
            ProfileBanner(
                bannerUrl = profile.bannerUrl,
                bannerType = preset.first,
                decoText = preset.second,
                modifier = Modifier.fillMaxWidth()
            )
            Row(
                modifier = Modifier
                    .align(Alignment.BottomStart)
                    .fillMaxWidth()
                    .padding(horizontal = HeaderIndent)
                    .offset(y = 40.dp),
                verticalAlignment = Alignment.Bottom
            ) {
                Box(
                    modifier = Modifier
                        .background(scheme.surface, CircleShape)
                        .padding(4.dp)
                ) {
                    if (profile.isBot) {
                        com.neb.ians.ui.avatar.neby.NebyAvatar(
                            animation = "idle",
                            size = 84.dp,
                            interactive = true,
                            modifier = Modifier.clip(CircleShape)
                        )
                    } else {
                        Avatar(
                            name = profile.displayName ?: profile.username,
                            imageUrl = profile.photoUrl,
                            size = 84.dp,
                            modifier = Modifier
                                .clip(CircleShape)
                                .nebPressable(scale = 0.94f, onClick = onAvatarClick)
                        )
                    }
                }

                Spacer(modifier = Modifier.weight(1f))

                // The action clears the banner rather than sitting flush
                // against its bottom edge: the row is bottom-aligned 40dp
                // below the art, and a 40dp-tall button would put its top
                // exactly on the seam. Sixteen more drops it clear.
                PrimaryAction(
                    profile = profile,
                    isSelf = isSelf,
                    isFollowing = isFollowing,
                    isRequested = isRequested,
                    onEditProfile = onEditProfile,
                    onFollowClick = onFollowClick,
                    modifier = Modifier.offset(y = 16.dp)
                )
            }
        }

        // The overhang the avatar and the action borrowed from the column
        // below them.
        Spacer(modifier = Modifier.height(64.dp))

        Column(modifier = Modifier.padding(horizontal = HeaderIndent)) {

            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    color = scheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f, fill = false)
                )
                if (profile.verificationLevel > 0 && badge?.type != "verified") {
                    Spacer(modifier = Modifier.width(6.dp))
                    Icon(
                        imageVector = Icons.Filled.Verified,
                        contentDescription = "Verified",
                        tint = scheme.onSurfaceVariant,
                        modifier = Modifier.size(17.dp)
                    )
                }
                if (badge != null) {
                    Spacer(modifier = Modifier.width(8.dp))
                    NebBadge(badge)
                }
            }

            Spacer(modifier = Modifier.height(3.dp))
            Text(
                text = "@${profile.username}",
                style = MaterialTheme.typography.bodyMedium,
                color = scheme.onSurfaceVariant
            )
            Text(
                text = formatRoleHeadline(profile),
                style = MaterialTheme.typography.bodySmall,
                color = scheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )

            if (bio.isNotBlank()) {
                Spacer(modifier = Modifier.height(12.dp))
                LinkifyText(
                    text = bio,
                    style = MaterialTheme.typography.bodyMedium,
                    color = scheme.onSurface
                )
            }

            // Where they are, where they study, when they arrived — one wrapped
            // line of grey, rather than three icon rows stacked vertically.
            val hasMeta = location.isNotBlank() || !profile.school.isNullOrBlank() || joined.isNotBlank()
            if (hasMeta) {
                Spacer(modifier = Modifier.height(10.dp))
                @OptIn(ExperimentalLayoutApi::class)
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(14.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (location.isNotBlank()) {
                        MetaItem(icon = Icons.Outlined.Place, text = location)
                    }
                    if (!profile.school.isNullOrBlank()) {
                        val schoolUsername = profile.schoolUsername
                        MetaItem(
                            painter = R.drawable.ic_school,
                            text = profile.school,
                            onClick = if (!schoolUsername.isNullOrBlank()) {
                                { onProfileClick(schoolUsername) }
                            } else null
                        )
                    }
                    if (joined.isNotBlank()) {
                        MetaItem(icon = Icons.Outlined.CalendarToday, text = joined)
                    }
                }
            }

            Spacer(modifier = Modifier.height(14.dp))
            ProfileStatsRow(
                profile = profile,
                followerCount = followerCount,
                onFollowersClick = onFollowersClick,
                onFollowingClick = onFollowingClick
            )

            if (profile.socialLinks.isNotEmpty()) {
                Spacer(modifier = Modifier.height(14.dp))
                SocialLinkRow(links = profile.socialLinks, onSocialLinkClick = onSocialLinkClick)
            }

            if (achievements.isNotEmpty()) {
                Spacer(modifier = Modifier.height(14.dp))
                @OptIn(ExperimentalLayoutApi::class)
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    achievements.forEach { pill -> AchievementPillChip(pill.label) }
                }
            }

            if (isSelf && profile.isLocked == 1) {
                Spacer(modifier = Modifier.height(14.dp))
                NebButton(
                    text = if (followRequestsCount > 0) {
                        "Follow requests ($followRequestsCount)"
                    } else {
                        "Follow requests"
                    },
                    onClick = onFollowRequestsClick,
                    icon = Icons.Outlined.GroupAdd,
                    tone = NebButtonTone.Outlined,
                    size = NebButtonSize.Small,
                    fillWidth = true
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))
    }
}

@Composable
private fun PrimaryAction(
    profile: UserProfileResponse,
    isSelf: Boolean,
    isFollowing: Boolean,
    isRequested: Boolean,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current

    if (isSelf) {
        NebButton(
            text = "Edit profile",
            onClick = onEditProfile,
            icon = Icons.Outlined.Edit,
            tone = NebButtonTone.Outlined,
            size = NebButtonSize.Small,
            modifier = modifier
        )
    } else {
        Row(modifier = modifier, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            NebButton(
                text = if (profile.isBot) "Ask" else "Mention",
                onClick = {
                    clipboard.setText(AnnotatedString("@${profile.username}"))
                    Toast.makeText(context, "Mention handle copied", Toast.LENGTH_SHORT).show()
                },
                icon = Icons.Outlined.AlternateEmail,
                tone = NebButtonTone.Outlined,
                size = NebButtonSize.Small
            )
            NebButton(
                text = when {
                    isFollowing -> "Following"
                    isRequested -> "Requested"
                    else -> "Follow"
                },
                onClick = onFollowClick,
                icon = when {
                    isFollowing -> Icons.Outlined.Check
                    isRequested -> Icons.Outlined.HourglassTop
                    else -> Icons.Outlined.Add
                },
                tone = if (isFollowing || isRequested) NebButtonTone.Tonal else NebButtonTone.Primary,
                size = NebButtonSize.Small
            )
        }
    }
}

@Composable
private fun ProfileStatsRow(
    profile: UserProfileResponse,
    followerCount: Int,
    onFollowersClick: () -> Unit,
    onFollowingClick: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(22.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        ProfileInlineStat(
            value = compactCount(followerCount),
            label = if (followerCount == 1) "Follower" else "Followers",
            onClick = onFollowersClick
        )
        ProfileInlineStat(
            value = compactCount(profile.followingCount),
            label = "Following",
            onClick = onFollowingClick
        )
        if (profile.isBot) {
            ProfileInlineStat(value = compactCount(profile.replyCount), label = "Replies")
        } else {
            ProfileInlineStat(value = compactCount(profile.postCount), label = "Posts")
        }
    }
}

@Composable
private fun ProfileInlineStat(
    value: String,
    label: String,
    onClick: (() -> Unit)? = null
) {
    val base = Modifier.clip(RoundedCornerShape(6.dp))
    val rowModifier = if (onClick != null) {
        base.nebPressable(scale = 0.95f, tactile = TactileType.ButtonTap, onClick = onClick)
    } else {
        base
    }
    Row(
        modifier = rowModifier.padding(vertical = 2.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1
        )
    }
}

@Composable
private fun MetaItem(
    text: String,
    icon: ImageVector? = null,
    painter: Int? = null,
    onClick: (() -> Unit)? = null
) {
    val scheme = MaterialTheme.colorScheme
    val rowModifier = if (onClick != null) {
        Modifier
            .clip(RoundedCornerShape(6.dp))
            .nebPressable(scale = 0.96f, tactile = TactileType.ButtonTap, onClick = onClick)
    } else {
        Modifier
    }
    Row(
        modifier = rowModifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        when {
            icon != null -> Icon(
                imageVector = icon,
                contentDescription = null,
                tint = scheme.onSurfaceVariant,
                modifier = Modifier.size(14.dp)
            )
            painter != null -> Icon(
                painter = painterResource(id = painter),
                contentDescription = null,
                tint = scheme.onSurfaceVariant,
                modifier = Modifier.size(14.dp)
            )
        }
        Text(
            text = text,
            style = MaterialTheme.typography.bodySmall,
            color = scheme.onSurfaceVariant,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
private fun AchievementPillChip(label: String) {
    Text(
        text = label,
        style = MaterialTheme.typography.labelSmall,
        fontWeight = FontWeight.SemiBold,
        color = MaterialTheme.colorScheme.onSurface,
        maxLines = 1,
        modifier = Modifier
            .clip(RoundedCornerShape(percent = 50))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(horizontal = 10.dp, vertical = 5.dp)
    )
}

@Composable
private fun SocialLinkRow(
    links: List<ApiSocialLink>,
    onSocialLinkClick: (ApiSocialLink) -> Unit
) {
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    val scheme = MaterialTheme.colorScheme

    @OptIn(ExperimentalLayoutApi::class)
    FlowRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        links.forEach { link ->
            val iconRes = socialIconRes(link.platform)
            Box(
                modifier = Modifier
                    .size(34.dp)
                    .clip(CircleShape)
                    .background(scheme.surfaceContainerHigh)
                    .nebPressable(scale = 0.9f, tactile = TactileType.ButtonTap) {
                        onSocialLinkClick(link)
                        try {
                            uriHandler.openUri(link.url)
                        } catch (_: Exception) {
                            Toast.makeText(context, "Invalid link", Toast.LENGTH_SHORT).show()
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                if (iconRes != null) {
                    Icon(
                        painter = painterResource(id = iconRes),
                        contentDescription = link.platformLabel,
                        tint = Color.Unspecified,
                        modifier = Modifier.size(17.dp)
                    )
                } else {
                    val domain = link.websiteDomain.takeIf { it.isNotBlank() }
                        ?: link.url.removePrefix("https://").removePrefix("http://")
                            .substringBefore("/").substringBefore("?")
                    AsyncImage(
                        model = "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON" +
                            "&fallback_opts=TYPE,SIZE,URL&url=https://$domain&size=64",
                        contentDescription = link.platformLabel,
                        modifier = Modifier.size(17.dp),
                        error = painterResource(R.drawable.ic_globe),
                        placeholder = null
                    )
                }
            }
        }
    }
}

private fun socialIconRes(platform: String): Int? = when (platform.lowercase().trim()) {
    "instagram" -> R.drawable.ic_instagram
    "facebook" -> R.drawable.ic_facebook
    "twitter", "x" -> R.drawable.ic_twitter
    "youtube" -> R.drawable.ic_youtube
    "linkedin" -> R.drawable.ic_linkedin
    "github" -> R.drawable.ic_github
    "tiktok" -> R.drawable.ic_tiktok
    "telegram" -> R.drawable.ic_telegram
    "discord" -> R.drawable.ic_discord
    else -> null
}

/** What the header looks like before the profile lands. */
@Composable
fun ProfileHeaderSkeleton(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxWidth()) {
        ShimmerLine(height = 160.dp, shape = RoundedCornerShape(0.dp))
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = HeaderIndent)
                .offset(y = (-40).dp)
        ) {
            ShimmerCircle(size = 92.dp)
        }
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = HeaderIndent)
                .offset(y = (-28).dp)
        ) {
            ShimmerLine(widthFraction = 0.5f, height = 20.dp)
            Spacer(modifier = Modifier.height(8.dp))
            ShimmerLine(widthFraction = 0.32f, height = 12.dp)
            Spacer(modifier = Modifier.height(14.dp))
            ShimmerLine(widthFraction = 0.95f, height = 11.dp)
            Spacer(modifier = Modifier.height(6.dp))
            ShimmerLine(widthFraction = 0.78f, height = 11.dp)
            Spacer(modifier = Modifier.height(16.dp))
            ShimmerLine(widthFraction = 0.6f, height = 14.dp)
        }
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
    }
}
