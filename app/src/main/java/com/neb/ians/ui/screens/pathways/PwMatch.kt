package com.neb.ians.ui.screens.pathways

/**
 * Course Lab matching. Rules, in order, so nothing irrelevant can appear:
 * 1. only routes of the chosen level, and only courses (no school or language-visa routes);
 * 2. stream gate for After +2 (a route that needs Science is never shown to a Management student);
 * 3. hard budget and time gates on the cheapest realistic fee and the shortest duration;
 * 4. interest fit: the answers build a taste vector over eight dimensions, each route has a vector from its group and name;
 * 5. a route must score at least 55% of the best route and an absolute floor, then a small priority bonus orders ties.
 */
internal val MATCH_DIMS = listOf("Building things", "Caring for people", "Business and money", "Law and public service", "Creative work", "Nature and fieldwork", "Teaching and society", "Hands on technical skill")

internal class PwOption(val label: String, val w: Map<Int, Float> = emptyMap(), val cap: Float = 0f, val tag: String = "")
internal class PwQuestion(val title: String, val kind: String, val options: List<PwOption>)

private fun o(label: String, vararg w: Pair<Int, Float>) = PwOption(label, w.toMap())

internal val MATCH_QUESTIONS = listOf(
    PwQuestion("Which task would you happily do for an hour?", "taste", listOf(
        o("Fix a gadget or write some code", 0 to 3f, 7 to 1f), o("Help someone feel better", 1 to 3f, 6 to 1f),
        o("Plan a budget or run a small shop", 2 to 3f), o("Draw, design or write a story", 4 to 3f),
        o("Work with plants, animals or soil", 5 to 3f, 7 to 1f), o("Explain something to a friend", 6 to 3f, 3 to 1f),
    )),
    PwQuestion("Which subject feels easiest?", "taste", listOf(
        o("Maths and computer", 0 to 2f, 2 to 1f), o("Biology and chemistry", 1 to 2f, 5 to 1f), o("Accountancy and economics", 2 to 2f),
        o("English and social studies", 3 to 2f, 6 to 1f, 4 to 1f), o("Art and languages", 4 to 2f, 6 to 1f), o("Practical and workshop work", 7 to 2f, 5 to 1f),
    )),
    PwQuestion("Where do you picture yourself working?", "taste", listOf(
        o("Office or lab with computers", 0 to 1f, 2 to 1f), o("Hospital, clinic or classroom", 1 to 2f, 6 to 2f),
        o("Field, farm or building site", 5 to 2f, 7 to 2f), o("Studio or creative space", 4 to 2f), o("Government office or court", 3 to 2f, 2 to 1f),
    )),
    PwQuestion("How much can the whole course cost?", "budget", listOf(
        PwOption("Under NPR 2 lakh", cap = 200_000f), PwOption("Up to NPR 6 lakh", cap = 600_000f),
        PwOption("Up to NPR 15 lakh", cap = 1_500_000f), PwOption("No limit", cap = Float.MAX_VALUE),
    )),
    PwQuestion("How long can you study before earning?", "time", listOf(
        PwOption("Up to 2 years", cap = 2f), PwOption("Up to 4 years", cap = 4f), PwOption("Up to 6 years", cap = 6f), PwOption("As long as needed", cap = 99f),
    )),
    PwQuestion("What matters most after you finish?", "goal", listOf(
        PwOption("Earn early", tag = "early"), PwOption("A stable job", tag = "stable"), PwOption("Work abroad", tag = "abroad"), PwOption("Serve society", tag = "serve"),
    )),
)

internal class PwMatchHit(val route: PwRoute, val score: Int, val reasons: List<String>)

private val KEYS = listOf(
    0 to Regex("""\b(computer|software|data|civil|electrical|electronics|mechanical|architecture|engineering|it|csit|bit|bca|geomatics|aerospace)\b"""),
    1 to Regex("""\b(nursing|pharm\w*|medicine|medical|dental|health|physiotherapy|optometry|laboratory|ayurved\w*|mbbs|bds)\b"""),
    2 to Regex("""\b(account\w*|bank\w*|finance|business|management|hotel|tourism|insurance|bba|bbs|bbm|bim|acca)\b"""),
    3 to Regex("""\b(law|llb|public|police|army|civil service|administration|lok)\b"""),
    4 to Regex("""\b(design|media|journalism|music|fine|film|fashion|arts?|bfa|bjmc)\b"""),
    5 to Regex("""\b(agriculture|forestry|environmental?|veterinary|geology|food|microbiology|biotechnology)\b"""),
    6 to Regex("""\b(education|teaching|teacher|social|humanities|bed|bsw)\b"""),
    7 to Regex("""\b(technician|diploma|skill|electrician|plumbing|mechanic|training|pilot|pre-diploma)\b"""),
)

