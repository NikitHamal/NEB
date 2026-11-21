package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/** GET /api/posts/{id}/insights/. Aggregates only; no viewer is ever named. */
@Serializable
data class ApiPostInsights(
    val postId: String = "",
    val title: String = "",
    val days: Int = 30,
    val createdAt: Long = 0,
    val ageDays: Int = 0,
    val lifetime: InsLifetime = InsLifetime(),
    val kpis: InsKpis = InsKpis(),
    val ctr: Double? = null,
    val engagementRate: Double? = null,
    val bookmarkRate: Double? = null,
    val series: List<InsDay> = emptyList(),
    val hourly: List<Int> = emptyList(),
    val peakHour: Int? = null,
    val peakHourLabel: String = "",
    val audience: InsAudience = InsAudience(),
    val surfaces: List<InsSplit> = emptyList(),
    val channels: List<InsSplit> = emptyList(),
    val devices: List<InsSplit> = emptyList(),
    val os: List<InsSplit> = emptyList(),
    val sources: List<InsSplit> = emptyList(),
    val countries: List<InsSplit> = emptyList(),
    val dwell: InsDwell = InsDwell(),
    val actionsByDevice: Map<String, List<InsSplit>> = emptyMap(),
    val standing: InsStanding = InsStanding(),
    val hasData: Boolean = false,
    val poll: InsPoll? = null,
    val insights: List<InsTip> = emptyList()
)

@Serializable
data class InsLifetime(
    val views: Int = 0, val likes: Int = 0, val replies: Int = 0, val bookmarks: Int = 0,
    val pollVotes: Int = 0, val uniqueViewers: Int = 0, val impressions: Int = 0
)

@Serializable
data class InsKpi(val value: Double = 0.0, val prev: Double = 0.0, val change: Double? = null)

@Serializable
data class InsKpis(
    val views: InsKpi = InsKpi(),
    val uniqueViewers: InsKpi = InsKpi(),
    val impressions: InsKpi = InsKpi(),
    val reactions: InsKpi = InsKpi(),
    val likes: InsKpi = InsKpi(),
    val replies: InsKpi = InsKpi(),
    val avgDwellSec: InsKpi = InsKpi()
)

@Serializable
data class InsDay(
    val date: String = "", val views: Int = 0, val unique: Int = 0, val impressions: Int = 0,
    val likes: Int = 0, val replies: Int = 0, val votes: Int = 0
)

@Serializable
data class InsAudience(
    val members: Int = 0, val guests: Int = 0, val followers: Int = 0,
    val returning: Int = 0, val newViewers: Int = 0,
    val followerPct: Double = 0.0
)

@Serializable
data class InsSplit(val key: String = "", val label: String = "", val count: Int = 0, val pct: Double = 0.0)

@Serializable
data class InsDwell(
    val avgSec: Double = 0.0, val medianSec: Double = 0.0,
    val buckets: List<InsSplit> = emptyList(), val samples: Int = 0
)

@Serializable
data class InsStanding(
    val rank: Int = 0,
    @SerialName("of") val total: Int = 0,
    val medianViews: Int = 0,
    val vsMedian: Double? = null
)

@Serializable
data class InsPoll(
    val id: String = "", val question: String = "", val pollType: String = "voting",
    val allowAddOptions: Boolean = false, val totalVotes: Int = 0, val voters: Int = 0,
    val participation: Double? = null, val options: List<InsPollOption> = emptyList()
)

@Serializable
data class InsPollOption(
    val id: String = "", val text: String = "", val votes: Int = 0, val pct: Double = 0.0,
    val added: Boolean = false, val devices: List<InsSplit> = emptyList()
)

@Serializable
data class InsTip(val tone: String = "info", val title: String = "", val body: String = "")
