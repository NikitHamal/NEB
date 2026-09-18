package com.agentx.app.data.embed

import com.agentx.app.data.engine.NeedleRuntime
import com.agentx.app.data.local.dao.NoteDao
import com.agentx.app.data.local.entity.NoteEmbeddingEntity
import com.agentx.app.data.local.entity.NoteEntity
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.security.MessageDigest
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlin.math.sqrt

@Singleton
class EmbeddingManager @Inject constructor(
    private val runtime: NeedleRuntime,
    private val noteDao: NoteDao
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    @Volatile private var dimHint: Int = 768

    suspend fun embed(text: String): List<Float>? {
        val clean = text.trim().take(600)
        if (clean.length < 2) return null
        val values = runtime.embedAndAwait(UUID.randomUUID().toString(), clean) ?: return null
        if (values.isEmpty()) return null
        dimHint = values.size
        return values
    }

    fun prime(noteId: Long, text: String) {
        scope.launch {
            runCatching {
                val values = embed(text) ?: return@launch
                noteDao.upsertEmbedding(
                    NoteEmbeddingEntity(
                        noteId = noteId,
                        dim = values.size,
                        vector = floatsToBytes(values),
                        textHash = sha256(text.trim().take(600))
                    )
                )
            }
        }
    }

    suspend fun searchRanked(query: String, notes: List<NoteEntity>): List<NoteEntity> {
        if (notes.isEmpty()) return emptyList()
        val queryVector = runCatching { embed(query) }.getOrNull()
        if (queryVector.isNullOrEmpty()) return keywordRanked(query, notes)
        val stored = noteDao.allEmbeddings().associateBy { it.noteId }
        val scored = notes.map { note ->
            val cached = stored[note.id]
            val semantic = if (cached != null && cached.dim == queryVector.size) {
                cosine(queryVector, bytesToFloats(cached.vector))
            } else {
                0.0
            }
            val keyword = keywordScore(query, note.title + " " + note.body)
            note to (semantic * 0.7 + keyword * 0.3)
        }
        return scored.filter { it.second > 0.02 }.sortedByDescending { it.second }.map { it.first }
    }

    fun keywordRanked(query: String, notes: List<NoteEntity>): List<NoteEntity> {
        return notes.map { it to keywordScore(query, it.title + " " + it.body) }
            .filter { it.second > 0.0 }
            .sortedByDescending { it.second }
            .map { it.first }
    }

    private fun keywordScore(query: String, text: String): Double {
        val lower = text.lowercase()
        var score = 0.0
        for (token in query.lowercase().split(' ', ',', '.', '?', '!')) {
            val term = token.trim()
            if (term.length < 2) continue
            if (lower.contains(term)) score += term.length.toDouble()
        }
        return score
    }

    private fun cosine(a: List<Float>, b: List<Float>): Double {
        if (a.size != b.size || a.isEmpty()) return 0.0
        var dot = 0.0
        var na = 0.0
        var nb = 0.0
        for (i in a.indices) {
            val x = a[i].toDouble()
            val y = b[i].toDouble()
            dot += x * y
            na += x * x
            nb += y * y
        }
        if (na <= 0.0 || nb <= 0.0) return 0.0
        return dot / (sqrt(na) * sqrt(nb))
    }

    private fun floatsToBytes(values: List<Float>): ByteArray {
        val buffer = ByteBuffer.allocate(values.size * 4).order(ByteOrder.LITTLE_ENDIAN)
        for (value in values) buffer.putFloat(value)
        return buffer.array()
    }

    private fun bytesToFloats(bytes: ByteArray): List<Float> {
        if (bytes.size % 4 != 0) return emptyList()
        val buffer = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN)
        val out = ArrayList<Float>(bytes.size / 4)
        while (buffer.hasRemaining()) out.add(buffer.float)
        return out
    }

    private fun sha256(text: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        return digest.digest(text.toByteArray()).joinToString("") { "%02x".format(it) }
    }
}
