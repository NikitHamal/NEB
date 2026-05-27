package com.neb.ians.data.repository

import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.entity.BookmarkEntity
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class BookmarkRepository @Inject constructor(
    private val bookmarkDao: BookmarkDao
) {
    fun getBookmarksForResource(resourceId: String): Flow<List<BookmarkEntity>> =
        bookmarkDao.getByResourceId(resourceId)

    fun getAllBookmarks(): Flow<List<BookmarkEntity>> = bookmarkDao.getAll()

    suspend fun addBookmark(bookmark: BookmarkEntity) = bookmarkDao.insert(bookmark)

    suspend fun deleteBookmark(id: Long) = bookmarkDao.delete(id)
}
