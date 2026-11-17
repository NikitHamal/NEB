package com.neb.ians.ui.screens.pathways

import android.content.Context
import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import javax.inject.Inject

/** A labelled share or value, used for splits, syllabus weights, quotas and pay ladders. Schema: docs/PATHWAYS_SCHEMA.md */
data class PwPart(val label: String, val value: Float)
data class PwStage(val id: String, val label: String, val icon: String, val blurb: String, val tip: String)
data class PwRoute(
    val id: String, val stage: String, val name: String, val kind: String, val group: String, val years: String,
    val feeMin: Long, val feeMax: Long, val entry: String, val about: String, val exam: String,
    val careers: List<String>, val skills: List<String>, val next: List<String>, val where: List<String>,
    val plan: List<String> = emptyList(), val tags: List<String> = emptyList(), val examId: String = "",
    val demand: Int = 0, val competition: Int = 0,
)
data class PwCareer(
    val id: String, val name: String, val about: String, val demand: Int, val competition: Int, val trend: String,
    val abroad: Int, val entryMin: Long, val entryMax: Long, val seniorMin: Long, val seniorMax: Long,
    val skills: List<String> = emptyList(), val ladder: List<String> = emptyList(), val day: List<PwPart> = emptyList(),
    val jobs: List<PwPart> = emptyList(), val employers: List<String> = emptyList(), val traits: Map<String, Int> = emptyMap(),
    val hours: Int = 0, val history: List<Int> = emptyList(), val licence: String = "", val licenceExam: String = "",
)
data class PwProvider(
    val id: String, val name: String, val kind: String, val sector: String, val district: String, val place: String, val note: String,
    val website: String = "", val fees: Map<String, Pair<Long, Long>> = emptyMap(), val seats: Int = 0,
)
data class PwScholarship(
    val id: String, val name: String, val scope: String, val levels: List<String>, val by: String, val covers: String, val who: String, val how: String,
    val link: String = "", val country: String = "", val type: String = "", val open: List<Int> = emptyList(), val awards: Int = 0,
)
data class PwAbroad(
    val id: String, val country: String, val tuitionMin: Long, val tuitionMax: Long, val livingMin: Long, val livingMax: Long,
    val exams: List<String>, val intakes: String, val fields: List<String>, val work: String, val note: String, val scholarships: List<String> = emptyList(),
    val code: String = "", val visaRate: Int = -1, val workHours: Int = -1, val stayBack: String = "", val visa: PwVisa? = null,
)
/** One step of the student visa: [days] is the usual wait, [cost] is text in the embassy currency, [mode] is online, in person or empty. */
data class PwVisaStep(val name: String, val days: Int, val cost: String, val mode: String, val note: String)
data class PwVisa(val name: String, val steps: List<PwVisaStep>)
data class PwExamStage(val name: String, val detail: String, val marks: String)
data class PwGovt(
    val id: String, val track: String, val name: String, val level: String, val need: String, val age: String, val body: String,
    val stages: List<PwExamStage>, val subjects: List<String>, val prep: List<String>, val note: String,
    val seats: Int = 0, val applicants: Int = 0, val fee: Long = 0, val apply: List<Int> = emptyList(), val examMonth: Int = 0,
    val prepHours: Int = 0, val syllabus: List<PwPart> = emptyList(), val quota: List<PwPart> = emptyList(),
    val ladder: List<PwPart> = emptyList(), val rung: Int = -1, val career: String = "", val pay: Long = 0,
)
data class PwStep(val title: String, val days: Int, val cost: Long, val online: Boolean)
data class PwGuide(val id: String, val name: String, val cat: String, val steps: List<PwStep>, val docs: List<String>, val link: String)
data class PwTopic(val id: String, val label: String, val group: String = "gov")
data class PwFaq(val id: String, val topic: String, val q: String, val a: String, val go: List<String>)
data class PwData(
    val reviewed: String, val stages: List<PwStage>, val routes: List<PwRoute>, val careers: Map<String, PwCareer>,
    val providers: Map<String, PwProvider>, val scholarships: List<PwScholarship>, val abroad: List<PwAbroad>,
    val topics: List<PwTopic> = emptyList(), val faq: List<PwFaq> = emptyList(),
    val govtTracks: List<PwTopic> = emptyList(), val govtGroups: List<PwTopic> = emptyList(), val govt: List<PwGovt> = emptyList(), val guides: List<PwGuide> = emptyList(),
) {
    val routeById: Map<String, PwRoute> by lazy { routes.associateBy { it.id } }
    val govtById: Map<String, PwGovt> by lazy { govt.associateBy { it.id } }
    val guideById: Map<String, PwGuide> by lazy { guides.associateBy { it.id } }
    val careerRoutes: Map<String, List<PwRoute>> by lazy { routes.flatMap { r -> r.careers.map { it to r } }.groupBy({ it.first }, { it.second }) }
    internal val matchIdx: Map<String, PwRouteIdx> by lazy { buildMatchIndex(this) }
    internal val wordIdf: Map<String, Float> by lazy { buildWordIdf(this) }
    private val memo = object : LinkedHashMap<PwProfile, PwMatchResult>(8, 0.75f, true) { override fun removeEldestEntry(e: MutableMap.MutableEntry<PwProfile, PwMatchResult>) = size > 6 }
    /** Ranking is a pure function of the data and the answers: coming back to the Match tab with the same answers costs nothing. */
    internal fun matchMemo(p: PwProfile, run: () -> PwMatchResult): PwMatchResult = synchronized(memo) { memo[p] } ?: run().also { synchronized(memo) { memo[p] = it } }
    internal val metrics: Map<String, PwMetrics> by lazy { routes.associate { it.id to routeMetrics(this, it) } }
    val maxSenior: Long by lazy { careers.values.maxOfOrNull { (it.seniorMin + it.seniorMax) / 2 }?.coerceAtLeast(1L) ?: 1L }
}

