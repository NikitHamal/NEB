package com.neb.ians.data.repo

import com.neb.ians.data.db.ForumDao
import com.neb.ians.data.db.PostEntity
import com.neb.ians.data.db.ThreadEntity
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ForumRepository @Inject constructor(
    private val forumDao: ForumDao,
) {
    suspend fun seedIfEmpty() {
        if (forumDao.observeThreads().first().isNotEmpty()) return
        listOf(
            ThreadEntity(
                id = "welcome",
                title = "Welcome to the NEBians forum",
                body = "Be kind, stay on-topic and help each other prepare for the boards.",
                author = "NEBians Team",
                subject = null,
                grade = null,
            ),
            ThreadEntity(
                id = "phy-doubt",
                title = "Doubt: Rotational dynamics — Chapter 8",
                body = "Stuck on the moment of inertia derivation for a thin disc. Anyone help?",
                author = "rina",
                subject = "PHYSICS",
                grade = "GRADE_11",
            ),
        ).forEach { forumDao.upsertThread(it) }
    }

    fun threads(): Flow<List<ThreadEntity>> = forumDao.observeThreads()
    fun thread(id: String): Flow<ThreadEntity?> = forumDao.observeThread(id)
    fun posts(threadId: String): Flow<List<PostEntity>> = forumDao.observePosts(threadId)

    suspend fun createThread(title: String, body: String, author: String, subject: String?, grade: String?): String {
        val id = UUID.randomUUID().toString()
        forumDao.upsertThread(
            ThreadEntity(id = id, title = title, body = body, author = author, subject = subject, grade = grade)
        )
        return id
    }

    suspend fun reply(threadId: String, body: String, author: String, parentId: String? = null) {
        val id = UUID.randomUUID().toString()
        forumDao.upsertPost(
            PostEntity(id = id, threadId = threadId, parentId = parentId, body = body, author = author)
        )
        forumDao.incrementReplyCount(threadId)
    }

    suspend fun toggleThreadThumb(id: String) {
        val t = forumDao.getThread(id) ?: return
        val on = !t.thumbed
        forumDao.setThreadThumb(id, on, if (on) 1 else -1)
    }

    suspend fun togglePostThumb(post: PostEntity) {
        val on = !post.thumbed
        forumDao.setPostThumb(post.id, on, if (on) 1 else -1)
    }
}
