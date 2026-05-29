package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ForumDao {

    @Query("SELECT * FROM forum_posts ORDER BY createdAt DESC")
    fun getAllPosts(): Flow<List<ForumPostEntity>>

    @Query("SELECT * FROM forum_posts WHERE id = :id")
    fun getPostById(id: String): Flow<ForumPostEntity?>

    @Query("SELECT * FROM forum_posts WHERE category = :category ORDER BY createdAt DESC")
    fun getPostsByCategory(category: String): Flow<List<ForumPostEntity>>

    @Query("SELECT * FROM forum_posts WHERE title LIKE '%' || :query || '%' OR content LIKE '%' || :query || '%' ORDER BY createdAt DESC")
    fun searchPosts(query: String): Flow<List<ForumPostEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPost(post: ForumPostEntity)

    @Query("UPDATE forum_posts SET thumbsUpCount = :count, isThumbedUp = :isThumbedUp WHERE id = :id")
    suspend fun updateThumbsUp(id: String, count: Int, isThumbedUp: Boolean)

    @Query("UPDATE forum_posts SET replyCount = :count WHERE id = :id")
    suspend fun updateReplyCount(id: String, count: Int)

    @Query("SELECT * FROM forum_posts WHERE id = :id")
    suspend fun getPostByIdSync(id: String): ForumPostEntity?

    @Query("DELETE FROM forum_posts WHERE id = :id")
    suspend fun deletePost(id: String)

    @Query("SELECT * FROM forum_replies WHERE postId = :postId ORDER BY createdAt ASC")
    fun getRepliesForPost(postId: String): Flow<List<ForumReplyEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertReply(reply: ForumReplyEntity)

    @Query("SELECT * FROM forum_replies WHERE id = :id")
    suspend fun getReplyByIdSync(id: String): ForumReplyEntity?

    @Query("DELETE FROM forum_replies WHERE id = :id")
    suspend fun deleteReply(id: String)

    @Query("UPDATE forum_replies SET thumbsUpCount = :count, isThumbedUp = :isThumbedUp WHERE id = :id")
    suspend fun updateReplyThumbsUp(id: String, count: Int, isThumbedUp: Boolean)

    @Query("DELETE FROM forum_posts WHERE id NOT IN (:ids)")
    suspend fun deletePostsExceptWithIds(ids: List<String>)

    @Query("DELETE FROM forum_posts")
    suspend fun deleteAllPosts()

    @Query("DELETE FROM forum_replies WHERE postId = :postId AND id NOT IN (:ids)")
    suspend fun deleteRepliesForPostExceptWithIds(postId: String, ids: List<String>)

    @Query("DELETE FROM forum_replies WHERE postId = :postId")
    suspend fun deleteAllRepliesForPost(postId: String)
}
