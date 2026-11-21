package com.neb.ians.ui.screens.profile

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.screens.institutions.StrengthCard

/** One thing a person can fill in: its name, its weight in the score, and whether it is filled. */
private data class Gap(val label: String, val weight: Int, val filled: Boolean, val tappable: Boolean = true)

private fun String?.has() = !this.isNullOrBlank()

/**
 * The same weights as the Profile concept (`SPEC` in NEBians-Profile.html): one list per account type drives the
 * score and the next steps. Nothing is required; the number only reflects how much the person chose to share.
 */
private fun gapsFor(p: UserProfileResponse, hasEntries: Boolean): List<Gap> = when (p.role) {
    "teacher" -> listOf(
        Gap("Current school", 15, p.school.has()), Gap("Type of work", 5, p.employment.has()),
        Gap("Subjects", 15, p.teachingSubjects.has()), Gap("Levels", 12, p.teachLevels.has()),
        Gap("Experience", 10, p.experienceYears > 0), Gap("About", 16, p.bio.has()),
        Gap("Skills", 5, p.skills.has()), Gap("Past schools", 22, hasEntries, tappable = false)
    )
    "explorer" -> listOf(
        Gap("About", 40, p.bio.has()),
        Gap("Skills", 30, p.skills.has()), Gap("Open to", 30, p.openTo.has())
    )
    else -> listOf(
        Gap("Class or program", 15, p.classLevel.has() || p.eduProgram.has()), Gap("School or college", 15, p.school.has()),
        Gap("About", 16, p.bio.has()), Gap("Skills", 16, p.skills.has()),
        Gap("Open to", 14, p.openTo.has()), Gap("Achievements and projects", 24, hasEntries, tappable = false)
    )
}

/** Owner-only card at the top of About: ring, one honest sentence, and the sections worth filling next. */
@Composable
fun ProfileStrengthCard(profile: UserProfileResponse, onEditProfile: () -> Unit) {
    val vm: PortfolioViewModel = hiltViewModel(key = "pf_" + profile.username)
    val state by vm.state.collectAsStateWithLifecycle()
    LaunchedEffect(profile.username) { vm.load(profile.username) }
    val gaps = remember(profile, state.sections) { gapsFor(profile, state.sections.isNotEmpty()) }
    val total = gaps.sumOf { it.weight }
    val percent = gaps.filter { it.filled }.sumOf { it.weight } * 100 / total
    val steps = gaps.filter { !it.filled && it.tappable }.sortedByDescending { it.weight }.take(4).map { it.label }
    StrengthCard(
        percent = percent,
        sentence = if (percent >= 90) "Complete. People get the full picture of you." else "Add what you like, whenever you like. Nothing is forced.",
        steps = steps,
        onStep = { onEditProfile() }
    )
}
