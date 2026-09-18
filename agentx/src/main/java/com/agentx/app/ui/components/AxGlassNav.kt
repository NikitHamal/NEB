package com.agentx.app.ui.components

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
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class AxNavItem(
    val route: String,
    val label: String,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector
)

@Composable
fun AxGlassBottomNav(
    items: List<AxNavItem>,
    currentRoute: String?,
    onSelect: (AxNavItem) -> Unit,
    modifier: Modifier = Modifier
) {
    val isDark = MaterialTheme.colorScheme.surface.axLuminanceIsDark()
    val glassBase = MaterialTheme.colorScheme.surfaceContainerLowest
    val glassBrush = Brush.verticalGradient(
        listOf(
            glassBase.copy(alpha = if (isDark) 0.92f else 0.88f),
            glassBase.copy(alpha = if (isDark) 0.80f else 0.74f)
        )
    )
    val borderColor = if (isDark) Color.White.copy(alpha = 0.10f) else Color.White.copy(alpha = 0.55f)
    val navHeight = 56.dp

    Box(
        modifier = modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 14.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            modifier = Modifier
                .height(navHeight)
                .shadow(18.dp, CircleShape, clip = false, ambientColor = Color.Black.copy(alpha = 0.18f), spotColor = Color.Black.copy(alpha = 0.22f))
                .clip(CircleShape)
                .background(glassBrush)
                .border(1.dp, borderColor, CircleShape)
                .padding(horizontal = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            items.forEach { item ->
                val selected = currentRoute == item.route
                AxGlassNavItem(item = item, selected = selected, onClick = { onSelect(item) })
            }
        }
    }
}

@Composable
private fun AxGlassNavItem(item: AxNavItem, selected: Boolean, onClick: () -> Unit) {
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

internal fun Color.axLuminanceIsDark(): Boolean {
    val l = 0.299f * red + 0.587f * green + 0.114f * blue
    return l < 0.5f
}
