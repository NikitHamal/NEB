package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.ForumDao
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import kotlinx.coroutines.flow.Flow
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ForumRepository @Inject constructor(
    private val forumDao: ForumDao
) {
    fun getAllPosts(): Flow<List<ForumPostEntity>> = forumDao.getAllPosts()

    fun getPostById(id: String): Flow<ForumPostEntity?> = forumDao.getPostById(id)

    fun getPostsByCategory(category: String): Flow<List<ForumPostEntity>> = forumDao.getPostsByCategory(category)

    fun searchPosts(query: String): Flow<List<ForumPostEntity>> = forumDao.searchPosts("%$query%")

    fun getRepliesForPost(postId: String): Flow<List<ForumReplyEntity>> = forumDao.getRepliesForPost(postId)

    suspend fun createPost(title: String, content: String, authorName: String, category: String): ForumPostEntity {
        val post = ForumPostEntity(
            id = UUID.randomUUID().toString(),
            title = title,
            content = content,
            authorName = authorName,
            authorId = "local_user",
            category = category,
            createdAt = System.currentTimeMillis(),
            updatedAt = System.currentTimeMillis()
        )
        forumDao.insertPost(post)
        return post
    }

    suspend fun createReply(postId: String, content: String, authorName: String, parentReplyId: String? = null): ForumReplyEntity {
        val reply = ForumReplyEntity(
            id = UUID.randomUUID().toString(),
            postId = postId,
            parentReplyId = parentReplyId,
            content = content,
            authorName = authorName,
            authorId = "local_user",
            createdAt = System.currentTimeMillis()
        )
        forumDao.insertReply(reply)
        val post = forumDao.getPostByIdSync(postId)
        if (post != null) {
            forumDao.updateReplyCount(postId, post.replyCount + 1)
        }
        return reply
    }

    suspend fun toggleThumbsUp(postId: String) {
        val post = forumDao.getPostByIdSync(postId) ?: return
        val newIsThumbedUp = !post.isThumbedUp
        val newCount = if (newIsThumbedUp) post.thumbsUpCount + 1 else post.thumbsUpCount - 1
        forumDao.updateThumbsUp(postId, newCount, newIsThumbedUp)
    }

    suspend fun toggleReplyThumbsUp(replyId: String) {
        val reply = forumDao.getReplyByIdSync(replyId) ?: return
        val newIsThumbedUp = !reply.isThumbedUp
        val newCount = if (newIsThumbedUp) reply.thumbsUpCount + 1 else reply.thumbsUpCount - 1
        forumDao.updateReplyThumbsUp(replyId, newCount, newIsThumbedUp)
    }

    suspend fun deletePost(id: String) = forumDao.deletePost(id)

    suspend fun deleteReply(id: String) = forumDao.deleteReply(id)
}
