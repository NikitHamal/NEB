package com.neb.ians.ui.screens.pathways

import kotlin.math.max
import kotlin.math.pow
import kotlin.math.roundToInt

private fun signal(x: String, r: PwRoute, ix: PwRouteIdx, groups: Map<String, Set<String>>, words: Map<String, List<String>>, idf: Map<String, Float>): Float {
    if (x in r.tags) return 1f
    val g = r.group in groups[x].orEmpty()
    val ws = words[x].orEmpty()
    // keyword hits are weighted by rarity: a word found in few routes is strong evidence, one found everywhere is nearly none
    val hit = ws.filter { it in ix.text }
    val kw = if (hit.isEmpty()) 0f else {
        val all = ws.sumOf { (idf[it] ?: 1f).toDouble() }.toFloat().coerceAtLeast(0.1f)
        0.45f + 0.55f * (hit.sumOf { (idf[it] ?: 1f).toDouble() }.toFloat() / all * 2.5f).coerceAtMost(1f)
    }
    return when { g && kw > 0f -> 0.6f + 0.4f * kw; g -> 0.6f; kw > 0f -> 0.55f * kw; else -> 0f }
}

/** One best signal and the average of all picks, so a single strong hit is not drowned by a third, unrelated pick. */
private fun agg(a: List<Float>): Float = when {
    a.isEmpty() -> 0.5f
    a.none { it > 0f } -> 0f
    else -> 0.15f + 0.85f * (0.5f * a.max() + 0.5f * a.average().toFloat())
}

private fun budgetFit(lo: Long, hi: Long, b: Long): Float = when {
    hi <= b -> 1f
    lo <= b -> 0.4f + 0.6f * (b - lo).toFloat() / (hi - lo).coerceAtLeast(1L).toFloat()
    else -> (0.3f * (1f - (lo - b).toFloat() / lo.coerceAtLeast(1L).toFloat())).coerceAtLeast(0f)
}

/**
 * Ranks every route of one stage. Each answer turns into a 0..1 signal per route (curated tags first, then field and keywords from the
 * route, its skills and the careers it leads to); budget uses the cheapest real provider fee; ease blends competition with the seats
 * and applicants of the entrance exam; outlook follows the demand history of the linked careers. Nothing is hard filtered: a poor fit
 * only sinks, and the reasons say why.
 */
