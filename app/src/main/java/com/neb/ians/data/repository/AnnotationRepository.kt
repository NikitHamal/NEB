package com.neb.ians.data.repository

import com.neb.ians.data.local.AnnotationDao
import com.neb.ians.data.model.PdfAnnotation
import kotlinx.coroutines.flow.Flow

class AnnotationRepository(private val dao: AnnotationDao) {
    fun getAnnotations(pdfUri: String): Flow<List<PdfAnnotation>> = dao.getForPdf(pdfUri)
    suspend fun save(annotation: PdfAnnotation): Long = dao.insert(annotation)
    suspend fun delete(annotation: PdfAnnotation) = dao.delete(annotation)
}
