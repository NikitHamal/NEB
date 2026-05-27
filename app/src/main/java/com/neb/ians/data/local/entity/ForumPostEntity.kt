package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "forum_posts")
data class ForumPostEntity(
    @PrimaryKey val id: String,
    val title: String,
    val content: String,
    val authorName: String,
    val authorId: String,
    val category: String,
    val thumbsUpCount: Int = 0,
    val replyCount: Int = 0,
    val createdAt: Long,
    val updatedAt: Long,
    val isThumbedUp: Boolean = false
)
