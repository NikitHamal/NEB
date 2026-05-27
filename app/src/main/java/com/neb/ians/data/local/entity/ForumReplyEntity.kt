package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "forum_replies")
data class ForumReplyEntity(
    @PrimaryKey val id: String,
    val postId: String,
    val parentReplyId: String? = null,  // null for top-level replies
    val content: String,
    val authorName: String,
    val authorId: String,
    val thumbsUpCount: Int = 0,
    val createdAt: Long,
    val isThumbedUp: Boolean = false
)
