package com.neb.ians.ui.screens.notifications

import androidx.compose.animation.animateColorAsState
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.PersonAdd
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiNotification
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.util.formatTimeAgo

@Composable
fun NotificationItem(
    notification: ApiNotification,
    onClick: () -> Unit,
    onAvatarClick: () -> Unit = {}
) {
    val isSystem = notification.actorName.isNullOrBlank() ||
        notification.actorName.equals("System", ignoreCase = true) ||
        notification.verb.equals("system", ignoreCase = true)
    val unread = !notification.isRead

    val container by animateColorAsState(
        targetValue = if (unread) {
            MaterialTheme.colorScheme.surfaceContainerHigh
        } else {
            MaterialTheme.colorScheme.surfaceContainerLowest
        },
        animationSpec = nebEffectsSpec(),
        label = "notif_container"
    )

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(20.dp))
            .background(container)
            .clickable(onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 13.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box {
            if (isSystem) {
                Box(
                    modifier = Modifier
                        .size(42.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Notifications,
                        contentDescription = null,
                        modifier = Modifier.size(20.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            } else {
                Avatar(
                    name = notification.actorName ?: "?",
                    imageUrl = notification.actorPhotoUrl,
                    size = 42.dp,
                    modifier = Modifier.clickable(onClick = onAvatarClick)
                )
            }
            Box(
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .size(18.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surface),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = verbIcon(notification.verb),
                    contentDescription = null,
                    modifier = Modifier.size(11.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = notificationMessage(notification),
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = if (unread) FontWeight.SemiBold else FontWeight.Normal,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(3.dp))
            Text(
                text = formatTimeAgo(notification.createdAt),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1
            )
        }

        if (unread) {
            Box(
                modifier = Modifier
                    .padding(top = 7.dp)
                    .size(7.dp)
                    .background(MaterialTheme.colorScheme.onSurface, CircleShape)
            )
        }
    }
}

private fun notificationMessage(notification: ApiNotification): String {
    if (notification.message.isNotBlank()) return notification.message
    val actor = notification.actorName?.takeIf { it.isNotBlank() } ?: "Someone"
    return when (notification.verb.lowercase()) {
        "like_post" -> "$actor liked your post"
        "like_reply" -> "$actor liked your reply"
        "reply" -> "$actor replied to your post"
        "reply_reply" -> "$actor replied to your comment"
        "follow" -> "$actor started following you"
        "follow_request" -> "$actor requested to follow you"
        "mention" -> "$actor mentioned you"
        "like_resource" -> "$actor liked your resource"
        "like_resource_comment" -> "$actor liked your comment"
        "resource_comment" -> "$actor commented on your resource"
        "resource_comment_reply" -> "$actor replied to your comment"
        else -> "New activity on your account"
    }
}

private fun verbIcon(verb: String): ImageVector {
    val v = verb.lowercase()
    return when {
        "like" in v || "thumb" in v -> Icons.Outlined.ThumbUp
        "repl" in v || "comment" in v -> Icons.AutoMirrored.Outlined.Reply
        "follow" in v -> Icons.Outlined.PersonAdd
        "mention" in v -> Icons.Outlined.AlternateEmail
        else -> Icons.Outlined.Notifications
    }
}

fun handleNotificationClick(
    notification: ApiNotification,
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    onResourceClick: (String) -> Unit
) {
    val targetType = notification.targetType ?: ""
    val targetId = notification.targetId ?: ""
    val referenceType = notification.referenceType ?: ""
    val referenceId = notification.referenceId ?: ""
    val actorUsername = notification.actorName

    when (notification.verb) {
        "follow", "follow_request" -> {
            if (!actorUsername.isNullOrBlank()) onProfileClick(actorUsername)
        }
        else -> when (targetType) {
            "post" -> if (targetId.isNotBlank()) onPostClick(targetId)
            "reply" -> {
                val postId = if (referenceType == "post") referenceId else ""
                if (postId.isNotBlank()) onPostClick(postId)
            }
            "resource" -> if (targetId.isNotBlank()) onResourceClick(targetId)
            "resource_comment" -> {
                val resourceId = if (referenceType == "resource") referenceId else ""
                if (resourceId.isNotBlank()) onResourceClick(resourceId)
            }
            "user" -> if (!actorUsername.isNullOrBlank()) onProfileClick(actorUsername)
            else -> {}
        }
    }
}
