package com.neb.ians.data.api

import kotlinx.serialization.Serializable

// Portfolio entries: education, experience, projects, achievements, certificates, volunteering.

@Serializable
data class ApiEntry(
    val id: Int = 0,
    val kind: String = "",
    val title: String = "",
    val org: String = "",
    val start: String = "",
    val end: String = "",
    val isCurrent: Boolean = false,
    val description: String = "",
    val url: String = ""
)

@Serializable
data class ApiEntrySection(
    val value: String = "",
    val label: String = "",
    val icon: String = "",
    val items: List<ApiEntry> = emptyList()
)

@Serializable
data class ApiPortfolio(val sections: List<ApiEntrySection> = emptyList())

@Serializable
data class ApiEntryBody(
    val kind: String,
    val title: String,
    val org: String = "",
    val start: String = "",
    val end: String = "",
    val isCurrent: Boolean = false,
    val description: String = "",
    val url: String = ""
)

@Serializable
data class ApiEntrySaved(val status: String = "", val error: String? = null, val entry: ApiEntry? = null)
