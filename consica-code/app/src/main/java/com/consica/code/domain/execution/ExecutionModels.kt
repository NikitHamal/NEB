package com.consica.code.domain.execution

/** Categories used to map technical errors to friendly, localizable explanations. */
enum class FriendlyErrorKind {
    SYNTAX, NAME, TYPE, VALUE, INDEX, DIVISION_BY_ZERO, RUNTIME, TIMEOUT
}

data class ExecutionError(
    /** Technical message shown to older learners (e.g. "NameError: name 'x' is not defined"). */
    val message: String,
    val line: Int? = null,
    val kind: FriendlyErrorKind = FriendlyErrorKind.RUNTIME,
)

data class ExecutionResult(
    val output: String,
    val error: ExecutionError? = null,
    val durationMs: Long = 0,
) {
    val isSuccess: Boolean get() = error == null
}
