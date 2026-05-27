package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "forum_posts")
data class ForumPostEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val body: String,
    val authorName: String,
    val subject: String = "",
    val grade: String = "",
    val thumbsUp: Int = 0,
    val replyCount: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
    val isThumbedByUser: Boolean = false,
)

@Entity(tableName = "forum_replies")
data class ForumReplyEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val postId: Long,
    val parentReplyId: Long? = null,
    val body: String,
    val authorName: String,
    val thumbsUp: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
    val isThumbedByUser: Boolean = false,
)
