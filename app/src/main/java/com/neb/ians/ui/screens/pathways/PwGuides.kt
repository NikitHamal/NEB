@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

internal fun PwData.guideTone(cat: String): Int = listOf(0, 4, 2, 1, 3, 5)[guides.map { it.cat }.distinct().indexOf(cat).coerceAtLeast(0) % 6]

internal fun guideDone(vm: PathwaysViewModel, g: PwGuide): Int = g.steps.indices.count { vm.has("done", "${g.id}:$it") }

@Composable
internal fun PwGuides(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    var cat by rememberSaveable { mutableStateOf("All") }
    var view by rememberSaveable { mutableStateOf(if (vm.sel.faqOpen.isNotEmpty()) "faq" else "guides") }
    androidx.compose.runtime.LaunchedEffect(vm.sel.faqOpen) {
        if (vm.sel.faqOpen.isNotEmpty()) view = "faq"
    }
    val hasBoth = d.guides.isNotEmpty() && d.faq.isNotEmpty()
    val shown = if (!hasBoth) (if (d.guides.isNotEmpty()) "guides" else "faq") else view
    PwScrollPage(24.dp) {
        PwRootBar { nav.push("search") }
        if (hasBoth) PwSeg(listOf("guides" to "Guides", "faq" to "Questions"), shown, { view = it }, Modifier.padding(16.dp, 8.dp, 16.dp, 12.dp))
        if (shown == "guides" && d.guides.isNotEmpty()) {
            val cats = listOf("All") + d.guides.map { it.cat }.distinct()
            PwChipRow(cats.map { it to it }, { it == cat }, { cat = it }, Modifier.padding(top = if (hasBoth) 0.dp else 8.dp, bottom = 12.dp))
            Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                d.guides.filter { cat == "All" || it.cat == cat }.chunked(2).forEach { row ->
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        row.forEach { g -> GuideCard(d, g, vm, Modifier.weight(1f)) { nav.push("guide:${g.id}") } }
                        if (row.size == 1) Spacer(Modifier.weight(1f))
                    }
                }
            }
        }
        if (shown == "faq" && d.faq.isNotEmpty()) PwQuestions(d, ui, vm, nav)
        if (d.guides.isEmpty() && d.faq.isEmpty()) PwEmpty("Guides are on the way")
    }
}

@Composable
private fun GuideCard(d: PwData, g: PwGuide, vm: PathwaysViewModel, modifier: Modifier, onClick: () -> Unit) {
    val tone = pwTone(d.guideTone(g.cat))
    val done = guideDone(vm, g)
    PwSurface(modifier.heightIn(min = 136.dp).pwRise(0), color = tone.bg, radius = 28.dp, onClick = onClick) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(g.name, color = tone.fg, fontSize = 15.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 19.sp, modifier = Modifier.heightIn(min = 40.dp))
            PwBar(if (g.steps.isEmpty()) 0f else done / g.steps.size.toFloat(), height = 6.dp, color = tone.fg, track = tone.fg.copy(alpha = 0.14f))
            Row {
                Text("${g.steps.size} steps", Modifier.weight(1f), color = tone.fg, fontSize = 11.5.sp, fontWeight = FontWeight.SemiBold)
                Text("${g.steps.sumOf { it.days }} days", color = tone.fg, fontSize = 11.5.sp, fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

@Composable
internal fun PwGuideDetail(d: PwData, g: PwGuide, vm: PathwaysViewModel, ui: PathwaysUiState, nav: PwNav) {
    val tone = pwTone(d.guideTone(g.cat))
    val done = guideDone(vm, g)
    val key = "guide:${g.id}"
    Box(Modifier.fillMaxSize()) {
        PwScrollPage(if (g.link.isNotBlank()) 96.dp else 24.dp) {
            PwHero(tone, g.name, g.cat, key in ui.saved, { vm.toggleSaved(key) }, nav.pop) {
                PwBadge(tone, 6) {
                    Text("$done", fontSize = 22.sp, fontWeight = FontWeight.SemiBold, lineHeight = 24.sp)
                    Text("of ${g.steps.size}", fontSize = 11.sp, fontWeight = FontWeight.SemiBold, lineHeight = 12.sp)
                }
            }
            PwFacts(
                listOf(
                    "Time" to "${g.steps.sumOf { it.days }} days",
                    "Cost" to npr(g.steps.sumOf { it.cost }),
                    "Online" to "${g.steps.count { it.online }} of ${g.steps.size}",
                ),
                Modifier.padding(16.dp, 16.dp, 16.dp, 12.dp),
            )
            PwBar(if (g.steps.isEmpty()) 0f else done / g.steps.size.toFloat(), Modifier.fillMaxWidth().padding(horizontal = 16.dp), height = 12.dp)
            Column(Modifier.padding(16.dp, 12.dp, 16.dp, 0.dp)) {
                PwSteps(
                    g.steps.map { st ->
                        Triple(st.title, listOf(if (st.days > 0) "${st.days} days" else "", if (st.cost > 0) npr(st.cost) else "", if (st.online) "Online" else "In person").filter { it.isNotEmpty() }.joinToString(" · "), "")
                    },
                    { vm.has("done", "${g.id}:$it") },
                ) { vm.toggle("done", "${g.id}:$it") }
                if (g.docs.isNotEmpty()) {
                    PwH4("Documents")
                    androidx.compose.foundation.layout.FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        g.docs.forEach { doc -> PwChip(doc, vm.has("docs", "${g.id}:$doc"), { vm.toggle("docs", "${g.id}:$doc") }) }
                    }
                }
            }
        }
        if (g.link.isNotBlank()) PwActions(Modifier.align(Alignment.BottomCenter)) {
            PwButton(linkLabel(g.link), Icons.AutoMirrored.Outlined.ArrowForward, false, { nav.push(g.link) }, Modifier.weight(1f))
        }
    }
}
