package com.consica.code.domain.runner

/** A single diagnostic from a run. [line] is 1-based when known. */
data class RunError(val line: Int?, val message: String)

data class RunResult(
    val output: String,
    val errors: List<RunError>,
    val success: Boolean,
) {
    val hasErrors: Boolean get() = errors.isNotEmpty()

    companion object {
        fun ok(output: String) = RunResult(output, emptyList(), true)
        fun fail(message: String, line: Int? = null, partialOutput: String = "") =
            RunResult(partialOutput, listOf(RunError(line, message)), false)
    }
}

/**
 * Executes code for one language, fully offline.
 *
 * HTML "execution" is rendering, handled by the UI WebView ([com.consica.code.ui.playground]),
 * so there is only a Python implementation here. The interface intentionally mirrors what a
 * Pyodide-in-WebView engine would expose, so a bundled-Pyodide runner can replace [MiniPython]
 * later without changing callers.
 */
interface CodeRunner {
    fun run(code: String): RunResult
}
