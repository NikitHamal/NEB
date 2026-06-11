package com.consica.code.ui.screens.lesson

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.model.LessonType
import com.consica.code.ui.character.TerraDialogue
import com.consica.code.ui.components.PillButton
import com.consica.code.ui.playground.CodeSnippet

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TerraNestScreen(
    onStartChallenge: (String) -> Unit,
    onStartPuzzle: (String) -> Unit,
    onFinished: () -> Unit,
    onBack: () -> Unit,
    viewModel: TerraNestViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()
    val lesson = state.lesson ?: return

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(lesson.titleRes), style = MaterialTheme.typography.titleLarge) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
            )
        },
    ) { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
        ) {
            if (lesson.steps.isNotEmpty()) {
                LinearProgressIndicator(
                    progress = { (state.stepIndex + 1f) / lesson.steps.size },
                    modifier = Modifier.fillMaxWidth(),
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    text = stringResource(R.string.lesson_step_progress, state.stepIndex + 1, lesson.steps.size),
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Spacer(Modifier.height(16.dp))

            Column(
                Modifier
                    .weight(1f)
                    .verticalScroll(rememberScrollState()),
            ) {
                val step = lesson.steps.getOrNull(state.stepIndex)
                if (step != null) {
                    TerraDialogue(
                        text = stringResource(step.textFor(state.ageGroup)),
                        expression = step.expression,
                        ageGroup = state.ageGroup,
                    )
                    step.codeSnippet?.let { snippet ->
                        Spacer(Modifier.height(16.dp))
                        CodeSnippet(code = snippet, language = lesson.language)
                    }
                }
            }

            val isLastStep = state.stepIndex >= lesson.steps.size - 1
            PillButton(
                text = stringResource(
                    when {
                        !isLastStep -> R.string.lesson_continue
                        lesson.type == LessonType.PUZZLE -> R.string.lesson_solve_puzzle
                        lesson.challenge != null -> R.string.lesson_lets_code
                        else -> R.string.lesson_finish
                    }
                ),
                onClick = {
                    if (!isLastStep) {
                        viewModel.nextStep()
                    } else {
                        when {
                            lesson.type == LessonType.PUZZLE && lesson.puzzle != null ->
                                onStartPuzzle(lesson.id)
                            lesson.challenge != null -> onStartChallenge(lesson.id)
                            else -> viewModel.completeTutorial(onFinished)
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
            )
        }
    }
}
