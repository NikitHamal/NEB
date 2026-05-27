package com.neb.ians.data.repository

import com.neb.ians.data.local.ForumDao
import com.neb.ians.data.model.ForumPost
import com.neb.ians.data.model.Reply
import kotlinx.coroutines.flow.Flow

class ForumRepository(private val dao: ForumDao) {
    fun getPosts(): Flow<List<ForumPost>> = dao.getPosts()
    suspend fun getPostById(id: Long): ForumPost? = dao.getPostById(id)
    suspend fun insertPost(post: ForumPost): Long = dao.insertPost(post)
    suspend fun deletePost(post: ForumPost) = dao.deletePost(post)
    suspend fun thumbPost(postId: Long) = dao.incrementThumbCount(postId)

    fun getReplies(postId: Long): Flow<List<Reply>> = dao.getReplies(postId)
    suspend fun insertReply(reply: Reply) = dao.addReplyAndUpdateCount(reply)
    suspend fun deleteReply(reply: Reply) = dao.deleteReply(reply)
    suspend fun thumbReply(replyId: Long) = dao.incrementReplyThumb(replyId)
}
