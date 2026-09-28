@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.layout.ExperimentalLayoutApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.OpenInNew
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiCreatorBlock

/* The ten sections added with the theme work.
 *
 * Every one exists because a storefront could not say something without it: a
 * tutor who cannot publish their fees is a tutor whose page ends in a phone
 * number, and a page that ends in a phone number does not enrol anybody.
 *
 * All of them read their colours from [LocalCreatorColors] rather than
 * `MaterialTheme.colorScheme`, because inside a creator's page the creator's
 * palette is the theme. The `.mkt-*` classes named in the comments are the web
 * rules these mirror, in `css/pages/marketplace/sections.css`. */


/** One benefit per line, which is how the creator types it, how the web renders
 *  it and what the server's `lines` filter reads back. */
private fun featureLines(raw: String): List<String> =
    raw.split('\n').map { it.trim() }.filter { it.isNotEmpty() }

/** How loud a creator-page button is, in the creator's own palette. */
internal enum class CreatorButtonTone { Filled, Outlined, Inverse }

/**
 * A button drawn in the creator's colours.
 *
 * `theme.css` re-points the `--md-*` tokens at the `--creator-*` ones inside
 * `.mkt-page`, so on the web a button on a storefront is already the creator's
 * accent rather than NEBians blue. NebButton reads `MaterialTheme`, which
 * inside a storefront is the wrong palette — a creator who picked terracotta
 * would get one blue button in the middle of their fees. So these sections draw
 * their own, from [LocalCreatorColors].
 *
 * Every link is either an in-page anchor or a real URL, which is the same fork
 * the web resolves in a template filter, so it lives here once rather than in
 * five copies that drift.
 */
@Composable
internal fun CreatorActionButton(
    label: String,
    url: String,
    tone: CreatorButtonTone,
    onJumpTo: (String) -> Unit,
    fallbackAnchor: String = "contact"
) {
    if (label.isBlank()) return
    val colors = LocalCreatorColors.current
    val style = LocalCreatorStyle.current
    val context = LocalContext.current
    val target = url.trim()
    val anchored = target.isBlank() || target.startsWith("#")

    val background = when (tone) {
        CreatorButtonTone.Filled -> colors.accent
        CreatorButtonTone.Inverse -> colors.onAccent
        CreatorButtonTone.Outlined -> Color.Transparent
    }
    val foreground = when (tone) {
        CreatorButtonTone.Filled -> colors.onAccent
        CreatorButtonTone.Inverse -> colors.accent
        CreatorButtonTone.Outlined -> colors.accent
    }
    Row(
        modifier = Modifier
            // 44dp: a tap target on a storefront has to be reachable by a thumb
            // on a bus, which is where most of these pages are read.
            .heightIn(min = 44.dp)
            .clip(style.pillShape)
            .background(background)
            .then(
                if (tone == CreatorButtonTone.Outlined) Modifier.border(1.dp, colors.accent, style.pillShape)
                else Modifier
            )
            .clickable {
                if (anchored) onJumpTo(target.removePrefix("#").ifBlank { fallbackAnchor })
                else openCreatorLink(context, target)
            }
            .padding(horizontal = 18.dp, vertical = 11.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelLarge,
            fontWeight = FontWeight.SemiBold,
            color = foreground,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        if (!anchored) {
            Icon(
                imageVector = Icons.AutoMirrored.Outlined.OpenInNew,
                contentDescription = null,
                tint = foreground,
                modifier = Modifier.size(15.dp)
            )
        }
    }
}


// ── Pricing ─────────────────────────────────────────────────────────────────

/**
 * Fees, side by side.
 *
 * The web lays plans out in an `auto-fit` grid; a phone has room for one plan
 * at a time, so this is a horizontal shelf instead. Both choices come from the
 * same reasoning: a plan card squeezed to a third of a phone's width cannot
 * show the feature list, and the feature list is what sells the plan.
 */
@Composable
internal fun CreatorPricingBlock(block: ApiCreatorBlock, isLast: Boolean, onJumpTo: (String) -> Unit) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.ifBlank { "Fees" },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        LazyRow(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
              item {
                // `.mkt-plan-featured`: the badge is how a creator says "this
                // one", so the badge is also what lifts the card.
                val featured = item.badge.isNotBlank()
                Column(
                    modifier = Modifier
                        .width(248.dp)
                        .clip(style.blockShape)
                        .background(if (featured) colors.soft else colors.surface)
                        .border(
                            width = if (featured) 2.dp else 1.dp,
                            color = if (featured) colors.accent else colors.line,
                            shape = style.blockShape
                        )
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    if (featured) {
                        Surface(shape = style.pillShape, color = colors.accent) {
                            Text(
                                text = item.badge.uppercase(),
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = colors.onAccent,
                                modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp)
                            )
                        }
                    }
                    Text(
                        text = item.name,
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        fontFamily = style.fontFamily,
                        color = colors.ink
                    )
                    if (item.price.isNotBlank()) {
                        // Amount and period on one baseline: "Rs 2,500" reads as
                        // a price, "Rs 2,500 / month" reads as an offer.
                        Row(verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text(
                                text = item.price,
                                style = MaterialTheme.typography.headlineSmall,
                                fontWeight = FontWeight.Bold,
                                color = colors.accent
                            )
                            if (item.period.isNotBlank()) {
                                Text(
                                    text = item.period,
                                    style = MaterialTheme.typography.labelMedium,
                                    color = colors.muted,
                                    modifier = Modifier.padding(bottom = 3.dp)
                                )
                            }
                        }
                    }
                    val features = featureLines(item.features)
                    if (features.isNotEmpty()) {
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            features.forEach { feature ->
                                Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                                    Icon(
                                        imageVector = Icons.Outlined.Check,
                                        contentDescription = null,
                                        tint = colors.accent,
                                        modifier = Modifier
                                            .size(16.dp)
                                            .padding(top = 2.dp)
                                    )
                                    Text(
                                        text = feature,
                                        style = MaterialTheme.typography.bodySmall,
                                        color = colors.ink,
                                        modifier = Modifier.weight(1f)
                                    )
                                }
                            }
                        }
                    }
                    CreatorActionButton(
                        label = item.ctaLabel,
                        url = item.ctaUrl,
                        tone = if (featured) CreatorButtonTone.Filled else CreatorButtonTone.Outlined,
                        onJumpTo = onJumpTo
                    )
                }
              }
            }
        }
    }
}


