package com.consica.code.ui.screens.playground

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.RestartAlt
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.data.repository.CompletionRewards
import com.consica.code.domain.execution.ExecutionError
import com.consica.code.domain.execution.FriendlyErrorKind
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.LeafConfetti
import com.consica.code.ui.components.PillButton
import com.consica.code.ui.playground.CodeEditor
import com.consica.code.ui.playground.CodeKeyboard
import com.consica.code.ui.playground.HtmlPreview
import com.consica.code.ui.theme.CodeTextStyle
import com.consica.code.ui.theme.EditorBackground
import com.consica.code.ui.theme.EditorText

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PlaygroundScreen(
    onLessonComplete: () -> Unit,
    onBack: () -> Unit,
    viewModel: PlaygroundViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()
    val code by viewModel.code.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = state.lesson?.let { stringResource(it.titleRes) }
                            ?: stringResource(R.string.playground_title),
                        style = MaterialTheme.typography.titleLarge,
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
                actions = {
                    if (state.isLessonMode) {
                        IconButton(onClick = viewModel::toggleHint) {
                            Icon(
                                Icons.Default.Lightbulb,
                                contentDescription = stringResource(R.string.playground_hint),
                                tint = if (state.showHint) MaterialTheme.colorScheme.tertiary
                                else MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                    IconButton(onClick = viewModel::resetCode) {
                        Icon(
                            Icons.Default.RestartAlt,
                            contentDescription = stringResource(R.string.playground_reset_code),
                        )
                    }
                },
            )
        },
    ) { padding ->
        Box(
            Modifier
                .fillMaxSize()
                .padding(padding),
        ) {
            Column(
                Modifier
                    .fillMaxSize()
                    .imePadding()
                    .padding(horizontal = 16.dp),
            ) {
                state.lesson?.challenge?.let { challenge ->
                    EcoCard(modifier = Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(14.dp)) {
                            Text(
                                stringResource(R.string.playground_instructions),
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.primary,
                            )
                            Text(
                                stringResource(challenge.instructionRes),
                                style = MaterialTheme.typography.bodyMedium,
                            )
                            if (state.showHint) {
                                Spacer(Modifier.height(6.dp))
                                Text(
                                    text = "💡 " + stringResource(challenge.hintRes),
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.tertiary,
                                )
                            }
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                }

                CodeEditor(
                    value = code,
                    onValueChange = viewModel::onCodeChange,
                    language = state.language,
                    showLineNumbers = state.proEditor,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                )

                if (state.ageGroup == AgeGroup.KIDS || !state.proEditor) {
                    CodeKeyboard(
                        language = state.language,
                        onKey = viewModel::onCodeKey,
                    )
                }

                if (state.hasRun) {
                    Spacer(Modifier.height(8.dp))
                    OutputPanel(state = state, modifier = Modifier.weight(0.8f))
                }

                Spacer(Modifier.height(8.dp))
                PillButton(
                    text = stringResource(
                        if (state.ageGroup == AgeGroup.KIDS) R.string.playground_run_kid
                        else R.string.playground_run
                    ),
                    onClick = viewModel::run,
                    enabled = !state.running,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 12.dp),
                )
            }

            state.celebration?.let { rewards ->
                CelebrationOverlay(
                    rewards = rewards,
                    onCollect = {
                        viewModel.dismissCelebration()
                        onLessonComplete()
                    },
                )
            }
            if (state.challengePassed && state.celebration == null && state.hasRun) {
                Box(
                    Modifier
                        .fillMaxWidth()
                        .align(Alignment.BottomCenter)
                        .padding(16.dp),
                ) {
                    PillButton(
                        text = stringResource(R.string.playground_collect_rewards),
                        onClick = onLessonComplete,
                        modifier = Modifier.fillMaxWidth(),
                        containerColor = MaterialTheme.colorScheme.tertiary,
                        contentColor = MaterialTheme.colorScheme.onTertiary,
                    )
                }
            }
        }
    }
}

