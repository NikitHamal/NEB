@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.OpenInNew
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
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
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
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
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .padding(top = 12.dp, bottom = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(132.dp)
                .clip(WebPanelShape)
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
        ) {
            when {
                page.coverUrl.isNotBlank() -> AsyncImage(
                    model = page.coverUrl,
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )

                else -> Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(accent.copy(alpha = 0.20f))
                )
            }
        }

        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(
                modifier = Modifier
                    .size(72.dp)
                    .clip(CircleShape)
                    .background(accent),
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
                        color = MaterialTheme.colorScheme.surface
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
                    if (page.verified) {
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
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                page.subjects.take(3).forEach { subject ->
                    Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.surfaceContainer) {
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

        if (block.ctaLabel.isNotBlank()) {
            val context = LocalContext.current
            val target = block.ctaUrl.ifBlank { "#offerings" }
            NebButton(
                text = block.ctaLabel,
                onClick = {
                    if (target.startsWith("#")) {
                        // an in-page jump: the offerings sit further down this list
                        onJumpTo("offerings")
                    } else {
                        openCreatorLink(context, target)
                    }
                },
                tone = NebButtonTone.Primary,
                size = NebButtonSize.Small,
                icon = Icons.Outlined.OpenInNew
            )
        }
    }
}

@Composable
internal fun CreatorAboutBlock(page: ApiCreatorPage, block: ApiCreatorBlock) {
    val body = block.body.ifBlank { page.about }
    if (body.isBlank()) return
    CreatorBlockShell(title = block.title.ifBlank { "About" }) {
        Text(
            text = body,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface
        )
    }
}

@Composable
internal fun CreatorStatsBlock(page: ApiCreatorPage, block: ApiCreatorBlock, accent: Color) {
    val items = block.items.ifEmpty {
        listOf(
            ApiCreatorBlockItem(label = "Offerings", value = page.courseCount.toString()),
            ApiCreatorBlockItem(label = "Views", value = compactCount(page.viewCount)),
            ApiCreatorBlockItem(label = "Resources", value = page.resources.size.toString())
        )
    }
    CreatorBlockShell(title = block.title.ifBlank { "Numbers" }) {
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            items.take(3).forEach { item ->
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clip(WebCardShape)
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
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
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
    accent: Color,
    onCourseClick: (String) -> Unit
) {
    CreatorBlockShell(title = block.title.ifBlank { "Courses and classes" }, subtitle = block.subtitle) {
        if (paid.isEmpty() && free.isEmpty()) {
            Text(
                text = "Nothing listed yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                if (paid.isNotEmpty()) {
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(paid, key = { it.id }) { course ->
                            MarketplaceCourseCard(
                                course = course,
                                onClick = { onCourseClick(course.id) },
                                accentHex = "#1F2937"
                            )
                        }
                    }
                }
                if (free.isNotEmpty()) {
                    if (paid.isNotEmpty()) {
                        Text(
                            text = "Free",
                            style = MaterialTheme.typography.labelMediumEmphasized,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(free, key = { it.id }) { course ->
                            MarketplaceCourseCard(
                                course = course,
                                onClick = { onCourseClick(course.id) },
                                accentHex = "#1F2937"
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
internal fun CreatorResourcesBlock(
    block: ApiCreatorBlock,
    page: ApiCreatorPage,
    accent: Color,
    onResourceClick: (String) -> Unit
) {
    CreatorBlockShell(title = block.title.ifBlank { "Resources" }, subtitle = block.subtitle) {
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
                            .clip(WebCardShape)
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
                        if (resource.isPaid) {
                            Surface(shape = WebPillShape, color = accent) {
                                Text(
                                    text = "Rs. ${resource.price}",
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.surface,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
internal fun CreatorPostsBlock(block: ApiCreatorBlock, page: ApiCreatorPage, accent: Color) {
    CreatorBlockShell(title = block.title.ifBlank { "Updates" }, subtitle = block.subtitle) {
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
                            .clip(WebCardShape)
                            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                            .padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        if (post.pinned) {
                            Text(
                                text = "PINNED",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = accent
                            )
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
                                    .clip(WebCardShape)
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
