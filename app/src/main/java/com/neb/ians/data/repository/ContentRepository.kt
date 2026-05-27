package com.neb.ians.data.repository

import com.neb.ians.data.local.ContentDao
import com.neb.ians.data.model.ContentItem
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class ContentRepository(private val dao: ContentDao) {
    fun getAll(): Flow<List<ContentItem>> = dao.getAll()

    fun search(query: String): Flow<List<ContentItem>> {
        return if (query.isBlank()) dao.getAll() else dao.search(query)
    }

    fun filter(subject: String?, grade: String?, type: String?): Flow<List<ContentItem>> {
        return if (subject.isNullOrBlank() && grade.isNullOrBlank() && type.isNullOrBlank()) {
            dao.getAll()
        } else {
            dao.getAll().map { list ->
                list.filter {
                    (subject.isNullOrBlank() || it.subject.equals(subject, true)) &&
                    (grade.isNullOrBlank() || it.grade.equals(grade, true)) &&
                    (type.isNullOrBlank() || it.type.equals(type, true))
                }
            }
        }
    }

    fun getDownloaded(): Flow<List<ContentItem>> = dao.getDownloaded()

    suspend fun insert(item: ContentItem) = dao.insert(item)
    suspend fun insertAll(items: List<ContentItem>) = dao.insertAll(items)
    suspend fun updateDownload(id: Long, downloaded: Boolean, path: String?) =
        dao.updateDownloadStatus(id, downloaded, path)
    suspend fun delete(item: ContentItem) = dao.delete(item)
}