private fun JSONArray?.strings(): List<String> = if (this == null) emptyList() else List(length()) { optString(it) }.filter { it.isNotEmpty() }
private fun JSONArray?.ints(): List<Int> = if (this == null) emptyList() else List(length()) { optInt(it) }
private fun JSONArray?.parts(): List<PwPart> = if (this == null) emptyList() else List(length()) { i ->
    optJSONArray(i)?.let { PwPart(it.optString(0), it.optDouble(1, 0.0).toFloat()) }
}.filterNotNull().filter { it.label.isNotEmpty() }
private inline fun <T> JSONArray.mapObjs(f: (JSONObject) -> T): List<T> = List(length()) { f(getJSONObject(it)) }
private fun JSONObject?.intMap(): Map<String, Int> = if (this == null) emptyMap() else keys().asSequence().associateWith { optInt(it) }

/**
 * A server that has not been redeployed yet answers without the exam groups, the entrance and language exams or the
 * route to exam links. The app ships that wave (`assets/pathways_wave17.json`) and fills the gap, so the Government,
 * Entrance and Language segments never depend on the deploy. A newer server already carries `govt_groups`, so nothing is merged.
 */
private fun mergeWave17(o: JSONObject, wave: JSONObject) {
    if (o.has("govt_groups")) return
    o.put("govt_groups", wave.getJSONArray("govt_groups"))
    fun append(key: String, more: JSONArray) {
        val base = o.optJSONArray(key) ?: JSONArray().also { o.put(key, it) }
        val have = HashSet<String>().also { set -> for (i in 0 until base.length()) set.add(base.getJSONObject(i).optString("id")) }
        for (i in 0 until more.length()) more.getJSONObject(i).let { if (have.add(it.optString("id"))) base.put(it) }
    }
    append("govt_tracks", wave.getJSONArray("govt_tracks_add"))
    append("govt", wave.getJSONArray("govt_add"))
    val links = wave.optJSONObject("route_exam")
    val routes = o.optJSONArray("routes")
    if (links != null && routes != null) for (i in 0 until routes.length()) {
        val r = routes.getJSONObject(i)
        if (r.optString("exam_id").isEmpty() && links.has(r.optString("id"))) r.put("exam_id", links.getString(r.optString("id")))
    }
}

