package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.CenterFocusStrong
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.OpenInFull
import androidx.compose.material.icons.outlined.Remove
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.launch

/** Real map of Nepal for the Colleges tab: tap a district, zoom with the buttons, open the full view for pinch and drag. */
@Composable
internal fun PwNepalMapCard(counts: Map<String, Int>, selected: String, onPick: (String) -> Unit, modifier: Modifier = Modifier) {
    val ctx = LocalContext.current
    val c = MaterialTheme.colorScheme
    var geo by remember { mutableStateOf(NepalGeoLoader.peek()) }
    LaunchedEffect(Unit) { if (geo == null) geo = runCatching { NepalGeoLoader.get(ctx) }.getOrNull() }
    var open by rememberSaveable { mutableStateOf(false) }
    val g = geo
    Box(modifier.fillMaxWidth().aspectRatio(4000f / 2299f).clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow)) {
        if (g != null) MapPane(g, counts, selected, false, onPick, { open = true }, Modifier.fillMaxSize())
    }
    if (open && g != null) PwNepalMapFull(g, counts, selected, onPick) { open = false }
}

@Composable
private fun MapPane(geo: NepalGeo, counts: Map<String, Int>, selected: String, full: Boolean, onPick: (String) -> Unit, onExpand: (() -> Unit)?, modifier: Modifier) {
    val cam = remember(geo) { MapCam(geo) }
    val scope = rememberCoroutineScope()
    LaunchedEffect(selected, geo) { cam.fit(geo.byName[selected]) }
    Box(modifier) {
        PwNepalCanvas(cam, counts, selected, full, onPick, Modifier.fillMaxSize())
        geo.byName[selected]?.let { InfoCard(it, counts[it.name] ?: 0, Modifier.align(Alignment.TopStart).padding(12.dp)) }
        Column(Modifier.align(Alignment.TopEnd).padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            PwIconButton(Icons.Outlined.Add, "Zoom in", { scope.launch { cam.zoomCentre(1.8f) } })
            PwIconButton(Icons.Outlined.Remove, "Zoom out", { scope.launch { cam.zoomCentre(1f / 1.8f) } })
            if (full) PwIconButton(Icons.Outlined.CenterFocusStrong, "Reset view", { scope.launch { cam.fit(null) } })
            if (onExpand != null) PwIconButton(Icons.Outlined.OpenInFull, "Open full map", onExpand)
        }
    }
}

@Composable
private fun InfoCard(d: GeoDistrict, n: Int, modifier: Modifier) {
    val c = MaterialTheme.colorScheme
    Surface(modifier, shape = RoundedCornerShape(18.dp), color = c.surface.copy(alpha = 0.92f)) {
        Column(Modifier.padding(14.dp, 9.dp)) {
            Text(d.name, fontSize = 15.sp, fontWeight = FontWeight.Bold, lineHeight = 18.sp)
            Text(listOf(PROVINCES[d.province], d.hq).filter { it.isNotBlank() }.joinToString(" · "), fontSize = 12.sp, color = c.onSurfaceVariant, lineHeight = 15.sp)
            Text(if (n == 1) "1 college" else "$n colleges", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = c.primary, lineHeight = 16.sp)
        }
    }
}

@Composable
private fun PwNepalMapFull(geo: NepalGeo, counts: Map<String, Int>, selected: String, onPick: (String) -> Unit, onClose: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val fills = mapFills()
    Dialog(onDismissRequest = onClose, properties = DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false)) {
        Surface(Modifier.fillMaxSize(), color = c.surface) {
            Column(Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding().padding(16.dp, 12.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("Nepal", fontSize = 22.sp, fontWeight = FontWeight.ExtraBold, lineHeight = 26.sp)
                        Text("${counts.values.sum()} colleges in ${counts.size} districts", fontSize = 13.sp, color = c.onSurfaceVariant)
                    }
                    PwIconButton(Icons.Outlined.Close, "Close map", onClose)
                }
                Spacer(Modifier.height(12.dp))
                MapPane(geo, counts, selected, true, onPick, null, Modifier.weight(1f).fillMaxWidth().clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow))
                Spacer(Modifier.height(12.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterHorizontally), verticalAlignment = Alignment.CenterVertically) {
                    Text("Fewer", fontSize = 11.sp, color = c.onSurfaceVariant)
                    fills.forEach { Box(Modifier.width(26.dp).height(10.dp).clip(RoundedCornerShape(5.dp)).background(it)) }
                    Text("More colleges", fontSize = 11.sp, color = c.onSurfaceVariant)
                }
                if (selected.isNotEmpty()) {
                    Spacer(Modifier.height(12.dp))
                    PwButton("Show colleges in $selected", null, true, onClose, Modifier.fillMaxWidth())
                }
            }
        }
    }
}
