package com.neb.ians.ui.screens.lab

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.nebHorizontalScroll

internal fun defaultLook(c: androidx.compose.material3.ColorScheme) = Look(
    "default", "Default", c.surfaceContainerLowest, c.onSurface, c.primary, c.secondaryContainer,
    FontFamily.Default, Pattern.None, false, true, 24,
)

private val TABS = listOf("Card", "Reading", "Mixed feed")

@Composable
fun DynamicPostsLabScreen(onNavigateBack: () -> Unit) {
    var index by rememberSaveable { mutableIntStateOf(0) }
    var tab by rememberSaveable { mutableIntStateOf(0) }
    var sample by rememberSaveable { mutableIntStateOf(0) }
    var useDefault by rememberSaveable { mutableStateOf(false) }
    var open by rememberSaveable { mutableStateOf(false) }
    var custom by remember { mutableStateOf<Look?>(null) }
    val c = MaterialTheme.colorScheme
    val base = if (useDefault) defaultLook(c) else LOOKS[index]
    val look = animateLook(custom ?: base)
    fun edit(f: (Look) -> Look) { custom = f(custom ?: base) }
    Scaffold(
        topBar = { WebTopBar(title = "Dynamic posts", showBack = true, onBackClick = onNavigateBack) },
        containerColor = c.surface,
    ) { inner ->
        Column(Modifier.fillMaxSize().padding(inner).verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            if (tab != 2) {
                Scroller {
                    LOOKS.forEachIndexed { i, l -> Pill(l.name, !useDefault && index == i, dot = l.accent) { index = i; useDefault = false; custom = null } }
                    Pill("Default", useDefault) { useDefault = true; custom = null }
                }
            }
            Scroller { TABS.forEachIndexed { i, t -> Pill(t, tab == i) { tab = i } } }
            if (tab != 2) Scroller { SAMPLES.forEachIndexed { i, s -> Pill(s.label, sample == i) { sample = i } } }
            when (tab) {
                0 -> FeedCard(look, SAMPLES[sample])
                1 -> ReadingView(look, SAMPLES[sample])
                else -> FEED_MIX.forEach { (si, id) -> FeedCard(LOOKS.firstOrNull { it.id == id } ?: defaultLook(c), SAMPLES[si]) }
            }
            if (tab != 2) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Pill("Customise", open, icon = true) { open = !open }
                    if (custom != null) Pill("Reset", false) { custom = null }
                }
                if (open) Customiser(look) { f -> edit(f) }
            }
        }
    }
}

@Composable
private fun Customiser(look: Look, edit: ((Look) -> Look) -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Control("Cover") { Pattern.entries.forEach { p -> Pill(p.label, look.pattern == p) { edit { it.copy(pattern = p) } } } }
        Control("Type") {
            listOf("Serif" to FontFamily.Serif, "Sans" to FontFamily.SansSerif, "Mono" to FontFamily.Monospace).forEach { (n, f) ->
                Pill(n, look.font == f) { edit { it.copy(font = f) } }
            }
        }
        Control("Corners") { listOf(12, 20, 28, 36).forEach { r -> Pill("$r", look.corner == r) { edit { it.copy(corner = r) } } } }
        Control("Layout") {
            Pill("Tall cover", look.tall) { edit { it.copy(tall = !it.tall) } }
            Pill("Centred title", look.center) { edit { it.copy(center = !it.center) } }
        }
        Control("Divider") { Divider.entries.forEach { d -> Pill(d.label, look.divider == d) { edit { it.copy(divider = d) } } } }
        Control("Extras") {
            Pill("Drop cap", look.dropCap) { edit { it.copy(dropCap = !it.dropCap) } }
            Pill("Quote bar", look.quoteBar) { edit { it.copy(quoteBar = !it.quoteBar) } }
            Pill("Highlight", look.mark) { edit { it.copy(mark = !it.mark) } }
        }
        Control("Accent") {
            SWATCHES.forEach { sw ->
                val on = look.accent == sw
                val shape = RoundedCornerShape(11.dp)
                Box(
                    Modifier.size(32.dp).clip(shape).background(sw)
                        .border(if (on) 3.dp else 0.dp, MaterialTheme.colorScheme.onSurface, shape)
                        .clickable { edit { it.copy(accent = sw, soft = lerp(it.bg, sw, 0.16f)) } },
                )
            }
        }
    }
}

@Composable
private fun Scroller(content: @Composable () -> Unit) {
    Row(Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) { content() }
}

@Composable
private fun Control(label: String, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Text(label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
        Scroller(content)
    }
}

@Composable
private fun Pill(label: String, on: Boolean, dot: Color? = null, icon: Boolean = false, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = onClick, shape = RoundedCornerShape(18.dp),
        color = if (on) c.secondaryContainer else Color.Transparent,
        contentColor = if (on) c.onSecondaryContainer else c.onSurfaceVariant,
        border = if (on) null else BorderStroke(1.dp, c.outlineVariant),
    ) {
        Row(Modifier.padding(horizontal = 14.dp, vertical = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (dot != null) Box(Modifier.size(10.dp).clip(RoundedCornerShape(5.dp)).background(dot))
            if (icon) Icon(Icons.Outlined.Tune, null, Modifier.size(16.dp))
            Text(label, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
        }
    }
}
