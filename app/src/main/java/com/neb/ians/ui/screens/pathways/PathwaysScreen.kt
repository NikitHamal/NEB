@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.HelpOutline
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.MilitaryTech
import androidx.compose.material.icons.outlined.Payments
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.WorkspacePremium
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.nebHorizontalScroll
import com.neb.ians.ui.theme.nebFloatColor

private const val TAB_ABROAD = "abroad"
private const val TAB_SCHOLARSHIPS = "scholarships"
private const val TAB_FAQ = "faq"

private fun stageIcon(name: String): ImageVector = when (name) {
    "menu_book" -> Icons.AutoMirrored.Outlined.MenuBook
    "school" -> Icons.Outlined.School
    "workspace_premium" -> Icons.Outlined.WorkspacePremium
    "military_tech" -> Icons.Outlined.MilitaryTech
    else -> Icons.Outlined.School
}

@Composable
fun PathwaysScreen(onNavigateBack: () -> Unit, viewModel: PathwaysViewModel = hiltViewModel()) {
    val ui by viewModel.state.collectAsStateWithLifecycle()
    var tab by rememberSaveable { mutableStateOf("after10") }
    var open by rememberSaveable { mutableStateOf<String?>(null) }
    var group by rememberSaveable { mutableStateOf("") }
    val data = ui.data
    Scaffold(
        topBar = { WebTopBar(title = "Pathways", showBack = true, onBackClick = onNavigateBack) },
        containerColor = MaterialTheme.colorScheme.surface,
    ) { inner ->
        Column(Modifier.fillMaxSize().padding(inner)) {
            if (data == null) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    if (ui.loading) CircularProgressIndicator()
                    else Text("Could not load Pathways. Check your connection and open it again.", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(32.dp))
                }
                return@Column
            }
            Row(
                Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                data.stages.forEach { s -> PwTab(s.label, stageIcon(s.icon), tab == s.id) { tab = s.id; group = "" } }
                PwTab("Abroad", Icons.Outlined.Public, tab == TAB_ABROAD) { tab = TAB_ABROAD }
                PwTab("Scholarships", Icons.Outlined.Payments, tab == TAB_SCHOLARSHIPS) { tab = TAB_SCHOLARSHIPS }
                if (data.faq.isNotEmpty()) PwTab("Questions", Icons.AutoMirrored.Outlined.HelpOutline, tab == TAB_FAQ) { tab = TAB_FAQ }
            }
            when (tab) {
                TAB_ABROAD -> AbroadList(Modifier.weight(1f), data)
                TAB_SCHOLARSHIPS -> ScholarshipList(Modifier.weight(1f), data)
                TAB_FAQ -> FaqList(Modifier.weight(1f), data) { open = it }
                else -> StageList(Modifier.weight(1f), data, tab, group, { group = it }) { open = it }
            }
            Text(
                "Indicative figures reviewed ${data.reviewed}. Confirm fees, seats and dates with the institution.",
                style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp).navigationBarsPadding(),
            )
        }
    }
    val route = open?.let { data?.routeById?.get(it) }
    if (data != null && route != null) {
        NebModalSheet(onDismiss = { open = null }, horizontalPadding = 20.dp) {
            RouteDetail(data, route, ui, viewModel) { open = it }
        }
    }
}

@Composable
private fun PwTab(label: String, icon: ImageVector, selected: Boolean, onClick: () -> Unit) {
    Surface(
        onClick = onClick, shape = RoundedCornerShape(22.dp),
        color = if (selected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceContainerLowest,
        contentColor = if (selected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
        border = if (selected) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Row(Modifier.height(44.dp).padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Icon(icon, null, Modifier.size(20.dp))
            Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, maxLines = 1)
        }
    }
}

@Composable
private fun Tag(text: String, tertiary: Boolean = false) {
    val c = MaterialTheme.colorScheme
    Surface(shape = RoundedCornerShape(12.dp), color = if (tertiary) c.tertiaryContainer else c.secondaryContainer, contentColor = if (tertiary) c.onTertiaryContainer else c.onSecondaryContainer) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 4.dp), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
internal fun PwCard(modifier: Modifier = Modifier, onClick: (() -> Unit)? = null, content: @Composable () -> Unit) {
    val shape = RoundedCornerShape(24.dp)
    Surface(
        modifier = modifier.fillMaxWidth().clip(shape).then(if (onClick != null) Modifier.clickable(onClick = onClick) else Modifier),
        shape = shape, color = MaterialTheme.colorScheme.surfaceContainerLowest, border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) { Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) { content() } }
}

@Composable
internal fun Soft(text: String) = Text(text, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)

