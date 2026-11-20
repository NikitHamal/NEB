@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.KeyboardArrowRight
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Flag
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Route
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Work
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private fun topicIcon(id: String): ImageVector = when (id) {
    "after8" -> Icons.Outlined.School
    "after10" -> Icons.Outlined.Route
    "after12" -> Icons.Outlined.Flag
    "afterbach" -> Icons.Outlined.Work
    "abroad" -> Icons.Outlined.Public
    "general" -> Icons.Outlined.Lightbulb
    else -> Icons.Outlined.Info
}

/** Search box, topic chips and the question cards. Answers carry live links; figures come from the courses a question points to. */
@Composable
internal fun PwQuestions(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav, topic: String = "All") {
    val c = MaterialTheme.colorScheme
    val s = vm.sel
    val topics = remember(d) { d.topics.filter { t -> d.faq.any { it.topic == t.id } } }
    var q by rememberSaveable { mutableStateOf("") }
    var all by rememberSaveable(topic) { mutableStateOf(false) }
    val list = remember(d, topic, q) {
        val n = q.trim().lowercase()
        d.faq.filter { (topic == "All" || it.topic == topic) && (n.isEmpty() || (it.q + " " + it.a).lowercase().contains(n)) }
    }
    val openAt = list.indexOfFirst { it.id == s.faqOpen }
    val shown = if (all || openAt >= LIMIT) list else list.take(LIMIT)
    Box(Modifier.padding(start = 16.dp, top = 6.dp, end = 16.dp, bottom = 10.dp).fillMaxWidth().height(48.dp).clip(RoundedCornerShape(24.dp)).background(c.surfaceContainerHigh), contentAlignment = Alignment.CenterStart) {
        BasicTextField(
            q, { q = it; all = false }, Modifier.fillMaxWidth().padding(start = 20.dp, end = 52.dp), singleLine = true,
            textStyle = TextStyle(color = c.onSurface, fontSize = 14.sp, fontWeight = FontWeight.Medium), cursorBrush = SolidColor(c.primary),
            decorationBox = { inner -> Box { if (q.isEmpty()) Text("Search questions", color = c.onSurfaceVariant, fontSize = 14.sp, fontWeight = FontWeight.Medium); inner() } },
        )
        Icon(Icons.Outlined.Search, null, Modifier.align(Alignment.CenterEnd).padding(end = 16.dp).size(20.dp), tint = c.onSurfaceVariant)
    }
    Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        if (list.isEmpty()) PwEmpty("No questions found")
        shown.forEachIndexed { i, f ->
            val label = topics.firstOrNull { it.id == f.topic }?.label ?: f.topic
            QuestionCard(d, f, label, s.faqOpen == f.id, "faq:${f.id}" in ui.saved, i, vm, nav) { s.faqOpen = if (s.faqOpen == f.id) "" else f.id }
        }
        if (shown.size < list.size) PwButton("Show ${list.size - shown.size} more", null, false, { all = true }, Modifier.fillMaxWidth())
    }
}

private const val LIMIT = 20

@Composable
private fun QuestionCard(d: PwData, f: PwFaq, topicLabel: String, open: Boolean, saved: Boolean, index: Int, vm: PathwaysViewModel, nav: PwNav, onToggle: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val bounce = spring<androidx.compose.ui.unit.Dp>(0.6f, Spring.StiffnessMediumLow)
    val card by animateDpAsState(if (open) 34.dp else 28.dp, bounce, label = "fqR")
    val tile by animateDpAsState(if (open) 22.dp else 16.dp, bounce, label = "fqT")
    val bg by animateColorAsState(if (open) c.primaryContainer else c.surfaceContainerLow, tween(250), label = "fqBg")
    val tileBg by animateColorAsState(if (open) c.primary else c.surfaceContainerHighest, tween(250), label = "fqTb")
    val turn by animateFloatAsState(if (open) 90f else 0f, tween(300, easing = FastOutSlowInEasing), label = "fqChv")
    val ink = if (open) c.onPrimaryContainer else c.onSurface
    val mins = remember(f.a) { maxOf(1, Math.round(f.a.split(' ').size / 40f)) }
    Surface(Modifier.fillMaxWidth().pwRise(index, f.id), shape = RoundedCornerShape(card), color = bg) {
        Column {
            Row(
                Modifier.fillMaxWidth().clickable(onClickLabel = if (open) "Close" else "Open", onClick = onToggle)
                    .semantics { stateDescription = if (open) "Open" else "Closed" }.padding(14.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                Box(Modifier.size(44.dp).clip(RoundedCornerShape(tile)).background(tileBg), contentAlignment = Alignment.Center) {
                    Icon(topicIcon(f.topic), null, Modifier.size(22.dp), tint = if (open) c.onPrimary else c.onSurface)
                }
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                    Text(f.q, color = ink, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, lineHeight = 19.sp, maxLines = if (open) 6 else 3, overflow = TextOverflow.Ellipsis)
                    Text("$topicLabel \u00b7 $mins min read", color = ink.copy(alpha = 0.7f), fontSize = 12.sp, fontWeight = FontWeight.Medium)
                }
                Icon(Icons.AutoMirrored.Outlined.KeyboardArrowRight, null, Modifier.size(20.dp).graphicsLayer { rotationZ = turn }, tint = ink)
            }
            AnimatedVisibility(open, enter = expandVertically(tween(400, easing = FastOutSlowInEasing)) + fadeIn(tween(300)), exit = shrinkVertically(tween(300, easing = FastOutSlowInEasing)) + fadeOut(tween(150))) {
                QuestionBody(d, f, saved, vm, nav)
            }
        }
    }
}

