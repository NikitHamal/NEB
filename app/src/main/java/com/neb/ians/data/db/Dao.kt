package com.neb.ians.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface ResourceDao {
    @Query("SELECT * FROM resources ORDER BY title ASC")
    fun getAll(): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE subject = :subject AND grade = :grade AND type = :type")
    suspend fun getByCategory(subject: String, grade: String, type: String): List<ResourceEntity>

    @Query("SELECT * FROM resources WHERE title LIKE '%' || :query || '%'")
    suspend fun search(query: String): List<ResourceEntity>

    @Query("SELECT * FROM resources WHERE isDownloaded = 1")
    fun getDownloaded(): Flow<List<ResourceEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(resources: List<ResourceEntity>)

    @Update
    suspend fun update(resource: ResourceEntity)

    @Query("DELETE FROM resources")
    suspend fun deleteAll()
}

@Dao
interface ForumThreadDao {
    @Query("SELECT * FROM forum_threads ORDER BY createdAt DESC")
    fun getAll(): Flow<List<ForumThreadEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(thread: ForumThreadEntity)

    @Query("UPDATE forum_threads SET likes = likes + 1 WHERE id = :id")
    suspend fun incrementLikes(id: String)

    @Query("UPDATE forum_threads SET repliesCount = repliesCount + 1 WHERE id = :id")
    suspend fun incrementReplies(id: String)

    @Query("DELETE FROM forum_threads WHERE id = :id")
    suspend fun delete(id: String)
}

@Dao
interface ForumReplyDao {
    @Query("SELECT * FROM forum_replies WHERE threadId = :threadId ORDER BY createdAt ASC")
    suspend fun getByThread(threadId: String): List<ForumReplyEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(reply: ForumReplyEntity)

    @Query("UPDATE forum_replies SET likes = likes + 1 WHERE id = :id")
    suspend fun incrementLikes(id: String)
}

@Dao
interface PdfAnnotationDao {
    @Query("SELECT * FROM pdf_annotations WHERE pdfPath = :pdfPath AND pageIndex = :pageIndex")
    suspend fun getForPage(pdfPath: String, pageIndex: Int): List<PdfAnnotationEntity>

    @Query("SELECT * FROM pdf_annotations WHERE pdfPath = :pdfPath")
    suspend fun getForDocument(pdfPath: String): List<PdfAnnotationEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(annotation: PdfAnnotationEntity)

    @Query("DELETE FROM pdf_annotations WHERE id = :id")
    suspend fun delete(id: String)

    @Query("DELETE FROM pdf_annotations WHERE pdfPath = :pdfPath")
    suspend fun deleteForDocument(pdfPath: String)
}
