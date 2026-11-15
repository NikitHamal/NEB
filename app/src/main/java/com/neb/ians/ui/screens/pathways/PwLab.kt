package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val STREAM_CHIPS = listOf("science" to "Science", "management" to "Management", "humanities" to "Humanities")

/** Course Lab: match (six questions) and compare. arg "cmp:ROUTE" opens compare with that route chosen. */
@Composable
internal fun PwLab(d: PwData, nav: PwNav, arg: String) {
    var mode by rememberSaveable(arg) { mutableStateOf(if (arg.startsWith("cmp")) "compare" else "intro") }
    var stage by rememberSaveable { mutableStateOf("after12") }
    var stream by rememberSaveable { mutableStateOf("science") }
    var answers by rememberSaveable { mutableStateOf("") }
    val picked = answers.split(",").filter { it.isNotEmpty() }.map { it.toInt() }
    val c = MaterialTheme.colorScheme
    fun back() { if (mode == "quiz" && picked.isNotEmpty()) answers = picked.dropLast(1).joinToString(",") else mode = "intro" }
    when (mode) {
        "quiz" -> PwQuiz(picked, { back() }) { opt ->
            val next = picked + opt
            answers = next.joinToString(",")
            if (next.size == MATCH_QUESTIONS.size) mode = "result"
        }
        "result" -> {
            val hits = remember(d, stage, stream, answers) { matchRoutes(d, stage, stream, picked) }
            LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                item("bar") { PwTopBar("Your best fits", nav, caption = "${levelShort(stage)}${if (stage == "after12") " \u00B7 " + stream else ""}") }
                if (hits.isEmpty()) item("none") {
                    Column(Modifier.padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Text("No route fits every answer.", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("Try a larger budget or more years, and we will widen the list without adding unrelated courses.", color = c.onSurfaceVariant)
                        PwChip("Answer again", true, { answers = ""; mode = "quiz" })
                    }
                }
                items(hits, key = { it.route.id }) { h ->
                    val i = hits.indexOf(h)
                    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 24.dp, onClick = { nav.push("route:${h.route.id}") }) {
                        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                PwTile(shortCode(h.route.name), pwTone(i), 48.dp)
                                Column(Modifier.weight(1f)) {
                                    Text(h.route.name.substringBefore(" ("), fontWeight = FontWeight.Bold, maxLines = 2)
                                    Text("${h.route.years.substringBefore(" including")} \u00B7 ${feeText(h.route.feeMin, h.route.feeMax)}", style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = 1)
                                }
                                Column(horizontalAlignment = Alignment.End) { Text("${h.score}", fontWeight = FontWeight.ExtraBold, fontSize = 22.sp, color = c.primary); PwMono("fit", color = c.onSurfaceVariant) }
                            }
                            if (h.reasons.isNotEmpty()) Pills(h.reasons)
                        }
                    }
                }
                if (hits.isNotEmpty()) item("again") { Row(Modifier.padding(horizontal = 16.dp)) { PwChip("Answer again", false, { answers = ""; mode = "quiz" }) } }
            }
        }
        "compare" -> PwCompare(d, nav, arg.substringAfter("cmp:", "")) { if (arg.startsWith("cmp")) nav.tab("lab") else mode = "intro" }
        else -> LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            item("title") { Text("Course Lab", Modifier.padding(start = 20.dp, top = 16.dp), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.ExtraBold) }
            item("match") {
                val t = pwTone(1)
                PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = t.bg, radius = 32.dp) {
                    Column(Modifier.padding(22.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        PwMono("Match", color = t.fg)
                        Text("Six questions. Routes that fit you.", color = t.fg, fontWeight = FontWeight.ExtraBold, fontSize = 25.sp, lineHeight = 30.sp)
                        Text("Your level first, then what you enjoy, your budget and your time.", color = t.fg.copy(alpha = 0.85f), style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
            item("level") { PwHeading("I am at"); }
            item("levels") { PwChipRow(d.stages.map { it.id }, { it == stage }, { levelShort(it) }, { stage = it }) }
            if (stage == "after12") item("streams") { PwChipRow(STREAM_CHIPS, { it.first == stream }, { it.second }, { stream = it.first }) }
            item("go") {
                Row(Modifier.padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    PwSurface(Modifier.weight(1f), color = c.primary, radius = 28.dp, onClick = { answers = ""; mode = "quiz" }) {
                        Text("Start match", Modifier.fillMaxWidth().padding(vertical = 18.dp), color = c.onPrimary, fontWeight = FontWeight.Bold, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                    }
                    PwSurface(Modifier.weight(1f), color = c.surfaceContainerHigh, radius = 28.dp, onClick = { mode = "compare" }) {
                        Text("Compare", Modifier.fillMaxWidth().padding(vertical = 18.dp), fontWeight = FontWeight.Bold, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                    }
                }
            }
        }
    }
}

@Composable
private fun PwQuiz(picked: List<Int>, onBack: () -> Unit, onPick: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    val step = picked.size.coerceAtMost(MATCH_QUESTIONS.size - 1)
    val q = MATCH_QUESTIONS[step]
    LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 24.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item("bar") { PwTopBar("Question ${step + 1} of ${MATCH_QUESTIONS.size}", PwNav({}, onBack, {})) }
        item("prog") { PwBar((step + 1f) / MATCH_QUESTIONS.size, c.primary, c.surfaceContainerHigh, Modifier.padding(horizontal = 20.dp).fillMaxWidth(), 8.dp) }
        item("q") { Text(q.title, Modifier.padding(horizontal = 20.dp, vertical = 8.dp), fontWeight = FontWeight.ExtraBold, fontSize = 26.sp, lineHeight = 32.sp) }
        items(q.options.size, key = { "$step-$it" }) { i ->
            PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth(), color = c.surfaceContainer, radius = 24.dp, onClick = { onPick(i) }) {
                Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    PwTile("${'A' + i}", pwTone(i), 40.dp)
                    Text(q.options[i].label, Modifier.weight(1f), fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}
