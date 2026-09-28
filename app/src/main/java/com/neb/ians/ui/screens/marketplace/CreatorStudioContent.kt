@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ArrowDownward
import androidx.compose.material.icons.outlined.ArrowUpward
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape

/** Where the studio's editors live. Shared with the studio screen. */

internal fun blockLabel(type: String): String = when (type) {
    "hero" -> "Hero"
    "about" -> "About"
    "stats" -> "Numbers"
    "courses" -> "Courses"
    "resources" -> "Resources"
    "posts" -> "Updates"
    "showcase" -> "Showcase"
    "gallery" -> "Gallery"
    "testimonials" -> "Testimonials"
    "faq" -> "FAQ"
    "schedule" -> "Schedule"
    "links" -> "Links"
    "contact" -> "Contact"
    "cta" -> "Call to action"
    "documents" -> "Documents"
    else -> type.replaceFirstChar { it.uppercase() }
}

@Composable
internal fun StudioCard(content: @Composable ColumnScope.() -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebPanelShape)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
        content = content
    )
}

@Composable
internal fun SaveRow(label: String, saving: Boolean, onSave: () -> Unit) {
    NebButton(
        text = label,
        onClick = onSave,
        tone = NebButtonTone.Primary,
        size = NebButtonSize.Standard,
        loading = saving,
        fillWidth = true
    )
}

@Composable
internal fun BlockRow(
    index: Int,
    block: com.neb.ians.data.api.ApiCreatorBlock,
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    onMoveUp: () -> Unit,
    onMoveDown: () -> Unit,
    onRemove: () -> Unit,
    onToggle: () -> Unit,
    onOpenEditor: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebCardShape)
            .background(MaterialTheme.colorScheme.surfaceContainer)
            .padding(horizontal = 10.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = blockLabel(block.type),
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold
            )
            Text(
                text = block.title.ifBlank { if (block.enabled) "Visible" else "Hidden" },
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
        IconButton(onClick = onToggle) {
            Icon(
                imageVector = if (block.enabled) Icons.Outlined.Visibility else Icons.Outlined.VisibilityOff,
                contentDescription = if (block.enabled) "Hide section" else "Show section",
                modifier = Modifier.size(18.dp)
            )
        }
        IconButton(onClick = onMoveUp, enabled = canMoveUp) {
            Icon(Icons.Outlined.ArrowUpward, contentDescription = "Move up", modifier = Modifier.size(18.dp))
        }
        IconButton(onClick = onMoveDown, enabled = canMoveDown) {
            Icon(Icons.Outlined.ArrowDownward, contentDescription = "Move down", modifier = Modifier.size(18.dp))
        }
        IconButton(onClick = onRemove) {
            Icon(
                imageVector = Icons.Outlined.Delete,
                contentDescription = "Remove section",
                tint = MaterialTheme.colorScheme.error,
                modifier = Modifier.size(18.dp)
            )
        }
        IconButton(onClick = onOpenEditor) {
            Icon(Icons.Outlined.Edit, contentDescription = "Edit section", modifier = Modifier.size(18.dp))
        }
    }
}

@Composable
internal fun BlockItemEditor(
    index: Int,
    itemIndex: Int,
    blockType: String,
    item: ApiCreatorBlockItem,
    viewModel: CreatorStudioViewModel
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebCardShape)
            .background(MaterialTheme.colorScheme.surfaceContainer)
            .padding(10.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Text(
            text = "Item ${itemIndex + 1}",
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        when (blockType) {
            "stats" -> {
                NebAuthField(item.label, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(label = value) } }, "Label")
                NebAuthField(item.value, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(value = value) } }, "Value")
                NebAuthField(item.icon, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(icon = value) } }, "Icon name (optional)")
            }
            "faq" -> {
                NebAuthField(item.q, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(q = value) } }, "Question")
                NebAuthField(item.a, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(a = value) } }, "Answer")
            }
            "testimonials" -> {
                NebAuthField(item.quote, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(quote = value) } }, "Quote", singleLine = false, minHeight = 88.dp)
                NebAuthField(item.name, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(name = value) } }, "Name")
                NebAuthField(item.role, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(role = value) } }, "Role")
                NebAuthField(item.avatarUrl, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(avatarUrl = value) } }, "Photo URL", keyboardType = KeyboardType.Uri)
            }
            "schedule" -> {
                NebAuthField(item.day, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(day = value) } }, "Day")
                NebAuthField(item.time, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(time = value) } }, "Time")
                NebAuthField(item.title, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(title = value) } }, "Title")
                NebAuthField(item.note, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(note = value) } }, "Note")
            }
            "links" -> {
                NebAuthField(item.label, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(label = value) } }, "Label")
                NebAuthField(item.url, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(url = value) } }, "Link", keyboardType = KeyboardType.Uri)
                NebAuthField(item.icon, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(icon = value) } }, "Icon name (optional)")
            }
            else -> {
                NebAuthField(
                    item.title,
                    { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(title = value) } },
                    "Title"
                )
                NebAuthField(
                    item.subtitle,
                    { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(subtitle = value) } },
                    "Subtitle"
                )
                NebAuthField(
                    item.imageUrl,
                    { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(imageUrl = value) } },
                    "Image URL",
                    keyboardType = KeyboardType.Uri
                )
                NebAuthField(
                    item.linkUrl,
                    { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(linkUrl = value) } },
                    "Link",
                    keyboardType = KeyboardType.Uri
                )
                NebAuthField(
                    item.badge,
                    { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(badge = value) } },
                    "Badge"
                )
            }
        }
    }
}
