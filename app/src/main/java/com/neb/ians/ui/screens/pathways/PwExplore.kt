package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.scaleIn
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.layout.onPlaced
import androidx.compose.ui.layout.LayoutCoordinates
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathMeasure
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.math.abs

@Composable
internal fun PwExplore(d: PwData, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    val stage = d.stages.firstOrNull { it.id == s.stage } ?: d.stages.firstOrNull()
    if (stage == null) { PwEmpty("Nothing here yet"); return }
    val inStage = remember(d, stage.id) { d.routes.filter { it.stage == stage.id } }
    val groups = remember(inStage) { inStage.map { it.group }.distinct() }
    val group = s.group.takeIf { it in groups } ?: groups.firstOrNull().orEmpty()
    val courses = remember(inStage, group) { inStage.filter { it.group == group } }
    val careers = remember(courses) { courses.flatMap { it.careers }.distinct().mapNotNull { d.careers[it] } }
    val hint = remember(s.trail, d) { s.trail.lastOrNull()?.let { d.routeById[it]?.next?.toSet() }.orEmpty() }
    val focus = s.focus.takeIf { f ->
        (f.startsWith("route:") && f.removePrefix("route:") == s.course) || (f.startsWith("career:") && f.removePrefix("career:") == s.career)
    } ?: s.course?.let { "route:$it" } ?: s.career?.let { "career:$it" }

    val scroll = rememberScrollState()
    LaunchedEffect(stage.id, group) { scroll.scrollTo(0) }
    Box(Modifier.fillMaxSize()) {
        PwScrollPage(
            bottom = 112.dp,
            state = scroll,
            topBar = { scrolled -> PwRootBar({ nav.push("search") }, nav.pop, scrolled) },
            stickyHeader = {
                PwTrail(d, vm, stage)
                PwStages(d.stages, stage.id) { id ->
                    s.stage = id; s.group = ""; s.course = null; s.career = null; s.focus = ""; s.trail = emptyList()
                }
                PwGroups(groups, group) { s.group = it; s.course = null; s.career = null; s.focus = "" }
            },
        ) {
            val linkedCount = when {
                s.course != null -> d.routeById[s.course]?.careers.orEmpty().count { id -> careers.any { it.id == id } }
                s.career != null -> courses.count { s.career in it.careers }
                else -> 0
            }
            PwLens(s.lens, s.course != null || s.career != null, linkedCount, s.linked, { s.linked = !s.linked }) { s.lens = if (s.lens == it) "" else it }
            PwRouteMap(
                d, courses, careers, s.course, s.career, hint, s.lens, s.linked, stage.id + group,
                onCourse = { id ->
                    if (s.course == id) s.course = null
                    else {
                        s.course = id
                        if (s.career != null && s.career !in d.routeById[id]?.careers.orEmpty()) s.career = null
                        s.focus = "route:$id"
                    }
                },
                onCareer = { id ->
                    if (s.career == id) s.career = null
                    else {
                        s.career = id
                        if (s.course != null && id !in d.routeById[s.course]?.careers.orEmpty()) s.course = null
                        s.focus = "career:$id"
                    }
                },
            )
        }
        AnimatedContent(
            targetState = focus, modifier = Modifier.align(Alignment.BottomCenter),
            transitionSpec = { (slideInVertically { it } + fadeIn()) togetherWith (slideOutVertically { it } + fadeOut()) },
            label = "peek",
        ) { f -> if (f != null) PwPeek(d, f) { nav.push(f) } else Spacer(Modifier.fillMaxWidth()) }
    }
}

