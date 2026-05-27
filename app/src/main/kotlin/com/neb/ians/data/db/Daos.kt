package com.neb.ians.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface ResourceDao {
    @Query("SELECT * FROM resources ORDER BY updatedAt DESC")
    fun observeAll(): Flow<List<ResourceEntity>>

    @Query("""
        SELECT * FROM resources
        WHERE (:query = '' OR title LIKE '%' || :query || '%' OR author LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%')
          AND (:subject IS NULL OR subject = :subject)
          AND (:grade IS NULL OR grade = :grade)
          AND (:type IS NULL OR type = :type)
        ORDER BY isFavorite DESC, updatedAt DESC
    """)
    fun search(query: String, subject: String?, grade: String?, type: String?): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE id = :id")
    suspend fun getById(id: String): ResourceEntity?

    @Query("SELECT * FROM resources WHERE id = :id")
    fun observeById(id: String): Flow<ResourceEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(items: List<ResourceEntity>)

    @Update
    suspend fun update(item: ResourceEntity)

    @Query("UPDATE resources SET isFavorite = :fav WHERE id = :id")
    suspend fun setFavorite(id: String, fav: Boolean)

    @Query("UPDATE resources SET localPath = :path, downloadedAt = :ts WHERE id = :id")
    suspend fun markDownloaded(id: String, path: String, ts: Long)
}

@Dao
interface AnnotationDao {
    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId ORDER BY page, createdAt")
    fun observeForResource(resourceId: String): Flow<List<AnnotationEntity>>

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId AND page = :page")
    suspend fun pageAnnotations(resourceId: String, page: Int): List<AnnotationEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(a: AnnotationEntity): Long

    @Query("DELETE FROM annotations WHERE id = :id")
    suspend fun delete(id: Long)

    @Query("DELETE FROM annotations WHERE resourceId = :resourceId")
    suspend fun deleteForResource(resourceId: String)
}

@Dao
interface ForumDao {
    @Query("SELECT * FROM threads ORDER BY createdAt DESC")
    fun observeThreads(): Flow<List<ThreadEntity>>

    @Query("SELECT * FROM threads WHERE id = :id")
    fun observeThread(id: String): Flow<ThreadEntity?>

    @Query("SELECT * FROM threads WHERE id = :id")
    suspend fun getThread(id: String): ThreadEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertThread(t: ThreadEntity)

    @Query("UPDATE threads SET thumbed = :on, thumbCount = thumbCount + :delta WHERE id = :id")
    suspend fun setThreadThumb(id: String, on: Boolean, delta: Int)

    @Query("UPDATE threads SET replyCount = replyCount + 1 WHERE id = :id")
    suspend fun incrementReplyCount(id: String)

    @Query("SELECT * FROM posts WHERE threadId = :threadId ORDER BY createdAt ASC")
    fun observePosts(threadId: String): Flow<List<PostEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertPost(p: PostEntity)

    @Query("UPDATE posts SET thumbed = :on, thumbCount = thumbCount + :delta WHERE id = :id")
    suspend fun setPostThumb(id: String, on: Boolean, delta: Int)
}
