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
import androidx.compose.material.icons.outlined.HistoryEdu
import androidx.compose.material.icons.outlined.Schedule
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
import com.neb.ians.ui.screens.institutions.AddSlot
import com.neb.ians.ui.screens.institutions.PCard
import com.neb.ians.ui.screens.institutions.StatGrid
import androidx.compose.material.icons.outlined.Star

private val KINDS = listOf(
    Triple("education", "Education", Icons.Outlined.School),
    Triple("experience", "Experience", Icons.Outlined.Work),
    Triple("past_school", "Past schools", Icons.Outlined.HistoryEdu),
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
private val TEACH_LEVELS = mapOf(
    "preprimary" to "Pre-primary", "basic_1_5" to "Basic 1 to 5", "basic_6_8" to "Basic 6 to 8",
    "secondary_9_10" to "Secondary 9 to 10", "plus_two" to "+2", "a_level" to "A Level", "diploma" to "Diploma / TSLC",
    "bachelor" to "Bachelor's", "master" to "Master's", "phd" to "PhD", "coaching" to "Entrance coaching"
)
private val EMPLOY = mapOf(
    "full_time" to "Full time", "part_time" to "Part time", "tutor" to "Home tutor", "freelance" to "Freelance", "visiting" to "Visiting"
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
private fun Tag(text: String, icon: ImageVector? = null, primary: Boolean = false) {
    val bg = if (primary) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer
    val fg = if (primary) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSecondaryContainer
    Row(
        Modifier.clip(RoundedCornerShape(12.dp)).background(bg)
            .padding(horizontal = 12.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        if (icon != null) Icon(icon, null, Modifier.size(14.dp), tint = fg)
        Text(text, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold, color = fg)
    }
}

/**
 * The profile body from the locked Profile concept: one calm card per section (a stat pair, what a teacher teaches,
 * a schools timeline, studying, skills, portfolio entries) with a dashed prompt where the owner has not filled one yet.
 * Nothing is required; every card is optional and the owner adds them whenever they like.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ProfilePortfolioCard(
    profile: UserProfileResponse, isSelf: Boolean, modifier: Modifier = Modifier, onEditProfile: () -> Unit = {},
    vm: PortfolioViewModel = hiltViewModel(key = "pf_" + profile.username)
) {
    val state by vm.state.collectAsStateWithLifecycle()
    LaunchedEffect(profile.username) { vm.load(profile.username) }
    var editing by remember { mutableStateOf<ApiEntry?>(null) }
    val edu = eduLine(profile)
    val status = STATUS[profile.eduStatus.orEmpty()].orEmpty()
    val open = profile.openTo.orEmpty().split(",").mapNotNull { OPEN[it] }
    val skills = profile.skills.orEmpty().split(",").filter { it.isNotBlank() }
    val teacher = profile.role == "teacher"
    val subjects = if (teacher) profile.teachingSubjects.orEmpty().split(",").filter { it.isNotBlank() } else emptyList()
    val levels = if (teacher) profile.teachLevels.orEmpty().split(",").mapNotNull { TEACH_LEVELS[it] } else emptyList()
    val years = if (teacher) profile.experienceYears else 0
    val work = if (teacher) EMPLOY[profile.employment.orEmpty()].orEmpty() else ""
    val school = if (teacher) profile.school.orEmpty() else ""
    val past = if (teacher) state.sections.firstOrNull { it.value == "past_school" }?.items.orEmpty() else emptyList()
    val sections = state.sections.filter { !teacher || it.value != "past_school" }
    val hasAny = school.isNotBlank() || subjects.isNotEmpty() || levels.isNotEmpty() || years > 0 || past.isNotEmpty() ||
        edu.isNotBlank() || status.isNotBlank() || open.isNotEmpty() || skills.isNotEmpty() || sections.isNotEmpty()
    if (!hasAny && !isSelf) return
    val edit = if (isSelf) "edit" else null
    Column(modifier.fillMaxWidth().animateContentSize(), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (teacher) {
            val count = (if (school.isNotBlank()) 1 else 0) + past.size
            if (years > 0 || count > 0) StatGrid(listOf("Years teaching" to years.toString(), "Schools" to count.toString()))
            if (subjects.isNotEmpty() || levels.isNotEmpty()) PCard("Teaches", Icons.Outlined.Star, edit, { onEditProfile() }) {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    if (subjects.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { subjects.forEach { Tag(it, primary = true) } }
                    if (levels.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { levels.forEach { Tag(it) } }
                }
            } else if (isSelf) AddSlot("Add subjects and levels you teach", onEditProfile)
            if (school.isNotBlank() || past.isNotEmpty()) PCard("Schools", Icons.Outlined.School, edit, { onEditProfile() }) {
                Column {
                    if (school.isNotBlank()) Column(Modifier.padding(bottom = if (past.isEmpty()) 0.dp else 14.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(school, fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall)
                        Text(listOf(work.ifBlank { "Current school" }, "Present").joinToString(" \u00B7 "), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    past.forEachIndexed { i, e -> TimelineRow(e, last = i == past.lastIndex, own = isSelf) { editing = e } }
                }
            } else if (isSelf) AddSlot("Add your school", onEditProfile)
            if (isSelf) AddSlot("Add a past school") { editing = ApiEntry(kind = "past_school") }
        }
        if (!teacher && (edu.isNotBlank() || status.isNotBlank())) PCard("Studying", Icons.Outlined.School, edit, { onEditProfile() }) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(Modifier.size(44.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.primaryContainer), Alignment.Center) {
                    Icon(Icons.Outlined.School, null, Modifier.size(22.dp), tint = MaterialTheme.colorScheme.onPrimaryContainer)
                }
                Column(Modifier.weight(1f)) {
                    Text(edu.ifBlank { status }, fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall)
                    if (!profile.school.isNullOrBlank()) Text(profile.school.orEmpty(), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                if (status.isNotBlank() && edu.isNotBlank()) Tag(status)
            }
        } else if (!teacher && isSelf) AddSlot("Add your class and school", onEditProfile)
        if (skills.isNotEmpty()) PCard("Skills", Icons.Outlined.Star, edit, { onEditProfile() }) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { skills.forEach { Tag(it, primary = true) } }
        } else if (isSelf) AddSlot("Add skills", onEditProfile)
        if (open.isNotEmpty()) PCard("Open to", Icons.Outlined.VolunteerActivism, edit, { onEditProfile() }) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) { open.forEach { Tag(it) } }
        }
        sections.forEach { sec ->
            val icon = KINDS.firstOrNull { it.first == sec.value }?.third ?: Icons.Outlined.Work
            PCard(sec.label, icon, null, {}) {
                Column {
                    sec.items.forEachIndexed { i, e -> TimelineRow(e, last = i == sec.items.lastIndex, own = isSelf) { editing = e } }
                }
            }
        }
        if (isSelf) PCard("Add to your portfolio", Icons.Outlined.Add, null, {}) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                KINDS.filter { it.first != "past_school" }.forEach { (k, l, ic) ->
                    Row(Modifier.clip(RoundedCornerShape(12.dp)).clickable { editing = ApiEntry(kind = k) }.background(MaterialTheme.colorScheme.surfaceContainerHigh)
                        .padding(horizontal = 12.dp, vertical = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Icon(ic, null, Modifier.size(16.dp)); Text(l, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
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
