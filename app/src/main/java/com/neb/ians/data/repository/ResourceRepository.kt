package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.dao.ResourceDao
import com.neb.ians.data.local.entity.BookmarkEntity
import com.neb.ians.data.local.entity.ResourceEntity
import kotlinx.coroutines.flow.Flow

class ResourceRepository(
    private val resourceDao: ResourceDao,
    private val bookmarkDao: BookmarkDao,
) {

    fun getAllResources(): Flow<List<ResourceEntity>> = resourceDao.getAllResources()

    suspend fun getResourceById(id: Long): ResourceEntity? = resourceDao.getResourceById(id)

    fun getFilteredResources(
        subject: String = "",
        grade: String = "",
        type: String = "",
    ): Flow<List<ResourceEntity>> = resourceDao.getFilteredResources(subject, grade, type)

    fun searchResources(query: String): Flow<List<ResourceEntity>> =
        resourceDao.searchResources(query)

    fun getAllSubjects(): Flow<List<String>> = resourceDao.getAllSubjects()

    fun getAllGrades(): Flow<List<String>> = resourceDao.getAllGrades()

    suspend fun insertResource(resource: ResourceEntity): Long =
        resourceDao.insertResource(resource)

    suspend fun insertAll(resources: List<ResourceEntity>) = resourceDao.insertAll(resources)

    suspend fun updateResource(resource: ResourceEntity) = resourceDao.updateResource(resource)

    fun getCachedResources(): Flow<List<ResourceEntity>> = resourceDao.getCachedResources()

    fun getAllBookmarks(): Flow<List<BookmarkEntity>> = bookmarkDao.getAllBookmarks()

    fun isBookmarked(resourceId: Long): Flow<Boolean> = bookmarkDao.isBookmarked(resourceId)

    suspend fun toggleBookmark(resourceId: Long, isCurrentlyBookmarked: Boolean) {
        if (isCurrentlyBookmarked) {
            bookmarkDao.removeBookmark(resourceId)
        } else {
            bookmarkDao.insertBookmark(BookmarkEntity(resourceId = resourceId))
        }
    }
}
