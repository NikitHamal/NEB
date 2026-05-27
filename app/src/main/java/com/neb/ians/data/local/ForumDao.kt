package com.neb.ians.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import com.neb.ians.data.model.ForumPost
import com.neb.ians.data.model.Reply
import kotlinx.coroutines.flow.Flow

@Dao
interface ForumDao {
    @Query("SELECT * FROM forum_posts ORDER BY createdAt DESC")
    fun getPosts(): Flow<List<ForumPost>>

    @Query("SELECT * FROM forum_posts WHERE id = :postId")
    suspend fun getPostById(postId: Long): ForumPost?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPost(post: ForumPost): Long

    @Query("UPDATE forum_posts SET answerCount = answerCount + 1 WHERE id = :postId")
    suspend fun incrementAnswerCount(postId: Long)

    @Query("UPDATE forum_posts SET thumbCount = thumbCount + 1 WHERE id = :postId")
    suspend fun incrementThumbCount(postId: Long)

    @Delete
    suspend fun deletePost(post: ForumPost)

    @Query("SELECT * FROM replies WHERE postId = :postId ORDER BY createdAt ASC")
    fun getReplies(postId: Long): Flow<List<Reply>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertReply(reply: Reply): Long

    @Query("UPDATE replies SET thumbCount = thumbCount + 1 WHERE id = :replyId")
    suspend fun incrementReplyThumb(replyId: Long)

    @Delete
    suspend fun deleteReply(reply: Reply)

    @Transaction
    suspend fun addReplyAndUpdateCount(reply: Reply) {
        insertReply(reply)
        incrementAnswerCount(reply.postId)
    }
}
