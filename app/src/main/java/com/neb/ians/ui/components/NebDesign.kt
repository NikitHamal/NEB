package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material.icons.filled.Explore
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.ui.res.painterResource
import com.neb.ians.R
import androidx.compose.material3.Icon
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiBadgeInfo

// ---------------------------------------------------------------------------
// Brand extra colors (mirrors web --md-surface-muted / --md-border-subtle and
// the brand gradient used for the logo + accents).
// ---------------------------------------------------------------------------

object NebColors {
    val BrandGradientStart = Color(0xFF0058DF)
    val BrandGradientMid = Color(0xFF004BD4)
    val BrandGradientEnd = Color(0xFF003CC3)

    val brandBrush: Brush
        get() = Brush.linearGradient(listOf(BrandGradientStart, BrandGradientMid, BrandGradientEnd))
}

/** Subtle hairline border color matching web --md-border-subtle. */
@Composable
fun nebBorderSubtle(): Color = MaterialTheme.colorScheme.outlineVariant

// ---------------------------------------------------------------------------
// Cards — mirrors .md-card (surface-container-lowest, 1px outline-variant,
// radius 16, no shadow).
// ---------------------------------------------------------------------------

@Composable
fun NebCard(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    shape: RoundedCornerShape = RoundedCornerShape(16.dp),
    containerColor: Color = MaterialTheme.colorScheme.surfaceContainerLowest,
    border: BorderStroke? = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    content: @Composable () -> Unit
) {
    val base = modifier
        .clip(shape)
        .background(containerColor)
        .then(if (border != null) Modifier.border(border, shape) else Modifier)
    Box(
        modifier = if (onClick != null) {
            base.clickable(onClick = onClick)
        } else base
    ) { content() }
}

// ---------------------------------------------------------------------------
// Buttons — pill shaped, height 40, weight 600 (mirrors .md-btn*).
// ---------------------------------------------------------------------------

@Composable
private fun NebButtonBase(
    onClick: () -> Unit,
    container: Color,
    contentColor: Color,
    modifier: Modifier = Modifier,
    border: BorderStroke? = null,
    enabled: Boolean = true,
    leadingIcon: ImageVector? = null,
    text: String,
) {
    val shape = CircleShape
    val bg = if (enabled) container else container.copy(alpha = 0.4f)
    Row(
        modifier = modifier
            .defaultMinSize(minHeight = 40.dp)
            .clip(shape)
            .background(bg)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .clickable(enabled = enabled, onClick = onClick)
            .padding(horizontal = 22.dp, vertical = 9.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterHorizontally),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (leadingIcon != null) {
            Icon(leadingIcon, null, tint = contentColor, modifier = Modifier.size(18.dp))
        }
        Text(
            text = text,
            color = contentColor,
            fontWeight = FontWeight.SemiBold,
            fontSize = 14.sp,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun NebFilledButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    leadingIcon: ImageVector? = null,
) = NebButtonBase(
    onClick, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary,
    modifier, null, enabled, leadingIcon, text
)

@Composable
fun NebTonalButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    leadingIcon: ImageVector? = null,
) = NebButtonBase(
    onClick, MaterialTheme.colorScheme.secondaryContainer, MaterialTheme.colorScheme.onSecondaryContainer,
    modifier, null, enabled, leadingIcon, text
)

@Composable
fun NebOutlinedButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    leadingIcon: ImageVector? = null,
) = NebButtonBase(
    onClick, Color.Transparent, MaterialTheme.colorScheme.primary,
    modifier, BorderStroke(1.dp, MaterialTheme.colorScheme.outline), enabled, leadingIcon, text
)

@Composable
fun NebTextButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    leadingIcon: ImageVector? = null,
) = NebButtonBase(
    onClick, Color.Transparent, MaterialTheme.colorScheme.primary,
    modifier, null, enabled, leadingIcon, text
)

/** Round icon button mirroring .md-btn-icon (40dp, on-surface-variant). */
@Composable
fun NebIconButton(
    icon: ImageVector,
    contentDescription: String?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    tint: Color = MaterialTheme.colorScheme.onSurfaceVariant,
    size: Dp = 40.dp,
) {
    Box(
        modifier = modifier
            .size(size)
            .clip(CircleShape)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Icon(icon, contentDescription, tint = tint, modifier = Modifier.size(22.dp))
    }
}

// ---------------------------------------------------------------------------
// Chips — mirrors .md-chip / .md-chip-active.
// ---------------------------------------------------------------------------

@Composable
fun NebChip(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    leadingIcon: ImageVector? = null,
) {
    val shape = CircleShape
    val bg = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent
    val fg = if (selected) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
    val border = if (selected) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
    Row(
        modifier = modifier
            .clip(shape)
            .background(bg)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 7.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (leadingIcon != null) {
            Icon(leadingIcon, null, tint = fg, modifier = Modifier.size(16.dp))
        }
        Text(label, color = fg, fontSize = 13.sp, fontWeight = FontWeight.Medium, maxLines = 1)
    }
}

