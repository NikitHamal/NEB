package com.consica.code.ui.screens.ecosystem

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Build
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.CodeLanguage
import com.consica.code.core.model.RunResult
import com.consica.code.core.model.TerraExpression
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.common.EcoCard
import com.consica.code.ui.common.LeafConfetti
import com.consica.code.ui.ecosystem.ConsolePanel
import com.consica.code.ui.ecosystem.DryPlant
import com.consica.code.ui.ecosystem.GrowingPlant
import com.consica.code.ui.ecosystem.HtmlPreview

/**
 * The Ecosystem View: shows HTML preview or Python console output plus the
 * biome's reaction — a growing plant on success, a thirsty plant on errors.
 */
@Composable
fun EcosystemResultView(
    runResult: RunResult,
    language: CodeLanguage,
    code: String,
    user: UserState,
    challengePassed: Boolean,
    hasChallenge: Boolean,
    successLabel: String?,
    rewardsClaimed: Boolean,
    onBackToCode: () -> Unit,
    onClaimRewards: () -> Unit,
) {
    val isSuccess = runResult.success
    val celebration = hasChallenge && challengePassed

    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .navigationBarsPadding(),
        ) {
            // Top bar
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                IconButton(onClick = onBackToCode) {
                    Icon(
                        Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = stringResource(R.string.ecosystem_back_to_code),
                    )
                }
                Text(
                    stringResource(R.string.ecosystem_title),
                    style = MaterialTheme.typography.titleMedium,
                )
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .padding(horizontal = 16.dp),
            ) {
                // Status banner
                StatusBanner(isSuccess = isSuccess, passed = challengePassed, hasChallenge = hasChallenge, ageGroup = user.ageGroup)

                Box(Modifier.height(10.dp))

                if (isSuccess) {
                    if (celebration || !hasChallenge) {
                        GrowingPlant(label = if (celebration) successLabel else null)
                    }
                    Box(Modifier.height(10.dp))
                    when (language) {
                        CodeLanguage.HTML -> {
                            Text(
                                stringResource(R.string.ecosystem_html_preview),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            HtmlPreview(
                                html = code,
                                darkMode = user.darkMode,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .weight(1f)
                                    .padding(vertical = 6.dp),
                            )
                        }
                        CodeLanguage.PYTHON -> {
                            Text(
                                stringResource(R.string.ecosystem_console_output),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            ConsolePanel(
                                output = runResult.output,
                                emptyLabel = stringResource(R.string.playground_empty_console),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .weight(1f)
                                    .padding(vertical = 6.dp),
                            )
                        }
                    }
                } else {
                    ErrorContent(runResult = runResult, ageGroup = user.ageGroup)
                }
            }

            // Bottom actions
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(10.dp),
            ) {
                OutlinedButton(
                    onClick = onBackToCode,
                    shape = PillShape,
                    modifier = Modifier
                        .weight(1f)
                        .height(52.dp),
                ) {
                    Text(stringResource(R.string.ecosystem_back_to_code))
                }
                if (celebration && !rewardsClaimed) {
                    Button(
                        onClick = onClaimRewards,
                        shape = PillShape,
                        modifier = Modifier
                            .weight(1f)
                            .height(52.dp),
                    ) {
                        Text(stringResource(R.string.ecosystem_claim_rewards))
                    }
                }
            }
        }

        if (celebration) {
            LeafConfetti(modifier = Modifier.fillMaxSize())
        }
    }
}

@Composable
private fun StatusBanner(isSuccess: Boolean, passed: Boolean, hasChallenge: Boolean, ageGroup: AgeGroup) {
    val (textRes, expression) = when {
        isSuccess && (!hasChallenge || passed) -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.ecosystem_success_kids to TerraExpression.EXCITED
            AgeGroup.TEENS -> R.string.ecosystem_success_teens to TerraExpression.PROUD
            AgeGroup.PRO -> R.string.ecosystem_success_pro to TerraExpression.PROFESSIONAL
        }
        isSuccess -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.playground_challenge_not_yet_kids to TerraExpression.ENCOURAGING
            AgeGroup.TEENS -> R.string.playground_challenge_not_yet_teens to TerraExpression.THINKING
            AgeGroup.PRO -> R.string.playground_challenge_not_yet_pro to TerraExpression.FOCUSED
        }
        else -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.ecosystem_error_kids to TerraExpression.ENCOURAGING
            AgeGroup.TEENS -> R.string.ecosystem_error_teens to TerraExpression.THINKING
            AgeGroup.PRO -> R.string.ecosystem_error_pro to TerraExpression.FOCUSED
        }
    }

    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.fillMaxWidth(),
    ) {
        TerraAvatar(expression = expression, size = 56.dp, bounce = false)
        Box(Modifier.width(10.dp))
        Text(
            stringResource(textRes),
            style = MaterialTheme.typography.titleSmall,
            modifier = Modifier.weight(1f),
        )
    }
}

@Composable
private fun ErrorContent(runResult: RunResult, ageGroup: AgeGroup) {
    var showTechnical by remember { mutableStateOf(ageGroup == AgeGroup.PRO) }

    Column(modifier = Modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            DryPlant(modifier = Modifier.weight(1f))
            Icon(
                Icons.Filled.Build,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.tertiary,
                modifier = Modifier.width(32.dp),
            )
        }

        if (runResult.friendlyError != null) {
            EcoCard(
                containerColor = MaterialTheme.colorScheme.errorContainer,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 6.dp),
            ) {
                Column(Modifier.padding(14.dp)) {
                    Text(
                        stringResource(R.string.ecosystem_friendly_explainer),
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                    )
                    Text(
                        runResult.friendlyError,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                    )
                }
            }
        }

        if (runResult.technicalError != null) {
            if (ageGroup != AgeGroup.KIDS || showTechnical) {
                ConsolePanel(
                    output = buildString {
                        if (runResult.output.isNotEmpty()) {
                            append(runResult.output)
                            append('\n')
                        }
                        append(runResult.technicalError)
                    },
                    emptyLabel = "",
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(160.dp)
                        .padding(vertical = 6.dp),
                )
            } else {
                OutlinedButton(
                    onClick = { showTechnical = true },
                    shape = PillShape,
                    modifier = Modifier.padding(top = 6.dp),
                ) {
                    Text(stringResource(R.string.ecosystem_technical_details))
                }
            }
        }
    }
}
