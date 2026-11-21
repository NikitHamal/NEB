package com.neb.ians.ui.screens.institutions

import com.neb.ians.ui.components.NebTopBar
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.api.ApiInstOption
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebSelectChip
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonNull
import kotlinx.serialization.json.JsonPrimitive

internal enum class Kind { Text, Area, Num, Year, Many, One, Toggle, Rows, Socials }
internal data class F(val key: String, val label: String, val kind: Kind, val cols: List<Pair<String, String>> = emptyList(), val opts: (com.neb.ians.data.api.ApiInstSchema) -> List<ApiInstOption> = { emptyList() })
internal data class Sec(val title: String, val fields: List<F>)

// Same keys as `api/institution_profile.py`; every section saves on its own, nothing is required.
internal val SECTIONS = listOf(
    Sec("About", listOf(F("about", "About the institution", Kind.Area), F("motto", "Motto", Kind.Text))),
    Sec("Basics", listOf(F("est", "Established (year)", Kind.Year), F("principal", "Principal", Kind.Text), F("principalTitle", "Principal title", Kind.Text), F("regNo", "Registration number", Kind.Text),
        F("ownership", "Ownership", Kind.One) { it.ownership }, F("affiliations", "Affiliated with", Kind.Many) { it.affiliations })),
    Sec("Classes and medium", listOf(F("streams", "Streams", Kind.Many) { it.streams }, F("mediums", "Medium of teaching", Kind.Many) { it.mediums },
        F("genderMix", "Who studies here", Kind.One) { it.genderMix })),
    Sec("Levels offered", listOf(F("levels", "Levels and courses", Kind.Many) { it.levels })),
    Sec("Numbers", listOf(F("students", "Total students", Kind.Num), F("teachers", "Teachers", Kind.Num), F("staff", "Other staff", Kind.Num), F("classrooms", "Classrooms", Kind.Num))),
    Sec("Programs", listOf(F("programs", "Program", Kind.Rows, listOf("name" to "Program name", "level" to "Level", "seats" to "Seats", "fee" to "Yearly fee (Rs)")))),
    Sec("Branches", listOf(F("branches", "Branch", Kind.Rows, listOf("name" to "Branch name", "place" to "Place", "phone" to "Phone")))),
    Sec("Facilities", listOf(F("facilities", "What you offer", Kind.Many) { it.facilities })),
    Sec("Fees", listOf(F("feeMin", "Lowest yearly fee (Rs)", Kind.Num), F("feeMax", "Highest yearly fee (Rs)", Kind.Num), F("feeNote", "Fee note", Kind.Text))),
    Sec("Admissions", listOf(F("admissionOpen", "Admissions are open", Kind.Toggle), F("admissionNote", "Intake note", Kind.Text))),
    Sec("Contact", listOf(F("phone", "Phone", Kind.Text), F("email", "Email", Kind.Text), F("address", "Address", Kind.Text))),
    Sec("Social links", listOf(F("socials", "Links", Kind.Socials)))
)

private val SOCIALS = listOf("facebook" to "Facebook", "instagram" to "Instagram", "youtube" to "YouTube", "tiktok" to "TikTok", "x" to "X", "linkedin" to "LinkedIn")

