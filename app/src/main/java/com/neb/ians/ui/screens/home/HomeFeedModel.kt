package com.neb.ians.ui.screens.home

import androidx.compose.runtime.Immutable
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.repository.FollowStateRepository

/**
 * The home feed as a flat list of typed entries.
 *
 * The screen used to nest every interstitial — the resource carousel, the news
 * strip, the people rail — inside the lazy item of the post it followed, which
 * meant one lazy item could be a card or a card plus a whole carousel, and the
 * list could never reuse a slot. Flattening them into siblings gives every row
 * one content type, so scrolling reuses compositions instead of rebuilding
 * them, and puts the cadence itself in one readable place.
 */
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
    data class Peers(val peers: List<ApiPost>) : HomeFeedEntry {
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

private const val HIGHLIGHT_START = 9
private const val HIGHLIGHT_EVERY = 5
private const val MAX_PEERS = 8

/**
 * People worth suggesting: real, not the viewer, not a bot, and not already
 * followed according to either the post payload or the local follow graph.
 */
fun suggestedPeersFrom(
    posts: List<ApiPost>,
    currentUserId: String?,
    followGraph: FollowStateRepository.Graph
): List<ApiPost> = posts.asSequence()
    .filter { post ->
        post.authorName.isNotBlank() &&
            post.authorId.isNotBlank() &&
            post.authorId != currentUserId &&
            !post.isAnonymous &&
            !post.authorIsBot &&
            !post.authorName.contains("Anonymous", ignoreCase = true) &&
            post.isFollowingAuthor != true &&
            !followGraph.contains(post.authorId, post.authorName)
    }
    .distinctBy { it.authorId }
    .take(MAX_PEERS)
    .toList()

/**
 * Interleaves posts with the standing interstitials at their anchor positions.
 *
 * An interstitial whose anchor is past the end of a short feed is appended
 * instead of dropped — a five-post feed should still surface the library and
 * the people rail rather than showing five cards and stopping.
 */
fun buildHomeFeed(
    posts: List<ApiPost>,
    currentUserId: String?,
    suggestedResources: List<ApiResource>,
    recentResources: List<ApiResource>,
    news: List<NewsAnnouncement>,
    peers: List<ApiPost>
): List<HomeFeedEntry> {
    val uniquePosts = posts.distinctBy { it.id }
    if (uniquePosts.isEmpty()) return emptyList()

    val anchored = buildList {
        if (suggestedResources.isNotEmpty()) {
            add(0 to HomeFeedEntry.ResourceCarousel(suggestedResources))
        }
        if (news.isNotEmpty()) add(2 to HomeFeedEntry.News(news))
        if (peers.isNotEmpty()) add(4 to HomeFeedEntry.Peers(peers))
        if (suggestedResources.isNotEmpty()) {
            add(6 to HomeFeedEntry.ResourceHighlight(suggestedResources.first(), 6, titled = true))
        }
        if (recentResources.isNotEmpty()) add(8 to HomeFeedEntry.NewResources(recentResources))
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
        if (index > HIGHLIGHT_START &&
            (index - HIGHLIGHT_START) % HIGHLIGHT_EVERY == 0 &&
            suggestedResources.isNotEmpty()
        ) {
            val resource = suggestedResources[(index / HIGHLIGHT_EVERY) % suggestedResources.size]
            entries += HomeFeedEntry.ResourceHighlight(resource, index, titled = false)
        }
    }

    anchored.forEach { (anchor, entry) ->
        if (anchor !in placed) entries += entry
    }

    return entries
}
