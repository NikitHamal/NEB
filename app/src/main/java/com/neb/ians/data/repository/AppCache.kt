package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiNotification
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.data.news.NewsAnnouncement
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AppCache @Inject constructor() {
    // Home Screen Cache
    @Volatile var recentResources: List<ApiResource> = emptyList()
    @Volatile var popularResources: List<ApiResource> = emptyList()
    @Volatile var recentPosts: List<ApiPost> = emptyList()
    @Volatile var latestNews: List<NewsAnnouncement> = emptyList()

    // Library Screen Cache
    @Volatile var libraryResources: List<ApiResource> = emptyList()
    @Volatile var libraryTotalCount: Int = 0
    @Volatile var libraryTotalPages: Int = 1
    @Volatile var libraryHasMore: Boolean = false

    // Every resource in every list page lands in resourceDetails, so unbounded these grew for as
    // long as the app stayed open. They keep the most recently added entries; anything older is
    // read from the offline cache or the network, as on a cold start.
    val resourceDetails: MutableMap<String, ApiResource> = boundedMap(400)
    val resourceComments: MutableMap<String, List<ApiResourceComment>> = boundedMap(40)
    val postDetails: MutableMap<String, ApiPost> = boundedMap(200)
    val postReplies: MutableMap<String, List<ApiReply>> = boundedMap(40)

    // Notifications Screen Cache
    @Volatile var notifications: List<ApiNotification> = emptyList()
    @Volatile var notificationsHasMore: Boolean = false
    @Volatile var notificationsPage: Int = 1

    // Last visited profile Cache
    @Volatile var lastProfileUsername: String? = null
    @Volatile var lastProfile: UserProfileResponse? = null
    @Volatile var lastProfileIsFollowing: Boolean = false
    @Volatile var lastProfileIsRequested: Boolean = false
    @Volatile var lastProfileFollowerCount: Int = 0
    @Volatile var lastProfileRepliesCount: Int = 0
    @Volatile var lastProfileResourcesCount: Int = 0
    @Volatile var lastProfilePosts: List<ApiPost> = emptyList()
    @Volatile var lastProfileReplies: List<ApiReply> = emptyList()
    @Volatile var lastProfileResources: List<ApiResource> = emptyList()
}

/** A thread-safe insertion-ordered map that drops its oldest entry past [max] (gets do not reorder it). */
private fun <V> boundedMap(max: Int): MutableMap<String, V> =
    java.util.Collections.synchronizedMap(object : LinkedHashMap<String, V>() {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<String, V>?) = size > max
    })