internal fun parsePathways(text: String, wave17: JSONObject? = null): PwData {
    val o = JSONObject(text)
    if (wave17 != null) runCatching { mergeWave17(o, wave17) }
    return PwData(
        reviewed = o.optString("reviewed"),
        stages = o.getJSONArray("stages").mapObjs { PwStage(it.getString("id"), it.getString("label"), it.optString("icon"), it.optString("blurb"), it.optString("tip")) },
        routes = o.getJSONArray("routes").mapObjs {
            val fee = it.getJSONArray("fee")
            PwRoute(
                it.getString("id"), it.getString("stage"), it.getString("name"), it.optString("kind"), it.optString("group"), it.optString("years"),
                fee.getLong(0), fee.getLong(1), it.optString("entry"), it.optString("about"), it.optString("exam"),
                it.optJSONArray("careers").strings(), it.optJSONArray("skills").strings(), it.optJSONArray("next").strings(), it.optJSONArray("where").strings(),
                plan = it.optJSONArray("plan").strings(), tags = it.optJSONArray("tags").strings(), examId = it.optString("exam_id"),
                demand = it.optInt("demand"), competition = it.optInt("competition"),
            )
        },
        careers = o.getJSONArray("careers").mapObjs {
            val s = it.getJSONObject("salary"); val e = s.getJSONArray("entry"); val sr = s.getJSONArray("senior")
            val lic = it.optJSONObject("licence")
            PwCareer(
                it.getString("id"), it.getString("name"), it.optString("about"), it.optInt("demand"), it.optInt("competition"), it.optString("trend"),
                it.optInt("abroad"), e.getLong(0), e.getLong(1), sr.getLong(0), sr.getLong(1),
                skills = it.optJSONArray("skills").strings(), ladder = it.optJSONArray("ladder").strings(), day = it.optJSONArray("day").parts(),
                jobs = it.optJSONArray("jobs").parts(), employers = it.optJSONArray("employers").strings(), traits = it.optJSONObject("traits").intMap(),
                hours = it.optInt("hours"), history = it.optJSONArray("history").ints(),
                licence = lic?.optString("name").orEmpty(), licenceExam = lic?.optString("exam").orEmpty(),
            )
        }.associateBy { it.id },
        providers = o.getJSONArray("providers").mapObjs { p ->
            val fees = p.optJSONObject("fees")?.let { f ->
                f.keys().asSequence().mapNotNull { k -> f.optJSONArray(k)?.let { a -> k to (a.optLong(0) to a.optLong(1)) } }.toMap()
            } ?: emptyMap()
            PwProvider(
                p.getString("id"), p.getString("name"), p.optString("kind"), p.optString("sector"), p.optString("district"), p.optString("place"), p.optString("note"),
                p.optString("website"), fees, p.optInt("seats"),
            )
        }.associateBy { it.id },
        scholarships = o.getJSONArray("scholarships").mapObjs {
            PwScholarship(
                it.getString("id"), it.getString("name"), it.optString("scope"), it.optJSONArray("levels").strings(), it.optString("by"), it.optString("covers"),
                it.optString("who"), it.optString("how"), it.optString("link"),
                country = it.optString("country"), type = it.optString("type"), open = it.optJSONArray("open").ints(), awards = it.optInt("awards"),
            )
        },
        abroad = o.getJSONArray("abroad").mapObjs {
            val t = it.getJSONArray("tuition"); val l = it.getJSONArray("living")
            PwAbroad(
                it.getString("id"), it.getString("country"), t.getLong(0), t.getLong(1), l.getLong(0), l.getLong(1),
                it.optJSONArray("exams").strings(), it.optString("intakes"), it.optJSONArray("fields").strings(), it.optString("work"), it.optString("note"),
                it.optJSONArray("scholarships").strings(),
                code = it.optString("code"), visaRate = it.optInt("visa_rate", -1), workHours = it.optInt("work_hours", -1), stayBack = it.optString("stay_back"),
                visa = it.optJSONObject("visa")?.let { v ->
                    PwVisa(v.optString("name"), v.optJSONArray("steps")?.let { a -> List(a.length()) { i -> a.getJSONArray(i).let { r -> PwVisaStep(r.optString(0), r.optInt(1), r.optString(2), r.optString(3), r.optString(4)) } } } ?: emptyList())
                },
            )
        },
        topics = o.optJSONArray("topics")?.mapObjs { PwTopic(it.getString("id"), it.optString("label")) } ?: emptyList(),
        govtTracks = o.optJSONArray("govt_tracks")?.mapObjs { PwTopic(it.getString("id"), it.optString("label"), it.optString("group").ifEmpty { "gov" }) } ?: emptyList(),
        govtGroups = o.optJSONArray("govt_groups")?.mapObjs { PwTopic(it.getString("id"), it.optString("label")) } ?: emptyList(),
        govt = o.optJSONArray("govt")?.mapObjs { g ->
            PwGovt(
                g.getString("id"), g.optString("track"), g.optString("name"), g.optString("level"), g.optString("need"), g.optString("age"), g.optString("body"),
                g.optJSONArray("stages")?.let { arr -> List(arr.length()) { i -> arr.optJSONArray(i)?.let { PwExamStage(it.optString(0), it.optString(1), it.optString(2)) } }.filterNotNull() } ?: emptyList(),
                g.optJSONArray("subjects").strings(), g.optJSONArray("prep").strings(), g.optString("note"),
                seats = g.optInt("seats"), applicants = g.optInt("applicants"), fee = g.optLong("fee"), apply = g.optJSONArray("apply").ints(),
                examMonth = g.optInt("exam_month"), prepHours = g.optInt("prep_hours"), syllabus = g.optJSONArray("syllabus").parts(),
                quota = g.optJSONArray("quota").parts(), ladder = g.optJSONArray("ladder").parts(), rung = g.optInt("rung", -1),
                career = g.optString("career"), pay = g.optLong("pay"),
            )
        } ?: emptyList(),
        faq = o.optJSONArray("faq")?.mapObjs { PwFaq(it.getString("id"), it.optString("topic"), it.optString("q"), it.optString("a"), it.optJSONArray("go").strings()) } ?: emptyList(),
        guides = o.optJSONArray("guides")?.mapObjs { g ->
            val steps = g.optJSONArray("steps")?.let { arr ->
                List(arr.length()) { i ->
                    arr.optJSONArray(i)?.let { s -> PwStep(s.optString(0), s.optInt(1), s.optLong(2), s.optString(3).let { w -> w == "online" || w == "true" }) }
                }.filterNotNull()
            } ?: emptyList()
            PwGuide(g.getString("id"), g.optString("name"), g.optString("cat"), steps, g.optJSONArray("docs").strings(), g.optString("link"))
        } ?: emptyList(),
    )
}

