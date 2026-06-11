package com.consica.code.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.audio.LocalSoundController
import com.consica.code.core.audio.Sfx
import com.consica.code.core.design.Dimens
import com.consica.code.core.model.LocalAgeConfig
import com.consica.code.data.repository.CompletionResult
import com.consica.code.domain.content.AgeIntro
import com.consica.code.domain.content.CodeLang
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.content.LessonKind
import com.consica.code.domain.runner.RunResult
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoButton
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.EcoOutlinedButton
import com.consica.code.ui.components.EmptyState
import com.consica.code.ui.components.LeafConfetti
import com.consica.code.ui.dragdrop.BlockPuzzleBoard
import com.consica.code.ui.mascot.CharacterGuide
import com.consica.code.ui.mascot.GuideTrigger
import com.consica.code.ui.mascot.TerraDialogue
import com.consica.code.ui.mascot.TerraExpression
import com.consica.code.ui.playground.CodeEditor
import com.consica.code.ui.playground.ConsolePanel
import com.consica.code.ui.playground.HtmlPreview
import com.consica.code.ui.playground.SymbolBar
import com.consica.code.ui.rewards.badgeIcon

@Composable
fun LessonScreen(
    viewModel: AppViewModel,
    lessonId: String,
    onBack: () -> Unit,
    onOpenLesson: (String) -> Unit,
) {
    val lesson = LessonCatalog.byId(lessonId)
    if (lesson == null) {
        Column(Modifier.fillMaxSize()) {
            EcoTopBar(title = stringResource(R.string.tutorial_title), onBack = onBack)
            EmptyState(text = stringResource(R.string.empty_generic))
        }
        return
    }

    val config = LocalAgeConfig.current
    val sound = LocalSoundController.current
    val prefs by viewModel.prefs.collectAsState()

    LaunchedEffect(lessonId) { viewModel.startLesson(lessonId) }

    var minimized by remember(lessonId) { mutableStateOf(false) }
    var showHint by remember(lessonId) { mutableStateOf(false) }
    var failed by remember(lessonId) { mutableStateOf(false) }
    var completion by remember(lessonId) { mutableStateOf<CompletionResult?>(null) }

    // Code lesson state.
    var code by remember(lessonId) { mutableStateOf(TextFieldValue(lesson.starterCode)) }
    var result by remember(lessonId) { mutableStateOf<RunResult?>(null) }

    // Puzzle lesson state.
    val correctOrder = lesson.puzzle?.blocksInOrder.orEmpty()
    val shuffled = remember(lessonId) {
        if (correctOrder.size <= 1) correctOrder
        else {
            var s = correctOrder.shuffled()
            while (s == correctOrder) s = correctOrder.shuffled()
            s
        }
    }
    var order by remember(lessonId) { mutableStateOf(shuffled) }

    val expression = when {
        completion != null -> CharacterGuide.expressionFor(GuideTrigger.Success, config)
        failed -> CharacterGuide.expressionFor(GuideTrigger.Error, config)
        showHint -> CharacterGuide.expressionFor(GuideTrigger.Hint, config)
        else -> CharacterGuide.expressionFor(GuideTrigger.Greet, config)
    }

    val hintLine = CharacterGuide.line(GuideTrigger.Hint)
    val errorLine = CharacterGuide.line(GuideTrigger.Error)
    val introText = lessonIntro(lesson.intro, lesson.goalRes, lesson.goal, config.toneBucket)
    val dialogueText = when {
        failed -> errorLine
        showHint -> hintLine
        else -> introText
    }

    val runLabel = stringResource(if (config.growLabel) R.string.action_grow else R.string.action_run)
    val showErrors = config.showErrorPanel || (config.isPro)

    fun finishCode() {
        val r = viewModel.runCode(lesson.lang, code.text)
        result = r
        viewModel.recordAttempt(lesson, code.text, r)
        if (viewModel.evaluate(lesson, code.text, r)) {
            failed = false
            sound.play(Sfx.Success)
            viewModel.completeLesson(lesson, code.text) { completion = it }
        } else {
            failed = true
            showHint = true
            sound.play(Sfx.GentleError)
        }
    }

    fun finishPuzzle() {
        if (order == correctOrder) {
            failed = false
            sound.play(Sfx.Success)
            viewModel.completeLesson(lesson, order.joinToString("\n")) { completion = it }
        } else {
            failed = true
            showHint = true
            sound.play(Sfx.GentleError)
        }
    }

    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize()) {
            EcoTopBar(title = stringResource(lesson.titleRes), onBack = onBack)

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
                    .padding(Dimens.screenPadding),
                verticalArrangement = Arrangement.spacedBy(Dimens.lg),
            ) {
                TerraDialogue(
                    text = dialogueText,
                    expression = expression,
                    minimized = minimized,
                    onToggleMinimize = { minimized = !minimized },
                    footer = {
                        EcoOutlinedButton(
                            text = stringResource(R.string.action_hint),
                            onClick = { showHint = true },
                        )
                    },
                )

                if (lesson.kind == LessonKind.PUZZLE) {
                    Text(
                        lesson.puzzle?.prompt ?: stringResource(R.string.dragdrop_instruction),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    BlockPuzzleBoard(
                        blocks = shuffled,
                        onOrderChange = { order = it },
                    )
                    if (failed) {
                        Text(
                            stringResource(R.string.dragdrop_incorrect),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.error,
                        )
                    }
                    EcoButton(
                        text = stringResource(R.string.dragdrop_check_order),
                        onClick = { finishPuzzle() },
                        leadingIcon = Icons.Filled.CheckCircle,
                    )
                } else {
                    CodeEditor(
                        value = code,
                        onValueChange = { code = it; failed = false },
                        modifier = Modifier.fillMaxWidth(),
                        showLineNumbers = config.showLineNumbers,
                    )
                    SymbolBar(lang = lesson.lang, value = code, onValueChange = { code = it })

                    Row(horizontalArrangement = Arrangement.spacedBy(Dimens.sm)) {
                        EcoButton(
                            text = if (config.growLabel) stringResource(R.string.action_grow)
                            else stringResource(R.string.action_check),
                            onClick = { finishCode() },
                            leadingIcon = Icons.Filled.CheckCircle,
                        )
                        EcoOutlinedButton(
                            text = runLabel,
                            onClick = { result = viewModel.runCode(lesson.lang, code.text) },
                        )
                    }

                    if (lesson.lang == CodeLang.HTML) {
                        EcoCard(modifier = Modifier.fillMaxWidth()) {
                            HtmlPreview(
                                html = code.text,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .heightIn(min = 180.dp),
                            )
                        }
                    } else {
                        ConsolePanel(
                            result = result,
                            placeholder = stringResource(R.string.playground_no_output, runLabel),
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(min = 120.dp),
                            showErrors = showErrors,
                        )
                    }
                }
                Spacer(Modifier.height(Dimens.xxl))
            }
        }

        LeafConfetti(
            play = completion != null && config.celebratoryRewards,
            modifier = Modifier.fillMaxSize(),
        )
    }

    completion?.let { c ->
        val next = LessonCatalog.next(lessonId)
        CompletionDialog(
            result = c,
            onClose = onBack,
            nextLabel = next?.let { stringResource(it.titleRes) },
            onNext = next?.let { { onOpenLesson(it.id) } },
        )
    }
}

