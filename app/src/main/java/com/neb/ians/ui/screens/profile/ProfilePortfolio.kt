package com.neb.ians.ui.screens.profile

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.EmojiEvents
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.VolunteerActivism
import androidx.compose.material.icons.outlined.Work
import androidx.compose.material.icons.outlined.WorkspacePremium
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiEntry
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.WebPanelShape

private val KINDS = listOf(
    Triple("education", "Education", Icons.Outlined.School),
    Triple("experience", "Experience", Icons.Outlined.Work),
    Triple("project", "Projects", Icons.Outlined.Code),
    Triple("achievement", "Achievements", Icons.Outlined.EmojiEvents),
    Triple("certificate", "Certificates", Icons.Outlined.WorkspacePremium),
    Triple("volunteering", "Volunteering", Icons.Outlined.VolunteerActivism)
)
private val OPEN = mapOf(
    "study_partner" to "Study partner", "mentoring" to "Mentoring juniors", "get_mentored" to "Finding a mentor",
    "tutoring" to "Tutoring", "collab" to "Project collab", "internship" to "Internships",
    "freelance" to "Freelance work", "hiring" to "Hiring", "scholarship" to "Scholarship info", "notes_swap" to "Swapping notes"
)
private val STATUS = mapOf(
    "studying" to "Studying", "completed" to "Graduated", "preparing" to "Preparing", "gap_year" to "Taking a break",
    "dropped_out" to "Dropped out", "working" to "Working", "self_learning" to "Self-learning", "abroad" to "Studying abroad"
)
private val MONTHS = listOf("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

private fun when_(e: ApiEntry): String {
    fun f(v: String) = v.split("-").let { p -> (p.getOrNull(1)?.toIntOrNull()?.let { MONTHS.getOrNull(it - 1) + " " } ?: "") + p[0] }
    if (e.start.isBlank() && !e.isCurrent) return ""
    return f(e.start) + if (e.isCurrent) " to now" else if (e.end.isNotBlank()) " to " + f(e.end) else ""
}

internal fun eduLine(p: UserProfileResponse): String {
    val level = p.classLevel.orEmpty(); val program = p.eduProgram.orEmpty(); val term = p.eduTerm.orEmpty()
    val parts = if (level.startsWith("Class")) listOf(level, program) else listOf(program.ifBlank { level }, term)
    return parts.filter { it.isNotBlank() }.joinToString(" \u00B7 ")
}

@Composable
private fun Tag(text: String, icon: ImageVector? = null) {
    Row(
        Modifier.clip(RoundedCornerShape(10.dp)).background(MaterialTheme.colorScheme.secondaryContainer)
            .padding(horizontal = 10.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        if (icon != null) Icon(icon, null, Modifier.size(14.dp), tint = MaterialTheme.colorScheme.onSecondaryContainer)
        Text(text, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSecondaryContainer)
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ProfilePortfolioCard(profile: UserProfileResponse, isSelf: Boolean, modifier: Modifier = Modifier, vm: PortfolioViewModel = hiltViewModel(key = "pf_" + profile.username)) {
    val state by vm.state.collectAsStateWithLifecycle()
    LaunchedEffect(profile.username) { vm.load(profile.username) }
    var editing by remember { mutableStateOf<ApiEntry?>(null) }
    val edu = eduLine(profile)
    val status = STATUS[profile.eduStatus.orEmpty()].orEmpty()
    val open = profile.openTo.orEmpty().split(",").mapNotNull { OPEN[it] }
    val skills = profile.skills.orEmpty().split(",").filter { it.isNotBlank() }
    val hasAny = edu.isNotBlank() || status.isNotBlank() || open.isNotEmpty() || skills.isNotEmpty() || state.sections.isNotEmpty()
    if (!hasAny && !isSelf) return
    val line = MaterialTheme.colorScheme.outlineVariant
    Card(modifier.fillMaxWidth().animateContentSize(), shape = WebPanelShape, border = BorderStroke(1.dp, line),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
            if (edu.isNotBlank() || status.isNotBlank()) Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(Modifier.size(40.dp).clip(RoundedCornerShape(14.dp)).background(MaterialTheme.colorScheme.primaryContainer), Alignment.Center) {
                    Icon(Icons.Outlined.School, null, Modifier.size(20.dp), tint = MaterialTheme.colorScheme.onPrimaryContainer)
                }
                Column(Modifier.weight(1f)) { Text(edu.ifBlank { status }, fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall) }
                if (status.isNotBlank() && edu.isNotBlank()) Tag(status)
            }
            if (open.isNotEmpty()) PfBlock("Open to") { FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { open.forEach { Tag(it) } } }
            if (skills.isNotEmpty()) PfBlock("Skills") { FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { skills.forEach { Tag(it) } } }
            state.sections.forEach { sec ->
                val icon = KINDS.firstOrNull { it.first == sec.value }?.third ?: Icons.Outlined.Work
                PfBlock(sec.label, icon, if (isSelf) ({ editing = ApiEntry(kind = sec.value) }) else null) {
                    sec.items.forEachIndexed { i, e -> TimelineRow(e, last = i == sec.items.lastIndex, own = isSelf) { editing = e } }
                }
            }
            if (isSelf) PfBlock("Add to your portfolio") {
                FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    KINDS.forEach { (k, l, ic) ->
                        Row(Modifier.clip(RoundedCornerShape(10.dp)).clickable { editing = ApiEntry(kind = k) }.background(MaterialTheme.colorScheme.surfaceContainerHigh)
                            .padding(horizontal = 10.dp, vertical = 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            Icon(ic, null, Modifier.size(16.dp)); Text(l, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
                        }
                    }
                }
            }
        }
    }
    editing?.let { e ->
        PortfolioEntrySheet(e, KINDS.firstOrNull { it.first == e.kind }?.second ?: "Entry", state.saving, state.error,
            onSave = { vm.save(it) { editing = null } },
            onDelete = if (e.id != 0) ({ vm.delete(e.id) { editing = null } }) else null,
            onDismiss = { editing = null; vm.clearError() })
    }
}

@Composable
private fun PfBlock(title: String, icon: ImageVector? = null, onAdd: (() -> Unit)? = null, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (icon != null) Icon(icon, null, Modifier.size(18.dp), tint = MaterialTheme.colorScheme.primary)
            Text(title, Modifier.weight(1f), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            if (onAdd != null) IconButton(onAdd, Modifier.size(36.dp)) { Icon(Icons.Outlined.Add, "Add to $title", Modifier.size(20.dp)) }
        }
        content()
    }
}

@Composable
private fun TimelineRow(e: ApiEntry, last: Boolean, own: Boolean, onEdit: () -> Unit) {
    val uri = LocalUriHandler.current
    val line = MaterialTheme.colorScheme.outlineVariant
    Row(Modifier.fillMaxWidth().height(IntrinsicSize.Min)) {
        Column(Modifier.width(18.dp).padding(top = 6.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Box(Modifier.size(8.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary))
            if (!last) Box(Modifier.width(2.dp).weight(1f).background(line))
        }
        Column(Modifier.weight(1f).padding(bottom = if (last) 0.dp else 14.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(e.title, fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.bodyMedium)
            if (e.org.isNotBlank()) Text(e.org, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            val w = when_(e); if (w.isNotBlank()) Text(w, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            if (e.description.isNotBlank()) { Spacer(Modifier.height(2.dp)); Text(e.description, style = MaterialTheme.typography.bodySmall) }
            if (e.url.isNotBlank()) Text(e.url.removePrefix("https://").removePrefix("http://").take(40), color = MaterialTheme.colorScheme.primary,
                style = MaterialTheme.typography.bodySmall, modifier = Modifier.clickable { uri.openUri(e.url) })
        }
        if (own) IconButton(onEdit, Modifier.size(36.dp)) { Icon(Icons.Outlined.Edit, "Edit ${e.title}", Modifier.size(18.dp)) }
    }
}
