package com.neb.ians.ui.screens.home

import androidx.compose.runtime.Immutable
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.repository.PersonSuggestion
import kotlin.math.ln
import kotlin.math.max
import kotlin.math.min
import kotlin.math.pow

@Immutable
sealed interface HomeFeedEntry {
    val key: String
    val contentType: String

    @Immutable
    data class Post(val post: ApiPost, val isOwnPost: Boolean) : HomeFeedEntry {
        override val key: String get() = "post_${post.id}"
        override val contentType: String get() = TYPE_POST
    }

    @Immutable
    data class ResourceCarousel(val resources: List<ApiResource>) : HomeFeedEntry {
        override val key: String get() = "suggested_resources"
        override val contentType: String get() = TYPE_RESOURCE_CAROUSEL
    }

    @Immutable
    data class News(val items: List<NewsAnnouncement>) : HomeFeedEntry {
        override val key: String get() = "news"
        override val contentType: String get() = TYPE_NEWS
    }

    @Immutable
    data class Peers(val peers: List<PersonSuggestion>) : HomeFeedEntry {
        override val key: String get() = "peers"
        override val contentType: String get() = TYPE_PEERS
    }

    @Immutable
    data class ResourceHighlight(
        val resource: ApiResource,
        val slot: Int,
        val titled: Boolean
    ) : HomeFeedEntry {
        override val key: String get() = "highlight_${slot}_${resource.id}"
        override val contentType: String get() = TYPE_HIGHLIGHT
    }

    @Immutable
    data class NewResources(val resources: List<ApiResource>) : HomeFeedEntry {
        override val key: String get() = "new_resources"
        override val contentType: String get() = TYPE_NEW_RESOURCES
    }

    companion object {
        const val TYPE_POST = "post"
        const val TYPE_RESOURCE_CAROUSEL = "resource_carousel"
        const val TYPE_NEWS = "news"
        const val TYPE_PEERS = "peers"
        const val TYPE_HIGHLIGHT = "highlight"
        const val TYPE_NEW_RESOURCES = "new_resources"
    }
}

private const val HIGHLIGHT_START = 12
private const val HIGHLIGHT_EVERY = 6

private val ACADEMIC_CATEGORIES = setOf(
    "physics", "chemistry", "mathematics", "biology",
    "computer science", "english", "nepali", "accountancy",
    "economics", "exam tips"
)

fun rankHomeFeedPosts(
    posts: List<ApiPost>,
    sort: String,
    currentUserId: String?,
    nowMs: Long = System.currentTimeMillis()
): List<ApiPost> {
    val unique = posts.distinctBy { it.id }
    if (unique.size <= 1) return unique
    return when (sort) {
        "new" -> unique.sortedByDescending { it.createdAt }
        "top" -> unique.sortedWith(compareByDescending<ApiPost> { it.thumbsUpCount }.thenByDescending { it.replyCount }.thenByDescending { it.createdAt })
        "discussed" -> unique.sortedWith(compareByDescending<ApiPost> { it.replyCount }.thenByDescending { it.thumbsUpCount }.thenByDescending { it.createdAt })
        else -> {
            val baseScores = unique.associateWith { p ->
                val ageHours = max(0.0, (nowMs - p.createdAt).toDouble() / 3_600_000.0)
                val engagement = p.thumbsUpCount * 3.2 + p.replyCount * 4.2 + min(p.viewCount, 1500) * 0.08
                val engScore = if (engagement > 0.0) ln(1.0 + engagement) * 2.2 else 0.0
                val freshnessBoost = if (ageHours < 6.0) (1.0 - ageHours / 6.0) * 2.4 else 0.0
                val gravity = (ageHours + 2.5).pow(0.45) + (ageHours / 72.0)
                val isOwn = p.isOwner || (currentUserId != null && p.authorId == currentUserId)
                val socialBoost = when {
                    isOwn && ageHours < 1.0 -> 3.0
                    p.isFollowingAuthor == true -> 2.1
                    else -> 0.0
                }
                val catLower = p.category.trim().lowercase()
                val qualityBoost = (if (catLower in ACADEMIC_CATEGORIES) 0.65 else 0.0) +
                    (if (p.images.isNotEmpty() || p.attachments.isNotEmpty() || p.poll != null) 0.55 else 0.0) +
                    (if (p.content.length >= 140) 0.35 else 0.0)
                val seenPenalty = if (p.isThumbedUp && ageHours > 4.0) 0.5 else 0.0
                (engScore + freshnessBoost + socialBoost + qualityBoost - seenPenalty) - gravity * 0.55
            }
            val remaining = unique.toMutableList()
            val authorCounts = HashMap<String, Int>()
            val ranked = ArrayList<ApiPost>(unique.size)
            while (remaining.isNotEmpty()) {
                var bestIdx = 0
                var bestScore = Double.NEGATIVE_INFINITY
                for (i in remaining.indices) {
                    val candidate = remaining[i]
                    val authorKey = candidate.authorId.ifBlank { candidate.authorName }
                    val priorByAuthor = authorCounts[authorKey] ?: 0
                    val adjusted = (baseScores[candidate] ?: 0.0) - priorByAuthor * 1.35
                    if (adjusted > bestScore) {
                        bestScore = adjusted
                        bestIdx = i
                    }
                }
                val picked = remaining.removeAt(bestIdx)
                val authorKey = picked.authorId.ifBlank { picked.authorName }
                authorCounts[authorKey] = (authorCounts[authorKey] ?: 0) + 1
                ranked.add(picked)
            }
            ranked
        }
    }
}

