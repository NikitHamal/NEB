@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Payments
import androidx.compose.material.icons.outlined.PushPin
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
import com.neb.ians.data.api.ApiMarketplaceSale
import com.neb.ians.data.api.ApiWithdrawal
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.nebBorderSubtle
import com.neb.ians.util.formatTimeAgo

/* The studio's Updates and Earnings tabs: posting to followers, and the
 * wallet, sales and commission the seller is paid under. The shared studio
 * widgets live in CreatorStudioContent.kt. */

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

/** `WithdrawalRequest.PAYOUT_METHODS`, in the server's order. */
private val PAYOUT_METHODS = listOf(
    "esewa" to "eSewa",
    "khalti" to "Khalti",
    "mobile_banking" to "Mobile banking",
    "connectips" to "ConnectIPS",
    "bank" to "Bank transfer"
)

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
        }
    }

    item(key = "withdraw") {
        StudioCard {
            NebSectionLabel("Withdraw")
            NebFieldHint(
                "We pay out by hand after a check, so give us the account exactly as it is " +
                    "registered. The amount leaves your available balance the moment you ask."
            )
            NebAuthField(
                value = uiState.withdrawAmount,
                onValueChange = viewModel::updateWithdrawAmount,
                label = "Amount (Rs.)",
                keyboardType = KeyboardType.Decimal
            )
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                PAYOUT_METHODS.forEach { (value, label) ->
                    NebChip(
                        label = label,
                        selected = uiState.withdrawMethod == value,
                        onClick = { viewModel.updateWithdrawMethod(value) }
                    )
                }
            }
            NebAuthField(
                value = uiState.withdrawDetails,
                onValueChange = viewModel::updateWithdrawDetails,
                label = "Account name and number",
                singleLine = false,
                minHeight = 84.dp
            )
            NebButton(
                text = "Request withdrawal",
                onClick = viewModel::requestWithdrawal,
                tone = NebButtonTone.Primary,
                size = NebButtonSize.Standard,
                loading = uiState.isRequestingWithdrawal
            )
            if (uiState.withdrawals.isNotEmpty()) {
                NebSectionLabel("Your requests")
                uiState.withdrawals.forEach { withdrawal ->
                    WithdrawalRow(withdrawal)
                    HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
                }
            }
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
internal fun WalletCell(label: String, value: String, modifier: Modifier = Modifier) {
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

/** Approved, pending, or neither — the same chip for a sale and for a payout. */
@Composable
internal fun StatusChip(status: String) {
    Surface(
        shape = WebPillShape,
        color = when (status) {
            "approved", "paid", "completed" -> MaterialTheme.colorScheme.surfaceContainerHighest
            "pending", "processing" -> MaterialTheme.colorScheme.surfaceContainerHigh
            else -> MaterialTheme.colorScheme.errorContainer
        }
    ) {
        Text(
            text = status.replace('_', ' ').replaceFirstChar { it.uppercase() },
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
        )
    }
}

@Composable
internal fun WithdrawalRow(withdrawal: ApiWithdrawal) {
    val label = PAYOUT_METHODS.firstOrNull { it.first == withdrawal.payoutMethod }?.second
        ?: withdrawal.payoutMethod
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = "Rs. ${withdrawal.amount}",
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold
            )
            Text(
                text = listOf(label, formatTimeAgo(withdrawal.createdAt))
                    .filter { it.isNotBlank() }
                    .joinToString(" · "),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            if (withdrawal.adminNotes.isNotBlank()) {
                Text(
                    text = withdrawal.adminNotes,
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        StatusChip(withdrawal.status)
    }
}

@Composable
internal fun SaleRow(sale: ApiMarketplaceSale) {
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
            StatusChip(sale.status)
            Text(
                text = "You receive Rs. ${sale.sellerEarnings}",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
