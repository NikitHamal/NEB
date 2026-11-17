package com.neb.ians.ui.screens.institutions

import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebTopBar
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material3.Button
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import kotlinx.coroutines.delay
import androidx.compose.ui.Alignment
import kotlinx.serialization.json.JsonPrimitive
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.api.ApiInstDetail

private const val WEB = "https://nebians.consica.com.np"

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun InstitutionScreen(
    slug: String,
    onBack: () -> Unit,
    onManage: (String) -> Unit,
    vm: InstitutionViewModel = hiltViewModel()
) {
    val st by vm.state.collectAsState()
    LaunchedEffect(slug) { vm.load(slug) }
    val d = st.detail
    val uri = LocalUriHandler.current
    Column(Modifier.fillMaxSize()) {
        NebTopBar(showBrand = false, title = d?.name ?: "", onBack = onBack, actions = {
            if (d?.canEdit == true) NebIconButton(Icons.Outlined.Edit, "Edit portfolio", onClick = { onManage(slug) })
        })
        if (d == null) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(if (st.loading) "Loading" else st.error.orEmpty(), color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            return@Column
        }
        val p = d.portfolio.details
        val schema = st.schema
        LazyColumn(contentPadding = PaddingValues(16.dp, 0.dp, 16.dp, 40.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            val blocks = buildList<@Composable () -> Unit> {
                add { Hero(d) }
                add { Actions(d, p.str("phone").ifBlank { d.phone }, onWeb = { uri.openUri(it) }, onClaim = { uri.openUri("$WEB/app/schools/verify/?school=${d.slug}") }) }
                val facts = listOf("Established" to (d.est), "Students" to (p.num("students")?.let { "%,d".format(it) } ?: ""),
                    "Teachers" to (p.num("teachers")?.toString() ?: ""), "Staff" to (p.num("staff")?.toString() ?: ""),
                    "Classrooms" to (p.num("classrooms")?.toString() ?: "")).filter { it.second.isNotBlank() }
                if (facts.isNotEmpty()) add { Facts(facts) }
                if (p.flag("admissionOpen")) add { Note("Admissions are open", p.str("admissionNote").ifBlank { "Call the office to book a visit." }) }
                if (p.str("about").isNotBlank()) add { Section("About") { Body(p.str("about")) } }
                if (p.list("levels").isNotEmpty()) add { Section("Levels offered") { Chips(p.list("levels").map { k -> schema.levels.firstOrNull { it.value == k }?.label ?: k }) } }
                if (p.num("feeMin") != null) add { Section("Yearly fees") {
                    Text(money(p.num("feeMin")) + (p.num("feeMax")?.let { " to " + money(it) } ?: ""), fontSize = 22.sp, fontWeight = FontWeight.SemiBold)
                    if (p.str("feeNote").isNotBlank()) Body(p.str("feeNote")) } }
                if (p.list("facilities").isNotEmpty()) add { Section("Facilities") { Chips(p.list("facilities").map { k -> schema.facilities.firstOrNull { it.value == k }?.label ?: k }) } }
                if (p.str("principal").isNotBlank()) add { Section(p.str("principalTitle").ifBlank { "Principal" }) { Body(p.str("principal")) } }
                if (p.list("streams").isNotEmpty()) add { Section("Streams") { Chips(p.list("streams").map { k -> schema.streams.firstOrNull { it.value == k }?.label ?: k }) } }
                if (p.list("mediums").isNotEmpty() || p.str("genderMix").isNotBlank()) add { Section("Classes") {
                    Chips(p.list("mediums").map { k -> schema.mediums.firstOrNull { it.value == k }?.label ?: k } +
                        listOfNotNull(schema.genderMix.firstOrNull { it.value == p.str("genderMix") }?.label)) } }
                if (p.rows("programs").isNotEmpty()) add { Section("Programs") { p.rows("programs").forEach { r ->
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(r["name"].orEmpty(), fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                            Text(listOf(r["level"].orEmpty(), r["seats"]?.takeIf { it.isNotBlank() }?.let { "$it seats" }.orEmpty()).filter { it.isNotBlank() }.joinToString(" · "),
                                fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        r["fee"]?.toLongOrNull()?.let { Text(money(it), fontSize = 13.sp, fontWeight = FontWeight.SemiBold) }
                    } } } }
                if (p.rows("branches").isNotEmpty()) add { Section("Branches") { p.rows("branches").forEach { r ->
                    Column {
                        Text(r["name"].orEmpty(), fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                        Text(listOf(r["place"].orEmpty(), r["phone"].orEmpty()).filter { it.isNotBlank() }.joinToString(" · "), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } } } }
                if (p.str("address").isNotBlank()) add { Section("Address") { Body(p.str("address")) } }
                (p["socials"] as? kotlinx.serialization.json.JsonObject)?.entries?.filter { (it.value as? JsonPrimitive)?.content?.isNotBlank() == true }?.takeIf { it.isNotEmpty() }?.let { links ->
                    add { Section("Follow") { FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        links.forEach { (k, v) -> FilledTonalButton(onClick = { uri.openUri((v as JsonPrimitive).content) }) { Text(k.replaceFirstChar { c -> c.uppercase() }) } } } } }
                }
                if (p.str("regNo").isNotBlank()) add { Section("Registration") { Body(p.str("regNo")) } }
                if (d.people.isNotEmpty()) add { Section("On NEBians (${d.counts.total})") { Chips(d.people.take(12).map { it.displayName }) } }
            }
            itemsIndexed(blocks) { i, block -> Rise(i) { block() } }
        }
    }
}

/** Rows rise in with a short stagger, the first dozen only. */
@Composable
private fun Rise(index: Int, content: @Composable () -> Unit) {
    val a = remember { Animatable(if (index > 12) 1f else 0f) }
    LaunchedEffect(Unit) {
        if (index <= 12) {
            delay(index * 40L)
            a.animateTo(1f, spring(dampingRatio = 0.62f, stiffness = Spring.StiffnessMediumLow))
        }
    }
    Box(Modifier.graphicsLayer {
        alpha = a.value.coerceIn(0f, 1f)
        val sc = 0.95f + 0.05f * a.value
        scaleX = sc
        scaleY = sc
    }) { content() }
}

@Composable
private fun Hero(d: ApiInstDetail) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(24.dp), modifier = Modifier.size(72.dp)) {
            Box(contentAlignment = Alignment.Center) {
                Icon(if (d.kind == "school") Icons.Outlined.School else Icons.Outlined.AccountBalance, null, Modifier.size(34.dp), tint = MaterialTheme.colorScheme.onPrimaryContainer)
            }
        }
        Spacer(Modifier.width(14.dp))
        Column {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(d.name, fontSize = 20.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f, fill = false))
                if (d.verified) { Spacer(Modifier.width(6.dp)); Icon(Icons.Outlined.Verified, "Verified", Modifier.size(20.dp), tint = MaterialTheme.colorScheme.primary) }
            }
            Text(listOf(d.kindLabel, d.location).filter { it.isNotBlank() }.joinToString(" · "), fontSize = 13.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun Actions(d: ApiInstDetail, phone: String, onWeb: (String) -> Unit, onClaim: () -> Unit) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        if (phone.isNotBlank()) Button(onClick = { onWeb("tel:" + phone.filter { it.isDigit() || it == '+' }) }) { Icon(Icons.Outlined.Phone, null, Modifier.size(18.dp)); Spacer(Modifier.width(6.dp)); Text("Call") }
        if (d.website.isNotBlank()) FilledTonalButton(onClick = { onWeb(d.website) }) { Icon(Icons.Outlined.Language, null, Modifier.size(18.dp)); Spacer(Modifier.width(6.dp)); Text("Website") }
        if (d.claimable) FilledTonalButton(onClick = onClaim) { Icon(Icons.Outlined.Verified, null, Modifier.size(18.dp)); Spacer(Modifier.width(6.dp)); Text("Claim") }
    }
}

