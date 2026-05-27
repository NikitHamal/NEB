package com.neb.ians.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.neb.ians.data.model.ContentItem
import kotlinx.coroutines.flow.Flow

@Dao
interface ContentDao {
    @Query("SELECT * FROM content_items ORDER BY addedAt DESC")
    fun getAll(): Flow<List<ContentItem>>

    @Query("SELECT * FROM content_items WHERE subject = :subject AND grade = :grade AND type = :type ORDER BY title ASC")
    fun filter(subject: String, grade: String, type: String): Flow<List<ContentItem>>

    @Query("SELECT * FROM content_items WHERE title LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%' ORDER BY title ASC")
    fun search(query: String): Flow<List<ContentItem>>

    @Query("SELECT * FROM content_items WHERE isDownloaded = 1 ORDER BY title ASC")
    fun getDownloaded(): Flow<List<ContentItem>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: ContentItem): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<ContentItem>)

    @Query("UPDATE content_items SET isDownloaded = :downloaded, localPath = :path WHERE id = :id")
    suspend fun updateDownloadStatus(id: Long, downloaded: Boolean, path: String?)

    @Delete
    suspend fun delete(item: ContentItem)
}
