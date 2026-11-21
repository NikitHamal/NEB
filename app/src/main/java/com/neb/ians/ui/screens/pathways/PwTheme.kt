package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Outline
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.roundToInt
import kotlin.math.sin

/** One flat colour family: container, its ink, and the strong version used for fills. */
internal data class PwTone(val bg: Color, val fg: Color, val solid: Color, val onSolid: Color)

@Composable
internal fun pwTone(i: Int): PwTone {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.luminance() < 0.5f
    val all = remember(c, dark) {
        listOf(
            PwTone(c.primaryContainer, c.onPrimaryContainer, c.primary, c.onPrimary),
            if (dark) PwTone(Color(0xFF5B3D57), Color(0xFFFFD7F5), Color(0xFFFFACE8), Color(0xFF380038))
            else PwTone(Color(0xFFFFD7F5), Color(0xFF380038), Color(0xFF7A2A6B), Color.White),
            if (dark) PwTone(Color(0xFF584400), Color(0xFFFFE08A), Color(0xFFFFD34D), Color(0xFF241A00))
            else PwTone(Color(0xFFFFE08A), Color(0xFF241A00), Color(0xFF5C4600), Color(0xFFFFE08A)),
            PwTone(c.secondaryContainer, c.onSecondaryContainer, c.secondary, c.onSecondary),
            if (dark) PwTone(Color(0xFF0F5223), Color(0xFFC4EFCB), Color(0xFF8BD99B), Color(0xFF00210C))
            else PwTone(Color(0xFFC4EFCB), Color(0xFF00210C), Color(0xFF1E6B34), Color.White),
            if (dark) PwTone(Color(0xFF73342B), Color(0xFFFFDAD4), Color(0xFFFFB4A8), Color(0xFF3B0907))
            else PwTone(Color(0xFFFFDAD4), Color(0xFF3B0907), Color(0xFF8C2A1F), Color.White),
        )
    }
    return all[((i % all.size) + all.size) % all.size]
}

/** Seven distinct series colours for splits and charts, first one is the brand primary. */
@Composable
internal fun pwSeries(): List<Color> {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.luminance() < 0.5f
    return remember(c, dark) {
        if (dark) listOf(c.primary, Color(0xFFFFD166), Color(0xFFFFACE8), Color(0xFF8BD99B), Color(0xFFFFB4A8), Color(0xFFA9ABB8), Color(0xFF6B6D7A))
        else listOf(c.primary, Color(0xFFC98A00), Color(0xFFB5479B), Color(0xFF1E8E4A), Color(0xFFD9532B), Color(0xFF6B6D7A), Color(0xFFA9ABB8))
    }
}

/** M3 Expressive scalloped blob with [lobes] bumps. */
internal class ScallopShape(private val lobes: Int, private val depth: Float = 0.1f) : Shape {
    override fun createOutline(size: Size, layoutDirection: LayoutDirection, density: Density): Outline {
        val p = Path()
        val cx = size.width / 2f
        val cy = size.height / 2f
        val r0 = min(cx, cy)
        for (i in 0 until 120) {
            val t = i / 120.0 * 2 * PI
            val r = r0 * (1.0 - depth + depth * cos(lobes * t)).toFloat()
            val x = cx + r * cos(t).toFloat()
            val y = cy + r * sin(t).toFloat()
            if (i == 0) p.moveTo(x, y) else p.lineTo(x, y)
        }
        p.close()
        return Outline.Generic(p)
    }
}

private val bouncy = spring<Dp>(dampingRatio = 0.5f, stiffness = Spring.StiffnessMediumLow)

@Composable
internal fun PwSurface(
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colorScheme.surfaceContainerLow,
    radius: Dp = 24.dp,
    onClick: (() -> Unit)? = null,
    content: @Composable () -> Unit,
) {
    if (onClick == null) {
        Surface(modifier, shape = RoundedCornerShape(radius), color = color, content = content)
        return
    }
    val src = remember { MutableInteractionSource() }
    val pressed by src.collectIsPressedAsState()
    val r by animateDpAsState(if (pressed) radius / 2 else radius, bouncy, label = "pressR")
    Surface(onClick = onClick, modifier = modifier, shape = RoundedCornerShape(r), color = color, interactionSource = src, content = content)
}

