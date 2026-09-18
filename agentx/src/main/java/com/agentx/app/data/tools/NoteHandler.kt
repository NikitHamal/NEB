package com.agentx.app.data.tools

import com.agentx.app.data.embed.EmbeddingManager
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.local.dao.NoteDao
import com.agentx.app.data.local.entity.NoteEntity
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class NoteHandler @Inject constructor(
    private val dao: NoteDao,
    private val embeddings: EmbeddingManager
) {
    suspend fun create(spec: ToolCallSpec): ToolExecution {
        val body = spec.arg("body") ?: return ToolExecution.fail("What should the note say?")
        if (body.length > 4000) return ToolExecution.fail("Keep notes under 4000 characters")
        val title = spec.arg("title").orEmpty().take(120)
        val id = dao.insert(NoteEntity(title = title, body = body))
        embeddings.prime(id, (if (title.isBlank()) "" else title + ". ") + body)
        return ToolExecution.done("Note saved (id " + id + ")")
    }

    suspend fun search(spec: ToolCallSpec): ToolExecution {
        val query = spec.arg("query") ?: return ToolExecution.fail("What should I search for?")
        val keywordHits = dao.keywordSearch(query).take(20)
        val recent = dao.recent(60)
        val pool = (keywordHits + recent).distinctBy { it.id }
        val ranked = embeddings.searchRanked(query, pool).take(8)
        if (ranked.isEmpty()) return ToolExecution.done("No notes matching " + query)
        val lines = StringBuilder()
        for (note in ranked) {
            val heading = if (note.title.isBlank()) "Note " + note.id else note.title
            val snippet = note.body.take(110).replace(System.lineSeparator(), " ")
            lines.appendLine(heading + " - " + snippet)
        }
        return ToolExecution.done(lines.toString().trim())
    }

    suspend fun listRecent(limit: Int = 10): List<NoteEntity> = dao.recent(limit)
}
