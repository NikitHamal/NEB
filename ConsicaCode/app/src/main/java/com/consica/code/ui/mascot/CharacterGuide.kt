package com.consica.code.ui.mascot

import androidx.annotation.StringRes
import androidx.compose.runtime.Composable
import androidx.compose.ui.res.stringResource
import com.consica.code.R
import com.consica.code.core.model.AgeConfig
import com.consica.code.core.model.LocalAgeConfig

/** Mascot expressions Terra can show in context. */
enum class TerraExpression { Happy, Excited, Thinking, Confused, Proud, Sleepy, Focused, Professional, Encouraging }

/** Contextual triggers that drive Terra's dialogue and expression. */
enum class GuideTrigger { Greet, Success, Error, Hint, Offline, Streak, Locked, Reward, Thinking }

/**
 * Maps a [GuideTrigger] to an age-appropriate dialogue line (resource-backed, so it localizes)
 * and a matching [TerraExpression]. Centralizing this keeps tone consistent and lets older users
 * get concise lines while younger users get warm, encouraging ones.
 */
object CharacterGuide {

    fun expressionFor(trigger: GuideTrigger, config: AgeConfig): TerraExpression = when (trigger) {
        GuideTrigger.Greet -> if (config.isPro) TerraExpression.Professional else TerraExpression.Happy
        GuideTrigger.Success -> if (config.isKid) TerraExpression.Excited else TerraExpression.Proud
        GuideTrigger.Error -> if (config.isKid) TerraExpression.Encouraging else TerraExpression.Thinking
        GuideTrigger.Hint -> TerraExpression.Thinking
        GuideTrigger.Offline -> if (config.isPro) TerraExpression.Professional else TerraExpression.Encouraging
        GuideTrigger.Streak -> TerraExpression.Excited
        GuideTrigger.Locked -> TerraExpression.Sleepy
        GuideTrigger.Reward -> TerraExpression.Proud
        GuideTrigger.Thinking -> TerraExpression.Focused
    }

    @StringRes
    private fun lineRes(trigger: GuideTrigger, tone: String): Int {
        fun pick(kid: Int, teen: Int, pro: Int) = when (tone) { "kid" -> kid; "teen" -> teen; else -> pro }
        return when (trigger) {
            GuideTrigger.Greet -> pick(R.string.terra_greet_kid, R.string.terra_greet_teen, R.string.terra_greet_pro)
            GuideTrigger.Success -> pick(R.string.terra_success_kid, R.string.terra_success_teen, R.string.terra_success_pro)
            GuideTrigger.Error -> pick(R.string.terra_error_kid, R.string.terra_error_teen, R.string.terra_error_pro)
            GuideTrigger.Hint -> pick(R.string.terra_hint_kid, R.string.terra_hint_teen, R.string.terra_hint_pro)
            GuideTrigger.Offline -> pick(R.string.terra_offline_kid, R.string.terra_offline_pro, R.string.terra_offline_pro)
            GuideTrigger.Streak -> pick(R.string.terra_streak_kid, R.string.terra_streak_pro, R.string.terra_streak_pro)
            GuideTrigger.Locked -> pick(R.string.terra_locked_kid, R.string.terra_locked_pro, R.string.terra_locked_pro)
            GuideTrigger.Reward -> pick(R.string.terra_reward_kid, R.string.terra_reward_pro, R.string.terra_reward_pro)
            GuideTrigger.Thinking -> pick(R.string.terra_hint_kid, R.string.terra_hint_teen, R.string.terra_hint_pro)
        }
    }

    @Composable
    fun line(trigger: GuideTrigger): String {
        val config = LocalAgeConfig.current
        return stringResource(lineRes(trigger, config.toneBucket))
    }
}
