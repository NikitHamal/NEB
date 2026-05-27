package com.neb.ians.data

import com.neb.ians.data.local.AnnotationDao
import com.neb.ians.data.local.AnnotationEntity
import com.neb.ians.data.local.ForumDao
import com.neb.ians.data.local.ForumReplyEntity
import com.neb.ians.data.local.ForumThreadEntity
import com.neb.ians.data.local.ResourceDao
import com.neb.ians.data.local.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow

@Singleton
class ResourceRepository @Inject constructor(
    private val dao: ResourceDao,
) {
    fun search(
        query: String = "",
        subject: Subject? = null,
        grade: Grade? = null,
        type: ResourceType? = null,
    ): Flow<List<ResourceEntity>> = dao.search(query, subject, grade, type)

    fun recent(limit: Int = 8) = dao.recent(limit)
    fun favorites() = dao.favorites()
    fun observe(id: Long) = dao.observe(id)
    suspend fun get(id: Long) = dao.get(id)
    suspend fun setFavorite(id: Long, fav: Boolean) = dao.setFavorite(id, fav)
    suspend fun touch(id: Long) = dao.touch(id)
    suspend fun upsertAll(items: List<ResourceEntity>) = dao.upsertAll(items)
    suspend fun count() = dao.count()
}

@Singleton
class AnnotationRepository @Inject constructor(
    private val dao: AnnotationDao,
) {
    fun forResource(id: Long) = dao.forResource(id)
    fun forPage(id: Long, page: Int) = dao.forPage(id, page)
    suspend fun add(item: AnnotationEntity) = dao.insert(item)
    suspend fun update(item: AnnotationEntity) = dao.update(item)
    suspend fun delete(id: Long) = dao.deleteById(id)
}

@Singleton
class ForumRepository @Inject constructor(
    private val dao: ForumDao,
) {
    fun threads() = dao.threads()
    fun thread(id: Long) = dao.thread(id)
    fun replies(id: Long) = dao.replies(id)
    suspend fun postThread(t: ForumThreadEntity) = dao.insertThread(t)
    suspend fun postReply(r: ForumReplyEntity): Long {
        val id = dao.insertReply(r)
        dao.incrementReply(r.threadId)
        return id
    }
    suspend fun likeThread(id: Long) = dao.likeThread(id, 1)
    suspend fun likeReply(id: Long) = dao.likeReply(id, 1)
    suspend fun count() = dao.count()
}
