package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ForumDao {

    @Query("SELECT * FROM forum_posts ORDER BY createdAt DESC")
    fun getAllPosts(): Flow<List<ForumPostEntity>>

    @Query("SELECT * FROM forum_posts WHERE id = :id")
    suspend fun getPostById(id: Long): ForumPostEntity?

    @Query("""
        SELECT * FROM forum_posts
        WHERE title LIKE '%' || :query || '%'
        OR body LIKE '%' || :query || '%'
        ORDER BY createdAt DESC
    """)
    fun searchPosts(query: String): Flow<List<ForumPostEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPost(post: ForumPostEntity): Long

    @Update
    suspend fun updatePost(post: ForumPostEntity)

    @Delete
    suspend fun deletePost(post: ForumPostEntity)

    @Query("SELECT * FROM forum_replies WHERE postId = :postId ORDER BY createdAt ASC")
    fun getRepliesForPost(postId: Long): Flow<List<ForumReplyEntity>>

    @Query("SELECT * FROM forum_replies WHERE id = :id")
    suspend fun getReplyById(id: Long): ForumReplyEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertReply(reply: ForumReplyEntity): Long

    @Update
    suspend fun updateReply(reply: ForumReplyEntity)

    @Delete
    suspend fun deleteReply(reply: ForumReplyEntity)
}