@Composable
internal fun PwChip(label: String, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier, height: Dp = 40.dp) {
    val c = MaterialTheme.colorScheme
    val r by animateDpAsState(if (selected) 12.dp else height / 2, bouncy, label = "chipR")
    val bg by animateColorAsState(if (selected) c.onSurface else c.surfaceContainerHigh, label = "chipBg")
    Surface(
        onClick = onClick, modifier = modifier.height(height), shape = RoundedCornerShape(r), color = bg,
        contentColor = if (selected) c.surface else c.onSurface,
    ) {
        Box(Modifier.padding(horizontal = 16.dp), contentAlignment = Alignment.Center) {
            Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, maxLines = 1)
        }
    }
}

@Composable
internal fun PwChipRow(items: List<Pair<String, String>>, selected: (String) -> Boolean, onClick: (String) -> Unit, modifier: Modifier = Modifier, inset: Dp = 16.dp) {
    Row(
        modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(horizontal = inset),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
    ) { items.forEach { (k, label) -> PwChip(label, selected(k), { onClick(k) }) } }
}

/** Connected button group: neighbours share tight corners, the selected one rounds fully. */
@Composable
internal fun <T> PwSeg(items: List<Pair<T, String>>, selected: T, onSelect: (T) -> Unit, modifier: Modifier = Modifier, fill: Boolean = true, height: Dp = 44.dp) {
    val c = MaterialTheme.colorScheme
    Row(if (fill) modifier.fillMaxWidth() else modifier, horizontalArrangement = Arrangement.spacedBy(3.dp)) {
        items.forEachIndexed { i, (key, label) ->
            val on = key == selected
            val l by animateDpAsState(if (on || i == 0) height / 2 else 8.dp, bouncy, label = "segL")
            val r by animateDpAsState(if (on || i == items.lastIndex) height / 2 else 8.dp, bouncy, label = "segR")
            val bg by animateColorAsState(if (on) c.onSurface else c.surfaceContainerHigh, label = "segBg")
            Surface(
                onClick = { onSelect(key) },
                modifier = (if (fill) Modifier.weight(1f) else Modifier).height(height),
                shape = RoundedCornerShape(topStart = l, bottomStart = l, topEnd = r, bottomEnd = r),
                color = bg, contentColor = if (on) c.surface else c.onSurface,
            ) {
                Box(Modifier.padding(horizontal = if (fill) 6.dp else 16.dp), contentAlignment = Alignment.Center) {
                    Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
            }
        }
    }
}

@Composable
internal fun PwTabs(items: List<Pair<String, String>>, selected: String, onSelect: (String) -> Unit) =
    PwChipRow(items, { it == selected }, onSelect)

@Composable
internal fun PwIconButton(
    icon: ImageVector, description: String, onClick: () -> Unit,
    container: Color = MaterialTheme.colorScheme.surfaceContainerHigh, tint: Color = MaterialTheme.colorScheme.onSurface, badge: Int = 0,
) {
    val src = remember { MutableInteractionSource() }
    val pressed by src.collectIsPressedAsState()
    val r by animateDpAsState(if (pressed) 14.dp else 22.dp, bouncy, label = "ibR")
    Box {
        Surface(onClick = onClick, shape = RoundedCornerShape(r), color = container, interactionSource = src) {
            Box(Modifier.size(44.dp), contentAlignment = Alignment.Center) { Icon(icon, description, Modifier.size(22.dp), tint = tint) }
        }
        if (badge > 0) PwCount(badge, Modifier.align(Alignment.TopEnd))
    }
}

@Composable
internal fun PwCount(n: Int, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    Box(modifier.heightIn(min = 18.dp).widthIn(min = 18.dp).clip(RoundedCornerShape(9.dp)).background(c.onSurface).padding(horizontal = 4.dp), contentAlignment = Alignment.Center) {
        Text("$n", color = c.surface, fontSize = 10.sp, fontWeight = FontWeight.SemiBold, lineHeight = 12.sp)
    }
}

@Composable
internal fun PwButton(text: String, icon: ImageVector?, filled: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    val src = remember { MutableInteractionSource() }
    val pressed by src.collectIsPressedAsState()
    val r by animateDpAsState(if (pressed) 16.dp else 28.dp, bouncy, label = "btnR")
    Surface(
        onClick = onClick, modifier = modifier.height(56.dp), shape = RoundedCornerShape(r), interactionSource = src,
        color = if (filled) c.primary else c.primaryContainer, contentColor = if (filled) c.onPrimary else c.onPrimaryContainer,
    ) {
        Row(Modifier.padding(horizontal = 20.dp), horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterHorizontally), verticalAlignment = Alignment.CenterVertically) {
            if (icon != null) Icon(icon, null, Modifier.size(18.dp))
            Text(text, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}

/** Sticky action bar at the bottom of a detail screen. */
@Composable
internal fun PwActions(modifier: Modifier = Modifier, content: @Composable RowScope.() -> Unit) {
    Row(
        modifier.fillMaxWidth().background(MaterialTheme.colorScheme.surface).navigationBarsPadding().padding(16.dp, 12.dp, 16.dp, 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp), content = content,
    )
}

@Composable
internal fun PwRootBar(onSearch: () -> Unit, onBack: (() -> Unit)? = null, scrolled: () -> Float = { 0f }) {
    val c = MaterialTheme.colorScheme
    val line = c.outlineVariant
    Row(
        Modifier.fillMaxWidth().background(c.surface)
            .drawBehind {
                val a = scrolled()
                if (a > 0f) drawRect(line.copy(alpha = a), Offset(0f, size.height - 1.dp.toPx()), Size(size.width, 1.dp.toPx()))
            }
            .statusBarsPadding().padding(16.dp, 12.dp, 16.dp, 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        if (onBack != null) PwIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack)
        Text("Pathways", Modifier.weight(1f), fontSize = 21.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.4).sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
        PwIconButton(Icons.Outlined.Search, "Search", onSearch)
    }
}

@Composable
internal fun PwBackBar(title: String, onBack: () -> Unit, scrolled: () -> Float = { 0f }) {
    val c = MaterialTheme.colorScheme
    val line = c.outlineVariant
    Row(
        Modifier.fillMaxWidth().background(c.surface)
            .drawBehind {
                val a = scrolled()
                if (a > 0f) drawRect(line.copy(alpha = a), Offset(0f, size.height - 1.dp.toPx()), Size(size.width, 1.dp.toPx()))
            }
            .statusBarsPadding().padding(16.dp, 12.dp, 16.dp, 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        PwIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack)
        Text(title, Modifier.weight(1f), fontSize = 22.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.5).sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@Composable
internal fun PwBadge(tone: PwTone, lobes: Int, size: Dp = 92.dp, content: @Composable ColumnScope.() -> Unit) {
    val spin = rememberInfiniteTransition(label = "badge").animateFloat(0f, 360f, infiniteRepeatable(tween(28000, easing = LinearEasing)), label = "spin")
    val shape = remember(lobes) { ScallopShape(lobes) }
    Box(Modifier.size(size), contentAlignment = Alignment.Center) {
        Box(Modifier.matchParentSize().graphicsLayer { rotationZ = spin.value }.background(tone.fg, shape))
        CompositionLocalProvider(LocalContentColor provides tone.bg) {
            Column(horizontalAlignment = Alignment.CenterHorizontally, content = content)
        }
    }
}

@Composable
internal fun PwHero(tone: PwTone, title: String, sub: String, badge: @Composable () -> Unit) {
    Column(
        Modifier.fillMaxWidth().clip(RoundedCornerShape(bottomStart = 36.dp, bottomEnd = 36.dp)).background(tone.bg)
            .statusBarsPadding().padding(start = 16.dp, end = 16.dp, top = 68.dp, bottom = 24.dp),
    ) {
        Row(verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Column(Modifier.weight(1f)) {
                Text(title, color = tone.fg, fontSize = 25.sp, lineHeight = 26.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.5).sp)
                if (sub.isNotBlank()) Text(sub, Modifier.padding(top = 4.dp), color = tone.fg.copy(alpha = 0.78f), fontSize = 13.sp, fontWeight = FontWeight.Medium)
            }
            badge()
        }
    }
}

/** Ring meter that sweeps in when it first appears and glides when the value changes. */
@Composable
internal fun PwRing(
    value: Int, label: String?, size: Dp = 64.dp,
    color: Color = MaterialTheme.colorScheme.primary, track: Color = MaterialTheme.colorScheme.surfaceContainerHighest,
    ink: Color = MaterialTheme.colorScheme.onSurface,
) {
    val a = remember { Animatable(0f) }
    LaunchedEffect(value) { a.animateTo(value.coerceIn(0, 100) / 100f, tween(900, easing = FastOutSlowInEasing)) }
    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Box(
            Modifier.size(size).drawBehind {
                val w = this.size.width * 0.11f
                val s = Size(this.size.width - w, this.size.height - w)
                val o = Offset(w / 2, w / 2)
                drawArc(track, 0f, 360f, false, o, s, style = Stroke(w))
                drawArc(color, -90f, 360f * a.value, false, o, s, style = Stroke(w, cap = StrokeCap.Round))
            },
            contentAlignment = Alignment.Center,
        ) { Text("$value", color = ink, fontSize = (size.value * 0.27f).sp, fontWeight = FontWeight.SemiBold) }
        if (label != null) Text(label, fontSize = 11.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
internal fun PwMeters(demand: Int, competition: Int, big: String?, small: String?) {
    val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth().padding(20.dp, 18.dp, 20.dp, 16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
        PwRing(demand, "Demand")
        PwRing(competition, "Competition", color = c.onSurface)
        if (big != null) Column(Modifier.weight(1f).clip(RoundedCornerShape(22.dp)).background(c.surfaceContainerHigh).padding(16.dp, 12.dp)) {
            Text(big, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.3).sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
            if (small != null) Text(small, fontSize = 11.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}

/** Track with a fill that grows once when it appears. */
@Composable
internal fun PwBar(fraction: Float, modifier: Modifier = Modifier.fillMaxWidth(), height: Dp = 8.dp, color: Color = MaterialTheme.colorScheme.primary, track: Color = MaterialTheme.colorScheme.surfaceContainerHighest, start: Float = 0f) {
    val a = remember { Animatable(0f) }
    LaunchedEffect(fraction) { a.animateTo(fraction.coerceIn(0f, 1f), tween(650, easing = FastOutSlowInEasing)) }
    Box(
        modifier.height(height).clip(RoundedCornerShape(height / 2)).drawBehind {
            drawRect(track)
            val x = size.width * start.coerceIn(0f, 1f)
            drawRoundRect(color, Offset(x, 0f), Size((size.width * a.value).coerceAtLeast(size.height), size.height), CornerRadius(size.height / 2))
        },
    )
}

/** Stacked bar plus legend; tapping a part spotlights it. */
@Composable
internal fun PwSplit(parts: List<PwPart>, fmt: (Float) -> String = { "${it.roundToInt()}%" }) {
    val c = MaterialTheme.colorScheme
    val cols = pwSeries()
    val ps = parts.filter { it.value > 0f }
    var sel by remember(parts) { mutableIntStateOf(-1) }
    Column {
        Row(Modifier.fillMaxWidth().height(40.dp), horizontalArrangement = Arrangement.spacedBy(3.dp)) {
            ps.forEachIndexed { i, p ->
                val l = if (i == 0) 20.dp else 8.dp
                val r = if (i == ps.lastIndex) 20.dp else 8.dp
                val rr = if (sel == i) 20.dp else 0.dp
                Box(
                    Modifier.weight(p.value).fillMaxHeight()
                        .clip(RoundedCornerShape(topStart = maxOf(l, rr), bottomStart = maxOf(l, rr), topEnd = maxOf(r, rr), bottomEnd = maxOf(r, rr)))
                        .background(cols[i % cols.size].copy(alpha = if (sel < 0 || sel == i) 1f else 0.28f))
                        .clickable { sel = if (sel == i) -1 else i },
                )
            }
        }
        Spacer(Modifier.height(8.dp))
        ps.forEachIndexed { i, p ->
            Row(
                Modifier.fillMaxWidth().clip(RoundedCornerShape(14.dp)).background(if (sel == i) c.surfaceContainerHigh else Color.Transparent)
                    .clickable { sel = if (sel == i) -1 else i }.height(40.dp).padding(horizontal = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Box(Modifier.size(12.dp).clip(RoundedCornerShape(4.dp)).background(cols[i % cols.size]))
                Text(p.label, Modifier.weight(1f).padding(start = 10.dp), fontSize = 13.5.sp, fontWeight = if (sel == i) FontWeight.SemiBold else FontWeight.Medium, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(fmt(p.value), fontSize = 13.5.sp, fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

/** Twelve month strip; the current month is outlined. */
@Composable
internal fun PwMonths(active: (Int) -> Boolean, modifier: Modifier = Modifier, fill: Color = MaterialTheme.colorScheme.primary, onFill: Color = MaterialTheme.colorScheme.onPrimary, cellBg: Color? = null) {
    val now = remember { nowMonth() }
    val ink = MaterialTheme.colorScheme.onSurface
    Row(modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(2.dp)) {
        for (m in 1..12) {
            val on = active(m)
            Box(
                Modifier.weight(1f).height(20.dp)
                    .then(if (m == now) Modifier.border(2.dp, ink, RoundedCornerShape(6.dp)) else Modifier)
                    .clip(RoundedCornerShape(6.dp)).background(if (on) (cellBg ?: fill) else fill.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center,
            ) { Text(MONTHS[m - 1].take(1), fontSize = 9.sp, fontWeight = FontWeight.SemiBold, color = if (on) onFill else fill, lineHeight = 10.sp) }
        }
    }
}

@Composable
internal fun PwCalendar(rows: List<Pair<String, (Int) -> Boolean>>) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        rows.forEach { (label, f) ->
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(label, Modifier.width(52.dp), fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                PwMonths(f, Modifier.weight(1f))
            }
        }
    }
}

@Composable
internal fun PwFacts(items: List<Pair<String, String>>, modifier: Modifier = Modifier, container: Color = MaterialTheme.colorScheme.surfaceContainerHigh, ink: Color = MaterialTheme.colorScheme.onSurface) {
    Column(modifier, verticalArrangement = Arrangement.spacedBy(6.dp)) {
        items.chunked(3).forEach { row ->
            Row(Modifier.fillMaxWidth().height(IntrinsicSize.Min), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                row.forEach { (k, v) ->
                    Column(Modifier.weight(1f).fillMaxHeight().clip(RoundedCornerShape(18.dp)).background(container).padding(12.dp, 10.dp)) {
                        Text(k, fontSize = 10.5.sp, fontWeight = FontWeight.Medium, color = ink.copy(alpha = 0.7f), maxLines = 1)
                        Text(v, fontSize = 13.5.sp, fontWeight = FontWeight.SemiBold, lineHeight = 17.sp, color = ink)
                    }
                }
                repeat(3 - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

@Composable
internal fun PwBig(big: String, small: String?, tone: PwTone = pwTone(2)) {
    Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(28.dp)).background(tone.bg).padding(22.dp, 18.dp)) {
        Text(big, color = tone.fg, fontSize = 30.sp, lineHeight = 30.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.9).sp)
        if (small != null) Text(small, color = tone.fg, fontSize = 12.5.sp, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
internal fun PwH4(text: String, modifier: Modifier = Modifier) {
    Text(text, modifier.padding(top = 18.dp, bottom = 8.dp), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
}

@Composable
internal fun PwBigLine(text: String, accent: String = "", modifier: Modifier = Modifier) {
    Row(modifier.padding(top = 6.dp, bottom = 10.dp)) {
        Text(text, fontSize = 20.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.4).sp, lineHeight = 22.sp)
        if (accent.isNotEmpty()) Text(" $accent", fontSize = 20.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.4).sp, lineHeight = 22.sp, color = MaterialTheme.colorScheme.primary)
    }
}

@Composable
internal fun PwOutlineChip(text: String, on: Boolean = false, off: Boolean = false) {
    val c = MaterialTheme.colorScheme
    Box(
        Modifier.height(34.dp).clip(RoundedCornerShape(17.dp))
            .then(if (on) Modifier.background(c.onSurface) else Modifier.border(1.5.dp, c.outlineVariant, RoundedCornerShape(17.dp)))
            .graphicsLayer { alpha = if (off) 0.4f else 1f }.padding(horizontal = 14.dp),
        contentAlignment = Alignment.Center,
    ) { Text(text, fontSize = 12.5.sp, fontWeight = FontWeight.Medium, color = if (on) c.surface else c.onSurface, maxLines = 1) }
}

@Composable
internal fun PwTag(text: String, tone: PwTone) {
    Box(Modifier.height(26.dp).clip(RoundedCornerShape(9.dp)).background(tone.bg).padding(horizontal = 10.dp), contentAlignment = Alignment.Center) {
        Text(text, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = tone.fg, maxLines = 1)
    }
}

@Composable
internal fun PwEmpty(text: String) {
    val c = MaterialTheme.colorScheme
    Column(Modifier.fillMaxWidth().padding(vertical = 40.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Box(Modifier.size(72.dp).background(c.surfaceContainerHighest, ScallopShape(6)))
        Text(text, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = c.onSurfaceVariant, textAlign = TextAlign.Center)
    }
}

/** General list row. */
@Composable
internal fun PwRow(
    title: String, sub: String = "", trailing: String = "", onClick: (() -> Unit)? = null,
    on: Boolean = false, dim: Boolean = false, strong: Boolean = false, rise: Int = -1, below: (@Composable () -> Unit)? = null,
) {
    val c = MaterialTheme.colorScheme
    PwSurface(
        Modifier.fillMaxWidth().pwRise(rise).graphicsLayer { alpha = if (dim) 0.45f else 1f },
        color = if (on) c.primaryContainer else c.surfaceContainerLow, radius = 24.dp, onClick = onClick,
    ) {
        Column(Modifier.padding(horizontal = 18.dp, vertical = 14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text(title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis, lineHeight = 19.sp)
                    if (sub.isNotEmpty()) Text(sub, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                if (trailing.isNotEmpty()) Text(
                    trailing, Modifier.padding(start = 12.dp), maxLines = 1,
                    fontSize = if (strong) 15.sp else 11.sp, fontWeight = if (strong) FontWeight.SemiBold else FontWeight.SemiBold,
                    color = if (strong) c.onSurface else c.onSurfaceVariant,
                )
            }
            below?.invoke()
        }
    }
}

/** Numbered steps joined by a rail. Checkable steps turn into ticks. */
@Composable
internal fun PwSteps(items: List<Triple<String, String, String>>, done: (Int) -> Boolean = { false }, onToggle: ((Int) -> Unit)? = null) {
    val c = MaterialTheme.colorScheme
    Column {
        items.forEachIndexed { i, (title, sub, trailing) ->
            val ok = done(i)
            val r by animateDpAsState(if (ok) 20.dp else 14.dp, bouncy, label = "stepR")
            val bg by animateColorAsState(if (ok) c.primary else c.primaryContainer, label = "stepBg")
            Row(
                Modifier.fillMaxWidth().heightIn(min = 62.dp).pwRise(i)
                    .then(if (onToggle != null) Modifier.clip(RoundedCornerShape(16.dp)).clickable { onToggle(i) } else Modifier)
                    .drawBehind {
                        val x = 20.dp.toPx()
                        val w = 2.dp.toPx()
                        if (i > 0) drawRect(c.primaryContainer, Offset(x - w / 2, 0f), Size(w, size.height / 2))
                        if (i < items.lastIndex) drawRect(c.primaryContainer, Offset(x - w / 2, size.height / 2), Size(w, size.height / 2))
                    },
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                Box(Modifier.size(40.dp).clip(RoundedCornerShape(r)).background(bg), contentAlignment = Alignment.Center) {
                    if (ok) Icon(Icons.Outlined.Check, null, Modifier.size(18.dp), tint = c.onPrimary)
                    else Text("${i + 1}", fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = c.onPrimaryContainer)
                }
                Column(Modifier.weight(1f).padding(vertical = 8.dp).graphicsLayer { alpha = if (ok) 0.5f else 1f }) {
                    Text(title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, lineHeight = 19.sp)
                    if (sub.isNotEmpty()) Text(sub, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant, lineHeight = 16.sp)
                }
                if (trailing.isNotEmpty()) Text(trailing, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
internal fun PwSlider(value: Float, onChange: (Float) -> Unit, range: ClosedFloatingPointRange<Float>, steps: Int, label: String) {
    val c = MaterialTheme.colorScheme
    val page = c.surface
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        Slider(
            value, onChange, Modifier.weight(1f).height(44.dp), valueRange = range, steps = steps,
            thumb = {
                Box(Modifier.width(14.dp).height(44.dp).border(4.dp, page, RoundedCornerShape(7.dp)).padding(4.dp).clip(RoundedCornerShape(3.dp)).background(c.primary))
            },
            track = { Box(Modifier.fillMaxWidth().height(16.dp).clip(RoundedCornerShape(8.dp)).background(c.primaryContainer)) },
        )
        if (label.isNotEmpty()) Text(label, Modifier.widthIn(min = 64.dp), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.End, maxLines = 1)
    }
}

/** Rise on first show: fade, lift 14dp and settle from 95% on a spring. Only the first 6 rows animate; long lists skip it. */
@Composable
internal fun Modifier.pwRise(index: Int, key: Any? = Unit): Modifier {
    val reduced = com.neb.ians.ui.theme.nebAnimationsReduced()
    val live = !reduced && index in 0..5
    val a = remember(key, reduced) { Animatable(if (live) 0f else 1f) }
    if (live) LaunchedEffect(key) { kotlinx.coroutines.delay(index * 40L); a.animateTo(1f, spring(0.6f, Spring.StiffnessMediumLow)) }
    return this.graphicsLayer {
        val v = a.value
        alpha = v.coerceIn(0f, 1f)
        translationY = (1f - v) * 14.dp.toPx()
        val sc = 0.95f + 0.05f * v
        scaleX = sc; scaleY = sc
    }
}

/** Three bar demand glyph. */
@Composable
internal fun PwSignal(value: Int, color: Color, size: Dp = 14.dp) {
    val n = when { value >= 75 -> 3; value >= 50 -> 2; else -> 1 }
    Canvas(Modifier.size(size)) {
        val u = this.size.width / 14f
        for (i in 0..2) {
            val h = (5 + i * 4) * u
            drawRoundRect(color.copy(alpha = if (i < n) 1f else 0.25f), Offset(i * 5 * u, this.size.height - h), Size(3.6f * u, h), CornerRadius(1.2f * u))
        }
    }
}
