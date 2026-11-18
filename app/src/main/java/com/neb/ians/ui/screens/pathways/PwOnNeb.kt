@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Call
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.screens.institutions.LocalOpenInstitution
import com.neb.ians.ui.screens.institutions.LocalOpenSchools
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

/** A claimed institution that filled its page. `/api/pathways/on-neb/`, fullest first. */
data class PwOnNebItem(
    val slug: String, val name: String, val kind: String, val district: String, val place: String,
    val completeness: Int, val levels: List<String>, val feeMin: Long?, val admissionOpen: Boolean,
    val phone: String, val website: String,
)

data class PwOnNebData(val items: List<PwOnNebItem>, val matches: Map<String, String>)

/** Blocking read, call from IO. Returns the raw text so the caller can keep a copy for offline. */
internal fun fetchOnNebText(): String? {
    val conn = URL("https://nebians.consica.com.np/api/pathways/on-neb/").openConnection() as HttpURLConnection
    conn.connectTimeout = 8000; conn.readTimeout = 10000
    return try { conn.inputStream.bufferedReader().use { it.readText() } } finally { conn.disconnect() }
}

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

/** Top of Find a college: colleges that filled their page come first, matched ones for this course ahead. */
@Composable
internal fun PwOnNebSection(data: PwOnNebData?, courseSlugs: Set<String>, district: String) {
    val open = LocalOpenInstitution.current
    if (data == null || data.items.isEmpty()) { Box(Modifier.padding(horizontal = 16.dp)) { com.neb.ians.ui.screens.institutions.PwOnNebRow() }; return }
    val c = MaterialTheme.colorScheme
    val ctx = LocalContext.current
    val shown = remember(data, courseSlugs, district) {
        data.items.sortedWith(compareBy({ if (it.slug in courseSlugs) 0 else 1 }, { if (district.isNotEmpty() && it.district == district) 0 else 1 }, { -it.completeness }))
            .take(6)
    }
    PwH4("On NEBians", Modifier.padding(horizontal = 16.dp))
    Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        shown.forEachIndexed { i, p ->
            PwSurface(Modifier.fillMaxWidth().pwRise(i, "onneb"), radius = 22.dp, onClick = {
                com.neb.ians.ui.screens.institutions.InstitutionPeek.put(p.slug, p.name, listOf(p.kind.replaceFirstChar { it.uppercase() }, p.place, p.district).filter { it.isNotBlank() }.distinct().joinToString(" · "))
                open(p.slug)
            }) {
                Column(Modifier.padding(16.dp, 14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Column(Modifier.weight(1f)) {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                Text(p.name, Modifier.weight(1f, fill = false), fontSize = 14.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp, maxLines = 2, overflow = TextOverflow.Ellipsis)
                                Icon(Icons.Filled.Verified, null, Modifier.size(16.dp), tint = c.primary)
                            }
                            Text(listOf(p.kind.replaceFirstChar { it.uppercase() }, p.place, p.district).filter { it.isNotBlank() }.distinct().joinToString(" · "),
                                fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                        Icon(Icons.Outlined.ChevronRight, null, tint = c.onSurfaceVariant)
                    }
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        if (p.admissionOpen) PwTag("Admissions open", pwTone(4))
                        if (p.slug in courseSlugs) PwTag("Offers this course", pwTone(0))
                        p.feeMin?.takeIf { it > 0 }?.let { PwTag("From ${lakhText(it / 100_000f)}", pwTone(1)) }
                        p.levels.take(3).forEach { PwTag(institutionLevelLabel(it), pwTone(2)) }
                    }
                    if (p.phone.isNotBlank()) Row(
                        Modifier.heightIn(min = 36.dp).clickable { runCatching { ctx.startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:" + p.phone.filter { it.isDigit() || it == '+' }))) } },
                        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        Icon(Icons.Outlined.Call, null, Modifier.size(16.dp), tint = c.primary)
                        Text("Call ${p.phone}", fontSize = 12.5.sp, fontWeight = FontWeight.SemiBold, color = c.primary, maxLines = 1)
                    }
                }
            }
        }
        val all = LocalOpenSchools.current
        PwButton("All colleges on NEBians", null, false, all, Modifier.fillMaxWidth())
    }
}
