package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiCreatorStyle

/**
 * A creator's chosen look, resolved once for the whole page.
 *
 * The vocabulary is the server's — `sanitize_style()` in
 * `api/creator_pages_sanitize.py` decides which values exist — and the numbers
 * here are the app-scale reading of the same CSS the web storefront uses:
 *
 * | style key         | web                                             | here                      |
 * |-------------------|-------------------------------------------------|---------------------------|
 * | `radius`          | `--mkt-block-radius`: 6px / 20px / 2px          | [blockShape]              |
 * | `density`         | `.mkt-block` padding 26px → 18px                | [blockPadding], [itemGap] |
 * | `hero`            | `.mkt-hero-plain` hides the art and the cover   | [heroArt], [heroCover]    |
 * | `gallery_columns` | `--mkt-gallery-cols`                            | [galleryColumns]          |
 * | `layout`          | `.mkt-layout-spotlight` / `-grid` overrides     | [heroHeight], [gridded]   |
 * | `show_*`          | -                                               | [showStats] and friends   |
 *
 * Phone widths are narrower than a browser's, so the paddings are scaled rather
 * than copied: what has to match is the *relationship* between a creator's
 * choice and what they see, not the pixel count.
 */
internal data class CreatorStyle(
    val blockShape: Shape,
    val pillShape: Shape,
    val blockPadding: Dp,
    val itemGap: Dp,
    val heroArt: Boolean,
    val heroCover: Boolean,
    val heroHeight: Dp,
    val galleryColumns: Int,
    val gridded: Boolean,
    val dividers: Boolean,
    val showStats: Boolean,
    val showContact: Boolean,
    val showVerified: Boolean,
)

@Composable
internal fun rememberCreatorStyle(page: ApiCreatorPage): CreatorStyle =
    remember(page.style, page.layout) { resolveCreatorStyle(page.style, page.layout) }

internal fun resolveCreatorStyle(style: ApiCreatorStyle, layout: String): CreatorStyle {
    val corner = when (style.radius) {
        "soft" -> 6.dp
        "sharp" -> 2.dp
        else -> 20.dp
    }
    val compact = style.density == "compact"
    // `grid` drops the rules between sections on web and lays the shelves out as
    // a grid; `spotlight` gives the hero more room. `editorial` and `classic`
    // are the default reading.
    val grid = layout == "grid"
    return CreatorStyle(
        blockShape = RoundedCornerShape(corner),
        pillShape = RoundedCornerShape(999.dp),
        blockPadding = if (compact) 9.dp else 14.dp,
        itemGap = if (compact) 7.dp else 10.dp,
        heroArt = style.hero == "art",
        heroCover = style.hero != "plain",
        heroHeight = if (layout == "spotlight") 172.dp else 132.dp,
        galleryColumns = style.galleryColumns.coerceIn(2, 4),
        gridded = grid,
        dividers = !grid,
        showStats = style.showStats,
        showContact = style.showContact,
        showVerified = style.showVerified,
    )
}


/**
 * The style the blocks below read.
 *
 * Every block is a leaf of one page, and on the web every block inherits the
 * same handful of CSS custom properties from `.mkt-page`. A composition local is
 * the same arrangement: [CreatorPageScreen] provides the creator's resolved
 * style once and each block reads what it needs, instead of fifteen composables
 * passing a style parameter down to each other.
 */
internal val LocalCreatorStyle = staticCompositionLocalOf {
    resolveCreatorStyle(ApiCreatorStyle(), "editorial")
}
