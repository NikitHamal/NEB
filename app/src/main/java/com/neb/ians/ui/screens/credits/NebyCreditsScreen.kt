@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.credits

import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material.icons.rounded.Remove
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LoadingIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiCreditTransaction
import com.neb.ians.ui.components.LinkifyText
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.util.formatTimeAgo

private const val POINTS_PER_CREDIT = 2

/**
 * Credits, said once.
 *
 * The screen used to open with a black gradient banner, then repeat the same
 * four numbers across three bordered cards, then ask for the conversion amount
 * in a text field that only accepted even numbers and rejected everything else
 * with a toast. Here the balance is the only large thing, the conversion is a
 * stepper that cannot produce an invalid amount, and the history is a plain
 * list — so there is nothing to read twice and nothing to get wrong.
 */
@Composable
fun NebyCreditsScreen(
    onBack: () -> Unit,
    viewModel: NebyCreditsViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val balance = uiState.balance
    val points = balance.nebiansPoints

    var requested by remember { mutableIntStateOf(POINTS_PER_CREDIT) }
    val maxPoints = remember(points) { points - points % POINTS_PER_CREDIT }
    LaunchedEffect(maxPoints) {
        requested = requested.coerceIn(POINTS_PER_CREDIT, maxOf(POINTS_PER_CREDIT, maxPoints))
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Credits", style = MaterialTheme.typography.titleLargeEmphasized) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { viewModel.loadData() }) {
                        Icon(Icons.Rounded.Refresh, contentDescription = "Refresh")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { padding ->
        if (uiState.isLoading) {
            Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) {
                LoadingIndicator(color = MaterialTheme.colorScheme.onSurface)
            }
            return@Scaffold
        }

        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(bottom = 40.dp)
        ) {
            item(key = "balance") {
                BalanceHeader(
                    total = balance.totalCredits,
                    free = balance.freeCredits,
                    converted = balance.aiCredits
                )
            }

            item(key = "convert") {
                ConvertSection(
                    points = points,
                    requested = requested,
                    maxPoints = maxPoints,
                    converting = uiState.isConverting,
                    onRequestChange = { requested = it },
                    onConvert = {
                        viewModel.convertPoints(
                            points = requested,
                            onSuccess = { Toast.makeText(context, it, Toast.LENGTH_SHORT).show() },
                            onError = { Toast.makeText(context, it, Toast.LENGTH_SHORT).show() }
                        )
                    }
                )
            }

            item(key = "support") {
                SupportSection(
                    contactName = balance.whatsappContact.name,
                    onOpen = {
                        val url = balance.whatsappContact.url
                        if (url.isNotBlank()) {
                            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                        }
                    }
                )
            }

            item(key = "activity_header") {
                SectionLabel("Activity")
            }

            if (uiState.transactions.isEmpty()) {
                item(key = "activity_empty") {
                    Text(
                        text = "Nothing yet. Credits you spend or earn show up here.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp)
                    )
                }
            } else {
                items(uiState.transactions, key = { it.id }) { tx -> ActivityRow(tx) }
            }
        }
    }
}

