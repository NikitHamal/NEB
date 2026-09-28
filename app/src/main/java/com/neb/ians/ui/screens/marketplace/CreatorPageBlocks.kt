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
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.OpenInNew
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.PushPin
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiCreatorBlock
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.ResourceBannerArt
import com.neb.ians.ui.components.nebBorderSubtle
import com.neb.ians.util.formatTimeAgo

/* The storefront blocks that carry the creator's own material: who they are,
 * the numbers they lead with, what they sell and what they have posted.
 * The dispatch that picks between them lives in CreatorPageScreen.kt, and the
 * remaining supporting blocks in CreatorPageDetailBlocks.kt. */

@Composable
internal fun CreatorHeroBlock(
    page: ApiCreatorPage,
    block: ApiCreatorBlock,
    accent: Color,
    onJumpTo: (String) -> Unit
) {
    val style = LocalCreatorStyle.current
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .padding(top = 12.dp, bottom = 10.dp)
            .clip(style.blockShape)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .border(1.dp, nebBorderSubtle(), style.blockShape)
    ) {
        // The same two layers the web hero stacks, at the same opacities: the
        // generated banner art behind, the creator's own cover over it. `plain`
        // drops both, `cover` drops the art. ResourceBannerArt is the very
        // drawing neb-art.js is generated from, so the picture is identical.
        if (style.heroArt) {
            ResourceBannerArt(
                seed = "${page.slug}|hero",
                subject = page.subjects.firstOrNull().orEmpty().ifBlank { "Study" },
                modifier = Modifier
                    .matchParentSize()
                    .alpha(0.5f)
            )
        }
        // The hero's own Image URL wins over the page cover, so a creator can give
        // the top of their page a different picture from the one their marketplace
        // card uses. Same two fields, same order, as the web hero.
        val heroImage = block.imageUrl.ifBlank { page.coverUrl }
        if (style.heroCover && heroImage.isNotBlank()) {
            AsyncImage(
                model = heroImage,
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .matchParentSize()
                    .alpha(0.55f)
            )
        }

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = style.heroHeight)
                .padding(horizontal = 16.dp)
                .padding(top = if (style.heroHeight > 150.dp) 26.dp else 18.dp, bottom = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Spacer(Modifier.weight(1f))
            Row(verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(
                    modifier = Modifier
                        .size(72.dp)
                        .clip(CircleShape)
                        .background(accent)
                        .border(3.dp, MaterialTheme.colorScheme.surfaceContainerLowest, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    if (page.avatarUrl.isNotBlank()) {
                        AsyncImage(
                            model = page.avatarUrl,
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                    } else {
                        Text(
                            text = page.displayName.take(1).ifBlank { "N" },
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }
                }
                Column(verticalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.weight(1f)) {
                    Text(
                        text = creatorKindLabel(page.kind).uppercase(),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = accent
                    )
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text(
                            text = block.title.ifBlank { page.displayName },
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 2,
                            overflow = TextOverflow.Ellipsis
                        )
                        if (page.verified && style.showVerified) {
                            Icon(
                                imageVector = Icons.Filled.Verified,
                                contentDescription = "Verified",
                                tint = accent,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                }
            }

            val tagline = block.subtitle.ifBlank { page.tagline }
            if (tagline.isNotBlank()) {
                Text(
                    text = tagline,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            if (page.subjects.isNotEmpty() || page.location.isNotBlank()) {
                // `.mkt-hero-meta` wraps, and four subject chips will not sit on
                // one phone-width line, so this wraps too rather than clipping
                // the fourth.
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    page.subjects.take(4).forEach { subject ->
                        Surface(shape = style.pillShape, color = MaterialTheme.colorScheme.surfaceContainer) {
                            Text(
                                text = subject,
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp)
                            )
                        }
                    }
                    if (page.location.isNotBlank()) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(3.dp)) {
                            Icon(
                                imageVector = Icons.Outlined.LocationOn,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(14.dp)
                            )
                            Text(
                                text = page.location,
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }

            // `show_stats` is the creator's answer to "lead with my numbers?".
            // These are the platform's counts, not the ones they typed into a
            // stats block, so they are the same three figures the marketplace
            // listing shows for them.
            if (style.showStats) {
                Row(horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.CenterVertically) {
                    HeroStat(page.courseCount.toString(), "offerings", accent)
                    HeroStat(compactCount(page.viewCount), "views", accent)
                    HeroStat(compactCount(page.followerCount), "followers", accent)
                }
            }

            // The web hero always offers a way on: the creator's own button when
            // they wrote one, "See offerings" when they did not. A creator who
            // labelled a button but left the link empty gets the anchor rather
            // than a button that does nothing.
            val context = LocalContext.current
            val label = block.ctaLabel.ifBlank { "See offerings" }
            val target = block.ctaUrl.trim()
            NebButton(
                text = label,
                onClick = {
                    if (target.isBlank() || target.startsWith("#")) {
                        onJumpTo(target.removePrefix("#").ifBlank { "offerings" })
                    } else {
                        openCreatorLink(context, target)
                    }
                },
                tone = NebButtonTone.Primary,
                size = NebButtonSize.Small,
                icon = if (target.isBlank() || target.startsWith("#")) null else Icons.AutoMirrored.Outlined.OpenInNew
            )
        }
    }
}

@Composable
private fun HeroStat(value: String, label: String, accent: Color) {
    Row(verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = accent
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(bottom = 2.dp)
        )
    }
}

@Composable
internal fun CreatorAboutBlock(page: ApiCreatorPage, block: ApiCreatorBlock, isLast: Boolean) {
    val body = block.body.ifBlank { page.about }
    if (body.isBlank()) return
    CreatorBlockShell(title = block.title.ifBlank { "About" }, isLast = isLast) {
        Text(
            text = body,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface
        )
    }
}

@Composable
internal fun CreatorStatsBlock(page: ApiCreatorPage, block: ApiCreatorBlock, accent: Color, isLast: Boolean) {
    // Whatever figures the creator wrote, in rows of three. A creator who added
    // the block and left it empty gets the page's own numbers rather than an
    // empty band -- but nothing here is invented beyond that.
    val items = block.items.filter { it.value.isNotBlank() || it.label.isNotBlank() }.ifEmpty {
        listOf(
            ApiCreatorBlockItem(label = "Offerings", value = page.courseCount.toString()),
            ApiCreatorBlockItem(label = "Views", value = compactCount(page.viewCount)),
            ApiCreatorBlockItem(label = "Followers", value = compactCount(page.followerCount))
        )
    }
    val style = LocalCreatorStyle.current
    CreatorBlockShell(title = block.title.ifBlank { "Numbers" }, isLast = isLast) {
        Column(verticalArrangement = Arrangement.spacedBy(style.itemGap)) {
            items.chunked(3).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                    row.forEach { item ->
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(style.blockShape)
                                .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                                .padding(12.dp),
                            verticalArrangement = Arrangement.spacedBy(2.dp)
                        ) {
                            Text(
                                text = item.value,
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = accent
                            )
                            Text(
                                text = item.label,
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 2,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                    // a trailing row of one or two keeps the card width of a
                    // full row instead of stretching to fill the band
                    repeat(3 - row.size) { Spacer(Modifier.weight(1f)) }
                }
            }
        }
    }
}

@Composable
internal fun CreatorCoursesBlock(
    block: ApiCreatorBlock,
    paid: List<ApiCreatorCourse>,
    free: List<ApiCreatorCourse>,
    accentHex: String,
    isLast: Boolean,
    onCourseClick: (String) -> Unit
) {
    val style = LocalCreatorStyle.current
    CreatorBlockShell(
        title = block.title.ifBlank { "Courses and classes" },
        subtitle = block.subtitle,
        isLast = isLast
    ) {
        if (paid.isEmpty() && free.isEmpty()) {
            Text(
                text = "Nothing listed yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                if (paid.isNotEmpty()) {
                    CourseShelf(paid, accentHex, style, onCourseClick)
                }
                if (free.isNotEmpty()) {
                    if (paid.isNotEmpty()) {
                        Text(
                            text = "Free",
                            style = MaterialTheme.typography.labelMediumEmphasized,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    CourseShelf(free, accentHex, style, onCourseClick)
                }
            }
        }
    }
}

/**
 * One run of courses: a side-scrolling shelf, or a two-column grid on a `grid`
 * page. `.mkt-course-grid` is `repeat(auto-fill, minmax(230px, 1fr))` on the
 * web, which is two columns at a phone's width -- so a grid storefront gets two
 * columns here and everything else gets the shelf the rest of the app uses.
 */
@Composable
private fun CourseShelf(
    courses: List<ApiCreatorCourse>,
    accentHex: String,
    style: CreatorStyle,
    onCourseClick: (String) -> Unit
) {
    if (style.gridded) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            courses.chunked(2).forEach { pair ->
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                    pair.forEach { course ->
                        Box(modifier = Modifier.weight(1f)) {
                            MarketplaceCourseCard(
                                course = course,
                                onClick = { onCourseClick(course.id) },
                                accentHex = accentHex,
                                fillCell = true,
                                shape = style.blockShape
                            )
                        }
                    }
                    repeat(2 - pair.size) { Spacer(Modifier.weight(1f)) }
                }
            }
        }
    } else {
        LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            items(courses, key = { it.id }) { course ->
                MarketplaceCourseCard(
                    course = course,
                    onClick = { onCourseClick(course.id) },
                    accentHex = accentHex,
                    shape = style.blockShape
                )
            }
        }
    }
}

@Composable
internal fun CreatorResourcesBlock(
    block: ApiCreatorBlock,
    page: ApiCreatorPage,
    accent: Color,
    isLast: Boolean,
    onResourceClick: (String) -> Unit
) {
    val style = LocalCreatorStyle.current
    CreatorBlockShell(title = block.title.ifBlank { "Resources" }, subtitle = block.subtitle, isLast = isLast) {
        if (page.resources.isEmpty()) {
            Text(
                text = "No library resources yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                page.resources.take(8).forEach { resource ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(style.blockShape)
                            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                            .clickable { onResourceClick(resource.id) }
                            .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                            Text(
                                text = resource.title,
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.SemiBold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = listOf(resource.subject.ifBlank { "General" }, resource.gradeLevel)
                                    .filter { it.isNotBlank() }
                                    .joinToString(" · "),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        // `.mkt-resource-foot`: price or Free, then the views.
                        // A free note says so rather than saying nothing, which
                        // is the difference between "it costs nothing" and "we
                        // forgot to say".
                        if (resource.isPaid) {
                            Surface(shape = style.pillShape, color = accent) {
                                Text(
                                    text = "Rs. ${resource.price}",
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.surface,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }
                        } else {
                            Surface(shape = style.pillShape, color = MaterialTheme.colorScheme.surfaceContainer) {
                                Text(
                                    text = "Free",
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.SemiBold,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }
                        }
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(3.dp)) {
                            Icon(
                                imageVector = Icons.Outlined.Visibility,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(14.dp)
                            )
                            Text(
                                text = compactCount(resource.viewCount),
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

/**
 * The documents block: the same library notes as `resources`, listed as plain
 * rows to open rather than as cards to browse. The web renders it with
 * `.mkt-link`, the same row the links block uses, so this does too.
 */
@Composable
internal fun CreatorDocumentsBlock(
    block: ApiCreatorBlock,
    page: ApiCreatorPage,
    accent: Color,
    isLast: Boolean,
    onResourceClick: (String) -> Unit
) {
    val style = LocalCreatorStyle.current
    CreatorBlockShell(title = block.title.ifBlank { "Documents" }, subtitle = block.subtitle, isLast = isLast) {
        if (page.resources.isEmpty()) {
            Text(
                text = "No documents yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                page.resources.take(10).forEach { resource ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(style.blockShape)
                            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                            .clickable { onResourceClick(resource.id) }
                            .padding(horizontal = 12.dp, vertical = 11.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Description,
                            contentDescription = null,
                            tint = accent,
                            modifier = Modifier.size(18.dp)
                        )
                        Text(
                            text = resource.title,
                            style = MaterialTheme.typography.bodyMedium,
                            modifier = Modifier.weight(1f),
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Icon(
                            imageVector = Icons.AutoMirrored.Outlined.OpenInNew,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(15.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
internal fun CreatorPostsBlock(block: ApiCreatorBlock, page: ApiCreatorPage, accent: Color, isLast: Boolean) {
    val style = LocalCreatorStyle.current
    val context = LocalContext.current
    CreatorBlockShell(title = block.title.ifBlank { "Updates" }, subtitle = block.subtitle, isLast = isLast) {
        if (page.posts.isEmpty()) {
            Text(
                text = "No updates posted yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                page.posts.forEach { post ->
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(style.blockShape)
                            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                            .padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        if (post.pinned) {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                Icon(
                                    imageVector = Icons.Outlined.PushPin,
                                    contentDescription = null,
                                    tint = accent,
                                    modifier = Modifier.size(14.dp)
                                )
                                Text(
                                    text = "Pinned",
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = accent
                                )
                            }
                        }
                        if (post.title.isNotBlank()) {
                            Text(
                                text = post.title,
                                style = MaterialTheme.typography.titleSmall,
                                fontWeight = FontWeight.SemiBold
                            )
                        }
                        if (post.body.isNotBlank()) {
                            Text(
                                text = post.body,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        if (post.mediaUrl.isNotBlank()) {
                            AsyncImage(
                                model = post.mediaUrl,
                                contentDescription = null,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(160.dp)
                                    .clip(style.blockShape)
                            )
                        }
                        // a post that links somewhere has to be able to go
                        // there, the way `.mkt-post-link` does
                        if (post.linkUrl.isNotBlank()) {
                            NebButton(
                                text = "Open link",
                                onClick = { openCreatorLink(context, post.linkUrl) },
                                tone = NebButtonTone.Text,
                                size = NebButtonSize.Small,
                                icon = Icons.AutoMirrored.Outlined.OpenInNew
                            )
                        }
                        Text(
                            text = formatTimeAgo(post.createdAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}
