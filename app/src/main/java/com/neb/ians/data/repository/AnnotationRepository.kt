package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.AnnotationDao
import com.neb.ians.data.local.entity.AnnotationEntity
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AnnotationRepository @Inject constructor(
    private val annotationDao: AnnotationDao
) {
    fun getAnnotationsForResource(resourceId: String): Flow<List<AnnotationEntity>> =
        annotationDao.getByResourceId(resourceId)

    fun getAnnotationsForPage(resourceId: String, page: Int): Flow<List<AnnotationEntity>> =
        annotationDao.getByResourceAndPage(resourceId, page)

    suspend fun addAnnotation(annotation: AnnotationEntity) = annotationDao.insert(annotation)

    suspend fun deleteAnnotation(id: Long) = annotationDao.delete(id)

    suspend fun deleteAllForResource(resourceId: String) = annotationDao.deleteByResourceId(resourceId)
}
