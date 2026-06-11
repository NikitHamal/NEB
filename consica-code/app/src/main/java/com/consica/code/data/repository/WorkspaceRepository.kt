package com.consica.code.data.repository

import com.consica.code.data.local.dao.WorkspaceDao
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.local.entity.WorkspaceFileEntity
import com.consica.code.domain.model.TrackLanguage
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class WorkspaceRepository @Inject constructor(
    private val workspaceDao: WorkspaceDao,
) {
    val workspaces: Flow<List<WorkspaceEntity>> = workspaceDao.observeAll()

    fun observe(id: Long): Flow<WorkspaceEntity?> = workspaceDao.observe(id)

    fun observeFiles(workspaceId: Long): Flow<List<WorkspaceFileEntity>> =
        workspaceDao.observeFiles(workspaceId)

    suspend fun get(id: Long): WorkspaceEntity? = workspaceDao.get(id)

    suspend fun files(workspaceId: Long): List<WorkspaceFileEntity> =
        workspaceDao.files(workspaceId)

    suspend fun create(
        name: String,
        language: TrackLanguage,
        initialContent: String,
        lessonId: String? = null,
        templateId: String? = null,
    ): Long {
        val now = System.currentTimeMillis()
        val workspaceId = workspaceDao.insert(
            WorkspaceEntity(
                name = name,
                language = language.name,
                createdAt = now,
                updatedAt = now,
                lessonId = lessonId,
                templateId = templateId,
            )
        )
        workspaceDao.insertFile(
            WorkspaceFileEntity(
                workspaceId = workspaceId,
                name = if (language == TrackLanguage.HTML) "index.html" else "main.py",
                content = initialContent,
                updatedAt = now,
            )
        )
        return workspaceId
    }

    suspend fun rename(id: Long, name: String) {
        val workspace = workspaceDao.get(id) ?: return
        workspaceDao.update(workspace.copy(name = name, updatedAt = System.currentTimeMillis()))
    }

    suspend fun saveFile(file: WorkspaceFileEntity, content: String) {
        val now = System.currentTimeMillis()
        workspaceDao.updateFile(file.copy(content = content, updatedAt = now))
        workspaceDao.get(file.workspaceId)?.let {
            workspaceDao.update(it.copy(updatedAt = now))
        }
    }

    suspend fun addFile(workspaceId: Long, name: String, content: String = ""): Long {
        val now = System.currentTimeMillis()
        return workspaceDao.insertFile(
            WorkspaceFileEntity(
                workspaceId = workspaceId,
                name = name,
                content = content,
                updatedAt = now,
            )
        )
    }

    suspend fun deleteFile(fileId: Long) = workspaceDao.deleteFile(fileId)

    suspend fun delete(id: Long) {
        workspaceDao.deleteFilesFor(id)
        workspaceDao.delete(id)
    }

    suspend fun clearAll() {
        workspaceDao.clearAllFiles()
        workspaceDao.clearAll()
    }
}
