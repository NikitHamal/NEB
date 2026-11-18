package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.matchParentSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.Avatar

/** One icon on the profile bar. */
class ProfileBarAction(val icon: ImageVector, val label: String, val onClick: () -> Unit)

/**
 * The profile's one fixed bar (Profile v3). Over the cover it is only a row of tonal buttons with a soft page-colour
 * scrim behind the status bar, so the clock and battery stay readable on any cover. As the page scrolls the bar
 * fills with the page colour, a hairline appears and the person's avatar and name take the middle.
 * [progress] is read in the draw phase only, so scrolling never recomposes this bar.
 */
@Composable
fun ProfileTopBar(
    progress: () -> Float,
    name: String,
    photoUrl: String?,
    onBack: () -> Unit,
    actions: List<ProfileBarAction>,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    Box(modifier.fillMaxWidth()) {
        Box(
            Modifier.matchParentSize().graphicsLayer { alpha = 1f - progress() }
                .background(Brush.verticalGradient(listOf(scheme.surface.copy(alpha = 0.78f), Color.Transparent)))
        )
        Box(Modifier.matchParentSize().graphicsLayer { alpha = progress() }.background(scheme.surface))
        Box(
            Modifier.align(Alignment.BottomCenter).fillMaxWidth().height(1.dp)
                .graphicsLayer { alpha = progress() }.background(scheme.outlineVariant)
        )
        Row(
            Modifier.fillMaxWidth().statusBarsPadding().height(56.dp).padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            BarButton(Icons.AutoMirrored.Filled.ArrowBack, "Back", progress, onBack)
            Row(
                Modifier.weight(1f).padding(start = 4.dp).graphicsLayer {
                    val p = progress()
                    alpha = p
                    translationY = (1f - p) * 10.dp.toPx()
                },
                verticalAlignment = Alignment.CenterVertically
            ) {
                Avatar(name = name, imageUrl = photoUrl, size = 32.dp)
                Box(Modifier.width(10.dp))
                Text(
                    name, maxLines = 1, overflow = TextOverflow.Ellipsis,
                    style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold,
                    color = scheme.onSurface
                )
            }
            actions.forEach { BarButton(it.icon, it.label, progress, it.onClick) }
        }
    }
}

@Composable
private fun BarButton(icon: ImageVector, label: String, progress: () -> Float, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Box(
        Modifier.size(44.dp).clip(RoundedCornerShape(16.dp))
            .clickable(role = Role.Button, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Box(
            Modifier.size(40.dp).clip(RoundedCornerShape(14.dp))
                .graphicsLayer { alpha = 1f - progress() }.background(scheme.surface.copy(alpha = 0.8f))
        )
        Icon(icon, contentDescription = label, tint = scheme.onSurface, modifier = Modifier.size(22.dp))
    }
}
