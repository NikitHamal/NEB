package com.neb.ians.ui.screens.pathways

import java.util.Calendar
import kotlin.math.roundToInt

internal data class PwMetrics(val demand: Int, val competition: Int, val payLo: Long, val payHi: Long, val senior: Long, val abroad: Int, val years: Float)

/** The source data rates demand, competition and abroad from 1 to 5; screens work in 0 to 100. */
internal fun pct(v: Int): Int = if (v in 1..5) v * 20 else v.coerceIn(0, 100)

internal fun routeMetrics(d: PwData, r: PwRoute): PwMetrics {
    val cs = r.careers.mapNotNull { d.careers[it] }
    fun avgI(f: (PwCareer) -> Int): Int = if (cs.isEmpty()) 50 else cs.map(f).average().roundToInt()
    fun avgL(f: (PwCareer) -> Long): Long = if (cs.isEmpty()) 0L else cs.map(f).average().toLong()
    return PwMetrics(
        demand = if (r.demand > 0) pct(r.demand) else avgI { pct(it.demand) },
        competition = if (r.competition > 0) pct(r.competition) else avgI { pct(it.competition) },
        payLo = avgL { it.entryMin }, payHi = avgL { it.entryMax }, senior = avgL { (it.seniorMin + it.seniorMax) / 2 },
        abroad = avgI { pct(it.abroad) }, years = yearsOf(r.years),
    )
}

internal fun PwData.m(r: PwRoute): PwMetrics = metrics[r.id] ?: routeMetrics(this, r)

internal fun yearsOf(s: String): Float {
    val n = Regex("""\d+(\.\d+)?""").find(s)?.value?.toFloatOrNull() ?: return 0f
    return if (s.contains("month", ignoreCase = true)) n / 12f else n
}

internal fun yearsText(y: Float): String = when {
    y <= 0f -> ""
    y < 1f -> "${(y * 12).roundToInt()} mo"
    else -> trim(y.toDouble()) + " yr"
}

internal fun yearsBadge(y: Float): Pair<String, String> = when {
    y <= 0f -> "" to ""
    y < 1f -> "${(y * 12).roundToInt()}" to "months"
    else -> trim(y.toDouble()) to if (y == 1f) "year" else "years"
}

internal fun npr(n: Long): String = if (n <= 0L) "Free" else "NPR ${money(n)}"

internal fun payAt(k: PwCareer, y: Float): Float {
    val e = (k.entryMin + k.entryMax) / 2f
    val s = (k.seniorMin + k.seniorMax) / 2f
    val mid = e + (s - e) * 0.45f
    return if (y <= 5f) e + (mid - e) * y / 5f else mid + (s - mid) * ((y - 5f) / 7f).coerceAtMost(1f)
}

internal val GROUP_LABEL = mapOf(
    "school" to "School", "tech" to "Engineering and IT", "sci" to "Science", "health" to "Health", "biz" to "Business",
    "arts" to "Arts and media", "edu" to "Education", "law" to "Law", "ag" to "Agriculture", "gov" to "Government", "abroad" to "Abroad",
)
internal fun groupLabel(g: String): String = GROUP_LABEL[g] ?: g.replaceFirstChar { it.uppercase() }
internal fun groupToneIndex(g: String): Int = when (g) {
    "tech", "sci" -> 0
    "arts", "law" -> 1
    "biz", "edu", "gov" -> 2
    "health", "ag", "abroad" -> 4
    else -> 3
}

internal fun shortStage(label: String): String =
    label.removePrefix("After ").removePrefix("a ").removePrefix("Class ").replaceFirstChar { it.uppercase() }

internal val PROVINCES = listOf("Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim")
internal val DISTRICT_PROVINCE: Map<String, Int> = buildMap {
    listOf(
        "Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang", "Okhaldhunga", "Panchthar", "Sankhuwasabha", "Solukhumbu", "Sunsari", "Taplejung", "Terhathum", "Udayapur",
    ).forEach { put(it, 0) }
    listOf("Bara", "Dhanusha", "Mahottari", "Parsa", "Rautahat", "Saptari", "Sarlahi", "Siraha").forEach { put(it, 1) }
    listOf(
        "Bhaktapur", "Chitwan", "Dhading", "Dolakha", "Kathmandu", "Kavrepalanchok", "Lalitpur", "Makwanpur", "Nuwakot", "Ramechhap", "Rasuwa", "Sindhuli", "Sindhupalchok",
    ).forEach { put(it, 2) }
    listOf("Baglung", "Gorkha", "Kaski", "Lamjung", "Manang", "Mustang", "Myagdi", "Nawalparasi East", "Parbat", "Syangja", "Tanahu").forEach { put(it, 3) }
    listOf("Arghakhanchi", "Banke", "Bardiya", "Dang", "Gulmi", "Kapilvastu", "Nawalparasi West", "Palpa", "Pyuthan", "Rolpa", "Rukum East", "Rupandehi").forEach { put(it, 4) }
    listOf("Dailekh", "Dolpa", "Humla", "Jajarkot", "Jumla", "Kalikot", "Mugu", "Rukum West", "Salyan", "Surkhet").forEach { put(it, 5) }
    listOf("Achham", "Baitadi", "Bajhang", "Bajura", "Dadeldhura", "Darchula", "Doti", "Kailali", "Kanchanpur").forEach { put(it, 6) }
}

