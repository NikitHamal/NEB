@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import org.json.JSONObject

/** A claimed institution that filled its page. `/api/pathways/on-neb/`, fullest first. */
data class PwOnNebItem(
    val slug: String, val name: String, val kind: String, val district: String, val place: String,
    val completeness: Int, val levels: List<String>, val feeMin: Long?, val admissionOpen: Boolean,
    val phone: String, val website: String,
)

data class PwOnNebData(val items: List<PwOnNebItem>, val matches: Map<String, String>)

/** Blocking read, call from IO. Returns the raw text so the caller can keep a copy for offline. */
internal fun fetchOnNebText(): String? = pwHttpGet("https://nebians.consica.com.np/api/pathways/on-neb/")

/** The server sends readable level names; an older payload sent the stored keys, so both read well. */
internal fun institutionLevelLabel(key: String): String = when (key) {
    "preprimary" -> "Pre-primary"; "basic_1_5" -> "Basic 1 to 5"; "basic_6_8" -> "Basic 6 to 8"
    "secondary_9_10" -> "Secondary 9 to 10"; "plus_two" -> "+2"; "a_level" -> "A Level"
    "diploma" -> "Diploma / TSLC"; "bachelor" -> "Bachelor's"; "master" -> "Master's"
    "phd" -> "PhD"; "coaching" -> "Entrance coaching"
    else -> if ('_' in key) key.replace('_', ' ').replaceFirstChar { it.uppercase() } else key
}

internal fun parseOnNeb(text: String): PwOnNebData {
    val o = JSONObject(text)
    val arr = o.optJSONArray("items")
    val items = (0 until (arr?.length() ?: 0)).mapNotNull { i ->
        val r = arr!!.optJSONObject(i) ?: return@mapNotNull null
        val lv = r.optJSONArray("levels")
        PwOnNebItem(
            r.optString("slug"), r.optString("name"), r.optString("kind"), r.optString("district"), r.optString("place"),
            r.optInt("completeness"), (0 until (lv?.length() ?: 0)).map { lv!!.optString(it) },
            if (r.isNull("feeMin")) null else r.optLong("feeMin"), r.optBoolean("admissionOpen"),
            r.optString("phone"), r.optString("website"),
        ).takeIf { it.slug.isNotEmpty() }
    }
    val m = o.optJSONObject("matches")
    val matches: Map<String, String> = if (m == null) emptyMap() else m.keys().asSequence().associateWith { k -> m.optString(k) }
    return PwOnNebData(items, matches)
}