@Composable
private fun Facts(facts: List<Pair<String, String>>) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        facts.chunked(2).forEach { row ->
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                row.forEach { (k, v) ->
                    Surface(color = MaterialTheme.colorScheme.surfaceContainerLow, shape = RoundedCornerShape(20.dp), modifier = Modifier.weight(1f)) {
                        Column(Modifier.padding(14.dp)) {
                            Text(v, fontSize = 24.sp, fontWeight = FontWeight.SemiBold)
                            Text(k, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
                if (row.size == 1) Spacer(Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun Note(title: String, text: String) {
    Surface(color = MaterialTheme.colorScheme.tertiaryContainer, shape = RoundedCornerShape(20.dp), modifier = Modifier.fillMaxWidth()) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Outlined.CalendarMonth, null, Modifier.size(22.dp))
            Spacer(Modifier.width(12.dp))
            Column { Text(title, fontWeight = FontWeight.SemiBold, fontSize = 14.sp); Text(text, fontSize = 13.sp) }
        }
    }
}

@Composable
private fun Section(title: String, content: @Composable () -> Unit) {
    Surface(color = MaterialTheme.colorScheme.surface, shape = RoundedCornerShape(24.dp), tonalElevation = 0.dp, shadowElevation = 0.dp,
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(title, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
            content()
        }
    }
}

@Composable
private fun Body(text: String) = Text(text, fontSize = 14.sp, lineHeight = 21.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun Chips(items: List<String>) {
    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        items.forEach {
            Surface(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(16.dp)) {
                Text(it, fontSize = 12.5.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(horizontal = 13.dp, vertical = 7.dp))
            }
        }
    }
}
