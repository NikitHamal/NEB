package com.neb.ians.data.repository

import com.neb.ians.data.db.ForumReplyDao
import com.neb.ians.data.db.ForumReplyEntity
import com.neb.ians.data.db.ForumThreadDao
import com.neb.ians.data.db.ForumThreadEntity
import com.neb.ians.data.model.ForumReply
import com.neb.ians.data.model.ForumThread
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.util.UUID

class ForumRepository(
    private val threadDao: ForumThreadDao,
    private val replyDao: ForumReplyDao
) {
    val allThreads: Flow<List<ForumThread>> = threadDao.getAll().map { list ->
        list.map { it.toModel() }
    }

    suspend fun createThread(title: String, body: String) {
        val thread = ForumThreadEntity(
            id = UUID.randomUUID().toString(),
            title = title,
            body = body
        )
        threadDao.insert(thread)
    }

    suspend fun getReplies(threadId: String): List<ForumReply> {
        return replyDao.getByThread(threadId).map { it.toModel() }
    }

    suspend fun addReply(threadId: String, body: String) {
        val reply = ForumReplyEntity(
            id = UUID.randomUUID().toString(),
            threadId = threadId,
            body = body
        )
        replyDao.insert(reply)
        threadDao.incrementReplies(threadId)
    }

    suspend fun likeThread(id: String) {
        threadDao.incrementLikes(id)
    }

    suspend fun likeReply(id: String) {
        replyDao.incrementLikes(id)
    }

    suspend fun seedSampleThreads() {
        val samples = listOf(
            ForumThreadEntity(
                id = "t1",
                title = "Tips for NEB Physics practical exam?",
                body = "I am really nervous about the practical exam next month. Any tips on common experiments and viva questions?",
                likes = 12,
                repliesCount = 3
            ),
            ForumThreadEntity(
                id = "t2",
                title = "Best notes for Organic Chemistry",
                body = "Can someone recommend concise and accurate notes for organic chemistry reactions?",
                likes = 8,
                repliesCount = 1
            ),
            ForumThreadEntity(
                id = "t3",
                title = "Grade 12 Math probability doubts",
                body = "Stuck on conditional probability problems. Can anyone explain with examples?",
                likes = 5,
                repliesCount = 2
            )
        )
        samples.forEach { threadDao.insert(it) }
    }

    private fun ForumThreadEntity.toModel() = ForumThread(
        id = id,
        title = title,
        body = body,
        authorName = authorName,
        likes = likes,
        repliesCount = repliesCount,
        createdAt = createdAt
    )

    private fun ForumReplyEntity.toModel() = ForumReply(
        id = id,
        threadId = threadId,
        body = body,
        authorName = authorName,
        likes = likes,
        createdAt = createdAt
    )
}