internal fun pwMatch(d: PwData, p: PwProfile): PwMatchResult {
    val pool = d.routes.filter { it.stage == p.stage }
    if (pool.isEmpty()) return PwMatchResult(emptyList(), emptyList(), emptyList(), 0)
    val idx = d.matchIdx
    val maxEntry = pool.maxOf { idx[it.id]?.entryPay ?: 0L }.coerceAtLeast(1L).toFloat()
    val maxSenior = pool.maxOf { idx[it.id]?.seniorPay ?: 0L }.coerceAtLeast(1L).toFloat()
    fun lowFee(r: PwRoute): Long = idx[r.id]?.cheapest?.takeIf { it > 0 }?.let { minOf(it, r.feeMin) } ?: r.feeMin
    val maxFee = pool.maxOf { lowFee(it) }.coerceAtLeast(1L).toFloat()
    val budget = p.budgetLakh * 100_000L
    val out = pool.map { r ->
        val ix = idx.getValue(r.id)
        val m = d.m(r)
        val intr = agg(p.interests.map { signal(it, r, ix, INTEREST_GROUPS, INTEREST_WORDS, d.wordIdf) })
        val strength = agg(p.strengths.map { signal(it, r, ix, STRENGTH_GROUPS, STRENGTH_WORDS, d.wordIdf) }).let { if (p.strengths.isNotEmpty() && it == 0f) 0.1f else it }
        val lo = lowFee(r); val hi = max(r.feeMax, lo)
        val bf = budgetFit(lo, hi, budget)
        val demand = m.demand / 100f
        val ease = 0.5f * (1f - m.competition / 100f) + 0.5f * (if (ix.examOdds >= 0f) ix.examOdds else 1f - m.competition / 100f)
        val pay = 0.4f * ix.entryPay / maxEntry + 0.6f * ix.seniorPay / maxSenior
        val near = when {
            p.district.isBlank() -> 0f
            p.district in ix.districts -> 1f
            DISTRICT_PROVINCE[p.district]?.let { it in ix.provinces } == true -> 0.55f
            else -> 0f
        }
        // abroad: the route's rating, lifted by how many real destinations teach it within the budget for its length
        val years = m.years.coerceAtLeast(1f)
        val reach = if (ix.abroadCosts.isEmpty()) 0f else (ix.abroadCosts.count { it * years <= budget } / ix.abroadCosts.size.coerceAtMost(3).toFloat()).coerceAtMost(1f)
        val abroad = if (ix.abroadCosts.isEmpty()) m.abroad / 100f * 0.7f else 0.4f * m.abroad / 100f + 0.6f * reach
        val pr = mapOf("pay" to pay, "demand" to demand, "ease" to ease, "cost" to 1f - lowFee(r) / maxFee, "abroad" to abroad, "near" to near)
        // entry subjects: the stream the course asks for against the strengths the student named
        val missing = if (p.strengths.isEmpty()) emptyList() else ix.needs.filter { !needMet(it, p.strengths) }
        val elig = when { ix.needs.isEmpty() || p.strengths.isEmpty() -> 1f; missing.isEmpty() -> 1f; missing.size < ix.needs.size -> 0.92f; else -> 0.8f }
        val chosen = p.priorities.filter { it in pr }
        val ps = if (chosen.isEmpty()) (demand + pay) / 2f else chosen.map { pr.getValue(it) }.average().toFloat()
        val yf = if (p.maxYears == 0 || m.years <= p.maxYears) 1f else (1f - (m.years - p.maxYears) / p.maxYears.toFloat()).coerceAtLeast(0f)
        val base = when (p.risk) { "safe" -> 0.4f * demand + 0.6f * ease; "bold" -> 0.4f * demand + 0.6f * pay; else -> demand }
        val outlook = (base + ix.trend * 0.12f).coerceIn(0f, 1f)
        val t = (0.32f * intr + 0.16f * strength + 0.14f * bf + 0.2f * ps + 0.18f * outlook) * (0.7f + 0.3f * yf) * (if (bf < 0.15f) 0.85f else 1f) * elig
        val why = buildList {
            if (p.interests.isNotEmpty() && intr >= 0.6f) add("Fits your interests")
            if (p.strengths.isNotEmpty() && strength >= 0.7f) add("Plays to your strengths")
            if (bf >= 1f) add("In budget")
            chosen.filter { pr.getValue(it) >= 0.7f }.forEach { k -> PRIORITIES.firstOrNull { o -> o.first == k }?.let { o -> add(o.second) } }
            if (ix.needs.isNotEmpty() && p.strengths.isNotEmpty() && missing.isEmpty()) add("Matches the subjects it needs")
            if ("abroad" in chosen && reach > 0f) add("Abroad within budget")
            if (ix.trend >= 0.3f) add("Demand is rising")
        }.take(3)
        val neg = buildList {
            if (bf < 0.4f) add("Fees start at ${npr(lo)}")
            if (yf < 1f) add("Takes ${yearsText(m.years)}")
            if (p.interests.isNotEmpty() && intr < 0.6f) add("Not your interests")
            if (p.strengths.isNotEmpty() && strength < 0.7f) add("Outside your strengths")
            if (missing.isNotEmpty()) add("Needs " + missing.joinToString(" and ") { NEED_LABEL[it] ?: it })
            if (p.risk == "safe" && ease < 0.35f) add("Hard to get into")
        }
        val s = (100f * t.coerceAtLeast(0f).pow(1.8f)).roundToInt().coerceIn(1, 99)
        PwMatch(r, s, why, neg, listOf("Interests" to intr, "Strengths" to strength, "Budget" to bf, "Priorities" to ps, "Outlook" to outlook))
    }.sortedWith(compareByDescending<PwMatch> { it.score }.thenByDescending { d.m(it.route).demand }.thenBy { it.route.feeMin })
    return PwMatchResult(out.filter { it.score >= 65 }, out.filter { it.score in 40..64 }, out.filter { it.score < 40 }, pool.size)
}
