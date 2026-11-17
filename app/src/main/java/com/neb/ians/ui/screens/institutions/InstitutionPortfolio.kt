package com.neb.ians.ui.screens.institutions

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.api.ApiInstDetail
import com.neb.ians.data.api.ApiInstSchema
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive

private fun facIcon(k: String) = when (k) {
    "library" -> Icons.Outlined.LocalLibrary; "science_lab" -> Icons.Outlined.Science; "computer_lab" -> Icons.Outlined.Computer
    "hostel" -> Icons.Outlined.Bed; "transport" -> Icons.Outlined.DirectionsBus; "canteen" -> Icons.Outlined.Restaurant
    "sports" -> Icons.Outlined.SportsSoccer; "wifi" -> Icons.Outlined.Wifi; "scholarship" -> Icons.Outlined.MonetizationOn
    "medical" -> Icons.Outlined.MedicalServices; "auditorium" -> Icons.Outlined.Theaters; "smart_class" -> Icons.Outlined.Tv
    "swimming" -> Icons.Outlined.Pool; "counselling" -> Icons.Outlined.Psychology; "placement" -> Icons.Outlined.Work
    else -> Icons.Outlined.ChildCare
}

/** The whole institution portfolio in the concept's order. Owners get the strength card, Edit on each card and an Add slot where a section is empty. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun InstitutionPortfolio(
    d: ApiInstDetail, schema: ApiInstSchema, owner: Boolean, onEdit: (String) -> Unit,
    onWeb: (String) -> Unit, onClaim: () -> Unit, showActions: Boolean = true
) {
    val p = d.portfolio.details
    fun lab(rows: List<com.neb.ians.data.api.ApiInstOption>, k: String) = rows.firstOrNull { it.value == k }?.label ?: k
    val ed: (String) -> Unit = onEdit
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (owner) {
            val pct = d.portfolio.completeness
            StrengthCard(
                pct, if (pct >= 90) "Complete. Students and parents get the full picture." else "The fuller your page, the higher you appear in Find a college.",
                d.portfolio.missing.mapNotNull { SECTION_FOR[it] }.distinct().take(4), ed
            )
        }
        val phone = p.str("phone").ifBlank { d.phone }
        if (showActions && (phone.isNotBlank() || d.website.isNotBlank() || d.claimable)) Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (phone.isNotBlank()) FilledTonalButton(onClick = { onWeb("tel:" + phone.filter { it.isDigit() || it == '+' }) }) { Icon(Icons.Outlined.Phone, null, Modifier.size(18.dp)); Spacer(Modifier.width(6.dp)); Text("Call") }
            if (d.website.isNotBlank()) FilledTonalButton(onClick = { onWeb(d.website) }) { Icon(Icons.Outlined.Language, null, Modifier.size(18.dp)); Spacer(Modifier.width(6.dp)); Text("Website") }
            if (d.claimable) FilledTonalButton(onClick = onClaim) { Icon(Icons.Outlined.Verified, null, Modifier.size(18.dp)); Spacer(Modifier.width(6.dp)); Text("Claim") }
        }
        val facts = listOf(
            "Established" to d.est, "Students" to (p.num("students")?.let { "%,d".format(it) } ?: ""), "Teachers" to (p.num("teachers")?.toString() ?: ""),
            "Staff" to (p.num("staff")?.toString() ?: ""), "Classrooms" to (p.num("classrooms")?.toString() ?: "")
        ).filter { it.second.isNotBlank() }
        if (facts.isNotEmpty()) StatGrid(facts) else if (owner) AddSlot("Add established year and numbers") { ed("Numbers") }
        if (p.flag("admissionOpen")) Note("Admissions are open", p.str("admissionNote").ifBlank { "Call the office to book a visit." })
        if (p.str("about").isNotBlank()) PCard("About", Icons.Outlined.Description, if (owner) "About" else null, ed) { Body(p.str("about")) }
        else if (owner) AddSlot("Write about your institution") { ed("About") }
        if (p.list("levels").isNotEmpty()) PCard("Levels offered", Icons.Outlined.School, if (owner) "Levels offered" else null, ed) { Chips(p.list("levels").map { lab(schema.levels, it) }) }
        else if (owner) AddSlot("Add the levels you offer") { ed("Levels offered") }
        val lo = p.num("feeMin")
        if (lo != null) PCard("Yearly fees", Icons.Outlined.MonetizationOn, if (owner) "Fees" else null, ed) {
            val hi = p.num("feeMax")
            Row(verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(money(lo), fontSize = 26.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.5).sp)
                if (hi != null && hi != lo) Text("to " + money(hi), fontSize = 13.5.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(bottom = 4.dp))
            }
            FeeBar(((hi ?: lo) / 300000f))
            Text("Compared with Rs 3,00,000 a year, the top of private schools in Nepal.", fontSize = 12.sp, lineHeight = 18.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            if (p.str("feeNote").isNotBlank()) Body(p.str("feeNote"))
        } else if (owner) AddSlot("Add your fees") { ed("Fees") }
        if (p.list("facilities").isNotEmpty()) PCard("Facilities", Icons.Outlined.LocalLibrary, if (owner) "Facilities" else null, ed) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                p.list("facilities").chunked(2).forEach { row ->
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        row.forEach { k ->
                            Surface(color = MaterialTheme.colorScheme.surfaceContainerLow, shape = RoundedCornerShape(18.dp), modifier = Modifier.weight(1f)) {
                                Row(Modifier.padding(11.dp, 11.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                                    Icon(facIcon(k), null, Modifier.size(20.dp), tint = MaterialTheme.colorScheme.primary)
                                    Text(lab(schema.facilities, k), fontSize = 12.5.sp, fontWeight = FontWeight.SemiBold, maxLines = 2)
                                }
                            }
                        }
                        if (row.size == 1) Spacer(Modifier.weight(1f))
                    }
                }
            }
        } else if (owner) AddSlot("Add your facilities") { ed("Facilities") }
        InstitutionMore(d, schema, owner, ed, onWeb)
    }
}

@Composable
internal fun Note(title: String, text: String) {
    Surface(color = MaterialTheme.colorScheme.tertiaryContainer, shape = RoundedCornerShape(20.dp), modifier = Modifier.fillMaxWidth()) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Outlined.CalendarMonth, null, Modifier.size(22.dp), tint = MaterialTheme.colorScheme.onTertiaryContainer)
            Spacer(Modifier.width(12.dp))
            Column {
                Text(title, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = MaterialTheme.colorScheme.onTertiaryContainer)
                Text(text, fontSize = 13.sp, color = MaterialTheme.colorScheme.onTertiaryContainer)
            }
        }
    }
}

@Composable
internal fun Body(text: String) = Text(text, fontSize = 13.5.sp, lineHeight = 21.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)

@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun Chips(items: List<String>) {
    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        items.forEach {
            Surface(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(16.dp)) {
                Text(it, fontSize = 12.5.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSecondaryContainer, modifier = Modifier.padding(horizontal = 13.dp, vertical = 7.dp))
            }
        }
    }
}