@Composable
private fun BalanceHeader(total: Int, free: Int, converted: Int) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .padding(top = 16.dp, bottom = 28.dp)
    ) {
        Text(
            text = total.toString(),
            style = MaterialTheme.typography.displayLargeEmphasized,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(Modifier.height(2.dp))
        Text(
            text = if (total == 1) "Neby credit" else "Neby credits",
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(Modifier.height(14.dp))
        Text(
            text = "$free free this month · $converted converted",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(Modifier.height(4.dp))
        Text(
            text = "Ten free credits arrive every month. Mentioning @neby in the forum never costs one.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun ConvertSection(
    points: Int,
    requested: Int,
    maxPoints: Int,
    converting: Boolean,
    onRequestChange: (Int) -> Unit,
    onConvert: () -> Unit
) {
    val canConvert = maxPoints >= POINTS_PER_CREDIT
    val credits = requested / POINTS_PER_CREDIT

    Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp)) {
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
        Spacer(Modifier.height(20.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "NEBians points",
                style = MaterialTheme.typography.titleMediumEmphasized,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = points.toString(),
                style = MaterialTheme.typography.titleMediumEmphasized,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Spacer(Modifier.height(2.dp))
        Text(
            text = "$POINTS_PER_CREDIT points make 1 credit.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        if (canConvert) {
            Spacer(Modifier.height(16.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                StepperButton(
                    icon = Icons.Rounded.Remove,
                    description = "Fewer points",
                    enabled = requested > POINTS_PER_CREDIT && !converting,
                    onClick = { onRequestChange(requested - POINTS_PER_CREDIT) }
                )
                Column(
                    modifier = Modifier.weight(1f),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "$requested pts",
                        style = MaterialTheme.typography.headlineSmallEmphasized,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = if (credits == 1) "becomes 1 credit" else "becomes $credits credits",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center
                    )
                }
                StepperButton(
                    icon = Icons.Rounded.Add,
                    description = "More points",
                    enabled = requested < maxPoints && !converting,
                    onClick = { onRequestChange(requested + POINTS_PER_CREDIT) }
                )
            }
            Spacer(Modifier.height(16.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                NebButton(
                    text = "Convert",
                    onClick = onConvert,
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Hero,
                    loading = converting,
                    modifier = Modifier.weight(1f)
                )
                NebButton(
                    text = "All $maxPoints",
                    onClick = { onRequestChange(maxPoints) },
                    tone = NebButtonTone.Outlined,
                    size = NebButtonSize.Hero,
                    enabled = requested != maxPoints && !converting
                )
            }
        } else {
            Spacer(Modifier.height(12.dp))
            Text(
                text = "Earn $POINTS_PER_CREDIT points to convert your first credit.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun StepperButton(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    description: String,
    enabled: Boolean,
    onClick: () -> Unit
) {
    val tint = if (enabled) {
        MaterialTheme.colorScheme.onSurface
    } else {
        MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f)
    }
    Box(
        modifier = Modifier
            .size(52.dp)
            .nebPressable(enabled = enabled, onClick = onClick)
            .clip(RoundedCornerShape(18.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh),
        contentAlignment = Alignment.Center
    ) {
        Icon(icon, contentDescription = description, tint = tint, modifier = Modifier.size(22.dp))
    }
}

@Composable
private fun SupportSection(contactName: String, onOpen: () -> Unit) {
    Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp)) {
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
        Spacer(Modifier.height(20.dp))
        Text(
            text = "Need more credits?",
            style = MaterialTheme.typography.titleMediumEmphasized
        )
        Spacer(Modifier.height(2.dp))
        Text(
            text = "Message ${contactName.ifBlank { "the developer" }} about extra credits or a project.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(Modifier.height(14.dp))
        NebButton(
            text = "WhatsApp",
            onClick = onOpen,
            tone = NebButtonTone.Tonal,
            size = NebButtonSize.Standard
        )
        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun SectionLabel(text: String) {
    Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp)) {
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
        Spacer(Modifier.height(20.dp))
        Text(text = text, style = MaterialTheme.typography.titleMediumEmphasized)
        Spacer(Modifier.height(8.dp))
    }
}

@Composable
private fun ActivityRow(tx: ApiCreditTransaction) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            LinkifyText(
                text = tx.description.ifBlank { tx.transactionType },
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = formatTimeAgo(tx.createdAt),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Spacer(Modifier.width(12.dp))
        Text(
            text = if (tx.amount > 0) "+${tx.amount}" else tx.amount.toString(),
            style = MaterialTheme.typography.titleSmallEmphasized,
            color = if (tx.amount > 0) {
                MaterialTheme.colorScheme.onSurface
            } else {
                MaterialTheme.colorScheme.onSurfaceVariant
            }
        )
    }
}
