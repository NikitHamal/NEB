package com.consica.code.data.repository

import com.consica.code.data.local.CodeAttemptDao
import com.consica.code.data.local.WorkspaceDao
import com.consica.code.data.local.WorkspaceEntity
import kotlinx.coroutines.flow.Flow

class WorkspaceRepository(
    private val workspaceDao: WorkspaceDao,
    private val codeAttemptDao: CodeAttemptDao,
) {
    val all: Flow<List<WorkspaceEntity>> = workspaceDao.observeAll()
    fun recent(limit: Int = 5): Flow<List<WorkspaceEntity>> = workspaceDao.observeRecent(limit)

    suspend fun get(id: Long): WorkspaceEntity? = workspaceDao.get(id)

    suspend fun save(name: String, language: String, content: String, lessonId: String? = null, id: Long = 0): Long {
        val now = System.currentTimeMillis()
        val existing = if (id != 0L) workspaceDao.get(id) else null
        return workspaceDao.upsert(
            WorkspaceEntity(
                id = id,
                name = name.ifBlank { "Untitled" },
                language = language,
                content = content,
                lessonId = lessonId ?: existing?.lessonId,
                createdAt = existing?.createdAt ?: now,
                updatedAt = now,
            )
        )
    }

    suspend fun delete(id: Long) = workspaceDao.delete(id)
}
