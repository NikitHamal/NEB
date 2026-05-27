package com.neb.ians.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "forum_posts")
data class ForumPost(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val title: String,
    val body: String,
    val author: String,
    val subjectTag: String? = null,
    val answerCount: Int = 0,
    val thumbCount: Int = 0,
    val createdAt: Long = System.currentTimeMillis()
)
