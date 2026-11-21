package com.neb.ians.ui.screens.profile.edit

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Badge
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel

// The portfolio header every account can fill, and what a teacher adds. Nothing here is required.
private val SKILLS = listOf("Python", "Public speaking", "Design", "Writing", "Chess", "Debate", "Guitar", "Maths olympiad")
private val OPEN_TO = listOf(
    "study_partner" to "Study partner", "mentoring" to "Mentoring juniors", "get_mentored" to "Finding a mentor",
    "tutoring" to "Tutoring", "collab" to "Project collab", "internship" to "Internships",
    "freelance" to "Freelance work", "hiring" to "Hiring", "scholarship" to "Scholarship info", "notes_swap" to "Swapping notes"
)
private val LEVELS = listOf(
    "preprimary" to "Pre-primary", "basic_1_5" to "Basic 1 to 5", "basic_6_8" to "Basic 6 to 8",
    "secondary_9_10" to "Secondary 9 to 10", "plus_two" to "+2", "a_level" to "A Level", "diploma" to "Diploma / TSLC",
    "bachelor" to "Bachelor's", "master" to "Master's", "phd" to "PhD", "coaching" to "Entrance coaching"
)
private val EMPLOYMENT = listOf("full_time" to "Full time", "part_time" to "Part time", "tutor" to "Home tutor", "freelance" to "Freelance", "visiting" to "Visiting")

@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun EditPortfolioSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    if (state.role == "institution" && !state.ownedKnown) return
    val gap = Arrangement.spacedBy(8.dp)
    EditSection(title = "Portfolio") {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
            if (state.role == "institution" && state.ownedKnown) {
                val manage = com.neb.ians.ui.screens.institutions.LocalManageInstitution.current
                val find = com.neb.ians.ui.screens.institutions.LocalOpenSchools.current
                androidx.compose.material3.FilledTonalButton(
                    onClick = { if (state.schoolSlug.isNotBlank()) manage(state.schoolSlug) else find() },
                    modifier = Modifier.fillMaxWidth()
                ) { androidx.compose.material3.Text(if (state.schoolSlug.isNotBlank()) "Edit institution portfolio" else "Find and claim your institution") }
            }
            if (state.role == "teacher") {
                Column {
                    NebFieldGroupLabel(text = "Levels you teach")
                    Spacer(Modifier.height(10.dp))
                    FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                        LEVELS.forEach { (k, l) -> NebSelectChip(l, k in state.teachLevels, { viewModel.toggleTeachLevel(k) }) }
                    }
                }
                NebAuthField(
                    value = state.experienceYears,
                    onValueChange = viewModel::onExperienceChange,
                    label = "Years of teaching",
                    leadingIcon = Icons.Outlined.Schedule,
                    keyboardType = KeyboardType.Number
                )
                Column {
                    NebFieldGroupLabel(text = "Type of work")
                    Spacer(Modifier.height(10.dp))
                    FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                        EMPLOYMENT.forEach { (k, l) -> NebSelectChip(l, state.employment == k, { viewModel.onEmploymentChange(k) }) }
                    }
                }
            }
            if (state.role != "institution") {
                Column {
                    NebFieldGroupLabel(text = "Skills")
                    Spacer(Modifier.height(10.dp))
                    FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                        (SKILLS + state.skills.filter { it !in SKILLS }).forEach { s ->
                            NebSelectChip(s, s in state.skills, { viewModel.toggleSkill(s) })
                        }
                    }
                }
                Column {
                    NebFieldGroupLabel(text = "Open to")
                    Spacer(Modifier.height(10.dp))
                    FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                        OPEN_TO.forEach { (k, l) -> NebSelectChip(l, k in state.openTo, { viewModel.toggleOpenTo(k) }) }
                    }
                }
            }
        }
    }
}
