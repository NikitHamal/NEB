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

/** The +2 stream a student finished, asked only at the After +2 stage. Index 0 of the saved number means not answered. */
internal val STREAMS = listOf(
    "pcm" to "Science, Physical group", "pcb" to "Science, Biology group", "mgt" to "Management", "hum" to "Humanities",
    "edu" to "Education", "law" to "Law", "tec" to "Technical",
)
/** Subjects each stream studies, shown under the stream name. Maths is compulsory in the Physical group; Computer Science is an optional subject. */
internal val STREAM_HINT = mapOf(
    "pcm" to "Maths compulsory, Physics, Chemistry, Computer optional", "pcb" to "Physics, Chemistry, Biology",
    "mgt" to "Accountancy, Economics, Business Studies", "hum" to "Sociology, Economics, Media, Population",
    "edu" to "Education and Development", "law" to "Constitutional and Procedural Law", "tec" to "CTEVT or technical stream",
)
/** What the student has finished, in plain words. The stage label itself reads "After ...", which is the wrong way round for a question about now. */
internal fun finishedLabel(s: PwStage): String = when (s.id) {
    "after8" -> "Class 8"
    "after10" -> "Class 10 / SEE"
    "after12" -> "+2 / Class 12"
    "afterbach" -> "Bachelor"
    "aftermaster" -> "Master"
    else -> s.label.removePrefix("After ").removePrefix("a ").replaceFirstChar { it.uppercase() }
}
/** Streams that satisfy each subject need read from an entry text. */
private val STREAM_MEETS = mapOf("sci" to setOf("pcm", "pcb"), "bio" to setOf("pcb"), "math" to setOf("pcm"), "mgmt" to setOf("mgt"))
internal const val STREAM_STAGE = "after12"

internal data class PwProfile(
    val stage: String, val interests: Set<String>, val strengths: Set<String>, val priorities: Set<String>,
    val budgetLakh: Int, val maxYears: Int, val risk: String, val district: String, val stream: String = "",
) {
    /** The stream only counts at the stage that asks for it. */
    val knownStream: String get() = if (stage == STREAM_STAGE) stream else ""
    /** Questions that carry a real answer; the stage and budget always count. */
    val answers: Int get() = 2 + (if (interests.isEmpty()) 0 else 1) + (if (strengths.isEmpty()) 0 else 1) + (if (priorities.isEmpty()) 0 else 1) + (if (knownStream.isEmpty()) 0 else 1)
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
    /** Nepal scholarships open to the level of this course. */
    val aid: Int = 0,
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

/** Subjects the entry text asks for. A note such as "(Maths helps)" or "(or Biology bridge)" is not a requirement; "PCB or PCM" asks for Science only. */
private fun entryNeeds(entry: String): Set<String> {
    val e = entry.lowercase().replace(Regex("\\([^)]*(helps|bridge)[^)]*\\)"), "")
    val both = "pcb or pcm" in e || "pcm or pcb" in e
    val phys = "(physical)" in e
    return buildSet {
        if (("pcb" in e || "biology" in e) && !both) add("bio")
        if ("pcm" in e || "mathematics" in e || "maths" in e || phys) add("math")
        if ("science" in e || "pcm" in e || "pcb" in e || "physics" in e || phys) add("sci")
        if ("management" in e || "commerce" in e || "business studies" in e) add("mgmt")
    }
}

/** Subject needs a student satisfies. A declared stream is exact; without one the strengths stand in for it (science is met by any of maths, science, biology or computers). */
internal fun needMet(need: String, strengths: Set<String>, stream: String = ""): Boolean = when {
    stream.isNotEmpty() -> stream in STREAM_MEETS[need].orEmpty()
    need == "sci" -> strengths.any { it in setOf("math", "sci", "bio", "comp") }
    need == "bio" -> "bio" in strengths
    need == "math" -> "math" in strengths || "comp" in strengths
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
        aid = d.scholarships.count { sc -> sc.scope.equals("nepal", true) && levelKey(r.kind)?.let { it in sc.levels } == true },
        abroadCosts = GROUP_FIELDS[r.group].orEmpty().let { ws ->
            val rn = r.name.lowercase()
            d.abroad.filter { a -> a.fields.any { f -> val fl = f.lowercase(); ws.any { fieldHit(fl, it) } || (fl.length > 3 && fl in rn) } }
                .map { it.tuitionMin + it.livingMin }.filter { it > 0 }.sorted()
        },
    )
}

/** The scholarship level word a course kind belongs to. */
private fun levelKey(kind: String): String? = when (kind.lowercase()) {
    "bachelor" -> "bachelor"; "master" -> "master"; "diploma", "technical", "professional" -> "diploma"; else -> null
}
