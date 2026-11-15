@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
internal fun Note(text: String) {
    Text(text, Modifier.padding(horizontal = 20.dp), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
}

@Composable
internal fun Pills(items: List<String>) {
    FlowRow(Modifier.padding(horizontal = 20.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        items.forEachIndexed { i, s ->
            val t = pwTone(i)
            Text(
                s, Modifier.clip(RoundedCornerShape(18.dp)).background(t.bg).padding(horizontal = 14.dp, vertical = 9.dp),
                color = t.fg, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold,
            )
        }
    }
}

@Composable
internal fun Related(title: String, routes: List<PwRoute>, nav: PwNav) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        PwHeading(title)
        PwChipRow(routes, { false }, { r -> r.name.substringBefore(" (").let { if (it.length > 24) shortCode(r.name) else it } }, { nav.push("route:${it.id}") })
    }
}

@Composable
internal fun CareerRow(k: PwCareer, index: Int, open: Boolean, onToggle: () -> Unit) {
    val c = MaterialTheme.colorScheme
    PwSurface(Modifier.padding(horizontal = 16.dp).fillMaxWidth().animateContentSize(), color = c.surfaceContainer, radius = 22.dp, onClick = onToggle) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                PwTile("0${index + 1}", pwTone(index), 44.dp)
                Column(Modifier.weight(1f)) {
                    Text(k.name, fontWeight = FontWeight.Bold, maxLines = if (open) 3 else 1)
                    Text(k.about, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant, maxLines = if (open) 6 else 1)
                }
            }
            if (open) {
                Meter("Demand", k.demand / 5f, c.primary, "${k.demand} of 5")
                Meter("Competition", k.competition / 5f, pwTone(1).solid, "${k.competition} of 5")
                Meter("Abroad demand", k.abroad / 5f, pwTone(2).solid, "${k.abroad} of 5")
                Text("Starts at NPR ${money(k.entryMin)} to ${money(k.entryMax)} a month, senior roles NPR ${money(k.seniorMin)} to ${money(k.seniorMax)}. Trend: ${k.trend}.", style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant)
            }
        }
    }
}

@Composable
internal fun Meter(label: String, fraction: Float, color: androidx.compose.ui.graphics.Color, value: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(label, Modifier.width(104.dp), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        PwBar(fraction, color, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f), Modifier.weight(1f))
        Text(value, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
    }
}
