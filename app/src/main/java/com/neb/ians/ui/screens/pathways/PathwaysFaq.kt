@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.nebHorizontalScroll

/** Plain answers to "what after ..." questions. Same data as the web Questions tab (`faq` in /api/pathways/). */
@Composable
internal fun FaqList(modifier: Modifier, data: PwData, onOpenRoute: (String) -> Unit) {
    var topic by rememberSaveable { mutableStateOf("") }
    var openId by rememberSaveable { mutableStateOf<String?>(null) }
    val list = data.faq.filter { topic.isEmpty() || it.topic == topic }
    LazyColumn(modifier.fillMaxWidth(), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item("head") {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Questions", style = MaterialTheme.typography.headlineSmall)
                Row(
                    Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    FilterPill("All", topic.isEmpty()) { topic = "" }
                    data.topics.forEach { t -> FilterPill(t.label, topic == t.id) { topic = if (topic == t.id) "" else t.id } }
                }
            }
        }
        items(list, key = { it.id }) { f ->
            val open = openId == f.id
            val turn by animateFloatAsState(if (open) 180f else 0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow), label = "faqTurn")
            PwCard(Modifier.animateContentSize(spring(Spring.DampingRatioNoBouncy, Spring.StiffnessMediumLow)), onClick = { openId = if (open) null else f.id }) {
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text(f.q, Modifier.weight(1f), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Icon(Icons.Outlined.ExpandMore, contentDescription = null, modifier = Modifier.size(22.dp).rotate(turn), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                if (open) {
                    Text(f.a, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
                    val routes = f.go.mapNotNull { data.routeById[it] }
                    if (routes.isNotEmpty()) {
                        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(top = 2.dp)) {
                            routes.forEach { r -> FilterPill(r.name, false) { onOpenRoute(r.id) } }
                        }
                    }
                }
            }
        }
    }
}