@Composable
private fun QuestionBody(d: PwData, f: PwFaq, saved: Boolean, vm: PathwaysViewModel, nav: PwNav) {
    val c = MaterialTheme.colorScheme
    val ink = c.onPrimaryContainer
    val routes = remember(d, f.id) { f.go.mapNotNull { d.routeById[it] } }
    val facts = remember(d, f.id) {
        val r = routes.firstOrNull() ?: return@remember emptyList<Pair<String, String>>()
        val m = d.m(r)
        buildList {
            if (m.years > 0f) add(yearsText(m.years) to "Duration")
            if (r.feeMax > 0) add(money(r.feeMin.takeIf { it > 0 } ?: r.feeMax) to if (r.feeMin > 0) "Fee from" else "Fee up to")
            if (m.payHi > 0) add(money((m.payLo + m.payHi) / 2) to "Start pay")
            if (size < 3 && m.demand > 0) add("${m.demand}" to "Demand")
        }.take(3)
    }
    val helpful = vm.has("helpful", f.id)
    Column(Modifier.padding(18.dp, 2.dp, 18.dp, 16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        PwLinkText(f.a, fontSize = 14.sp, lineHeight = 22.sp, color = ink, weight = FontWeight.Medium)
        if (facts.isNotEmpty()) Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            facts.forEach { (v, l) ->
                Column(Modifier.weight(1f).clip(RoundedCornerShape(16.dp)).background(ink.copy(alpha = 0.08f)).padding(10.dp, 8.dp)) {
                    Text(v, color = ink, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text(l, color = ink.copy(alpha = 0.75f), fontSize = 11.sp, fontWeight = FontWeight.Medium, maxLines = 1)
                }
            }
            repeat(3 - facts.size) { Spacer(Modifier.weight(1f)) }
        }
        if (routes.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            routes.take(4).forEach { r ->
                Box(Modifier.height(36.dp).clip(RoundedCornerShape(18.dp)).background(ink.copy(alpha = 0.1f)).clickable(role = Role.Button) { nav.push("route:${r.id}") }.padding(horizontal = 14.dp), contentAlignment = Alignment.Center) {
                    Text(r.name, color = ink, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
                }
            }
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            val on by animateColorAsState(if (helpful) c.primary else ink.copy(alpha = 0.1f), tween(200), label = "helpBg")
            Row(
                Modifier.height(40.dp).clip(RoundedCornerShape(20.dp)).background(on).clickable(role = Role.Button) { vm.toggle("helpful", f.id) }.padding(horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Icon(Icons.Outlined.Check, null, Modifier.size(18.dp), tint = if (helpful) c.onPrimary else ink)
                Text("Helpful", color = if (helpful) c.onPrimary else ink, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
            }
            Spacer(Modifier.weight(1f))
            Box(Modifier.size(44.dp).clip(RoundedCornerShape(22.dp)).clickable(role = Role.Button, onClickLabel = "Save") { vm.toggleSaved("faq:${f.id}") }, contentAlignment = Alignment.Center) {
                Icon(if (saved) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, "Save", tint = if (saved) c.primary else ink)
            }
        }
    }
}
