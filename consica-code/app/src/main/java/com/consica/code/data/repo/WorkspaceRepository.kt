package com.consica.code.data.repo

import com.consica.code.core.model.CodeLanguage
import com.consica.code.data.local.CcodeDatabase
import com.consica.code.data.local.entity.WorkspaceEntity
import kotlinx.coroutines.flow.Flow

class WorkspaceRepository(private val db: CcodeDatabase) {

    private val dao get() = db.workspaceDao()

    val all: Flow<List<WorkspaceEntity>> = dao.observeAll()

    suspend fun get(id: Long): WorkspaceEntity? = dao.get(id)

    suspend fun create(
        name: String,
        language: CodeLanguage,
        code: String,
        lessonId: String? = null,
    ): Long {
        val now = System.currentTimeMillis()
        return dao.insert(
            WorkspaceEntity(
                name = name,
                language = language.name,
                code = code,
                lessonId = lessonId,
                isFreePlay = lessonId == null,
                createdAt = now,
                updatedAt = now,
            ),
        )
    }

    suspend fun saveCode(id: Long, code: String) {
        dao.get(id)?.let { dao.update(it.copy(code = code, updatedAt = System.currentTimeMillis())) }
    }

    suspend fun rename(id: Long, name: String) {
        dao.get(id)?.let { dao.update(it.copy(name = name, updatedAt = System.currentTimeMillis())) }
    }

    suspend fun delete(id: Long) = dao.delete(id)
}
