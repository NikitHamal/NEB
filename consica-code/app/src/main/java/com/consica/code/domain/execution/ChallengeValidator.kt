package com.consica.code.domain.execution

import com.consica.code.domain.model.ChallengeValidation

/**
 * Evaluates lesson challenge validation rules against the learner's code and
 * the output produced by running it.
 */
object ChallengeValidator {

    fun validate(rule: ChallengeValidation, code: String, output: String): Boolean = when (rule) {
        is ChallengeValidation.OutputContains ->
            rule.needles.all { output.contains(it, ignoreCase = rule.ignoreCase) }

        is ChallengeValidation.CodeMatches ->
            Regex(rule.pattern, setOf(RegexOption.IGNORE_CASE, RegexOption.DOT_MATCHES_ALL))
                .containsMatchIn(code)

        is ChallengeValidation.HtmlHasTag -> {
            val tagRegex = Regex(
                "<${Regex.escape(rule.tag)}(\\s[^>]*)?>(.*?)</${Regex.escape(rule.tag)}>",
                setOf(RegexOption.IGNORE_CASE, RegexOption.DOT_MATCHES_ALL)
            )
            val match = tagRegex.find(code)
            when {
                match == null -> false
                rule.textContains == null -> true
                else -> match.groupValues[2].contains(rule.textContains, ignoreCase = true)
            }
        }

        is ChallengeValidation.All -> rule.rules.all { validate(it, code, output) }

        is ChallengeValidation.AnyOf -> rule.rules.any { validate(it, code, output) }
    }
}
