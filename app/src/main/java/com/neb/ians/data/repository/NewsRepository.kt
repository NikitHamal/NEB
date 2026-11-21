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

    suspend fun postComment(slug: String, text: String, parentCommentId: String? = null, isAnonymous: Boolean = false): Result<NewsComment> =
        withContext(Dispatchers.IO) {
            runCatching {
                val token = SecurePrefs.getAuthToken(context)?.takeIf { it.isNotBlank() }
                    ?: error("Please sign in to comment")
                val response = apiService.createNewsComment(
                    "Bearer $token",
                    NewsCommentRequest(slug = slug, text = text, parentCommentId = parentCommentId, isAnonymous = isAnonymous)
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

    private val newsCardListRegex = Regex(
        pattern = "<a\\s+href=\"(?<href>[^\"]+)\"\\s+class=\"(?:news-card|bcard|bhero)(?<classes>[^\"]*)\"[^>]*>(?<body>.*?)</a>",
        option = RegexOption.DOT_MATCHES_ALL
    )
    private val newsCategoryBadgeRegex = Regex(
        "<span[^>]*class=\"news-category-badge\"[^>]*style=\"(?:background|--cat-color):([^\";]+)[^\"]*\"[^>]*>\\s*<span[^>]*>(.*?)</span>\\s*([^<]+)",
        setOf(RegexOption.DOT_MATCHES_ALL, RegexOption.IGNORE_CASE)
    )

    private fun parseNewsList(html: String): List<NewsAnnouncement> {
        // Both card generations: the old `.news-card` and the web's current `.bcard` / `.bhero`.
        return newsCardListRegex.findAll(html)
            .mapIndexedNotNull { index, match -> parseCard(index, match) }
            .take(60)
            .toList()
    }

    private fun parseNewsDetail(slug: String, html: String): NewsDetail {
        val header = html.firstGroup("<(?:div|header)[^>]*class=\"news-detail-header\"[^>]*>(.*?)</(?:div|header)>\\s*(?:<div class=\"news-detail-cover\"|<div class=\"news-detail-content)")
            .ifBlank { html }
        val title = header.firstGroup("<h1[^>]*class=\"[^\"]*news-detail-title[^\"]*\"[^>]*>(.*?)</h1>").cleanHtml()
            .ifBlank { html.firstGroup("<title>(.*?)</title>").cleanHtml().substringBefore(" — ") }
        val summary = header.firstGroup("<p[^>]*class=\"[^\"]*news-detail-summary[^\"]*\"[^>]*>(.*?)</p>").cleanHtml()
        val badge = newsCategoryBadgeRegex.find(html)
        val icon = badge?.groups?.get(2)?.value?.cleanHtml().orEmpty().ifBlank { "info" }
        val label = badge?.groups?.get(3)?.value?.cleanHtml().orEmpty().ifBlank { "General" }
        val color = badge?.groups?.get(1)?.value.orEmpty().ifBlank { label.toCategoryColor() }
        val cover = html.firstGroup("<div[^>]*class=\"news-detail-cover\"[^>]*>\\s*<img[^>]*?\\ssrc=\"([^\"]+)\"").absoluteMediaUrl()
        val content = articleHtml(html).cleanArticleContent()
        val external = html.firstGroup("<a[^>]*class=\"[^\"]*nd-source-btn[^\"]*\"[^>]*href=\"([^\"]+)\"").cleanHtml()
            .ifBlank { html.firstGroup("<a\\s+href=\"([^\"]+)\"[^>]*class=\"[^\"]*news-detail-cta[^\"]*\"").cleanHtml() }
        val headerClean = header.replace(verifiedMark, "")
        val authorBlock = headerClean.firstGroup("<span[^>]*class=\"news-card-author\"[^>]*>(.*?)</span>")
        val authorPhoto = authorBlock.firstGroup("<img[^>]*\\ssrc=\"([^\"]+)\"").absoluteMediaUrl()
        val authorName = authorBlock.replace(imgTagDotAllRegex, "").cleanHtml().ifBlank { "NEBians Team" }
        val publishedAgo = header.findTimeAgo().ifBlank { html.findTimeAgo() }
        val views = header.findViews().ifBlank { html.findViews() }
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

    /** The article body: from `#news-content` to the block that follows it (nested divs safe). */
    private fun articleHtml(html: String): String {
        val marker = html.indexOf("id=\"news-content\"")
        if (marker < 0) return ""
        val start = html.indexOf('>', marker) + 1
        val ends = listOf("<section class=\"nd-files\"", "<aside class=\"nd-source\"", "<div class=\"nd-actionbar\"", "</article>")
            .map { html.indexOf(it, start) }
            .filter { it >= 0 }
        val end = ends.minOrNull() ?: html.length
        return html.substring(start, end).trimEnd().removeSuffix("</div>")
    }

    private val verifiedMark = Regex("<span[^>]*src-verified[^>]*>.*?</span>", RegexOption.DOT_MATCHES_ALL)
    private val categoryBadgeRegex = Regex(
        "<span[^>]*class=\"(?:news-category-badge|bcard-cat|bhero-kicker)\"[^>]*>\\s*<span[^>]*>(.*?)</span>\\s*([^<]+)",
        setOf(RegexOption.DOT_MATCHES_ALL, RegexOption.IGNORE_CASE)
    )

    private fun parseCard(index: Int, match: MatchResult): NewsAnnouncement? {
        val href = match.groups["href"]?.value.orEmpty()
        val body = match.groups["body"]?.value.orEmpty()
        val classes = match.groups["classes"]?.value.orEmpty()
        val slug = href.trim('/').substringAfterLast('/').takeIf { it.isNotBlank() } ?: return null
        val title = body.firstGroup("<h2[^>]*class=\"(?:news-card|bcard|bhero)-title\"[^>]*>(.*?)</h2>").cleanHtml()
        if (title.isBlank()) return null
        val summary = body.firstGroup("<p[^>]*class=\"(?:news-card-summary|bcard-sum|bhero-sum)\"[^>]*>(.*?)</p>").cleanHtml()
        val badgeMatch = categoryBadgeRegex.find(body)
        val icon = badgeMatch?.groups?.get(1)?.value?.cleanHtml().orEmpty().ifBlank { "info" }
        val rawLabel = badgeMatch?.groups?.get(2)?.value?.cleanHtml().orEmpty()
        val pinned = classes.contains("pinned", ignoreCase = true) || body.contains("news-pin-badge") ||
            rawLabel.equals("Pinned", ignoreCase = true) || icon == "push_pin"
        val categoryLabel = rawLabel.takeUnless { pinned || it.isBlank() } ?: "General"
        val color = body.firstGroup("--cc:\\s*([^;\"]+)")
            .ifBlank { match.value.firstGroup("--cc:\\s*([^;\"]+)") }
            .ifBlank { body.firstGroup("--accent-color:\\s*([^;\"]+)") }
            .ifBlank { categoryLabel.toCategoryColor() }
        val cover = body.firstGroup("<img[^>]*?\\ssrc=\"([^\"]+)\"").absoluteMediaUrl()
        val bodyClean = body.replace(verifiedMark, "")
        val authorBlock = bodyClean.firstGroup("<span[^>]*class=\"news-card-author\"[^>]*>(.*?)</span>")
            .ifBlank { bodyClean.firstGroup("<(?:b|strong)>(.*?)</(?:b|strong)>") }
        val authorPhoto = authorBlock.firstGroup("<img[^>]*\\ssrc=\"([^\"]+)\"").absoluteMediaUrl()
        val authorName = authorBlock.replace(imgTagDotAllRegex, "")
            .cleanHtml().ifBlank { "NEBians Team" }
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
            isPinned = pinned,
            coverImageUrl = cover,
            authorName = authorName,
            authorPhotoUrl = authorPhoto,
            publishedAgo = publishedAgo,
            viewCount = views
        )
    }

    private val firstGroupPatternCache = java.util.concurrent.ConcurrentHashMap<String, Regex>(24)
    private val imgTagDotAllRegex = Regex("<img[^>]*>", RegexOption.DOT_MATCHES_ALL)
    private val brTagRegex = Regex("<br\\s*/?>", RegexOption.IGNORE_CASE)
    private val closePTagRegex = Regex("</p>", RegexOption.IGNORE_CASE)
    private val anyHtmlTagRegex = Regex("<[^>]+>")
    private val inlineTabSpaceRegex = Regex("[ \\t]+")
    private val newlineIndentRegex = Regex("\\n\\s+")
    private val multiNewlineRegex = Regex("\\n{3,}")
    private val scriptBlockRegex = Regex("<script[\\s\\S]*?</script>", RegexOption.IGNORE_CASE)
    private val styleBlockRegex = Regex("<style[\\s\\S]*?</style>", RegexOption.IGNORE_CASE)
    private val boldTagRegex = Regex("<(b|strong)[^>]*>([\\s\\S]*?)</\\1>", RegexOption.IGNORE_CASE)
    private val italicTagRegex = Regex("<(i|em)[^>]*>([\\s\\S]*?)</\\1>", RegexOption.IGNORE_CASE)
    private val strikeTagRegex = Regex("<(s|del|strike)[^>]*>([\\s\\S]*?)</\\1>", RegexOption.IGNORE_CASE)
    private val codeTagRegex = Regex("<code[^>]*>([\\s\\S]*?)</code>", RegexOption.IGNORE_CASE)
    private val anchorTagRegex = Regex("<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>([\\s\\S]*?)</a>", RegexOption.IGNORE_CASE)
    private val imgAltTagRegex = Regex("<img[^>]*alt=[\"']([^\"']*)[\"'][^>]*>", RegexOption.IGNORE_CASE)
    private val imgTagRegex = Regex("<img[^>]*>", RegexOption.IGNORE_CASE)
    private val blockCloseTagRegex = Regex("</(p|div|h1|h2|h3|h4|li|ul|ol|blockquote|pre)>", RegexOption.IGNORE_CASE)
    private val h1TagRegex = Regex("<h1[^>]*>", RegexOption.IGNORE_CASE)
    private val h2TagRegex = Regex("<h2[^>]*>", RegexOption.IGNORE_CASE)
    private val h3TagRegex = Regex("<h3[^>]*>", RegexOption.IGNORE_CASE)
    private val h4TagRegex = Regex("<h4[^>]*>", RegexOption.IGNORE_CASE)
    private val liTagRegex = Regex("<li[^>]*>", RegexOption.IGNORE_CASE)
    private val blockquoteTagRegex = Regex("<blockquote[^>]*>", RegexOption.IGNORE_CASE)
    private val trailingLineSpaceRegex = Regex("[ \\t]+\\n")
    private val timeAgoSpanRegex = Regex("<span[^>]*>([^<]*(?:ago|just now|Yesterday)[^<]*)</span>", RegexOption.IGNORE_CASE)
    private val viewsCountRegex = Regex("([0-9][0-9.,KkMm]*)\\s*views", RegexOption.IGNORE_CASE)
    private val numberCountRegex = Regex("([0-9][0-9.,KkMm]*)")

    private fun String.firstGroup(pattern: String): String {
        val regex = firstGroupPatternCache.getOrPut(pattern) { Regex(pattern, RegexOption.DOT_MATCHES_ALL) }
        return regex.find(this)?.groups?.get(1)?.value.orEmpty()
    }

    private fun String.cleanHtml(): String {
        if (isBlank()) return ""
        val stripped = replace(brTagRegex, "\n")
            .replace(closePTagRegex, "\n\n")
            .replace(anyHtmlTagRegex, " ")
            .replace(inlineTabSpaceRegex, " ")
            .replace(newlineIndentRegex, "\n")
            .replace(multiNewlineRegex, "\n\n")
            .trim()
        return Html.fromHtml(stripped, Html.FROM_HTML_MODE_LEGACY).toString().trim()
    }

    /**
     * Convert the article HTML into real markdown so the reader renders rich
     * formatting (headings, bold/italic/code/strike, blockquotes, lists,
     * clickable links) instead of a flat text dump. Relative link URLs are
     * absolutized against the site origin.
     */
    private fun String.cleanArticleContent(): String {
        if (isBlank()) return ""
        return replace(scriptBlockRegex, "")
            .replace(styleBlockRegex, "")
            // Inline formatting first (before generic tag stripping).
            .replace(boldTagRegex, "**$2**")
            .replace(italicTagRegex, "*$2*")
            .replace(strikeTagRegex, "~~$2~~")
            .replace(codeTagRegex, "`$1`")
            .replace(anchorTagRegex) { m ->
                val href = absolutizeUrl(m.groups[1]?.value.orEmpty())
                val label = m.groups[2]?.value.orEmpty()
                    .replace(anyHtmlTagRegex, "").trim()
                    .ifBlank { href }
                "[$label]($href)"
            }
            .replace(imgAltTagRegex, " $1 ")
            .replace(imgTagRegex, " ")
            // Block structure → markdown blocks.
            .replace(brTagRegex, "\n")
            .replace(blockCloseTagRegex, "\n")
            .replace(h1TagRegex, "\n# ")
            .replace(h2TagRegex, "\n## ")
            .replace(h3TagRegex, "\n### ")
            .replace(h4TagRegex, "\n### ")
            .replace(liTagRegex, "- ")
            .replace(blockquoteTagRegex, "\n> ")
            .replace(anyHtmlTagRegex, "")
            .decodeEntitiesPerLine()
            .replace(trailingLineSpaceRegex, "\n")
            .replace(multiNewlineRegex, "\n\n")
            .trim()
    }

    /**
     * Decode HTML entities without letting the parser flatten the document.
     * [Html.fromHtml] treats newlines as insignificant whitespace, so feeding it
     * the whole article collapses every paragraph, heading and list item into a
     * single run-on line. Decoding line by line keeps the block structure the
     * markdown renderer depends on.
     */
    private fun String.decodeEntitiesPerLine(): String =
        split('\n').joinToString("\n") { line ->
            if (line.isBlank()) "" else Html.fromHtml(line, Html.FROM_HTML_MODE_LEGACY).toString()
        }

    private fun absolutizeUrl(raw: String): String {
        val value = raw.trim()
        if (value.isBlank()) return value
        return when {
            value.startsWith("http://") || value.startsWith("https://") -> value
            value.startsWith("//") -> "https:$value"
            value.startsWith("/") -> "https://nebians.consica.com.np$value"
            value.startsWith("mailto:") || value.startsWith("tel:") -> value
            else -> "https://nebians.consica.com.np/$value"
        }
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
        val matches = timeAgoSpanRegex
            .findAll(this)
            .map { it.groups[1]?.value.orEmpty().cleanHtml() }
            .filter { it.isNotBlank() }
            .toList()
        return matches.lastOrNull().orEmpty()
    }

    private fun String.findViews(): String {
        viewsCountRegex.find(this)?.groups?.get(1)?.value?.let { return it }
        val afterVisibility = substringAfter("visibility", missingDelimiterValue = "")
        return numberCountRegex.find(afterVisibility)?.value.orEmpty()
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
