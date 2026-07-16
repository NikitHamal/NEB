package com.neb.ians.data.news

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class NewsComment(
    val id: String,
    @SerialName("author_name") val authorName: String = "NEBian",
    @SerialName("author_initials") val authorInitials: String = "N",
    @SerialName("author_photo") val authorPhoto: String = "",
    val text: String = "",
    @SerialName("created_at") val createdAt: Long = 0
)

@Serializable
data class NewsCommentsResponse(
    val ok: Boolean = false,
    val comments: List<NewsComment> = emptyList(),
    val error: String? = null
)

@Serializable
data class NewsCommentRequest(
    val slug: String,
    val text: String
)

@Serializable
data class NewsCommentResponse(
    val ok: Boolean = false,
    val comment: NewsComment? = null,
    val error: String? = null
)
