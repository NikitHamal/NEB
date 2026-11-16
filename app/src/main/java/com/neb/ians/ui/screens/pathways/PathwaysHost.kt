@file:OptIn(androidx.compose.animation.ExperimentalAnimationApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Checklist
import androidx.compose.material.icons.outlined.Flag
import androidx.compose.material.icons.outlined.Route
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.TaskAlt
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.saveable.rememberSaveableStateHolder
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

/** Navigation inside Pathways. One string stack ("explore|route:bsc-csit|career:software-dev") survives rotation and process death. */
internal class PwNav(val push: (String) -> Unit, val pop: () -> Unit, val tab: (String) -> Unit)

private data class PwNavItem(val key: String, val icon: ImageVector, val label: String)
private val NAV = listOf(
    PwNavItem("explore", Icons.Outlined.Route, "Explore"),
    PwNavItem("study", Icons.Outlined.School, "Study"),
    PwNavItem("exams", Icons.Outlined.TaskAlt, "Exams"),
    PwNavItem("guides", Icons.Outlined.Checklist, "Guides"),
    PwNavItem("plan", Icons.Outlined.Flag, "Plan"),
)
private val ROOTS = NAV.map { it.key }.toSet()

@Composable
fun PathwaysScreen(onNavigateBack: () -> Unit, viewModel: PathwaysViewModel = hiltViewModel()) {
    val ui by viewModel.state.collectAsStateWithLifecycle()
    var stackStr by rememberSaveable { mutableStateOf("explore") }
    val exit by rememberUpdatedState(onNavigateBack)
    val nav = remember {
        PwNav(
            push = { stackStr = "$stackStr|$it" },
            pop = { if (stackStr.contains("|")) stackStr = stackStr.substringBeforeLast("|") else exit() },
            tab = { stackStr = it },
        )
    }
    BackHandler { nav.pop() }
    val holder = rememberSaveableStateHolder()
    val data = ui.data
    val atRoot = !stackStr.contains("|")
    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface,
        contentWindowInsets = WindowInsets(0, 0, 0, 0),
        bottomBar = {
            AnimatedVisibility(atRoot && data != null, enter = expandVertically() + fadeIn(), exit = shrinkVertically() + fadeOut()) {
                PwBottomNav(stackStr.substringBefore("|").takeIf { it in ROOTS } ?: "explore", ui.saved.size, nav.tab)
            }
        },
    ) { inner ->
        Box(Modifier.fillMaxSize().padding(inner)) {
            if (data == null) {
                Column(Modifier.fillMaxSize().statusBarsPadding().padding(32.dp), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                    if (ui.loading) CircularProgressIndicator()
                    else PwEmpty("Could not load Pathways")
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
                        deeper -> (slideInHorizontally(tween(320, easing = ease)) { it / 6 } + fadeIn(tween(220))) togetherWith
                            (slideOutHorizontally(tween(260, easing = ease)) { -it / 12 } + fadeOut(tween(120)))
                        else -> (slideInHorizontally(tween(320, easing = ease)) { -it / 12 } + fadeIn(tween(220))) togetherWith
                            (slideOutHorizontally(tween(260, easing = ease)) { it / 6 } + fadeOut(tween(120)))
                    }
                },
                label = "pwStack",
            ) { s ->
                holder.SaveableStateProvider(s) { PwDispatch(s.substringAfterLast("|"), data, ui, viewModel, nav) }
            }
        }
    }
}

