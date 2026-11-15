package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.OpenInNew
import androidx.compose.material.icons.outlined.WorkspacePremium
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.boundedWidth
import androidx.compose.foundation.layout.size

private val LEVELS = listOf("" to "All levels", "bachelor" to "Bachelor", "master" to "Master", "phd" to "PhD", "diploma" to "Diploma")

@Composable
internal fun PwAbroadTab(d: PwData, nav: PwNav) {
    var scope by rememberSaveable { mutableStateOf("") }
    val shown = remember(d, scope) { d.scholarships.filter { scope.isEmpty() || it.scope == scope } }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("title") { Text("Abroad and scholarships", Modifier.padding(start = 20.dp, top = 16.dp), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.ExtraBold) }
        item("hero") {
            val t = pwTone(1)
            Column(
                Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(30.dp)).background(t.bg)
                    .drawBehind { drawCircle(t.solid.copy(alpha = 0.10f), 90.dp.toPx(), Offset(size.width, 0f)) }.padding(22.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                PwMono("Beyond Nepal", color = t.fg)
                Text("Study abroad, step by step.", color = t.fg, fontWeight = FontWeight.ExtraBold, fontSize = 28.sp, lineHeight = 33.sp)
                Text("Costs, visas, tests and scholarships for ${d.abroad.size} countries.", color = t.fg.copy(alpha = 0.85f), style = MaterialTheme.typography.bodyMedium)
            }
        }
        item("destHead") { PwHeading("Popular destinations") }
        item("dest") {
            LazyRow(Modifier.boundedWidth(), contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                items(d.abroad.size, key = { d.abroad[it].id }) { i ->
                    val a = d.abroad[i]; val t = pwTone(i + 3)
                    PwSurface(Modifier.width(150.dp), color = t.bg, radius = 28.dp, onClick = { nav.push("country:${a.id}") }) {
                        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            PwTile(a.id.uppercase(), t, 44.dp, solid = true)
                            Text(a.country, color = t.fg, fontWeight = FontWeight.Bold, maxLines = 2, overflow = TextOverflow.Ellipsis, lineHeight = 19.sp)
                            Text("Costs, tests, intakes", color = t.fg.copy(alpha = 0.8f), style = MaterialTheme.typography.bodySmall)
                        }
                    }
                }
            }
        }
        item("schHead") { PwHeading("Scholarships", trailing = "${shown.size} listed") }
        item("scope") { PwChipRow(listOf("" to "All", "abroad" to "Abroad", "nepal" to "In Nepal"), { it.first == scope }, { it.second }, { scope = it.first }) }
        items(shown.take(4), key = { it.id }) { s -> ScholarshipRow(s, shown.indexOf(s)) }
        if (shown.size > 4) item("more") {
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = MaterialTheme.colorScheme.primaryContainer, radius = 24.dp, onClick = { nav.push("scholarships") }) {
                Text("See all ${shown.size} scholarships", Modifier.padding(18.dp), color = MaterialTheme.colorScheme.onPrimaryContainer, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
internal fun PwScholarships(d: PwData, nav: PwNav) {
    var scope by rememberSaveable { mutableStateOf("") }
    var level by rememberSaveable { mutableStateOf("") }
    val shown = remember(d, scope, level) { d.scholarships.filter { (scope.isEmpty() || it.scope == scope) && (level.isEmpty() || level in it.levels) } }
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") { PwTopBar("Scholarships", nav, caption = "${shown.size} listed") }
        item("scope") { PwChipRow(listOf("" to "All", "abroad" to "Abroad", "nepal" to "In Nepal"), { it.first == scope }, { it.second }, { scope = it.first }) }
        item("level") { PwChipRow(LEVELS, { it.first == level }, { it.second }, { level = it.first }) }
        if (shown.isEmpty()) item("none") { Note("No scholarship matches both filters.") }
        items(shown, key = { it.id }) { s -> ScholarshipRow(s, shown.indexOf(s)) }
    }
}

@Composable
internal fun ScholarshipRow(s: PwScholarship, index: Int) {
    val c = MaterialTheme.colorScheme
    val uri = LocalUriHandler.current
    var open by rememberSaveable(s.id) { mutableStateOf(false) }
    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth().animateContentSize(), color = c.surfaceContainer, radius = 22.dp, onClick = { open = !open }) {
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                PwIconTile(Icons.Outlined.WorkspacePremium, pwTone(index + 1), 46.dp)
                Column(Modifier.weight(1f)) {
                    Text(s.name, fontWeight = FontWeight.Bold, maxLines = if (open) 3 else 1, overflow = TextOverflow.Ellipsis)
                    Text(s.by + " \u00B7 " + s.levels.joinToString(", ") { it.replaceFirstChar { ch -> ch.uppercase() } }, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = if (open) 3 else 1, overflow = TextOverflow.Ellipsis)
                }
                Text(if (s.scope == "abroad") "Abroad" else "Nepal", Modifier.clip(RoundedCornerShape(12.dp)).background(pwTone(1).bg).padding(horizontal = 10.dp, vertical = 5.dp), color = pwTone(1).fg, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
            }
            if (open) {
                Text(s.covers, style = MaterialTheme.typography.bodyMedium)
                PwMono("Who can apply", color = c.onSurfaceVariant); Text(s.who, style = MaterialTheme.typography.bodySmall)
                PwMono("How to apply", color = c.onSurfaceVariant); Text(s.how, style = MaterialTheme.typography.bodySmall)
                if (s.link.isNotBlank()) PwSurface(color = c.primaryContainer, radius = 18.dp, onClick = { uri.openUri(s.link) }) {
                    Row(Modifier.padding(horizontal = 14.dp, vertical = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("Official page", color = c.onPrimaryContainer, fontWeight = FontWeight.SemiBold)
                        Icon(Icons.Outlined.OpenInNew, null, Modifier.size(16.dp), tint = c.onPrimaryContainer)
                    }
                }
            }
        }
    }
}
