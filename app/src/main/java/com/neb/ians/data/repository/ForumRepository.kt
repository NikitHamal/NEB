package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.ForumDao
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ForumRepository @Inject constructor(
    private val forumDao: ForumDao,
    private val apiService: com.neb.ians.data.api.ApiService,
    private val authRepository: AuthRepository
) {
    private suspend fun getBearerToken(): String? {
        return authRepository.tokenFlow.first()?.let { "Bearer $it" }
    }

    suspend fun syncPosts() {
        try {
            val bearer = getBearerToken()
            val apiPosts = apiService.getPosts(bearer)
            val entities = apiPosts.map { p ->
                ForumPostEntity(
                    id = p.id,
                    title = p.title,
                    content = p.content,
                    authorName = p.authorName,
                    authorId = p.authorId,
                    category = p.category,
                    thumbsUpCount = p.thumbsUpCount,
                    replyCount = p.replyCount,
                    createdAt = p.createdAt,
                    updatedAt = p.updatedAt,
                    isThumbedUp = p.isThumbedUp
                )
            }
            // Clear current post cache and save latest synced posts
            entities.forEach { forumDao.insertPost(it) }
        } catch (e: Exception) {
            // Offline fallback
        }
    }

    suspend fun syncRepliesForPost(postId: String) {
        try {
            val bearer = getBearerToken()
            val apiReplies = apiService.getReplies(bearer, postId)
            val entities = apiReplies.map { r ->
                ForumReplyEntity(
                    id = r.id,
                    postId = r.postId,
                    parentReplyId = r.parentReplyId,
                    content = r.content,
                    authorName = r.authorName,
                    authorId = r.authorId,
                    thumbsUpCount = r.thumbsUpCount,
                    createdAt = r.createdAt,
                    isThumbedUp = r.isThumbedUp
                )
            }
            entities.forEach { forumDao.insertReply(it) }
        } catch (e: Exception) {
            // Offline fallback
        }
    }

    fun getAllPosts(): Flow<List<ForumPostEntity>> = forumDao.getAllPosts()

    fun getPostById(id: String): Flow<ForumPostEntity?> = forumDao.getPostById(id)

    fun getPostsByCategory(category: String): Flow<List<ForumPostEntity>> = forumDao.getPostsByCategory(category)

    fun searchPosts(query: String): Flow<List<ForumPostEntity>> = forumDao.searchPosts("%$query%")

    fun getRepliesForPost(postId: String): Flow<List<ForumReplyEntity>> = forumDao.getRepliesForPost(postId)

    suspend fun createPost(title: String, content: String, authorName: String, category: String): ForumPostEntity {
        val bearer = getBearerToken() ?: throw IllegalStateException("User not authenticated")
        val apiPost = apiService.createPost(bearer, com.neb.ians.data.api.ApiPostCreateRequest(title, content, category))
        
        val post = ForumPostEntity(
            id = apiPost.id,
            title = apiPost.title,
            content = apiPost.content,
            authorName = apiPost.authorName,
            authorId = apiPost.authorId,
            category = apiPost.category,
            thumbsUpCount = apiPost.thumbsUpCount,
            replyCount = apiPost.replyCount,
            createdAt = apiPost.createdAt,
            updatedAt = apiPost.updatedAt,
            isThumbedUp = apiPost.isThumbedUp
        )
        forumDao.insertPost(post)
        return post
    }

    suspend fun createReply(postId: String, content: String, authorName: String, parentReplyId: String? = null): ForumReplyEntity {
        val bearer = getBearerToken() ?: throw IllegalStateException("User not authenticated")
        val apiReply = apiService.createReply(bearer, postId, com.neb.ians.data.api.ApiReplyCreateRequest(content, parentReplyId))
        
        val reply = ForumReplyEntity(
            id = apiReply.id,
            postId = apiReply.postId,
            parentReplyId = apiReply.parentReplyId,
            content = apiReply.content,
            authorName = apiReply.authorName,
            authorId = apiReply.authorId,
            thumbsUpCount = apiReply.thumbsUpCount,
            createdAt = apiReply.createdAt,
            isThumbedUp = apiReply.isThumbedUp
        )
        forumDao.insertReply(reply)
        
        // Sync post local reply count
        val post = forumDao.getPostByIdSync(postId)
        if (post != null) {
            forumDao.updateReplyCount(postId, post.replyCount + 1)
        }
        return reply
    }

    suspend fun toggleThumbsUp(postId: String) {
        val bearer = getBearerToken() ?: return
        try {
            val response = apiService.toggleLikePost(bearer, postId)
            forumDao.updateThumbsUp(postId, response.thumbsUpCount, response.isThumbedUp)
        } catch (e: Exception) {
            // Offline local fallback or fail silently
        }
    }

    suspend fun toggleReplyThumbsUp(replyId: String) {
        val bearer = getBearerToken() ?: return
        try {
            val response = apiService.toggleLikeReply(bearer, replyId)
            forumDao.updateReplyThumbsUp(replyId, response.thumbsUpCount, response.isThumbedUp)
        } catch (e: Exception) {
            // Offline local fallback or fail silently
        }
    }

    suspend fun deletePost(id: String) {
        val bearer = getBearerToken() ?: return
        try {
            apiService.deletePost(bearer, id)
            forumDao.deletePost(id)
        } catch (e: Exception) {
            // Offline local delete or fail
        }
    }

    suspend fun deleteReply(id: String) = forumDao.deleteReply(id)
}
