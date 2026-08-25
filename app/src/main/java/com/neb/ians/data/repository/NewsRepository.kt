package com.neb.ians.data.repository

import android.content.Context
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.news.ApiAnnouncement
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.news.NewsCategories
import com.neb.ians.data.news.NewsDetail
import com.neb.ians.data.news.NewsComment
import com.neb.ians.data.news.NewsCommentLikeResponse
import com.neb.ians.data.news.NewsCommentRequest
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

/**
 * News/announcements feed over the public JSON API (/api/news/).
 * Stale-while-revalidate: cached pages render instantly (even past their TTL,
 * e.g. offline), a background fetch refreshes them, and the [CacheBus]
 * notifies open screens so the UI updates silently without pull-to-refresh.
 */
@Singleton
class NewsRepository @Inject constructor(
    private val apiService: ApiService,
    private val cacheBus: CacheBus,
    @ApplicationContext private val context: Context
) {
    private data class CacheEntry(val createdAtMs: Long, val items: List<NewsAnnouncement>)
    private data class DetailCacheEntry(val createdAtMs: Long, val item: NewsDetail)

    private val bgScope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private val cache = mutableMapOf<String, CacheEntry>()
    private val detailCache = mutableMapOf<String, DetailCacheEntry>()
    private val commentsCache = mutableMapOf<String, List<NewsComment>>()
    private val ttlMs = 2 * 60 * 1000L

    private fun listKey(category: String?): String = CacheBus.PREFIX_NEWS_LIST + category.orEmpty()
    private fun detailKey(slug: String): String = CacheBus.PREFIX_NEWS_DETAIL + slug
    private fun commentsKey(slug: String): String = CacheBus.PREFIX_NEWS_COMMENTS + slug

    suspend fun getAnnouncements(category: String? = null, forceRefresh: Boolean = false, cacheOnly: Boolean = false): Result<List<NewsAnnouncement>> =
        withContext(Dispatchers.IO) {
            runCatching {
                val key = category.orEmpty()
                val now = System.currentTimeMillis()
                val cached = cache[key]
                if (cached != null && !forceRefresh) {
                    if (now - cached.createdAtMs < ttlMs) return@runCatching cached.items
                    // Stale: serve now, revalidate in the background.
                    if (!cacheOnly) refreshListInBackground(category)
                    return@runCatching cached.items
                }

                val response = apiService.getNewsList(category)
                if (!response.ok) error(response.error ?: "Couldn't load blog posts")
                val parsed = response.items.map { it.toDomain() }
                cache[key] = CacheEntry(now, parsed)
                parsed
            }
        }

    private fun refreshListInBackground(category: String?) {
        val key = category.orEmpty()
        bgScope.launch {
            try {
                val response = apiService.getNewsList(category)
                if (response.ok) {
                    val parsed = response.items.map { it.toDomain() }
                    if (parsed.isNotEmpty() || cache[key] == null) {
                        cache[key] = CacheEntry(System.currentTimeMillis(), parsed)
                        cacheBus.publish(listKey(category))
                    }
                }
            } catch (_: Exception) {}
        }
    }

    suspend fun getAnnouncementDetail(slug: String, forceRefresh: Boolean = false, cacheOnly: Boolean = false): Result<NewsDetail> =
        withContext(Dispatchers.IO) {
            runCatching {
                val now = System.currentTimeMillis()
                val cached = detailCache[slug]
                if (cached != null && !forceRefresh) {
                    if (now - cached.createdAtMs < ttlMs) return@runCatching cached.item
                    if (!cacheOnly) refreshDetailInBackground(slug)
                    return@runCatching cached.item
                }
                val response = apiService.getNewsDetail(slug)
                if (!response.ok) error(response.error ?: "Couldn't load article")
                val item = response.item ?: error("Article was empty")
                val parsed = item.toDetail(response.related)
                detailCache[slug] = DetailCacheEntry(now, parsed)
                parsed
            }
        }

    /** Count one real article open (server de-dupes web sessions separately). */
    suspend fun trackView(slug: String): Result<Boolean> =
        withContext(Dispatchers.IO) {
            runCatching {
                val response = apiService.trackNewsView(slug)
                if (!response.ok) error(response.error ?: "Couldn't track view")
                response.counted
            }
        }

    private fun refreshDetailInBackground(slug: String) {
        bgScope.launch {
            try {
                val response = apiService.getNewsDetail(slug)
                if (response.ok && response.item != null) {
                    val parsed = response.item.toDetail(response.related)
                    detailCache[slug] = DetailCacheEntry(System.currentTimeMillis(), parsed)
                    cacheBus.publish(detailKey(slug))
                }
            } catch (_: Exception) {}
        }
    }

    suspend fun getComments(slug: String, cacheOnly: Boolean = false): Result<List<NewsComment>> =
        withContext(Dispatchers.IO) {
            runCatching {
                val cached = commentsCache[slug]
                if (cached != null) {
                    if (!cacheOnly) refreshCommentsInBackground(slug)
                    return@runCatching cached
                }
                val response = apiService.getNewsComments(slug)
                if (!response.ok) error(response.error ?: "Couldn't load comments")
                commentsCache[slug] = response.comments
                response.comments
            }
        }

    private fun refreshCommentsInBackground(slug: String) {
        bgScope.launch {
            try {
                val response = apiService.getNewsComments(slug)
                if (response.ok) {
                    commentsCache[slug] = response.comments
                    cacheBus.publish(commentsKey(slug))
                }
            } catch (_: Exception) {}
        }
    }

    suspend fun postComment(slug: String, text: String, parentCommentId: String? = null): Result<NewsComment> =
        withContext(Dispatchers.IO) {
            runCatching {
                val token = SecurePrefs.getAuthToken(context)?.takeIf { it.isNotBlank() }
                    ?: error("Please sign in to comment")
                val response = apiService.createNewsComment(
                    "Bearer $token",
                    NewsCommentRequest(slug = slug, text = text, parentCommentId = parentCommentId)
                )
                if (!response.ok) error(response.error ?: "Couldn't post comment")
                val comment = response.comment ?: error("Comment was not returned")
                val current = commentsCache[slug].orEmpty()
                if (current.none { it.id == comment.id }) {
                    commentsCache[slug] = current + comment
                    cacheBus.publish(commentsKey(slug))
                }
                comment
            }
        }

    suspend fun toggleCommentLike(commentId: String): Result<NewsCommentLikeResponse> =
        withContext(Dispatchers.IO) {
            runCatching {
                val token = SecurePrefs.getAuthToken(context)?.takeIf { it.isNotBlank() }
                    ?: error("Please sign in to like comments")
                val response = apiService.toggleBlogCommentLike("Bearer $token", commentId)
                if (response.error != null) error(response.error)
                response
            }
        }

    suspend fun deleteComment(commentId: String): Result<Unit> =
        withContext(Dispatchers.IO) {
            runCatching {
                val token = SecurePrefs.getAuthToken(context)?.takeIf { it.isNotBlank() }
                    ?: error("Please sign in to delete comments")
                apiService.deleteBlogComment("Bearer $token", commentId)
                val touched = commentsCache.filterValues { comments -> comments.any { it.id == commentId } }.keys.toList()
                touched.forEach { slug ->
                    commentsCache[slug] = commentsCache[slug].orEmpty().filterNot { it.id == commentId }
                    cacheBus.publish(commentsKey(slug))
                }
                Unit
            }
        }

    /**
     * Raw markdown from the API; screens render it with MarkdownText so
     * headings, bold/italic, lists, code and LaTeX formulas all display.
     */
    private fun ApiAnnouncement.toDomain(): NewsAnnouncement = NewsAnnouncement(
        id = slug.ifBlank { id.toString() },
        slug = slug,
        title = title,
        summary = summary,
        categoryKey = NewsCategories.firstOrNull { it.key == category }?.key ?: category,
        categoryLabel = categoryLabel,
        categoryIcon = categoryIcon,
        categoryColorHex = categoryColor,
        isPinned = isPinned,
        coverImageUrl = coverImageUrl,
        authorName = authorName,
        authorPhotoUrl = authorPhoto,
        publishedAgo = formatTimeAgo(publishedAt),
        viewCount = formatCount(viewCount)
    )

    private fun ApiAnnouncement.toDetail(related: List<ApiAnnouncement> = emptyList()): NewsDetail = NewsDetail(
        announcement = toDomain(),
        content = content.orEmpty(),
        externalUrl = externalUrl,
        related = related.map { it.toDomain() }
    )

    private fun formatCount(n: Int): String = when {
        n >= 1_000_000 -> String.format(java.util.Locale.US, "%.1fM", n / 1_000_000.0)
        n >= 1_000 -> String.format(java.util.Locale.US, "%.1fK", n / 1_000.0)
        else -> n.toString()
    }
}
