package com.neb.ians.data

data class CommunityAnswer(
    val id: String,
    val author: String,
    val body: String,
    val createdAt: String,
    val thumbs: Int
)

data class CommunityThread(
    val id: String,
    val title: String,
    val body: String,
    val subject: Subject,
    val author: String,
    val createdAt: String,
    val thumbs: Int,
    val answers: List<CommunityAnswer>
)
