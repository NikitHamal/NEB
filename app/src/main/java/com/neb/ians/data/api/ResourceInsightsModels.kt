package com.neb.ians.data.api

import kotlinx.serialization.Serializable

/**
 * GET /api/resources/{id}/insights/ and GET /api/uploads/insights/. One lenient shape for both:
 * the per-resource payload fills `lifetime` and `standing`, the all-uploads payload fills
 * `totals`, `resources`, `subjects` and `posts`. Aggregates only; no viewer is ever named.
 */
@Serializable
data class ApiResourceInsights(
    val resourceId: String = "",
    val title: String = "",
    val subject: String = "",
    val gradeLevel: String = "",
    val days: Int = 30,
    val ageDays: Int = 0,
    val kpis: ResKpis = ResKpis(),
    val ctr: Double? = null,
    val readRate: Double? = null,
    val downloadRate: Double? = null,
    val funnel: List<InsSplit> = emptyList(),
    val series: List<ResDay> = emptyList(),
    val hourly: List<Int> = emptyList(),
    val peakHourLabel: String = "",
    val audience: ResAudience = ResAudience(),
    val surfaces: List<InsSplit> = emptyList(),
    val channels: List<InsSplit> = emptyList(),
    val devices: List<InsSplit> = emptyList(),
    val sources: List<InsSplit> = emptyList(),
    val countries: List<InsSplit> = emptyList(),
    val classes: List<InsSplit> = emptyList(),
    val dwell: InsDwell = InsDwell(),
    val push: ResPush = ResPush(),
    val hasData: Boolean = false,
    val lifetime: ResLifetime? = null,
    val standing: ResStanding? = null,
    val totals: ResTotals? = null,
    val resources: List<ResRow> = emptyList(),
    val subjects: List<InsSplit> = emptyList(),
    val posts: ResPosts? = null,
    val insights: List<InsTip> = emptyList()
)

@Serializable
data class ResKpis(
    val views: InsKpi = InsKpi(),
    val uniqueViewers: InsKpi = InsKpi(),
    val impressions: InsKpi = InsKpi(),
    val reads: InsKpi = InsKpi(),
    val downloads: InsKpi = InsKpi(),
    val shares: InsKpi = InsKpi(),
    val saves: InsKpi = InsKpi(),
    val comments: InsKpi = InsKpi(),
    val avgDwellSec: InsKpi = InsKpi()
)

@Serializable
data class ResDay(
    val date: String = "", val views: Int = 0, val unique: Int = 0, val reads: Int = 0,
    val downloads: Int = 0, val impressions: Int = 0
)

@Serializable
data class ResAudience(
    val members: Int = 0, val guests: Int = 0, val returning: Int = 0, val newViewers: Int = 0
)

@Serializable
data class ResPush(
    val announced: Int = 0, val notified: Int = 0, val views: Int = 0,
    val shareOfViews: Double? = null, val taps: Int = 0
)

@Serializable
data class ResLifetime(
    val views: Int = 0, val likes: Int = 0, val comments: Int = 0, val downloads: Int = 0,
    val bookmarks: Int = 0, val uniqueViewers: Int = 0, val impressions: Int = 0
)

@Serializable
data class ResStanding(
    val rank: Int = 0, val of: Int = 0, val medianViews: Int = 0, val vsMedian: Double? = null
)

@Serializable
data class ResTotals(
    val resources: Int = 0, val live: Int = 0, val pending: Int = 0, val views: Int = 0,
    val likes: Int = 0, val comments: Int = 0, val downloads: Int = 0
)

@Serializable
data class ResRow(
    val id: String = "", val title: String = "", val subject: String = "", val gradeLevel: String = "",
    val status: String = "", val views: Int = 0, val unique: Int = 0, val reads: Int = 0,
    val downloads: Int = 0, val shares: Int = 0, val impressions: Int = 0,
    val avgDwellSec: Double = 0.0, val lifetimeViews: Int = 0
)

@Serializable
data class ResPosts(
    val count: Int = 0, val views: Int = 0, val change: Double? = null,
    val likes: Int = 0, val replies: Int = 0, val top: List<ResPostRow> = emptyList()
)

@Serializable
data class ResPostRow(
    val id: String = "", val title: String = "", val views: Int = 0, val lifetimeViews: Int = 0,
    val likes: Int = 0, val replies: Int = 0
)
