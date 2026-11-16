package com.neb.ians.ui.screens.pathways

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
internal val INTEREST_HINT = mapOf(
    "build" to "Making and fixing things", "heal" to "Helping people get well", "num" to "Data, money, patterns", "ppl" to "Teaching, leading, talking",
    "make" to "Design, art, media", "law" to "Rules, fairness, debate", "nature" to "Land, plants, outdoors", "serve" to "Public service, community",
)
internal val PRIORITY_HINT = mapOf(
    "pay" to "A bigger salary", "demand" to "Plenty of jobs open", "ease" to "Easier to get in", "cost" to "Lower fees",
    "abroad" to "Chances overseas", "near" to "Colleges close to me",
)
internal val RISKS = listOf(
    Triple("safe", "Play it safe", "Courses where getting in is realistic"),
    Triple("mid", "Balanced", "A mix of safe and ambitious"),
    Triple("bold", "Aim high", "Tough entry is fine if the payoff is big"),
)

internal val INTEREST_GROUPS = mapOf(
    "build" to setOf("tech", "sci"), "heal" to setOf("health"), "num" to setOf("biz", "sci", "tech"), "ppl" to setOf("edu", "biz", "arts", "gov"),
    "make" to setOf("arts", "tech"), "law" to setOf("law", "gov"), "nature" to setOf("ag", "sci"), "serve" to setOf("gov", "edu", "health"),
)
internal val STRENGTH_GROUPS = mapOf(
    "math" to setOf("tech", "sci", "biz"), "sci" to setOf("sci", "tech", "health", "ag"), "bio" to setOf("health", "ag"),
    "lang" to setOf("arts", "law", "edu", "gov"), "biz" to setOf("biz"), "comp" to setOf("tech"), "art" to setOf("arts"),
)
/** Words that show up in a course name, its about line, its skills or the careers it leads to. */
internal val INTEREST_WORDS = mapOf(
    "build" to listOf("build", "engineer", "construct", "machine", "civil", "mechanic", "electric", "software", "repair", "survey"),
    "heal" to listOf("health", "patient", "clinic", "nurs", "medic", "pharma", "care", "dental", "therap"),
    "num" to listOf("account", "finance", "statist", "data", "audit", "bank", "math", "econom", "actuar"),
    "ppl" to listOf("teach", "people", "manage", "communicat", "lead", "counsel", "social", "hospitality", "educat"),
    "make" to listOf("design", "art", "media", "creative", "film", "music", "architect", "journal", "fashion"),
    "law" to listOf("law", "legal", "court", "justice", "policy", "police", "judge"),
    "nature" to listOf("agricultur", "forest", "environment", "plant", "animal", "land", "veterin", "fisher", "hydro"),
    "serve" to listOf("public", "govern", "service", "community", "army", "police", "civil"),
)
internal val STRENGTH_WORDS = mapOf(
    "math" to listOf("math", "statist", "account", "data", "physics"),
    "sci" to listOf("science", "physic", "chem", "lab", "research"),
    "bio" to listOf("biolog", "anatomy", "patient", "clinic", "agricultur", "nurs"),
    "lang" to listOf("english", "writing", "communicat", "nepali", "language", "journal"),
    "biz" to listOf("business", "finance", "account", "market", "sales", "manage"),
    "comp" to listOf("program", "computer", "coding", "software", "data", "network"),
    "art" to listOf("design", "draw", "creative", "art", "media"),
)

internal data class PwProfile(
    val stage: String, val interests: Set<String>, val strengths: Set<String>, val priorities: Set<String>,
    val budgetLakh: Int, val maxYears: Int, val risk: String, val district: String,
) {
    /** Questions that carry a real answer, out of the six; the stage and budget always count. */
    val answers: Int get() = 2 + (if (interests.isEmpty()) 0 else 1) + (if (strengths.isEmpty()) 0 else 1) + (if (priorities.isEmpty()) 0 else 1)
}

internal data class PwMatch(val route: PwRoute, val score: Int, val why: List<String>, val neg: List<String>, val parts: List<Pair<String, Float>>)
internal data class PwMatchResult(val strong: List<PwMatch>, val possible: List<PwMatch>, val weak: List<PwMatch>, val pool: Int) {
    val good get() = strong.size + possible.size
    val all get() = strong + possible + weak
}

/** Facts about a route that never change with the answers, computed once per data load. */
internal class PwRouteIdx(
    val text: String, val groups: Set<String>, val trend: Float, val cheapest: Long,
    val examOdds: Float, val districts: Set<String>, val provinces: Set<Int>, val entryPay: Long, val seniorPay: Long,
    /** School subjects the entry text asks for: "sci", "bio", "math", "mgmt". */
    val needs: Set<String> = emptySet(),
    /** Cheapest yearly cost (tuition plus living, NPR) of each study-abroad destination that teaches this field. */
    val abroadCosts: List<Long> = emptyList(),
)

