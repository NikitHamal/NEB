package com.neb.ians.data.news

data class NewsDetail(
    val announcement: NewsAnnouncement,
    val content: String = "",
    val externalUrl: String = "",
    val related: List<NewsAnnouncement> = emptyList()
)
