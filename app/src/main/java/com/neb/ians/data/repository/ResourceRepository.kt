package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.ResourceDao
import com.neb.ians.data.local.entity.ResourceEntity
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ResourceRepository @Inject constructor(
    private val resourceDao: ResourceDao,
    private val apiService: com.neb.ians.data.api.ApiService
) {
    suspend fun syncResources() {
        try {
            val apiRes = apiService.getResources()
            val entities = apiRes.map { res ->
                ResourceEntity(
                    id = res.id,
                    title = res.title,
                    description = res.description,
                    subject = res.subject,
                    gradeLevel = res.gradeLevel,
                    type = res.type,
                    fileUrl = res.fileUrl,
                    thumbnailUrl = res.thumbnailUrl,
                    fileSize = res.fileSize,
                    addedAt = res.addedAt,
                    viewCount = res.viewCount,
                    // keep download local status if it exists in DB
                    isDownloaded = resourceDao.getByIdSync(res.id)?.isDownloaded ?: false,
                    localPath = resourceDao.getByIdSync(res.id)?.localPath
                )
            }
            resourceDao.insertAll(entities)
        } catch (e: Exception) {
            // Offline fallback
        }
    }

    fun getAllResources(): Flow<List<ResourceEntity>> = resourceDao.getAll()

    fun getResourceById(id: String): Flow<ResourceEntity?> = resourceDao.getById(id)

    fun getBySubject(subject: String): Flow<List<ResourceEntity>> = resourceDao.getBySubject(subject)

    fun getByGradeLevel(gradeLevel: String): Flow<List<ResourceEntity>> = resourceDao.getByGradeLevel(gradeLevel)

    fun getByType(type: String): Flow<List<ResourceEntity>> = resourceDao.getByType(type)

    fun searchResources(query: String): Flow<List<ResourceEntity>> = resourceDao.search("%$query%")

    fun getDownloadedResources(): Flow<List<ResourceEntity>> = resourceDao.getDownloaded()

    fun getFilteredResources(
        subject: String? = null,
        gradeLevel: String? = null,
        type: String? = null
    ): Flow<List<ResourceEntity>> = resourceDao.getFiltered(subject, gradeLevel, type)

    suspend fun insertResource(resource: ResourceEntity) = resourceDao.insert(resource)

    suspend fun insertResources(resources: List<ResourceEntity>) = resourceDao.insertAll(resources)

    suspend fun updateDownloadStatus(id: String, isDownloaded: Boolean, localPath: String?) =
        resourceDao.updateDownloadStatus(id, isDownloaded, localPath)

    suspend fun updateDownloadProgress(id: String, progress: Int) =
        resourceDao.updateDownloadProgress(id, progress)

    suspend fun deleteResource(id: String) = resourceDao.delete(id)
}
