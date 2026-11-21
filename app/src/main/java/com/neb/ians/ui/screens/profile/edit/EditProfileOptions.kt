package com.neb.ians.ui.screens.profile.edit

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.Explore
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.outlined.School
import androidx.compose.ui.graphics.vector.ImageVector
import com.neb.ians.R

internal data class EditRole(
    val key: String,
    val title: String,
    val subtitle: String,
    val icon: ImageVector
)

internal val EDIT_ROLES = listOf(
    EditRole("student", "Student", "Learn, ask and save resources", Icons.Outlined.School),
    EditRole("teacher", "Teacher", "Teach, guide and share resources", Icons.AutoMirrored.Outlined.MenuBook),
    EditRole("institution", "Institution", "Represent a school or college", Icons.Outlined.AccountBalance),
    EditRole("explorer", "Explorer", "Browse first, fill the rest in later", Icons.Outlined.Explore)
)

internal val EDIT_INSTITUTION_TYPES = listOf("School", "College", "Academy", "Other")

internal data class SocialPlatform(
    val key: String,
    val label: String,
    val fieldLabel: String,
    val placeholder: String,
    val help: String
)

internal val SOCIAL_PLATFORMS = listOf(
    SocialPlatform("instagram", "Instagram", "Username or link", "username", "We turn a handle into a full Instagram link."),
    SocialPlatform("facebook", "Facebook", "Username or link", "username", "We turn a handle into a full Facebook link."),
    SocialPlatform("twitter", "X (Twitter)", "Username or link", "username", "An X handle or the full profile URL."),
    SocialPlatform("youtube", "YouTube", "Channel or link", "channel", "A channel name or the full channel URL."),
    SocialPlatform("tiktok", "TikTok", "Username or link", "username", "A TikTok handle or profile URL."),
    SocialPlatform("linkedin", "LinkedIn", "Username or link", "username", "A LinkedIn handle or profile URL."),
    SocialPlatform("github", "GitHub", "Username or link", "username", "A GitHub handle or profile URL."),
    SocialPlatform("telegram", "Telegram", "Username or link", "username", "A Telegram handle or invite link."),
    SocialPlatform("whatsapp", "WhatsApp", "Number or link", "98XXXXXXXX", "A phone number or a direct chat link."),
    SocialPlatform("discord", "Discord", "Invite or username", "username", "A server invite link or a username."),
    SocialPlatform("snapchat", "Snapchat", "Username or link", "username", "A Snapchat handle or profile URL."),
    SocialPlatform("pinterest", "Pinterest", "Username or link", "username", "A Pinterest handle or profile URL."),
    SocialPlatform("reddit", "Reddit", "Username or link", "username", "A Reddit handle or profile URL."),
    SocialPlatform("website", "Website", "Website URL", "https://your.site", "Any other link you want on your profile.")
)

internal fun socialIconRes(platform: String): Int? = when (platform.lowercase().trim()) {
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

internal fun socialDomainOf(url: String, fallbackDomain: String): String =
    fallbackDomain.takeIf { it.isNotBlank() }
        ?: url.removePrefix("https://").removePrefix("http://").substringBefore("/").substringBefore("?")
