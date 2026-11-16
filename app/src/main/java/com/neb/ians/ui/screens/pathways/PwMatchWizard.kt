package com.neb.ians.ui.screens.pathways

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

private val QTITLE = listOf(
    "" to "", "Where are you now?" to "This sets which courses we compare.", "What do you enjoy?" to "Pick up to 3. Go with your gut.",
    "What are you good at?" to "Pick up to 3 subjects or skills.", "What matters most?" to "Pick up to 3. We weigh these hardest.",
    "What can you spend?" to "Total fees for the whole course.", "How do you take risks?" to "Some courses are hard to get into.",
)

/** The six questions as their own full screen, like the concept: bars on top, answers in the middle, one action at the bottom. */
@OptIn(ExperimentalAnimationApi::class)
@Composable
internal fun PwMatchWizard(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val step = vm.num("mstep").coerceIn(1, 7)
    var dir by remember { mutableIntStateOf(1) }
    var shakeKey by remember { mutableStateOf("") }
    var shakeN by remember { mutableIntStateOf(0) }
    val scope = rememberCoroutineScope()
    val px = LocalDensity.current.density * 32f
    fun go(n: Int, to: Int) { dir = to; vm.setNum("mstep", n) }
    fun leave() {
        if (vm.num("mdone") == 0 && vm.num("mstep") == 1) vm.setNum("mstep", 0)
        s.matchEdit = false; nav.pop()
    }
    fun finish() { vm.setNum("mdone", 1); vm.setNum("mstep", 0); s.matchOpen = null; s.matchWeak = false; s.matchEdit = false; nav.pop() }
    fun next() { if (s.matchEdit) finish() else go(step + 1, 1) }
    fun back() { if (step == 7) go(6, -1) else if (step > 1 && !s.matchEdit) go(step - 1, -1) else leave() }
    BackHandler { back() }
    fun pick(set: String, key: String) {
        if (!vm.has(set, key) && vm.set(set).size >= 3) { shakeKey = key; shakeN++; return }
        vm.toggle(set, key)
    }
    val stage = matchStageOf(d, s)
    val set = when (step) { 2 -> "interests"; 3 -> "strengths"; 4 -> "priorities"; else -> "" }
    val picked = if (set.isEmpty()) 0 else vm.set(set).size

    Column(Modifier.fillMaxSize().statusBarsPadding()) {
        if (step < 7) Row(Modifier.fillMaxWidth().padding(start = 12.dp, end = 12.dp, top = 14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            if (step > 1 && !s.matchEdit) PwIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", { back() }, container = c.surface)
            else PwIconButton(Icons.Outlined.Close, "Close", { back() }, container = c.surface)
            QuizProgress(step, Modifier.weight(1f))
            Box(Modifier.heightIn(min = 44.dp).widthIn(min = 56.dp).clip(RoundedCornerShape(22.dp)).clickable(enabled = set.isNotEmpty()) {
                vm.set(set).toList().forEach { vm.toggle(set, it) }; next()
            }.padding(horizontal = 12.dp), contentAlignment = Alignment.Center) {
                if (set.isNotEmpty()) Text("Skip", fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant)
            }
        }
        AnimatedContent(
            targetState = step, modifier = Modifier.weight(1f).fillMaxWidth(), label = "quiz",
            transitionSpec = {
                val to = if (targetState >= initialState) 1 else -1
                (slideInHorizontally(tween(450, easing = FastOutSlowInEasing)) { (px * to).roundToInt() } + fadeIn(tween(350))) togetherWith
                    (slideOutHorizontally(tween(300, easing = FastOutSlowInEasing)) { (-px * to).roundToInt() } + fadeOut(tween(200)))
            },
        ) { k ->
            if (k == 7) QLoading(d, stage) { finish() } else Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(start = 16.dp, end = 16.dp, top = 20.dp, bottom = 12.dp)) {
                Text(QTITLE[k].first, fontSize = 28.sp, lineHeight = 30.sp, fontWeight = FontWeight.Bold, letterSpacing = (-0.8).sp)
                Text(QTITLE[k].second, Modifier.padding(top = 8.dp, bottom = 20.dp), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
                QBody(k, d, ui, vm, stage, shakeKey, shakeN, ::pick) { to -> scope.launch { delay(280); if (!s.matchEdit && vm.num("mstep") == 1) go(to, 1) } }
            }
        }
        if (step < 7) Column(Modifier.navigationBarsPadding().padding(start = 16.dp, end = 16.dp, top = 10.dp, bottom = 18.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(if (set.isNotEmpty()) "$picked of 3 picked" else "", Modifier.fillMaxWidth().heightIn(min = 16.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant, textAlign = TextAlign.Center)
            QButton(if (s.matchEdit) "Update matches" else if (step == 6) "See my matches" else "Next", enabled = set.isEmpty() || picked > 0) {
                if (step == 6 && !s.matchEdit) go(7, 1) else next()
            }
        }
    }
}

@Composable
private fun QBody(k: Int, d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, stage: String, shakeKey: String, shakeN: Int, onPick: (String, String) -> Unit, advance: (Int) -> Unit) {
    when (k) {
        1 -> Column {
            QGrid(d.stages.map { Triple(it.id, it.label, it.blurb.takeIf { b -> b.isNotBlank() }) }, 1, { it == stage }, "", 0) { vm.setMatchStage(it); if (it != STREAM_STAGE) advance(2) }
            // the stream decides which degrees are open, so it is asked here and only at the After +2 stage
            AnimatedVisibility(stage == STREAM_STAGE, enter = fadeIn(tween(300)) + expandVertically(tween(350, easing = FastOutSlowInEasing)), exit = fadeOut(tween(150)) + shrinkVertically(tween(250))) {
                Column {
                    PwH4("Which stream did you study?", Modifier.padding(top = 18.dp))
                    QGrid(STREAMS.map { Triple(it.first, it.second, null) }, 2, { k -> STREAMS.getOrNull(vm.num("mstream") - 1)?.first == k }, "", 0) { k ->
                        val i = STREAMS.indexOfFirst { it.first == k } + 1
                        vm.setNum("mstream", if (vm.num("mstream") == i) 0 else i)
                    }
                }
            }
        }
        2 -> QGrid(INTERESTS.map { Triple(it.first, it.second, INTEREST_HINT[it.first]) }, 2, { vm.has("interests", it) }, shakeKey, shakeN) { onPick("interests", it) }
        3 -> QGrid(STRENGTHS.map { Triple(it.first, it.second, null) }, 2, { vm.has("strengths", it) }, shakeKey, shakeN) { onPick("strengths", it) }
        4 -> QGrid(PRIORITIES.filter { it.first != "near" || ui.district.isNotBlank() }.map { Triple(it.first, it.second, PRIORITY_HINT[it.first]) }, 2, { vm.has("priorities", it) }, shakeKey, shakeN) { onPick("priorities", it) }
        5 -> {
            val b = vm.num("budget")
            val pool = d.routes.filter { it.stage == stage }
            val fits = pool.count { it.feeMax <= b * 100_000L }
            PwBig("NPR ${b}L", "$fits of ${pool.size} courses fit fully")
            Spacer(Modifier.height(6.dp))
            PwSlider(b.toFloat(), { vm.setNum("budget", it.roundToInt()) }, 1f..60f, 0, "")
            PwH4("How long can you study?", Modifier.padding(top = 14.dp))
            QGrid(listOf(Triple("2", "Up to 2 yr", null), Triple("4", "Up to 4 yr", null), Triple("0", "Any length", null)), 3, { it.toInt() == vm.num("myears") }, "", 0) { vm.setNum("myears", it.toInt()) }
        }
        else -> QGrid(RISKS.map { Triple(it.first, it.second, it.third) }, 1, { it == (RISKS.getOrNull(vm.num("mrisk"))?.first ?: "mid") }, "", 0) { key -> vm.setNum("mrisk", RISKS.indexOfFirst { it.first == key }.coerceAtLeast(0)) }
    }
}

@Composable
private fun QLoading(d: PwData, stage: String, done: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val n = d.routes.count { it.stage == stage }
    val lines = listOf("Reading your answers", "Weighing $n courses", "Ranking your matches")
    var line by remember { mutableIntStateOf(0) }
    LaunchedEffect(Unit) { for (i in 1..2) { delay(550); line = i }; delay(450); done() }
    Column(Modifier.fillMaxSize(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(18.dp, Alignment.CenterVertically)) {
        PwBadge(PwTone(c.onPrimaryContainer, c.primaryContainer, c.primary, c.onPrimary), 8, 150.dp) {
            Text("$n", fontSize = 34.sp, fontWeight = FontWeight.Bold, color = c.onPrimaryContainer)
        }
        AnimatedContent(line, label = "qline", transitionSpec = { fadeIn(tween(400)) togetherWith fadeOut(tween(150)) }) { i ->
            Text(lines[i], fontSize = 16.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.Center)
        }
    }
}