@Composable
fun InstitutionManageScreen(slug: String, onBack: () -> Unit, vm: InstitutionViewModel = hiltViewModel()) {
    val st by vm.state.collectAsState()
    LaunchedEffect(slug) { vm.load(slug) }
    val d = st.detail
    var open by remember { mutableStateOf<Sec?>(null) }
    val score by animateFloatAsState((d?.portfolio?.completeness ?: 0) / 100f, label = "score")
    Column(Modifier.fillMaxSize()) {
        NebTopBar(showBrand = false, title = "Your portfolio", onBack = onBack)
        if (d == null) return@Column
        LazyColumn(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            item {
                Surface(color = MaterialTheme.colorScheme.surfaceContainerLow, shape = RoundedCornerShape(24.dp), modifier = Modifier.fillMaxWidth()) {
                    Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Box(Modifier.size(76.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(progress = { score }, modifier = Modifier.size(76.dp), strokeWidth = 8.dp,
                                trackColor = MaterialTheme.colorScheme.surfaceContainerHighest)
                            Text("${d.portfolio.completeness}%", fontSize = 18.sp, fontWeight = FontWeight.SemiBold)
                        }
                        Spacer(Modifier.width(16.dp))
                        Text("Portfolio", fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
            items(SECTIONS, key = { it.title }, contentType = { "section" }) { sec ->
                val done = sec.fields.any { f -> d.portfolio.details[f.key]?.let { it !is JsonNull && it.toString() != "\"\"" && it.toString() != "[]" && it.toString() != "{}" } == true }
                Surface(color = MaterialTheme.colorScheme.surface, shape = RoundedCornerShape(20.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                    modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(20.dp)).clickable { open = sec }) {
                    Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(sec.title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                        if (done) Icon(Icons.Outlined.Check, "Filled", tint = MaterialTheme.colorScheme.primary)
                        else Text("Add", fontSize = 12.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)
                        Icon(Icons.Outlined.ChevronRight, null)
                    }
                }
            }
            item { Spacer(Modifier.size(40.dp)) }
        }
    }
    open?.let { sec ->
        SectionSheet(sec, st.schema, d?.portfolio?.details ?: emptyMap(), st.saving, st.error,
            onSave = { vm.save(slug, it) }, onDismiss = { open = null })
        LaunchedEffect(st.saved) { if (st.saved) { open = null; vm.clearSaved() } }
    }
}

@OptIn(ExperimentalLayoutApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
internal fun SectionSheet(sec: Sec, schema: com.neb.ians.data.api.ApiInstSchema, current: Map<String, JsonElement>, saving: Boolean, error: String?,
                         onSave: (Map<String, JsonElement>) -> Unit, onDismiss: () -> Unit) {
    val draft = remember(sec) { mutableStateOf(current.filterKeys { k -> sec.fields.any { it.key == k } }) }
    fun text(k: String) = (draft.value[k] as? JsonPrimitive)?.content.orEmpty()
    fun many(k: String) = (draft.value[k] as? JsonArray)?.map { (it as JsonPrimitive).content } ?: emptyList()
    fun put(k: String, v: JsonElement) { draft.value = draft.value + (k to v) }
    NebModalSheet(onDismiss = onDismiss, title = sec.title) {
        Column(Modifier.verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            sec.fields.forEach { f ->
                when (f.kind) {
                    Kind.Toggle -> Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(f.label, Modifier.weight(1f), fontWeight = FontWeight.SemiBold)
                        Switch((draft.value[f.key] as? JsonPrimitive)?.content == "true", { put(f.key, JsonPrimitive(it)) })
                    }
                    Kind.Rows -> RowsEditor(f, draft.value[f.key], onChange = { put(f.key, it) })
                    Kind.Socials -> Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        val cur = draft.value[f.key] as? JsonObject
                        SOCIALS.forEach { (k, label) ->
                            NebDialogTextField(value = (cur?.get(k) as? JsonPrimitive)?.content.orEmpty(), label = label, singleLine = true, modifier = Modifier.fillMaxWidth(),
                                onValueChange = { v -> put(f.key, JsonObject((cur ?: JsonObject(emptyMap())) + (k to JsonPrimitive(v)))) })
                        }
                    }
                    Kind.Many, Kind.One -> Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(f.label, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            f.opts(schema).forEach { o ->
                                val on = if (f.kind == Kind.One) text(f.key) == o.value else o.value in many(f.key)
                                NebSelectChip(o.label, on, {
                                    if (f.kind == Kind.One) put(f.key, JsonPrimitive(if (on) "" else o.value))
                                    else put(f.key, JsonArray((if (on) many(f.key) - o.value else many(f.key) + o.value).map { JsonPrimitive(it) }))
                                })
                            }
                        }
                    }
                    else -> NebDialogTextField(
                        value = text(f.key), onValueChange = { v -> put(f.key, JsonPrimitive(if (f.kind == Kind.Num || f.kind == Kind.Year) v.filter(Char::isDigit) else v)) },
                        label = f.label, singleLine = f.kind != Kind.Area, minLines = if (f.kind == Kind.Area) 4 else 1,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }
            if (error != null) Text(error, color = MaterialTheme.colorScheme.error, fontSize = 13.sp)
            Button(onClick = { onSave(draft.value) }, enabled = !saving, modifier = Modifier.fillMaxWidth()) { Text(if (saving) "Saving" else "Save") }
            Spacer(Modifier.size(12.dp))
        }
    }
}

/** A short list of rows (programs, branches). Each row has the columns of the field; empty rows are dropped by the server. */
@Composable
private fun RowsEditor(f: F, current: JsonElement?, onChange: (JsonElement) -> Unit) {
    val rows = (current as? JsonArray)?.mapNotNull { (it as? JsonObject)?.mapValues { e -> (e.value as? JsonPrimitive)?.content.orEmpty() } } ?: emptyList()
    fun emit(next: List<Map<String, String>>) = onChange(JsonArray(next.map { r -> JsonObject(r.mapValues { JsonPrimitive(it.value) }) }))
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        rows.forEachIndexed { i, row ->
            Surface(color = MaterialTheme.colorScheme.surface, shape = RoundedCornerShape(20.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    f.cols.forEach { (k, label) ->
                        val num = k == "seats" || k == "fee"
                        NebDialogTextField(value = row[k].orEmpty(), label = label, singleLine = true, modifier = Modifier.fillMaxWidth(),
                            onValueChange = { v -> emit(rows.toMutableList().also { it[i] = row + (k to (if (num) v.filter(Char::isDigit) else v)) }) })
                    }
                    androidx.compose.material3.TextButton(onClick = { emit(rows.filterIndexed { j, _ -> j != i }) }) { Text("Remove") }
                }
            }
        }
        androidx.compose.material3.FilledTonalButton(onClick = { emit(rows + mapOf(f.cols.first().first to "")) }, modifier = Modifier.fillMaxWidth()) { Text("Add ${f.label.lowercase()}") }
    }
}
