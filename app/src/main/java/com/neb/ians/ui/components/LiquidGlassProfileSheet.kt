package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ExitToApp
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.outlined.Build
import androidx.compose.material.icons.outlined.Newspaper
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LiquidGlassProfileSheet(
    displayName: String,
    username: String,
    role: String?,
    photoUrl: String?,
    onDismiss: () -> Unit,
    onProfileClick: () -> Unit,
    onBookmarksClick: () -> Unit,
    onDownloadsClick: () -> Unit,
    onBlogClick: () -> Unit,
    onToolsClick: () -> Unit,
    onSettingsClick: () -> Unit,
    onSignOutClick: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp)
    val isDark = MaterialTheme.colorScheme.surface.luminanceIsDark()

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
        scrimColor = Color.Black.copy(alpha = if (isDark) 0.54f else 0.32f),
        shape = shape,
        dragHandle = null
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(start = 16.dp, top = 10.dp, end = 16.dp, bottom = 18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Box(
                modifier = Modifier
                    .align(Alignment.CenterHorizontally)
                    .width(42.dp)
                    .height(4.dp)
                    .background(MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.28f), CircleShape)
            )

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .clickable(onClick = onProfileClick)
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                NebAvatar(
                    name = displayName.ifBlank { "N" },
                    photoUrl = photoUrl,
                    size = 54.dp
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = displayName,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(Modifier.height(3.dp))
                    Text(
                        text = "@$username, ${roleLabel(role)}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Box(
                    modifier = Modifier
                        .size(38.dp)
                        .background(MaterialTheme.colorScheme.primaryContainer, CircleShape)
                        .clickable(onClick = onSettingsClick),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Settings,
                        contentDescription = "Settings",
                        tint = MaterialTheme.colorScheme.onPrimaryContainer,
                        modifier = Modifier.size(19.dp)
                    )
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                ProfileGlassAction(
                    icon = Icons.Filled.Bookmark,
                    label = "Bookmarks",
                    onClick = onBookmarksClick,
                    modifier = Modifier.weight(1f)
                )
                ProfileGlassAction(
                    icon = Icons.Filled.Download,
                    label = "Downloads",
                    onClick = onDownloadsClick,
                    modifier = Modifier.weight(1f)
                )
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .padding(vertical = 6.dp)
            ) {
                ProfileGlassRow(Icons.Outlined.Newspaper, "Blog", onBlogClick)
                ProfileGlassRow(Icons.Outlined.Build, "Tools", onToolsClick)
                HorizontalDivider(
                    modifier = Modifier.padding(horizontal = 16.dp),
                    color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.42f)
                )
                ProfileGlassRow(
                    icon = Icons.Outlined.ExitToApp,
                    label = "Sign out",
                    onClick = onSignOutClick,
                    contentColor = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

@Composable
private fun ProfileGlassAction(
    icon: ImageVector,
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .height(64.dp)
            .clip(RoundedCornerShape(20.dp))
            .background(MaterialTheme.colorScheme.secondaryContainer)
            .clickable(onClick = onClick)
            .padding(horizontal = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSecondaryContainer,
            modifier = Modifier.size(21.dp)
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSecondaryContainer,
            fontWeight = FontWeight.SemiBold
        )
    }
}

@Composable
private fun ProfileGlassRow(
    icon: ImageVector,
    label: String,
    onClick: () -> Unit,
    contentColor: Color = MaterialTheme.colorScheme.onSurface
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(54.dp)
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = contentColor.copy(alpha = 0.86f),
            modifier = Modifier.size(21.dp)
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodyLarge,
            color = contentColor,
            fontWeight = FontWeight.Medium
        )
    }
}

private fun roleLabel(role: String?): String = when (role) {
    "teacher" -> "Teacher"
    "institution" -> "Institution"
    "explorer" -> "Explorer"
    else -> "Student"
}

private fun Color.luminanceIsDark(): Boolean {
    return 0.299f * red + 0.587f * green + 0.114f * blue < 0.5f
}