private fun routeVector(r: PwRoute): FloatArray {
    val v = FloatArray(8)
    when (r.group) {
        "tech" -> { v[0] = 0.9f; v[7] = 0.3f }
        "sci" -> { v[5] = 0.6f; v[0] = 0.5f; v[6] = 0.2f }
        "health" -> { v[1] = 1f; v[5] = 0.2f }
        "biz" -> { v[2] = 1f; v[3] = 0.2f }
        "arts" -> { v[4] = 1f; v[6] = 0.3f }
        "edu" -> { v[6] = 1f; v[1] = 0.2f }
        "law" -> { v[3] = 1f; v[2] = 0.2f }
        "ag" -> { v[5] = 1f; v[7] = 0.4f }
        "gov" -> { v[3] = 0.8f; v[7] = 0.3f }
        else -> v.fill(0.2f)
    }
    val name = r.name.lowercase()
    KEYS.forEach { (dim, re) -> if (re.containsMatchIn(name)) v[dim] = minOf(1f, v[dim] + 0.3f) }
    if (r.kind == "Diploma" || r.kind == "Technical") v[7] = minOf(1f, v[7] + 0.4f)
    return v
}

internal fun streamOk(r: PwRoute, stream: String): Boolean {
    val e = r.entry.lowercase()
    if (!e.contains("+2") && !e.contains("any")) return false
    if (e.contains("any stream")) return true
    val needs = buildList {
        if (e.contains("science")) add("science")
        if (e.contains("management") || e.contains("commerce")) add("management")
        if (e.contains("humanities")) add("humanities")
    }
    return needs.isEmpty() || stream in needs
}

internal fun matchRoutes(d: PwData, stage: String, stream: String, answers: List<Int>): List<PwMatchHit> {
    val taste = FloatArray(8)
    var budget = Float.MAX_VALUE; var time = 99f; var goal = ""
    MATCH_QUESTIONS.forEachIndexed { i, q ->
        val opt = q.options.getOrNull(answers.getOrNull(i) ?: -1) ?: return@forEachIndexed
        when (q.kind) {
            "taste" -> opt.w.forEach { (k, w) -> taste[k] += w }
            "budget" -> budget = opt.cap
            "time" -> time = opt.cap
            "goal" -> goal = opt.tag
        }
    }
    val total = taste.sum().takeIf { it > 0f } ?: return emptyList()
    for (k in 0 until 8) taste[k] /= total
    val pool = d.routes.filter { r ->
        r.stage == stage && r.group != "school" && r.group != "abroad" &&
            (stage != "after12" || streamOk(r, stream)) && r.feeMin <= budget && yearsNum(r.years) <= time + 0.01f
    }
    val scored = pool.map { r ->
        val v = routeVector(r)
        var s = 0f
        for (k in 0 until 8) s += taste[k] * v[k]
        Triple(r, s, v)
    }
    val top = scored.maxOfOrNull { it.second } ?: return emptyList()
    if (top < 0.12f) return emptyList()
    return scored.filter { it.second >= top * 0.55f && it.second >= 0.1f }.map { (r, s, v) ->
        val cs = routeCareers(d, r)
        val bonus = when (goal) {
            "early" -> (4f - yearsNum(r.years)).coerceIn(-1f, 2f) * 0.012f
            "stable" -> (3f - competitionScore(d, r)).coerceIn(-1f, 2f) * 0.01f + demandScore(d, r) * 0.008f
            "abroad" -> (cs.map { it.abroad }.average().takeIf { !it.isNaN() } ?: 0.0).toFloat() * 0.015f
            "serve" -> (v[1] + v[6] + v[3]) * 0.03f
            else -> 0f
        }
        val reasons = (0 until 8).filter { taste[it] * v[it] > 0.06f }.sortedByDescending { taste[it] * v[it] }.take(2).map { MATCH_DIMS[it] }
        PwMatchHit(r, ((s / top) * 90f + bonus * 100f).toInt().coerceIn(40, 99), reasons)
    }.sortedByDescending { it.score }.take(6)
}
