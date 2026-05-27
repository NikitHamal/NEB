package com.neb.ians.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.neb.ians.data.local.entity.AnnotationEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface AnnotationDao {

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId ORDER BY page, createdAt")
    fun getAnnotationsForResource(resourceId: Long): Flow<List<AnnotationEntity>>

    @Query("SELECT * FROM annotations WHERE resourceId = :resourceId AND page = :page ORDER BY createdAt")
    fun getAnnotationsForPage(resourceId: Long, page: Int): Flow<List<AnnotationEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAnnotation(annotation: AnnotationEntity): Long

    @Update
    suspend fun updateAnnotation(annotation: AnnotationEntity)

    @Delete
    suspend fun deleteAnnotation(annotation: AnnotationEntity)

    @Query("DELETE FROM annotations WHERE resourceId = :resourceId")
    suspend fun deleteAllForResource(resourceId: Long)
}