fun buildHomeFeed(
    posts: List<ApiPost>,
    currentUserId: String?,
    suggestedResources: List<ApiResource>,
    recentResources: List<ApiResource>,
    news: List<NewsAnnouncement>,
    peers: List<PersonSuggestion>,
    sort: String = "hot",
    selectedCategory: String? = null
): List<HomeFeedEntry> {
    val uniquePosts = posts.distinctBy { it.id }
    if (uniquePosts.isEmpty()) return emptyList()

    val isDefaultFeed = selectedCategory == null && sort == "hot"
    val matchingResources = if (selectedCategory != null) {
        suggestedResources.filter {
            it.subject.contains(selectedCategory, ignoreCase = true) ||
                it.title.contains(selectedCategory, ignoreCase = true)
        }.ifEmpty { suggestedResources }
    } else {
        suggestedResources
    }

    val anchored = buildList {
        if (isDefaultFeed) {
            if (matchingResources.isNotEmpty()) {
                add(1 to HomeFeedEntry.ResourceCarousel(matchingResources))
            }
            if (news.isNotEmpty()) add(3 to HomeFeedEntry.News(news))
            if (peers.isNotEmpty()) add(5 to HomeFeedEntry.Peers(peers))
            if (matchingResources.isNotEmpty()) {
                add(7 to HomeFeedEntry.ResourceHighlight(matchingResources.first(), 7, titled = true))
            }
            if (recentResources.isNotEmpty()) add(10 to HomeFeedEntry.NewResources(recentResources))
        } else if (selectedCategory != null && matchingResources.isNotEmpty()) {
            add(2 to HomeFeedEntry.ResourceCarousel(matchingResources))
        }
    }

    val entries = ArrayList<HomeFeedEntry>(uniquePosts.size + anchored.size + 4)
    val placed = HashSet<Int>(anchored.size)

    uniquePosts.forEachIndexed { index, post ->
        entries += HomeFeedEntry.Post(
            post = post,
            isOwnPost = post.isOwner || (currentUserId != null && post.authorId == currentUserId)
        )
        anchored.forEach { (anchor, entry) ->
            if (anchor == index) {
                entries += entry
                placed += anchor
            }
        }
        if (isDefaultFeed &&
            index >= HIGHLIGHT_START &&
            (index - HIGHLIGHT_START) % HIGHLIGHT_EVERY == 0 &&
            matchingResources.isNotEmpty()
        ) {
            val resource = matchingResources[(index / HIGHLIGHT_EVERY) % matchingResources.size]
            entries += HomeFeedEntry.ResourceHighlight(resource, index, titled = false)
        }
    }

    anchored.forEach { (anchor, entry) ->
        if (anchor !in placed) entries += entry
    }

    return entries
}
