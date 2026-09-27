@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.ArrowDownward
import androidx.compose.material.icons.outlined.ArrowUpward
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Payments
import androidx.compose.material.icons.outlined.PushPin
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
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
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiMarketplaceSale
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.NebPriceField
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.nebBorderSubtle
import com.neb.ians.util.formatTimeAgo

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
            }
            "faq" -> {
                NebAuthField(item.q, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(q = value) } }, "Question")
                NebAuthField(item.a, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(a = value) } }, "Answer")
            }
            "testimonials" -> {
                NebAuthField(item.quote, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(quote = value) } }, "Quote", singleLine = false, minHeight = 88.dp)
                NebAuthField(item.name, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(name = value) } }, "Name")
                NebAuthField(item.role, { value -> viewModel.updateBlockItem(index, itemIndex) { it.copy(role = value) } }, "Role")
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
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Tab bodies
// ---------------------------------------------------------------------------

internal fun LazyListScope.studioCoursesTab(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    item(key = "course_list") {
        StudioCard {
            NebSectionLabel("Your offerings")
            NebFieldHint("Paid courses and classes, plus the free ones. Buyers check out by QR on your page.")
            if (uiState.courses.isEmpty()) {
                NebEmptyState(
                    icon = Icons.Outlined.Payments,
                    title = "No offerings yet",
                    subtitle = "Add your first course below — a title and a price are enough to start."
                )
            } else {
                uiState.courses.forEach { course ->
                    CourseStudioRow(
                        course = course,
                        onEdit = { viewModel.editCourse(course) },
                        onDelete = { viewModel.deleteCourse(course.id) }
                    )
                    HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
                }
            }
        }
    }

    item(key = "course_form") {
        val draft = uiState.courseDraft
        StudioCard {
            NebSectionLabel(if (draft.id.isBlank()) "New offering" else "Edit offering")
            NebAuthField(draft.title, { value -> viewModel.updateCourseDraft { it.copy(title = value) } }, "Title")
            NebAuthField(
                draft.summary,
                { value -> viewModel.updateCourseDraft { it.copy(summary = value) } },
                "One-line summary"
            )
            NebAuthField(
                draft.description,
                { value -> viewModel.updateCourseDraft { it.copy(description = value) } },
                "Description",
                singleLine = false,
                minHeight = 108.dp
            )

            NebPriceField(
                isPaid = draft.isPaid,
                price = draft.price,
                onIsPaidChange = { paid -> viewModel.updateCourseDraft { it.copy(isPaid = paid) } },
                onPriceChange = { value -> viewModel.updateCourseDraft { it.copy(price = value) } },
                commissionPercent = uiState.commissionPercent,
                title = "Price this offering",
                subtitle = "Free offerings show in the marketplace for everyone. Paid ones check out by QR, and your share lands in your wallet once verified."
            )

            NebAuthField(draft.level, { value -> viewModel.updateCourseDraft { it.copy(level = value) } }, "Level")
            NebAuthField(
                draft.durationLabel,
                { value -> viewModel.updateCourseDraft { it.copy(durationLabel = value) } },
                "Duration"
            )
            NebAuthField(
                draft.lessonCount,
                { value -> viewModel.updateCourseDraft { it.copy(lessonCount = value.filter { c -> c.isDigit() }) } },
                "Lessons",
                keyboardType = KeyboardType.Number
            )
            NebAuthField(
                draft.seatLimit,
                { value -> viewModel.updateCourseDraft { it.copy(seatLimit = value.filter { c -> c.isDigit() }) } },
                "Seats (0 = unlimited)",
                keyboardType = KeyboardType.Number
            )
            NebAuthField(
                draft.includes,
                { value -> viewModel.updateCourseDraft { it.copy(includes = value) } },
                "What's included (one per line)",
                singleLine = false,
                minHeight = 88.dp
            )
            NebAuthField(draft.tags, { value -> viewModel.updateCourseDraft { it.copy(tags = value) } }, "Tags")
            NebAuthField(
                draft.coverUrl,
                { value -> viewModel.updateCourseDraft { it.copy(coverUrl = value) } },
                "Cover image URL",
                keyboardType = KeyboardType.Uri
            )
            NebSectionLabel("Status")
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("draft", "published", "archived").forEach { status ->
                    NebChip(
                        label = status.replaceFirstChar { it.uppercase() },
                        selected = draft.status == status,
                        onClick = { viewModel.updateCourseDraft { it.copy(status = status) } }
                    )
                }
            }
            NebToggleRow(
                title = "Feature this offering",
                subtitle = "Featured offerings sort first in the marketplace",
                checked = draft.featured,
                onCheckedChange = { value -> viewModel.updateCourseDraft { it.copy(featured = value) } }
            )

            if (uiState.resourceOptions.isNotEmpty()) {
                NebSectionLabel("Attach your library resources")
                uiState.resourceOptions.take(12).forEach { (id, title) ->
                    val selected = draft.resourceIds.contains(id)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(WebCardShape)
                            .clickable {
                                viewModel.updateCourseDraft { current ->
                                    current.copy(
                                        resourceIds = if (selected) {
                                            current.resourceIds - id
                                        } else {
                                            current.resourceIds + id
                                        }
                                    )
                                }
                            }
                            .padding(horizontal = 10.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(18.dp)
                                .clip(CircleShape)
                                .background(
                                    if (selected) {
                                        MaterialTheme.colorScheme.onSurface
                                    } else {
                                        MaterialTheme.colorScheme.surfaceContainerHigh
                                    }
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            if (selected) {
                                Icon(
                                    imageVector = Icons.Filled.Check,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.surface,
                                    modifier = Modifier.size(12.dp)
                                )
                            }
                        }
                        Text(
                            text = title,
                            style = MaterialTheme.typography.bodySmall,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                NebButton(
                    text = if (draft.id.isBlank()) "Save offering" else "Save changes",
                    onClick = viewModel::saveCourse,
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Standard,
                    loading = uiState.isSavingCourse
                )
                if (draft.id.isNotBlank()) {
                    NebButton(
                        text = "Start a new one",
                        onClick = viewModel::newCourse,
                        tone = NebButtonTone.Text,
                        size = NebButtonSize.Standard
                    )
                }
            }
        }
    }
}

@Composable
private fun CourseStudioRow(course: ApiCreatorCourse, onEdit: () -> Unit, onDelete: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = course.title,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = listOf(
                    if (course.isFree) "Free" else "Rs. ${course.price}",
                    course.status.replaceFirstChar { it.uppercase() },
                    if (course.saleCount > 0) "${course.saleCount} sold" else null
                ).filterNotNull().joinToString(" · "),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        NebButton(
            text = "Edit",
            onClick = onEdit,
            tone = NebButtonTone.Text,
            size = NebButtonSize.Small
        )
        IconButton(onClick = onDelete) {
            Icon(
                imageVector = Icons.Outlined.Delete,
                contentDescription = "Delete offering",
                tint = MaterialTheme.colorScheme.error,
                modifier = Modifier.size(18.dp)
            )
        }
    }
}

internal fun LazyListScope.studioUpdatesTab(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    item(key = "post_list") {
        StudioCard {
            NebSectionLabel("Updates")
            NebFieldHint("Announcements, new batches, exam tips — the first thing your students see on your page.")
            if (uiState.posts.isEmpty()) {
                NebEmptyState(
                    icon = Icons.Outlined.PushPin,
                    title = "No updates yet",
                    subtitle = "Post your first one below."
                )
            } else {
                uiState.posts.forEach { post ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = post.title.ifBlank { post.body.take(48) },
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.SemiBold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = listOfNotNull(
                                    if (post.pinned) "Pinned" else null,
                                    formatTimeAgo(post.createdAt),
                                    if (!post.published) "Hidden" else null
                                ).joinToString(" · "),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        NebButton(
                            text = "Edit",
                            onClick = { viewModel.editPost(post) },
                            tone = NebButtonTone.Text,
                            size = NebButtonSize.Small
                        )
                        IconButton(onClick = { viewModel.deletePost(post.id) }) {
                            Icon(
                                imageVector = Icons.Outlined.Delete,
                                contentDescription = "Delete update",
                                tint = MaterialTheme.colorScheme.error,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                    HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
                }
            }
        }
    }

    item(key = "post_form") {
        val draft = uiState.postDraft
        StudioCard {
            NebSectionLabel(if (draft.id.isBlank()) "New update" else "Edit update")
            NebAuthField(draft.title, { value -> viewModel.updatePostDraft { it.copy(title = value) } }, "Headline (optional)")
            NebAuthField(
                draft.body,
                { value -> viewModel.updatePostDraft { it.copy(body = value) } },
                "Message",
                singleLine = false,
                minHeight = 108.dp
            )
            NebAuthField(
                draft.mediaUrl,
                { value -> viewModel.updatePostDraft { it.copy(mediaUrl = value) } },
                "Image URL",
                keyboardType = KeyboardType.Uri
            )
            NebAuthField(
                draft.linkUrl,
                { value -> viewModel.updatePostDraft { it.copy(linkUrl = value) } },
                "Link",
                keyboardType = KeyboardType.Uri
            )
            NebToggleRow(
                title = "Pin to the top",
                subtitle = "Pinned updates lead the section",
                checked = draft.pinned,
                onCheckedChange = { value -> viewModel.updatePostDraft { it.copy(pinned = value) } }
            )
            NebToggleRow(
                title = "Visible on my page",
                subtitle = "Turn off to write without publishing",
                checked = draft.published,
                onCheckedChange = { value -> viewModel.updatePostDraft { it.copy(published = value) } }
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                NebButton(
                    text = if (draft.id.isBlank()) "Post update" else "Save update",
                    onClick = viewModel::savePost,
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Standard,
                    loading = uiState.isSavingPost
                )
                if (draft.id.isNotBlank()) {
                    NebButton(
                        text = "Start a new one",
                        onClick = viewModel::newPost,
                        tone = NebButtonTone.Text,
                        size = NebButtonSize.Standard
                    )
                }
            }
        }
    }
}

internal fun LazyListScope.studioEarningsTab(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    item(key = "wallet") {
        StudioCard {
            NebSectionLabel("Wallet")
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                WalletCell("Available", "Rs. ${uiState.wallet.currentBalance}", Modifier.weight(1f))
                WalletCell("Earned", "Rs. ${uiState.wallet.totalEarned}", Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                WalletCell("Withdrawn", "Rs. ${uiState.wallet.totalWithdrawn}", Modifier.weight(1f))
                WalletCell("Nebians points", uiState.nebiansPoints.toString(), Modifier.weight(1f))
            }
            NebFieldHint(
                "Withdrawals open at Rs. ${uiState.wallet.withdrawMin}. The platform fee is " +
                    "${uiState.commissionPercent}% of a sale, and it is already deducted in the numbers above."
            )
            NebFieldHint("Request a withdrawal from the web studio, or from your profile's wallet page in the app.")
        }
    }

    item(key = "sales") {
        StudioCard {
            NebSectionLabel("Sales")
            if (uiState.sales.isEmpty()) {
                NebEmptyState(
                    icon = Icons.Outlined.Payments,
                    title = "No sales yet",
                    subtitle = "A verified sale shows here with the buyer, the amount and your share."
                )
            } else {
                uiState.sales.forEach { sale ->
                    SaleRow(sale)
                    HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
                }
            }
        }
    }
}

@Composable
private fun WalletCell(label: String, value: String, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .clip(WebCardShape)
            .background(MaterialTheme.colorScheme.surfaceContainer)
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = value,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
    }
}

@Composable
private fun SaleRow(sale: ApiMarketplaceSale) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = sale.targetTitle,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = "${sale.buyerName} · ${formatTimeAgo(sale.createdAt)}",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Column(horizontalAlignment = Alignment.End) {
            Text(
                text = "Rs. ${sale.amount}",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold
            )
            Surface(
                shape = WebPillShape,
                color = when (sale.status) {
                    "approved" -> MaterialTheme.colorScheme.surfaceContainerHighest
                    "pending" -> MaterialTheme.colorScheme.surfaceContainerHigh
                    else -> MaterialTheme.colorScheme.errorContainer
                }
            ) {
                Text(
                    text = sale.status.replaceFirstChar { it.uppercase() },
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                )
            }
            Text(
                text = "You receive Rs. ${sale.sellerEarnings}",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
