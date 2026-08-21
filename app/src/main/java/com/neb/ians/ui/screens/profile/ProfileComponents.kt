package com.neb.ians.ui.screens.profile

import com.neb.ians.ui.components.LinkifyText

import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import com.neb.ians.R
import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiSocialLink
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.ProfileBanner
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.WebPostCard
import com.neb.ians.ui.components.buildInlineAnnotatedString
import com.neb.ians.ui.components.markdownToInlinePreview
import coil.compose.AsyncImage
import androidx.compose.ui.platform.LocalUriHandler
import com.neb.ians.ui.components.bannerPresetFor
import com.neb.ians.ui.components.compactCount
import com.neb.ians.util.formatTimeAgo
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

import androidx.compose.ui.graphics.RectangleShape

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

data class AchievementPill(val key: String, val label: String, val color: Color)

fun parseAchievements(raw: String?): List<AchievementPill> {
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

fun plainTextPreview(content: String): String {
    return content
        .replace(Regex("!\\[[^\\]]*\\]\\([^)]*\\)"), "")
        .replace(Regex("\\[([^\\]]*)\\]\\([^)]*\\)"), "$1")
        .replace(Regex("[*_`#>~]"), "")
        .replace(Regex("\\s+"), " ")
        .trim()
}

fun formatJoined(createdAtMs: Long): String {
    if (createdAtMs <= 0) return ""
    return try {
        "Joined " + SimpleDateFormat("MMM yyyy", Locale.US).format(Date(createdAtMs))
    } catch (_: Exception) {
        ""
    }
}

fun formatRoleHeadline(profile: UserProfileResponse): String {
    if (profile.isBot) {
        return "AI Study Companion"
    }
    return when (profile.role) {
        "teacher" -> {
            val parts = mutableListOf<String>()
            parts.add("Teacher")
            if (!profile.teachingSubjects.isNullOrBlank()) {
                parts.add(profile.teachingSubjects.split(",").joinToString(", ") { it.trim() })
            }
            if (!profile.school.isNullOrBlank()) {
                parts.add(profile.school)
            }
            parts.joinToString(" · ")
        }
        "institution" -> {
            val type = when (profile.institutionType) {
                "school" -> "School"
                "college" -> "College"
                "academy" -> "Academy"
                else -> "Institution"
            }
            val parts = mutableListOf<String>()
            parts.add(type)
            if (!profile.school.isNullOrBlank()) {
                parts.add(profile.school)
            }
            parts.joinToString(" · ")
        }
        "explorer" -> {
            profile.school?.takeIf { it.isNotBlank() }
                ?: profile.classLevel?.takeIf { it.isNotBlank() }
                ?: "Explorer"
        }
        else -> {
            val classStr = when (profile.classLevel) {
                "11" -> "Class 11"
                "12" -> "Class 12"
                "+2 Passout" -> "+2 Passout"
                "Diploma" -> "Diploma"
                "Teacher" -> "Teacher / Educator"
                "Bachelors" -> "Bachelors"
                else -> profile.classLevel
            }
            val parts = mutableListOf<String>()
            if (!classStr.isNullOrBlank()) {
                parts.add(classStr)
            }
            if (!profile.subjects.isNullOrBlank()) {
                parts.add(profile.subjects.split(",").joinToString(", ") { it.trim() })
            }
            if (parts.isEmpty()) {
                "NEBians Member"
            } else {
                parts.joinToString(" | ")
            }
        }
    }
}

@Composable
fun ProfileHeaderCard(
    profile: UserProfileResponse,
    isSelf: Boolean,
    isFollowing: Boolean,
    isRequested: Boolean,
    followRequestsCount: Int,
    followerCount: Int,
    onEditProfile: () -> Unit,
    onFollowClick: () -> Unit,
    onAvatarClick: () -> Unit,
    onNavigateBack: () -> Unit,
    onAnalyticsClick: () -> Unit,
    onFollowersClick: () -> Unit,
    onFollowingClick: () -> Unit,
    onFollowRequestsClick: () -> Unit,
    onProfileClick: (String) -> Unit = {},
    onSocialLinkClick: ((ApiSocialLink) -> Unit)? = null
) {
    val badge = remember(profile) { buildBadgeInfo(profile) }
    val achievements = remember(profile.achievementBadges) { parseAchievements(profile.achievementBadges) }
    val preset = remember(profile) { bannerPresetFor(profile) }
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    var showMenu by remember { mutableStateOf(false) }

    val bioText = remember(profile) {
        if (!profile.bio.isNullOrBlank()) {
            profile.bio
        } else if (profile.isBot) {
            "Your friendly AI study buddy. Always learning, always here to help."
        } else if (profile.role == "institution") {
            "${profile.displayName ?: "An institution"} on NEBians."
        } else {
            val builder = StringBuilder()
            builder.append(profile.displayName?.takeIf { it.isNotBlank() } ?: "A NEBians member")
            if (!profile.school.isNullOrBlank()) {
                builder.append(" at ${profile.school}")
            }
            if (!profile.subjects.isNullOrBlank()) {
                builder.append(". Focusing on ${profile.subjects.split(",").joinToString(", ") { it.trim() }}")
            }
            builder.append(".")
            builder.toString()
        }
    }

    val location = remember(profile.district, profile.pradesh) {
        val list = mutableListOf<String>()
        if (!profile.district.isNullOrBlank()) {
            list.add(profile.district)
        }
        if (!profile.pradesh.isNullOrBlank()) {
            val cleanedProvince = when (val p = profile.pradesh) {
                "Province 1", "Koshi Province" -> "Koshi"
                "Madhesh Province", "Province 2" -> "Madhesh"
                "Bagmati Province", "Province 3" -> "Bagmati"
                "Gandaki Province", "Province 4" -> "Gandaki"
                "Lumbini Province", "Province 5" -> "Lumbini"
                "Karnali Province", "Province 6" -> "Karnali"
                "Sudurpashchim Province", "Province 7", "Sudurpaschim Province", "Sudurpashchim" -> "Sudurpashchim"
                else -> p
            }
            list.add(cleanedProvince)
        }
        list.joinToString(", ")
    }

    val joinedText = remember(profile.createdAt, profile.isBot) {
        val dateStr = formatJoined(profile.createdAt)
        if (profile.isBot) {
            if (dateStr.startsWith("Joined ")) {
                "Online since " + dateStr.substringAfter("Joined ")
            } else {
                "Online since " + dateStr
            }
        } else {
            dateStr
        }
    }

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 16.dp)
            .clip(RoundedCornerShape(24.dp)),
        shape = RoundedCornerShape(24.dp),
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
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 16.dp)
                        .offset(y = 48.dp)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest, CircleShape)
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
                                .clickable(onClick = onAvatarClick)
                        )
                    }
                }
            }

            Column(modifier = Modifier.padding(16.dp)) {
                Spacer(modifier = Modifier.height(38.dp))

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username,
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.ExtraBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false)
                    )
                    if (profile.verificationLevel > 0 && badge?.type != "verified") {
                        Spacer(modifier = Modifier.width(6.dp))
                        Icon(
                            imageVector = Icons.Filled.Verified,
                            contentDescription = "Verified",
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                    if (badge != null) {
                        Spacer(modifier = Modifier.width(8.dp))
                        NebBadge(badge)
                    }
                }

                if (!profile.displayName.isNullOrBlank()) {
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = "@${profile.username}",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }

                Text(
                    text = formatRoleHeadline(profile),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )

                Spacer(modifier = Modifier.height(16.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(40.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (profile.isBot) {
                        ProfileStatCell("Replies", compactCount(profile.replyCount))
                        ProfileStatCell("Followers", compactCount(followerCount), onClick = onFollowersClick)
                        ProfileStatCell("Following", compactCount(profile.followingCount), onClick = onFollowingClick)
                    } else {
                        ProfileStatCell("Followers", compactCount(followerCount), onClick = onFollowersClick)
                        ProfileStatCell("Following", compactCount(profile.followingCount), onClick = onFollowingClick)
                        ProfileStatCell("Posts", compactCount(profile.postCount))
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (isSelf) {
                        OutlinedButton(
                            onClick = onEditProfile,
                            modifier = Modifier.weight(1f),
                            shape = CircleShape,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.primary),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = MaterialTheme.colorScheme.primary
                            ),
                            contentPadding = PaddingValues(vertical = 12.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Filled.Edit,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Edit", fontWeight = FontWeight.Bold)
                        }

                        OutlinedButton(
                            onClick = onAnalyticsClick,
                            modifier = Modifier.weight(1f),
                            shape = CircleShape,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = MaterialTheme.colorScheme.onSurface
                            ),
                            contentPadding = PaddingValues(vertical = 12.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.TrendingUp,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Analytics", fontWeight = FontWeight.Bold)
                        }
                    } else {
                        Button(
                            onClick = onFollowClick,
                            modifier = Modifier.weight(1f),
                            shape = CircleShape,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = when {
                                    isFollowing -> MaterialTheme.colorScheme.surfaceVariant
                                    isRequested -> MaterialTheme.colorScheme.secondaryContainer
                                    else -> MaterialTheme.colorScheme.primary
                                },
                                contentColor = when {
                                    isFollowing -> MaterialTheme.colorScheme.onSurfaceVariant
                                    isRequested -> MaterialTheme.colorScheme.onSecondaryContainer
                                    else -> Color.White
                                }
                            ),
                            contentPadding = PaddingValues(vertical = 12.dp)
                        ) {
                            Icon(
                                imageVector = when {
                                    isFollowing -> Icons.Outlined.Check
                                    isRequested -> Icons.Outlined.HourglassTop
                                    else -> Icons.Outlined.Add
                                },
                                contentDescription = null,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                text = when {
                                    isFollowing -> "Following"
                                    isRequested -> "Requested"
                                    else -> "Follow"
                                },
                                fontWeight = FontWeight.Bold
                            )
                        }

                        OutlinedButton(
                            onClick = {
                                clipboard.setText(AnnotatedString("@${profile.username}"))
                                Toast.makeText(context, "Mention handle copied", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.weight(1f),
                            shape = CircleShape,
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                            contentPadding = PaddingValues(vertical = 12.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.AlternateEmail,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                text = if (profile.isBot) "Try Neby" else "Mention",
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }
                }

                if (isSelf && profile.isLocked == 1) {
                    Spacer(modifier = Modifier.height(12.dp))
                    OutlinedButton(
                        onClick = onFollowRequestsClick,
                        modifier = Modifier.fillMaxWidth(),
                        shape = CircleShape,
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.secondary),
                        colors = ButtonDefaults.outlinedButtonColors(
                            contentColor = MaterialTheme.colorScheme.secondary
                        ),
                        contentPadding = PaddingValues(vertical = 12.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.GroupAdd,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        val label = if (followRequestsCount > 0) "Follow Requests ($followRequestsCount)" else "Follow Requests"
                        Text(label, fontWeight = FontWeight.Bold)
                    }
                }

                if (achievements.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(14.dp))
                    @OptIn(ExperimentalLayoutApi::class)
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

                Spacer(modifier = Modifier.height(16.dp))
                val outlineVariantColor = MaterialTheme.colorScheme.outlineVariant
                Canvas(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(1.dp)
                ) {
                    drawLine(
                        color = outlineVariantColor,
                        start = Offset(0f, 0f),
                        end = Offset(size.width, 0f),
                        pathEffect = PathEffect.dashPathEffect(floatArrayOf(6f, 6f), 0f),
                        strokeWidth = 1.dp.toPx()
                    )
                }
                Spacer(modifier = Modifier.height(16.dp))

                Text(
                    text = if (profile.isBot) "ABOUT NEBY" else "ABOUT",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.ExtraBold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(8.dp))
                LinkifyText(
                    text = bioText,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )

                if (location.isNotBlank() || !profile.school.isNullOrBlank() || joinedText.isNotBlank()) {
                    Spacer(modifier = Modifier.height(12.dp))
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (location.isNotBlank()) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.Place,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp),
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Text(
                                    text = location,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }

                        if (!profile.school.isNullOrBlank()) {
                            val hasLinkedSchool = !profile.schoolUsername.isNullOrBlank()
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                                modifier = if (hasLinkedSchool) Modifier.clickable { onProfileClick(profile.schoolUsername!!) } else Modifier
                            ) {
                                Icon(
                                    painter = painterResource(id = R.drawable.ic_school),
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp),
                                    tint = if (hasLinkedSchool) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Text(
                                    text = profile.school,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = if (hasLinkedSchool) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    textDecoration = androidx.compose.ui.text.style.TextDecoration.None
                                )
                            }
                        }

                        if (joinedText.isNotBlank()) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.CalendarToday,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp),
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Text(
                                    text = joinedText,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                        }
                    }
                }
            }

            if (profile.socialLinks.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(14.dp))
                    @OptIn(ExperimentalLayoutApi::class)
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        profile.socialLinks.forEach { link ->
                            val p = link.platform.lowercase().trim()
                            val iconRes: Int? = when (p) {
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
                            Box(
                                modifier = Modifier
                                    .size(34.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f))
                                    .clickable {
                                        onSocialLinkClick?.invoke(link)
                                        try {
                                            uriHandler.openUri(link.url)
                                        } catch (e: Exception) {
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
                                        modifier = Modifier.size(18.dp)
                                    )
                                } else {
                                    val domain = link.websiteDomain.takeIf { it.isNotBlank() }
                                        ?: link.url.removePrefix("https://").removePrefix("http://")
                                            .substringBefore("/").substringBefore("?")
                                        ?: "${link.platform}.com"
                                    val faviconUrl = "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://$domain&size=64"
                                    AsyncImage(
                                        model = faviconUrl,
                                        contentDescription = link.platformLabel,
                                        modifier = Modifier.size(18.dp),
                                        error = androidx.compose.ui.res.painterResource(R.drawable.ic_globe),
                                        placeholder = null
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ProfileStatCell(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null
) {
    val cellModifier = if (onClick != null) {
        modifier.clip(RoundedCornerShape(4.dp)).clickable(onClick = onClick)
    } else {
        modifier
    }
    Column(
        modifier = cellModifier,
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1
        )
        Text(
            text = value,
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.ExtraBold,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1
        )
    }
}

@Composable
fun PrivateProfileNotice() {
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

@Composable
fun ProfilePostCard(post: ApiPost, onClick: () -> Unit) {
    WebPostCard(
        post = post,
        onClick = onClick,
        onLikeClick = {},
        compact = true
    )
}

@Composable
fun ProfileReplyCard(reply: ApiReply, onClick: () -> Unit) {
    val preview = remember(reply.content) { markdownToInlinePreview(reply.content) }
    val primary = MaterialTheme.colorScheme.primary
    val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
    val bodyColor = MaterialTheme.colorScheme.onSurfaceVariant
    val previewAnnotated = remember(preview, primary, codeBg, bodyColor) {
        buildInlineAnnotatedString(preview, bodyColor, primary, codeBg)
    }
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
                text = "Reply on ${reply.postTitle.ifBlank { "Discussion" }}",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (preview.isNotBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = previewAnnotated,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "${formatTimeAgo(reply.createdAt)} \u00B7 ${compactCount(reply.thumbsUpCount)} likes",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
fun ProfileEmptyTabBox(
    title: String,
    message: String,
    icon: ImageVector
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(24.dp)
                )
            }
            Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = message,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
fun ProfileProgressIndicator() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator(modifier = Modifier.size(26.dp), strokeWidth = 3.dp)
    }
}

@Composable
fun ProfileLoadMoreButton(onClick: () -> Unit) {
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = WebPillShape,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Text("Load more", fontWeight = FontWeight.Bold)
    }
}

@Composable
fun AboutStatsCard(profile: UserProfileResponse) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.Leaderboard,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = "Stats",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth()) {
                Box(modifier = Modifier.weight(1f)) {
                    AboutStatItem(value = compactCount(profile.postCount), label = "Discussions")
                }
                Box(modifier = Modifier.weight(1f)) {
                    AboutStatItem(value = compactCount(profile.replyCount), label = "Replies")
                }
                Box(modifier = Modifier.weight(1f)) {
                    AboutStatItem(value = compactCount(profile.followerCount), label = "Followers")
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth()) {
                Box(modifier = Modifier.weight(1f)) {
                    AboutStatItem(value = compactCount(profile.likesReceivedCount), label = "Likes Received")
                }
                Box(modifier = Modifier.weight(1f)) {
                    AboutStatItem(value = compactCount(profile.contributionScore), label = "NEBian Score", isAcademic = true)
                }
                Box(modifier = Modifier.weight(1f)) {
                    AboutStatItem(value = compactCount(profile.followingCount), label = "Following")
                }
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
            color = if (isAcademic) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun AboutAchievementsCard(profile: UserProfileResponse) {
    val achievements = remember(profile.achievementBadges) { parseAchievements(profile.achievementBadges) }
    val postCount = profile.postCount
    val replyCount = profile.replyCount
    val likesReceived = profile.likesReceivedCount

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.WorkspacePremium,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = "Achievements",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            Spacer(modifier = Modifier.height(16.dp))

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
                        AchievementBadgePill(label = ach.label, color = ach.color, icon = Icons.Outlined.WorkspacePremium)
                    }
                    if (postCount >= 1) {
                        AchievementBadgePill(label = "First Discussion", color = Color(0xFF1B9AF0), icon = Icons.Outlined.Chat)
                    }
                    if (replyCount >= 1) {
                        AchievementBadgePill(label = "First Reply", color = Color(0xFF2E7D32), icon = Icons.Outlined.ChatBubble)
                    }
                    if (likesReceived >= 1) {
                        AchievementBadgePill(label = "First Thumb Received", color = Color(0xFFF59E0B), icon = Icons.Outlined.ThumbUp)
                    }
                }
            }
        }
    }
}

