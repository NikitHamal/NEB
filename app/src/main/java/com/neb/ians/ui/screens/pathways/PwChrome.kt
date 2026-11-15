package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Route
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Route
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Science
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.boundedWidth

private class PwTab(val root: String, val label: String, val off: ImageVector, val on: ImageVector)

private val TABS = listOf(
    PwTab("home", "Pathways", Icons.Outlined.Route, Icons.Filled.Route),
    PwTab("lab", "Course Lab", Icons.Outlined.Science, Icons.Filled.Science),
    PwTab("colleges", "Colleges", Icons.Outlined.School, Icons.Filled.School),
    PwTab("abroad", "Abroad", Icons.Outlined.Public, Icons.Filled.Public),
    PwTab("govt", "Lok Sewa", Icons.Outlined.AccountBalance, Icons.Filled.AccountBalance),
)

/** Icon only: the five sections are learnt once, and the screen below always says where you are. */
@Composable
internal fun PwBottomNav(rootKey: String, onTab: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    Column(Modifier.fillMaxWidth().background(c.surfaceContainerLow)) {
        Box(Modifier.fillMaxWidth().height(1.dp).background(c.outlineVariant.copy(alpha = 0.6f)))
        Row(Modifier.fillMaxWidth().navigationBarsPadding().height(68.dp).padding(horizontal = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            TABS.forEach { t ->
                val on = t.root == rootKey.substringBefore(":")
                val pill by animateFloatAsState(if (on) 1f else 0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow), label = "pill")
                Box(
                    Modifier.weight(1f).height(68.dp).semantics { contentDescription = t.label }
                        .clickable(role = Role.Tab, onClick = { onTab(t.root) }),
                    contentAlignment = Alignment.Center,
                ) {
                    Box(
                        Modifier.width(64.dp).height(36.dp).graphicsLayer { scaleX = 0.5f + 0.5f * pill; alpha = pill }
                            .clip(RoundedCornerShape(18.dp)).background(c.primaryContainer),
                    )
                    Icon(
                        if (on) t.on else t.off, null, Modifier.size(25.dp),
                        tint = if (on) c.onPrimaryContainer else c.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

/** Back, title (with a mono caption) and optional actions. */
@Composable
internal fun PwTopBar(title: String, nav: PwNav, caption: String = "", trailing: @Composable () -> Unit = {}) {
    Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        PwIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", nav.pop)
        Column(Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, maxLines = 1)
            if (caption.isNotEmpty()) PwMono(caption, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        trailing()
    }
}

@Composable
internal fun PwSaveButton(key: String, ui: PathwaysUiState, vm: PathwaysViewModel) {
    val on = key in ui.saved
    PwIconButton(if (on) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, if (on) "Remove from saved" else "Save", { vm.toggleSaved(key) },
        tint = if (on) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface)
}

@Composable
internal fun <T> PwChipRow(items: List<T>, selected: (T) -> Boolean, label: (T) -> String, onPick: (T) -> Unit, modifier: Modifier = Modifier, pad: Int = 20) {
    LazyRow(modifier.fillMaxWidth().boundedWidth(), contentPadding = PaddingValues(horizontal = pad.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        items(items.size, key = { it }) { i -> PwChip(label(items[i]), selected(items[i]), { onPick(items[i]) }) }
    }
}

@Composable
internal fun PwHeading(text: String, modifier: Modifier = Modifier, trailing: String = "") {
    Row(modifier.fillMaxWidth().padding(horizontal = 20.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(text, Modifier.weight(1f), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
        if (trailing.isNotEmpty()) PwMono(trailing, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

internal val PwHairline @Composable get() = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f))