@Composable
private fun OutputPanel(state: PlaygroundUiState, modifier: Modifier = Modifier) {
    Column(modifier.fillMaxWidth()) {
        Text(
            text = stringResource(
                if (state.language == TrackLanguage.HTML) R.string.playground_preview
                else R.string.playground_output
            ),
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(Modifier.height(4.dp))
        when {
            state.error != null -> ErrorCard(state.error)
            state.language == TrackLanguage.HTML -> HtmlPreview(
                html = state.output,
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .clip(RoundedCornerShape(12.dp)),
            )
            else -> Box(
                Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .clip(RoundedCornerShape(12.dp))
                    .background(EditorBackground)
                    .padding(12.dp),
            ) {
                Text(
                    text = state.output.ifBlank { stringResource(R.string.playground_empty_output) },
                    style = CodeTextStyle,
                    color = EditorText,
                    modifier = Modifier.verticalScroll(rememberScrollState()),
                )
            }
        }
        if (state.isLessonMode && state.error == null) {
            Spacer(Modifier.height(4.dp))
            Text(
                text = stringResource(
                    if (state.challengePassed) R.string.playground_success
                    else R.string.playground_check_again
                ),
                style = MaterialTheme.typography.bodyMedium,
                color = if (state.challengePassed) MaterialTheme.colorScheme.primary
                else MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun ErrorCard(error: ExecutionError) {
    EcoCard(
        modifier = Modifier.fillMaxWidth(),
        containerColor = MaterialTheme.colorScheme.errorContainer,
    ) {
        Column(Modifier.padding(14.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                Text(
                    stringResource(R.string.playground_error_title),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onErrorContainer,
                )
                error.line?.let { line ->
                    Text(
                        stringResource(R.string.playground_error_line, line),
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                    )
                }
            }
            Text(
                text = stringResource(error.kind.friendlyRes()),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onErrorContainer,
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = error.message,
                style = CodeTextStyle,
                color = MaterialTheme.colorScheme.onErrorContainer,
            )
        }
    }
}

private fun FriendlyErrorKind.friendlyRes(): Int = when (this) {
    FriendlyErrorKind.SYNTAX -> R.string.error_friendly_syntax
    FriendlyErrorKind.NAME -> R.string.error_friendly_name
    FriendlyErrorKind.TYPE -> R.string.error_friendly_type
    FriendlyErrorKind.VALUE -> R.string.error_friendly_value
    FriendlyErrorKind.INDEX -> R.string.error_friendly_index
    FriendlyErrorKind.DIVISION_BY_ZERO -> R.string.error_friendly_division
    FriendlyErrorKind.RUNTIME -> R.string.error_friendly_runtime
    FriendlyErrorKind.TIMEOUT -> R.string.error_friendly_timeout
}

@Composable
private fun CelebrationOverlay(
    rewards: CompletionRewards,
    onCollect: () -> Unit,
) {
    Box(Modifier.fillMaxSize()) {
        Box(
            Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.scrim.copy(alpha = 0.45f)),
        )
        LeafConfetti(active = true, modifier = Modifier.fillMaxSize())
        EcoCard(
            modifier = Modifier
                .align(Alignment.Center)
                .fillMaxWidth()
                .padding(28.dp),
        ) {
            Column(
                Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Text("🎉", style = MaterialTheme.typography.displayMedium)
                Text(
                    stringResource(R.string.celebrate_lesson_complete),
                    style = MaterialTheme.typography.headlineSmall,
                )
                Text(
                    stringResource(R.string.celebrate_xp_gained, rewards.xp),
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                )
                if (rewards.sun > 0) {
                    Text(
                        stringResource(R.string.celebrate_sun_gained, rewards.sun),
                        style = MaterialTheme.typography.bodyLarge,
                    )
                }
                if (rewards.water > 0) {
                    Text(
                        stringResource(R.string.celebrate_water_gained, rewards.water),
                        style = MaterialTheme.typography.bodyLarge,
                    )
                }
                rewards.leveledUpTo?.let { level ->
                    Text(
                        stringResource(R.string.celebrate_level_up, level),
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.tertiary,
                    )
                }
                if (rewards.professionalModeJustUnlocked) {
                    Text(
                        stringResource(R.string.celebrate_pro_unlocked),
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.tertiary,
                    )
                }
                if (rewards.newBadgeIds.isNotEmpty()) {
                    Text(
                        stringResource(R.string.celebrate_new_badge),
                        style = MaterialTheme.typography.bodyLarge,
                    )
                }
                if (rewards.newEcosystemItemIds.isNotEmpty()) {
                    Text(
                        stringResource(R.string.celebrate_new_item),
                        style = MaterialTheme.typography.bodyLarge,
                    )
                }
                Spacer(Modifier.height(8.dp))
                PillButton(
                    text = stringResource(R.string.celebrate_continue),
                    onClick = onCollect,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}
