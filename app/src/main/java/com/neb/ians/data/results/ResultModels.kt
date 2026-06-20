package com.neb.ians.data.results

import com.neb.ians.data.api.ResultPayload

data class BulkResultRow(
    val symbol: String,
    val name: String = "—",
    val gpa: String = "—",
    val grade: String = "—",
    val status: String = "Pending",
    val success: Boolean = false,
    val error: String? = null
)

data class ResultLookup(
    val payload: ResultPayload,
    val cached: Boolean
)

enum class ResultExam(val label: String, val iconLabel: String) {
    Class12("12", "school"),
    Class10("10", "auto_stories")
}

enum class ResultMode { Single, Bulk }

enum class ResultExamType { Regular, ReExam }