@Composable
private fun CompletionDialog(
    result: CompletionResult,
    onClose: () -> Unit,
    nextLabel: String?,
    onNext: (() -> Unit)?,
) {
    AlertDialog(
        onDismissRequest = onClose,
        title = {
            Text(
                stringResource(R.string.terra_success_kid),
                fontWeight = FontWeight.Bold,
            )
        },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(Dimens.sm)) {
                Text(
                    stringResource(R.string.ecosystem_grew),
                    style = MaterialTheme.typography.bodyMedium,
                )
                Text(
                    "+${result.xpGained} " + stringResource(R.string.stat_xp) +
                        "   +${result.sunGained} " + stringResource(R.string.stat_sun) +
                        "   +${result.waterGained} " + stringResource(R.string.stat_water),
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.primary,
                )
                if (result.leveledUp) {
                    Text(
                        stringResource(R.string.stat_level) + " " + result.newLevel,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.tertiary,
                    )
                }
                result.newBadges.forEach { badge ->
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        androidx.compose.material3.Icon(
                            badgeIcon(badge.iconKey),
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.tertiary,
                            modifier = Modifier.height(20.dp),
                        )
                        Spacer(Modifier.height(Dimens.xs))
                        Text(
                            "  " + stringResource(R.string.rewards_new_badge) + " " + badge.name,
                            style = MaterialTheme.typography.bodyMedium,
                        )
                    }
                }
            }
        },
        confirmButton = {
            if (onNext != null) {
                TextButton(onClick = onNext) {
                    Text(stringResource(R.string.action_next) + (nextLabel?.let { ": $it" } ?: ""))
                }
            } else {
                TextButton(onClick = onClose) { Text(stringResource(R.string.action_done)) }
            }
        },
        dismissButton = {
            if (onNext != null) {
                TextButton(onClick = onClose) { Text(stringResource(R.string.action_done)) }
            }
        },
    )
}

/** Picks the age-toned intro line, falling back to the lesson goal. */
@Composable
private fun lessonIntro(intro: AgeIntro?, goalRes: Int?, goal: String, tone: String): String = when {
    intro != null -> stringResource(
        when (tone) {
            "kid" -> intro.kid
            "teen" -> intro.teen
            else -> intro.pro
        }
    )
    goalRes != null -> stringResource(goalRes)
    else -> goal
}
