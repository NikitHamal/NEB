package com.neb.ians.ui.theme

import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.draw.drawBehind
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
    val motif = theme.motif?.let { PixelMotifs.sprite(it, hex(c.primary).toArgb()) }
    val greet = theme.neby?.greet?.let { com.neb.ians.ui.pixel.NebyState.fromName(it) } ?: com.neb.ians.ui.pixel.NebyState.Wave
    val reduced = com.neb.ians.ui.theme.nebAnimationsReduced()
    val clock by androidx.compose.runtime.produceState(0f, reduced) {
        if (!reduced) { val s0 = androidx.compose.runtime.withFrameNanos { it }; while (true) androidx.compose.runtime.withFrameNanos { value = (it - s0) / 1e9f } }
    }
    val bitmap = remember(motif) { motif?.let { m -> android.graphics.Bitmap.createBitmap(m.width, m.height, android.graphics.Bitmap.Config.ARGB_8888).apply { setPixels(m.frames[0], 0, m.width, 0, 0, m.width, m.height) }.asImageBitmap() } }
    Box(
        modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(androidx.compose.ui.graphics.Brush.linearGradient(listOf(container, primary.copy(alpha = 0.22f).compositeOver(container))))
            .drawBehind {
                // the festival's motif drifting slowly across the card, a few small and faint
                val b = bitmap ?: return@drawBehind
                for (i in 0 until 5) {
                    val sp = 0.035f + i * 0.011f
                    val x = ((i * 0.23f + clock * sp) % 1.2f - 0.1f) * size.width
                    val y = size.height * (0.15f + 0.7f * ((i * 0.37f) % 1f)) + kotlin.math.sin(clock * 1.3f + i) * 6.dp.toPx()
                    val px = (18 + i * 4).dp.toPx()
                    drawImage(b, dstOffset = androidx.compose.ui.unit.IntOffset(x.toInt(), y.toInt()), dstSize = androidx.compose.ui.unit.IntSize(px.toInt(), px.toInt()), alpha = 0.22f, filterQuality = androidx.compose.ui.graphics.FilterQuality.None)
                }
            }
            .padding(start = 8.dp, end = 6.dp, top = 8.dp, bottom = 8.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            com.neb.ians.ui.pixel.NebyPixel(state = com.neb.ians.ui.pixel.NebyState.Idle, intro = greet, size = 76.dp, interactive = true)
            Column(Modifier.weight(1f).padding(start = 6.dp, end = 4.dp)) {
                val g = theme.greeting
                if (g != null && g.ne.isNotBlank()) {
                    Text(g.ne, color = onContainer, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    if (g.en.isNotBlank()) Text(g.en, color = onContainer.copy(alpha = 0.75f), style = MaterialTheme.typography.labelLarge)
                } else {
                    Text(theme.name, color = onContainer, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                }
            }
            NebIconButton(Icons.Rounded.Close, "Close", state.onDismissCard, tint = onContainer, size = 36.dp)
        }
    }
}