// ---------------------------------------------------------------------------
// Avatar with brand gradient ring + initials fallback.
// ---------------------------------------------------------------------------

@Composable
fun NebAvatar(
    photoUrl: String?,
    name: String,
    size: Dp = 40.dp,
    ring: Boolean = false,
    modifier: Modifier = Modifier,
) {
    val ringMod = if (ring) {
        Modifier
            .background(NebColors.brandBrush, CircleShape)
            .padding(2.dp)
    } else Modifier
    Box(modifier = modifier.then(ringMod), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(size)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center
        ) {
            if (!photoUrl.isNullOrBlank()) {
                AsyncImage(
                    model = photoUrl,
                    contentDescription = name,
                    modifier = Modifier.size(size).clip(CircleShape)
                )
            } else {
                Text(
                    text = name.trim().take(1).uppercase().ifBlank { "?" },
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = (size.value * 0.4f).sp
                )
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Role / verification badge (mirrors .role-badge-* / verified pills).
// ---------------------------------------------------------------------------

@Composable
fun NebBadge(badge: ApiBadgeInfo?, modifier: Modifier = Modifier) {
    if (badge == null) return
    val (bg, fg, icon, drawableRes) = badgeStyle(badge)
    Box(
        modifier = modifier
            .size(20.dp)
            .clip(CircleShape)
            .background(bg),
        contentAlignment = Alignment.Center
    ) {
        if (drawableRes != null) {
            Icon(
                painter = painterResource(id = drawableRes),
                contentDescription = badge.label,
                tint = fg,
                modifier = Modifier.size(11.dp)
            )
        } else if (icon != null) {
            Icon(
                imageVector = icon,
                contentDescription = badge.label,
                tint = fg,
                modifier = Modifier.size(11.dp)
            )
        }
    }
}

private data class BadgeStyle(val bg: Color, val fg: Color, val icon: ImageVector? = null, val drawableRes: Int? = null)

@Composable
private fun badgeStyle(badge: ApiBadgeInfo): BadgeStyle = when (badge.type) {
    "admin" -> BadgeStyle(Color(0xFFFEF3C7), Color(0xFF92400E), drawableRes = R.drawable.ic_crown)
    "moderator" -> BadgeStyle(Color(0xFFDBEAFE), Color(0xFF1E40AF), icon = Icons.Outlined.Shield)
    "verified" -> BadgeStyle(Color(0xFFDBEAFE), Color(0xFF1E40AF), icon = Icons.Filled.Verified)
    "teacher" -> BadgeStyle(Color(0xFFD1FAE5), Color(0xFF047857), icon = Icons.Filled.School)
    "institution" -> BadgeStyle(Color(0xFFE0E7FF), Color(0xFF4338CA), icon = Icons.Filled.AccountBalance)
    "explorer" -> BadgeStyle(Color(0xFFFEF3C7), Color(0xFFB45309), icon = Icons.Filled.Explore)
    "bot" -> BadgeStyle(Color(0xFFF3E8FF), Color(0xFF7E22CE), icon = Icons.Filled.AutoAwesome)
    else -> BadgeStyle(
        MaterialTheme.colorScheme.secondaryContainer,
        MaterialTheme.colorScheme.onSecondaryContainer,
        null
    )
}

// ---------------------------------------------------------------------------
// Section header — title + optional trailing "View all" action.
// ---------------------------------------------------------------------------

@Composable
fun NebSectionHeader(
    title: String,
    modifier: Modifier = Modifier,
    actionLabel: String? = null,
    onAction: (() -> Unit)? = null,
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Bottom
    ) {
        Text(
            title,
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )
        if (actionLabel != null && onAction != null) {
            Text(
                actionLabel,
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.clip(CircleShape).clickable(onClick = onAction).padding(horizontal = 8.dp, vertical = 4.dp)
            )
        }
    }
}

// ---------------------------------------------------------------------------
// Empty state.
// ---------------------------------------------------------------------------

@Composable
fun NebEmptyState(
    icon: ImageVector,
    title: String,
    subtitle: String? = null,
    modifier: Modifier = Modifier,
    action: (@Composable () -> Unit)? = null,
) {
    androidx.compose.foundation.layout.Column(
        modifier = modifier.fillMaxWidth().padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Surface(
            shape = CircleShape,
            color = MaterialTheme.colorScheme.surfaceContainerHigh,
            modifier = Modifier.size(72.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(icon, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(34.dp))
            }
        }
        Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        if (subtitle != null) {
            Text(
                subtitle,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
        }
        if (action != null) {
            Spacer(Modifier.height(4.dp))
            action()
        }
    }
}

// ---------------------------------------------------------------------------
// Small inline stat (icon + value) used on cards.
// ---------------------------------------------------------------------------

@Composable
fun NebStat(icon: ImageVector, value: String, tint: Color = MaterialTheme.colorScheme.onSurfaceVariant) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(3.dp)) {
        Icon(icon, null, tint = tint, modifier = Modifier.size(15.dp))
        Text(value, color = tint, fontSize = 12.sp, style = MaterialTheme.typography.labelMedium)
    }
}
