package com.neb.ians.data.repository

import android.content.Context
import android.text.Html
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.news.NewsCategories
import com.neb.ians.data.news.NewsDetail
import com.neb.ians.data.news.NewsComment
import com.neb.ians.data.news.NewsCommentLikeResponse
import com.neb.ians.data.news.NewsCommentRequest
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

/**
 * News/announcements feed. Stale-while-revalidate: cached pages render
 * instantly (even past their TTL, e.g. offline), a background fetch
 * refreshes them, and the [CacheBus] notifies open screens so the UI
 * updates silently without a manual pull-to-refresh.
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

                val html = apiService.getNewsPage(category).string()
                val parsed = parseNewsList(html)
                cache[key] = CacheEntry(now, parsed)
                parsed
            }
        }

    private fun refreshListInBackground(category: String?) {
        val key = category.orEmpty()
        bgScope.launch {
            try {
                val html = apiService.getNewsPage(category).string()
                val parsed = parseNewsList(html)
                if (parsed.isNotEmpty() || cache[key] == null) {
                    cache[key] = CacheEntry(System.currentTimeMillis(), parsed)
                    cacheBus.publish(listKey(category))
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
                val html = apiService.getNewsDetailPage(slug).string()
                val parsed = parseNewsDetail(slug, html)
                detailCache[slug] = DetailCacheEntry(now, parsed)
                parsed
            }
        }

    private fun refreshDetailInBackground(slug: String) {
        bgScope.launch {
            try {
                val html = apiService.getNewsDetailPage(slug).string()
                val parsed = parseNewsDetail(slug, html)
                detailCache[slug] = DetailCacheEntry(System.currentTimeMillis(), parsed)
                cacheBus.publish(detailKey(slug))
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

    private fun parseNewsList(html: String): List<NewsAnnouncement> {
        val cardRegex = Regex(
            pattern = "<a\\s+href=\"(?<href>[^\"]+)\"\\s+class=\"news-card(?<classes>[^\"]*)\"[^>]*>(?<body>.*?)</a>",
            option = RegexOption.DOT_MATCHES_ALL
        )
        return cardRegex.findAll(html)
            .mapIndexedNotNull { index, match -> parseCard(index, match) }
            .take(60)
            .toList()
    }

    private fun parseNewsDetail(slug: String, html: String): NewsDetail {
        val header = html.firstGroup("<div[^>]*class=\"news-detail-header\"[^>]*>(.*?)</div>\\s*(?:<div class=\"news-detail-cover\"|<div class=\"news-detail-content)")
            .ifBlank { html }
        val title = header.firstGroup("<h1[^>]*class=\"[^\"]*news-detail-title[^\"]*\"[^>]*>(.*?)</h1>").cleanHtml()
            .ifBlank { html.firstGroup("<title>(.*?)</title>").cleanHtml().substringBefore(" — ") }
        val summary = header.firstGroup("<p[^>]*class=\"[^\"]*news-detail-summary[^\"]*\"[^>]*>(.*?)</p>").cleanHtml()
        val badge = Regex("<span[^>]*class=\"news-category-badge\"[^>]*style=\"background:([^\"]+)\"[^>]*>\\s*<span[^>]*>(.*?)</span>\\s*([^<]+)", setOf(RegexOption.DOT_MATCHES_ALL, RegexOption.IGNORE_CASE)).find(html)
        val icon = badge?.groups?.get(2)?.value?.cleanHtml().orEmpty().ifBlank { "info" }
        val label = badge?.groups?.get(3)?.value?.cleanHtml().orEmpty().ifBlank { "General" }
        val color = badge?.groups?.get(1)?.value.orEmpty().ifBlank { label.toCategoryColor() }
        val cover = html.firstGroup("<div[^>]*class=\"news-detail-cover\"[^>]*>\\s*<img\\s+src=\"([^\"]+)\"").absoluteMediaUrl()
        val content = html.firstGroup("<div[^>]*class=\"news-detail-content[^\"]*\"[^>]*id=\"news-content\"[^>]*>(.*?)</div>").cleanArticleContent()
        val external = html.firstGroup("<a\\s+href=\"([^\"]+)\"[^>]*class=\"[^\"]*news-detail-cta[^\"]*\"").cleanHtml()
        val authorBlock = html.firstGroup("<span[^>]*class=\"news-card-author\"[^>]*>(.*?)</span>")
        val authorPhoto = authorBlock.firstGroup("<img\\s+src=\"([^\"]+)\"").absoluteMediaUrl()
        val authorName = authorBlock.replace(Regex("<img[^>]*>", RegexOption.DOT_MATCHES_ALL), "").cleanHtml().ifBlank { "NEBians Team" }
        val publishedAgo = html.findTimeAgo()
        val views = html.findViews()
        val announcement = NewsAnnouncement(
            id = slug,
            slug = slug,
            title = title,
            summary = summary,
            categoryKey = NewsCategories.firstOrNull { it.label.equals(label, ignoreCase = true) }?.key ?: "general",
            categoryLabel = label,
            categoryIcon = icon,
            categoryColorHex = color.trim(),
            isPinned = html.contains("news-pin-badge"),
            coverImageUrl = cover,
            authorName = authorName,
            authorPhotoUrl = authorPhoto,
            publishedAgo = publishedAgo,
            viewCount = views
        )
        val relatedBlock = html.substringAfter("<div class=\"news-related\"", missingDelimiterValue = "")
        val related = if (relatedBlock.isNotBlank()) parseNewsList(relatedBlock) else emptyList()
        return NewsDetail(announcement = announcement, content = content, externalUrl = external, related = related)
    }

    private fun parseCard(index: Int, match: MatchResult): NewsAnnouncement? {
        val href = match.groups["href"]?.value.orEmpty()
        val body = match.groups["body"]?.value.orEmpty()
        val classes = match.groups["classes"]?.value.orEmpty()
        val slug = href.trim('/').substringAfterLast('/').takeIf { it.isNotBlank() } ?: return null
        val title = body.firstGroup("<h2[^>]*class=\"news-card-title\"[^>]*>(.*?)</h2>").cleanHtml()
        if (title.isBlank()) return null
        val summary = body.firstGroup("<p[^>]*class=\"news-card-summary\"[^>]*>(.*?)</p>").cleanHtml()
        val badgeMatch = Regex(
            "<span[^>]*class=\"news-category-badge\"[^>]*style=\"background:([^\"]+)\"[^>]*>\\s*<span[^>]*>(.*?)</span>\\s*([^<]+)",
            setOf(RegexOption.DOT_MATCHES_ALL, RegexOption.IGNORE_CASE)
        ).find(body)
        val icon = badgeMatch?.groups?.get(2)?.value?.cleanHtml().orEmpty().ifBlank { "info" }
        val categoryLabel = badgeMatch?.groups?.get(3)?.value?.cleanHtml().orEmpty().ifBlank { "General" }
        val color = badgeMatch?.groups?.get(1)?.value.orEmpty().ifBlank {
            body.firstGroup("--accent-color:\\s*([^;\"]+)")
        }.ifBlank { categoryLabel.toCategoryColor() }
        val cover = body.firstGroup("<img\\s+src=\"([^\"]+)\"").absoluteMediaUrl()
        val authorBlock = body.firstGroup("<span[^>]*class=\"news-card-author\"[^>]*>(.*?)</span>")
        val authorPhoto = authorBlock.firstGroup("<img\\s+src=\"([^\"]+)\"").absoluteMediaUrl()
        val authorName = authorBlock.replace(Regex("<img[^>]*>", RegexOption.DOT_MATCHES_ALL), "").cleanHtml().ifBlank { "NEBians Team" }
        val publishedAgo = body.findTimeAgo()
        val views = body.findViews()
        val categoryKey = NewsCategories.firstOrNull { it.label.equals(categoryLabel, ignoreCase = true) }?.key ?: "general"

        return NewsAnnouncement(
            id = slug.ifBlank { "news-$index" },
            slug = slug,
            title = title,
            summary = summary,
            categoryKey = categoryKey,
            categoryLabel = categoryLabel,
            categoryIcon = icon,
            categoryColorHex = color.trim(),
            isPinned = classes.contains("pinned", ignoreCase = true) || body.contains("news-pin-badge"),
            coverImageUrl = cover,
            authorName = authorName,
            authorPhotoUrl = authorPhoto,
            publishedAgo = publishedAgo,
            viewCount = views
        )
    }

    private fun String.firstGroup(pattern: String): String {
        return Regex(pattern, RegexOption.DOT_MATCHES_ALL).find(this)?.groups?.get(1)?.value.orEmpty()
    }

    private fun String.cleanHtml(): String {
        if (isBlank()) return ""
        val stripped = replace(Regex("<br\\s*/?>", RegexOption.IGNORE_CASE), "\n")
            .replace(Regex("</p>", RegexOption.IGNORE_CASE), "\n\n")
            .replace(Regex("<[^>]+>"), " ")
            .replace(Regex("[ \\t]+"), " ")
            .replace(Regex("\\n\\s+"), "\n")
            .replace(Regex("\\n{3,}"), "\n\n")
            .trim()
        return Html.fromHtml(stripped, Html.FROM_HTML_MODE_LEGACY).toString().trim()
    }

    private fun String.cleanArticleContent(): String {
        if (isBlank()) return ""
        return replace(Regex("<script[\\s\\S]*?</script>", RegexOption.IGNORE_CASE), "")
            .replace(Regex("<style[\\s\\S]*?</style>", RegexOption.IGNORE_CASE), "")
            .replace(Regex("<br\\s*/?>", RegexOption.IGNORE_CASE), "\n")
            .replace(Regex("</(p|div|h1|h2|h3|li|ul|ol|blockquote)>", RegexOption.IGNORE_CASE), "\n")
            .replace(Regex("<li[^>]*>", RegexOption.IGNORE_CASE), "- ")
            .replace(Regex("<h1[^>]*>", RegexOption.IGNORE_CASE), "# ")
            .replace(Regex("<h2[^>]*>", RegexOption.IGNORE_CASE), "## ")
            .replace(Regex("<h3[^>]*>", RegexOption.IGNORE_CASE), "### ")
            .replace(Regex("<[^>]+>"), "")
            .let { Html.fromHtml(it, Html.FROM_HTML_MODE_LEGACY).toString() }
            .replace(Regex("\\n{3,}"), "\n\n")
            .trim()
    }

    private fun String.absoluteMediaUrl(): String {
        val raw = cleanHtml()
        if (raw.isBlank()) return ""
        return when {
            raw.startsWith("http://") || raw.startsWith("https://") -> raw
            raw.startsWith("/") -> "https://nebians.consica.com.np$raw"
            else -> raw
        }
    }

    private fun String.findTimeAgo(): String {
        val matches = Regex("<span[^>]*>([^<]*(?:ago|just now|Yesterday)[^<]*)</span>", RegexOption.IGNORE_CASE)
            .findAll(this)
            .map { it.groups[1]?.value.orEmpty().cleanHtml() }
            .filter { it.isNotBlank() }
            .toList()
        return matches.lastOrNull().orEmpty()
    }

    private fun String.findViews(): String {
        val afterVisibility = substringAfter("visibility", missingDelimiterValue = "")
        return Regex("([0-9.,KkMm]+)").find(afterVisibility)?.value.orEmpty()
    }

    private fun String.toCategoryColor(): String = when (lowercase()) {
        "exam results" -> "#dc2626"
        "notice" -> "#2563eb"
        "event" -> "#7c3aed"
        "update" -> "#059669"
        "alert" -> "#d97706"
        else -> "#6b7280"
    }
}
