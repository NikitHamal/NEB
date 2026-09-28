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
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
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
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.getMaterialIcon

/* The supporting storefront blocks: showcase, gallery, testimonials, FAQ,
 * schedule, links, contact and the closing call to action. Dispatched from
 * CreatorPageScreen.kt alongside CreatorPageBlocks.kt. */

@Composable
internal fun CreatorShowcaseBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Showcase" }, subtitle = block.subtitle) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
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
                                .clip(WebCardShape)
                        )
                    }
                    if (item.badge.isNotBlank()) {
                        Surface(shape = WebPillShape, color = accent) {
                            Text(
                                text = item.badge,
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.surface,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                            )
                        }
                    }
                    if (item.title.isNotBlank()) {
                        Text(item.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
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
internal fun CreatorGalleryBlock(block: ApiCreatorBlock, page: ApiCreatorPage) {
    if (block.images.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Gallery" }, subtitle = block.subtitle) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.images.chunked(2).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    row.forEach { image ->
                        AsyncImage(
                            model = image,
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .weight(1f)
                                .height(130.dp)
                                .clip(WebCardShape)
                        )
                    }
                    if (row.size == 1) Spacer(Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
internal fun CreatorTestimonialsBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "What students say" }) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
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
internal fun CreatorFaqBlock(block: ApiCreatorBlock) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Questions" }) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
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
internal fun CreatorScheduleBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Schedule" }) {
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
internal fun CreatorLinksBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Links" }) {
        val context = LocalContext.current
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.items.forEach { item ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
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
                        imageVector = Icons.Outlined.OpenInNew,
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
internal fun CreatorContactBlock(page: ApiCreatorPage, block: ApiCreatorBlock, accent: Color) {
    val rows = buildList {
        if (page.contactEmail.isNotBlank()) add("Email" to page.contactEmail)
        if (page.contactPhone.isNotBlank()) add("Phone" to page.contactPhone)
        page.socials.forEach { (key, value) ->
            if (value.isNotBlank()) add(key.replaceFirstChar { it.uppercase() } to value)
        }
    }
    CreatorBlockShell(title = block.title.ifBlank { "Get in touch" }, subtitle = block.subtitle) {
        if (block.body.isNotBlank()) {
            Text(block.body, style = MaterialTheme.typography.bodyMedium)
        }
        if (rows.isEmpty()) {
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
                            .clip(WebCardShape)
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
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 14.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(WebPanelShape)
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
                NebButton(
                    text = block.ctaLabel,
                    onClick = {
                        if (block.ctaUrl.startsWith("#")) {
                            onJumpTo(block.ctaUrl.removePrefix("#"))
                        } else {
                            openCreatorLink(context, block.ctaUrl)
                        }
                    },
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Small,
                    icon = Icons.Outlined.OpenInNew
                )
            }
        }
    }
}
