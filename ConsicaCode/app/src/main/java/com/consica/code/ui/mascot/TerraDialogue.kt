package com.consica.code.ui.mascot

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.LocalReducedMotion
import com.consica.code.core.design.SheetShape
import com.consica.code.core.model.LocalAgeConfig
import kotlinx.coroutines.delay

/**
 * Terra's bottom-sheet-style dialogue bubble. Large, rounded, readable, with optional typewriter
 * reveal (kids/tweens, unless reduced-motion) and a minimize control for older learners who want
 * less guidance.
 */
@Composable
fun TerraDialogue(
    text: String,
    expression: TerraExpression,
    modifier: Modifier = Modifier,
    minimized: Boolean = false,
    onToggleMinimize: (() -> Unit)? = null,
    footer: (@Composable () -> Unit)? = null,
) {
    val config = LocalAgeConfig.current
    val reducedMotion = LocalReducedMotion.current
    val useTypewriter = config.typewriterDialogue && !reducedMotion

    var shown by remember(text) { mutableIntStateOf(if (useTypewriter) 0 else text.length) }
    LaunchedEffect(text, useTypewriter) {
        if (useTypewriter) {
            for (i in 1..text.length) { shown = i; delay(18) }
        } else shown = text.length
    }

    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = SheetShape,
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 2.dp,
        shadowElevation = 0.dp,
    ) {
        Column(Modifier.padding(Dimens.lg)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Terra(expression = expression, size = if (minimized) Dimens.mascotSmall else Dimens.mascotSize)
                Spacer(Modifier.width(Dimens.md))
                if (!minimized) {
                    Text(
                        text = text.take(shown),
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurface,
                        modifier = Modifier.weight(1f),
                    )
                } else {
                    Text(
                        text = stringResource(R.string.tutorial_expand_guide),
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.weight(1f),
                    )
                }
                if (onToggleMinimize != null) {
                    IconButton(onClick = onToggleMinimize) {
                        Icon(
                            imageVector = if (minimized) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore,
                            contentDescription = stringResource(
                                if (minimized) R.string.tutorial_expand_guide else R.string.tutorial_minimize_guide
                            ),
                        )
                    }
                }
            }
            AnimatedVisibility(visible = !minimized && footer != null) {
                Column {
                    Spacer(Modifier.height(Dimens.md))
                    Row(
                        Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.End,
                    ) { footer?.invoke() }
                }
            }
        }
    }
}
