package com.neb.ians.ui.theme

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiSiteTheme
import com.neb.ians.data.api.ApiThemeColors
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.pixel.PixelMotifs
import com.neb.ians.ui.pixel.PixelSpriteView

/**
 * The live festival theme, as the UI sees it. The app's chrome stays in its mono house style;
 * the season shows in two quiet places only: a small pixel motif beside the wordmark and the
 * season card at the top of Home, both in the festival's own colours.
 */
data class SiteThemeState(
    val theme: ApiSiteTheme? = null,
    val cardOpen: Boolean = false,
    val onDismissCard: () -> Unit = {},
) {
    val festive: Boolean get() = theme?.festive == true && theme.light != null
}

val LocalSiteTheme = staticCompositionLocalOf { SiteThemeState() }

private fun hex(s: String): Color = runCatching { Color(android.graphics.Color.parseColor(s)) }.getOrDefault(Color.Unspecified)

/** The season's colours for the current light or dark scheme. */
@Composable
fun seasonColors(): ApiThemeColors? {
    val state = LocalSiteTheme.current
    if (!state.festive) return null
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    return if (dark) state.theme?.dark ?: state.theme?.light else state.theme?.light
}

/** The festival's pixel motif, or nothing on an ordinary day. */
@Composable
fun SeasonMotif(size: Dp = 22.dp, modifier: Modifier = Modifier) {
    val state = LocalSiteTheme.current
    val colors = seasonColors() ?: return
    val sprite = PixelMotifs.sprite(state.theme?.motif ?: return, hex(colors.primary).toArgb()) ?: return
    PixelSpriteView(sprite = sprite, modifier = modifier.size(size))
}

/** The season card for the top of Home. [onAction] receives the card's link. */
@Composable
fun SeasonCard(onAction: (String) -> Unit, modifier: Modifier = Modifier) {
    val state = LocalSiteTheme.current
    if (!state.festive || !state.cardOpen) return
    val theme = state.theme ?: return
    val c = seasonColors() ?: return
    val container = hex(c.primaryContainer)
    val onContainer = hex(c.onPrimaryContainer)
    val primary = hex(c.primary)
    val onPrimary = hex(c.onPrimary)
    Column(
        modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(container)
            .padding(start = 18.dp, end = 8.dp, top = 16.dp, bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Row(verticalAlignment = Alignment.Top) {
            Box(
                Modifier.size(52.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface),
                contentAlignment = Alignment.Center
            ) { SeasonMotif(size = 36.dp) }
            Column(Modifier.weight(1f).padding(start = 14.dp, end = 4.dp)) {
                val g = theme.greeting
                if (g != null && g.ne.isNotBlank()) {
                    Text(g.ne, color = onContainer, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                    if (g.en.isNotBlank()) Text(g.en, color = onContainer.copy(alpha = 0.72f), style = MaterialTheme.typography.labelLarge)
                } else {
                    Text(theme.name, color = onContainer, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                }
                theme.card?.message?.takeIf { it.isNotBlank() }?.let {
                    Text(it, color = onContainer.copy(alpha = 0.86f), style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(top = 6.dp))
                }
            }
            NebIconButton(Icons.Rounded.Close, "Close", state.onDismissCard, tint = onContainer, size = 36.dp)
        }
        theme.card?.cta?.takeIf { it.label.isNotBlank() }?.let { cta ->
            Box(
                Modifier
                    .padding(start = 66.dp)
                    .clip(CircleShape)
                    .background(primary)
                    .nebPressable(onClick = { onAction(cta.url) })
                    .padding(horizontal = 18.dp, vertical = 10.dp)
            ) { Text(cta.label, color = onPrimary, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold) }
        }
    }
}