@Composable
private fun AchievementBadgePill(label: String, color: Color, icon: ImageVector) {
    Surface(
        shape = WebPillShape,
        color = color.copy(alpha = 0.12f),
        border = BorderStroke(1.dp, color.copy(alpha = 0.25f))
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(16.dp)
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                color = color
            )
        }
    }
}

@Composable
fun AboutDetailsCard(profile: UserProfileResponse, onProfileClick: (String) -> Unit = {}) {
    val pradesh = profile.pradesh
    val district = profile.district
    val joinedText = formatJoined(profile.createdAt)

    val location = remember(pradesh, district) {
        val list = mutableListOf<String>()
        if (!district.isNullOrBlank()) {
            list.add(district)
        }
        if (!pradesh.isNullOrBlank()) {
            val cleaned = when (pradesh) {
                "Province 1", "Koshi Province" -> "Koshi"
                "Madhesh Province", "Province 2" -> "Madhesh"
                "Bagmati Province", "Province 3" -> "Bagmati"
                "Gandaki Province", "Province 4" -> "Gandaki"
                "Lumbini Province", "Province 5" -> "Lumbini"
                "Karnali Province", "Province 6" -> "Karnali"
                "Sudurpashchim Province", "Province 7", "Sudurpaschim Province", "Sudurpashchim" -> "Sudurpashchim"
                else -> pradesh
            }
            list.add(cleaned)
        }
        list.joinToString(", ")
    }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.Info,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = "Details",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                if (!profile.classLevel.isNullOrBlank()) {
                    val classStr = when (profile.classLevel) {
                        "11" -> "Class 11"
                        "12" -> "Class 12"
                        "+2 Passout" -> "+2 Passout"
                        "Diploma" -> "Diploma"
                        "Teacher" -> "Teacher"
                        "Bachelors" -> "Bachelors"
                        else -> profile.classLevel
                    }
                    AboutDetailRow(icon = Icons.Outlined.School, label = "Class", value = classStr ?: "")
                }
                if (!profile.subjects.isNullOrBlank()) {
                    val formattedSubjects = profile.subjects.split(",").joinToString(", ") { it.trim() }
                    AboutDetailRow(icon = Icons.Outlined.MenuBook, label = "Subjects", value = formattedSubjects)
                }
                if (!profile.school.isNullOrBlank()) {
                    val hasLinkedSchool = !profile.schoolUsername.isNullOrBlank()
                    AboutDetailRow(
                        icon = Icons.Outlined.Apartment,
                        label = "School",
                        value = profile.school ?: "",
                        onClick = if (hasLinkedSchool) ({ onProfileClick(profile.schoolUsername!!) }) else null
                    )
                }
                if (location.isNotBlank()) {
                    AboutDetailRow(icon = Icons.Outlined.LocationOn, label = "Location", value = location)
                }
                if (joinedText.isNotBlank()) {
                    AboutDetailRow(icon = Icons.Outlined.CalendarMonth, label = "Joined", value = joinedText)
                }
                if (!profile.gender.isNullOrBlank()) {
                    AboutDetailRow(icon = Icons.Outlined.Person, label = "Gender", value = profile.gender ?: "")
                }
            }
        }
    }
}

@Composable
private fun AboutDetailRow(icon: ImageVector, label: String, value: String, onClick: (() -> Unit)? = null) {
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
            tint = if (isClickable) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
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
            color = if (isClickable) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
            textDecoration = androidx.compose.ui.text.style.TextDecoration.None,
            modifier = Modifier.weight(1f)
        )
    }
}

@Composable
fun AboutProgressCard(profile: UserProfileResponse) {
    val subjects = remember(profile.subjects) {
        if (profile.subjects.isNullOrBlank()) emptyList()
        else profile.subjects.split(",").map { it.trim() }.filter { it.isNotBlank() }
    }
    if (subjects.isEmpty() || profile.isBot) return

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.TrendingUp,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = "Progress",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
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
}
