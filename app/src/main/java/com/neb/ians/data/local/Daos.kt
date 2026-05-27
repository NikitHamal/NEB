package com.neb.ians.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import kotlinx.coroutines.flow.Flow

@Dao
interface ResourceDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(items: List<ResourceEntity>): List<Long>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(item: ResourceEntity): Long

    @Update
    suspend fun update(item: ResourceEntity)

    @Query("SELECT * FROM resources WHERE id = :id")
    fun observe(id: Long): Flow<ResourceEntity?>

    @Query("SELECT * FROM resources WHERE id = :id LIMIT 1")
    suspend fun get(id: Long): ResourceEntity?

    @Query("SELECT COUNT(*) FROM resources")
    suspend fun count(): Int

    @Query("""
        SELECT * FROM resources
        WHERE (:query = '' OR title LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%' OR author LIKE '%' || :query || '%')
          AND (:subject IS NULL OR subject = :subject)
          AND (:grade IS NULL OR grade = :grade)
          AND (:type IS NULL OR type = :type)
        ORDER BY lastOpenedAt DESC, title ASC
    """)
    fun search(
        query: String,
        subject: Subject?,
        grade: Grade?,
        type: ResourceType?,
    ): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources ORDER BY lastOpenedAt DESC LIMIT :limit")
    fun recent(limit: Int = 8): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE isFavorite = 1 ORDER BY title ASC")
    fun favorites(): Flow<List<ResourceEntity>>

    @Query("UPDATE resources SET isFavorite = :fav WHERE id = :id")
    suspend fun setFavorite(id: Long, fav: Boolean)

    @Query("UPDATE resources SET lastOpenedAt = :ts WHERE id = :id")
    suspend fun touch(id: Long, ts: Long = System.currentTimeMillis())
}

@Dao
interface AnnotationDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: AnnotationEntity): Long

    @Update
    suspend fun update(item: AnnotationEntity)

    @Delete
    suspend fun delete(item: AnnotationEntity)

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId ORDER BY page ASC, createdAt ASC")
    fun forResource(resourceId: Long): Flow<List<AnnotationEntity>>

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId AND page = :page ORDER BY createdAt ASC")
    fun forPage(resourceId: Long, page: Int): Flow<List<AnnotationEntity>>

    @Query("DELETE FROM annotations WHERE id = :id")
    suspend fun deleteById(id: Long)
}

@Dao
interface ForumDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertThread(t: ForumThreadEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertReply(r: ForumReplyEntity): Long

    @Query("SELECT * FROM forum_threads ORDER BY createdAt DESC")
    fun threads(): Flow<List<ForumThreadEntity>>

    @Query("SELECT * FROM forum_threads WHERE id = :id")
    fun thread(id: Long): Flow<ForumThreadEntity?>

    @Query("SELECT * FROM forum_replies WHERE threadId = :id ORDER BY createdAt ASC")
    fun replies(id: Long): Flow<List<ForumReplyEntity>>

    @Query("UPDATE forum_threads SET likes = likes + :delta WHERE id = :id")
    suspend fun likeThread(id: Long, delta: Int = 1)

    @Query("UPDATE forum_replies SET likes = likes + :delta WHERE id = :id")
    suspend fun likeReply(id: Long, delta: Int = 1)

    @Query("UPDATE forum_threads SET replyCount = replyCount + 1 WHERE id = :id")
    suspend fun incrementReply(id: Long)

    @Query("SELECT COUNT(*) FROM forum_threads")
    suspend fun count(): Int
}
