package com.neb.ians.data.repository

import com.neb.ians.data.db.PdfAnnotationDao
import com.neb.ians.data.db.PdfAnnotationEntity
import com.neb.ians.data.model.AnnotationType
import com.neb.ians.data.model.PdfAnnotation

class AnnotationRepository(private val dao: PdfAnnotationDao) {

    suspend fun getForPage(pdfPath: String, pageIndex: Int): List<PdfAnnotation> {
        return dao.getForPage(pdfPath, pageIndex).map { it.toModel() }
    }

    suspend fun getForDocument(pdfPath: String): List<PdfAnnotation> {
        return dao.getForDocument(pdfPath).map { it.toModel() }
    }

    suspend fun save(annotation: PdfAnnotation) {
        dao.insert(annotation.toEntity())
    }

    suspend fun delete(id: String) {
        dao.delete(id)
    }

    private fun PdfAnnotationEntity.toModel() = PdfAnnotation(
        id = id,
        pdfPath = pdfPath,
        pageIndex = pageIndex,
        type = AnnotationType.valueOf(type),
        x = x,
        y = y,
        width = width,
        height = height,
        noteText = noteText,
        color = color,
        createdAt = createdAt
    )

    private fun PdfAnnotation.toEntity() = PdfAnnotationEntity(
        id = id,
        pdfPath = pdfPath,
        pageIndex = pageIndex,
        type = type.name,
        x = x,
        y = y,
        width = width,
        height = height,
        noteText = noteText,
        color = color,
        createdAt = createdAt
    )
}
