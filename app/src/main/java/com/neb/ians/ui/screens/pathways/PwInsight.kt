package com.neb.ians.ui.screens.pathways

/** Numbers shown on cards, all derived from the careers a route leads to. Pure functions, no state. */

internal fun routeCareers(d: PwData, r: PwRoute): List<PwCareer> = r.careers.mapNotNull { d.careers[it] }

internal fun demandScore(d: PwData, r: PwRoute): Float = routeCareers(d, r).map { it.demand }.average().let { if (it.isNaN()) 0f else it.toFloat() }

internal fun competitionScore(d: PwData, r: PwRoute): Float = routeCareers(d, r).map { it.competition }.average().let { if (it.isNaN()) 0f else it.toFloat() }

internal fun demandWord(v: Float): String = when { v <= 0f -> "Open"; v >= 3.7f -> "High"; v >= 2.7f -> "Medium"; else -> "Steady" }

internal fun competitionWord(v: Float): String = when { v <= 0f -> "Open"; v >= 3.7f -> "High"; v >= 2.7f -> "Medium"; else -> "Low" }

/** Entry pay, monthly NPR: average of the lowest and of the highest starting figure across its careers. */
internal fun payText(d: PwData, r: PwRoute): String {
    val cs = routeCareers(d, r)
    if (cs.isEmpty()) return "Varies"
    val lo = cs.map { it.entryMin }.average().toLong()
    val hi = cs.map { it.entryMax }.average().toLong()
    return "${money(lo)} to ${money(hi)}"
}

/** Years as a number: "5.5 years" 5.5, "6 to 24 months" 0.5, "3 or 5 years" 3. */
internal fun yearsNum(text: String): Float {
    val n = Regex("""\d+(\.\d+)?""").find(text)?.value?.toFloatOrNull() ?: return 4f
    return if (text.contains("month", ignoreCase = true)) n / 12f else n
}

/** Short monogram for a tile: "(CSIT)" in the name, else a short first word, else initials. */
internal fun shortCode(name: String): String {
    Regex("""\(([A-Za-z.]{2,6})\)""").find(name)?.let { return it.groupValues[1].uppercase() }
    val head = name.substringBefore("(").trim()
    val first = head.split(" ", "/").firstOrNull().orEmpty()
    if (first.length in 2..5 && first.any { it.isUpperCase() }) return first.uppercase()
    return head.split(" ").filter { it.firstOrNull()?.isUpperCase() == true }.take(3).joinToString("") { it.take(1) }.ifEmpty { head.take(2).uppercase() }
}

internal fun stageWord(label: String): String = label.removePrefix("After ").let { if (it == "Bachelor") "Bachelor's" else it }

internal data class PwHits(val routes: List<PwRoute>, val careers: List<PwCareer>, val providers: List<PwProvider>, val govt: List<PwGovt>) {
    val empty get() = routes.isEmpty() && careers.isEmpty() && providers.isEmpty() && govt.isEmpty()
}

/** Every word of the query must appear in the name (or district for colleges). Prefix hits rank first, so nothing unrelated shows. */
internal fun pwSearch(d: PwData, query: String): PwHits {
    val words = query.lowercase().split(" ", ",").filter { it.length >= 2 }
    if (words.isEmpty()) return PwHits(emptyList(), emptyList(), emptyList(), emptyList())
    fun <T> pick(items: Collection<T>, text: (T) -> String, limit: Int): List<T> =
        items.mapNotNull { x ->
            val t = text(x).lowercase()
            if (words.all { it in t }) Pair(x, if (t.startsWith(words[0])) 0 else if (" ${words[0]}" in t) 1 else 2) else null
        }.sortedBy { it.second }.take(limit).map { it.first }
    return PwHits(
        routes = pick(d.routes, { it.name + " " + (GROUP_LABEL[it.group] ?: "") }, 8),
        careers = pick(d.careers.values, { it.name }, 6),
        providers = pick(d.providers.values, { it.name + " " + it.district + " " + it.place }, 8),
        govt = pick(d.govt, { it.name + " " + it.body }, 4),
    )
}
