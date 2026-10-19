package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ApiSyllabusStudyMeta(
    val language: String = "en",
    val topics: List<String> = emptyList(),
    val hours: Int? = null,
    val summary: String = "",
    @SerialName("source_url") val sourceUrl: String = "",
    @SerialName("self_checks") val selfChecks: List<ApiSyllabusSelfCheck> = emptyList()
)

@Serializable
data class ApiSyllabusSelfCheck(
    val question: String = "",
    val answer: String = ""
)