data class PwPlace(val name: String, val where: String)

data class PathwaysUiState(
    val data: PwData? = null,
    val loading: Boolean = true,
    val failed: Boolean = false,
    val district: String = "",
    val live: List<PwPlace> = emptyList(),
    val saved: Set<String> = emptySet(),
    val onNeb: PwOnNebData? = null,
)

/** Where the student is inside Pathways. Lives in the ViewModel so Explore, details and Plan share one picture. */
@Stable
class PwSel {
    var stage by mutableStateOf("")
    var group by mutableStateOf("")
    var course by mutableStateOf<String?>(null)
    var career by mutableStateOf<String?>(null)
    var focus by mutableStateOf("")
    var lens by mutableStateOf("")
    var linked by mutableStateOf(false)
    var trail by mutableStateOf(listOf<String>())
    var study by mutableStateOf("colleges")
    var collegeRoute by mutableStateOf("")
    var abroadOpen by mutableStateOf("")
    var schCountry by mutableStateOf("")
    var schOpen by mutableStateOf("")
    var track by mutableStateOf("")
    var plan by mutableStateOf("match")
    var matchStage by mutableStateOf("")
    var matchOpen by mutableStateOf<String?>(null)
    var matchWeak by mutableStateOf(false)
    var matchEdit by mutableStateOf(false)
    var faqOpen by mutableStateOf("")
}

private val SET_KEYS = listOf("done", "docs", "have", "interests", "strengths", "priorities", "helpful")
private val NUM_DEFAULTS = mapOf("age" to 17, "edu" to 2, "woman" to 0, "budget" to 15, "hours" to 3, "abroadBudget" to 60, "mstep" to 0, "mdone" to 0, "myears" to 0, "mrisk" to 1, "mstream" to 0)

@HiltViewModel
class PathwaysViewModel @Inject constructor(@ApplicationContext private val context: Context) : ViewModel() {
    private val _state = MutableStateFlow(PathwaysUiState())
    val state: StateFlow<PathwaysUiState> = _state.asStateFlow()
    private val cacheFile get() = File(context.filesDir, "pathways.json")
    private val prefs get() = context.getSharedPreferences("pathways", Context.MODE_PRIVATE)

    val sel = PwSel()
    private val sets = mutableStateMapOf<String, Set<String>>()
    private val nums = mutableStateMapOf<String, Int>()

    private val wave17: JSONObject? by lazy {
        runCatching { JSONObject(context.assets.open("pathways_wave17.json").bufferedReader().use { it.readText() }) }.getOrNull()
    }

    init {
        SET_KEYS.forEach { sets[it] = prefs.getStringSet("set_$it", emptySet()).orEmpty().toSet() }
        NUM_DEFAULTS.forEach { (k, v) -> nums[k] = prefs.getInt("num_$k", v) }
        sel.matchStage = prefs.getString("matchStage", "").orEmpty()
        _state.update { it.copy(district = prefs.getString("district", "") ?: "", saved = prefs.getStringSet("saved", emptySet()).orEmpty().toSet()) }
        loadOnNeb()
        viewModelScope.launch {
            // the saved copy shows at once; the network only refreshes it (ETag keeps that call tiny)
            val cached = withContext(Dispatchers.IO) { runCatching { parsePathways(cacheFile.readText(), wave17) }.getOrNull() }
            if (cached != null) _state.update { it.copy(data = cached, loading = false) }
            val fresh = withContext(Dispatchers.IO) { runCatching { fetch() }.getOrNull() }
            _state.update {
                when {
                    fresh != null -> it.copy(data = fresh, loading = false, failed = false)
                    it.data == null -> it.copy(loading = false, failed = true)
                    else -> it
                }
            }
        }
    }

