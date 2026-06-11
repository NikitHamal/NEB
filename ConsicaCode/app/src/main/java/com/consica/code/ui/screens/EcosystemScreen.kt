package com.consica.code.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.item
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.CardShape
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.PillShape
import com.consica.code.core.model.EcosystemItemType
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.EmptyState
import com.consica.code.ui.ecosystem.BiomeScene
import com.consica.code.ui.rewards.ecosystemIcon

@Composable
fun EcosystemScreen(
    viewModel: AppViewModel,
    onBack: () -> Unit,
) {
    val ecosystem by viewModel.ecosystem.collectAsState()
    val count by viewModel.ecosystemCount.collectAsState()

    Column(Modifier.fillMaxWidth()) {
        EcoTopBar(title = stringResource(R.string.ecosystem_title), onBack = onBack)

        LazyColumn(
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(Dimens.screenPadding),
            verticalArrangement = Arrangement.spacedBy(Dimens.lg),
        ) {
            item {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Box(
                        Modifier
                            .fillMaxWidth()
                            .clip(CardShape),
                    ) {
                        BiomeScene(
                            items = ecosystem.map { EcosystemItemType.from(it.type) },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(240.dp),
                        )
                    }
                }
            }

            item {
                Text(
                    stringResource(R.string.stat_lessons_done) + " · " + count,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                )
            }

            if (ecosystem.isEmpty()) {
                item { EcoCard { EmptyState(text = stringResource(R.string.rewards_empty)) } }
            } else {
                items(ecosystem, key = { it.id }) { eco ->
                    EcoItemRow(
                        type = EcosystemItemType.from(eco.type),
                        label = eco.label,
                    )
                }
            }

            item { Spacer(Modifier.height(Dimens.xl)) }
        }
    }
}

@Composable
private fun EcoItemRow(type: EcosystemItemType, label: String?) {
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Row(
            Modifier.padding(Dimens.cardPadding),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                Modifier
                    .size(Dimens.iconButton)
                    .clip(PillShape)
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center,
            ) {
                Icon(
                    ecosystemIcon(type),
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                )
            }
            Spacer(Modifier.size(Dimens.lg))
            Column(Modifier.weight(1f)) {
                Text(
                    label ?: type.name.lowercase().replaceFirstChar { it.uppercase() },
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    stringResource(R.string.ecosystem_grew),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}
