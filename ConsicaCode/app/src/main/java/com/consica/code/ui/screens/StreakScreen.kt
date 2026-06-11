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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocalFireDepartment
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.EcoPalette
import com.consica.code.core.design.PillShape
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.OfflineBanner
import java.util.concurrent.TimeUnit

@Composable
fun StreakScreen(
    viewModel: AppViewModel,
    onBack: () -> Unit,
) {
    val prefs by viewModel.prefs.collectAsState()

    val today = TimeUnit.MILLISECONDS.toDays(System.currentTimeMillis())
    val doneToday = prefs.lastActiveEpochDay == today

    Column(Modifier.fillMaxWidth()) {
        EcoTopBar(title = stringResource(R.string.streak_title), onBack = onBack)

        LazyColumn(
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(Dimens.screenPadding),
            verticalArrangement = Arrangement.spacedBy(Dimens.lg),
        ) {
            // Big streak number.
            item {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        Modifier
                            .fillMaxWidth()
                            .padding(Dimens.xl),
                        horizontalAlignment = Alignment.CenterHorizontally,
                    ) {
                        Box(
                            Modifier
                                .size(96.dp)
                                .clip(PillShape)
                                .background(EcoPalette.SunYellowDeep.copy(alpha = 0.16f)),
                            contentAlignment = Alignment.Center,
                        ) {
                            Icon(
                                Icons.Filled.LocalFireDepartment,
                                contentDescription = null,
                                tint = EcoPalette.SunYellowDeep,
                                modifier = Modifier.size(48.dp),
                            )
                        }
                        Spacer(Modifier.height(Dimens.md))
                        Text(
                            prefs.currentStreak.toString(),
                            style = MaterialTheme.typography.displaySmall,
                            fontWeight = FontWeight.Bold,
                        )
                        Text(
                            stringResource(R.string.stat_streak_days, prefs.currentStreak),
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }

            // Today status.
            item {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        stringResource(
                            if (doneToday) R.string.streak_today_done else R.string.streak_today_pending
                        ),
                        style = MaterialTheme.typography.titleMedium,
                        textAlign = TextAlign.Center,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(Dimens.cardPadding),
                    )
                }
            }

            // Best streak.
            item {
                Row(
                    Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        stringResource(R.string.streak_best, prefs.bestStreak),
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                }
            }

            item {
                OfflineBanner(
                    text = stringResource(R.string.offline_banner_kid),
                )
            }

            item { Spacer(Modifier.height(Dimens.xl)) }
        }
    }
}