@Composable
private fun PwDispatch(top: String, d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val arg = top.substringAfter(":", "")
    val shown: Boolean = when (top.substringBefore(":")) {
        "route" -> d.routeById[arg]?.let { PwRouteDetail(d, it, ui, vm, nav); true } ?: false
        "career" -> d.careers[arg]?.let { PwCareerDetail(d, it, ui, vm, nav); true } ?: false
        "exam" -> d.govtById[arg]?.let { PwExamDetail(d, it, ui, vm, nav); true } ?: false
        "guide" -> d.guideById[arg]?.let { PwGuideDetail(d, it, vm, ui, nav); true } ?: false
        "colleges" -> { PwCollegesPage(d, arg, ui, vm, nav); true }
        "search" -> { PwSearch(d, vm, nav); true }
        "study" -> { PwStudy(d, ui, vm, nav); true }
        "exams" -> { PwExams(d, vm, nav); true }
        "guides" -> { PwGuides(d, vm, nav); true }
        "plan" -> { PwPlan(d, ui, vm, nav); true }
        else -> { PwExplore(d, vm, nav); true }
    }
    // a saved item can point at something the latest data dropped; step back instead of showing a blank page
    if (!shown) LaunchedEffect(top) { nav.pop() }
}

@Composable
private fun PwBottomNav(root: String, saved: Int, onTab: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth().background(c.surfaceContainerLow).navigationBarsPadding().padding(horizontal = 8.dp, vertical = 10.dp)) {
        NAV.forEach { item ->
            val on = root == item.key
            val w by animateDpAsState(if (on) 64.dp else 48.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "navW")
            Box(
                Modifier.weight(1f).height(48.dp).clip(RoundedCornerShape(24.dp)).clickable { onTab(item.key) },
                contentAlignment = Alignment.Center,
            ) {
                Box {
                    Box(
                        Modifier.width(w).height(40.dp).clip(RoundedCornerShape(20.dp)).background(if (on) c.primaryContainer else c.surfaceContainerLow),
                        contentAlignment = Alignment.Center,
                    ) { Icon(item.icon, item.label, Modifier.size(24.dp), tint = if (on) c.onPrimaryContainer else c.onSurfaceVariant) }
                    if (item.key == "plan" && saved > 0) PwCount(saved, Modifier.align(Alignment.TopEnd).offset(x = 2.dp, y = (-4).dp))
                }
            }
        }
    }
}

@Composable
internal fun PwSearch(d: PwData, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    var q by rememberSaveable { mutableStateOf("") }
    val focus = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
    val hits = remember(q, d) { pwSearch(d, q) }
    val s = vm.sel
    fun open(h: PwHit) {
        when (h.kind) {
            "Course" -> nav.push("route:${h.id}")
            "Career" -> nav.push("career:${h.id}")
            "Exam" -> nav.push("exam:${h.id}")
            "Guide" -> nav.push("guide:${h.id}")
            "College" -> d.routes.firstOrNull { h.id in it.where }?.let { nav.push("colleges:${it.id}") }
            "Scholarship" -> { s.study = "funding"; s.schCountry = ""; s.schOpen = h.id; nav.tab("study") }
            "Country" -> { s.study = "abroad"; s.abroadOpen = h.id; nav.tab("study") }
            "Question" -> { s.faqOpen = h.id; nav.tab("guides") }
        }
    }
    Column(Modifier.fillMaxSize().statusBarsPadding()) {
        Row(Modifier.fillMaxWidth().padding(16.dp, 12.dp, 16.dp, 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            PwIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", nav.pop)
            BasicTextField(
                q, { q = it },
                Modifier.weight(1f).height(44.dp).clip(RoundedCornerShape(22.dp)).background(c.surfaceContainerHigh).focusRequester(focus),
                singleLine = true,
                textStyle = MaterialTheme.typography.bodyLarge.copy(color = c.onSurface, fontWeight = FontWeight.Medium),
                cursorBrush = SolidColor(c.primary),
                decorationBox = { inner ->
                    Box(Modifier.padding(horizontal = 18.dp), contentAlignment = Alignment.CenterStart) {
                        if (q.isEmpty()) Text("Search", color = c.onSurfaceVariant, style = MaterialTheme.typography.bodyLarge)
                        inner()
                    }
                },
            )
        }
        LazyColumn(contentPadding = PaddingValues(16.dp, 0.dp, 16.dp, 24.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            if (q.isNotBlank() && hits.isEmpty()) item("none") { PwEmpty("No results") }
            items(hits, key = { it.kind + it.id }) { h -> PwRow(h.title, h.sub, h.kind, onClick = { open(h) }) }
        }
    }
}
