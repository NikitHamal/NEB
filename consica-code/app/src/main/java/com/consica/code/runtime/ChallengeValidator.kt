package com.consica.code.runtime

import com.consica.code.core.model.ChallengeCheck
import com.consica.code.core.model.CodeChallenge
import com.consica.code.core.model.CodeLanguage
import com.consica.code.core.model.RunResult
import com.consica.code.runtime.html.HtmlSupport
import com.consica.code.runtime.python.MiniPython

/** Runs code and evaluates the declarative checks of a [CodeChallenge]. */
object ChallengeValidator {

    data class Outcome(
        val runResult: RunResult,
        val passed: Boolean,
    )

    fun execute(language: CodeLanguage, code: String): RunResult = when (language) {
        CodeLanguage.PYTHON -> {
            val result = MiniPython.run(code)
            RunResult(
                success = result.success,
                output = result.output,
                errorLine = result.error?.line,
                friendlyError = result.error?.let { friendlyPythonError(it) },
                technicalError = result.error?.describe(),
            )
        }
        CodeLanguage.HTML -> {
            val unclosed = HtmlSupport.findUnclosedTags(code)
            if (unclosed.isEmpty()) {
                RunResult(success = true, output = code)
            } else {
                RunResult(
                    success = true, // preview still renders; lint is advisory
                    output = code,
                    friendlyError = null,
                    technicalError = "Unclosed tags: ${unclosed.joinToString(", ") { "<$it>" }}",
                )
            }
        }
    }

    fun validate(challenge: CodeChallenge, code: String, runResult: RunResult): Outcome {
        val passed = challenge.checks.all { check ->
            when (check) {
                is ChallengeCheck.OutputContains ->
                    runResult.success && runResult.output.contains(check.needle, ignoreCase = check.ignoreCase)
                is ChallengeCheck.HtmlHasTag -> HtmlSupport.hasTag(code, check.tag, check.content)
                is ChallengeCheck.CodeContains -> code.contains(check.needle, ignoreCase = check.ignoreCase)
                is ChallengeCheck.RunsCleanly -> runResult.success
            }
        }
        return Outcome(runResult, passed)
    }

    /** Maps interpreter errors to beginner-friendly, localizable hints (English fallback). */
    private fun friendlyPythonError(error: MiniPython.PyError): String = when (error.kind) {
        "NameError" -> "Python doesn't know that name yet. Check the spelling, or create the variable before using it."
        "SyntaxError" -> "Something about the code shape confused Python. Check brackets, quotes and colons."
        "IndentationError" -> "The spaces at the start of a line matter! Lines inside if/for/def need to be indented."
        "TypeError" -> "Two things that don't mix were combined — like adding words and numbers. Try str() to convert."
        "ZeroDivisionError" -> "Dividing by zero isn't allowed — not even for computers!"
        "IndexError" -> "You reached past the end of the list. Remember positions start at 0."
        "ValueError" -> "That value couldn't be converted. Check what you're passing in."
        "TimeoutError" -> "The program ran for too long — there might be a loop that never ends."
        "OutputLimitError" -> "The program printed too much! Try printing fewer things."
        else -> "Something unexpected happened. Read the technical details and try again."
    }
}