    private val onNebFile get() = File(context.filesDir, "pathways_on_neb.json")

    /** Claimed institutions that filled their page: saved copy first, then the small live call. */
    private fun loadOnNeb() = viewModelScope.launch {
        val cached = withContext(Dispatchers.IO) { runCatching { parseOnNeb(onNebFile.readText()) }.getOrNull() }
        if (cached != null) _state.update { it.copy(onNeb = cached) }
        val fresh = withContext(Dispatchers.IO) {
            runCatching { fetchOnNebText()?.also { onNebFile.writeText(it) }?.let(::parseOnNeb) }.getOrNull()
        }
        if (fresh != null) _state.update { it.copy(onNeb = fresh) }
    }

    private fun fetch(): PwData? {
        val conn = URL("https://nebians.consica.com.np/api/pathways/").openConnection() as HttpURLConnection
        conn.connectTimeout = 8000; conn.readTimeout = 12000
        prefs.getString("etag", null)?.let { if (cacheFile.exists()) conn.setRequestProperty("If-None-Match", it) }
        return try {
            if (conn.responseCode == 304) return null
            val text = conn.inputStream.bufferedReader().use { it.readText() }
            val parsed = parsePathways(text, wave17)
            cacheFile.writeText(text)
            prefs.edit().putString("etag", conn.getHeaderField("ETag")).apply()
            parsed
        } finally { conn.disconnect() }
    }

    fun toggleSaved(key: String) {
        val next = _state.value.saved.let { if (key in it) it - key else it + key }
        prefs.edit().putStringSet("saved", next).apply()
        _state.update { it.copy(saved = next) }
    }

    fun set(name: String): Set<String> = sets[name] ?: emptySet()
    fun has(name: String, value: String): Boolean = value in set(name)
    fun toggle(name: String, value: String) {
        val next = set(name).let { if (value in it) it - value else it + value }
        sets[name] = next
        prefs.edit().putStringSet("set_$name", next).apply()
    }

    fun num(name: String): Int = nums[name] ?: NUM_DEFAULTS[name] ?: 0
    fun setNum(name: String, value: Int) {
        if (nums[name] == value) return
        nums[name] = value
        prefs.edit().putInt("num_$name", value).apply()
    }

    fun setMatchStage(id: String) {
        sel.matchStage = id
        prefs.edit().putString("matchStage", id).apply()
    }

    fun clearMatch() {
        listOf("interests", "strengths", "priorities").forEach { sets[it] = emptySet(); prefs.edit().remove("set_$it").apply() }
        setNum("myears", 0); setNum("mrisk", 1); setNum("mstep", 0); setNum("mdone", 0); setNum("budget", 15)
        sel.matchOpen = null; sel.matchWeak = false
    }

    fun setDistrict(district: String, kind: String) {
        prefs.edit().putString("district", district).apply()
        _state.update { it.copy(district = district, live = emptyList()) }
        if (district.isBlank()) return
        viewModelScope.launch {
            val places = withContext(Dispatchers.IO) {
                runCatching {
                    val url = "https://nebians.consica.com.np/api/institutions/?limit=6&kind=$kind&district=${URLEncoder.encode(district, "UTF-8")}"
                    val conn = URL(url).openConnection() as HttpURLConnection
                    conn.connectTimeout = 8000; conn.readTimeout = 12000
                    try {
                        val items = JSONObject(conn.inputStream.bufferedReader().use { it.readText() }).getJSONArray("items")
                        items.mapObjs { PwPlace(it.optString("name"), it.optString("location").ifBlank { it.optString("district") }) }
                    } finally { conn.disconnect() }
                }.getOrDefault(emptyList())
            }
            _state.update { if (it.district == district) it.copy(live = places) else it }
        }
    }
}

internal fun money(n: Long): String = when {
    n >= 10_000_000 -> trim(n / 10_000_000.0) + " crore"
    n >= 100_000 -> trim(n / 100_000.0) + " lakh"
    n >= 1_000 -> trim(n / 1_000.0) + "k"
    else -> n.toString()
}
internal fun trim(x: Double): String = (Math.round(x * 10) / 10.0).toString().removeSuffix(".0")
internal fun feeText(min: Long, max: Long): String = if (max == 0L) "Free" else if (min == 0L) "Free to NPR ${money(max)}" else "NPR ${money(min)} to ${money(max)}"
