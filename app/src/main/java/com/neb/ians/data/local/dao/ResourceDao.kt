package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.neb.ians.data.local.entity.ResourceEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ResourceDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(resource: ResourceEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(resources: List<ResourceEntity>)

    @Query("SELECT * FROM resources ORDER BY addedAt DESC")
    fun getAll(): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE id = :id")
    fun getById(id: String): Flow<ResourceEntity?>

    @Query("SELECT * FROM resources WHERE id = :id")
    suspend fun getByIdSync(id: String): ResourceEntity?

    @Query("SELECT * FROM resources WHERE id IN (:ids)")
    suspend fun getByIdsSync(ids: List<String>): List<ResourceEntity>

    @Query("SELECT * FROM resources WHERE subject = :subject ORDER BY addedAt DESC")
    fun getBySubject(subject: String): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE gradeLevel = :gradeLevel ORDER BY addedAt DESC")
    fun getByGradeLevel(gradeLevel: String): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE type = :type ORDER BY addedAt DESC")
    fun getByType(type: String): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE title LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%' ORDER BY addedAt DESC")
    fun search(query: String): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE isDownloaded = 1 ORDER BY lastAccessedAt DESC")
    fun getDownloaded(): Flow<List<ResourceEntity>>

    @Query(
        "SELECT * FROM resources WHERE " +
        "(:subject IS NULL OR subject = :subject) AND " +
        "(:gradeLevel IS NULL OR gradeLevel = :gradeLevel) AND " +
        "(:type IS NULL OR type = :type) " +
        "ORDER BY addedAt DESC"
    )
    fun getFiltered(subject: String?, gradeLevel: String?, type: String?): Flow<List<ResourceEntity>>

    @Query("UPDATE resources SET isDownloaded = :isDownloaded, localPath = :localPath WHERE id = :id")
    suspend fun updateDownloadStatus(id: String, isDownloaded: Boolean, localPath: String?)

    @Query("UPDATE resources SET downloadProgress = :progress WHERE id = :id")
    suspend fun updateDownloadProgress(id: String, progress: Int)

    @Query("DELETE FROM resources WHERE id = :id")
    suspend fun delete(id: String)

    @Query("DELETE FROM resources WHERE id NOT IN (:ids)")
    suspend fun deleteExceptWithIds(ids: List<String>)

    @Query("DELETE FROM resources")
    suspend fun deleteAll()
}
