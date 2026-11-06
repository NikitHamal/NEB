package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import java.security.MessageDigest

/**
 * Who a post goes out as: the account or its anonymous mask.
 *
 * The avatar (and name) is the control and a flat dropdown picks between the two, the
 * same menu the web composer opens: a section for the mask, a section for yourself,
 * a tick on the active row. It replaces the old on/off anonymous switch.
 */
@Composable
fun NebIdentityPicker(
    isAnonymous: Boolean,
    userName: String,
    handle: String,
    photoUrl: String?,
    anonTag: String,
    onSelect: (anonymous: Boolean) -> Unit,
    modifier: Modifier = Modifier,
    showName: Boolean = true,
    avatarSize: Dp = 28.dp,
    enabled: Boolean = true
) {
    val scheme = MaterialTheme.colorScheme
    var open by remember { mutableStateOf(false) }
    val shape = RoundedCornerShape(22.dp)

    Box(modifier = modifier) {
        Row(
            modifier = Modifier
                .heightIn(min = 40.dp)
                .clip(shape)
                .background(scheme.surfaceContainerLow)
                .nebPressable(enabled = enabled, onClick = { open = true })
                .padding(start = 6.dp, end = 10.dp, top = 4.dp, bottom = 4.dp)
                .semantics {
                    role = Role.Button
                    contentDescription = "Switch identity"
                },
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            IdentityAvatar(isAnonymous, userName, photoUrl, avatarSize)
            if (showName) {
                Text(
                    text = if (isAnonymous) anonTag else userName.ifBlank { "You" },
                    style = MaterialTheme.typography.labelLarge,
                    color = scheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.widthIn(max = 120.dp)
                )
            }
            NebIcon(NebIcons.ChevronDown, "Choose identity", size = 20.dp, tint = scheme.onSurface)
        }

        IdentityDropdown(
            open = open,
            onDismiss = { open = false },
            isAnonymous = isAnonymous,
            userName = userName,
            handle = handle,
            photoUrl = photoUrl,
            anonTag = anonTag,
            onSelect = onSelect
        )
    }
}

/**
 * The composer's leading control on the web: the identity's avatar with a small chevron badge at
 * its corner; tapping opens the same menu as [NebIdentityPicker].
 */
@Composable
fun NebIdentityAvatarMenu(
    isAnonymous: Boolean,
    userName: String,
    handle: String,
    photoUrl: String?,
    anonTag: String,
    onSelect: (anonymous: Boolean) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    avatarSize: Dp = 36.dp
) {
    val scheme = MaterialTheme.colorScheme
    var open by remember { mutableStateOf(false) }
    Box(
        modifier = modifier
            .size(avatarSize + 6.dp)
            .nebPressable(enabled = enabled, onClick = { open = true })
            .semantics {
                role = Role.Button
                contentDescription = "Switch identity"
            },
        contentAlignment = Alignment.Center
    ) {
        IdentityAvatar(isAnonymous, userName, photoUrl, avatarSize)
        Box(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .size(16.dp)
                .clip(CircleShape)
                .background(scheme.surfaceContainerHighest),
            contentAlignment = Alignment.Center
        ) {
            NebIcon(NebIcons.ChevronDown, null, size = 12.dp, tint = scheme.onSurface)
        }
        IdentityDropdown(
            open = open,
            onDismiss = { open = false },
            isAnonymous = isAnonymous,
            userName = userName,
            handle = handle,
            photoUrl = photoUrl,
            anonTag = anonTag,
            onSelect = onSelect
        )
    }
}

@Composable
private fun IdentityDropdown(
    open: Boolean,
    onDismiss: () -> Unit,
    isAnonymous: Boolean,
    userName: String,
    handle: String,
    photoUrl: String?,
    anonTag: String,
    onSelect: (anonymous: Boolean) -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    DropdownMenu(
        expanded = open,
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(24.dp),
        containerColor = nebMenuColor(),
        tonalElevation = 0.dp,
        shadowElevation = 0.dp
    ) {
        Column(modifier = Modifier.widthIn(min = 264.dp)) {
            IdentitySection("Post anonymously as")
            IdentityRow(
                active = isAnonymous,
                title = anonTag,
                sub = "Identity kept private",
                leading = { IdentityAvatar(true, userName, photoUrl, 32.dp) },
                onClick = { onSelect(true); onDismiss() }
            )
            Box(
                modifier = Modifier
                    .padding(vertical = 6.dp, horizontal = 16.dp)
                    .fillMaxWidth()
                    .height(1.dp)
                    .background(scheme.outlineVariant)
            )
            IdentitySection("Post as yourself")
            IdentityRow(
                active = !isAnonymous,
                title = userName.ifBlank { "You" },
                sub = handle.takeIf { it.isNotBlank() }?.let { "@" + it.removePrefix("@") },
                leading = { IdentityAvatar(false, userName, photoUrl, 32.dp) },
                onClick = { onSelect(false); onDismiss() }
            )
        }
    }
}

/** The menu fill: tonal in light (the page is white), a raised step in dark. */
@Composable
fun nebMenuColor(): Color {
    val scheme = MaterialTheme.colorScheme
    return if (scheme.surface.luminance() > 0.5f) scheme.surfaceContainerLow else scheme.surfaceContainerHigh
}

@Composable
private fun IdentitySection(label: String) {
    Text(
        text = label,
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 10.dp, bottom = 4.dp)
    )
}

@Composable
private fun IdentityRow(
    active: Boolean,
    title: String,
    sub: String?,
    leading: @Composable () -> Unit,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    Row(
        modifier = Modifier
            .padding(horizontal = 8.dp)
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(if (active) scheme.primaryContainer else Color.Transparent)
            .nebPressable(onClick = onClick)
            .padding(horizontal = 8.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        leading()
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.SemiBold),
                color = if (active) scheme.onPrimaryContainer else scheme.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            if (sub != null) {
                Text(
                    text = sub,
                    style = MaterialTheme.typography.bodySmall,
                    color = if (active) scheme.onPrimaryContainer else scheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
        if (active) {
            NebIcon(NebIcons.Check, null, size = 18.dp, tint = scheme.onPrimaryContainer)
        }
    }
}

/** The account's avatar, or the tonal disc with the crossed eye that stands for the mask. */
@Composable
fun IdentityAvatar(isAnonymous: Boolean, name: String, photoUrl: String?, size: Dp) {
    val scheme = MaterialTheme.colorScheme
    if (isAnonymous) {
        Box(
            modifier = Modifier
                .size(size)
                .clip(CircleShape)
                .background(scheme.surfaceContainerHighest),
            contentAlignment = Alignment.Center
        ) {
            NebIcon(NebIcons.EyeOff, null, size = size * 0.55f, tint = scheme.onSurfaceVariant)
        }
    } else {
        NebAvatar(photoUrl = photoUrl, name = name, size = size, showBorder = false)
    }
}

/** The same stable handle the server derives (`Anon#` plus four hex digits of SHA-256(user id)). */
fun anonTagFor(userId: String?): String {
    if (userId.isNullOrBlank()) return "Anonymous"
    val digest = MessageDigest.getInstance("SHA-256").digest(userId.toByteArray(Charsets.UTF_8))
    val hex = digest.joinToString("") { "%02x".format(it) }.take(4)
    return "Anon#$hex"
}
