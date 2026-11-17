package com.neb.ians.ui.screens.institutions

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Badge
import androidx.compose.material.icons.outlined.Groups
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.MaterialTheme
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

/** Everything after the headline sections: leadership, classes, programs, branches, contact, links, registration, people. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun InstitutionMore(d: ApiInstDetail, schema: ApiInstSchema, owner: Boolean, ed: (String) -> Unit, onWeb: (String) -> Unit) {
    val p = d.portfolio.details
    fun key(s: String) = if (owner) s else null
    fun lab(rows: List<com.neb.ians.data.api.ApiInstOption>, k: String) = rows.firstOrNull { it.value == k }?.label ?: k
    val sub = MaterialTheme.colorScheme.onSurfaceVariant
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (p.str("principal").isNotBlank()) PCard(p.str("principalTitle").ifBlank { "Principal" }, Icons.Outlined.Badge, key("Basics"), ed) { Body(p.str("principal")) }
        val classes = p.list("streams").map { lab(schema.streams, it) } + p.list("mediums").map { lab(schema.mediums, it) } +
            listOfNotNull(schema.genderMix.firstOrNull { it.value == p.str("genderMix") }?.label)
        if (classes.isNotEmpty()) PCard("Classes and medium", Icons.Outlined.Tune, key("Classes and medium"), ed) { Chips(classes) }
        if (p.list("affiliations").isNotEmpty()) PCard("Affiliated with", Icons.Outlined.Badge, key("Basics"), ed) { Chips(p.list("affiliations").map { lab(schema.affiliations, it) }) }
        if (p.rows("programs").isNotEmpty()) PCard("Programs", Icons.Outlined.Tune, key("Programs"), ed) {
            p.rows("programs").forEach { r ->
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text(r["name"].orEmpty(), fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                        Text(listOf(r["level"].orEmpty(), r["seats"]?.takeIf { it.isNotBlank() }?.let { "$it seats" }.orEmpty()).filter { it.isNotBlank() }.joinToString(" · "), fontSize = 12.sp, color = sub)
                    }
                    r["fee"]?.toLongOrNull()?.let { Text(money(it), fontSize = 13.sp, fontWeight = FontWeight.SemiBold) }
                }
            }
        }
        if (p.rows("branches").isNotEmpty()) PCard("Branches", Icons.Outlined.LocationOn, key("Branches"), ed) {
            p.rows("branches").forEach { r ->
                Column {
                    Text(r["name"].orEmpty(), fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                    Text(listOf(r["place"].orEmpty(), r["phone"].orEmpty()).filter { it.isNotBlank() }.joinToString(" · "), fontSize = 12.sp, color = sub)
                }
            }
        }
        val contact = listOf(p.str("address"), p.str("phone"), p.str("email")).filter { it.isNotBlank() }
        if (contact.isNotEmpty()) PCard("Contact and places", Icons.Outlined.LocationOn, key("Contact"), ed) { contact.forEach { Body(it) } }
        (p["socials"] as? JsonObject)?.entries?.filter { (it.value as? JsonPrimitive)?.content?.isNotBlank() == true }?.takeIf { it.isNotEmpty() }?.let { links ->
            PCard("Follow", Icons.Outlined.Share, key("Social links"), ed) {
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    links.forEach { (k, v) -> FilledTonalButton(onClick = { onWeb((v as JsonPrimitive).content) }) { Text(k.replaceFirstChar { c -> c.uppercase() }) } }
                }
            }
        }
        if (p.str("regNo").isNotBlank()) PCard("Registration", Icons.Outlined.Badge, key("Basics"), ed) { Body(p.str("regNo")) }
        if (d.people.isNotEmpty()) PCard("On NEBians (${d.counts.total})", Icons.Outlined.Groups, null, ed) { Chips(d.people.take(12).map { it.displayName }) }
    }
}
