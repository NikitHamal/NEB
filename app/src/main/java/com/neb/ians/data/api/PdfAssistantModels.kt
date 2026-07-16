package com.neb.ians.data.api

import kotlinx.serialization.Serializable

@Serializable
data class PdfAssistantHistoryItem(
    val role: String,
    val content: String
)

@Serializable
data class PdfAssistantRequest(
    val prompt: String,
    val history: List<PdfAssistantHistoryItem> = emptyList()
)

@Serializable
data class PdfAssistantResponse(
    val answer: String = "",
    val error: String? = null,
    val resourceId: String = "",
    val title: String = ""
)
