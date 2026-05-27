package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.AnnotationDao
import com.neb.ians.data.local.entity.AnnotationEntity
import kotlinx.coroutines.flow.Flow

class AnnotationRepository(private val annotationDao: AnnotationDao) {

    fun getAnnotationsForResource(resourceId: Long): Flow<List<AnnotationEntity>> =
        annotationDao.getAnnotationsForResource(resourceId)

    fun getAnnotationsForPage(resourceId: Long, page: Int): Flow<List<AnnotationEntity>> =
        annotationDao.getAnnotationsForPage(resourceId, page)

    suspend fun insertAnnotation(annotation: AnnotationEntity): Long =
        annotationDao.insertAnnotation(annotation)

    suspend fun updateAnnotation(annotation: AnnotationEntity) =
        annotationDao.updateAnnotation(annotation)

    suspend fun deleteAnnotation(annotation: AnnotationEntity) =
        annotationDao.deleteAnnotation(annotation)
}
