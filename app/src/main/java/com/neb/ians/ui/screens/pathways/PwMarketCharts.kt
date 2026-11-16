package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.TrendingDown
import androidx.compose.material.icons.automirrored.outlined.TrendingFlat
import androidx.compose.material.icons.automirrored.outlined.TrendingUp
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.abs

private fun level(v: Int) = when { v <= 20 -> "Very low"; v <= 40 -> "Low"; v <= 60 -> "Medium"; v <= 80 -> "High"; else -> "Very high" }

private fun verdict(d: Int, c: Int) = when {
    d >= 60 && c <= 40 -> "Open field"
    d >= 60 && c >= 60 -> "In demand, crowded"
    d <= 40 && c >= 60 -> "Tough market"
    d <= 40 && c <= 40 -> "Small, quiet niche"
    else -> "Balanced market"
}

/** Demand and competition side by side with a plain verdict and the direction of travel. */
@Composable
internal fun PwMarketBalance(k: PwCareer) {
    val c = MaterialTheme.colorScheme
    val d = pct(k.demand); val comp = pct(k.competition)
    val t = k.trend.lowercase()
    Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow).padding(20.dp, 18.dp, 20.dp, 20.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            Text(verdict(d, comp), Modifier.weight(1f), fontSize = 20.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-0.4).sp)
            if (t == "rising" || t == "falling" || t == "stable") Row(
                Modifier.clip(RoundedCornerShape(16.dp)).background(if (t == "rising") c.primaryContainer else c.surfaceContainerHighest).padding(10.dp, 6.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                Icon(when (t) { "rising" -> Icons.AutoMirrored.Outlined.TrendingUp; "falling" -> Icons.AutoMirrored.Outlined.TrendingDown; else -> Icons.AutoMirrored.Outlined.TrendingFlat }, null, Modifier.size(18.dp), tint = if (t == "rising") c.onPrimaryContainer else c.onSurfaceVariant)
                Text(t.replaceFirstChar { it.uppercase() }, fontSize = 12.sp, fontWeight = FontWeight.Bold, color = if (t == "rising") c.onPrimaryContainer else c.onSurfaceVariant)
            }
        }
        Meter("Demand", d, c.primary)
        Meter("Competition", comp, c.onSurface)
    }
}

@Composable
private fun Meter(label: String, v: Int, color: androidx.compose.ui.graphics.Color) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text(label, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Text("${level(v)} · $v", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        PwBar(v / 100f, Modifier.fillMaxWidth(), 12.dp, color)
    }
}

/** Real yearly demand when the data has it: line, soft area, a dot per year, first and last year, last value. */
@Composable
internal fun PwTrendChart(vals: List<Float>, lastYear: Int) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val tick = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.Medium)
    val tip = MaterialTheme.typography.labelMedium.copy(color = c.surface, fontWeight = FontWeight.Bold)
    Canvas(Modifier.fillMaxWidth().height(150.dp).clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow)) {
        val l = 24.dp.toPx(); val w = size.width - 2 * l
        val t = 34.dp.toPx(); val b = size.height - 28.dp.toPx()
        fun px(i: Int) = l + i * w / (vals.size - 1)
        fun py(v: Float) = b - v.coerceIn(0f, 100f) / 100f * (b - t)
        val dash = PathEffect.dashPathEffect(floatArrayOf(5.dp.toPx(), 5.dp.toPx()))
        listOf(50f, 100f).forEach { drawLine(c.outlineVariant, Offset(l, py(it)), Offset(l + w, py(it)), 1.dp.toPx(), pathEffect = dash) }
        val line = Path().apply { vals.forEachIndexed { i, v -> if (i == 0) moveTo(px(i), py(v)) else lineTo(px(i), py(v)) } }
        val area = Path().apply { addPath(line); lineTo(px(vals.lastIndex), b); lineTo(px(0), b); close() }
        drawPath(area, c.primary.copy(alpha = 0.14f))
        drawPath(line, c.primary, style = Stroke(3.5.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round))
        vals.forEachIndexed { i, v -> drawCircle(c.surfaceContainerLow, 6.dp.toPx(), Offset(px(i), py(v))); drawCircle(c.primary, 4.dp.toPx(), Offset(px(i), py(v))) }
        val first = tm.measure("${lastYear - vals.size + 1}", tick); val last = tm.measure("$lastYear", tick)
        drawText(first, topLeft = Offset(l - first.size.width / 2f + 6.dp.toPx(), b + 8.dp.toPx()))
        drawText(last, topLeft = Offset(l + w - last.size.width + 6.dp.toPx(), b + 8.dp.toPx()))
        val txt = tm.measure("${vals.last().toInt()}", tip)
        val p = Offset(px(vals.lastIndex), py(vals.last()))
        val pw = txt.size.width + 18.dp.toPx(); val ph = 24.dp.toPx()
        drawRoundRect(c.onSurface, Offset(p.x - pw / 2f, p.y - ph - 12.dp.toPx()), Size(pw, ph), CornerRadius(ph / 2f))
        drawText(txt, topLeft = Offset(p.x - txt.size.width / 2f, p.y - ph - 12.dp.toPx() + (ph - txt.size.height) / 2f))
    }
}

private fun spot(w: Float, h: Float, d: Float, comp: Float, dem: Float): Offset {
    val l = 30 * d; val r = 12 * d; val t = 12 * d; val b = 30 * d
    return Offset(l + (0.08f + 0.84f * comp / 100f) * (w - l - r), h - b - (0.08f + 0.84f * dem / 100f) * (h - t - b))
}