// ── Video ───────────────────────────────────────────────────────────────────

/**
 * A YouTube or Vimeo link, as a poster you tap.
 *
 * The web frames an iframe; a phone does not need a WebView for this. The
 * player the visitor already has installed is faster, remembers their place and
 * handles full screen properly — so the section shows the real thumbnail and
 * hands the link over on tap. The host allowlist is the same one
 * `video_embed()` uses, and a link from anywhere else is shown as a link rather
 * than dressed up as a video that will not play.
 */
@Composable
internal fun CreatorVideoBlock(block: ApiCreatorBlock, isLast: Boolean) {
    val url = block.mediaUrl.trim()
    if (url.isBlank()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    val context = LocalContext.current
    val youTubeId = youTubeVideoId(url)
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.ifBlank { "Watch" },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .clip(style.blockShape)
                .background(colors.ink)
                .clickable { openCreatorLink(context, url) },
            contentAlignment = Alignment.Center
        ) {
            if (youTubeId != null) {
                // hqdefault exists for every video; maxres does not, and a
                // missing maxres is a blank black box where the poster was.
                AsyncImage(
                    model = "https://i.ytimg.com/vi/$youTubeId/hqdefault.jpg",
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
            }
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(colors.accent),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.PlayArrow,
                    contentDescription = "Play",
                    tint = colors.onAccent,
                    modifier = Modifier.size(30.dp)
                )
            }
        }
    }
}

/** The video id, for the hosts we are willing to show a poster for. */
private fun youTubeVideoId(url: String): String? {
    val patterns = listOf(
        Regex("""youtube\.com/watch\?(?:.*&)?v=([\w-]{6,20})"""),
        Regex("""youtube(?:-nocookie)?\.com/embed/([\w-]{6,20})"""),
        Regex("""youtu\.be/([\w-]{6,20})""")
    )
    for (pattern in patterns) {
        val match = pattern.find(url)
        if (match != null) return match.groupValues[1]
    }
    return null
}


// ── Team ────────────────────────────────────────────────────────────────────

