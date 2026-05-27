package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.ForumDao
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import kotlinx.coroutines.flow.Flow

class ForumRepository(private val forumDao: ForumDao) {

    fun getAllPosts(): Flow<List<ForumPostEntity>> = forumDao.getAllPosts()

    suspend fun getPostById(id: Long): ForumPostEntity? = forumDao.getPostById(id)

    fun searchPosts(query: String): Flow<List<ForumPostEntity>> = forumDao.searchPosts(query)

    suspend fun insertPost(post: ForumPostEntity): Long = forumDao.insertPost(post)

    suspend fun updatePost(post: ForumPostEntity) = forumDao.updatePost(post)

    fun getRepliesForPost(postId: Long): Flow<List<ForumReplyEntity>> =
        forumDao.getRepliesForPost(postId)

    suspend fun insertReply(reply: ForumReplyEntity): Long = forumDao.insertReply(reply)

    suspend fun updateReply(reply: ForumReplyEntity) = forumDao.updateReply(reply)

    suspend fun toggleThumbPost(postId: Long) {
        val post = forumDao.getPostById(postId) ?: return
        forumDao.updatePost(
            post.copy(
                isThumbedByUser = !post.isThumbedByUser,
                thumbsUp = if (post.isThumbedByUser) post.thumbsUp - 1 else post.thumbsUp + 1
            )
        )
    }

    suspend fun toggleThumbReply(replyId: Long) {
        val reply = forumDao.getReplyById(replyId) ?: return
        forumDao.updateReply(
            reply.copy(
                isThumbedByUser = !reply.isThumbedByUser,
                thumbsUp = if (reply.isThumbedByUser) reply.thumbsUp - 1 else reply.thumbsUp + 1
            )
        )
    }
}
