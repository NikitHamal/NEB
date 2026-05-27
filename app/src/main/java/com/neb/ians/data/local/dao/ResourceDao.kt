package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.neb.ians.data.local.entity.ResourceEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ResourceDao {

    @Query("SELECT * FROM resources ORDER BY addedAt DESC")
    fun getAllResources(): Flow<List<ResourceEntity>>

    @Query("SELECT * FROM resources WHERE id = :id")
    suspend fun getResourceById(id: Long): ResourceEntity?

    @Query("""
        SELECT * FROM resources
        WHERE (:subject = '' OR subject = :subject)
        AND (:grade = '' OR grade = :grade)
        AND (:type = '' OR type = :type)
        ORDER BY addedAt DESC
    """)
    fun getFilteredResources(subject: String, grade: String, type: String): Flow<List<ResourceEntity>>

    @Query("""
        SELECT * FROM resources
        WHERE title LIKE '%' || :query || '%'
        OR description LIKE '%' || :query || '%'
        OR author LIKE '%' || :query || '%'
        ORDER BY addedAt DESC
    """)
    fun searchResources(query: String): Flow<List<ResourceEntity>>

    @Query("SELECT DISTINCT subject FROM resources ORDER BY subject")
    fun getAllSubjects(): Flow<List<String>>

    @Query("SELECT DISTINCT grade FROM resources ORDER BY grade")
    fun getAllGrades(): Flow<List<String>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertResource(resource: ResourceEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(resources: List<ResourceEntity>)

    @Update
    suspend fun updateResource(resource: ResourceEntity)

    @Delete
    suspend fun deleteResource(resource: ResourceEntity)

    @Query("SELECT * FROM resources WHERE isCached = 1 ORDER BY addedAt DESC")
    fun getCachedResources(): Flow<List<ResourceEntity>>
}
