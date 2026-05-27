package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.neb.ians.data.local.entity.AnnotationEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface AnnotationDao {

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId ORDER BY page ASC, createdAt ASC")
    fun getByResourceId(resourceId: String): Flow<List<AnnotationEntity>>

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId AND page = :page ORDER BY createdAt ASC")
    fun getByResourceAndPage(resourceId: String, page: Int): Flow<List<AnnotationEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(annotation: AnnotationEntity)

    @Query("DELETE FROM annotations WHERE id = :id")
    suspend fun delete(id: Long)

    @Query("DELETE FROM annotations WHERE resourceId = :resourceId")
    suspend fun deleteByResourceId(resourceId: String)
}
