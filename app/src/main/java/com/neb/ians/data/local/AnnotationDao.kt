package com.neb.ians.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.neb.ians.data.model.PdfAnnotation
import kotlinx.coroutines.flow.Flow

@Dao
interface AnnotationDao {
    @Query("SELECT * FROM annotations WHERE pdfUri = :pdfUri ORDER BY pageIndex, createdAt")
    fun getForPdf(pdfUri: String): Flow<List<PdfAnnotation>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(annotation: PdfAnnotation): Long

    @Delete
    suspend fun delete(annotation: PdfAnnotation)

    @Query("DELETE FROM annotations WHERE pdfUri = :pdfUri")
    suspend fun deleteAllForPdf(pdfUri: String)
}