/** Study-abroad field names (as the dataset spells them) each route group is taught under. */
private val GROUP_FIELDS = mapOf(
    "tech" to listOf("engineering", "it", "computer", "data science", "renewable", "architecture", "aviation"),
    "biz" to listOf("business", "management", "economics", "hospitality", "tourism"),
    "health" to listOf("medicine", "nursing", "public health", "pharmacy"),
    "sci" to listOf("physics", "water", "nuclear", "data science"),
    "ag" to listOf("agriculture"), "arts" to listOf("design", "music", "arts", "architecture"),
    "law" to listOf("law", "social"), "edu" to listOf("education", "social"), "gov" to listOf("public", "social", "economics"),
)

private fun fieldHit(field: String, w: String): Boolean = field == w || field.startsWith("$w ") || (w.length >= 4 && w in field)

private fun entryNeeds(entry: String): Set<String> {
    val e = entry.lowercase()
    return buildSet {
        if ("pcb" in e || "biology" in e) add("bio")
        if ("pcm" in e || "mathematics" in e || "maths" in e) add("math")
        if ("science" in e || "pcm" in e || "pcb" in e || "physics" in e) add("sci")
        if ("management" in e || "commerce" in e || "business studies" in e) add("mgmt")
    }
}

/** Subject needs a student's strengths satisfy: science is met by any of maths, science, biology or computers. */
internal fun needMet(need: String, strengths: Set<String>): Boolean = when (need) {
    "sci" -> strengths.any { it in setOf("math", "sci", "bio", "comp") }
    "bio" -> "bio" in strengths
    "math" -> "math" in strengths || "comp" in strengths
    else -> "biz" in strengths
}
internal val NEED_LABEL = mapOf("sci" to "Science", "bio" to "Biology", "math" to "Maths", "mgmt" to "Management")

/** How rare each match keyword is across the routes: a word in every course says little, a rare word says a lot. */
internal fun buildWordIdf(d: PwData): Map<String, Float> {
    val texts = d.matchIdx.values.map { it.text }
    val n = texts.size.coerceAtLeast(1)
    return (INTEREST_WORDS.values + STRENGTH_WORDS.values).flatten().distinct().associateWith { w ->
        val df = texts.count { w in it }
        (kotlin.math.ln((n + 1f) / (df + 1f)) + 0.4f).coerceAtLeast(0.2f)
    }
}

internal fun buildMatchIndex(d: PwData): Map<String, PwRouteIdx> = d.routes.associate { r ->
    val cs = r.careers.mapNotNull { d.careers[it] }
    val provs = r.where.mapNotNull { d.providers[it] }
    val trends = cs.map { k ->
        if (k.history.size >= 3) ((k.history.last() - k.history.first()).toFloat() / (k.history.size - 1) / 6f).coerceIn(-1f, 1f)
        else when (k.trend.lowercase()) { "rising" -> 0.5f; "falling" -> -0.5f; else -> 0f }
    }
    val exam = d.govtById[r.examId]
    val odds = if (exam != null && exam.seats > 0 && exam.applicants > 0) (exam.seats.toFloat() / exam.applicants * 1.6f).coerceIn(0f, 1f) else -1f
    val m = d.m(r)
    r.id to PwRouteIdx(
        text = (r.name + " " + r.about + " " + r.skills.joinToString(" ") + " " + cs.joinToString(" ") { it.name + " " + it.skills.joinToString(" ") }).lowercase(),
        groups = setOf(r.group), trend = if (trends.isEmpty()) 0f else trends.average().toFloat(),
        cheapest = provs.flatMap { p -> p.fees[r.id]?.first?.takeIf { it > 0 }?.let { listOf(it) }.orEmpty() }.minOrNull() ?: 0L,
        examOdds = odds, districts = provs.map { it.district }.toSet(), provinces = provs.mapNotNull { DISTRICT_PROVINCE[it.district] }.toSet(),
        entryPay = (m.payLo + m.payHi) / 2, seniorPay = m.senior,
        needs = entryNeeds(r.entry),
        abroadCosts = GROUP_FIELDS[r.group].orEmpty().let { ws ->
            val rn = r.name.lowercase()
            d.abroad.filter { a -> a.fields.any { f -> val fl = f.lowercase(); ws.any { fieldHit(fl, it) } || (fl.length > 3 && fl in rn) } }
                .map { it.tuitionMin + it.livingMin }.filter { it > 0 }.sorted()
        },
    )
}
