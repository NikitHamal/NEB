package com.consica.code.ui.screens.puzzle

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.Lightbulb
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
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.model.PuzzleBlock
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.LeafConfetti
import com.consica.code.ui.components.PillButton
import com.consica.code.ui.theme.EditorBackground
import com.consica.code.ui.theme.EditorText

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PuzzleScreen(
    onComplete: () -> Unit,
    onBack: () -> Unit,
    viewModel: PuzzleViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()
    val puzzle = state.lesson?.puzzle ?: return

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.puzzle_title), style = MaterialTheme.typography.titleLarge) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
                actions = {
                    IconButton(onClick = viewModel::toggleHint) {
                        Icon(
                            Icons.Default.Lightbulb,
                            contentDescription = stringResource(R.string.playground_hint),
                            tint = if (state.showHint) MaterialTheme.colorScheme.tertiary
                            else MaterialTheme.colorScheme.onSurfaceVariant,
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
                    .padding(horizontal = 16.dp)
                    .verticalScroll(rememberScrollState()),
            ) {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(14.dp)) {
                        Text(
                            stringResource(puzzle.promptRes),
                            style = MaterialTheme.typography.bodyLarge,
                        )
                        if (state.showHint) {
                            Spacer(Modifier.height(6.dp))
                            Text(
                                text = "💡 " + stringResource(puzzle.hintRes),
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.tertiary,
                            )
                        }
                    }
                }

                Spacer(Modifier.height(14.dp))
                Text(
                    stringResource(R.string.puzzle_your_blocks),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.height(6.dp))
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(EditorBackground)
                        .padding(10.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    if (state.answer.isEmpty()) {
                        Spacer(Modifier.height(40.dp))
                    }
                    state.answer.forEachIndexed { index, block ->
                        AnswerBlockRow(
                            block = block,
                            canMoveUp = index > 0,
                            canMoveDown = index < state.answer.lastIndex,
                            onClick = { viewModel.returnToPool(index) },
                            onMoveUp = { viewModel.moveAnswer(index, -1) },
                            onMoveDown = { viewModel.moveAnswer(index, +1) },
                        )
                    }
                }

                Spacer(Modifier.height(14.dp))
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    state.pool.forEachIndexed { index, block ->
                        PoolBlock(block = block, onClick = { viewModel.pickFromPool(index) })
                    }
                }

                if (state.checked) {
                    Spacer(Modifier.height(10.dp))
                    Text(
                        text = stringResource(
                            if (state.correct) R.string.puzzle_correct else R.string.puzzle_incorrect
                        ),
                        style = MaterialTheme.typography.bodyLarge,
                        color = if (state.correct) MaterialTheme.colorScheme.primary
                        else MaterialTheme.colorScheme.error,
                    )
                }

                Spacer(Modifier.height(14.dp))
                PillButton(
                    text = stringResource(R.string.puzzle_check),
                    onClick = viewModel::check,
                    enabled = state.answer.isNotEmpty(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 24.dp),
                )
            }

            state.celebration?.let { rewards ->
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
                        Text("🧩", style = MaterialTheme.typography.displayMedium)
                        Text(
                            stringResource(R.string.celebrate_lesson_complete),
                            style = MaterialTheme.typography.headlineSmall,
                        )
                        Text(
                            stringResource(R.string.celebrate_xp_gained, rewards.xp),
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.primary,
                        )
                        Spacer(Modifier.height(8.dp))
                        PillButton(
                            text = stringResource(R.string.celebrate_continue),
                            onClick = {
                                viewModel.dismissCelebration()
                                onComplete()
                            },
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun AnswerBlockRow(
    block: PuzzleBlock,
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    onClick: () -> Unit,
    onMoveUp: () -> Unit,
    onMoveDown: () -> Unit,
) {
    Row(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(10.dp))
            .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.18f))
            .clickable(onClick = onClick)
            .padding(start = (10 + block.indent * 18).dp, top = 4.dp, bottom = 4.dp, end = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = block.code,
            style = MaterialTheme.typography.bodyMedium.copy(fontFamily = FontFamily.Monospace),
            color = EditorText,
            modifier = Modifier.weight(1f),
        )
        IconButton(onClick = onMoveUp, enabled = canMoveUp, modifier = Modifier.size(32.dp)) {
            Icon(
                Icons.Default.KeyboardArrowUp,
                contentDescription = stringResource(R.string.puzzle_move_up),
                tint = EditorText,
            )
        }
        Spacer(Modifier.width(2.dp))
        IconButton(onClick = onMoveDown, enabled = canMoveDown, modifier = Modifier.size(32.dp)) {
            Icon(
                Icons.Default.KeyboardArrowDown,
                contentDescription = stringResource(R.string.puzzle_move_down),
                tint = EditorText,
            )
        }
    }
}

@Composable
private fun PoolBlock(block: PuzzleBlock, onClick: () -> Unit) {
    Box(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(10.dp))
            .background(MaterialTheme.colorScheme.secondaryContainer)
            .clickable(onClick = onClick)
            .padding(horizontal = 12.dp, vertical = 10.dp),
    ) {
        Text(
            text = block.code,
            style = MaterialTheme.typography.bodyMedium.copy(fontFamily = FontFamily.Monospace),
            color = MaterialTheme.colorScheme.onSecondaryContainer,
        )
    }
}
