package com.neb.ians.data.news

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/** Payload of GET /api/news/ items and GET /api/news/{slug}/. */
@Serializable
data class ApiAnnouncement(
    val id: Long = 0,
    val title: String = "",
    val slug: String = "",
    val summary: String = "",
    val category: String = "general",
    @SerialName("category_icon") val categoryIcon: String = "info",
    @SerialName("category_label") val categoryLabel: String = "General",
    @SerialName("category_color") val categoryColor: String = "#6b7280",
    @SerialName("is_pinned") val isPinned: Boolean = false,
    @SerialName("cover_image_url") val coverImageUrl: String = "",
    @SerialName("external_url") val externalUrl: String = "",
    val tags: String? = null,
    @SerialName("author_name") val authorName: String = "NEBians Team",
    @SerialName("author_photo") val authorPhoto: String = "",
    @SerialName("published_at") val publishedAt: Long = 0,
    @SerialName("created_at") val createdAt: Long = 0,
    @SerialName("view_count") val viewCount: Int = 0,
    val content: String? = null,
    @SerialName("content_html") val contentHtml: String? = null,
)

@Serializable
data class NewsListResponse(
    val ok: Boolean = false,
    val items: List<ApiAnnouncement> = emptyList(),
    val page: Int = 1,
    @SerialName("has_more") val hasMore: Boolean = false,
    val error: String? = null,
)

@Serializable
data class NewsDetailResponse(
    val ok: Boolean = false,
    val item: ApiAnnouncement? = null,
    val related: List<ApiAnnouncement> = emptyList(),
    val error: String? = null,
)

@Serializable
data class NewsViewTrackResponse(
    val ok: Boolean = false,
    val counted: Boolean = false,
    val error: String? = null,
)