/** Every career on demand against competition. The sweet corner (high demand, low competition) is tinted; tap a dot to read it. */
@Composable
internal fun PwQuadrant(d: PwData, k: PwCareer, onOpen: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    val tm = rememberTextMeasurer()
    val tick = MaterialTheme.typography.labelSmall.copy(color = c.onSurfaceVariant, fontWeight = FontWeight.Medium)
    val zone = MaterialTheme.typography.labelMedium.copy(color = c.onPrimaryContainer, fontWeight = FontWeight.Bold)
    val tip = MaterialTheme.typography.labelMedium.copy(color = c.surface, fontWeight = FontWeight.Bold)
    // ratings are whole steps, so a small stable offset per career keeps dots on one step from hiding each other
    val pts = remember(d) { d.careers.values.map { x -> val h = abs(x.id.hashCode()); Triple(x, (pct(x.competition) + (h % 11 - 5)).toFloat(), (pct(x.demand) + (h / 11 % 11 - 5)).toFloat()) } }
    var sel by remember(k.id) { mutableStateOf(k.id) }
    val chosen = pts.firstOrNull { it.first.id == sel }
    Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(28.dp)).background(c.surfaceContainerLow).padding(bottom = 6.dp)) {
        Canvas(
            Modifier.fillMaxWidth().aspectRatio(1.2f)
                .semantics { contentDescription = "Demand against competition for ${pts.size} careers. ${k.name}: demand ${pct(k.demand)}, competition ${pct(k.competition)}" }
                .pointerInput(pts) {
                    detectTapGestures { pos ->
                        val hit = pts.minByOrNull { (_, x, y) -> (spot(size.width.toFloat(), size.height.toFloat(), density, x, y) - pos).getDistance() }
                        if (hit != null && (spot(size.width.toFloat(), size.height.toFloat(), density, hit.second, hit.third) - pos).getDistance() < 26.dp.toPx()) sel = hit.first.id
                    }
                },
        ) {
            val l = 30.dp.toPx(); val r = 12.dp.toPx(); val t = 12.dp.toPx(); val b = 30.dp.toPx()
            val pw = size.width - l - r; val ph = size.height - t - b
            drawRoundRect(c.surfaceContainerHigh.copy(alpha = 0.6f), Offset(l, t), Size(pw, ph), CornerRadius(20.dp.toPx()))
            drawRoundRect(c.primaryContainer.copy(alpha = 0.75f), Offset(l, t), Size(pw / 2f, ph / 2f), CornerRadius(20.dp.toPx()))
            val dash = PathEffect.dashPathEffect(floatArrayOf(4.dp.toPx(), 5.dp.toPx()))
            drawLine(c.outlineVariant, Offset(l + pw / 2f, t), Offset(l + pw / 2f, t + ph), 1.dp.toPx(), pathEffect = dash)
            drawLine(c.outlineVariant, Offset(l, t + ph / 2f), Offset(l + pw, t + ph / 2f), 1.dp.toPx(), pathEffect = dash)
            val z = tm.measure("Best odds", zone)
            drawText(z, topLeft = Offset(l + 12.dp.toPx(), t + 10.dp.toPx()))
            val xl = tm.measure("Competition", tick)
            drawText(xl, topLeft = Offset(l + pw / 2f - xl.size.width / 2f, size.height - xl.size.height - 4.dp.toPx()))
            val yl = tm.measure("Demand", tick)
            rotate(-90f, Offset(10.dp.toPx(), t + ph / 2f)) { drawText(yl, topLeft = Offset(10.dp.toPx() - yl.size.width / 2f, t + ph / 2f - yl.size.height / 2f)) }
            pts.forEach { (x, cx, cy) -> if (x.id != k.id && x.id != sel) drawCircle(c.onSurfaceVariant.copy(alpha = 0.5f), 4.5.dp.toPx(), spot(size.width, size.height, density, cx, cy)) }
            pts.firstOrNull { it.first.id == k.id }?.let { (_, cx, cy) ->
                val p = spot(size.width, size.height, density, cx, cy)
                drawCircle(c.primary.copy(alpha = 0.22f), 16.dp.toPx(), p); drawCircle(c.primary, 8.dp.toPx(), p)
            }
            if (chosen != null && chosen.first.id != k.id) {
                val p = spot(size.width, size.height, density, chosen.second, chosen.third)
                drawCircle(c.surfaceContainerLow, 9.dp.toPx(), p); drawCircle(c.onSurface, 6.5.dp.toPx(), p)
            }
            if (chosen != null) {
                val p = spot(size.width, size.height, density, chosen.second, chosen.third)
                val txt = tm.measure(chosen.first.name, tip)
                val bw = txt.size.width + 20.dp.toPx(); val bh = 26.dp.toPx()
                val bx = (p.x - bw / 2f).coerceIn(l, size.width - r - bw)
                val by = if (p.y - bh - 16.dp.toPx() < t) p.y + 14.dp.toPx() else p.y - bh - 14.dp.toPx()
                drawRoundRect(c.onSurface, Offset(bx, by), Size(bw, bh), CornerRadius(bh / 2f))
                drawText(txt, topLeft = Offset(bx + 10.dp.toPx(), by + (bh - txt.size.height) / 2f))
            }
        }
        if (chosen != null && chosen.first.id != k.id) Row(Modifier.fillMaxWidth().padding(16.dp, 4.dp, 8.dp, 4.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text(chosen.first.name, fontSize = 14.sp, fontWeight = FontWeight.Bold, maxLines = 1)
                Text("Demand ${pct(chosen.first.demand)} · Competition ${pct(chosen.first.competition)}", fontSize = 12.sp, color = c.onSurfaceVariant)
            }
            PwButton("Open", null, false, { onOpen(chosen.first.id) })
        } else Spacer(Modifier.height(6.dp))
    }
}
