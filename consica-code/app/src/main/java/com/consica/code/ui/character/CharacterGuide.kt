package com.consica.code.ui.character

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
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
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.GuidanceLevel
import com.consica.code.domain.model.TerraExpression
import com.consica.code.ui.components.TypewriterText
import com.consica.code.ui.theme.LocalReducedMotion
import kotlinx.coroutines.delay

/**
 * Conditional triggers the guide reacts to. Screens report moments and the
 * guide picks an age-appropriate line and expression.
 */
enum class GuideTrigger {
    LESSON_START, STEP_SUCCESS, MISTAKE, OFFLINE, REWARD, LOCKED, STREAK, IDLE_HINT
}

object CharacterGuide {

    fun expressionFor(trigger: GuideTrigger, ageGroup: AgeGroup): TerraExpression = when (trigger) {
        GuideTrigger.LESSON_START -> if (ageGroup == AgeGroup.ADULTS) TerraExpression.PROFESSIONAL else TerraExpression.EXCITED
        GuideTrigger.STEP_SUCCESS -> TerraExpression.PROUD
        GuideTrigger.MISTAKE -> if (ageGroup == AgeGroup.KIDS) TerraExpression.ENCOURAGING else TerraExpression.THINKING
        GuideTrigger.OFFLINE -> TerraExpression.HAPPY
        GuideTrigger.REWARD -> TerraExpression.EXCITED
        GuideTrigger.LOCKED -> TerraExpression.THINKING
        GuideTrigger.STREAK -> TerraExpression.PROUD
        GuideTrigger.IDLE_HINT -> TerraExpression.ENCOURAGING
    }

    fun messageFor(trigger: GuideTrigger, ageGroup: AgeGroup): Int = when (trigger) {
        GuideTrigger.LESSON_START -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_lesson_start_kid
            AgeGroup.TEENS -> R.string.guide_lesson_start_teen
            AgeGroup.ADULTS -> R.string.guide_lesson_start_adult
        }
        GuideTrigger.STEP_SUCCESS -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_success_kid
            AgeGroup.TEENS -> R.string.guide_success_teen
            AgeGroup.ADULTS -> R.string.guide_success_adult
        }
        GuideTrigger.MISTAKE -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_mistake_kid
            AgeGroup.TEENS -> R.string.guide_mistake_teen
            AgeGroup.ADULTS -> R.string.guide_mistake_adult
        }
        GuideTrigger.OFFLINE -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_offline_kid
            else -> R.string.guide_offline_older
        }
        GuideTrigger.REWARD -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_reward_kid
            AgeGroup.TEENS -> R.string.guide_reward_teen
            AgeGroup.ADULTS -> R.string.guide_reward_adult
        }
        GuideTrigger.LOCKED -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_locked_kid
            else -> R.string.guide_locked_older
        }
        GuideTrigger.STREAK -> R.string.guide_streak
        GuideTrigger.IDLE_HINT -> when (ageGroup) {
            AgeGroup.KIDS -> R.string.guide_idle_kid
            else -> R.string.guide_idle_older
        }
    }

    /** Whether the guide should speak for this trigger given the learner's guidance level. */
    fun shouldSpeak(trigger: GuideTrigger, level: GuidanceLevel): Boolean = when (level) {
        GuidanceLevel.FULL -> true
        GuidanceLevel.BALANCED -> trigger != GuideTrigger.IDLE_HINT
        GuidanceLevel.MINIMAL -> trigger == GuideTrigger.REWARD || trigger == GuideTrigger.OFFLINE
    }
}

/**
 * Terra + a rounded dialogue bubble. Text reveals typewriter-style for young
 * learners (instant when reduced motion or minimal guidance is preferred).
 */
@Composable
fun TerraDialogue(
    text: String,
    expression: TerraExpression,
    modifier: Modifier = Modifier,
    ageGroup: AgeGroup = AgeGroup.KIDS,
    typewriter: Boolean = ageGroup != AgeGroup.ADULTS,
) {
    val reducedMotion = LocalReducedMotion.current
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.Bottom,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        TerraAvatar(
            expression = expression,
            modifier = Modifier.size(if (ageGroup == AgeGroup.KIDS) 84.dp else 64.dp),
        )
        Card(
            modifier = Modifier.weight(1f),
            shape = MaterialTheme.shapes.large,
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
        ) {
            Column(Modifier.padding(16.dp)) {
                Text(
                    text = stringResource(R.string.terra_name),
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.primary,
                )
                if (typewriter && !reducedMotion) {
                    TypewriterText(
                        text = text,
                        style = MaterialTheme.typography.bodyLarge,
                    )
                } else {
                    Text(
                        text = text,
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurface,
                    )
                }
            }
        }
    }
}

/**
 * A transient, self-dismissing Terra toast used for conditional triggers
 * (offline, rewards, streaks) without blocking the screen.
 */
@Composable
fun TerraToast(
    text: String,
    expression: TerraExpression,
    visible: Boolean,
    modifier: Modifier = Modifier,
    autoDismissMs: Long = 5000,
    onDismiss: () -> Unit = {},
) {
    var shown by remember { mutableIntStateOf(0) }
    LaunchedEffect(visible) {
        if (visible) {
            shown++
            delay(autoDismissMs)
            onDismiss()
        }
    }
    AnimatedVisibility(
        visible = visible,
        enter = slideInVertically { -it } + fadeIn(),
        exit = fadeOut(),
        modifier = modifier,
    ) {
        Card(
            shape = MaterialTheme.shapes.large,
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer),
            elevation = CardDefaults.cardElevation(defaultElevation = 3.dp),
        ) {
            Row(
                Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                TerraAvatar(expression = expression, modifier = Modifier.size(40.dp), animated = false)
                Text(
                    text = text,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSecondaryContainer,
                )
            }
        }
    }
}
