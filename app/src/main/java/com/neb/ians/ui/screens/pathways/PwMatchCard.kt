@file:OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.roundToInt

/** One ranked course. The best one is tinted; tapping a card opens why it scored, five bars and the facts. */
@Composable
internal fun PwMatchCard(d: PwData, m: PwMatch, top: Boolean, open: Boolean, saved: Boolean, onToggle: () -> Unit, onOpen: () -> Unit, onSave: () -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    val fg = if (top) c.onPrimaryContainer else c.onSurface
    val turn by animateFloatAsState(if (open) 90f else 0f, tween(300, easing = FastOutSlowInEasing), label = "chv")
    PwSurface(modifier.fillMaxWidth(), color = if (top) c.primaryContainer else c.surfaceContainerLow, radius = 26.dp) {
        Column {
            PwSurface(Modifier.fillMaxWidth(), color = androidx.compose.ui.graphics.Color.Transparent, radius = 26.dp, onClick = onToggle) {
                Row(Modifier.padding(12.dp, 12.dp, 16.dp, 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    PwRing(m.score, null, 46.dp, fg, fg.copy(alpha = if (top) 0.14f else 1f).let { if (top) it else c.surfaceContainerHighest }, fg)
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text(m.route.name, color = fg, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis, lineHeight = 18.sp)
                        if (m.why.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(4.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            m.why.forEach { PwReason(it, fg) }
                        } else Text(groupLabel(m.route.group), color = fg.copy(alpha = 0.72f), fontSize = 12.sp, fontWeight = FontWeight.Medium)
                    }
                    Icon(Icons.AutoMirrored.Outlined.ArrowForward, null, Modifier.graphicsLayer { rotationZ = turn }, tint = fg)
                }
            }
            AnimatedVisibility(open, enter = expandVertically(tween(300, easing = FastOutSlowInEasing)) + fadeIn(tween(300)), exit = shrinkVertically(tween(220)) + fadeOut(tween(120))) {
                Column(Modifier.padding(16.dp, 2.dp, 16.dp, 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    m.parts.forEach { (label, v) ->
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text(label, Modifier.width(76.dp), color = fg, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            PwBar(v.coerceAtLeast(0.04f), Modifier.weight(1f), 8.dp, fg, fg.copy(alpha = 0.12f))
                            Text("${(v * 100).roundToInt()}", Modifier.width(30.dp), color = fg, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.End)
                        }
                    }
                    val mt = d.m(m.route)
                    val pay = if (mt.payHi > 0) "NPR ${money(mt.payLo)}–${money(mt.payHi)}" else "Varies"
                    PwFacts(
                        listOf("Duration" to yearsText(mt.years).ifEmpty { "Varies" }, "Fees" to feeText(m.route.feeMin, m.route.feeMax).removePrefix("NPR "), "Start pay" to pay),
                        Modifier.padding(top = 6.dp), container = fg.copy(alpha = if (top) 0.08f else 0.0f).let { if (top) it else c.surfaceContainerHigh }, ink = fg,
                    )
                    if (m.neg.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(4.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) { m.neg.forEach { PwReason(it, fg, 0.6f) } }
                    Row(Modifier.padding(top = 2.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        PwButton("Open course", null, false, onOpen, Modifier.weight(1f))
                        PwIconButton(if (saved) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, "Save", onSave, container = if (saved) c.primary else fg.copy(alpha = 0.1f), tint = if (saved) c.onPrimary else fg)
                    }
                }
            }
        }
    }
}

@Composable
internal fun PwReason(text: String, ink: androidx.compose.ui.graphics.Color, alpha: Float = 1f) {
    Text(
        text, Modifier.clip(RoundedCornerShape(8.dp)).background(ink.copy(alpha = 0.1f)).padding(horizontal = 8.dp, vertical = 2.dp),
        color = ink.copy(alpha = alpha), fontSize = 11.sp, fontWeight = FontWeight.SemiBold, maxLines = 1,
    )
}