/** The people who teach with you: `.mkt-team` / `.mkt-member`. */
@Composable
internal fun CreatorTeamBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.ifBlank { "Teachers" },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        LazyRow(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                item {
                    Column(
                        modifier = Modifier
                            .width(156.dp)
                            .clip(style.blockShape)
                            .background(colors.surface)
                            .border(1.dp, colors.line, style.blockShape)
                            .padding(14.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(7.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(colors.soft),
                            contentAlignment = Alignment.Center
                        ) {
                            if (item.avatarUrl.isNotBlank()) {
                                AsyncImage(
                                    model = item.avatarUrl,
                                    contentDescription = null,
                                    contentScale = ContentScale.Crop,
                                    modifier = Modifier.fillMaxSize()
                                )
                            } else {
                                Text(
                                    text = item.name.take(1).ifBlank { "?" }.uppercase(),
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = colors.accent
                                )
                            }
                        }
                        Text(
                            text = item.name,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            fontFamily = style.fontFamily,
                            color = colors.ink,
                            textAlign = TextAlign.Center,
                            maxLines = 2,
                            overflow = TextOverflow.Ellipsis
                        )
                        if (item.role.isNotBlank()) {
                            Text(
                                text = item.role,
                                style = MaterialTheme.typography.labelSmall,
                                color = colors.accent,
                                textAlign = TextAlign.Center
                            )
                        }
                        if (item.note.isNotBlank()) {
                            Text(
                                text = item.note,
                                style = MaterialTheme.typography.bodySmall,
                                color = colors.muted,
                                textAlign = TextAlign.Center,
                                maxLines = 3,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }
        }
    }
}


// ── Partners ────────────────────────────────────────────────────────────────

/**
 * Schools, boards and partners: `.mkt-logos`.
 *
 * A wrapping row rather than a shelf, because these are small and a creator
 * with eight of them wants all eight seen at once. A partner with no artwork
 * falls back to their name in a chip, which is what the web does too — a
 * missing logo should not leave a gap the visitor has to interpret.
 */
@Composable
internal fun CreatorLogosBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    val context = LocalContext.current
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.takeIf { it.isNotBlank() },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        FlowRow(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            block.items.forEach { item ->
                val clickable = item.linkUrl.isNotBlank()
                Box(
                    modifier = Modifier
                        .height(56.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(colors.soft)
                        .then(
                            if (clickable) Modifier.clickable { openCreatorLink(context, item.linkUrl) }
                            else Modifier
                        )
                        .padding(horizontal = 14.dp),
                    contentAlignment = Alignment.Center
                ) {
                    if (item.imageUrl.isNotBlank()) {
                        AsyncImage(
                            model = item.imageUrl,
                            contentDescription = item.label.takeIf { it.isNotBlank() },
                            contentScale = ContentScale.Fit,
                            modifier = Modifier
                                .height(34.dp)
                                .width(84.dp)
                        )
                    } else {
                        Text(
                            text = item.label,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Medium,
                            color = colors.ink,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }
    }
}


// ── Milestones ──────────────────────────────────────────────────────────────

/**
 * Milestones, or results by year: `.mkt-timeline`.
 *
 * The rail with a dot per entry is drawn rather than borrowed, because it is
 * the one thing that makes a list of years read as a sequence instead of as
 * five unrelated facts.
 */
@Composable
internal fun CreatorTimelineBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.ifBlank { "Milestones" },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        Column {
            block.items.forEachIndexed { index, item ->
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    // The rail: a dot on the entry's own line and a hairline
                    // running to the next one. The last entry gets no line, so
                    // the sequence ends instead of trailing off.
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.width(12.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .padding(top = 5.dp)
                                .size(10.dp)
                                .clip(CircleShape)
                                .background(colors.accent)
                        )
                        if (index < block.items.lastIndex) {
                            Box(
                                modifier = Modifier
                                    .padding(top = 3.dp)
                                    .width(2.dp)
                                    .height(38.dp)
                                    .background(colors.line)
                            )
                        }
                    }
                    Column(
                        modifier = Modifier
                            .weight(1f)
                            .padding(bottom = if (index < block.items.lastIndex) 14.dp else 0.dp),
                        verticalArrangement = Arrangement.spacedBy(3.dp)
                    ) {
                        if (item.label.isNotBlank()) {
                            Text(
                                text = item.label,
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = colors.accent
                            )
                        }
                        Text(
                            text = item.title,
                            style = MaterialTheme.typography.bodyLarge,
                            fontWeight = FontWeight.SemiBold,
                            fontFamily = style.fontFamily,
                            color = colors.ink
                        )
                        if (item.note.isNotBlank()) {
                            Text(
                                text = item.note,
                                style = MaterialTheme.typography.bodySmall,
                                color = colors.muted
                            )
                        }
                    }
                }
            }
        }
    }
}


// ── How it works ────────────────────────────────────────────────────────────

/**
 * Numbered steps: `.mkt-steps`.
 *
 * The web numbers these with a CSS counter so reordering in the studio never
 * leaves a page reading 1, 2, 2, 4. `forEachIndexed` is the same guarantee: the
 * number is the position, never a field a creator could get wrong.
 */
@Composable
internal fun CreatorStepsBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.ifBlank { "How to join" },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEachIndexed { index, item ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(style.blockShape)
                        .background(colors.surface)
                        .border(1.dp, colors.line, style.blockShape)
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(30.dp)
                            .clip(CircleShape)
                            .background(colors.accent),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "${index + 1}",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            color = colors.onAccent
                        )
                    }
                    Column(
                        modifier = Modifier.weight(1f),
                        verticalArrangement = Arrangement.spacedBy(3.dp)
                    ) {
                        Text(
                            text = item.title,
                            style = MaterialTheme.typography.bodyLarge,
                            fontWeight = FontWeight.SemiBold,
                            fontFamily = style.fontFamily,
                            color = colors.ink
                        )
                        if (item.note.isNotBlank()) {
                            Text(
                                text = item.note,
                                style = MaterialTheme.typography.bodySmall,
                                color = colors.muted
                            )
                        }
                    }
                }
            }
        }
    }
}


