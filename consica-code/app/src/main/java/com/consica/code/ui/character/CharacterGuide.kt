package com.consica.code.ui.character

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
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
import androidx.compose.ui.unit.dp
import com.consica.code.core.designsystem.BubbleShape
import com.consica.code.core.designsystem.CodeTextStyle
import com.consica.code.core.designsystem.EditorBackground
import com.consica.code.core.designsystem.EditorText
import com.consica.code.core.designsystem.LocalEcoUiConfig
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.TerraExpression
import kotlinx.coroutines.delay

/**
 * Reusable character guide: Terra + a rounded dialogue bubble.
 *
 * - Typewriter reveal for KIDS (skipped with reduced motion or tap)
 * - Concise instant text for PRO
 * - Minimized mode for learners who want less guidance
 */
@Composable
fun CharacterGuide(
    text: String,
    expression: TerraExpression,
    ageGroup: AgeGroup,
    guidance: GuidanceLevel,
    modifier: Modifier = Modifier,
    codeSnippet: String? = null,
    minimized: Boolean = false,
    onTap: (() -> Unit)? = null,
) {
    val config = LocalEcoUiConfig.current
    val useTypewriter = ageGroup == AgeGroup.KIDS && !config.reducedMotion && guidance != GuidanceLevel.MINIMAL

    var visibleChars by remember(text) { mutableIntStateOf(if (useTypewriter) 0 else text.length) }

    LaunchedEffect(text, useTypewriter) {
        if (useTypewriter) {
            visibleChars = 0
            while (visibleChars < text.length) {
                delay(16)
                visibleChars = (visibleChars + 2).coerceAtMost(text.length)
            }
        } else {
            visibleChars = text.length
        }
    }

    AnimatedVisibility(
        visible = !minimized,
        enter = fadeIn() + expandVertically(),
        exit = fadeOut() + shrinkVertically(),
        modifier = modifier,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clickable {
                    if (visibleChars < text.length) {
                        visibleChars = text.length
                    } else {
                        onTap?.invoke()
                    }
                },
            verticalAlignment = Alignment.Bottom,
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            TerraAvatar(
                expression = expression,
                size = if (ageGroup == AgeGroup.KIDS) 88.dp else 64.dp,
                bounce = ageGroup != AgeGroup.PRO,
            )
            Surface(
                shape = BubbleShape,
                color = MaterialTheme.colorScheme.surface,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                modifier = Modifier.weight(1f),
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = text.take(visibleChars),
                        style = if (ageGroup == AgeGroup.KIDS) {
                            MaterialTheme.typography.bodyLarge
                        } else {
                            MaterialTheme.typography.bodyMedium
                        },
                    )
                    if (codeSnippet != null && visibleChars >= text.length) {
                        Surface(
                            shape = MaterialTheme.shapes.small,
                            color = EditorBackground,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 12.dp),
                        ) {
                            Text(
                                text = codeSnippet,
                                style = CodeTextStyle,
                                color = EditorText,
                                modifier = Modifier.padding(12.dp),
                            )
                        }
                    }
                }
            }
        }
    }
}
