package com.neb.ians.ui.screens.marketplace

import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import com.neb.ians.data.api.ApiCreatorTheme
import com.neb.ians.data.api.ApiCreatorThemeColors

/**
 * A creator's colours on the app side.
 *
 * Every value here is parsed from hex the *server* resolved. The palette table
 * lives once, in `api/creator_themes.py`, and both renderers are told the
 * answer rather than working it out — otherwise the day somebody nudged one hex
 * in Python would be the day the same storefront looked different on a phone.
 *
 * These are the Compose reading of the eight CSS custom properties `.mkt-page`
 * carries on the web:
 *
 * | CSS                  | here        | used for                              |
 * |----------------------|-------------|---------------------------------------|
 * | `--creator-accent`   | [accent]    | buttons, prices, the active rule      |
 * | `--creator-on-accent`| [onAccent]  | text on top of the accent             |
 * | `--creator-bg`       | [background]| the page behind the sections          |
 * | `--creator-surface`  | [surface]   | a section's own card                  |
 * | `--creator-ink`      | [ink]       | headings and body text                |
 * | `--creator-muted`    | [muted]     | subtitles, captions, metadata         |
 * | `--creator-line`     | [line]      | rules and card borders                |
 * | `--creator-soft`     | [soft]      | tinted panels, chips, item cards      |
 */
@Immutable
internal data class CreatorColors(
    val accent: Color,
    val onAccent: Color,
    val background: Color,
    val surface: Color,
    val ink: Color,
    val muted: Color,
    val line: Color,
    val soft: Color,
) {
    /** The wash behind a `tone = "soft"` section, and behind tinted item cards. */
    val softBrush: Brush get() = Brush.verticalGradient(listOf(soft, soft))

    /** Readable text on [soft] — the palette's soft tints are light in the light
     *  ramp and deep in the dark one, so ink is right in both. */
    val onSoft: Color get() = ink
}

private fun parse(hex: String, fallback: Color): Color =
    runCatching { Color(android.graphics.Color.parseColor(hex.trim())) }.getOrDefault(fallback)

internal fun resolveCreatorColors(colors: ApiCreatorThemeColors): CreatorColors = CreatorColors(
    accent = parse(colors.accent, Color(0xFF004BD4)),
    onAccent = parse(colors.onAccent, Color.White),
    background = parse(colors.bg, Color(0xFFFFFFFF)),
    surface = parse(colors.surface, Color(0xFFFFFFFF)),
    ink = parse(colors.ink, Color(0xFF0B1020)),
    muted = parse(colors.muted, Color(0xFF535E78)),
    line = parse(colors.line, Color(0xFFE2E7F2)),
    soft = parse(colors.soft, Color(0xFFE8EEFF)),
)

/**
 * The creator's chosen type.
 *
 * Deliberately all system families: a storefront must never wait on a webfont
 * to become readable, and the same rule is why `theme.css` uses system stacks
 * for `.mkt-font-*`. What carries across is the *character* of the choice —
 * a serif page reads as a serif page on both surfaces.
 */
internal fun creatorFontFamily(font: String): FontFamily = when (font) {
    "serif" -> FontFamily.Serif
    "mono" -> FontFamily.Monospace
    // `display` and `rounded` have no distinct system family on Android; the
    // sans stack is the honest answer rather than a wrong one.
    else -> FontFamily.Default
}

@Composable
internal fun rememberCreatorColors(theme: ApiCreatorTheme): CreatorColors =
    remember(theme.colors) { resolveCreatorColors(theme.colors) }

/**
 * The colours the blocks below read.
 *
 * Same arrangement as [LocalCreatorStyle], and for the same reason: on the web
 * every block inherits these from `.mkt-page` rather than being handed them,
 * and fifteen composables passing a colour parameter to each other is how one
 * of them ends up missing it.
 */
internal val LocalCreatorColors = staticCompositionLocalOf {
    resolveCreatorColors(ApiCreatorThemeColors())
}