// ── Pull quote ──────────────────────────────────────────────────────────────

/**
 * One line, set large: `.mkt-pullquote`.
 *
 * Deliberately the only section with no heading of its own. Its whole job is to
 * be a pause between two dense sections, and a heading above a pull quote turns
 * the pause back into another section.
 */
@Composable
internal fun CreatorQuoteBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.title.isBlank()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    CreatorBlockShell(settings = block.settings, title = null, isLast = isLast) {
        Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            Box(
                modifier = Modifier
                    .width(3.dp)
                    .height(if (block.subtitle.isBlank()) 54.dp else 74.dp)
                    .clip(style.pillShape)
                    .background(colors.accent)
            )
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(
                    text = block.title,
                    style = MaterialTheme.typography.titleLarge,
                    fontStyle = FontStyle.Italic,
                    fontFamily = style.fontFamily,
                    color = colors.ink
                )
                if (block.subtitle.isNotBlank()) {
                    Text(
                        text = "— ${block.subtitle}",
                        style = MaterialTheme.typography.labelMedium,
                        color = colors.muted
                    )
                }
            }
        }
    }
}


// ── Announcement ────────────────────────────────────────────────────────────

/**
 * A thin strip for an admission date or a discount: `.mkt-banner`.
 *
 * Painted in the accent whatever the section tone says, because an
 * announcement that matches the page around it is an announcement nobody
 * reads. The copy and the button stack on a phone — side by side they leave the
 * copy about eleven characters, which is the failure the old studio rows had.
 */
@Composable
internal fun CreatorBannerBlock(block: ApiCreatorBlock, onJumpTo: (String) -> Unit) {
    if (block.title.isBlank()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(style.blockShape)
                .background(colors.accent)
                .padding(horizontal = 16.dp, vertical = 14.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Text(
                text = block.title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                fontFamily = style.fontFamily,
                color = colors.onAccent
            )
            if (block.subtitle.isNotBlank()) {
                Text(
                    text = block.subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = colors.onAccent.copy(alpha = 0.86f)
                )
            }
            CreatorActionButton(
                label = block.ctaLabel,
                url = block.ctaUrl,
                tone = CreatorButtonTone.Inverse,
                onJumpTo = onJumpTo
            )
        }
    }
}


// ── Text and image ──────────────────────────────────────────────────────────

/**
 * A paragraph beside a picture: `.mkt-rich`. The flexible one.
 *
 * Side by side in a browser, stacked here: the web rule itself collapses to a
 * single column under 720px, so stacking is not a phone compromise — it is the
 * same layout at the same width.
 */
@Composable
internal fun CreatorRichTextBlock(block: ApiCreatorBlock, isLast: Boolean, onJumpTo: (String) -> Unit) {
    if (block.body.isBlank() && block.title.isBlank()) return
    val style = LocalCreatorStyle.current
    val colors = LocalCreatorColors.current
    CreatorBlockShell(
        settings = block.settings,
        title = block.title.takeIf { it.isNotBlank() },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        if (block.imageUrl.isNotBlank()) {
            AsyncImage(
                model = block.imageUrl,
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(16f / 10f)
                    .clip(style.blockShape)
                    .background(colors.soft)
            )
        }
        if (block.body.isNotBlank()) {
            Text(
                text = block.body,
                style = MaterialTheme.typography.bodyMedium,
                color = colors.ink
            )
        }
        CreatorActionButton(
            label = block.ctaLabel,
            url = block.ctaUrl,
            tone = CreatorButtonTone.Outlined,
            onJumpTo = onJumpTo
        )
    }
}


// ── Divider ─────────────────────────────────────────────────────────────────

/** Breathing room, and a rule: `.mkt-block-divider`. */
@Composable
internal fun CreatorDividerBlock(block: ApiCreatorBlock) {
    val colors = LocalCreatorColors.current
    // `width = "wide"` on a divider is the creator asking for the rule to run
    // edge to edge, which is the one place a full-bleed line looks deliberate.
    val inset = if (block.settings.width == "wide") 0.dp else 16.dp
    HorizontalDivider(
        color = colors.line,
        thickness = 1.dp,
        modifier = Modifier.padding(horizontal = inset, vertical = 14.dp)
    )
}
