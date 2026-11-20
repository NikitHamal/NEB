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
    var schScope by rememberSaveable { mutableStateOf("All") }
    val withWhere = remember(d) { d.routes.filter { it.where.isNotEmpty() } }
    val activeColRouteId = remember(s.collegeRoute, s.course, withWhere) {
        listOf(s.collegeRoute, s.course.orEmpty()).firstOrNull { id -> id.isNotEmpty() && withWhere.any { it.id == id } } ?: withWhere.firstOrNull()?.id
    }
    val activeColRoute = activeColRouteId?.let { d.routeById[it] }
    val nearRoutes = remember(activeColRoute?.id, withWhere) {
        if (activeColRoute == null) emptyList()
        else (listOf(activeColRoute) + withWhere.filter { it.stage == activeColRoute.stage && it.group == activeColRoute.group && it.id != activeColRoute.id }).take(20)
    }
    val schCountry = d.abroad.firstOrNull { it.id == s.schCountry }
    val schScopes = remember(d) { d.scholarships.map { it.scope }.filter { it.isNotBlank() }.distinct() }
    val schChips = remember(schCountry, schScopes) {
        buildList {
            if (schCountry != null) add("x" to schCountry.country)
            add("All" to "All"); schScopes.forEach { add(it to levelLabel(it)) }
        }
    }
    val hasSubChips = (s.study == "colleges" && nearRoutes.isNotEmpty()) || (s.study == "funding" && schChips.size > 1)
    val scroll = rememberScrollState()
    androidx.compose.runtime.LaunchedEffect(s.study, activeColRouteId, schScope, s.schCountry) { scroll.scrollTo(0) }
    PwScrollPage(
        bottom = 24.dp,
        state = scroll,
        topBar = { scrolled -> PwRootBar({ nav.push("search") }, nav.pop, scrolled) },
        stickyHeader = {
            PwSeg(
                listOf("colleges" to "Colleges", "abroad" to "Abroad", "funding" to "Funding"),
                s.study,
                { s.study = it },
                Modifier.padding(16.dp, 4.dp, 16.dp, if (hasSubChips) 4.dp else 10.dp)
            )
            if (s.study == "colleges" && nearRoutes.isNotEmpty()) {
                PwChipRow(nearRoutes.map { it.id to it.name }, { it == activeColRoute?.id }, { s.collegeRoute = it }, Modifier.padding(top = 2.dp, bottom = 10.dp))
            } else if (s.study == "funding" && schChips.size > 1) {
                PwChipRow(schChips, { it == "x" || it == schScope }, { k -> if (k == "x") s.schCountry = "" else schScope = k }, Modifier.padding(top = 2.dp, bottom = 10.dp))
            }
        },
    ) {
        Spacer(Modifier.height(6.dp))
        when (s.study) {
            "abroad" -> PwAbroadBody(d, ui, vm, nav)
            "funding" -> PwFundingBody(d, ui, vm, schScope)
            else -> PwCollegesBody(d, "", ui, vm, showRouteChips = false)
        }
    }
}

@Composable
internal fun PwCollegesPage(d: PwData, routeId: String, ui: PathwaysUiState, vm: PathwaysViewModel, nav: PwNav) {
    PwScrollPage(24.dp, topBar = { scrolled -> PwBackBar(d.routeById[routeId]?.name ?: "Colleges", nav.pop, scrolled) }) {
        PwCollegesBody(d, routeId, ui, vm, showRouteChips = false)
    }
}

private fun levelLabel(l: String): String = when (l.lowercase()) {
    "phd" -> "PhD"
    "plus2", "+2" -> "+2"
    else -> l.replaceFirstChar { it.uppercase() }
}

@Composable
private fun PwFundingBody(d: PwData, ui: PathwaysUiState, vm: PathwaysViewModel, scope: String) {
    val s = vm.sel
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    var level by rememberSaveable { mutableStateOf("All") }
    var filterQ by rememberSaveable { mutableStateOf("") }
    var shown by rememberSaveable(scope, s.schCountry) { androidx.compose.runtime.mutableIntStateOf(24) }
    val country = d.abroad.firstOrNull { it.id == s.schCountry }
    val levels = remember(d) { d.scholarships.flatMap { it.levels }.distinct().take(3) }
    val needle = filterQ.trim().lowercase()
    val list = remember(d, country, scope, level, needle) {
        d.scholarships.filter { x ->
            (country == null || x.id in country.scholarships || x.country == country.id) &&
                (scope == "All" || x.scope == scope) && (level == "All" || level in x.levels) &&
                (needle.isEmpty() || "${x.name} ${x.by} ${x.covers} ${x.country}".lowercase().contains(needle))
        }.sortedWith(compareBy({ if (it.open.size == 2) monthsUntil(it.open[0], it.open[1]) else 99 }, { it.name }))
    }
    val openAt = list.indexOfFirst { it.id == s.schOpen }
    val limit = if (openAt >= shown) openAt + 4 else shown
    Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        androidx.compose.foundation.text.BasicTextField(
            value = filterQ,
            onValueChange = { filterQ = it; shown = 24 },
            singleLine = true,
            textStyle = MaterialTheme.typography.bodyMedium.copy(color = c.onSurface, fontWeight = FontWeight.Medium),
            cursorBrush = androidx.compose.ui.graphics.SolidColor(c.primary),
            modifier = Modifier
                .fillMaxWidth()
                .height(44.dp)
                .background(c.surfaceContainerLow, RoundedCornerShape(22.dp))
                .padding(horizontal = 16.dp),
            decorationBox = { inner ->
                Box(contentAlignment = Alignment.CenterStart) {
                    if (filterQ.isEmpty()) Text("Filter scholarships or provider", color = c.onSurfaceVariant, fontSize = 13.5.sp)
                    inner()
                }
            }
        )
        if (levels.size > 1) {
            PwSeg((listOf("All") + levels).map { it to levelLabel(it) }, level, { level = it; shown = 24 })
            Spacer(Modifier.height(6.dp))
        }
        if (list.isEmpty()) PwEmpty("No match")
        list.take(limit).forEachIndexed { i, x ->
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
        if (list.size > limit) {
            PwButton("Show ${minOf(24, list.size - limit)} more", null, false, { shown = limit + 24 }, Modifier.fillMaxWidth())
        }
    }
}

