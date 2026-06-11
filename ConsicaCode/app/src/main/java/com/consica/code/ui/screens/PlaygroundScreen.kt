package com.consica.code.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.Dimens
import com.consica.code.core.model.LocalAgeConfig
import com.consica.code.domain.content.CodeLang
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.runner.RunResult
import com.consica.code.ui.AppViewModel
import com.consica.code.ui.components.EcoButton
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.EcoOutlinedButton
import com.consica.code.ui.components.OfflineBanner
import com.consica.code.ui.components.SectionHeader
import com.consica.code.ui.playground.CodeEditor
import com.consica.code.ui.playground.ConsolePanel
import com.consica.code.ui.playground.HtmlPreview
import com.consica.code.ui.playground.SymbolBar

@Composable
fun PlaygroundScreen(
    viewModel: AppViewModel,
    lessonId: String? = null,
    onBack: (() -> Unit)? = null,
) {
    val prefs by viewModel.prefs.collectAsState()
    val config = LocalAgeConfig.current

    val lesson = lessonId?.let { LessonCatalog.byId(it) }
    val initialLang = lesson?.lang ?: CodeLang.HTML

    var lang by remember { mutableStateOf(initialLang) }
    var code by remember { mutableStateOf(TextFieldValue(lesson?.starterCode.orEmpty())) }
    var result by remember { mutableStateOf<RunResult?>(null) }
    var proMode by remember { mutableStateOf(config.defaultEditorMode == com.consica.code.core.model.EditorMode.PRO) }
    var showSaveDialog by remember { mutableStateOf(false) }

    // Pro tools are available when the age default is pro OR the learner has unlocked them.
    val proAvailable = config.isPro || prefs.proUnlocked
    val effectivePro = proMode && proAvailable
    val showLineNumbers = effectivePro || config.showLineNumbers
    val showErrors = effectivePro || config.showErrorPanel

    val runLabel = stringResource(if (config.growLabel) R.string.action_grow else R.string.action_run)

    Column(
        modifier = Modifier.fillMaxWidth(),
    ) {
        EcoTopBar(title = stringResource(R.string.playground_title), onBack = onBack)

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(Dimens.screenPadding),
            verticalArrangement = Arrangement.spacedBy(Dimens.lg),
        ) {
            // Language selector.
            Row(horizontalArrangement = Arrangement.spacedBy(Dimens.sm)) {
                FilterChip(
                    selected = lang == CodeLang.HTML,
                    onClick = { lang = CodeLang.HTML; result = null },
                    label = { Text(stringResource(R.string.playground_lang_html)) },
                )
                FilterChip(
                    selected = lang == CodeLang.PYTHON,
                    onClick = { lang = CodeLang.PYTHON; result = null },
                    label = { Text(stringResource(R.string.playground_lang_python)) },
                )
                Spacer(Modifier.weight(1f))
                if (proAvailable) {
                    FilterChip(
                        selected = proMode,
                        onClick = { proMode = !proMode },
                        label = {
                            Text(
                                stringResource(
                                    if (proMode) R.string.playground_pro_mode
                                    else R.string.playground_beginner_mode
                                )
                            )
                        },
                    )
                }
            }

            // Pro unlock prompt for those who haven't unlocked it yet.
            if (!proAvailable) {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(Dimens.cardPadding)) {
                        Text(
                            stringResource(R.string.playground_locked_pro),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        Spacer(Modifier.height(Dimens.md))
                        EcoOutlinedButton(
                            text = stringResource(R.string.playground_unlock_pro),
                            onClick = viewModel::unlockPro,
                        )
                    }
                }
            }

            CodeEditor(
                value = code,
                onValueChange = { code = it },
                modifier = Modifier.fillMaxWidth(),
                showLineNumbers = showLineNumbers,
            )

            SymbolBar(lang = lang, value = code, onValueChange = { code = it })

            Row(horizontalArrangement = Arrangement.spacedBy(Dimens.sm)) {
                EcoButton(
                    text = runLabel,
                    onClick = { result = viewModel.runCode(lang, code.text) },
                    leadingIcon = Icons.Filled.PlayArrow,
                )
                EcoOutlinedButton(
                    text = stringResource(R.string.playground_save_workspace),
                    onClick = { showSaveDialog = true },
                    leadingIcon = Icons.Filled.Save,
                )
            }

            // Output: HTML renders in the WebView; Python prints to the console.
            SectionHeader(
                title = stringResource(
                    if (lang == CodeLang.HTML) R.string.playground_preview else R.string.playground_console
                )
            )
            if (lang == CodeLang.HTML) {
                EcoCard(modifier = Modifier.fillMaxWidth()) {
                    HtmlPreview(
                        html = code.text,
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 200.dp),
                    )
                }
            } else {
                ConsolePanel(
                    result = result,
                    placeholder = stringResource(R.string.playground_no_output, runLabel),
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 140.dp),
                    showErrors = showErrors,
                )
            }

            OfflineBanner(
                text = stringResource(
                    if (config.isPro) R.string.offline_banner_pro else R.string.offline_banner_kid
                ),
            )
            Spacer(Modifier.height(Dimens.xl))
        }
    }

    if (showSaveDialog) {
        var name by remember { mutableStateOf(lesson?.let { stringResource(it.titleRes) } ?: "") }
        AlertDialog(
            onDismissRequest = { showSaveDialog = false },
            title = { Text(stringResource(R.string.playground_save_workspace), fontWeight = FontWeight.Bold) },
            text = {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text(stringResource(R.string.playground_workspace_name)) },
                    singleLine = true,
                )
            },
            confirmButton = {
                TextButton(
                    enabled = name.isNotBlank(),
                    onClick = {
                        viewModel.saveWorkspace(name.trim(), lang, code.text, lessonId)
                        showSaveDialog = false
                    },
                ) { Text(stringResource(R.string.action_save)) }
            },
            dismissButton = {
                TextButton(onClick = { showSaveDialog = false }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
        )
    }
}
