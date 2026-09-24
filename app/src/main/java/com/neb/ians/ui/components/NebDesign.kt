package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
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
import com.neb.ians.ui.avatar.blobatarAnim
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.ripple
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.ui.components.art.NebIconHalo
import com.neb.ians.util.TactileType

// ---------------------------------------------------------------------------
// Brand extra colors (mirrors web --md-surface-muted / --md-border-subtle and
// the brand gradient used for the logo + accents).
// ---------------------------------------------------------------------------

object NebColors {
    val BrandGradientStart = Color(0xFF313136)
    val BrandGradientMid = Color(0xFF1F1F21)
    val BrandGradientEnd = Color(0xFF0A0A0B)

    val brandBrush: Brush
        get() = Brush.linearGradient(listOf(BrandGradientStart, BrandGradientMid, BrandGradientEnd))
}

/** Subtle hairline border color matching web --md-border-subtle. */
@Composable
fun nebBorderSubtle(): Color = MaterialTheme.colorScheme.outline.copy(alpha = 0.16f)

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
    border: BorderStroke? = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.16f)),
    content: @Composable () -> Unit
) {
    val tactile = rememberTactileFeedback()
    val base = modifier
        .clip(shape)
        .background(containerColor)
        .then(if (border != null) Modifier.border(border, shape) else Modifier)
    Box(
        modifier = if (onClick != null) {
            base.clickable(onClick = {
                tactile.perform(TactileType.LightTap)
                onClick()
            })
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
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (isPressed && enabled) 0.94f else 1.0f,
        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
        label = "btnScale"
    )
    val tactile = rememberTactileFeedback()

    Row(
        modifier = modifier
            .defaultMinSize(minHeight = 40.dp)
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
            .clip(shape)
            .background(bg)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .clickable(
                enabled = enabled,
                interactionSource = interactionSource,
                indication = ripple(bounded = true, color = contentColor),
                onClick = {
                    tactile.perform(TactileType.ButtonTap)
                    onClick()
                }
            )
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
            fontWeight = FontWeight.Bold,
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
    modifier, BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant), enabled, leadingIcon, text
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
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (isPressed) 0.88f else 1.0f,
        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
        label = "iconBtnScale"
    )
    val tactile = rememberTactileFeedback()

    Box(
        modifier = modifier
            .size(size)
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
            .clip(CircleShape)
            .clickable(
                interactionSource = interactionSource,
                indication = ripple(bounded = true, color = tint),
                onClick = {
                    tactile.perform(TactileType.ButtonTap)
                    onClick()
                }
            ),
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
    val bg by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
        animationSpec = tween(180),
        label = "chipBg"
    )
    val fg by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
        animationSpec = tween(180),
        label = "chipFg"
    )
    val border = if (selected) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (isPressed) 0.94f else 1.0f,
        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
        label = "chipScale"
    )
    val tactile = rememberTactileFeedback()

    Row(
        modifier = modifier
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
            .clip(shape)
            .background(bg)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .clickable(
                interactionSource = interactionSource,
                indication = ripple(bounded = true),
                onClick = {
                    tactile.perform(TactileType.SelectionChange)
                    onClick()
                }
            )
            .padding(horizontal = 16.dp, vertical = 7.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (leadingIcon != null) {
            Icon(leadingIcon, null, tint = fg, modifier = Modifier.size(16.dp))
        }
        Text(label, color = fg, fontSize = 13.sp, fontWeight = FontWeight.Bold, maxLines = 1)
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
    showBorder: Boolean = true,
    verificationLevel: Int = 0,
    modifier: Modifier = Modifier,
) {
    val ringMod = if (ring) {
        Modifier
            .background(NebColors.brandBrush, CircleShape)
            .padding(2.dp)
    } else Modifier

    val resolvedUrl = remember(photoUrl) {
        if (photoUrl.isNullOrBlank()) null
        else {
            var url = photoUrl.trim()
            if (url.startsWith("http://127.0.0.1:8000/") || url.startsWith("http://localhost:8000/")) {
                url = url.replace("http://127.0.0.1:8000/", "https://nebians.consica.com.np/")
                         .replace("http://localhost:8000/", "https://nebians.consica.com.np/")
            }
            if (url.startsWith("http://") || url.startsWith("https://")) {
                url
            } else {
                "https://nebians.consica.com.np${if (url.startsWith("/")) "" else "/"}$url"
            }
        }
    }

    var isError by remember(resolvedUrl) { mutableStateOf(false) }
    val isNeby = remember(name) { name.equals("Neby", ignoreCase = true) || name.equals("neby", ignoreCase = true) }
    val nebAnim = remember(resolvedUrl) { com.neb.ians.ui.avatar.avatarAnimFromUrl(resolvedUrl) }
    val hasImageBgNeb = !isNeby && !resolvedUrl.isNullOrBlank() && !isError

    Box(modifier = modifier.then(ringMod), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(size)
                .clip(CircleShape)
                .background(
                    if (isNeby) Color.Transparent
                    else if (hasImageBgNeb) MaterialTheme.colorScheme.surfaceContainerLowest
                    else MaterialTheme.colorScheme.primaryContainer
                )
                .then(
                    if ((isNeby || hasImageBgNeb) && showBorder) Modifier.border(1.5.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape)
                    else Modifier
                ),
            contentAlignment = Alignment.Center
        ) {
            if (isNeby) {
                Box(contentAlignment = Alignment.Center) {
                    com.neb.ians.ui.avatar.neby.NebyAvatarMini(
                        animation = "idle",
                        size = size,
                        interactive = false
                    )
                }
            } else if (!resolvedUrl.isNullOrBlank() && !isError) {
                AsyncImage(
                    model = resolvedUrl,
                    contentDescription = name,
                    modifier = Modifier.size(size).clip(CircleShape).blobatarAnim(nebAnim),
                    contentScale = ContentScale.Crop,
                    onError = { isError = true }
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

        if (verificationLevel > 0) {
            val badgeColor = when (verificationLevel) {
                1 -> MaterialTheme.colorScheme.outline
                2 -> MaterialTheme.colorScheme.onSurfaceVariant
                else -> MaterialTheme.colorScheme.onSurface
            }
            val badgeSize = (size * 0.38f).coerceIn(13.dp, 20.dp)
            Box(
                modifier = Modifier
                    .size(badgeSize)
                    .align(Alignment.BottomEnd)
                    .background(MaterialTheme.colorScheme.surface, CircleShape)
                    .padding(1.dp),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Filled.Verified,
                    contentDescription = "Verified",
                    tint = badgeColor,
                    modifier = Modifier.size(badgeSize)
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
    val badgeSize = 20.dp
    val iconSize = 14.dp

    Surface(
        modifier = modifier.size(badgeSize),
        shape = CircleShape,
        color = bg,
        contentColor = fg
    ) {
        Box(contentAlignment = Alignment.Center) {
            when {
                drawableRes != null -> Icon(
                    painter = painterResource(id = drawableRes),
                    contentDescription = badge.label,
                    tint = fg,
                    modifier = Modifier.size(iconSize)
                )
                icon != null -> Icon(
                    imageVector = icon,
                    contentDescription = badge.label,
                    tint = fg,
                    modifier = Modifier.size(iconSize)
                )
            }
        }
    }
}

private data class BadgeStyle(val bg: Color, val fg: Color, val icon: ImageVector? = null, val drawableRes: Int? = null)

@Composable
private fun badgeStyle(badge: ApiBadgeInfo): BadgeStyle = when (badge.type) {
    "admin" -> BadgeStyle(
        MaterialTheme.colorScheme.inverseSurface,
        MaterialTheme.colorScheme.inverseOnSurface,
        drawableRes = R.drawable.ic_crown
    )
    "moderator" -> BadgeStyle(
        MaterialTheme.colorScheme.surfaceContainerHighest,
        MaterialTheme.colorScheme.onSurface,
        icon = Icons.Outlined.Shield
    )
    "verified" -> BadgeStyle(
        MaterialTheme.colorScheme.surfaceContainerHighest,
        MaterialTheme.colorScheme.onSurface,
        icon = Icons.Filled.Verified
    )
    "teacher" -> BadgeStyle(
        MaterialTheme.colorScheme.surfaceContainerHigh,
        MaterialTheme.colorScheme.onSurface,
        icon = Icons.Filled.School
    )
    "institution" -> BadgeStyle(
        MaterialTheme.colorScheme.surfaceContainerHigh,
        MaterialTheme.colorScheme.onSurface,
        icon = Icons.Filled.AccountBalance
    )
    "explorer" -> BadgeStyle(
        MaterialTheme.colorScheme.surfaceContainer,
        MaterialTheme.colorScheme.onSurfaceVariant,
        icon = Icons.Filled.Explore
    )
    "bot" -> BadgeStyle(
        MaterialTheme.colorScheme.surfaceContainer,
        MaterialTheme.colorScheme.onSurfaceVariant,
        icon = Icons.Filled.AutoAwesome
    )
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
        Box(contentAlignment = Alignment.Center) {
            NebIconHalo(diameter = 82.dp)
            Icon(icon, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(32.dp))
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

@Composable
fun ExpandableText(
    text: String,
    modifier: Modifier = Modifier,
    style: androidx.compose.ui.text.TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurfaceVariant,
    fontSize: androidx.compose.ui.unit.TextUnit = 13.sp,
    minimizedMaxLines: Int = 3
) {
    var isExpanded by remember { mutableStateOf(false) }
    var hasOverflow by remember { mutableStateOf(false) }

    androidx.compose.foundation.layout.Column(modifier = modifier) {
        LinkifyText(
            text = text,
            style = style,
            color = color,
            fontSize = fontSize,
            maxLines = if (isExpanded) Int.MAX_VALUE else minimizedMaxLines,
            overflow = TextOverflow.Ellipsis,
            onTextLayout = { textLayoutResult ->
                if (!isExpanded) {
                    hasOverflow = textLayoutResult.hasVisualOverflow
                }
            }
        )
        if (hasOverflow || isExpanded) {
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = if (isExpanded) "See less" else "See more",
                style = style.copy(fontWeight = FontWeight.SemiBold),
                color = MaterialTheme.colorScheme.primary,
                fontSize = fontSize,
                modifier = Modifier.clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = { isExpanded = !isExpanded }
                )
            )
        }
    }
}
