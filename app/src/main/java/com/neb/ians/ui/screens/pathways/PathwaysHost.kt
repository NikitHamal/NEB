@file:OptIn(androidx.compose.animation.ExperimentalAnimationApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

/** Navigation inside Pathways. One string stack ("home|level:after12|route:bsc-csit") survives rotation and process death. */
internal class PwNav(val push: (String) -> Unit, val pop: () -> Unit, val tab: (String) -> Unit)

@Composable
fun PathwaysScreen(onNavigateBack: () -> Unit, viewModel: PathwaysViewModel = hiltViewModel()) {
    val ui by viewModel.state.collectAsStateWithLifecycle()
    var stackStr by rememberSaveable { mutableStateOf("home") }
    val nav = PwNav(
        push = { stackStr = "$stackStr|$it" },
        pop = { if (stackStr.contains("|")) stackStr = stackStr.substringBeforeLast("|") else onNavigateBack() },
        tab = { stackStr = it },
    )
    BackHandler { nav.pop() }
    val data = ui.data
    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface,
        contentWindowInsets = WindowInsets(0, 0, 0, 0),
        bottomBar = { PwBottomNav(stackStr.substringBefore("|"), nav.tab) },
    ) { inner ->
        Box(Modifier.fillMaxSize().padding(inner).statusBarsPadding()) {
            if (data == null) {
                Column(Modifier.fillMaxSize().padding(32.dp), verticalArrangement = androidx.compose.foundation.layout.Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                    if (ui.loading) CircularProgressIndicator()
                    else Text("Could not load Pathways. Check your connection and open it again.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                return@Box
            }
            AnimatedContent(
                targetState = stackStr,
                transitionSpec = {
                    val sameRoot = targetState.substringBefore("|") == initialState.substringBefore("|")
                    val deeper = targetState.length > initialState.length
                    val ease = FastOutSlowInEasing
                    when {
                        !sameRoot -> fadeIn(tween(180)) togetherWith fadeOut(tween(110))
                        deeper -> (slideInHorizontally(tween(280, easing = ease)) { it / 7 } + fadeIn(tween(220))) togetherWith
                            (slideOutHorizontally(tween(220, easing = ease)) { -it / 12 } + fadeOut(tween(120)))
                        else -> (slideInHorizontally(tween(280, easing = ease)) { -it / 12 } + fadeIn(tween(220))) togetherWith
                            (slideOutHorizontally(tween(220, easing = ease)) { it / 7 } + fadeOut(tween(120)))
                    }
                },
                label = "pwStack",
            ) { s -> PwDispatch(s.substringAfterLast("|"), data, ui, viewModel, nav) }
        }
    }
}

@Composable
private fun PwDispatch(top: String, d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val arg = top.substringAfter(":", "")
    when (top.substringBefore(":")) {
        "home" -> PwHome(d, ui, nav)
        "level" -> PwLevel(d, arg, ui, nav)
        "route" -> d.routeById[arg]?.let { PwRouteScreen(d, it, ui, vm, nav) }
        "where" -> PwColleges(d, ui, vm, nav, d.routeById[arg])
        "colleges" -> PwColleges(d, ui, vm, nav, null)
        "search" -> PwSearch(d, nav)
        "saved" -> PwSaved(d, ui, vm, nav)
        "faq" -> PwFaqScreen(d, nav)
        "lab" -> PwLab(d, nav, arg)
        "abroad" -> PwAbroadTab(d, nav)
        "country" -> d.abroad.firstOrNull { it.id == arg }?.let { PwCountry(d, it, ui, vm, nav) }
        "scholarships" -> PwScholarships(d, nav)
        "govt" -> PwGovtHome(d, nav)
        "job" -> d.govt.firstOrNull { it.id == arg }?.let { PwGovtDetail(it, ui, vm, nav) }
    }
}