private val GROUP_LABEL = mapOf(
    "school" to "School", "tech" to "Engineering and IT", "sci" to "Science", "health" to "Health", "biz" to "Business", "arts" to "Arts and media",
    "edu" to "Education", "law" to "Law", "ag" to "Agriculture", "gov" to "Government", "abroad" to "Abroad",
)

@Composable
private fun StageList(modifier: Modifier, data: PwData, stageId: String, group: String, onGroup: (String) -> Unit, onOpen: (String) -> Unit) {
    val stage = data.stages.firstOrNull { it.id == stageId } ?: return
    val all = data.routes.filter { it.stage == stageId }
    val groups = all.map { it.group }.distinct()
    val list = all.filter { group.isEmpty() || it.group == group }
    LazyColumn(modifier.fillMaxWidth(), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("intro") {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(stage.label, style = MaterialTheme.typography.headlineSmall)
                Soft(stage.blurb)
                Soft(stage.tip)
            }
        }
        if (groups.size > 1) item("filters") {
            Row(Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                FilterPill("All", group.isEmpty()) { onGroup("") }
                groups.forEach { g -> FilterPill(GROUP_LABEL[g] ?: g, group == g) { onGroup(if (group == g) "" else g) } }
            }
        }
        items(list, key = { it.id }) { r ->
            PwCard(onClick = { onOpen(r.id) }) {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) { Tag(r.kind); Tag(GROUP_LABEL[r.group] ?: r.group, tertiary = true) }
                Text(r.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                Soft("${r.years}  |  ${feeText(r.feeMin, r.feeMax)}")
                Text(r.about, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2)
            }
        }
    }
}

@Composable
internal fun FilterPill(label: String, on: Boolean, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = onClick, shape = RoundedCornerShape(18.dp),
        color = if (on) c.secondaryContainer else Color.Transparent,
        contentColor = if (on) c.onSecondaryContainer else c.onSurfaceVariant,
        border = if (on) null else BorderStroke(1.dp, c.outlineVariant),
    ) { Text(label, Modifier.padding(horizontal = 14.dp, vertical = 9.dp), style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold) }
}

@Composable
private fun Meter(label: String, fraction: Float, color: Color, text: String, from: Float = 0f) {
    val p by animateFloatAsState(fraction, spring(Spring.DampingRatioLowBouncy, Spring.StiffnessLow), label = "pw_meter")
    val track = MaterialTheme.colorScheme.surfaceContainerHigh
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(label, Modifier.width(92.dp), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
        Box(
            Modifier.weight(1f).height(8.dp).drawBehind {
                drawRoundRect(track, size = size, cornerRadius = CornerRadius(4.dp.toPx()))
                drawRoundRect(color, topLeft = Offset(size.width * from, 0f), size = Size(size.width * (p - from).coerceAtLeast(0.03f), size.height), cornerRadius = CornerRadius(4.dp.toPx()))
            }
        )
        Text(text, Modifier.width(78.dp), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.SemiBold, maxLines = 1)
    }
}

@Composable
private fun AbroadList(modifier: Modifier, data: PwData) {
    val c = MaterialTheme.colorScheme
    val max = 11_000_000f
    LazyColumn(modifier.fillMaxWidth(), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("intro") {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("Study abroad", style = MaterialTheme.typography.headlineSmall)
                Soft("Yearly cost bars show the low to high range in NPR on one shared scale.")
            }
        }
        items(data.abroad, key = { it.id }) { a ->
            PwCard {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text(a.country, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                    Tag(a.intakes)
                }
                Meter("Tuition / yr", a.tuitionMax / max, c.primary, if (a.tuitionMax == 0L) "Free" else money(a.tuitionMax), from = a.tuitionMin / max)
                Meter("Living / yr", a.livingMax / max, c.secondary, money(a.livingMax), from = a.livingMin / max)
                FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { a.fields.forEach { Tag(it, tertiary = true) } }
                Soft("Tests: ${a.exams.joinToString(", ")}.")
                Soft("${a.work}. ${a.note}")
            }
        }
    }
}

@Composable
private fun ScholarshipList(modifier: Modifier, data: PwData) {
    var scope by rememberSaveable { mutableStateOf("") }
    val list = data.scholarships.filter { scope.isEmpty() || it.scope == scope }
    LazyColumn(modifier.fillMaxWidth(), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("head") {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Scholarships", style = MaterialTheme.typography.headlineSmall)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterPill("All", scope.isEmpty()) { scope = "" }
                    FilterPill("In Nepal", scope == "nepal") { scope = if (scope == "nepal") "" else "nepal" }
                    FilterPill("Abroad", scope == "abroad") { scope = if (scope == "abroad") "" else "abroad" }
                }
            }
        }
        items(list, key = { it.id }) { s ->
            PwCard {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) { Tag(if (s.scope == "nepal") "Nepal" else "Abroad"); Tag(s.levels.joinToString(", "), tertiary = true) }
                Text(s.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                Soft(s.by)
                Soft("Covers: ${s.covers}")
                Soft("Who: ${s.who}")
                Soft("How: ${s.how}")
            }
        }
    }
}

