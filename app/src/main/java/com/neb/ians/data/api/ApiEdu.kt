package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

// The education catalogue: situations, levels with their programs and terms. One request, cached.

@Serializable
data class ApiEduStatus(
    val value: String = "",
    val label: String = "",
    val hint: String = "",
    @SerialName("ask_completed") val askCompleted: Boolean = false
)

@Serializable
data class ApiEduLevel(
    val value: String = "",
    val label: String = "",
    val programs: List<String> = emptyList(),
    @SerialName("program_label") val programLabel: String = "",
    val terms: String = "none"
)

@Serializable
data class ApiEduOption(val value: String = "", val label: String = "")

@Serializable
data class ApiEduCatalog(
    val statuses: List<ApiEduStatus> = emptyList(),
    val levels: List<ApiEduLevel> = emptyList(),
    val terms: Map<String, List<String>> = emptyMap(),
    val completed: List<ApiEduOption> = emptyList()
)
