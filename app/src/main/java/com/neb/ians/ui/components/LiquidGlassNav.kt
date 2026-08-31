package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.R

// ---------------------------------------------------------------------------
// NEBians "N" logo as a Compose drawable.
// ---------------------------------------------------------------------------

@Composable
fun NebLogo(modifier: Modifier = Modifier, size: Dp = 32.dp) {
    androidx.compose.foundation.Image(
        painter = painterResource(id = R.drawable.n_logo),
        contentDescription = "NEBians",
        modifier = modifier.size(size)
    )
}

// ---------------------------------------------------------------------------
// Top app bar — mirrors the web .md-topbar (brand + actions).
// ---------------------------------------------------------------------------

@Composable
fun NebTopBar(
    modifier: Modifier = Modifier,
    showBrand: Boolean = true,
    title: String? = null,
    titleFontWeight: FontWeight = FontWeight.Bold,
    onBack: (() -> Unit)? = null,
    onSearch: (() -> Unit)? = null,
    isAuthenticated: Boolean = false,
    photoUrl: String? = null,
    username: String = "",
    unread: Int = 0,
    onProfile: (() -> Unit)? = null,
    actions: (@Composable () -> Unit)? = null,
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surface)
            .statusBarsPadding()
            .padding(horizontal = 12.dp, vertical = 8.dp)
            .height(48.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (onBack != null) {
            NebIconButton(
                icon = Icons.AutoMirrored.Outlined.ArrowBack,
                contentDescription = "Back",
                onClick = onBack
            )
            Spacer(Modifier.width(4.dp))
        }
        if (showBrand) {
            NebLogo(size = 30.dp)
            Spacer(Modifier.width(8.dp))
            Text(
                "NEBians",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface
            )
            Spacer(Modifier.weight(1f))
        } else if (title != null) {
            Text(
                title,
                modifier = Modifier.weight(1f),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = titleFontWeight,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )
            Spacer(Modifier.width(8.dp))
        } else {
            Spacer(Modifier.weight(1f))
        }
        if (actions != null) {
            actions()
        }
        if (onSearch != null) {
            NebIconButton(Icons.Outlined.Search, "Search", onSearch)
        }
        if (isAuthenticated && onProfile != null) {
            Box {
                NebAvatar(photoUrl = photoUrl, name = username, size = 34.dp, ring = true,
                    modifier = Modifier.clickable(onClick = onProfile))
                if (unread > 0) {
                    UnreadCountBadge(
                        count = unread,
                        modifier = Modifier
                            .align(Alignment.TopEnd)
                            .padding(top = 1.dp, end = 1.dp)
                    )
                }
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Liquid-glass floating bottom navigation (3 items, like the web nav pill).
// ---------------------------------------------------------------------------

data class NebNavItem(
    val route: String,
    val label: String,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector,
)

@Composable
fun LiquidGlassBottomNav(
    items: List<NebNavItem>,
    currentRoute: String?,
    onSelect: (NebNavItem) -> Unit,
    modifier: Modifier = Modifier,
    photoUrl: String? = null,
    username: String = "",
    onProfileClick: (() -> Unit)? = null,
) {
    val isDark = MaterialTheme.colorScheme.surface.luminanceIsDark()
    val glassBase = MaterialTheme.colorScheme.surfaceContainerLowest
    val glassBrush = Brush.verticalGradient(
        listOf(
            glassBase.copy(alpha = if (isDark) 0.92f else 0.88f),
            glassBase.copy(alpha = if (isDark) 0.80f else 0.74f),
        )
    )
    val borderColor = if (isDark) Color.White.copy(alpha = 0.10f) else Color.White.copy(alpha = 0.55f)

    Box(
        modifier = modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 14.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(
                modifier = Modifier
                    .shadow(18.dp, CircleShape, clip = false, ambientColor = Color.Black.copy(alpha = 0.18f), spotColor = Color.Black.copy(alpha = 0.22f))
                    .clip(CircleShape)
                    .background(glassBrush)
                    .border(1.dp, borderColor, CircleShape)
                    .padding(horizontal = 8.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                items.forEach { item ->
                    val selected = currentRoute == item.route
                    GlassNavItem(item = item, selected = selected, onClick = { onSelect(item) })
                }
            }

            if (onProfileClick != null) {
                Box(
                    modifier = Modifier
                        .shadow(18.dp, CircleShape, clip = false, ambientColor = Color.Black.copy(alpha = 0.18f), spotColor = Color.Black.copy(alpha = 0.22f))
                        .clip(CircleShape)
                        .background(glassBrush)
                        .border(1.dp, borderColor, CircleShape)
                        .clickable(
                            interactionSource = remember { MutableInteractionSource() },
                            indication = null,
                            onClick = onProfileClick
                        )
                        .padding(6.dp),
                    contentAlignment = Alignment.Center
                ) {
                    NebAvatar(
                        photoUrl = photoUrl,
                        name = username.ifBlank { "User" },
                        size = 38.dp,
                        ring = false
                    )
                }
            }
        }
    }
}

@Composable
private fun GlassNavItem(item: NebNavItem, selected: Boolean, onClick: () -> Unit) {
    val indicator by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent,
        animationSpec = tween(220), label = "indicator"
    )
    val contentColor by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
        animationSpec = tween(220), label = "navContent"
    )
    val hPad by animateDpAsState(if (selected) 18.dp else 16.dp, tween(220), label = "navPad")
    Row(
        modifier = Modifier
            .clip(CircleShape)
            .background(indicator)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            )
            .padding(horizontal = hPad, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(
            if (selected) item.selectedIcon else item.unselectedIcon,
            contentDescription = item.label,
            tint = contentColor,
            modifier = Modifier.size(24.dp)
        )
        if (selected) {
            Text(item.label, color = contentColor, fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
        }
    }
}

private fun Color.luminanceIsDark(): Boolean {
    val l = 0.299f * red + 0.587f * green + 0.114f * blue
    return l < 0.5f
}
