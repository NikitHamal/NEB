package com.neb.ians.ui.screens.pathways

import kotlin.math.roundToInt

internal val INTERESTS = listOf(
    "build" to "Building", "heal" to "Healing", "num" to "Numbers", "ppl" to "People",
    "make" to "Creating", "law" to "Justice", "nature" to "Nature", "serve" to "Serving",
)
internal val STRENGTHS = listOf(
    "math" to "Maths", "sci" to "Science", "bio" to "Biology", "lang" to "Languages", "biz" to "Business", "comp" to "Computers", "art" to "Art",
)
internal val PRIORITIES = listOf(
    "pay" to "Pay", "demand" to "Demand", "ease" to "Easy entry", "cost" to "Low cost", "abroad" to "Abroad", "near" to "Near me",
)

private val INTEREST_GROUPS = mapOf(
    "build" to setOf("tech", "sci"), "heal" to setOf("health"), "num" to setOf("biz", "sci", "tech"), "ppl" to setOf("edu", "biz", "arts", "gov"),
    "make" to setOf("arts", "tech"), "law" to setOf("law", "gov"), "nature" to setOf("ag", "sci"), "serve" to setOf("gov", "edu", "health"),
)
private val STRENGTH_GROUPS = mapOf(
    "math" to setOf("tech", "sci", "biz"), "sci" to setOf("sci", "tech", "health", "ag"), "bio" to setOf("health", "ag"),
    "lang" to setOf("arts", "law", "edu", "gov"), "biz" to setOf("biz"), "comp" to setOf("tech"), "art" to setOf("arts"),
)
private val SKILL_HINTS = mapOf(
    "comp" to listOf("program", "computer", "coding", "software", "data"), "math" to listOf("math", "statist", "account"),
    "bio" to listOf("biology", "anatomy", "patient", "clinical"), "lang" to listOf("english", "writing", "nepali", "communication"),
    "art" to listOf("design", "drawing", "creative"), "biz" to listOf("finance", "account", "market", "sales"),
)

internal data class PwProfile(
    val stage: String, val interests: Set<String>, val strengths: Set<String>, val budgetLakh: Int, val priorities: Set<String>, val district: String,
)
internal data class PwMatch(val route: PwRoute, val score: Int, val reasons: List<String>)

/**
 * Ranks every route of a stage for one student. Interests and strengths weigh most, then priorities, budget and demand.
 * Route "tags" in the data override the group based guess, so curated data always wins over inference.
 */
internal fun pwMatch(d: PwData, p: PwProfile, limit: Int = 8): List<PwMatch> {
    val pool = d.routes.filter { it.stage == p.stage }
    if (pool.isEmpty()) return emptyList()
    val maxSenior = pool.maxOf { d.m(it).senior }.coerceAtLeast(1L).toFloat()
    val maxFee = pool.maxOf { it.feeMin }.coerceAtLeast(1L).toFloat()
    val budget = p.budgetLakh * 100_000L
    return pool.map { r ->
        val m = d.m(r)
        val tags = r.tags.toSet()
        val text = (r.skills + r.name + r.about).joinToString(" ").lowercase()
        val iHits = p.interests.count { it in tags || r.group in INTEREST_GROUPS[it].orEmpty() }
        val sHits = p.strengths.count { s -> s in tags || r.group in STRENGTH_GROUPS[s].orEmpty() || SKILL_HINTS[s].orEmpty().any { it in text } }
        val interest = when {
            p.interests.isEmpty() -> 0.5f
            iHits == 0 -> 0f
            else -> 0.6f + 0.4f * iHits / p.interests.size
        }
        val strength = when {
            p.strengths.isEmpty() -> 0.5f
            sHits == 0 -> 0.1f
            else -> 0.7f + 0.3f * sHits / p.strengths.size
        }
        val budgetFit = when {
            r.feeMax <= budget -> 1f
            r.feeMin <= budget -> 0.4f + 0.6f * (budget - r.feeMin).toFloat() / (r.feeMax - r.feeMin).coerceAtLeast(1L).toFloat()
            else -> (0.3f * (1f - (r.feeMin - budget).toFloat() / r.feeMin.coerceAtLeast(1L).toFloat())).coerceAtLeast(0f)
        }
        val near = p.district.isNotEmpty() && r.where.any { d.providers[it]?.district == p.district }
        val prio = mapOf(
            "pay" to m.senior / maxSenior, "demand" to m.demand / 100f, "ease" to 1f - m.competition / 100f,
            "cost" to 1f - r.feeMin / maxFee, "abroad" to m.abroad / 100f, "near" to if (near) 1f else 0f,
        )
        val chosen = p.priorities.filter { it in prio }
        val prioScore = if (chosen.isEmpty()) (prio.getValue("demand") + prio.getValue("pay")) / 2f else chosen.map { prio.getValue(it) }.average().toFloat()
        val total = 0.36f * interest + 0.18f * strength + 0.16f * budgetFit + 0.22f * prioScore + 0.08f * m.demand / 100f
        val reasons = buildList {
            if (p.interests.isNotEmpty() && interest >= 0.6f) add("Interests")
            if (p.strengths.isNotEmpty() && strength >= 0.7f) add("Strengths")
            if (budgetFit >= 1f) add("In budget")
            chosen.filter { prio.getValue(it) >= 0.7f }.forEach { k -> PRIORITIES.firstOrNull { it.first == k }?.let { add(it.second) } }
        }.take(3)
        PwMatch(r, (total * 100).roundToInt().coerceIn(1, 99), reasons)
    }.sortedByDescending { it.score }.take(limit)
}