internal val MONTHS = listOf("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
internal fun nowMonth(): Int = Calendar.getInstance().get(Calendar.MONTH) + 1
internal fun monthsIn(text: String): Set<Int> {
    val t = text.lowercase()
    return MONTHS.mapIndexedNotNull { i, m -> if (Regex("""\b${m.lowercase()}""").containsMatchIn(t)) i + 1 else null }.toSet()
}
internal fun inWindow(from: Int, to: Int, m: Int): Boolean = if (from <= to) m in from..to else m >= from || m <= to
internal fun windowLabel(from: Int, to: Int): String = if (inWindow(from, to, nowMonth())) "Closes ${MONTHS[to - 1]}" else "Opens ${MONTHS[from - 1]}"
internal fun monthsUntil(from: Int, to: Int): Int = if (inWindow(from, to, nowMonth())) -1 else (from - nowMonth() + 12) % 12

internal val EDU_LABELS = listOf("Class 8", "SEE", "+2", "Bachelor", "Master")
internal fun eduOf(need: String): Int {
    val t = need.lowercase()
    return when {
        "master" in t -> 4
        "bachelor" in t || "graduate" in t || "degree" in t -> 3
        "+2" in t || "plus two" in t || "class 12" in t || "higher secondary" in t -> 2
        Regex("""\bsee\b|\bslc\b|class 10""").containsMatchIn(t) -> 1
        else -> 0
    }
}

/** "18 to 35 years, up to 40 for women" gives min 18, max 35, max for women 40. */
internal fun ageOf(age: String): Triple<Int, Int, Int>? {
    val n = Regex("""\d+""").findAll(age).map { it.value.toInt() }.toList()
    return if (n.size >= 2) Triple(n[0], n[1], n.getOrElse(2) { n[1] }) else null
}
internal fun ageText(age: String): String = ageOf(age)?.let { (lo, hi, w) -> if (w > hi) "$lo–$hi, women $w" else "$lo–$hi" } ?: age

internal fun whyNot(g: PwGovt, edu: Int, age: Int, woman: Boolean): String {
    val need = eduOf(g.need)
    if (edu < need) return "Needs ${EDU_LABELS[need]}"
    val a = ageOf(g.age) ?: return ""
    val max = if (woman) a.third else a.second
    return if (age < a.first || age > max) "Age ${a.first}–$max" else ""
}

internal fun prepHoursOf(g: PwGovt): Int = if (g.prepHours > 0) g.prepHours else when (eduOf(g.need)) { 0, 1 -> 500; 2 -> 700; else -> 900 }

internal data class PwOdds(val text: String, val big: String, val pre: String, val post: String, val ratio: Float)
internal fun oddsOf(g: PwGovt): PwOdds? {
    if (g.seats <= 0 || g.applicants <= 0) return null
    val r = g.applicants.toFloat() / g.seats
    return if (r >= 20f) {
        val n = r.roundToInt()
        PwOdds("1 in $n", "$n", "1 in", "", r)
    } else {
        val n = (100f / r).roundToInt().coerceAtMost(100)
        PwOdds("$n in 100", "$n", "", "in 100", r)
    }
}

internal fun linkLabel(link: String): String = when (link.substringBefore(":")) {
    "exam" -> "Exam"
    "route" -> "Course"
    "career" -> "Career"
    "guide" -> "Guide"
    else -> "Open"
}

internal data class PwHit(val kind: String, val id: String, val title: String, val sub: String)

internal fun pwSearch(d: PwData, q: String): List<PwHit> {
    val words = q.lowercase().split(" ").filter { it.length >= 2 }
    if (words.isEmpty()) return emptyList()
    fun hit(vararg s: String): Boolean { val t = s.joinToString(" ").lowercase(); return words.all { it in t } }
    val out = mutableListOf<PwHit>()
    d.routes.filter { hit(it.name, it.kind, it.about) }.forEach { out += PwHit("Course", it.id, it.name, groupLabel(it.group)) }
    d.careers.values.filter { hit(it.name, it.about) }.forEach { out += PwHit("Career", it.id, it.name, "NPR ${money(it.entryMin)}–${money(it.seniorMax)} / month") }
    d.govt.filter { hit(it.name, it.body, it.level) }.forEach { out += PwHit("Exam", it.id, it.name, it.body) }
    d.guides.filter { hit(it.name, it.cat) }.forEach { out += PwHit("Guide", it.id, it.name, it.cat) }
    d.providers.values.filter { hit(it.name, it.place, it.district) }.forEach { out += PwHit("College", it.id, it.name, it.district) }
    d.scholarships.filter { hit(it.name, it.by) }.forEach { out += PwHit("Scholarship", it.id, it.name, it.by) }
    d.abroad.filter { hit(it.country) }.forEach { out += PwHit("Country", it.id, it.country, "NPR ${money(it.tuitionMin + it.livingMin)} / year") }
    d.faq.filter { hit(it.q) }.forEach { out += PwHit("Question", it.id, it.q, "") }
    return out.take(80)
}
