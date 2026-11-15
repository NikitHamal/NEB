package com.neb.ians.ui.screens.pathways

import android.content.Context
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

data class PwStage(val id: String, val label: String, val icon: String, val blurb: String, val tip: String)
data class PwRoute(
    val id: String, val stage: String, val name: String, val kind: String, val group: String, val years: String,
    val feeMin: Long, val feeMax: Long, val entry: String, val about: String, val exam: String,
    val careers: List<String>, val skills: List<String>, val next: List<String>, val where: List<String>,
)
data class PwCareer(
    val id: String, val name: String, val about: String, val demand: Int, val competition: Int, val trend: String,
    val abroad: Int, val entryMin: Long, val entryMax: Long, val seniorMin: Long, val seniorMax: Long,
)
data class PwProvider(val id: String, val name: String, val kind: String, val sector: String, val district: String, val place: String, val note: String)
data class PwScholarship(val id: String, val name: String, val scope: String, val levels: List<String>, val by: String, val covers: String, val who: String, val how: String)
data class PwAbroad(
    val id: String, val country: String, val tuitionMin: Long, val tuitionMax: Long, val livingMin: Long, val livingMax: Long,
    val exams: List<String>, val intakes: String, val fields: List<String>, val work: String, val note: String,
)
data class PwData(
    val reviewed: String, val stages: List<PwStage>, val routes: List<PwRoute>, val careers: Map<String, PwCareer>,
    val providers: Map<String, PwProvider>, val scholarships: List<PwScholarship>, val abroad: List<PwAbroad>,
) { val routeById: Map<String, PwRoute> by lazy { routes.associateBy { it.id } } }

private fun JSONArray?.strings(): List<String> = if (this == null) emptyList() else List(length()) { optString(it) }
private inline fun <T> JSONArray.mapObjs(f: (JSONObject) -> T): List<T> = List(length()) { f(getJSONObject(it)) }

internal fun parsePathways(text: String): PwData {
    val o = JSONObject(text)
    return PwData(
        reviewed = o.optString("reviewed"),
        stages = o.getJSONArray("stages").mapObjs { PwStage(it.getString("id"), it.getString("label"), it.optString("icon"), it.optString("blurb"), it.optString("tip")) },
        routes = o.getJSONArray("routes").mapObjs {
            val fee = it.getJSONArray("fee")
            PwRoute(
                it.getString("id"), it.getString("stage"), it.getString("name"), it.optString("kind"), it.optString("group"), it.optString("years"),
                fee.getLong(0), fee.getLong(1), it.optString("entry"), it.optString("about"), it.optString("exam"),
                it.optJSONArray("careers").strings(), it.optJSONArray("skills").strings(), it.optJSONArray("next").strings(), it.optJSONArray("where").strings(),
            )
        },
        careers = o.getJSONArray("careers").mapObjs {
            val s = it.getJSONObject("salary"); val e = s.getJSONArray("entry"); val sr = s.getJSONArray("senior")
            PwCareer(it.getString("id"), it.getString("name"), it.optString("about"), it.optInt("demand"), it.optInt("competition"), it.optString("trend"),
                it.optInt("abroad"), e.getLong(0), e.getLong(1), sr.getLong(0), sr.getLong(1))
        }.associateBy { it.id },
        providers = o.getJSONArray("providers").mapObjs {
            PwProvider(it.getString("id"), it.getString("name"), it.optString("kind"), it.optString("sector"), it.optString("district"), it.optString("place"), it.optString("note"))
        }.associateBy { it.id },
        scholarships = o.getJSONArray("scholarships").mapObjs {
            PwScholarship(it.getString("id"), it.getString("name"), it.optString("scope"), it.optJSONArray("levels").strings(), it.optString("by"), it.optString("covers"), it.optString("who"), it.optString("how"))
        },
        abroad = o.getJSONArray("abroad").mapObjs {
            val t = it.getJSONArray("tuition"); val l = it.getJSONArray("living")
            PwAbroad(it.getString("id"), it.getString("country"), t.getLong(0), t.getLong(1), l.getLong(0), l.getLong(1),
                it.optJSONArray("exams").strings(), it.optString("intakes"), it.optJSONArray("fields").strings(), it.optString("work"), it.optString("note"))
        },
    )
}

data class PwPlace(val name: String, val where: String)

data class PathwaysUiState(
    val data: PwData? = null,
    val loading: Boolean = true,
    val failed: Boolean = false,
    val district: String = "",
    val live: List<PwPlace> = emptyList(),
)

@HiltViewModel
class PathwaysViewModel @Inject constructor(@ApplicationContext private val context: Context) : ViewModel() {
    private val _state = MutableStateFlow(PathwaysUiState())
    val state: StateFlow<PathwaysUiState> = _state.asStateFlow()
    private val cacheFile get() = File(context.filesDir, "pathways.json")
    private val prefs get() = context.getSharedPreferences("pathways", Context.MODE_PRIVATE)

    init {
        _state.update { it.copy(district = prefs.getString("district", "") ?: "") }
        viewModelScope.launch {
            // the saved copy shows at once; the network only refreshes it (ETag keeps that call tiny)
            val cached = withContext(Dispatchers.IO) { runCatching { parsePathways(cacheFile.readText()) }.getOrNull() }
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

    private fun fetch(): PwData? {
        val conn = URL("https://nebians.consica.com.np/api/pathways/").openConnection() as HttpURLConnection
        conn.connectTimeout = 8000; conn.readTimeout = 12000
        prefs.getString("etag", null)?.let { if (cacheFile.exists()) conn.setRequestProperty("If-None-Match", it) }
        return try {
            if (conn.responseCode == 304) return null
            val text = conn.inputStream.bufferedReader().use { it.readText() }
            val parsed = parsePathways(text)
            cacheFile.writeText(text)
            prefs.edit().putString("etag", conn.getHeaderField("ETag")).apply()
            parsed
        } finally { conn.disconnect() }
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
private fun trim(x: Double): String = (Math.round(x * 10) / 10.0).toString().removeSuffix(".0")
internal fun feeText(min: Long, max: Long): String = if (max == 0L) "Free" else if (min == 0L) "Free to NPR ${money(max)}" else "NPR ${money(min)} to ${money(max)}"

internal val NEPAL_DISTRICT_LIST = listOf(
    "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", "Banke", "Bara", "Bardiya", "Bhaktapur", "Bhojpur", "Chitwan",
    "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading", "Dhankuta", "Dhanusha", "Dolakha", "Dolpa", "Doti", "Gorkha", "Gulmi",
    "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali", "Kalikot", "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok",
    "Khotang", "Lalitpur", "Lamjung", "Mahottari", "Makwanpur", "Manang", "Morang", "Mugu", "Mustang", "Myagdi", "Nawalparasi East", "Nuwakot",
    "Okhaldhunga", "Palpa", "Panchthar", "Nawalparasi West", "Parbat", "Parsa", "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat", "Rolpa", "Rukum East",
    "Rukum West", "Rupandehi", "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu",
    "Sunsari", "Surkhet", "Syangja", "Tanahun", "Taplejung", "Tehrathum", "Udayapur",
)
