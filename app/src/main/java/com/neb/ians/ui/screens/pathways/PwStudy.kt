@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.OpenInNew
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
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
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
internal fun PwStudy(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    val s = vm.sel
    PwScrollPage(24.dp) {
        PwRootBar { nav.push("search") }
        PwSeg(listOf("colleges" to "Colleges", "abroad" to "Abroad", "funding" to "Funding"), s.study, { s.study = it }, Modifier.padding(16.dp, 8.dp, 16.dp, 14.dp))
        when (s.study) {
            "abroad" -> PwAbroadBody(d, ui, vm, nav)
            "funding" -> PwFundingBody(d, ui, vm)
            else -> PwCollegesBody(d, "", ui, vm)
        }
    }
}

@Composable
internal fun PwCollegesPage(d: PwData, routeId: String, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    PwScrollPage(24.dp) {
        PwBackBar(d.routeById[routeId]?.name ?: "Colleges", nav.pop)
        PwCollegesBody(d, routeId, ui, vm)
    }
}

private fun levelLabel(l: String): String = when (l.lowercase()) {
    "phd" -> "PhD"
    "plus2", "+2" -> "+2"
    else -> l.replaceFirstChar { it.uppercase() }
}

@Composable
private fun PwFundingBody(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    var scope by rememberSaveable { mutableStateOf("All") }
    var level by rememberSaveable { mutableStateOf("All") }
    val country = d.abroad.firstOrNull { it.id == s.schCountry }
    val scopes = remember(d) { d.scholarships.map { it.scope }.filter { it.isNotBlank() }.distinct() }
    val levels = remember(d) { d.scholarships.flatMap { it.levels }.distinct().take(3) }
    val list = remember(d, country, scope, level) {
        d.scholarships.filter { x ->
            (country == null || x.id in country.scholarships || x.country == country.id) &&
                (scope == "All" || x.scope == scope) && (level == "All" || level in x.levels)
        }.sortedWith(compareBy({ if (it.open.size == 2) monthsUntil(it.open[0], it.open[1]) else 99 }, { it.name }))
    }
    val chips = buildList {
        if (country != null) add("x" to country.country)
        add("All" to "All"); scopes.forEach { add(it to levelLabel(it)) }
    }
    PwChipRow(chips, { it == "x" || it == scope }, { k -> if (k == "x") s.schCountry = "" else scope = k }, Modifier.padding(bottom = 10.dp))
    Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        if (levels.size > 1) {
            PwSeg((listOf("All") + levels).map { it to levelLabel(it) }, level, { level = it })
            Spacer(Modifier.height(6.dp))
        }
        if (list.isEmpty()) PwEmpty("No match")
        list.forEachIndexed { i, x ->
            val open = s.schOpen == x.id
            val live = x.open.size == 2 && inWindow(x.open[0], x.open[1], nowMonth())
            PwSurface(Modifier.fillMaxWidth().pwRise(i).animateContentSize(), radius = 22.dp, onClick = { s.schOpen = if (open) "" else x.id }) {
                Column(Modifier.padding(16.dp, 14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Column(Modifier.weight(1f)) {
                            Text(x.name, fontSize = 14.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 18.sp)
                            Text(x.by, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                        val code = d.abroad.firstOrNull { it.id == x.country }?.code.orEmpty()
                        if (code.isNotBlank()) Box(Modifier.height(24.dp).clip(RoundedCornerShape(8.dp)).background(c.surfaceContainerHighest).padding(horizontal = 8.dp), contentAlignment = Alignment.Center) {
                            Text(code, fontSize = 10.5.sp, fontWeight = FontWeight.SemiBold)
                        }
                        Text(
                            if (x.open.size == 2) windowLabel(x.open[0], x.open[1]) else x.levels.joinToString(", ") { levelLabel(it) },
                            fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = if (live) c.primary else c.onSurfaceVariant, maxLines = 1,
                        )
                    }
                    if (x.open.size == 2) {
                        if (live) PwMonths({ inWindow(x.open[0], x.open[1], it) })
                        else PwMonths({ inWindow(x.open[0], x.open[1], it) }, fill = c.onPrimaryContainer, onFill = c.onPrimaryContainer, cellBg = c.primaryContainer)
                    }
                    if (open) {
                        val cv = x.covers.lowercase()
                        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            val t = "tuition" in cv; val st = "stipend" in cv || "allowance" in cv; val fl = "flight" in cv || "airfare" in cv || "travel" in cv
                            PwOutlineChip("Tuition", on = t, off = !t); PwOutlineChip("Stipend", on = st, off = !st); PwOutlineChip("Flights", on = fl, off = !fl)
                        }
                        listOf("Covers" to x.covers, "Who" to x.who, "How" to x.how).filter { it.second.isNotBlank() }.forEach { (k, v) ->
                            Column {
                                Text(k, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant)
                                PwLinkText(v, fontSize = 14.sp, lineHeight = 20.sp)
                            }
                        }
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            if (x.awards > 0) Text("${x.awards} awards", Modifier.weight(1f), fontSize = 13.sp, fontWeight = FontWeight.SemiBold) else Spacer(Modifier.weight(1f))
                            val key = "sch:${x.id}"
                            val saved = key in ui.saved
                            PwIconButton(if (saved) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, "Save", { vm.toggleSaved(key) },
                                if (saved) c.onSurface else c.surfaceContainerHigh, if (saved) c.surface else c.onSurface)
                            if (x.link.isNotBlank()) PwButton("Website", Icons.AutoMirrored.Outlined.OpenInNew, false, { runCatching { uri.openUri(x.link) } })
                        }
                    }
                }
            }
        }
    }
}

