package com.neb.ians.ui.screens.institutions

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/** The section of the owner editor that holds each completeness key (one list, shared with the server weights). */
internal val SECTION_FOR = mapOf(
    "about" to "About", "est" to "Basics", "levels" to "Levels offered", "principal" to "Basics", "teachers" to "Numbers",
    "students" to "Numbers", "facilities" to "Facilities", "feeMin" to "Fees", "phone" to "Contact", "address" to "Contact",
    "affiliations" to "Basics", "branches" to "Branches", "admissionOpen" to "Admissions", "socials" to "Social links", "ownership" to "Basics"
)

/** Page-card colour from the concept: white card in light, the raised graphite step in dark. */
@Composable
internal fun cardColor() = MaterialTheme.colorScheme.let { if (it.surface.luminance() < 0.5f) it.surfaceContainerLow else it.surface }

/** Concept `.card`: 24dp, hairline, title row with a primary glyph and an optional Edit action on the right. */
@Composable
internal fun PCard(title: String, icon: ImageVector, editKey: String?, onEdit: (String) -> Unit, content: @Composable () -> Unit) {
    Surface(
        color = cardColor(), shape = RoundedCornerShape(24.dp), tonalElevation = 0.dp, shadowElevation = 0.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.55f)), modifier = Modifier.fillMaxWidth()
    ) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Icon(icon, null, Modifier.size(20.dp), tint = MaterialTheme.colorScheme.primary)
                Text(title, Modifier.weight(1f), fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                if (editKey != null) Text(
                    "Edit", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.clip(RoundedCornerShape(12.dp)).clickable { onEdit(editKey) }.padding(horizontal = 10.dp, vertical = 8.dp)
                )
            }
            content()
        }
    }
}

/** Concept `.add`: a dashed, tappable placeholder the owner sees where a section is still empty. */
@Composable
internal fun AddSlot(text: String, onClick: () -> Unit) {
    val line = MaterialTheme.colorScheme.outlineVariant
    Row(
        Modifier.fillMaxWidth().clip(RoundedCornerShape(20.dp)).clickable(onClick = onClick)
            .drawDashed(line).padding(14.dp),
        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Icon(Icons.Outlined.Add, null, Modifier.size(20.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(text, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

private fun Modifier.drawDashed(color: androidx.compose.ui.graphics.Color) = this.drawBehind {
    val w = 1.5.dp.toPx()
    drawRoundRect(
        color, Offset(w / 2, w / 2), Size(size.width - w, size.height - w), androidx.compose.ui.geometry.CornerRadius(20.dp.toPx()),
        style = Stroke(w, pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(18f, 12f)))
    )
}

/** Concept `.stat`: big number over a small caption in a quiet tile. */
@Composable
internal fun StatGrid(facts: List<Pair<String, String>>) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        facts.chunked(2).forEach { row ->
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                row.forEach { (k, v) ->
                    Surface(color = MaterialTheme.colorScheme.surfaceContainerLow, shape = RoundedCornerShape(20.dp), modifier = Modifier.weight(1f)) {
                        Column(Modifier.padding(14.dp)) {
                            Text(v, fontSize = 26.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.5).sp, maxLines = 1)
                            Text(k, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
                if (row.size == 1) Spacer(Modifier.weight(1f))
            }
        }
    }
}

/** Concept `.bar2`: a 12dp rounded bar that grows in once. */
@Composable
internal fun FeeBar(fraction: Float) {
    val f by animateFloatAsState(fraction.coerceIn(0.04f, 1f), tween(800), label = "fee")
    Box(Modifier.fillMaxWidth().height(12.dp).clip(RoundedCornerShape(6.dp)).background(MaterialTheme.colorScheme.surfaceContainerHighest)) {
        Box(Modifier.fillMaxWidth(f).height(12.dp).clip(RoundedCornerShape(6.dp)).background(MaterialTheme.colorScheme.primary))
    }
}

/** Concept `.ring`: portfolio strength as a rounded arc with the percentage inside. */
@Composable
internal fun StrengthRing(percent: Int) {
    val sweep by animateFloatAsState(percent / 100f, tween(900), label = "ring")
    val track = MaterialTheme.colorScheme.surfaceContainerHighest
    val arc = MaterialTheme.colorScheme.primary
    Box(Modifier.size(84.dp), contentAlignment = Alignment.Center) {
        Canvas(Modifier.size(84.dp)) {
            val w = 9.dp.toPx()
            val inset = w / 2
            val sz = Size(size.width - w, size.height - w)
            drawArc(track, 0f, 360f, false, Offset(inset, inset), sz, style = Stroke(w))
            drawArc(arc, -90f, 360f * sweep, false, Offset(inset, inset), sz, style = Stroke(w, cap = StrokeCap.Round))
        }
        Text("$percent%", fontSize = 19.sp, fontWeight = FontWeight.SemiBold)
    }
}

/** Ring, one honest sentence, and the sections that would lift the score most (tap opens that section). */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun StrengthCard(percent: Int, sentence: String, steps: List<String>, onStep: (String) -> Unit) {
    PCardBare {
        Row(verticalAlignment = Alignment.CenterVertically) {
            StrengthRing(percent)
            Spacer(Modifier.width(16.dp))
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("Portfolio strength", fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                Text(sentence, fontSize = 12.5.sp, lineHeight = 18.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        if (steps.isNotEmpty()) FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            steps.forEach { s ->
                Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(18.dp), modifier = Modifier.clip(RoundedCornerShape(18.dp)).clickable { onStep(s) }) {
                    Text(s, fontSize = 12.5.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onPrimaryContainer, modifier = Modifier.padding(horizontal = 13.dp, vertical = 9.dp))
                }
            }
        }
    }
}

@Composable
internal fun PCardBare(content: @Composable () -> Unit) {
    Surface(
        color = cardColor(), shape = RoundedCornerShape(24.dp), tonalElevation = 0.dp, shadowElevation = 0.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.55f)), modifier = Modifier.fillMaxWidth()
    ) { Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) { content() } }
}
