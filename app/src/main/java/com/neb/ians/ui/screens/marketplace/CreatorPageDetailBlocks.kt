@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.OpenInNew
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiCreatorBlock
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.getMaterialIcon

/* The supporting storefront blocks: showcase, gallery, testimonials, FAQ,
 * schedule, links, contact and the closing call to action. Dispatched from
 * CreatorPageScreen.kt alongside CreatorPageBlocks.kt. */

@Composable
internal fun CreatorShowcaseBlock(block: ApiCreatorBlock, accent: Color, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    val context = LocalContext.current
    CreatorBlockShell(title = block.title.ifBlank { "Showcase" }, subtitle = block.subtitle, isLast = isLast) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                // `.mkt-showcase-item` is an <a> when the creator gave it a
                // link and a plain <div> otherwise; a card that does nothing
                // should not look like one that does, so only the linked ones
                // take a click.
                val link = item.linkUrl.trim()
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(style.blockShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .then(
                            if (link.isNotBlank()) Modifier.clickable { openCreatorLink(context, link) }
                            else Modifier
                        )
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (item.imageUrl.isNotBlank()) {
                        AsyncImage(
                            model = item.imageUrl,
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(150.dp)
                                .clip(style.blockShape)
                        )
                    }
                    if (item.badge.isNotBlank()) {
                        Surface(shape = style.pillShape, color = accent) {
                            Text(
                                text = item.badge,
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.surface,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                            )
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        if (item.title.isNotBlank()) {
                            Text(
                                text = item.title,
                                style = MaterialTheme.typography.titleSmall,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier.weight(1f, fill = false)
                            )
                        }
                        if (link.isNotBlank()) {
                            Icon(
                                imageVector = Icons.AutoMirrored.Outlined.OpenInNew,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }
                    if (item.subtitle.isNotBlank()) {
                        Text(
                            item.subtitle,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
internal fun CreatorGalleryBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.images.isEmpty()) return
    val style = LocalCreatorStyle.current
    // `--mkt-gallery-cols` is the creator's own choice on the web; the tiles get
    // shorter as the columns multiply so a four-up row still reads as a row of
    // pictures rather than a row of slivers.
    val columns = style.galleryColumns
    val tileHeight = when (columns) {
        2 -> 130.dp
        3 -> 104.dp
        else -> 84.dp
    }
    CreatorBlockShell(title = block.title.ifBlank { "Gallery" }, subtitle = block.subtitle, isLast = isLast) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.images.chunked(columns).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    row.forEach { image ->
                        AsyncImage(
                            model = image,
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .weight(1f)
                                .height(tileHeight)
                                .clip(style.blockShape)
                        )
                    }
                    repeat(columns - row.size) { Spacer(Modifier.weight(1f)) }
                }
            }
        }
    }
}

@Composable
internal fun CreatorTestimonialsBlock(block: ApiCreatorBlock, accent: Color, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    CreatorBlockShell(title = block.title.ifBlank { "What students say" }, subtitle = block.subtitle, isLast = isLast) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(style.blockShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        text = "“${item.quote}”",
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (item.avatarUrl.isNotBlank()) {
                            AsyncImage(
                                model = item.avatarUrl,
                                contentDescription = null,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier
                                    .size(28.dp)
                                    .clip(CircleShape)
                            )
                        }
                        Column {
                            Text(
                                item.name,
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = accent
                            )
                            if (item.role.isNotBlank()) {
                                Text(
                                    item.role,
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
}

@Composable
internal fun CreatorFaqBlock(block: ApiCreatorBlock, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    CreatorBlockShell(title = block.title.ifBlank { "Questions" }, subtitle = block.subtitle, isLast = isLast) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(style.blockShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Text(item.q, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Text(
                        item.a,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
internal fun CreatorScheduleBlock(block: ApiCreatorBlock, accent: Color, isLast: Boolean) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Schedule" }, subtitle = block.subtitle, isLast = isLast) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.items.forEach { item ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.Top,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Text(
                        text = listOf(item.day, item.time).filter { it.isNotBlank() }.joinToString(" · "),
                        style = MaterialTheme.typography.labelMedium,
                        color = accent,
                        modifier = Modifier.width(96.dp)
                    )
                    Column(modifier = Modifier.weight(1f)) {
                        Text(item.title, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
                        if (item.note.isNotBlank()) {
                            Text(
                                item.note,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
internal fun CreatorLinksBlock(block: ApiCreatorBlock, accent: Color, isLast: Boolean) {
    if (block.items.isEmpty()) return
    val style = LocalCreatorStyle.current
    CreatorBlockShell(title = block.title.ifBlank { "Links" }, subtitle = block.subtitle, isLast = isLast) {
        val context = LocalContext.current
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.items.forEach { item ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(style.blockShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .clickable { openCreatorLink(context, item.url) }
                        .padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Icon(
                        imageVector = getMaterialIcon(item.icon.ifBlank { "link" }),
                        contentDescription = null,
                        tint = accent,
                        modifier = Modifier.size(18.dp)
                    )
                    Text(
                        text = item.label.ifBlank { item.url },
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.weight(1f),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Icon(
                        imageVector = Icons.AutoMirrored.Outlined.OpenInNew,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        }
    }
}

@Composable
internal fun CreatorContactBlock(page: ApiCreatorPage, block: ApiCreatorBlock, accent: Color, isLast: Boolean) {
    val style = LocalCreatorStyle.current
    // `show_contact` off means the creator wants the section without publishing
    // an address to the world: the copy stays, the rows go.
    val rows = if (!style.showContact) emptyList() else buildList {
        if (page.contactEmail.isNotBlank()) add("Email" to page.contactEmail)
        if (page.contactPhone.isNotBlank()) add("Phone" to page.contactPhone)
        page.socials.forEach { (key, value) ->
            if (value.isNotBlank()) add(key.replaceFirstChar { it.uppercase() } to value)
        }
    }
    CreatorBlockShell(title = block.title.ifBlank { "Get in touch" }, subtitle = block.subtitle, isLast = isLast) {
        if (block.body.isNotBlank()) {
            Text(block.body, style = MaterialTheme.typography.bodyMedium)
        }
        if (rows.isEmpty() && style.showContact) {
            Text(
                text = "No contact details published yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            val context = LocalContext.current
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                rows.forEach { (label, value) ->
                    val href = when (label.lowercase()) {
                        "email" -> "mailto:$value"
                        "phone" -> "tel:$value"
                        else -> value
                    }
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(style.blockShape)
                            .clickable { openCreatorLink(context, href) }
                            .padding(horizontal = 10.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelMedium,
                            color = accent,
                            modifier = Modifier.width(84.dp)
                        )
                        Text(
                            text = value,
                            style = MaterialTheme.typography.bodyMedium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }
    }
}

@Composable
internal fun CreatorCtaBlock(block: ApiCreatorBlock, accent: Color, onJumpTo: (String) -> Unit) {
    val style = LocalCreatorStyle.current
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = style.blockPadding)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(style.blockShape)
                .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = block.title.ifBlank { "Ready to start?" },
                style = MaterialTheme.typography.titleMediumEmphasized,
                fontWeight = FontWeight.SemiBold,
                color = accent
            )
            if (block.subtitle.isNotBlank()) {
                Text(
                    text = block.subtitle,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (block.ctaLabel.isNotBlank()) {
                val context = LocalContext.current
                // `href="{{ block.cta_url|default:'#offerings' }}"`: a label with
                // no link still goes somewhere, and it goes to the offerings.
                val target = block.ctaUrl.trim()
                val anchored = target.isBlank() || target.startsWith("#")
                NebButton(
                    text = block.ctaLabel,
                    onClick = {
                        if (anchored) {
                            onJumpTo(target.removePrefix("#").ifBlank { "offerings" })
                        } else {
                            openCreatorLink(context, target)
                        }
                    },
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Small,
                    icon = if (anchored) null else Icons.AutoMirrored.Outlined.OpenInNew
                )
            }
        }
    }
}
