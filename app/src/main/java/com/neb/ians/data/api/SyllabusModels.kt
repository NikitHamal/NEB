package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ApiSyllabusIndex(
    val grades: List<ApiSyllabusGrade> = emptyList(),
    val totals: ApiSyllabusTotals = ApiSyllabusTotals()
)

@Serializable
data class ApiSyllabusTotals(
    val grades: Int = 0,
    val subjects: Int = 0,
    val units: Int = 0,
    val topics: Int = 0
)

@Serializable
data class ApiSyllabusGrade(
    val grade: String = "",
    val label: String = "",
    @SerialName("label_ne") val labelNe: String = "",
    val exam: String = "",
    val subjects: List<ApiSyllabusSubjectCard> = emptyList()
)

@Serializable
data class ApiSyllabusSubjectCard(
    val subject: String = "",
    val name: String = "",
    @SerialName("name_ne") val nameNe: String = "",
    val icon: String = "",
    val group: String = "",
    val lang: String = "en",
    val hours: Int? = null,
    @SerialName("unit_count") val unitCount: Int = 0,
    @SerialName("topic_count") val topicCount: Int = 0
)

@Serializable
data class ApiSyllabusDoc(
    val grade: String = "",
    @SerialName("grade_label") val gradeLabel: String = "",
    @SerialName("grade_label_ne") val gradeLabelNe: String = "",
    val subject: String = "",
    val name: String = "",
    @SerialName("name_ne") val nameNe: String = "",
    val icon: String = "",
    val lang: String = "en",
    val code: String = "",
    val hours: Int? = null,
    val exam: String = "",
    val areas: List<String> = emptyList(),
    val units: List<ApiSyllabusUnit> = emptyList(),
    @SerialName("unit_count") val unitCount: Int = 0,
    @SerialName("topic_count") val topicCount: Int = 0
)

@Serializable
data class ApiSyllabusUnit(
    val no: Int = 0,
    val title: String = "",
    val hours: Int? = null,
    val area: String = "",
    val topics: List<String> = emptyList(),
    val sections: List<ApiSyllabusBookSection> = emptyList(),
    val summary: List<String> = emptyList(),
    val terms: List<String> = emptyList()
)

@Serializable
data class ApiSyllabusBookSection(
    val no: String = "",
    val title: String = ""
)

@Serializable
data class ApiSyllabusSearch(
    val q: String = "",
    val results: List<ApiSyllabusHit> = emptyList(),
    val total: Int = 0
)

@Serializable
data class ApiSyllabusHit(
    val grade: String = "",
    val subject: String = "",
    val name: String = "",
    val unit: Int = 0,
    val title: String = "",
    val match: String = ""
)
