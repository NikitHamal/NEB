package com.neb.ians.ui.screens.profile.edit

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel

/**
 * The situation under a level: what you are doing there, which course, which year, what you finished.
 * Every part is optional and can be filled in later; the lists come from the server.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun EduSituation(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel, modifier: Modifier = Modifier) {
    LaunchedEffect(Unit) { viewModel.loadEduCatalog() }
    val cat = state.eduCatalog ?: return
    if (state.role == "institution") return
    val gap = Arrangement.spacedBy(8.dp)
    val level = cat.levels.firstOrNull { it.value == state.classLevel.removePrefix("Class ") || it.label == state.classLevel }
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Column {
            NebFieldGroupLabel("Right now")
            Spacer(Modifier.height(10.dp))
            FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                cat.statuses.forEach { s -> NebSelectChip(s.label, state.eduStatus == s.value, { viewModel.onEduStatus(s.value) }) }
            }
        }
        if (level != null && level.programs.isNotEmpty()) Column {
            NebFieldGroupLabel(level.programLabel.ifBlank { "Course" })
            Spacer(Modifier.height(10.dp))
            FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                level.programs.forEach { p -> NebSelectChip(p, state.eduProgram == p, { viewModel.onEduProgram(p) }) }
            }
        }
        val terms = when (level?.terms) {
            "year" -> cat.terms["year"]
            "part" -> cat.terms["part"]
            "any" -> (cat.terms["year"].orEmpty() + cat.terms["semester"].orEmpty())
            else -> null
        }
        if (!terms.isNullOrEmpty()) Column {
            NebFieldGroupLabel("Year or semester")
            Spacer(Modifier.height(10.dp))
            FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                (terms + cat.terms["finished"].orEmpty()).forEach { t -> NebSelectChip(t, state.eduTerm == t, { viewModel.onEduTerm(t) }) }
            }
        }
        if (cat.statuses.firstOrNull { it.value == state.eduStatus }?.askCompleted == true) Column {
            NebFieldGroupLabel("Last level you finished")
            Spacer(Modifier.height(10.dp))
            FlowRow(Modifier.fillMaxWidth(), horizontalArrangement = gap, verticalArrangement = gap) {
                cat.completed.forEach { c -> NebSelectChip(c.label, state.eduCompleted == c.value, { viewModel.onEduCompleted(c.value) }) }
            }
        }
    }
}
