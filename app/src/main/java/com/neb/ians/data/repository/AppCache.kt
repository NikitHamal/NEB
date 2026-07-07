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
    var recentResources: List<ApiResource> = emptyList()
    var popularResources: List<ApiResource> = emptyList()
    var recentPosts: List<ApiPost> = emptyList()
    var latestNews: List<NewsAnnouncement> = emptyList()
    
    // Library Screen Cache
    var libraryResources: List<ApiResource> = emptyList()
    var libraryTotalCount: Int = 0
    var libraryTotalPages: Int = 1
    var libraryHasMore: Boolean = false
    
    // Forum Screen Cache
    var forumPosts: List<ApiPost> = emptyList()
    var forumHasMore: Boolean = false
    var forumPage: Int = 1

    var resourceDetails: MutableMap<String, ApiResource> = mutableMapOf()
    var resourceComments: MutableMap<String, List<ApiResourceComment>> = mutableMapOf()
    var postDetails: MutableMap<String, ApiPost> = mutableMapOf()
    var postReplies: MutableMap<String, List<ApiReply>> = mutableMapOf()
    
    // Notifications Screen Cache
    var notifications: List<ApiNotification> = emptyList()
    var notificationsHasMore: Boolean = false
    var notificationsPage: Int = 1

    // Last visited profile Cache
    var lastProfileUsername: String? = null
    var lastProfile: UserProfileResponse? = null
    var lastProfileIsFollowing: Boolean = false
    var lastProfileIsRequested: Boolean = false
    var lastProfileFollowerCount: Int = 0
    var lastProfileRepliesCount: Int = 0
    var lastProfileResourcesCount: Int = 0
    var lastProfilePosts: List<ApiPost> = emptyList()
    var lastProfileReplies: List<ApiReply> = emptyList()
    var lastProfileResources: List<ApiResource> = emptyList()
}