@Composable
private fun Section(title: String, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(title.uppercase(), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
        content()
    }
}

@Composable
private fun RouteDetail(data: PwData, r: PwRoute, ui: PathwaysUiState, vm: PathwaysViewModel, onOpen: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    var menu by remember { mutableStateOf(false) }
    val kind = if (r.kind == "Diploma" || r.kind == "Technical") "institute" else if (r.stage == "afterbach") "university" else "college"
    val here = r.where.mapNotNull { data.providers[it] }.filter { ui.district.isEmpty() || it.district == ui.district }
    Column(Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(bottom = 28.dp), verticalArrangement = Arrangement.spacedBy(20.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) { Tag(r.kind); Tag(GROUP_LABEL[r.group] ?: r.group, tertiary = true) }
            Text(r.name, style = MaterialTheme.typography.headlineSmall)
            Text(r.about, style = MaterialTheme.typography.bodyMedium, color = c.onSurfaceVariant)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Stat("Duration", r.years, Modifier.weight(1f)); Stat("Total cost", feeText(r.feeMin, r.feeMax).removePrefix("NPR "), Modifier.weight(1f))
        }
        Section("Who can apply") { Soft(r.entry); Soft("Exam: ${r.exam}") }
        if (r.skills.isNotEmpty()) Section("Skills you build") {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { r.skills.forEach { Tag(it) } }
        }
        val cs = r.careers.mapNotNull { data.careers[it] }
        if (cs.isNotEmpty()) Section("Careers it leads to") {
            cs.forEach { k ->
                PwCard {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Text(k.name, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                        Tag(k.trend)
                    }
                    Soft(k.about)
                    Meter("Demand", k.demand / 5f, c.primary, "${k.demand} of 5")
                    Meter("Competition", k.competition / 5f, c.tertiary, "${k.competition} of 5")
                    Meter("Abroad demand", k.abroad / 5f, c.primary, "${k.abroad} of 5")
                    Meter("Monthly pay", k.seniorMax / 600_000f, c.secondary, "${money(k.entryMin)} to ${money(k.seniorMax)}", from = k.entryMin / 600_000f)
                }
            }
        }
        if (r.next.isNotEmpty()) Section("Next steps") {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                r.next.mapNotNull { data.routeById[it] }.forEach { n -> FilterPill(n.name, false) { onOpen(n.id) } }
            }
        }
        Section("Where to study") {
            Box {
                Surface(onClick = { menu = true }, shape = RoundedCornerShape(18.dp), color = c.surfaceContainerLow, border = BorderStroke(1.dp, c.outlineVariant)) {
                    Row(Modifier.fillMaxWidth().height(48.dp).padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(ui.district.ifEmpty { "All districts" }, Modifier.weight(1f), style = MaterialTheme.typography.bodyLarge)
                        Icon(Icons.Outlined.ExpandMore, null)
                    }
                }
                DropdownMenu(expanded = menu, onDismissRequest = { menu = false }, containerColor = nebFloatColor(), tonalElevation = 0.dp, shadowElevation = 0.dp) {
                    DropdownMenuItem(text = { Text("All districts") }, onClick = { menu = false; vm.setDistrict("", kind) })
                    NEPAL_DISTRICT_LIST.forEach { d -> DropdownMenuItem(text = { Text(d) }, onClick = { menu = false; vm.setDistrict(d, kind) }) }
                }
            }
            here.forEach { p ->
                PwCard { Text(p.name, fontWeight = FontWeight.SemiBold); Soft("${p.kind}, ${p.sector}, ${p.place}, ${p.district}"); Soft(p.note) }
            }
            if (here.isEmpty()) Soft(if (ui.district.isEmpty()) "Pick a district to see providers near you." else "No listed provider in ${ui.district} yet. Colleges found there:")
            ui.live.forEach { p -> PwCard { Text(p.name, fontWeight = FontWeight.SemiBold); Soft(p.where) } }
        }
    }
}

@Composable
private fun Stat(label: String, value: String, modifier: Modifier) {
    Surface(modifier, shape = RoundedCornerShape(18.dp), color = MaterialTheme.colorScheme.surfaceContainer) {
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(value, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