@Composable
private fun PwTrail(d: PwData, vm: PathwaysViewModel, stage: PwStage) {
    val s = vm.sel
    if (s.trail.isEmpty() && s.course == null && s.career == null) return
    val c = MaterialTheme.colorScheme
    Row(
        Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(horizontal = 16.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        val items = buildList<Triple<String, Boolean, () -> Unit>> {
            s.trail.forEachIndexed { i, id -> d.routeById[id]?.let { r -> add(Triple(r.name, false) { restoreTrail(d, vm, i) }) } }
            add(Triple(stage.label, false) { s.course = null; s.career = null; s.focus = "" })
            s.course?.let { id -> d.routeById[id]?.let { add(Triple(it.name, true) { s.focus = "route:$id" }) } }
            s.career?.let { id -> d.careers[id]?.let { add(Triple(it.name, true) { s.focus = "career:$id" }) } }
        }
        items.forEachIndexed { i, (label, on, go) ->
            if (i > 0) Box(Modifier.width(10.dp).height(2.dp).background(c.outlineVariant))
            Surface(onClick = go, shape = RoundedCornerShape(15.dp), color = if (on) c.onSurface else c.surfaceContainerHigh, contentColor = if (on) c.surface else c.onSurfaceVariant) {
                Box(Modifier.height(30.dp).padding(horizontal = 12.dp), contentAlignment = Alignment.Center) {
                    Text(label, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
                }
            }
        }
    }
}

private fun restoreTrail(d: PwData, vm: PathwaysViewModel, i: Int) {
    val s = vm.sel
    val r = d.routeById[s.trail.getOrNull(i) ?: return] ?: return
    s.trail = s.trail.take(i)
    s.stage = r.stage; s.group = r.group; s.course = r.id; s.career = null; s.focus = "route:${r.id}"
}

@Composable
private fun PwStages(stages: List<PwStage>, current: String, onPick: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    val scroll = rememberScrollState()
    Row(
        Modifier.fillMaxWidth().nebHorizontalScroll(scroll).padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically,
    ) {
        stages.forEach { st ->
            val on = st.id == current
            val r by animateDpAsState(if (on) 14.dp else 19.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "stR")
            val bg by animateColorAsState(if (on) c.primary else c.surfaceContainerHigh, label = "stBg")
            val pop = remember { Animatable(1f) }
            LaunchedEffect(on) { if (on) { pop.snapTo(0.8f); pop.animateTo(1f, spring(0.5f, Spring.StiffnessMediumLow)) } }
            Surface(
                onClick = { onPick(st.id) }, modifier = Modifier.height(38.dp).widthIn(min = 44.dp).graphicsLayer { scaleX = pop.value; scaleY = pop.value },
                shape = RoundedCornerShape(r), color = bg, contentColor = if (on) c.onPrimary else c.onSurface,
            ) {
                Box(Modifier.padding(horizontal = if (on) 18.dp else 14.dp), contentAlignment = Alignment.Center) {
                    Text(if (on) st.label else shortStage(st.label), maxLines = 1, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}

@Composable
private fun PwGroups(groups: List<String>, current: String, onPick: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(3.dp)) {
        groups.forEachIndexed { i, g ->
            val on = g == current
            val tone = pwTone(groupToneIndex(g))
            val l by animateDpAsState(if (on || i == 0) 22.dp else 8.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "gL")
            val r by animateDpAsState(if (on || i == groups.lastIndex) 22.dp else 8.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "gR")
            val bg by animateColorAsState(if (on) tone.bg else c.surfaceContainerHigh, label = "gBg")
            Surface(
                onClick = { onPick(g) }, modifier = Modifier.height(44.dp),
                shape = RoundedCornerShape(topStart = l, bottomStart = l, topEnd = r, bottomEnd = r),
                color = bg, contentColor = if (on) tone.fg else c.onSurface,
            ) {
                Box(Modifier.padding(horizontal = 16.dp), contentAlignment = Alignment.Center) {
                    Text(groupLabel(g), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
                }
            }
        }
    }
}

@Composable
private fun PwLens(current: String, any: Boolean, linked: Int, linkedOn: Boolean, onLinked: () -> Unit, onPick: (String) -> Unit) {
    Row(Modifier.fillMaxWidth().padding(16.dp, 10.dp, 16.dp, 0.dp), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
        AnimatedVisibility(any, enter = fadeIn() + scaleIn(spring(0.6f, Spring.StiffnessMediumLow), initialScale = 0.85f), exit = fadeOut()) {
            PwChip("Linked $linked", linkedOn, onLinked, height = 32.dp)
        }
        Spacer(Modifier.weight(1f))
        listOf("demand" to "Demand", "pay" to "Pay", "odds" to "Odds").forEach { (k, label) -> PwChip(label, current == k, { onPick(k) }, height = 32.dp) }
    }
}

/** Two columns, courses and careers. Curves appear only for the current selection, measured relative to the map itself. */
@Composable
private fun PwRouteMap(
    d: PwData, courses: List<PwRoute>, careers: List<PwCareer>, course: String?, career: String?, hint: Set<String>, lens: String, linked: Boolean, key: String,
    onCourse: (String) -> Unit, onCareer: (String) -> Unit,
) {
    val c = MaterialTheme.colorScheme
    val nodes = remember(key) { HashMap<String, LayoutCoordinates>() }
    var mapCoords by remember { mutableStateOf<LayoutCoordinates?>(null) }
    var placed by remember { mutableIntStateOf(0) }
    val any = course != null || career != null
    val courseCareers = course?.let { d.routeById[it]?.careers }.orEmpty()
    fun cState(r: PwRoute): Int = when {
        course != null -> if (r.id == course) 2 else 0
        career != null -> if (career in r.careers) 1 else 0
        r.id in hint -> 1
        else -> 0
    }
    fun kState(k: String): Int = when {
        career != null -> if (k == career) 2 else 0
        course != null -> if (k in courseCareers) 1 else 0
        else -> 0
    }
    val draw = remember { Animatable(0f) }
    LaunchedEffect(course, career) { draw.snapTo(0f); draw.animateTo(1f, tween(600, easing = FastOutSlowInEasing)) }
    val maxPay = remember(courses, careers) {
        maxOf(courses.maxOfOrNull { d.m(it).payHi } ?: 1L, careers.maxOfOrNull { it.entryMax } ?: 1L).coerceAtLeast(1L).toFloat()
    }
    val hot = c.primary
    Row(
        Modifier.fillMaxWidth().padding(16.dp, 16.dp, 16.dp, 8.dp)
            .onGloballyPositioned { mapCoords = it }
            .drawBehind {
                placed
                val map = mapCoords ?: return@drawBehind
                if (!any || !map.isAttached) return@drawBehind
                val measure = PathMeasure()
                val seg = Path()
                val corner = 14.dp.toPx()
                courses.forEach { r ->
                    if (cState(r) == 0) return@forEach
                    val a = nodes["c:${r.id}"]?.takeIf { it.isAttached }?.let { map.localBoundingBoxOf(it, false) } ?: return@forEach
                    r.careers.forEach inner@{ k ->
                        if (kState(k) == 0) return@inner
                        val b = nodes["k:$k"]?.takeIf { it.isAttached }?.let { map.localBoundingBoxOf(it, false) } ?: return@inner
                        // one trunk in the gap: every link runs out to the same x, along it and in again, so many links read as one bracket
                        val mx = (a.right + b.left) / 2
                        val dy = b.center.y - a.center.y
                        val rr = minOf(corner, abs(dy) / 2f, (b.left - a.right) / 2f)
                        val sg = if (dy < 0f) -1f else 1f
                        val p = Path().apply {
                            moveTo(a.right, a.center.y)
                            if (abs(dy) < 1f) lineTo(b.left, b.center.y) else {
                                lineTo(mx - rr, a.center.y)
                                quadraticTo(mx, a.center.y, mx, a.center.y + sg * rr)
                                lineTo(mx, b.center.y - sg * rr)
                                quadraticTo(mx, b.center.y, mx + rr, b.center.y)
                                lineTo(b.left, b.center.y)
                            }
                        }
                        measure.setPath(p, false)
                        seg.reset()
                        measure.getSegment(0f, measure.length * draw.value, seg, true)
                        drawPath(seg, hot, style = Stroke(2.5.dp.toPx(), cap = StrokeCap.Round))
                    }
                }
            },
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(Modifier.weight(1f)) {
            courses.forEachIndexed { i, r ->
                val m = d.m(r)
                val st = cState(r)
                val gone = linked && any && st == 0
                val (fill, tail) = when (lens) {
                    "demand" -> m.demand / 100f to "${m.demand}"
                    "odds" -> (100 - m.competition) / 100f to "${100 - m.competition}"
                    "pay" -> m.payHi / maxPay to if (m.payHi > 0) money(m.payHi) else ""
                    else -> 0f to ""
                }
                AnimatedVisibility(!gone, enter = fadeIn() + expandVertically(), exit = fadeOut() + shrinkVertically()) {
                    PwNode(
                        shortName(r.name), tail, st, any && st == 0, fill, i, key, null, { onCourse(r.id) },
                        Modifier.padding(bottom = 8.dp).onPlaced { nodes["c:${r.id}"] = it; placed++ },
                    )
                }
            }
        }
        Spacer(Modifier.width(28.dp))
        Column(Modifier.weight(1f)) {
            careers.forEachIndexed { i, k ->
                val st = kState(k.id)
                val gone = linked && any && st == 0
                val (fill, tail) = when (lens) {
                    "demand" -> pct(k.demand) / 100f to "${pct(k.demand)}"
                    "odds" -> (100 - pct(k.competition)) / 100f to "${100 - pct(k.competition)}"
                    "pay" -> k.entryMax / maxPay to money(k.entryMax)
                    else -> 0f to ""
                }
                AnimatedVisibility(!gone, enter = fadeIn() + expandVertically(), exit = fadeOut() + shrinkVertically()) {
                    PwNode(
                        k.name, tail, st, any && st == 0, fill, i + 3, key, pct(k.demand), { onCareer(k.id) },
                        Modifier.padding(bottom = 8.dp).onPlaced { nodes["k:${k.id}"] = it; placed++ },
                    )
                }
            }
        }
    }
}

@Composable
private fun PwNode(
    label: String, trailing: String, state: Int, dim: Boolean, fill: Float, index: Int, key: String, signal: Int?,
    onClick: () -> Unit, modifier: Modifier,
) {
    val c = MaterialTheme.colorScheme
    val bg by animateColorAsState(when (state) { 2 -> c.primary; 1 -> c.primaryContainer; else -> c.surfaceContainerHigh }, label = "nBg")
    val fg by animateColorAsState(when (state) { 2 -> c.onPrimary; 1 -> c.onPrimaryContainer; else -> c.onSurface }, label = "nFg")
    val r by animateDpAsState(if (state == 2) 14.dp else 22.dp, spring(0.5f, Spring.StiffnessMediumLow), label = "nR")
    val dimA by animateFloatAsState(if (dim) 0.4f else 1f, label = "nA")
    val fillA by animateFloatAsState(fill, tween(500, easing = FastOutSlowInEasing), label = "nFill")
    val enter = remember(key) { Animatable(0f) }
    LaunchedEffect(key) { delay(index * 30L); enter.animateTo(1f, tween(320, easing = FastOutSlowInEasing)) }
    Surface(
        onClick = onClick,
        modifier = modifier.fillMaxWidth().heightIn(min = 52.dp).graphicsLayer {
            alpha = dimA * enter.value
            translationY = (1f - enter.value) * 10.dp.toPx()
        },
        shape = RoundedCornerShape(r), color = bg, contentColor = fg,
    ) {
        Box(Modifier.drawBehind { if (fillA > 0f) drawRect(fg.copy(alpha = 0.14f), size = Size(size.width * fillA, size.height)) }) {
            Row(
                Modifier.padding(horizontal = 14.dp, vertical = 8.dp).heightIn(min = 36.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                if (signal != null) PwSignal(signal, fg)
                Text(label, Modifier.weight(1f), fontSize = 13.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 17.sp, maxLines = 2, overflow = TextOverflow.Ellipsis)
                if (trailing.isNotEmpty()) Text(trailing, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = fg.copy(alpha = 0.75f), maxLines = 1)
            }
        }
    }
}

@Composable
private fun PwPeek(d: PwData, focus: String, onOpen: () -> Unit) {
    val id = focus.substringAfter(":")
    val route = if (focus.startsWith("route:")) d.routeById[id] else null
    val career = if (focus.startsWith("career:")) d.careers[id] else null
    val tone = pwTone(route?.let { groupToneIndex(it.group) } ?: 3)
    val title = route?.name ?: career?.name ?: return
    val sub = route?.let { r -> listOf(r.kind, yearsText(d.m(r).years)).filter { it.isNotBlank() }.joinToString(" · ") }
        ?: career?.let { "NPR ${money(it.entryMin)}–${money(it.seniorMax)} / month" }.orEmpty()
    val demand = route?.let { d.m(it).demand } ?: career?.let { pct(it.demand) } ?: 0
    PwSurface(Modifier.fillMaxWidth().padding(12.dp, 0.dp, 12.dp, 10.dp), color = tone.bg, radius = 28.dp, onClick = onOpen) {
        Row(Modifier.padding(start = 20.dp, top = 12.dp, end = 12.dp, bottom = 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Column(Modifier.weight(1f)) {
                Text(title, color = tone.fg, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.3).sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(sub, color = tone.fg.copy(alpha = 0.75f), fontSize = 12.sp, fontWeight = FontWeight.Medium, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
            PwRing(demand, null, 46.dp, tone.fg, tone.fg.copy(alpha = 0.14f), tone.fg)
            Box(Modifier.size(48.dp).clip(RoundedCornerShape(16.dp)).background(tone.fg), contentAlignment = Alignment.Center) {
                Icon(Icons.AutoMirrored.Outlined.ArrowForward, "Open", tint = tone.bg)
            }
        }
    }
}
