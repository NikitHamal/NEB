package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * `GET api/users/me/analytics/?days=7|30|90` (v2). Every field has a default so an older or
 * newer server never breaks the screen. Field meanings: backend_python/docs/ANALYTICS.md.
 */
@Serializable
data class ApiPrivateAnalyticsResponse(
    val username: String = "",
    val version: Int = 0,
    val range: ApiAnalyticsRange = ApiAnalyticsRange(),
    val standing: ApiAnalyticsStanding = ApiAnalyticsStanding(),
    val stats: ApiAnalyticsStats = ApiAnalyticsStats(),
    val overview: List<ApiAnalyticsKpi> = emptyList(),
    val trend: List<ApiAnalyticsTrendDay> = emptyList(),
    val streak: ApiAnalyticsStreak = ApiAnalyticsStreak(),
    val heatmap: ApiAnalyticsHeatmap = ApiAnalyticsHeatmap(),
    val rhythm: ApiAnalyticsRhythm = ApiAnalyticsRhythm(),
    val mix: List<ApiAnalyticsMix> = emptyList(),
    val reach: ApiAnalyticsReach = ApiAnalyticsReach(),
    val helpfulness: ApiAnalyticsHelpfulness = ApiAnalyticsHelpfulness(),
    val library: ApiAnalyticsLibrary = ApiAnalyticsLibrary(),
    val milestones: List<ApiAnalyticsMilestone> = emptyList(),
    val insights: List<ApiAnalyticsInsight> = emptyList(),
    @SerialName("topCategories") val topCategories: List<ApiAnalyticsTopic> = emptyList(),
    @SerialName("topSubjects") val topSubjects: List<ApiAnalyticsTopic> = emptyList(),
    @SerialName("topPosts") val topPosts: List<ApiAnalyticsPost> = emptyList(),
    @SerialName("topResources") val topResources: List<ApiAnalyticsResource> = emptyList()
)

@Serializable
data class ApiAnalyticsRange(
    val days: Int = 30,
    val from: String = "",
    val to: String = "",
    val options: List<Int> = listOf(7, 30, 90)
)

@Serializable
data class ApiAnalyticsStanding(
    val score: Int = 0,
    val level: Int = 1,
    val levelName: String = "",
    val levelFloor: Int = 0,
    val nextLevelAt: Int? = null,
    val nextLevelName: String = "",
    val progress: Int = 0,
    val topPercent: Int? = null,
    val memberSince: Long = 0
)

@Serializable
data class ApiAnalyticsStats(
    val posts: Int = 0,
    val replies: Int = 0,
    val postViews: Int = 0,
    val postLikesReceived: Int = 0,
    val postRepliesReceived: Int = 0,
    val resources: Int = 0,
    val resourceViews: Int = 0,
    val resourceLikesReceived: Int = 0,
    val resourceCommentsReceived: Int = 0,
    val resourceCommentsMade: Int = 0,
    val followers: Int = 0,
    val following: Int = 0,
    val bookmarks: Int = 0,
    val notificationsUnread: Int = 0,
    val recentPosts: Int = 0,
    val recentReplies: Int = 0,
    val contributionScore: Int = 0,
    val likesGiven: Int = 0
)

@Serializable
data class ApiAnalyticsKpi(
    val key: String = "",
    val label: String = "",
    val value: Int = 0,
    val previous: Int = 0,
    /** Whole-percent change against the previous period; null when there was nothing to compare. */
    val change: Int? = null,
    val series: List<Int> = emptyList()
)

@Serializable
data class ApiAnalyticsTrendDay(
    val date: String = "",
    val label: String = "",
    val weekday: String = "",
    val posts: Int = 0,
    val replies: Int = 0,
    val resources: Int = 0,
    val comments: Int = 0,
    val reads: Int = 0,
    val likes: Int = 0,
    val responses: Int = 0,
    val followers: Int = 0,
    val actions: Int = 0
)

@Serializable
data class ApiAnalyticsStreak(
    val current: Int = 0,
    val longest: Int = 0,
    val activeToday: Boolean = false,
    val atRisk: Boolean = false,
    val activeDays30: Int = 0
)

@Serializable
data class ApiAnalyticsHeatCell(
    val date: String = "",
    val count: Int = 0,
    /** 0 to 4; -1 is a day that has not happened yet. */
    val level: Int = 0
)

@Serializable
data class ApiAnalyticsHeatmap(
    val weeks: Int = 17,
    val start: String = "",
    val max: Int = 0,
    val cells: List<ApiAnalyticsHeatCell> = emptyList()
)

@Serializable
data class ApiAnalyticsRhythm(
    val hours: List<Int> = emptyList(),
    val weekdays: List<Int> = emptyList(),
    val total: Int = 0,
    val peakHour: Int? = null,
    val peakHourLabel: String = "",
    val peakWeekday: Int? = null,
    val peakWeekdayLabel: String = ""
)

@Serializable
data class ApiAnalyticsMix(
    val key: String = "",
    val label: String = "",
    val count: Int = 0
)

@Serializable
data class ApiAnalyticsReach(
    val views: Int = 0,
    val postViews: Int = 0,
    val resourceViews: Int = 0,
    val likes: Int = 0,
    val replies: Int = 0,
    val resourceComments: Int = 0,
    val engagementRate: Double = 0.0,
    val avgViewsPerPost: Int = 0,
    val avgViewsPerResource: Int = 0,
    val uniqueReaders: Int = 0,
    val readersPrevious: Int = 0
)

@Serializable
data class ApiAnalyticsCount(
    val key: String = "",
    val count: Int = 0
)

@Serializable
data class ApiAnalyticsHelpfulness(
    val answersWritten: Int = 0,
    val kinds: List<ApiAnalyticsCount> = emptyList(),
    val labels: List<ApiAnalyticsCount> = emptyList(),
    val goodLabels: Int = 0,
    val solvedPosts: Int = 0
)

@Serializable
data class ApiAnalyticsSaved(
    val posts: Int = 0,
    val replies: Int = 0,
    val resources: Int = 0
)

@Serializable
data class ApiAnalyticsLibrary(
    val saved: ApiAnalyticsSaved = ApiAnalyticsSaved(),
    val likesGiven: Int = 0,
    val resourceLikesGiven: Int = 0
)

@Serializable
data class ApiAnalyticsMilestone(
    val id: String = "",
    val title: String = "",
    val progress: Int = 0,
    val target: Int = 1,
    val done: Boolean = false
)

@Serializable
data class ApiAnalyticsInsight(
    val id: String = "",
    /** good, info or action. */
    val tone: String = "info",
    val title: String = "",
    val body: String = ""
)

@Serializable
data class ApiAnalyticsTopic(
    val label: String = "",
    val count: Int = 0,
    val width: Int = 0
)

@Serializable
data class ApiAnalyticsPost(
    val id: String = "",
    val title: String = "",
    val category: String = "",
    @SerialName("view_count") val viewCount: Int = 0,
    @SerialName("like_count") val likeCount: Int = 0,
    @SerialName("reply_count") val replyCount: Int = 0,
    @SerialName("created_at") val createdAt: Long = 0
)

@Serializable
data class ApiAnalyticsResource(
    val id: String = "",
    val title: String = "",
    val subject: String = "",
    val type: String = "",
    @SerialName("view_count") val viewCount: Int = 0,
    @SerialName("like_count") val likeCount: Int = 0,
    @SerialName("comment_count") val commentCount: Int = 0,
    @SerialName("added_at") val addedAt: Long = 0
)
