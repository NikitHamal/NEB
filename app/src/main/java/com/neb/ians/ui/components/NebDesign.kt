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
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType

// ---------------------------------------------------------------------------
// Brand extra colors (mirrors web --md-surface-muted / --md-border-subtle and
// the brand gradient used for the logo + accents).
// ---------------------------------------------------------------------------



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
    if (onClick == null) {
        Box(
            modifier = modifier
                .clip(shape)
                .background(containerColor)
                .then(if (border != null) Modifier.border(border, shape) else Modifier)
        ) { content() }
        return
    }
    val tactile = rememberTactileFeedback()
    val interaction = remember { MutableInteractionSource() }
    val pressed by interaction.collectIsPressedAsState()
    val pressScale by animateFloatAsState(
        targetValue = if (pressed) 0.985f else 1f,
        animationSpec = com.neb.ians.ui.theme.nebFastSpatialSpec(),
        label = "nebCardPress"
    )
    val fill = if (pressed) MaterialTheme.colorScheme.surfaceContainerLow else containerColor
    Box(
        modifier = modifier
            .graphicsLayer { scaleX = pressScale; scaleY = pressScale }
            .clip(shape)
            .background(fill)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .clickable(interactionSource = interaction, indication = null, onClick = {
                tactile.perform(TactileType.LightTap)
                onClick()
            })
    ) { content() }
}

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
            .nebPressable(scale = 0.88f, tactile = TactileType.ButtonTap, onClick = onClick),
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
    showBorder: Boolean = false,
    verificationLevel: Int = 0,
    modifier: Modifier = Modifier,
) {
    // `ring` is kept for call-site compatibility; avatars carry no stroke and no gradient.
    val ringMod = Modifier

    val resolvedUrl = remember(photoUrl) {
        if (photoUrl.isNullOrBlank()) null
        else {
            var url = photoUrl.trim()
            if (url.startsWith("/avatar/") || url.contains("/avatar/")) null
            else {
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
    }

    var isError by remember(resolvedUrl) { mutableStateOf(false) }
    val isNeby = remember(name) { name.equals("Neby", ignoreCase = true) || name.equals("neby", ignoreCase = true) }
    val hasImageBgNeb = !isNeby && !resolvedUrl.isNullOrBlank() && !isError
    val avatarShape: androidx.compose.ui.graphics.Shape =
        if (isNeby) CircleShape else rememberAvatarShape(name)
    val (toneFill, toneInk) = avatarTone(name)

    val context = androidx.compose.ui.platform.LocalContext.current
    val avatarRequest = remember(context, resolvedUrl) {
        resolvedUrl?.let { url ->
            coil.request.ImageRequest.Builder(context)
                .data(url)
                .size(128, 128)
                .crossfade(false)
                .build()
        }
    }

    Box(modifier = modifier.then(ringMod), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(size)
                .clip(avatarShape)
                .background(
                    if (isNeby) Color.Transparent
                    else if (hasImageBgNeb) MaterialTheme.colorScheme.surfaceContainerLowest
                    else toneFill
                ),
            contentAlignment = Alignment.Center
        ) {
            if (isNeby) {
                Box(contentAlignment = Alignment.Center) {
                    com.neb.ians.ui.pixel.NebyPixel(size = size, ambient = false, avatar = true)
                }
            } else if (avatarRequest != null && !isError) {
                AsyncImage(
                    model = avatarRequest,
                    contentDescription = name,
                    modifier = Modifier.size(size),
                    contentScale = ContentScale.Crop,
                    onError = { isError = true }
                )
            } else {
                Text(
                    text = name.trim().take(1).uppercase().ifBlank { "?" },
                    color = toneInk,
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
                    ,
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

/**
 * Role / verification badge, the web's `.role-badge`: the Material Symbols glyph the server names
 * (`authorBadgeInfo.icon`), filled, in the role's ink colour. No disc, no fill, no ring behind it.
 */
@Composable
fun NebBadge(badge: ApiBadgeInfo?, modifier: Modifier = Modifier, size: androidx.compose.ui.unit.Dp = 18.dp) {
    if (badge == null) return
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    Icon(
        painter = painterResource(id = badgeGlyph(badge)),
        contentDescription = badge.label,
        tint = badgeInk(badge.type, dark),
        modifier = modifier.size(size)
    )
}

/** The glyph the web draws, by the Material Symbols name the API sends (falls back by role). */
private fun badgeGlyph(badge: ApiBadgeInfo): Int = when (badge.icon ?: badge.type) {
    "crown", "admin" -> R.drawable.ic_sym_crown
    "smart_toy", "bot" -> R.drawable.ic_sym_smart_toy
    "local_police" -> R.drawable.ic_sym_local_police
    "shield" -> R.drawable.ic_sym_shield
    "shield_with_heart" -> R.drawable.ic_sym_shield_with_heart
    "moderator" -> R.drawable.ic_sym_local_police
    "school", "teacher" -> R.drawable.ic_sym_school
    "account_balance", "institution" -> R.drawable.ic_sym_account_balance
    "travel_explore", "explorer" -> R.drawable.ic_sym_travel_explore
    else -> R.drawable.ic_sym_verified
}

/** `--bd-ink` per role from `m3x-app.css`, with the `--neb-accent-*` values for light and dark. */
private fun badgeInk(type: String, dark: Boolean): Color = when (type) {
    "admin", "explorer" -> if (dark) Color(0xFFE8B457) else Color(0xFF9A6206)
    "bot" -> if (dark) Color(0xFFC9B6FE) else Color(0xFF7C3AED)
    "teacher" -> if (dark) Color(0xFF7CD9A0) else Color(0xFF15803D)
    "institution" -> if (dark) Color(0xFFB4B0FF) else Color(0xFF4F46E5)
    else -> if (dark) Color(0xFFB4C5FF) else Color(0xFF004AC6)
}

// ---------------------------------------------------------------------------
// Section header — title + optional trailing "View all" action.
// ---------------------------------------------------------------------------

@Composable
fun NebEmptyState(
    icon: ImageVector,
    title: String,
    subtitle: String? = null,
    modifier: Modifier = Modifier,
    action: (@Composable () -> Unit)? = null,
    /** The animated pixel art shown above the title; picked from [icon] unless given. Null: the plain icon disc. */
    art: com.neb.ians.ui.pixel.PixelSprite? = com.neb.ians.ui.pixel.PixelStates.forIcon(icon),
) {
    androidx.compose.foundation.layout.Column(
        modifier = modifier.fillMaxWidth().padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        if (art != null) {
            com.neb.ians.ui.pixel.PixelSpriteView(sprite = art, modifier = Modifier.size(96.dp))
        } else {
            Box(
                modifier = Modifier
                    .size(64.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(28.dp))
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
